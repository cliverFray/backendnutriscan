from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from ...models import MalnutritionDetection
import boto3
from django.conf import settings

class GenerateNewPresignedUrlView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def generate_presigned_url(self, s3_client, bucket_name, object_name, expiration=3600):
        """Genera una URL firmada para acceder al archivo S3"""
        try:
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            return None

    def get(self, request, detection_id):
        user = request.user
        try:
            # Buscar la detección específica por ID
            detection = MalnutritionDetection.objects.get(id=detection_id, child__user=user)

            # Verificar si la URL firmada ha expirado
            if detection.expirationDate and datetime.now() > detection.expirationDate:
                # Si ha expirado, generar una nueva URL firmada
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_REGION
                )
                new_image_url = self.generate_presigned_url(s3_client, settings.AWS_S3_BUCKET_NAME, detection.detectionImageUrl.split('/')[-1])

                if new_image_url:
                    # Actualizar la URL y la fecha de expiración en el modelo
                    detection.detectionImageUrl = new_image_url
                    detection.expirationDate = datetime.now() + timedelta(hours=1)  # Establecer la nueva fecha de expiración
                    detection.save()
                    return Response({"newImageUrl": new_image_url}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "No se pudo generar una nueva URL firmada."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Si no ha expirado, devolver la URL actual
            return Response({"imageUrl": detection.detectionImageUrl}, status=status.HTTP_200_OK)

        except MalnutritionDetection.DoesNotExist:
            return Response({"error": "No se encontró la detección."}, status=status.HTTP_404_NOT_FOUND)
