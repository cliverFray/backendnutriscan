from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ...models import GrowthHistory, Child
from django.shortcuts import get_object_or_404

class GrowthChartDataView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request, child_id):
        user = request.user
        try:
            child = Child.objects.get(pk=child_id, user=user)
        except Child.DoesNotExist:
            return Response({"error": "El niño no pertenece al usuario autenticado o no existe."}, status=status.HTTP_404_NOT_FOUND)

        growth_data = GrowthHistory.objects.filter(child=child).order_by("date_recorded")

        if not growth_data.exists():
            return Response(
                {"error": "No hay suficientes datos para generar el gráfico."},
                status=status.HTTP_204_NO_CONTENT
            )

        chart_data = {
            "dates": [record.date_recorded.strftime("%Y-%m-%d") for record in growth_data],
            "weights": [float(record.weight) for record in growth_data],
            "heights": [float(record.height) for record in growth_data],
            "child_name": child.childName,
        }

        return Response(chart_data, status=status.HTTP_200_OK)

