import boto3
import random
from datetime import timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ....models import VerificationCode, AditionalInfoUser
from django.utils.translation import gettext_lazy as _

class ResendVerificationCodeView(APIView):
    http_method_names = ['post']  # Solo permite POST

    def post(self, request):
        phone_number = request.data.get('phone')
        
        if not phone_number:
            return Response({
                "codigo": "telefono_requerido",
                "mensaje": _("Número de teléfono es requerido")
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el número de teléfono existe en AditionalInfoUser
        try:
            user_info = AditionalInfoUser.objects.get(userPhone=phone_number)
        except AditionalInfoUser.DoesNotExist:
            return Response({
                "codigo": "telefono_no_encontrado",
                "mensaje": _("Número de teléfono no encontrado")
            }, status=status.HTTP_404_NOT_FOUND)

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
                PhoneNumber=f"+51{phone_number}",  # Ajustar el código de país si es necesario
                Message=f"Tu nuevo código de verificación de NutriScan es {verification_code}. Expira en 10 minutos"
            )
        except Exception as e:
            return Response({
                "codigo": "error_envio_sms",
                "mensaje": _("Error al enviar SMS. Por favor intenta de nuevo.")
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Guardar el nuevo código en la base de datos con expiración de 10 minutos
        expiration_time = timezone.now() + timedelta(minutes=10)
        VerificationCode.objects.create(
            phone=phone_number,
            code=verification_code,
            expiration=expiration_time,
            created_at=timezone.now()
        )

        return Response({
            "codigo": "exito",
            "mensaje": _("Nuevo código de verificación enviado correctamente")
        }, status=status.HTTP_200_OK)
