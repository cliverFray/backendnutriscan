from rest_framework import serializers
from ...models import AppInfo,Feedback

class AppInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppInfo
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'message', 'date_created', 'date_modified']