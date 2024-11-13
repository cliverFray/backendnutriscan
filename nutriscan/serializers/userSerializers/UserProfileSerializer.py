from django.contrib.auth.models import User
from rest_framework import serializers
from ...models import AditionalInfoUser

class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    
    class Meta:
        model = AditionalInfoUser
        fields = ['first_name', 'last_name', 'userDNI', 'userPhone', 'userPlace']
