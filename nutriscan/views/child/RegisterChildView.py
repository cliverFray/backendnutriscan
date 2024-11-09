from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Child
from ...serializers.childSerializers.childSerializer import ChildSerializer
from rest_framework.permissions import IsAuthenticated

class RegisterChildView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']  # Solo permite POST
    def post(self, request):
        child_data = request.data.copy()  # Crea una copia de los datos del niño
        child_data['user'] = request.user  # Asocia el objeto de usuario autenticado directamente

        serializer = ChildSerializer(data=child_data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Pasa el usuario autenticado como argumento
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
