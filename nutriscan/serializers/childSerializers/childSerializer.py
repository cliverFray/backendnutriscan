from rest_framework import serializers
from ...models import Child

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = [
            'childId', 
            'childName', 
            'childLastName', 
            'childAgeMonth', 
            'childGender', 
            'childCurrentWeight', 
            'childCurrentHeight', 
            'childBirthDate',  # Nuevo campo
            'user'
        ]
        read_only_fields = ['childId', 'user']  # childId y user son solo de lectura
