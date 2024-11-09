from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete']  # Solo permite DELETE

    def delete(self, request):
        user = request.user
        password = request.data.get('password')  # Obtener la contraseña proporcionada por el usuario

        # Verificar la contraseña
        if not authenticate(username=user.username, password=password):
            return Response({"error": "La contraseña es incorrecta"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                user.delete()  # Eliminar el usuario y sus datos relacionados
            return Response({"message": "Cuenta eliminada exitosamente"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": "Error al eliminar la cuenta. Intente nuevamente más tarde."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
