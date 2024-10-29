# serializers.py

from rest_framework import serializers
from ...models import MalnutritionDetection

class MalnutritionDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MalnutritionDetection
        fields = '__all__'
