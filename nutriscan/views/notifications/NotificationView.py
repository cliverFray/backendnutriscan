from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ...models import Notification
from ...serializers.notifications.NotificationSerializer import NotificationSerializer
from django.utils import timezone

class NotificationView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']  # Solo permite GET y POST

    def get(self, request):
        """Listar notificaciones del usuario autenticado"""
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Crear una nueva notificación manualmente (opcional)"""
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
