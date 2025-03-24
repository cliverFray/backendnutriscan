# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import TermsAndConditions
from ...serializers.statycInfo.TermsAndConditionsSerializer import TermsAndConditionsSerializer

class TermsAndConditionsView(APIView):
    def get(self, request):
        terms = TermsAndConditions.objects.last()
        if terms:
            serializer = TermsAndConditionsSerializer(terms)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Términos y Condiciones no encontrados.'}, status=status.HTTP_404_NOT_FOUND)
