from django.db import models

# Create your models here.
from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    max_temperature = models.FloatField()
    pressure_rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
