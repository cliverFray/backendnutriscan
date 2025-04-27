from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Child,GrowthHistory
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
            #serializer.save(user=request.user)  # Pasa el usuario autenticado como argumento
            child = serializer.save(user=request.user)  # Guarda el niño

            # Crear el primer registro de GrowthHistory si tiene peso y talla
            if child.childCurrentWeight is not None and child.childCurrentHeight is not None:
                GrowthHistory.objects.create(
                    child=child,
                    weight=child.childCurrentWeight,
                    height=child.childCurrentHeight
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
