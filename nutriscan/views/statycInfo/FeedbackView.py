# Vista en Django
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Feedback
from ...serializers.statycInfo.FeedbackSerializer import FeedbackSerializer
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError

class FeedbackView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def get(self, request):
        feedbacks = Feedback.objects.all().order_by('-date_created')
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"error": "Error al guardar el feedback. Intente nuevamente."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)