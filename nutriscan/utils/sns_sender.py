# utils/sns_sender.py
import boto3
from botocore.exceptions import ClientError
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class SnsWrapper:
    def __init__(self, sns_resource):
        self.sns_resource = sns_resource

    def publish_text_message(self, phone_number, message):
        try:
            response = self.sns_resource.meta.client.publish(
                PhoneNumber=phone_number,
                Message=message
            )
            message_id = response["MessageId"]
            logger.info("Published message to %s. MessageId: %s", phone_number, message_id)
            return message_id
        except ClientError as e:
            logger.error("No se pudo enviar SMS a %s: %s", phone_number, e)
            return None
