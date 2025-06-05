from django.http import JsonResponse
from PIL import Image, ImageOps
import numpy as np
import cv2
from mtcnn import MTCNN
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date
import io
from datetime import timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta  # Para cálculo de edad exacta

import pillow_heif
pillow_heif.register_heif_opener()

# Amazon Rekognition
import boto3
from django.conf import settings

# Modelos de tu backend
from nutriscan.models import Child

# Inicializar detector de rostros
detector = MTCNN()

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
TARGET_SIZE = (224, 224)

# Inicializar cliente de Rekognition
rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

def calcular_edad(fecha_nacimiento):
    try:
        ahora = timezone.now().date()
        edad = relativedelta(ahora, fecha_nacimiento).years
        return edad
    except Exception as e:
        return -1

def estimar_edad_rekognition(image_bytes):
    response = rekognition.detect_faces(
        Image={'Bytes': image_bytes},
        Attributes=['ALL']
    )
    if not response['FaceDetails']:
        return -1  # No rostro detectado

    # Tomamos el primer rostro detectado
    face = response['FaceDetails'][0]
    age_range = face['AgeRange']
    # Promedio del rango estimado
    estimated_age = (age_range['Low'] + age_range['High']) / 2
    return estimated_age

class ValidateImageView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def post(self, request, child_id):
        if not child_id:
            return Response({"valid": False, "message": "Se requiere el ID del niño."}, status=400)

        try:
            child = Child.objects.get(childId=child_id)
        except Child.DoesNotExist:
            return Response({"valid": False, "message": "Niño no encontrado."}, status=404)

        if 'image' not in request.FILES:
            return Response({"valid": False, "message": "No se proporcionó ninguna imagen."}, status=400)

        file = request.FILES['image']
        file_name = file.name.lower()
        image_bytes = file.read()

        if len(image_bytes) > MAX_IMAGE_SIZE:
            return Response({"valid": False, "message": "La foto es demasiado pesada."}, status=400)

        # Convertir imagen
        if file_name.endswith('.heic'):
            try:
                heif_img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
                img_rgb = np.array(heif_img)
            except Exception as e:
                return Response({"valid": False, "message": f"No se pudo procesar la imagen HEIC: {str(e)}"}, status=400)
        else:
            np_img = np.frombuffer(image_bytes, np.uint8)
            img_cv = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            if img_cv is None:
                return Response({"valid": False, "message": "Imagen no válida."}, status=400)
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

        # Detección de rostros con MTCNN
        faces = detector.detect_faces(img_rgb)
        if not faces:
            return Response({"valid": False, "message": "No se detectó ningún rostro en la imagen."}, status=400)
        if len(faces) > 1:
            return Response({"valid": False, "message": "Asegúrate de que solo un niño esté en la imagen."}, status=400)

        # Validar orientación y recorte
        largest_face = max(faces, key=lambda face: face['box'][2] * face['box'][3])
        x, y, w, h = largest_face['box']
        face_crop = img_rgb[y:y + h, x:x + w]

        face_img = Image.fromarray(face_crop)
        face_img = ImageOps.pad(face_img, TARGET_SIZE, method=Image.Resampling.LANCZOS)

        # Validar orientación
        keypoints = largest_face['keypoints']
        left_eye, right_eye, nose = keypoints['left_eye'], keypoints['right_eye'], keypoints['nose']
        eye_center_x = (left_eye[0] + right_eye[0]) / 2
        if abs(eye_center_x - nose[0]) > 10:
            return Response({"valid": False, "message": "Asegúrate de que el niño mire directamente a la cámara."}, status=400)
        if y < 10:
            return Response({"valid": False, "message": "Mantén la cámara a la altura de los ojos del niño."}, status=400)
        forehead_y = keypoints['left_eye'][1] - 0.3 * (keypoints['left_eye'][1] - keypoints['nose'][1])
        if forehead_y < y:
            return Response({"valid": False, "message": "Evita accesorios como gorros o gafas."}, status=400)

        # 🟢 Estimar edad usando Amazon Rekognition
        try:
            edad_estimado = estimar_edad_rekognition(image_bytes)
            if edad_estimado == -1:
                return Response({
                    "valid": False,
                    "message": "No se pudo estimar la edad automáticamente (sin rostro o error de Rekognition)."
                }, status=400)
        except Exception as e:
            return Response({
                "valid": False,
                "message": f"Error en la estimación de edad: {str(e)}"
            }, status=500)

        # Validar que la edad sea infantil (ejemplo: menor de 14)
        if edad_estimado > 14:
            return Response({
                "valid": False,
                "message": f"La imagen parece de una persona mayor ({edad_estimado} años aprox.). Sube solo fotos de niños."
            }, status=400)

        # 🟢 Edad real
        edad_real = calcular_edad(child.childBirthDate)
        if edad_real < 0:
            return Response({"valid": False, "message": "Error al calcular la edad real."}, status=500)

        # 🟢 Comparar edad estimada y real (con margen de 3 años)
        if abs(edad_real - edad_estimado) > 3:
            return Response({
                "valid": False,
                "message": f"La edad estimada ({edad_estimado}) no coincide con la edad real del niño ({edad_real})."
            }, status=400)

        return Response({
            "valid": True,
            "message": "La imagen es válida y la edad coincide.",
            "edad_real": edad_real,
            "edad_estimada": edad_estimado
        }, status=200)
