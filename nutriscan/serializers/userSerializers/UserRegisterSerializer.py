from django.contrib.auth.models import User
from rest_framework import serializers
from ...models import AditionalInfoUser

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password','date_joined']
        extra_kwargs = {
            'username': {
                'error_messages': {
                    'unique': 'Ya existe un usuario registrado con el numero celular brindado. Por ingrese otro numero de celular.'
                }
            },
            'password': {
                'write_only': True
            }
        }

class AditionalInfoUserSerializer(serializers.ModelSerializer):
    # Anidar el serializer de User para mostrar los datos del usuario
    user = UserRegisterSerializer(required=False)

    class Meta:
        model = AditionalInfoUser
        fields = ['user', 'userDNI', 'userPhone', 'userPlace']
