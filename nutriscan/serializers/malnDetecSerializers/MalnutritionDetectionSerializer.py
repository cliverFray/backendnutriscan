from rest_framework import serializers
from ...models import MalnutritionDetection

class MalnutritionDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MalnutritionDetection
        fields = ['detectionId', 'detectionDate', 'detectionResult', 'detectionImageUrl', 'child']
        read_only_fields = ['detectionDate', 'detectionResult']  # `detectionDate` y `detectionResult` solo se generan después de la predicción
