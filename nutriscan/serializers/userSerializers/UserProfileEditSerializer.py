from django.contrib.auth.models import User
from rest_framework import serializers
from ...models import AditionalInfoUser

class UserDataSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class AditionalInfoUserDataSerializer(serializers.ModelSerializer):
    user = UserDataSerializer(required=False)

    class Meta:
        model = AditionalInfoUser
        fields = ['user', 'userDNI', 'userPhone', 'userPlace','is_confirmed']
        read_only_fields = ['is_confirmed']  #Añade esta línea
