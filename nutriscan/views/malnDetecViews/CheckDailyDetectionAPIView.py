# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from ...models import MalnutritionDetection, Child
from rest_framework.permissions import IsAuthenticated

class CheckDailyDetectionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']  # Solo permite GET

    def get(self, request, child_id):
        user = request.user

        # Verificar que el niño pertenece al usuario autenticado
        try:
            child = Child.objects.get(pk=child_id, user=user)
        except Child.DoesNotExist:
            return Response({"error": "El niño no existe o no pertenece al usuario."}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.localdate()  # Fecha local actual (timezone-aware)
        exists = MalnutritionDetection.objects.filter(child=child, detectionDate=today).exists()

        return Response({
            "exists": exists,
            "message": "Ya existe una detección para este niño hoy." if exists else "No hay detección registrada hoy para este niño."
        }, status=status.HTTP_200_OK)
