from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Q

from ...serializers.userSerializers.UserProfileEditSerializer import UserDataSerializer, AditionalInfoUserDataSerializer
from ...models import AditionalInfoUser

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']  # Solo permite el método PUT

    def put(self, request):
        user = request.user
        user_data = request.data.get("user")
        aditional_info_data = request.data.get("aditional_info")
        
        # Validaciones para evitar duplicados en DNI y Phone, excluyendo el propio usuario actual
        if AditionalInfoUser.objects.filter(~Q(user=user), userDNI=aditional_info_data['userDNI']).exists():
            return Response({"error": "El DNI ya existe en el sistema."}, status=status.HTTP_400_BAD_REQUEST)
        
        if AditionalInfoUser.objects.filter(~Q(user=user), userPhone=aditional_info_data['userPhone']).exists():
            return Response({"error": "El número de teléfono ya existe en el sistema."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                # Actualizar los datos principales del usuario
                user_serializer = UserDataSerializer(user, data=user_data, partial=True)
                if user_serializer.is_valid():
                    user_serializer.save()
                else:
                    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # Actualizar la información adicional del usuario
                aditional_info = AditionalInfoUser.objects.get(user=user)
                aditional_info_serializer = AditionalInfoUserDataSerializer(aditional_info, data=aditional_info_data, partial=True)
                if aditional_info_serializer.is_valid():
                    aditional_info_serializer.save()
                else:
                    return Response(aditional_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # Respuesta de éxito con datos actualizados
                response_data = {
                    "user": user_serializer.data,
                    "aditional_info": aditional_info_serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
                
        except AditionalInfoUser.DoesNotExist:
            return Response(
                {"error": "No se encontró información adicional para el usuario."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Error al actualizar los datos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
