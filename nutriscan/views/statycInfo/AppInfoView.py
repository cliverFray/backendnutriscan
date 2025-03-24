from rest_framework import generics,status
from ...models import AppInfo
from ...serializers.statycInfo.AppInfoSerializer import AppInfoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class AppInfoView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']  # Solo permite GET
    queryset = AppInfo.objects.all()
    serializer_class = AppInfoSerializer

    def get(self):
        try:
            return self.queryset.first()  # Asumimos que solo habrá un registro
        except AppInfo.DoesNotExist:
            return Response(
                {"error": "No se encontró la información de la aplicación."},
                status=status.HTTP_404_NOT_FOUND
            )
