from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from nutriscan.models import AditionalInfoUser
#from nutriscan.serializers.userSerializers import UserRegisterSerializer

from ...serializers.userSerializers.UserRegisterSerializer import UserRegisterSerializer, AditionalInfoUserSerializer

from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

class UserRegisterView(APIView):
    http_method_names = ['post']  # Solo permite POST
    def post(self, request):
        user_data = request.data.get('user')
        aditional_info_data = {
            'userDNI': request.data.get('userDNI'),
            'userPhone': request.data.get('userPhone'),
            'userPlace': request.data.get('userPlace')
        }

        # Revisa si el DNI ya existe en la base de datos
        if AditionalInfoUser.objects.filter(userDNI=aditional_info_data['userDNI']).exists():
            raise ValidationError({"userDNI": "Este DNI ya existe en el sistema."})

        if AditionalInfoUser.objects.filter(userPhone=aditional_info_data['userPhone']).exists():
            raise ValidationError({"userPhone": "Este número de teléfono ya existe en el sistema."})

        user_serializer = UserRegisterSerializer(data=user_data)
        if user_serializer.is_valid():
            try:
                validated_user_data = user_serializer.validated_data
                user = User.objects.create_user(
                    username=validated_user_data['username'],
                    first_name=validated_user_data['first_name'],
                    last_name=validated_user_data['last_name'],
                    email=validated_user_data['email'],
                    password=validated_user_data['password']
                )

                # Crea el serializer sin incluir el campo `user` en los datos iniciales
                aditional_info_serializer = AditionalInfoUserSerializer(data=aditional_info_data)
                if aditional_info_serializer.is_valid():
                    # Guarda la información adicional y asocia la instancia de `user`
                    aditional_info_serializer.save(user=user)
                    return Response({"message": "Usuario registrado exitosamente."}, status=status.HTTP_201_CREATED)
                else:
                    user.delete()  # Elimina el usuario si falla la creación de información adicional
                    return Response(aditional_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError:
                return Response({"error": "Error de integridad, el DNI o teléfono ya existe."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)