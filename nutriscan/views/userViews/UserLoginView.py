from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserLoginView(APIView):
    http_method_names = ['post']  # Solo permite POST
    def post(self, request):
        username = request.data.get("userPhone")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        
        if user:
            # Genera tokens de acceso y refresco con SimpleJWT
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
