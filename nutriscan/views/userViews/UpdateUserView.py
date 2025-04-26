from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from ...models import AditionalInfoUser
from ...serializers.userSerializers.UserRegisterSerializer import UserRegisterSerializer, AditionalInfoUserSerializer
from rest_framework.exceptions import ValidationError

class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']  # Solo permite PUT para actualizar datos

    def put(self, request):
        user = request.user  # Usuario autenticado
        user_data = request.data.get('user', {})
        additional_info_data = request.data.get('additional_info', {})

        # Validaciones manuales para campos requeridos (excepto contraseña)
        required_user_fields = ['first_name', 'last_name', 'email']
        required_additional_fields = ['userDNI', 'userPlace']

        for field in required_user_fields:
            if field not in user_data or not user_data[field].strip():
                return Response({"error": f"El campo {field} es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        for field in required_additional_fields:
            if field not in additional_info_data or not additional_info_data[field].strip():
                return Response({"error": f"El campo {field} es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar si el nuevo correo ya existe (y no es el mismo usuario)
        if 'email' in user_data:
            if User.objects.filter(email=user_data['email']).exclude(id=user.id).exists():
                return Response({"email": "Esta dirección de correo ya se encuentra en uso."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar si el nuevo DNI ya existe
        if 'userDNI' in additional_info_data:
            if AditionalInfoUser.objects.filter(userDNI=additional_info_data['userDNI']).exclude(user=user).exists():
                return Response({"userDNI": "El número de DNI ya se encuentra en uso."}, status=status.HTTP_400_BAD_REQUEST)

        additional_info = AditionalInfoUser.objects.get(user=user)

        user_serializer = UserRegisterSerializer(user, data=user_data, partial=True)
        additional_info_serializer = AditionalInfoUserSerializer(additional_info, data=additional_info_data, partial=True)

        if user_serializer.is_valid() and additional_info_serializer.is_valid():
            with transaction.atomic():
                user_serializer.save()
                additional_info_serializer.save()
            return Response({"message": "Usuario actualizado exitosamente."}, status=status.HTTP_200_OK)

        errors = {
            "user_errors": user_serializer.errors,
            "additional_info_errors": additional_info_serializer.errors
        }
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
