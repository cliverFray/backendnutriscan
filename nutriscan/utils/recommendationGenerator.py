import random
from ..models import RecommendationTemplate, ImmediateRecommendation, MalnutritionDetection

class RecommendationGenerator:
    @staticmethod
    def generate_recommendation(detection: MalnutritionDetection):
        # Mapea el resultado del modelo a las categorías de RecommendationTemplate
        result_map = {
            'Con desnutrición': 'Desnutricion severa',
            'Normal': 'Normal',
            'Riesgo en desnutrición': 'Riesgo desnutricion'
        }
        category = result_map.get(detection.detectionResult, "Desconocido")

        # Obtener una recomendación aleatoria para la categoría
        recommendations = RecommendationTemplate.objects.filter(category=category)
        
        if recommendations.exists():
            selected_recommendation = random.choice(recommendations).message
        else:
            selected_recommendation = "No se encontraron recomendaciones para esta categoría."

        # Crear la recomendación inmediata en la base de datos
        ImmediateRecommendation.objects.update_or_create(
            detection=detection,
            defaults={'inmediateRecomMessage': selected_recommendation}
        )

        return selected_recommendation
