from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ...models import Child
from ...serializers.childSerializers.ChildNameSerializer import ChildNameSerializer

class ChildrenNamesView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']  # Solo permite GET
    def get(self, request):
        # Obtener los niños asociados al usuario autenticado
        children = Child.objects.filter(user=request.user)
        
        # Serializar solo los nombres
        serializer = ChildNameSerializer(children, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
