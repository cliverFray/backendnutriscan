import boto3
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Child, MalnutritionDetection, GrowthHistory
from ...serializers.malnDetecSerializers.MalnutritionDetectionSerializer import MalnutritionDetectionSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from decimal import Decimal  # Importar Decimal aquí

from cnnmodel.modelHandler import predict_image_from_url

class UploadDetectionImageView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']  # Solo permite POST

    def post(self, request, child_id):
        user = request.user
        
        # Verificar que el niño pertenece al usuario
        try:
            child = Child.objects.get(pk=child_id, user=user)
        except Child.DoesNotExist:
            return Response({"error": "El niño no pertenece al usuario autenticado o no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Sube la imagen a S3
        image = request.FILES.get('image')
        if not image:
            return Response({"error": "El archivo de imagen es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        s3_client = boto3.client(
            'sns',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        s3_bucket_name = settings.AWS_S3_BUCKET_NAME
        s3_file_name = f"{child.childId}/detections/{image.name}"

        try:
            s3_client.upload_fileobj(image, s3_bucket_name, s3_file_name)
            image_url = f"https://{s3_bucket_name}.s3.amazonaws.com/{s3_file_name}"
        except Exception as e:
            return Response({"error": f"Error al subir la imagen: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Ejecuta el modelo de detección con la URL de la imagen
        detection_result = predict_image_from_url(image_url)

        if detection_result is None:
            return Response({"error": "No se pudo procesar la imagen con el modelo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Guarda el resultado de la detección en la base de datos
        detection = MalnutritionDetection.objects.create(
            detectionImageUrl=image_url,
            detectionResult=detection_result,
            child=child
        )

        # Registrar peso y altura en GrowthHistory si están presentes
        weight = request.data.get("weight")
        height = request.data.get("height")
        if weight and height:
            GrowthHistory.objects.create(
                child=child,
                weight=Decimal(weight),
                height=Decimal(height)
            )

        serializer = MalnutritionDetectionSerializer(detection)
        return Response(serializer.data, status=status.HTTP_201_CREATED)