import random
import boto3
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import AditionalInfoUser, PasswordResetCode

class RequestPasswordResetView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        
        # Buscar usuario por teléfono
        try:
            user_info = AditionalInfoUser.objects.get(userPhone=phone)
            user = user_info.user
        except AditionalInfoUser.DoesNotExist:
            return Response({"error": "Número de teléfono no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Generar un código de 6 dígitos
        reset_code = str(random.randint(100000, 999999))
        
        # Configurar tiempo de expiración (10 minutos)
        expiration_time = timezone.now() + timedelta(minutes=10)
        
        # Eliminar códigos anteriores y crear uno nuevo con tiempo de expiración
        PasswordResetCode.objects.filter(user=user).delete()
        PasswordResetCode.objects.create(user=user, code=reset_code, expiration=expiration_time)

        # Enviar el código por SMS usando Amazon SNS
        sns_client = boto3.client(
            'sns',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        message = f"Su código de restablecimiento de contraseña es: {reset_code}. Expira en 10 minutos."
        try:
            sns_client.publish(
                PhoneNumber=f"+51{phone}",  # Cambia el prefijo según el país
                Message=message
            )
            return Response({"message": "Código de restablecimiento de contraseña enviado exitosamente."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error en el envío de SMS: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)