from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ....models import VerificationCode

class VerifyCodeView(APIView):
    http_method_names = ['post']  # Solo permite POST

    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get("code")
        
        # Verificar que el código exista para el número de teléfono proporcionado y no haya expirado
        try:
            verification_code = VerificationCode.objects.filter(phone=phone, code=code).order_by('-created_at').first()
            if not verification_code:
                return Response({"error": "Código no válido."}, status=status.HTTP_400_BAD_REQUEST)

            if timezone.now() > verification_code.expiration:
                return Response({"error": "El código ha expirado."}, status=status.HTTP_400_BAD_REQUEST)

        except VerificationCode.DoesNotExist:
            return Response({"error": "Código no válido."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Código verificado correctamente."}, status=status.HTTP_200_OK)
