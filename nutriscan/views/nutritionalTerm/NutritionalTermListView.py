# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import NutritionalTerm
from ...serializers.nutritionalTerm.NutritionalTermSerializer import NutritionalTermSerializer
from rest_framework.permissions import IsAuthenticated

class NutritionalTermListView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']  # Solo permite GET
    def get(self, request):
        terms = NutritionalTerm.objects.all()
        serializer = NutritionalTermSerializer(terms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
