from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ...models import AditionalInfoUser
from ...utils.ResendVerifyEmailSender import resend_verify_email_sender

class ResendVerificationEmailView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request):
        user = request.user

        try:
            aditional_info = AditionalInfoUser.objects.get(user=user)

            if aditional_info.is_confirmed:
                return Response({"message": "El correo ya ha sido confirmado."}, status=status.HTTP_200_OK)

            resend_verify_email_sender(user)  # Envía el correo al email actual del usuario

            return Response({"message": "Correo de verificación enviado correctamente."}, status=status.HTTP_200_OK)

        except AditionalInfoUser.DoesNotExist:
            return Response(
                {"error": "No se encontró información adicional del usuario."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Ocurrió un error al enviar el correo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )