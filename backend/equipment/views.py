from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .models import Equipment
from .serializers import EquipmentSerializer
import pandas as pd


# GET all equipment
@api_view(['GET'])
def get_equipment(request):
    equipment = Equipment.objects.all().order_by('-uploaded_at')
    serializer = EquipmentSerializer(equipment, many=True)
    return Response(serializer.data)


# Upload CSV
@api_view(['POST'])
def upload_csv(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    if not file.name.endswith('.csv'):
        return Response({"error": "Only CSV files allowed"}, status=400)

    df = pd.read_csv(file)

    required_columns = {
        'Equipment Name',
        'Type',
        'Flowrate',
        'Pressure',
        'Temperature'
    }

    if not required_columns.issubset(df.columns):
        return Response({"error": "Invalid CSV format"}, status=400)

    for _, row in df.iterrows():
        Equipment.objects.create(
            equipment_name=row['Equipment Name'],
            equipment_type=row['Type'],
            flowrate=row['Flowrate'],
            pressure=row['Pressure'],
            temperature=row['Temperature'],
        )

    return Response({"message": "CSV uploaded successfully"}, status=201)


# Summary API
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


# ✅ DELETE SINGLE EQUIPMENT
@api_view(['DELETE'])
def delete_equipment(request, id):
    try:
        equipment = Equipment.objects.get(id=id)
        equipment.delete()
        return Response({"message": "Equipment deleted successfully"})
    except Equipment.DoesNotExist:
        return Response({"error": "Equipment not found"}, status=404)




@api_view(['DELETE'])
def delete_all_equipment(request):
    deleted_count, _ = Equipment.objects.all().delete()

    return Response(
        {
            "message": "All equipment data deleted successfully",
            "deleted_records": deleted_count
        },
        status=status.HTTP_200_OK
    )
