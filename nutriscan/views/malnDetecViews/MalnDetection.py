import boto3
import uuid
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Child, MalnutritionDetection, GrowthHistory
from rest_framework.permissions import IsAuthenticated
from cnnmodel.modelHandler import predict_image_from_url
from cnnmodel.modelHandler import predict_image
from ...utils.recommendationGenerator import RecommendationGenerator
from datetime import datetime, timedelta

class UploadDetectionImageView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']  # Solo permite POST

    def generate_presigned_url(self, s3_client, bucket_name, object_name, expiration=3600):
        """Genera una URL firmada"""
        try:
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            return None

    def post(self, request, child_id):
        user = request.user

        # Verificar que el niño pertenece al usuario
        try:
            child = Child.objects.get(pk=child_id, user=user)
        except Child.DoesNotExist:
            return Response({"error": "El niño no pertenece al usuario autenticado o no existe."}, status=status.HTTP_404_NOT_FOUND)

        
        image = request.FILES.get('image')
        if not image:
            return Response({"error": "El archivo de imagen es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        detection_result = predict_image(image)

        if detection_result is None:
            return Response({"error": "No se pudo procesar la imagen con el modelo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        result_map = {
            'N_DESNUTRIDO': 'Con desnutrición',
            'N_NORMAL': 'Normal',
            'N_RIESGO_DESNUTRIDO': 'Riesgo en desnutricion'
        }
        readable_result = result_map.get(detection_result, "desconocido")
        

        s3_client = boto3.client(
            's3',  
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        s3_bucket_name = settings.AWS_S3_BUCKET_NAME
        
        # Generar un nombre único para el archivo
        unique_id = uuid.uuid4().hex
        file_extension = image.name.split('.')[-1]
        s3_file_name = f"{child.childId}/detections/{unique_id}.{file_extension}"

        try:
            s3_client.upload_fileobj(image.file, s3_bucket_name, s3_file_name)
            
        except Exception as e:
            return Response({"error": f"Error al subir la imagen: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Genera el url firmada
        image_url = self.generate_presigned_url(s3_client, s3_bucket_name, s3_file_name, expiration=3600)

        if not image_url:
            return Response({"error": "No se pudo generar la URL firmada para la imagen."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Guarda el resultado de la detección en la base de datos

        detection = MalnutritionDetection.objects.create(
            detectionImageUrl=image_url,
            detectionResult=readable_result,
            expirationDate = datetime.now() + timedelta(hours=1),  # Establecer la nueva fecha de expiración
            child=child
        )

        # Generar el nombre legible y la recomendación
        
        immediate_recommendation = RecommendationGenerator.generate_recommendation(detection)

        # Recuperar peso y altura desde el modelo Child si existen y no son nulos
        weight = child.childCurrentWeight
        height = child.childCurrentHeight

        # Registrar peso y altura en GrowthHistory si están presentes
        if weight is not None and height is not None:
            GrowthHistory.objects.create(
                child=child,
                weight=weight,
                height=height
            )

        # Devolver el resultado de la detección y la recomendación
        return Response({
            "detectionResult": readable_result,
            "immediateRecommendation": immediate_recommendation
        }, status=status.HTTP_201_CREATED)
