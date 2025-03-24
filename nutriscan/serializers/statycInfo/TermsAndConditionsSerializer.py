# serializers.py
from rest_framework import serializers
from ...models import TermsAndConditions

class TermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditions
        fields = ['id', 'content', 'date_created', 'date_modified']