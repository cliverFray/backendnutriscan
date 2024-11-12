from rest_framework import serializers
from ...models import Child

class ChildNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ['childId', 'childName']  # Incluye tanto el ID como el nombre
