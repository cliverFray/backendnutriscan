import boto3
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

def send_welcome_email(user):
    ses_client = boto3.client(
        'ses',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    subject = "¡Bienvenido a NutriScan!"
    body_text = f"Hola {user.first_name},\n\nGracias por registrarte en NutriScan."
    body_html = f"""
    <html>
    <head></head>
    <body>
        <img src='https://myassetsapp.s3.us-east-2.amazonaws.com/imagesapp/Nutriscan+(1).png' alt='NutriScan Logo' style='width: 150px;'>
        <h1>¡Bienvenido, {user.first_name}!</h1>
        <p>Gracias por registrarte en <strong>NutriScan</strong>. Estamos encantados de tenerte con nosotros.</p>
        <p>Por favor, confirma tu cuenta haciendo clic en el siguiente enlace:</p>
        <p><a href='https://nutriscanapp.me/confirmar-cuenta/{user.id}/'>Confirmar mi cuenta</a></p>
        <p>Si no solicitaste este registro, ignora este mensaje.</p>
    </body>
    </html>
    """

    ses_client.send_email(
        Source=settings.AWS_SES_SOURCE_EMAIL,
        Destination={'ToAddresses': [user.email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': body_text},
                'Html': {'Data': body_html}
            }
        }
    )
