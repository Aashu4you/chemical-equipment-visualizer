from django.db import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Equipment
from .serializers import EquipmentSerializer
import pandas as pd

from django.db import models

# GET API
@api_view(['GET'])
def get_equipment(request):
    equipment = Equipment.objects.all().order_by('-uploaded_at')
    serializer = EquipmentSerializer(equipment, many=True)
    return Response(serializer.data)

# Add CSV upload API
@api_view(['POST'])
def upload_csv(request):
    file = request.FILES.get('file')

    if not file:
        return Response(
            {"error": "No file uploaded"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not file.name.endswith('.csv'):
        return Response(
            {"error": "Only CSV files are allowed"},
            status=status.HTTP_400_BAD_REQUEST
        )

    df = pd.read_csv(file)

    required_columns = {
        'Equipment Name',
        'Type',
        'Flowrate',
        'Pressure',
        'Temperature'
    }

    if not required_columns.issubset(df.columns):
        return Response(
            {"error": "CSV format is invalid"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Save data
    for _, row in df.iterrows():
        Equipment.objects.create(
            equipment_name=row['Equipment Name'],
            equipment_type=row['Type'],
            flowrate=row['Flowrate'],
            pressure=row['Pressure'],
            temperature=row['Temperature']
        )

    # Summary analytics
    summary = {
        "total_equipment": Equipment.objects.count(),
        "avg_flowrate": Equipment.objects.aggregate(models.Avg('flowrate'))['flowrate__avg'],
        "avg_pressure": Equipment.objects.aggregate(models.Avg('pressure'))['pressure__avg'],
        "avg_temperature": Equipment.objects.aggregate(models.Avg('temperature'))['temperature__avg'],
        "equipment_type_distribution": dict(
            Equipment.objects.values_list('equipment_type')
            .annotate(count=models.Count('equipment_type'))
        )
    }

    return Response(
        {"message": "CSV uploaded successfully", "summary": summary},
        status=status.HTTP_201_CREATED
    )


# for the summary
@api_view(['GET'])
def equipment_summary(request):
    summary = {
        "total_equipment": Equipment.objects.count(),
        "avg_flowrate": Equipment.objects.aggregate(models.Avg('flowrate'))['flowrate__avg'],
        "avg_pressure": Equipment.objects.aggregate(models.Avg('pressure'))['pressure__avg'],
        "avg_temperature": Equipment.objects.aggregate(models.Avg('temperature'))['temperature__avg'],
        "equipment_type_distribution": {
            item['equipment_type']: item['count']
            for item in Equipment.objects
                .values('equipment_type')
                .annotate(count=models.Count('equipment_type'))
        }
    }

    return Response(summary)
