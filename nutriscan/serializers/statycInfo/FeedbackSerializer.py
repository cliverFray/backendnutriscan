from rest_framework import serializers
from ...models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'message', 'date_created', 'date_modified']