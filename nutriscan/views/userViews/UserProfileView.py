# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from ...serializers.userSerializers.UserRegisterSerializer import UserRegisterSerializer, AditionalInfoUserSerializer
from ...models import AditionalInfoUser

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get(self, request):
        try:
            # Obtén el usuario autenticado
            user = User.objects.get(id=request.user.id)
            aditional_info = AditionalInfoUser.objects.get(user=user)
            serializer = AditionalInfoUserSerializer(aditional_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AditionalInfoUser.DoesNotExist:
            return Response(
                {"error": "No se encontró información adicional para el usuario."},
                status=status.HTTP_404_NOT_FOUND,
            )
