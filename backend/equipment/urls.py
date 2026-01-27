from django.urls import path
from .views import get_equipment, upload_csv, equipment_summary

urlpatterns = [
    path('equipment/', get_equipment),
    path('upload/', upload_csv),
    path('summary/', equipment_summary),
]
