from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import PasswordResetCode, AditionalInfoUser

class VerifyPasswordResetCodeView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get("code")
        
        # Verificar que el usuario existe por el número de teléfono
        try:
            user_info = AditionalInfoUser.objects.get(userPhone=phone)
            user = user_info.user
        except AditionalInfoUser.DoesNotExist:
            return Response({"error": "Número de teléfono no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Verificar si el código es válido y no ha expirado
        try:
            reset_code = PasswordResetCode.objects.get(user=user, code=code)
            if reset_code.expiration < timezone.now():
                return Response({"error": "El código ha expirado. Solicita uno nuevo."}, status=status.HTTP_400_BAD_REQUEST)
        except PasswordResetCode.DoesNotExist:
            return Response({"error": "Código no válido."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Si todo está correcto, permitir cambiar la contraseña
        return Response({"message": "Código verificado. Ahora puedes cambiar tu contraseña."}, status=status.HTTP_200_OK)
