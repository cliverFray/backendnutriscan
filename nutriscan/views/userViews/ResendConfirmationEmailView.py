from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

from ...utils.SendWelcomeEmail import send_welcome_email

class ResendConfirmationEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                send_welcome_email(user)
                return Response({"message": "Correo de confirmación reenviado."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "La cuenta ya está activa."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
