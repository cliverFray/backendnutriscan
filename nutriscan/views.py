from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import (
    AidPrograms, ArticlesAndTips, Child, DailyTips, GrowthReports, 
    HealthCenters, MalnutritionDetection, Notifications, 
    NutritionalRecommendations, PregnancyTips, Recipes, 
    RecommendationRecipes, User
)
from .serializers import (
    AidProgramsSerializer, ArticlesAndTipsSerializer, ChildSerializer, 
    DailyTipsSerializer, GrowthReportsSerializer, HealthCentersSerializer, 
    MalnutritionDetectionSerializer, NotificationsSerializer, 
    NutritionalRecommendationsSerializer, PregnancyTipsSerializer, 
    RecipesSerializer, RecommendationRecipesSerializer, UserSerializer
)

# ViewSet para Programas de Ayuda
class AidProgramsViewSet(viewsets.ModelViewSet):
    queryset = AidPrograms.objects.all()
    serializer_class = AidProgramsSerializer

# ViewSet para Artículos y Tips
class ArticlesAndTipsViewSet(viewsets.ModelViewSet):
    queryset = ArticlesAndTips.objects.all()
    serializer_class = ArticlesAndTipsSerializer

# ViewSet para Niño
class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

# ViewSet para Tips Diarios
class DailyTipsViewSet(viewsets.ModelViewSet):
    queryset = DailyTips.objects.all()
    serializer_class = DailyTipsSerializer

# ViewSet para Reportes de Crecimiento
class GrowthReportsViewSet(viewsets.ModelViewSet):
    queryset = GrowthReports.objects.all()
    serializer_class = GrowthReportsSerializer

# ViewSet para Centros de Salud
class HealthCentersViewSet(viewsets.ModelViewSet):
    queryset = HealthCenters.objects.all()
    serializer_class = HealthCentersSerializer

# ViewSet para Detección de Desnutrición
class MalnutritionDetectionViewSet(viewsets.ModelViewSet):
    queryset = MalnutritionDetection.objects.all()
    serializer_class = MalnutritionDetectionSerializer

# ViewSet para Notificaciones
class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer

# ViewSet para Recomendaciones Nutricionales
class NutritionalRecommendationsViewSet(viewsets.ModelViewSet):
    queryset = NutritionalRecommendations.objects.all()
    serializer_class = NutritionalRecommendationsSerializer

# ViewSet para Tips para Embarazadas
class PregnancyTipsViewSet(viewsets.ModelViewSet):
    queryset = PregnancyTips.objects.all()
    serializer_class = PregnancyTipsSerializer

# ViewSet para Recetas
class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer

# ViewSet para Recomendación de Recetas
class RecommendationRecipesViewSet(viewsets.ModelViewSet):
    queryset = RecommendationRecipes.objects.all()
    serializer_class = RecommendationRecipesSerializer

# ViewSet para Usuario
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
