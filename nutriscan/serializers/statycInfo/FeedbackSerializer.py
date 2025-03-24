from rest_framework import serializers
from ...models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'message', 'date_created', 'date_modified']
        read_only_fields = ['id', 'date_created', 'date_modified']
