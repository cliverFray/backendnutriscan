from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User

class ConfirmAccountView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        if user.is_active:
            return HttpResponse("<h2>Tu cuenta ya está confirmada. Puedes iniciar sesión.</h2>")

        user.is_active = True
        user.save()
        return HttpResponse("<h2>¡Cuenta confirmada exitosamente! Ya puedes usar la app.</h2>")
