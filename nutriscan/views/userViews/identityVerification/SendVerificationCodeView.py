import boto3
import random
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ....models import VerificationCode, AditionalInfoUser
from django.contrib.auth.models import User

class SendVerificationCodeView(APIView):
    def post(self, request):
        # Obtener el número de teléfono del usuario
        phone_number = request.data.get('phone')
        if not phone_number:
            return Response({"error": "Número de teléfono es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_info = AditionalInfoUser.objects.get(userPhone=phone_number)
        except AditionalInfoUser.DoesNotExist:
            return Response({"error": "Número de teléfono no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Generar un código de 6 dígitos
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
                PhoneNumber=f"+51{phone_number}",  # Incluye el código de país, por ejemplo: +51 para Perú
                Message=f"Tu código de verificación es {verification_code}"
            )
        except Exception as e:
            return Response({"error": f"Error al enviar SMS: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Guardar el código en la base de datos con expiración de 10 minutos
        expiration_time = timezone.now() + timedelta(minutes=10)
        VerificationCode.objects.update_or_create(
            user=user_info.user,
            defaults={'code': verification_code, 'expiration': expiration_time}
        )

        return Response({"message": "Código de verificación enviado correctamente"}, status=status.HTTP_200_OK)
