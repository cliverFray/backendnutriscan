from rest_framework import serializers
from ...models import Child

class ChildListSerializer(serializers.ModelSerializer):
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
            'childBirthDate'
        ]
        read_only_fields = ['childId']
