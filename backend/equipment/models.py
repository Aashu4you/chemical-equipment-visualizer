from django.db import models


# ✅ NEW MODEL: represents one CSV upload (history entry)
class UploadBatch(models.Model):
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    total_records = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()

    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


# ✅ EXISTING MODEL: now linked to an upload batch
class Equipment(models.Model):
    upload_batch = models.ForeignKey(
        UploadBatch,
        on_delete=models.CASCADE,
        related_name="equipments",
        null=True,
        blank=True
    )

    equipment_name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=50)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.equipment_name
