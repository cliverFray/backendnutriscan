import boto3
from django.conf import settings
from botocore.exceptions import ClientError

def send_cod_pass_email(user,otp):
    ses_client = boto3.client(
        'ses',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    subject = "Código de reestablecimiento de contraseña de NutriScan"
    body_text = f"Hola {user.first_name},\n\nTu código de reestablecimiento de contraseña es {otp}. Expira en 10 minutos."
    body_html = f"""
    <html>
    <head></head>
    <body>
        <img src='https://myassetsapp.s3.us-east-2.amazonaws.com/imagesapp/Nutriscan+(1).png' alt='NutriScan Logo' style='width: 150px;'>
        <h1>Tu código de reestablecimiento de contraseña es: {otp}</h1>
        <p>Este código expira en 10 minutos. Si no solicitaste este código, por favor ignora este mensaje.</p>
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
            ReplyToAddresses=[settings.AWS_SES_REPLYTO_EMAIL]  # Agregado Reply-To
        )
        return response
    except ClientError as e:
        raise Exception(f"Error al enviar el correo de bienvenida: {e.response['Error']['Message']}")
