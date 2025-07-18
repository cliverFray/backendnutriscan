from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ...models import Child, MalnutritionDetection
from datetime import datetime, timedelta
from django.utils import timezone
from ...serializers.malnDetecSerializers.MalnutritionDetectionSerializer import MalnutritionDetectionSerializer
import boto3

from django.conf import settings
from urllib.parse import urlparse


class DetectionHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']  # Solo permite GET

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

    def get_object_name_from_url(self, url):
        parsed_url = urlparse(url)
        object_key = parsed_url.path.lstrip('/')  # Elimina la barra inicial
        return object_key

    def get(self, request):
        user = request.user
        detections = MalnutritionDetection.objects.filter(child__user=user).select_related('child', 'immediate_recommendation')

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        # Serializar las detecciones con los datos necesarios
        serialized_data = []
        for detection in detections:
            # Verificar si la URL firmada ha expirado
            if detection.expirationDate:
                if detection.expirationDate.tzinfo is None:  # Si es naive, hacerla "aware"
                    detection.expirationDate = timezone.make_aware(detection.expirationDate, timezone.get_current_timezone())

                if timezone.now() > detection.expirationDate:
                    object_name = self.get_object_name_from_url(detection.detectionImageUrl)
                    new_image_url = self.generate_presigned_url(s3_client, settings.AWS_S3_BUCKET_NAME, object_name)

                    if new_image_url:
                        detection.detectionImageUrl = new_image_url
                        detection.expirationDate = timezone.localtime(timezone.now() + timedelta(hours=1))
                        detection.save()

            # Agregar los datos al resultado
            serialized_data.append({
                "detectionId": detection.detectionId,
                "detectionDate": detection.detectionDate,
                "detectionResult": detection.detectionResult,
                "detectionImageUrl": detection.detectionImageUrl,
                "childId": detection.child.childId,
                "childName": detection.child.childName,
                "confidence": str(detection.confidence) if detection.confidence is not None else None,
                "immediateRecommendation": detection.immediate_recommendation.inmediateRecomMessage if hasattr(detection, "immediate_recommendation") and detection.immediate_recommendation else None,
            })

        return Response(serialized_data, status=status.HTTP_200_OK)
