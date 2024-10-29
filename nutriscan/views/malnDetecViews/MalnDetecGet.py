# views.py
# views.py

from rest_framework import generics
from ...models import MalnutritionDetection
from nutriscan.serializers import MalnutritionDetectionSerializer
from rest_framework.permissions import IsAuthenticated
# Vista para leer detecciones de desnutrición
class MalnutritionDetectionListView(generics.ListAPIView):
    queryset = MalnutritionDetection.objects.all()
    serializer_class = MalnutritionDetectionSerializer
    permission_classes = [IsAuthenticated]

    # Filtrar por childId
    def get_queryset(self):
        child_id = self.request.query_params.get('childId', None)
        if child_id:
            return MalnutritionDetection.objects.filter(childId=child_id)
        return super().get_queryset()
