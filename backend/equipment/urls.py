from django.urls import path
from .views import (
    get_equipment,
    upload_csv,
    equipment_summary,
    delete_equipment,
    delete_all_equipment
)

urlpatterns = [
    path('equipment/', get_equipment),
    path('upload/', upload_csv),
    path('summary/', equipment_summary),

    # DELETE endpoints
    path('equipment/<int:id>/', delete_equipment),
    path('equipment/delete-all/', delete_all_equipment),
]
