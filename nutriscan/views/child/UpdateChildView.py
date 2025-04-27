from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Child,GrowthHistory
from ...serializers.childSerializers.childSerializer import ChildSerializer
from rest_framework.permissions import IsAuthenticated

class UpdateChildView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']  # Solo permite el método PUT
    
    def put(self, request, pk):
        try:
            # Obtiene el objeto del niño, asegurándose de que pertenezca al usuario autenticado
            child = Child.objects.get(pk=pk, user=request.user)
        except Child.DoesNotExist:
            return Response({"error": "Child not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)
        
        previous_weight = child.childCurrentWeight
        previous_height = child.childCurrentHeight

        # Realiza la actualización parcial para permitir actualizaciones de campos individuales
        serializer = ChildSerializer(child, data=request.data, partial=True)
        if serializer.is_valid():
            #serializer.save()  # Guarda los cambios en la base de datos
            updated_child = serializer.save()

            # Si cambiaron peso o altura, registrar en GrowthHistory
            new_weight = updated_child.childCurrentWeight
            new_height = updated_child.childCurrentHeight

            if new_weight is not None and new_height is not None:
                # Opcional: evitar duplicar si ya existe hoy
                exists_today = GrowthHistory.objects.filter(child=updated_child, date_recorded=date.today()).exists()
                if not exists_today:
                    GrowthHistory.objects.create(
                        child=updated_child,
                        weight=new_weight,
                        height=new_height
                    )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
