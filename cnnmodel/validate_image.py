from django.http import JsonResponse
from PIL import Image, ImageOps
import numpy as np
import cv2
from mtcnn import MTCNN
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import io

# Inicializar el detector de rostros MTCNN
detector = MTCNN()

# Tamaño máximo permitido para la imagen (en bytes)
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
TARGET_SIZE = (224, 224)  # Tamaño deseado de salida

class ValidateImageView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']  # Solo permite GET
    def post (self, request):
    
        if 'image' not in request.FILES:
            return Response({"valid": False, "message": "No se proporcionó ninguna imagen."}, status=400)
        
        file = request.FILES['image']
        image_bytes = file.read()

        # Validación del tamaño de la imagen
        if len(image_bytes) > MAX_IMAGE_SIZE:
            return Response({"valid": False, "message": "La foto es demasiado pesada."}, status=400)

        # Convertir la imagen en formato OpenCV
        np_img = np.frombuffer(image_bytes, np.uint8)
        img_cv = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if img_cv is None:
            return Response({"valid": False, "message": "Imagen no válida."}, status=400)

        # Convertir la imagen a RGB (OpenCV usa BGR por defecto)
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

        # Detectar rostros
        faces = detector.detect_faces(img_rgb)

        if not faces:
            return Response({"valid": False, "message": "No se detectó ningún rostro en la imagen."})
        if len(faces) > 1:
            return Response({"valid": False, "message": "Asegúrate de que solo un niño esté en la imagen."})

        # Validación de orientación del rostro y otras condiciones
        largest_face = max(faces, key=lambda face: face['box'][2] * face['box'][3])
        x, y, w, h = largest_face['box']
        face_crop = img_rgb[y:y + h, x:x + w]

        # Redimensionar el rostro
        face_img = Image.fromarray(face_crop)
        face_img = ImageOps.pad(face_img, TARGET_SIZE, method=Image.Resampling.LANCZOS)

        # Validación de la orientación del rostro (mirada directa)
        keypoints = largest_face['keypoints']
        left_eye, right_eye, nose = keypoints['left_eye'], keypoints['right_eye'], keypoints['nose']
        eye_center_x = (left_eye[0] + right_eye[0]) / 2

        if abs(eye_center_x - nose[0]) > 10:
            return Response({"valid": False, "message": "Asegúrate de que el niño mire directamente a la cámara."})

        if y < 10:
            return Response({"valid": False, "message": "Mantén la cámara a la altura de los ojos del niño."})

        forehead_y = keypoints['left_eye'][1] - 0.3 * (keypoints['left_eye'][1] - keypoints['nose'][1])
        if forehead_y < y:
            return Response({"valid": False, "message": "Evita accesorios como gorros o gafas."})

        # Si todas las validaciones se pasan
        return Response({"valid": True, "message": "La imagen es válida."})