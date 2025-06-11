import boto3
from botocore.exceptions import ClientError
from django.conf import settings

def resend_verify_email_sender(user):
    ses_client = boto3.client(
        'ses',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    subject = "Verificación de tu correo en NutriScan"
    body_text = f"Hola {user.first_name},\n\nAun no has actualizado tu correo en NutriScan. Por favor, confirma este nuevo correo para poder continuar."
    body_html = f"""
    <html>
    <head></head>
    <body>
        <img src='https://myassetsapp.s3.us-east-2.amazonaws.com/imagesapp/Nutriscan+(1).png' alt='NutriScan Logo' style='width: 150px;'>
        <h1>¡Hola, {user.first_name}!</h1>
        <p>Aun no has actualizado tu correo electrónico en <strong>NutriScan</strong>.</p>
        <p>Por favor, confirma tu correo haciendo clic en el siguiente enlace:</p>
        <p><a href='https://nutriscanapp.me/nutriscan/confirmar-cuenta/{user.id}/'>Confirmar correo</a></p>
        <p>Si no realizaste la solicitud de verificación de tu correo, ignora este mensaje.</p>
    </body>
    </html>
    """

    try:
        response = ses_client.send_email(
            Source=settings.AWS_SES_SOURCE_EMAIL,
            Destination={'ToAddresses': [user.email]},
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {
                    'Text': {'Data': body_text, 'Charset': 'UTF-8'},
                    'Html': {'Data': body_html, 'Charset': 'UTF-8'}
                }
            },
            ReplyToAddresses=[settings.AWS_SES_REPLYTO_EMAIL]
        )
        return response
    except ClientError as e:
        raise Exception(f"Error al enviar el correo de verificación: {e.response['Error']['Message']}")
