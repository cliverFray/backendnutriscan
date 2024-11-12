from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ...models import Child
from ...serializers.childSerializers.childSerializer import ChildSerializer

class RetrieveChildView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']  # Solo permite GET

    def get(self, request, child_id):
        try:
            # Filtra el niño por ID y usuario autenticado
            child = Child.objects.get(childId=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response(
                {"error": "El niño no pertenece al usuario autenticado o no existe."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        # Serializar y devolver los datos del niño
        serializer = ChildSerializer(child)
        return Response(serializer.data, status=status.HTTP_200_OK)
