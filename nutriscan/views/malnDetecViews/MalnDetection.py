import boto3
import uuid
from io import BytesIO
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
from django.utils import timezone

from decimal import Decimal

# Función auxiliar para calcular el IMC
def calcular_imc(peso, talla_cm):
    if not peso or not talla_cm:
        return None
    try:
        talla_m = float(talla_cm) / 100.0
        imc = float(peso) / (talla_m ** 2)
        return round(imc, 2)
    except (ZeroDivisionError, ValueError):
        return None

# Clasificación del IMC según referencias generales (puedes ajustar según OMS por edad)
def clasificar_imc(imc):
    if imc < 14:
        return "Desnutrición"
    elif imc < 16:
        return "Riesgo"
    else:
        return "Normal"

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
        
        # Crear una copia de la imagen en memoria para pasar a `predict_image`
        image_copy = BytesIO(image.read())
        image.seek(0)  # Reiniciar el stream del archivo original para que esté listo para la carga

        """ detection_result = predict_image(image_copy)

        if detection_result is None:
            return Response({"error": "No se pudo procesar la imagen con el modelo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        result_map = {
            'N_DESNUTRIDO': 'Con desnutrición',
            'N_NORMAL': 'Normal',
            'N_RIESGO_DESNUTRIDO': 'Riesgo en desnutricion'
        }
        readable_result = result_map.get(detection_result, "desconocido") """
        prediction = predict_image(image_copy)
        if prediction is None:
            return Response({"error": "No se pudo procesar la imagen con el modelo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        predicted_label = prediction["label"]
        confidence = prediction["confidence"]

        result_map = {
            'N_DESNUTRIDO': 'Con desnutrición',
            'N_NORMAL': 'Normal',
            'N_RIESGO_DESNUTRIDO': 'Riesgo en desnutrición'
        }
        readable_result = result_map.get(predicted_label, "Desconocido")

        

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
            s3_client.upload_fileobj(image, s3_bucket_name, s3_file_name)
            
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
            confidence=confidence,  # ← Guardamos la precisión
            expirationDate = timezone.localtime(timezone.now() + timedelta(hours=1)),  # Establecer la nueva fecha de expiración
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
            imc = calcular_imc(weight, height)
            if imc:
                imc_category = clasificar_imc(imc)

        # Devolver el resultado de la detección y la recomendación
        return Response({
            "detectionResult": readable_result,
            "confidence": confidence,
            "immediateRecommendation": immediate_recommendation,
            "imc": imc,
            "imcCategory": imc_category
        }, status=status.HTTP_201_CREATED)
