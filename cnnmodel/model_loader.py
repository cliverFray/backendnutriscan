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
    model_key = 'ResNetModels/model_resnet50_nutriscan.pth'#configuracion de la carpeta de bucket

    # Crear la carpeta temporal si no existe
    if not os.path.exists('/tmp'):
        os.makedirs('/tmp')

    model_path = r'D:\OneDrive - Universidad Peruana de Ciencias\Archivos 2024\Ciclo 9 -2024 II\Proyecto tesis\Develop\models CNN codigo\ResNetModels\model_resnet50_nutriscan.pth'
    #model_path = settings.MODEL_PATH # es l carpeta donde se almacenará el modelo cuando se descarga

    if not os.path.exists(model_path):
        # Descargar el modelo desde S3
        s3_client.download_file(bucket_name, model_key, model_path)

    # Define la arquitectura del modelo
    model = models.resnet50(weights=None)  # Crea una instancia del modelo ResNet50
    num_ftrs = model.fc.in_features
    model.fc = torch.nn.Linear(num_ftrs, 3)  # Ajusta el número de clases si es necesario

    # Carga los pesos en el modelo
    #model.load_state_dict(torch.load(model_path))

    #engaño
    model_path = r'D:\OneDrive - Universidad Peruana de Ciencias\Archivos 2024\Ciclo 9 -2024 II\Proyecto tesis\Develop\models CNN codigo\ResNetModels\model_resnet50_nutriscan.pth'
    #cargamos
    model.load_state_dict(torch.load(model_path, weights_only=True))
    
    model.eval()
    return model
