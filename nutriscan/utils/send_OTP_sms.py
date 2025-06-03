# utils/SendotpBySMS.py
import boto3
from django.conf import settings
from .sns_sender import SnsWrapper

def send_OTP_sms(phone_number, message):
    sns_resource = boto3.resource(
        'sns',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    sns_wrapper = SnsWrapper(sns_resource)
    message_id = sns_wrapper.publish_text_message(phone_number, message)
    return bool(message_id)
