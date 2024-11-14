from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from ...models import AditionalInfoUser
from ...serializers.userSerializers.UserProfileEditSerializer import UserDataSerializer, AditionalInfoUserDataSerializer

class UserProfileRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            # Serializa los datos del usuario
            user_serializer = UserDataSerializer(user)

            # Obtiene y serializa la información adicional del usuario
            aditional_info = AditionalInfoUser.objects.get(user=user)
            aditional_info_serializer = AditionalInfoUserDataSerializer(aditional_info)

            # Combina ambos serializadores en la respuesta
            response_data = {
                "user": aditional_info_serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except AditionalInfoUser.DoesNotExist:
            return Response(
                {"error": "No se encontró información adicional para el usuario."},
                status=status.HTTP_404_NOT_FOUND,
            )
