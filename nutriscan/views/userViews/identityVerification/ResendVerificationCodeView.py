import boto3
import random
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ....models import VerificationCode, AditionalInfoUser

class ResendVerificationCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone')
        
        if not phone_number:
            return Response({"error": "Número de teléfono es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_info = AditionalInfoUser.objects.get(userPhone=phone_number)
        except AditionalInfoUser.DoesNotExist:
            return Response({"error": "Número de teléfono no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Generar un nuevo código de 6 dígitos
        verification_code = str(random.randint(100000, 999999))

        # Configurar el cliente SNS de AWS
        sns_client = boto3.client(
            'sns',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        # Enviar el SMS con el código de verificación
        try:
            sns_client.publish(
                PhoneNumber=f"+{phone_number}",  # Incluye el código de país
                Message=f"Tu nuevo código de verificación es {verification_code}"
            )
        except Exception as e:
            return Response({"error": f"Error al enviar SMS: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Guardar el nuevo código en la base de datos con expiración de 10 minutos
        expiration_time = timezone.now() + timedelta(minutes=10)
        VerificationCode.objects.update_or_create(
            user=user_info.user,
            defaults={'code': verification_code, 'expiration': expiration_time}
        )

        return Response({"message": "Nuevo código de verificación enviado correctamente"}, status=status.HTTP_200_OK)
