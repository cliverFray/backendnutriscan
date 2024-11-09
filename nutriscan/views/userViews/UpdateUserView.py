from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db import transaction
from ...models import AditionalInfoUser
from ...serializers.userSerializers.UserRegisterSerializer import UserRegisterSerializer, AditionalInfoUserSerializer

class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']  # Solo permite PUT para actualizar datos

    def put(self, request):
        user = request.user  # Usuario autenticado
        user_data = request.data.get('user', {})
        additional_info_data = request.data.get('additional_info', {})

        # Serializar y validar los datos del usuario principal
        user_serializer = UserRegisterSerializer(user, data=user_data, partial=True)
        additional_info = AditionalInfoUser.objects.get(user=user)
        additional_info_serializer = AditionalInfoUserSerializer(additional_info, data=additional_info_data, partial=True)

        if user_serializer.is_valid() and additional_info_serializer.is_valid():
            with transaction.atomic():  # Garantizar que ambas operaciones se realicen en conjunto
                user_serializer.save()
                additional_info_serializer.save()
            return Response({"message": "Usuario actualizado exitosamente."}, status=status.HTTP_200_OK)
        
        # Si alguna de las serializaciones no es válida, devolver los errores
        errors = {
            "user_errors": user_serializer.errors,
            "additional_info_errors": additional_info_serializer.errors
        }
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
