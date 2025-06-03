import boto3
import random
import logging
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from ....models import VerificationCode, AditionalInfoUser
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

from ....utils.SendotpByEmail import send_OTP_email

class GenerateAndSendVerificationCodeView(APIView):
    http_method_names = ['post']

    def post(self, request):
        phone_number = request.data.get('phone')
        dni = request.data.get('dni')
        email = request.data.get('email')

        user = User(
            username=email,  # Usamos email como username
            email=email,
            first_name="",  # Opcional
        )
        
        if not phone_number:
            return Response({
                "codigo": "telefono_requerido",
                "mensaje": _("Número de teléfono es requerido")
            }, status=status.HTTP_400_BAD_REQUEST)

        if not phone_number.isdigit() or len(phone_number) != 9:
            return Response({
                "codigo": "telefono_invalido",
                "mensaje": _("El número de teléfono debe contener 9 dígitos.")
            }, status=status.HTTP_400_BAD_REQUEST)

        if AditionalInfoUser.objects.filter(userPhone=phone_number).exists():
            return Response({
                "codigo": "telefono_registrado",
                "mensaje": _("El número de teléfono ya está registrado.")
            }, status=status.HTTP_400_BAD_REQUEST)

        if AditionalInfoUser.objects.filter(userDNI=dni).exists():
            return Response({
                "codigo": "dni_registrado",
                "mensaje": _("El DNI ya está registrado.")
            }, status=status.HTTP_400_BAD_REQUEST)
        

        # Revisa si el correo ya está registrado
        if User.objects.filter(email=email).exists():
            return Response({
                "codigo": "correo_registrado",
                "mensaje": _("El correo ya está registrado.")
            }, status=status.HTTP_400_BAD_REQUEST)
        
        verification_code = str(random.randint(100000, 999999))

        # Intentar ambos envíos y registrar estado
        sms_sent = False
        email_sent = False
        sms_error = ""
        email_error = ""

        # Envío SMS
        try:
            sns_client = boto3.client(
                'sns',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            response = sns_client.publish(
                PhoneNumber=f"+51{phone_number}",
                Message=f"Tu código de verificación de NutriScan es {verification_code}. Expira en 10 minutos"
            )
            if response.get('MessageId'):
                sms_sent = True
            else:
                sms_error = _("No se pudo enviar el código por SMS.")
        except Exception as e:
            logger.error(f"Error al enviar SMS: {str(e)}")
            sms_error = _("No se pudo enviar el código por SMS.")

        # Envío Correo
        try:
            email_response = send_OTP_email(user, verification_code)
            if email_response.get('MessageId'):
                email_sent = True
            else:
                email_error = _("No se pudo enviar el correo electrónico.")
        except Exception as e:
            logger.error(f"Error al enviar correo: {str(e)}")
            email_error = _("No se pudo enviar el correo electrónico.")

        # Solo guardamos el código si al menos uno fue enviado
        if sms_sent or email_sent:
            expiration_time = timezone.now() + timedelta(minutes=10)
            VerificationCode.objects.create(
                phone=phone_number,
                code=verification_code,
                expiration=expiration_time,
                created_at=timezone.now()
            )
            return Response({
                "codigo": "parcial" if not (sms_sent and email_sent) else "exito",
                "mensaje": _("Código enviado con éxito.") if sms_sent and email_sent else _("Hubo problemas en algunos envíos."),
                "sms_enviado": sms_sent,
                "correo_enviado": email_sent,
                "sms_error": sms_error,
                "correo_error": email_error
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "codigo": "error_envio_ambos",
                "mensaje": _("No se pudo enviar el código ni por SMS ni por correo."),
                "sms_error": sms_error,
                "correo_error": email_error
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
