from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .models import Equipment, UploadBatch
from .serializers import EquipmentSerializer, UploadBatchSerializer
import pandas as pd
from .serializers import EquipmentSerializer, UploadBatchSerializer


# ✅ GET ALL UPLOAD HISTORY (latest first)
@api_view(['GET'])
def get_upload_batches(request):
    batches = UploadBatch.objects.all().order_by('-uploaded_at')
    serializer = UploadBatchSerializer(batches, many=True)
    return Response(serializer.data)


# ✅ GET EQUIPMENT (OPTIONALLY FILTER BY BATCH)
@api_view(['GET'])
def get_equipment(request):
    batch_id = request.GET.get('batch_id')

    equipment = Equipment.objects.all()

    if batch_id:
        equipment = equipment.filter(upload_batch_id=batch_id)

    equipment = equipment.order_by('-uploaded_at')
    serializer = EquipmentSerializer(equipment, many=True)

    return Response(serializer.data)



# ✅ UPLOAD CSV + CREATE UPLOAD HISTORY
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

    # ✅ CALCULATE SUMMARY STATS
    total_records = len(df)
    avg_flowrate = float(df['Flowrate'].mean())
    avg_pressure = float(df['Pressure'].mean())
    avg_temperature = float(df['Temperature'].mean())

    # ✅ CREATE UPLOAD BATCH
    batch = UploadBatch.objects.create(
        filename=file.name,
        total_records=total_records,
        avg_flowrate=avg_flowrate,
        avg_pressure=avg_pressure,
        avg_temperature=avg_temperature
    )

    # ✅ CREATE EQUIPMENT RECORDS
    equipment_objects = [
        Equipment(
            upload_batch=batch,
            equipment_name=row['Equipment Name'],
            equipment_type=row['Type'],
            flowrate=row['Flowrate'],
            pressure=row['Pressure'],
            temperature=row['Temperature']
        )
        for _, row in df.iterrows()
    ]

    Equipment.objects.bulk_create(equipment_objects)

    return Response(
        {
            "message": "CSV uploaded successfully",
            "batch_id": batch.id,
            "records_added": total_records
        },
        status=status.HTTP_201_CREATED
    )


# ✅ SUMMARY (ALL DATA)
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


# ✅ DELETE AN ENTIRE UPLOAD (CASCADE SAFE)
@api_view(['DELETE'])
def delete_upload_batch(request, id):
    try:
        batch = UploadBatch.objects.get(id=id)
        batch.delete()
        return Response({"message": "Upload batch deleted successfully"})
    except UploadBatch.DoesNotExist:
        return Response({"error": "Upload batch not found"}, status=404)

# ✅ GET UPLOAD HISTORY (latest first)
@api_view(['GET'])
def upload_history(request):
    batches = UploadBatch.objects.all().order_by('-uploaded_at')

    data = [
        {
            "id": batch.id,
            "filename": batch.filename,
            "uploaded_at": batch.uploaded_at,
            "total_records": batch.total_records,
            "avg_flowrate": batch.avg_flowrate,
            "avg_pressure": batch.avg_pressure,
            "avg_temperature": batch.avg_temperature
        }
        for batch in batches
    ]

    return Response(data)


@api_view(['DELETE'])
def delete_upload_batch(request, batch_id):
    try:
        batch = UploadBatch.objects.get(id=batch_id)
        batch.delete()  # cascades to Equipment
        return Response({"message": "Upload batch deleted successfully"})
    except UploadBatch.DoesNotExist:
        return Response({"error": "Batch not found"}, status=404)


@api_view(['DELETE'])
def delete_all_equipment(request):
    deleted_count, _ = Equipment.objects.all().delete()

    return Response(
        {
            "message": "All equipment deleted successfully",
            "deleted_records": deleted_count
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_upload_batches(request):
    batches = UploadBatch.objects.all().order_by('-uploaded_at')
    serializer = UploadBatchSerializer(batches, many=True)
    return Response(serializer.data)
