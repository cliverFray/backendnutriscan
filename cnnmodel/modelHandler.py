import torch
from torchvision import models, transforms
from PIL import Image
import requests
from io import BytesIO
from .model_loader import load_model_from_s3  # Asegúrate de ajustar la ruta de importación según tu estructura de archivos

# Configurar el dispositivo (GPU o CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Definir las transformaciones
test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Cargar el modelo ResNet50 entrenado desde S3
model = load_model_from_s3()
model = model.to(device)
model.eval()

# Función para predecir la clase desde la URL de una imagen
def predict_image_from_url(image_url):
    try:
        # Descargar la imagen desde la URL
        response = requests.get(image_url)
        response.raise_for_status()  # Verificar que la solicitud fue exitosa
        
        # Procesar la imagen
        image = Image.open(BytesIO(response.content))
        image = test_transform(image).unsqueeze(0)
        image = image.to(device)

        # Realizar la predicción
        with torch.no_grad():
            outputs = model(image)
            _, preds = torch.max(outputs, 1)

        # Mapeo de las clases
        class_names = ['N_DESNUTRIDO', 'N_NORMAL', 'N_RIESGO_DESNUTRIDO']
        return class_names[preds.item()]  # Retorna la clase predicha
    except requests.exceptions.RequestException as req_err:
        print(f"Error al descargar la imagen: {req_err}")
        return None
    except Exception as e:
        print(f"Error al predecir la imagen: {e}")
        return None

def predict_image(image):
    try:
        
        # Procesar la imagen
        image = Image.open(image).convert("RGB")
        image = test_transform(image).unsqueeze(0)
        image = image.to(device)

        # Realizar la predicción
        with torch.no_grad():
            outputs = model(image)
            _, preds = torch.max(outputs, 1)

        # Mapeo de las clases
        class_names = ['N_DESNUTRIDO', 'N_NORMAL', 'N_RIESGO_DESNUTRIDO']
        return class_names[preds.item()]
    except Exception as e:
        print(f"Error al predecir la imagen: {e}")
        return None
