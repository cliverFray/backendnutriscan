import random
import boto3
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import AditionalInfoUser, PasswordResetCode

class ResendPasswordResetCodeView(APIView):
    def post(self, request):
        phone = request.data.get("phone")

        # Verificar que el número de teléfono existe
        try:
            user_info = AditionalInfoUser.objects.get(userPhone=phone)
            user = user_info.user
        except AditionalInfoUser.DoesNotExist:
            return Response({"error": "Número de teléfono no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Generar un nuevo código de restablecimiento y actualizar o crear el registro
        reset_code = str(random.randint(100000, 999999))
        expiration_time = timezone.now() + timezone.timedelta(minutes=10)

        # Eliminar el código anterior si existe y crear uno nuevo
        PasswordResetCode.objects.filter(user=user).delete()
        PasswordResetCode.objects.create(user=user, code=reset_code, expiration=expiration_time)

        # Enviar el código por SMS usando Amazon SNS
        sns_client = boto3.client(
            'sns',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        message = f"Su nuevo código de restablecimiento de contraseña es: {reset_code}"
        try:
            sns_client.publish(
                PhoneNumber=f"+51{phone}",  # Cambia el prefijo según el país
                Message=message
            )
            return Response({"message": "Nuevo código de restablecimiento de contraseña enviado exitosamente."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error en el envío de SMS: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
