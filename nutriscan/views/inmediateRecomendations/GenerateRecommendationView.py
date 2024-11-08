import random
from decimal import Decimal
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ...models import MalnutritionDetection, RecommendationTemplate, ImmediateRecommendation, Child

class GenerateRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, child_id):
        user = request.user

        # Verificar que el niño pertenece al usuario autenticado
        try:
            child = Child.objects.get(pk=child_id, user=user)
        except Child.DoesNotExist:
            return Response({"error": "El niño no pertenece al usuario autenticado o no existe."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la detección más reciente del niño
        try:
            latest_detection = MalnutritionDetection.objects.filter(child=child).latest('detectionDate')
        except MalnutritionDetection.DoesNotExist:
            return Response({"error": "No se encontró ninguna detección para este niño."}, status=status.HTTP_404_NOT_FOUND)

        # Comprobar si el peso y la altura están disponibles
        if child.childCurrentWeight and child.childCurrentHeight:
            # Calcular el IMC (Peso / Altura^2)
            height_m = Decimal(child.childCurrentHeight) / 100  # Convertir cm a metros
            bmi = child.childCurrentWeight / (height_m ** 2)
            bmi = round(bmi, 2)
            bmi_info = f"El IMC calculado del niño es: {bmi}"
        else:
            bmi_info = "No se pudo calcular el IMC debido a la falta de peso o altura."

        # Seleccionar una recomendación de acuerdo a la categoría de la detección
        category = latest_detection.detectionResult
        recommendations = RecommendationTemplate.objects.filter(category=category)
        
        if recommendations.exists():
            # Seleccionar una recomendación aleatoria
            selected_recommendation = random.choice(recommendations).message

            # Crear la recomendación inmediata en la base de datos si no existe
            ImmediateRecommendation.objects.update_or_create(
                detection=latest_detection,
                defaults={'inmediateRecomMessage': selected_recommendation}
            )
        else:
            selected_recommendation = "No se encontraron recomendaciones para esta categoría."

        # Construir la respuesta
        response_message = {
            "detection_result": category,
            "immediate_recommendation": selected_recommendation,
            "bmi_info": bmi_info
        }

        return Response(response_message, status=status.HTTP_200_OK)
