# serializers.py

from rest_framework import serializers
from ...models import NutritionalTerm

class NutritionalTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionalTerm
        fields = ['name', 'description', 'examples', 'image_url']
