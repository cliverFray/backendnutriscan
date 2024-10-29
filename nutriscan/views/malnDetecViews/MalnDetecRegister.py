# views.py

from rest_framework import generics
from ...models import MalnutritionDetection
from nutriscan.serializers import MalnutritionDetectionSerializer
from rest_framework.permissions import IsAuthenticated

# Vista para insertar detección de desnutrición
class MalnutritionDetectionCreateView(generics.CreateAPIView):
    queryset = MalnutritionDetection.objects.all()
    serializer_class = MalnutritionDetectionSerializer
    permission_classes = [IsAuthenticated]  # Requiere que el usuario esté autenticado

    def perform_create(self, serializer):
        serializer.save()
