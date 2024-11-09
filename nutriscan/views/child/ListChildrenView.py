from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ...models import Child
from ...serializers.childSerializers.childSerializer import ChildSerializer

class ListChildrenView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']  # Solo permite GET
    def get(self, request):
        # Filtra los niños asociados al usuario autenticado
        children = Child.objects.filter(user=request.user)
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
