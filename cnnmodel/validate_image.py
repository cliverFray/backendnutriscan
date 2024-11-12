from django.http import JsonResponse
from google.cloud import vision
import io

# Instancia del cliente de Vision
client = vision.ImageAnnotatorClient()

# Tamaño máximo permitido para la imagen (en bytes)
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

def validate_image(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({"error": "No se proporcionó ninguna imagen."}, status=400)
    
    file = request.FILES['image']
    image_bytes = file.read()

    # Validación del tamaño de la imagen
    if len(image_bytes) > MAX_IMAGE_SIZE:
        return JsonResponse({"valid": False, "message": "La foto es demasiado pesada."})

    # Validación de si la imagen está completamente oscura (muy básica)
    if image_bytes[:2] == b'\xff\xd8' and image_bytes[-2:] == b'\xff\xd9':
        return JsonResponse({"valid": False, "message": "La imagen está completamente oscura o no se detectó correctamente."})

    # Carga la imagen en Vision API
    image = vision.Image(content=image_bytes)
    
    # Detección de rostros
    face_response = client.face_detection(image=image)
    faces = face_response.face_annotations

    # Verificar si se detecta un solo rostro
    if not faces:
        return JsonResponse({"valid": False, "message": "No se detectó ningún rostro en la imagen."})
    if len(faces) > 1:
        return JsonResponse({"valid": False, "message": "Asegúrate de que solo un niño esté en la imagen."})
    
    face = faces[0]

    # Validación de la mirada directa (usando los ángulos de orientación)
    if abs(face.pan_angle) > 10 or abs(face.tilt_angle) > 10:
        return JsonResponse({"valid": False, "message": "Asegúrate de que el niño mire directamente a la cámara."})
    
    # Validación de la altura de los ojos (posición del rostro en la imagen)
    # Puedes ajustar los valores si es necesario
    face_box = face.bounding_poly
    if face_box.vertices[0].y < 10 or face_box.vertices[1].y < 10:
        return JsonResponse({"valid": False, "message": "Mantén la cámara a la altura de los ojos del niño."})
    
    # Validación para accesorios (como gafas o gorros)
    for landmark in face.landmarks:
        if landmark.type_ in [
            vision.FaceAnnotation.Landmark.Type.LEFT_EAR_TRAGION,
            vision.FaceAnnotation.Landmark.Type.RIGHT_EAR_TRAGION,
            vision.FaceAnnotation.Landmark.Type.FOREHEAD_GLABELLA
        ]:
            return JsonResponse({"valid": False, "message": "Evita accesorios como gorros o gafas."})

    # Si todas las validaciones se pasan
    return JsonResponse({"valid": True, "message": "La imagen es válida."})
