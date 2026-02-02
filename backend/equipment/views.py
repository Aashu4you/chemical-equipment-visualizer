from django.http import HttpResponse
from django.db import models
from django.db.models import Avg, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

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
# PDF GENERATION - SIMPLIFIED & GUARANTEED TO WORK
# ======================================================

def generate_pdf(request):
    """Generate PDF with filters support - Simplified version"""
    try:
        # Get filter parameters
        equipment_type = request.GET.get('type', 'All')
        search_text = request.GET.get('search', '').strip()
        
        # Filter equipment
        equipment_qs = Equipment.objects.all()
        
        if equipment_type and equipment_type != 'All':
            equipment_qs = equipment_qs.filter(equipment_type=equipment_type)
        
        if search_text:
            equipment_qs = equipment_qs.filter(equipment_name__icontains=search_text)
        
        # Create response
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=equipment_report.pdf"
        
        # Create canvas with landscape orientation
        c = canvas.Canvas(response, pagesize=landscape(A4))
        page_width, page_height = landscape(A4)
        
        # Starting position
        y = page_height - 60
        margin = 50
        
        # ===== HEADER =====
        c.setFillColorRGB(0.12, 0.23, 0.37)
        c.rect(0, page_height - 100, page_width, 100, fill=1)
        
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(page_width / 2, page_height - 50, "Chemical Equipment Report")
        
        c.setFont("Helvetica", 12)
        report_date = datetime.now().strftime("%B %d, %Y at %H:%M")
        c.drawCentredString(page_width / 2, page_height - 75, f"Generated: {report_date}")
        
        y = page_height - 120
        
        # ===== FILTERS INFO =====
        c.setFillColorRGB(0, 0, 0)
        if equipment_type != 'All' or search_text:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(margin, y, "Active Filters:")
            y -= 20
            c.setFont("Helvetica", 10)
            if equipment_type != 'All':
                c.drawString(margin + 20, y, f"• Equipment Type: {equipment_type}")
                y -= 15
            if search_text:
                c.drawString(margin + 20, y, f"• Search: \"{search_text}\"")
                y -= 15
            y -= 10
        
        # ===== SUMMARY =====
        summary = equipment_qs.aggregate(
            total=Count("id"),
            avg_flow=Avg("flowrate"),
            avg_pressure=Avg("pressure"),
            avg_temp=Avg("temperature")
        )
        
        # Summary box
        c.setFillColorRGB(0.95, 0.97, 0.98)
        c.roundRect(margin, y - 80, page_width - 100, 80, 10, fill=1, stroke=0)
        
        c.setFillColorRGB(0.12, 0.23, 0.37)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin + 20, y - 25, "Summary Statistics")
        
        c.setFillColorRGB(0.2, 0.2, 0.2)
        c.setFont("Helvetica", 11)
        
        col1 = margin + 20
        col2 = margin + 250
        col3 = margin + 500
        
        y -= 50
        
        total = summary['total'] or 0
        avg_flow = summary['avg_flow'] or 0
        avg_press = summary['avg_pressure'] or 0
        avg_temp = summary['avg_temp'] or 0
        
        c.drawString(col1, y, f"Total Equipment: {total}")
        c.drawString(col2, y, f"Avg Flowrate: {avg_flow:.2f}")
        y -= 20
        c.drawString(col1, y, f"Avg Pressure: {avg_press:.2f}")
        c.drawString(col2, y, f"Avg Temperature: {avg_temp:.2f}")
        
        y -= 50
        
        # ===== CHARTS SECTION =====
        dist_data = equipment_qs.values("equipment_type").annotate(
            count=Count("equipment_type")
        ).order_by('-count')
        
        if dist_data.exists() and len(list(dist_data)) > 0:
            try:
                from reportlab.graphics.shapes import Drawing
                from reportlab.graphics.charts.piecharts import Pie
                from reportlab.graphics.charts.barcharts import VerticalBarChart
                
                c.setFillColorRGB(0.12, 0.23, 0.37)
                c.setFont("Helvetica-Bold", 14)
                c.drawString(margin, y, "Visual Analytics")
                y -= 30
                
                # ===== PIE CHART - Equipment Type Distribution =====
                pie_drawing = Drawing(300, 220)
                pie = Pie()
                pie.x = 100
                pie.y = 40
                pie.width = 140
                pie.height = 140
                
                # Prepare data
                pie_data = []
                pie_labels = []
                for item in dist_data:
                    pie_data.append(float(item['count']))
                    pie_labels.append(str(item['equipment_type'])[:15])
                
                pie.data = pie_data
                pie.labels = pie_labels
                
                # Colors
                chart_colors = [
                    colors.HexColor('#2a6f7f'),
                    colors.HexColor('#1e3a5f'),
                    colors.HexColor('#4a9aab'),
                    colors.HexColor('#6bb6c7'),
                    colors.HexColor('#8cd2e3'),
                    colors.HexColor('#aedeff'),
                ]
                
                for i in range(len(pie_data)):
                    pie.slices[i].fillColor = chart_colors[i % len(chart_colors)]
                
                pie.slices.strokeWidth = 1
                pie.slices.strokeColor = colors.white
                
                pie_drawing.add(pie)
                
                # Draw pie chart
                pie_drawing.drawOn(c, margin, y - 220)
                
                # Pie chart label
                c.setFont("Helvetica-Bold", 11)
                c.setFillColorRGB(0.12, 0.23, 0.37)
                c.drawString(margin + 60, y - 10, "Equipment Type Distribution")
                
                # ===== BAR CHART - Average Parameters =====
                bar_drawing = Drawing(400, 220)
                bar_chart = VerticalBarChart()
                bar_chart.x = 50
                bar_chart.y = 40
                bar_chart.width = 300
                bar_chart.height = 150
                
                bar_chart.data = [[
                    float(avg_flow),
                    float(avg_press),
                    float(avg_temp)
                ]]
                
                bar_chart.categoryAxis.categoryNames = ['Flowrate', 'Pressure', 'Temperature']
                bar_chart.categoryAxis.labels.fontSize = 10
                bar_chart.categoryAxis.labels.angle = 0
                
                bar_chart.valueAxis.valueMin = 0
                bar_chart.valueAxis.labels.fontSize = 9
                
                # Bar styling
                bar_chart.bars[0].fillColor = colors.HexColor('#2a6f7f')
                bar_chart.bars[0].strokeColor = colors.HexColor('#1e3a5f')
                bar_chart.bars[0].strokeWidth = 1
                
                bar_drawing.add(bar_chart)
                
                # Draw bar chart
                bar_drawing.drawOn(c, margin + 350, y - 220)
                
                # Bar chart label
                c.setFont("Helvetica-Bold", 11)
                c.setFillColorRGB(0.12, 0.23, 0.37)
                c.drawString(margin + 420, y - 10, "Average Operating Parameters")
                
                y -= 250
                
            except Exception as chart_error:
                # If charts fail, show text distribution instead
                c.setFillColorRGB(0.12, 0.23, 0.37)
                c.setFont("Helvetica-Bold", 14)
                c.drawString(margin, y, "Equipment Type Distribution")
                y -= 25
                
                c.setFillColorRGB(0.2, 0.2, 0.2)
                c.setFont("Helvetica", 10)
                
                for item in dist_data:
                    eq_type = item['equipment_type']
                    count = item['count']
                    percentage = (count / total * 100) if total > 0 else 0
                    
                    c.drawString(margin + 20, y, f"• {eq_type}: {count} units ({percentage:.1f}%)")
                    y -= 18
                
                y -= 20
        else:
            y -= 10
        
        # ===== TABLE =====
        c.setFillColorRGB(0.12, 0.23, 0.37)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y, "Equipment Details")
        y -= 25
        
        # Table data
        table_data = [
            ["ID", "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"]
        ]
        
        equipment_list = list(equipment_qs.all()[:25])
        
        for eq in equipment_list:
            name = str(eq.equipment_name)[:30] if eq.equipment_name else "N/A"
            eq_type = str(eq.equipment_type)[:20] if eq.equipment_type else "N/A"
            
            table_data.append([
                str(eq.id),
                name,
                eq_type,
                f"{float(eq.flowrate):.2f}",
                f"{float(eq.pressure):.2f}",
                f"{float(eq.temperature):.2f}",
            ])
        
        # Create table
        col_widths = [0.6*inch, 2.8*inch, 1.5*inch, 1.2*inch, 1.2*inch, 1.4*inch]
        table = Table(table_data, colWidths=col_widths)
        
        table.setStyle(TableStyle([
            # Header
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor('#1e3a5f')),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("TOPPADDING", (0, 0), (-1, 0), 10),
            
            # Body
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor('#2d3748')),
            ("ALIGN", (0, 1), (0, -1), "CENTER"),
            ("ALIGN", (1, 1), (2, -1), "LEFT"),
            ("ALIGN", (3, 1), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("TOPPADDING", (0, 1), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 7),
            
            # Grid and styling
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        
        # Calculate table position
        table_height = len(table_data) * 20
        
        if y - table_height < 50:
            c.showPage()
            y = page_height - 50
        
        table.wrapOn(c, page_width, page_height)
        table.drawOn(c, margin, y - table_height)
        
        y -= (table_height + 20)
        
        # Footer note
        if equipment_qs.count() > 25:
            c.setFont("Helvetica-Oblique", 9)
            c.setFillColorRGB(0.4, 0.4, 0.4)
            c.drawString(margin, y, f"* Showing first 25 of {equipment_qs.count()} records")
        
        # Page number
        c.setFont("Helvetica", 8)
        c.drawCentredString(page_width / 2, 25, "Page 1")
        
        # Save
        c.showPage()
        c.save()
        
        return response
        
    except Exception as e:
        # Return error as plain text if PDF generation fails
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)