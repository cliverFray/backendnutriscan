from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Child
from ...serializers.childSerializers.childSerializer import ChildSerializer
from rest_framework.permissions import IsAuthenticated

class UpdateChildView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            # Obtiene el objeto del niño, asegurándose de que pertenezca al usuario autenticado
            child = Child.objects.get(pk=pk, user=request.user)
        except Child.DoesNotExist:
            return Response({"error": "Child not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

        # Realiza la actualización parcial para permitir actualizaciones de campos individuales
        serializer = ChildSerializer(child, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Guarda los cambios en la base de datos
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
