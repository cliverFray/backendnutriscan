from ...models import NutritionTip
from ...serializers.nutritionTip.NutritionTipSerializer import NutritionTipSerializer

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class NutritionTipListView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']  # Solo permite GET

    def get(self, request):
        try:
            # Filtrar solo los registros del usuario autenticado
            nutrition_tips = NutritionTip.objects.all().order_by('-date_created')
            serializer = NutritionTipSerializer(nutrition_tips, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NutritionTip.DoesNotExist:
            return Response(
                {"error": "No se encontraron recomendaciones de nutrición para el usuario."},
                status=status.HTTP_404_NOT_FOUND,
            )
