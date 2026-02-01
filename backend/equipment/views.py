from django.http import HttpResponse
from django.db import models
from django.db.models import Avg, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors

from .models import Equipment, UploadBatch
from .serializers import EquipmentSerializer, UploadBatchSerializer


# ======================================================
# EQUIPMENT APIs
# ======================================================

@api_view(['GET'])
def get_equipment(request):
    batch_id = request.GET.get('batch_id')

    qs = Equipment.objects.all()
    if batch_id:
        qs = qs.filter(upload_batch_id=batch_id)

    serializer = EquipmentSerializer(qs.order_by('-uploaded_at'), many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_equipment(request, id):
    try:
        Equipment.objects.get(id=id).delete()
        return Response({"message": "Equipment deleted"})
    except Equipment.DoesNotExist:
        return Response({"error": "Equipment not found"}, status=404)


@api_view(['DELETE'])
def delete_all_equipment(request):
    count, _ = Equipment.objects.all().delete()
    return Response(
        {"message": "All equipment deleted", "deleted": count},
        status=status.HTTP_200_OK
    )


# ======================================================
# CSV UPLOAD + BATCH TRACKING
# ======================================================

@api_view(['POST'])
def upload_csv(request):
    file = request.FILES.get("file")

    if not file or not file.name.endswith(".csv"):
        return Response({"error": "Valid CSV file required"}, status=400)

    df = pd.read_csv(file)

    required_cols = {
        "Equipment Name",
        "Type",
        "Flowrate",
        "Pressure",
        "Temperature"
    }

    if not required_cols.issubset(df.columns):
        return Response({"error": "Invalid CSV format"}, status=400)

    batch = UploadBatch.objects.create(
        filename=file.name,
        total_records=len(df),
        avg_flowrate=float(df["Flowrate"].mean()),
        avg_pressure=float(df["Pressure"].mean()),
        avg_temperature=float(df["Temperature"].mean())
    )

    Equipment.objects.bulk_create([
        Equipment(
            upload_batch=batch,
            equipment_name=row["Equipment Name"],
            equipment_type=row["Type"],
            flowrate=row["Flowrate"],
            pressure=row["Pressure"],
            temperature=row["Temperature"]
        )
        for _, row in df.iterrows()
    ])

    return Response(
        {"message": "Upload successful", "batch_id": batch.id},
        status=status.HTTP_201_CREATED
    )


# ======================================================
# UPLOAD HISTORY
# ======================================================

@api_view(['GET'])
def get_upload_batches(request):
    batches = UploadBatch.objects.all().order_by('-uploaded_at')
    serializer = UploadBatchSerializer(batches, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_upload_batch(request, id):
    try:
        UploadBatch.objects.get(id=id).delete()
        return Response({"message": "Batch deleted"})
    except UploadBatch.DoesNotExist:
        return Response({"error": "Batch not found"}, status=404)


# ======================================================
# SUMMARY API
# ======================================================

@api_view(['GET'])
def equipment_summary(request):
    summary = Equipment.objects.aggregate(
        total=models.Count('id'),
        avg_flow=models.Avg('flowrate'),
        avg_pressure=models.Avg('pressure'),
        avg_temperature=models.Avg('temperature')
    )

    distribution = {
        item["equipment_type"]: item["count"]
        for item in Equipment.objects
            .values("equipment_type")
            .annotate(count=models.Count("equipment_type"))
    }

    summary["equipment_type_distribution"] = distribution
    return Response(summary)


# ======================================================
# PDF GENERATION
# ======================================================

def generate_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=equipment_report.pdf"

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 50

    # ===== TITLE =====
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, y, "Chemical Equipment Report")
    y -= 40

    # ===== SUMMARY =====
    summary = Equipment.objects.aggregate(
        total=Count("id"),
        avg_flow=Avg("flowrate"),
        avg_pressure=Avg("pressure"),
        avg_temp=Avg("temperature")
    )

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Summary")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(60, y, f"Total Equipment: {summary['total']}")
    y -= 15
    c.drawString(60, y, f"Average Flowrate: {summary['avg_flow']:.2f}")
    y -= 15
    c.drawString(60, y, f"Average Pressure: {summary['avg_pressure']:.2f}")
    y -= 15
    c.drawString(60, y, f"Average Temperature: {summary['avg_temp']:.2f}")
    y -= 40

    # ===== BAR CHART =====
    chart_data = Equipment.objects.values("equipment_type").annotate(
        count=Count("equipment_type")
    )

    if chart_data.exists():
        drawing = Drawing(400, 200)
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 30
        chart.width = 300
        chart.height = 150
        chart.data = [[item["count"] for item in chart_data]]
        chart.categoryAxis.categoryNames = [
            item["equipment_type"] for item in chart_data
        ]
        chart.valueAxis.valueMin = 0

        drawing.add(chart)
        drawing.drawOn(c, 50, y - 220)
        y -= 260

    # ===== TABLE =====
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Equipment Details")
    y -= 20

    table_data = [
        ["Name", "Type", "Flowrate", "Pressure", "Temperature"]
    ]

    for eq in Equipment.objects.all():
        table_data.append([
            eq.equipment_name,
            eq.equipment_type,
            str(eq.flowrate),
            str(eq.pressure),
            str(eq.temperature),
        ])

    table = Table(table_data, colWidths=[2 * inch] * 5)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (2, 1), (-1, -1), "CENTER"),
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, 50, y - 20 * len(table_data))

    c.showPage()
    c.save()
    return response
