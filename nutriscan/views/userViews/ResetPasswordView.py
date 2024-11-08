from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import PasswordResetCode, AditionalInfoUser

class ResetPasswordView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        code = request.data.get("code")
        new_password = request.data.get("new_password")

        try:
            user_info = AditionalInfoUser.objects.get(userPhone=phone)
            user = user_info.user
        except AditionalInfoUser.DoesNotExist:
            return Response({"error": "Numero de telefono no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Verificar el código
        try:
            reset_code = PasswordResetCode.objects.get(user=user, code=code)
        except PasswordResetCode.DoesNotExist:
            return Response({"error": "Codigo no valido."}, status=status.HTTP_400_BAD_REQUEST)

        # Cambiar la contraseña del usuario
        user.password = make_password(new_password)
        user.save()

        # Eliminar el código de restablecimiento
        reset_code.delete()

        return Response({"message": "Cotraseña cambiada correctamente."}, status=status.HTTP_200_OK)
