from django.db import models

class Equipment(models.Model):
    equipment_name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=50)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.equipment_name
