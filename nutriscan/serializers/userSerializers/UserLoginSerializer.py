from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from ...models import User

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(userEmail=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuario no encontrado")

        if not check_password(data['password'], user.userPassword):
            raise serializers.ValidationError("Contraseña incorrecta")

        return {
            "userId": user.userId,
            "userFirstName": user.userFirstName,
            "userLastName": user.userLastName,
            "email": user.userEmail,
        }
