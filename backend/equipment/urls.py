from django.urls import path
from .views import get_equipment, upload_csv

urlpatterns = [
    path('equipment/', get_equipment),
    path('upload/', upload_csv),
]
