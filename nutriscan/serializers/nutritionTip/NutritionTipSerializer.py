from rest_framework import serializers
from ...models import NutritionTip

class NutritionTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionTip
        fields = ['id', 'title', 'description', 'calories', 'portion_size', 'image_url', 'date_created','tipo']
