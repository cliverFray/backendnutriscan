from rest_framework import status
from ...models import AppInfo
from ...serializers.statycInfo.AppInfoSerializer import AppInfoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class AppInfoView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']  # Solo permite GET

    def get(self, request):
        app_info = AppInfo.objects.first()  # Asumimos que solo hay un registro
        if app_info:
            serializer = AppInfoSerializer(app_info)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "No se encontró la información de la aplicación."},
                status=status.HTTP_404_NOT_FOUND
            )
