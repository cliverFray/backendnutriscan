from django.contrib import admin
from django.urls import path, include

from nutriscan.views import MalnutritionDetectionCreateView, MalnutritionDetectionListView, LoginView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('detections/', MalnutritionDetectionListView.as_view(), name='detection-list'),
    path('detections/create/', MalnutritionDetectionCreateView.as_view(), name='detection-create'),
]
