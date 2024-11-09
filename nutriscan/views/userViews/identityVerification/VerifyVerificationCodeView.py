from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ....models import VerificationCode, AditionalInfoUser

class VerifyVerificationCodeView(APIView):
    http_method_names = ['post']  # Solo permite POST
    def post(self, request):
        phone_number = request.data.get('phone')
        code = request.data.get('code')

        if not phone_number or not code:
            return Response({"error": "Número de teléfono y código son requeridos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_info = AditionalInfoUser.objects.get(userPhone=phone_number)
        except AditionalInfoUser.DoesNotExist:
            return Response({"error": "Número de teléfono no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        try:
            verification = VerificationCode.objects.get(user=user_info.user, code=code)
        except VerificationCode.DoesNotExist:
            return Response({"error": "Código de verificación incorrecto"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el código ha expirado
        if verification.expiration < timezone.now():
            return Response({"error": "El código de verificación ha expirado. Solicita un nuevo código."}, status=status.HTTP_400_BAD_REQUEST)

        # Si el código es válido y no ha expirado
        return Response({"message": "Código de verificación correcto"}, status=status.HTTP_200_OK)
