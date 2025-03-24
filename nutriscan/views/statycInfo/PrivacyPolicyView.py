# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import PrivacyPolicy
from ...serializers.statycInfo.PrivacyPolicySerializer import PrivacyPolicySerializer

class PrivacyPolicyView(APIView):
    def get(self, request):
        policy = PrivacyPolicy.objects.last()
        if policy:
            serializer = PrivacyPolicySerializer(policy)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Política de privacidad no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
