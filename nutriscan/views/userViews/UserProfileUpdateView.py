from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Q

from ...serializers.userSerializers.UserProfileEditSerializer import UserDataSerializer, AditionalInfoUserDataSerializer
from ...models import AditionalInfoUser

from ...utils.VerifyEmailSender import verify_email_sender

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    def put(self, request):
        user = request.user
        user_data = request.data.get("user", {})
        aditional_info_data = request.data.get("aditional_info", {})

        # Validar correo duplicado (excluyendo el del propio usuario)
        if 'email' in user_data and User.objects.filter(~Q(pk=user.pk), email=user_data['email']).exists():
            return Response({"error": "El correo ya existe en el sistema."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar DNI duplicado (excluyendo al propio usuario)
        if 'userDNI' in aditional_info_data and AditionalInfoUser.objects.filter(~Q(user=user), userDNI=aditional_info_data['userDNI']).exists():
            return Response({"error": "El DNI ya existe en el sistema."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Obtener la info adicional
                aditional_info = AditionalInfoUser.objects.get(user=user)

                # Verificar si el correo fue actualizado
                new_email = user_data.get("email")
                email_changed = new_email and new_email != user.email

                # Si la contraseña está vacía, no actualizarla
                if not user_data.get("password"):
                    user_data.pop("password", None)

                # Actualizar datos principales del usuario
                user_serializer = UserDataSerializer(user, data=user_data, partial=True)
                if user_serializer.is_valid():
                    user_serializer.save()
                else:
                    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # Obtener y actualizar info adicional
                aditional_info = AditionalInfoUser.objects.get(user=user)

                # No permitir actualizar el teléfono
                aditional_info_data.pop('userPhone', None)

                aditional_info_serializer = AditionalInfoUserDataSerializer(aditional_info, data=aditional_info_data, partial=True)
                if aditional_info_serializer.is_valid():
                    aditional_info_serializer.save()
                else:
                    return Response(aditional_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                # Si el correo fue cambiado, poner is_confirmed en False y enviar correo de verificación
                if email_changed:
                    aditional_info.is_confirmed = False
                    aditional_info.save()
                    verify_email_sender(user)  # Envía el correo de verificación

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
            import traceback
            traceback.print_exc()
            return Response(
                {"error": f"Error al actualizar los datos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
