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
from dateutil.relativedelta import relativedelta

import pillow_heif
pillow_heif.register_heif_opener()

# Amazon Rekognition
import boto3
from django.conf import settings

# Modelos de tu backend
from nutriscan.models import Child

# Inicializar cliente de Rekognition
rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

# Inicializar detector de rostros
detector = MTCNN()

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
TARGET_SIZE = (224, 224)

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
        return -1, None  # No rostro detectado

    face = response['FaceDetails'][0]
    age_range = face['AgeRange']
    estimated_age = (age_range['Low'] + age_range['High']) / 2
    return estimated_age, face

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

        # Detección de rostros con MTCNN (asegurar solo 1 rostro)
        faces = detector.detect_faces(img_rgb)
        if not faces:
            return Response({"valid": False, "message": "No se detectó ningún rostro en la imagen."}, status=400)
        if len(faces) > 1:
            return Response({"valid": False, "message": "Asegúrate de que solo un niño esté en la imagen."}, status=400)

        # Recortar rostro para consistencia
        largest_face = max(faces, key=lambda face: face['box'][2] * face['box'][3])
        x, y, w, h = largest_face['box']
        face_crop = img_rgb[y:y + h, x:x + w]
        face_img = Image.fromarray(face_crop)
        face_img = ImageOps.pad(face_img, TARGET_SIZE, method=Image.Resampling.LANCZOS)

        # Estimar edad y obtener detalles con Rekognition
        try:
            edad_estimado, face_detail = estimar_edad_rekognition(image_bytes)
            if edad_estimado == -1 or face_detail is None:
                return Response({
                    "valid": False,
                    "message": "No se pudo estimar la edad automáticamente (sin rostro o error de Rekognition)."
                }, status=400)
        except Exception as e:
            return Response({
                "valid": False,
                "message": f"Error en la estimación de edad: {str(e)}"
            }, status=500)

        # Validar accesorios
        accessories = face_detail.get('Accessories', [])
        if any(acc['Type'] in ['Sunglasses', 'Glasses'] for acc in accessories):
            return Response({"valid": False, "message": "Por favor, retira las gafas del niño."}, status=400)

        if any(acc['Type'] == 'Hat' for acc in accessories):
            return Response({"valid": False, "message": "Por favor, retira el gorro del niño."}, status=400)


        # Validar orientación de la cabeza (frente, no perfil extremo)
        pose_yaw = face_detail['Pose']['Yaw']
        if abs(pose_yaw) > 20:  # Perfil exagerado
            return Response({
                "valid": False,
                "message": "La cabeza del niño está demasiado girada. Asegúrate de que esté de frente."
            }, status=400)

        # Validar que sea un niño (ejemplo: menor de 14)
        if edad_estimado > 14:
            return Response({
                "valid": False,
                "message": f"La imagen parece de una persona mayor ({edad_estimado} años aprox.). Sube solo fotos de niños."
            }, status=400)

        # Edad real
        # Validar edad: debe estar dentro del rango estimado ±3 años
        #edad_min = int(face_detail['AgeRange']['Low'])
        #edad_max = int(face_detail['AgeRange']['High'])
        

        # Comparar edad estimada y real (con margen de 3 años)
        try:
            edad_min = int(face_detail['AgeRange']['Low'])
            edad_max = int(face_detail['AgeRange']['High'])
            edad_real = calcular_edad(child.childBirthDate)
            if edad_real < 0:
                return Response({"valid": False, "message": "Error al calcular la edad real."}, status=500)

            if edad_real < (edad_min - 3) or edad_real > (edad_max + 3):
                return Response({
                    "valid": False,
                    "message": f"La edad real del niño ({edad_real}) no está dentro del rango estimado por Rekognition ({edad_min}-{edad_max})."
                }, status=400)
        except KeyError as e:
            return Response({
                "valid": False,
                "message": f"No se encontró el rango de edad en la respuesta de Rekognition: {str(e)}"
            }, status=400)
        except Exception as e:
            return Response({
                "valid": False,
                "message": f"Error inesperado: {str(e)}"
            }, status=500)

        return Response({
            "valid": True,
            "message": "La imagen es válida y la edad coincide.",
            "edad_real": edad_real,
            "edad_estimada": edad_estimado
        }, status=200)
