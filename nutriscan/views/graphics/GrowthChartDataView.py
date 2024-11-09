from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ...models import GrowthHistory, Child
from django.shortcuts import get_object_or_404

class GrowthChartDataView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']  # Solo permite GET
    def get(self, request, child_id):
        user = request.user
        # Verificar que el niño pertenece al usuario autenticado
        child = get_object_or_404(Child, pk=child_id, user=user)

        # Obtener datos de historial de crecimiento para el niño
        growth_data = GrowthHistory.objects.filter(child=child).order_by("date_recorded")

        # Formatear datos para el gráfico
        chart_data = {
            "dates": [record.date_recorded.strftime("%Y-%m-%d") for record in growth_data],
            "weights": [float(record.weight) for record in growth_data],
            "heights": [float(record.height) for record in growth_data],
        }

        return Response(chart_data, status=status.HTTP_200_OK)
