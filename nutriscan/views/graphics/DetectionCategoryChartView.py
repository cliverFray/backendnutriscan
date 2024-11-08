
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from ...models import Child, MalnutritionDetection




class DetectionCategoryChartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        user = request.user
        # Verificar que el niño pertenece al usuario autenticado
        try:
            child = Child.objects.get(pk=child_id, user=user)
        except Child.DoesNotExist:
            return Response({"error": "El niño no pertenece al usuario autenticado o no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la cantidad de detecciones por categoría para el niño
        category_counts = (
            MalnutritionDetection.objects
            .filter(child=child)
            .values("detectionResult")
            .annotate(count=Count("detectionResult"))
        )

        # Formatear los datos para el gráfico circular
        chart_data = {item["detectionResult"]: item["count"] for item in category_counts}

        return Response(chart_data, status=status.HTTP_200_OK)