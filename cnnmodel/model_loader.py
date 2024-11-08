import boto3
import torch
import os
from torchvision import models
from django.conf import settings

def load_model_from_s3():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    bucket_name = 'cnnmodelsdetection'
    model_key = 'ResNetModels/model_resnet50_nutriscan.pth'  # Configuración de la ruta del modelo en S3
    model_path = '/tmp/model_resnet50_nutriscan.pth'  # Carpeta temporal en EC2 para almacenar el modelo descargado

    # Descargar el modelo desde S3 solo si no existe localmente
    if not os.path.exists(model_path):
        s3_client.download_file(bucket_name, model_key, model_path)

    # Define la arquitectura del modelo
    model = models.resnet50(weights=None)  # Crea una instancia del modelo ResNet50
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, 3)  # Ajusta el número de clases si es necesario

    # Carga los pesos en el modelo
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

    model.eval()  # Cambia el modelo a modo de evaluación
    return model
