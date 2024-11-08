from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ....models import VerificationCode, AditionalInfoUser
from django.contrib.auth.models import User
from ....views.userViews.SendWelcomeEmailView import SendWelcomeEmailView
from rest_framework.test import APIRequestFactory  # Import necesario para crear la solicitud

class VerifyCodeView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get("code")
        
        try:
            user_info = AditionalInfoUser.objects.get(userPhone=phone)
            user = user_info.user
        except AditionalInfoUser.DoesNotExist:
            return Response({"error": "Número de teléfono no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        try:
            verification_code = VerificationCode.objects.get(user=user, code=code)
            if timezone.now() > verification_code.expiration:
                return Response({"error": "El código ha expirado."}, status=status.HTTP_400_BAD_REQUEST)
        except VerificationCode.DoesNotExist:
            return Response({"error": "Código no válido."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Código verificado correctamente, enviar el correo de bienvenida
        factory = APIRequestFactory()
        welcome_email_data = {"user_id": user.id}
        welcome_email_request = factory.post('welcome-email/', welcome_email_data)

        # Llamar a la vista para enviar el correo de bienvenida
        welcome_email_view = SendWelcomeEmailView.as_view()
        welcome_email_response = welcome_email_view(welcome_email_request)

        if welcome_email_response.status_code == status.HTTP_200_OK:
            return Response({"message": "Código verificado y correo de bienvenida enviado."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Código verificado, pero hubo un error al enviar el correo de bienvenida."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
