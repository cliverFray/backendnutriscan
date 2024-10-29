from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ...models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'userFirstName', 'userLastName', 'userEmail', 'userPassword', 'userDNI', 'userPhone', 'UserPlace']
        extra_kwargs = {
            'userPassword': {'write_only': True}
        }
    def create(self, validated_data):
        # Encriptar la contraseña
        validated_data['userPassword'] = make_password(validated_data['userPassword'])
        return super(UserRegisterSerializer, self).create(validated_data)
