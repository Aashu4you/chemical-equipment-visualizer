from django.shortcuts import render

# Create your views here.
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Equipment

class CSVUploadView(APIView):
    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        df = pd.read_csv(file)

        for _, row in df.iterrows():
            Equipment.objects.create(
                name=row['name'],
                category=row['category'],
                material=row['material'],
                max_temperature=row['max_temperature'],
                pressure_rating=row['pressure_rating']
            )

        return Response({"message": "CSV uploaded successfully"})


# list equipment api
from rest_framework.generics import ListAPIView
from .serializers import EquipmentSerializer

class EquipmentListView(ListAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
