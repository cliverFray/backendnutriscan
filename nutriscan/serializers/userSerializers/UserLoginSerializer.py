from rest_framework import serializers
#from django.contrib.auth.hashers import check_password
#from ...models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userFirstName', 'userLastName', 'userEmail', 'userPhone', 'userPassword', 'userPlace')
        extra_kwargs = {'userPassword': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            userFirstName=validated_data['userFirstName'],
            userLastName=validated_data['userLastName'],
            userEmail=validated_data['userEmail'],
            userPhone=validated_data['userPhone'],
            userPlace=validated_data['userPlace']
        )
        user.set_password(validated_data['userPassword'])  # Hashea la contraseña
        user.save()
        return user