from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from nutriscan.serializers import UserLoginSerializer
import jwt
from django.conf import settings

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            # Crear un token JWT
            token = jwt.encode(user_data, settings.SECRET_KEY, algorithm='HS256')
            return Response({"token": token}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
