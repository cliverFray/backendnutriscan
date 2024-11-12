from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ...models import Child, MalnutritionDetection
from ...serializers.malnDetecSerializers.MalnutritionDetectionSerializer import MalnutritionDetectionSerializer

class DetectionHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']  # Solo permite POST

    def get(self, request):
        user = request.user
        detections = MalnutritionDetection.objects.filter(child__user=user).select_related('child')
        
        # Serializar las detecciones con los datos necesarios
        serialized_data = [
            {
                "detectionId": detection.detectionId,
                "detectionDate": detection.detectionDate,
                "detectionResult": detection.detectionResult,
                "detectionImageUrl": detection.detectionImageUrl,
                "childName": detection.child.childName
            }
            for detection in detections
        ]

        return Response(serialized_data, status=status.HTTP_200_OK)
