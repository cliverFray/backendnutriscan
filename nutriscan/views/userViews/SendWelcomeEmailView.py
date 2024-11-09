import boto3
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class SendWelcomeEmailView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']  # Solo permite POST
    def post(self, request):
        # Obtener el ID del usuario o cualquier dato que identifique al usuario autenticado
        user_id = request.data.get("user_id")
        
        # Validar que el usuario existe
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Crear el cliente SES de AWS
        ses_client = boto3.client(
            'ses',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        # Configurar el mensaje del correo de bienvenida
        subject = "¡Bienvenido a Nuestra Aplicación!"
        body_text = f"Hola {user.first_name},\n\nGracias por registrarte en nuestra aplicación."
        body_html = f"""
        <html>
        <head></head>
        <body>
            <h1>¡Bienvenido, {user.first_name}!</h1>
            <p>Gracias por registrarte en nuestra aplicación. Estamos encantados de tenerte con nosotros.</p>
            <p>Si tienes alguna pregunta, no dudes en contactarnos.</p>
        </body>
        </html>
        """

        # Enviar el correo electrónico
        try:
            response = ses_client.send_email(
                Source=settings.AWS_SES_SOURCE_EMAIL,
                Destination={
                    'ToAddresses': [user.email],
                },
                Message={
                    'Subject': {'Data': subject},
                    'Body': {
                        'Text': {'Data': body_text},
                        'Html': {'Data': body_html}
                    }
                }
            )
            return Response({"message": "Correo de bienvenida enviado con éxito."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error al enviar el correo: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
