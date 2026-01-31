from django.urls import path
from .views import (
    get_equipment,
    upload_csv,
    equipment_summary,
    delete_equipment,
    delete_all_equipment,
    get_upload_batches,
    delete_upload_batch,
)
from .views import (
    get_equipment,
    upload_csv,
    equipment_summary,
    delete_equipment,
    get_upload_batches,
)


urlpatterns = [
    # Equipment data
    path('equipment/', get_equipment),
    path('equipment/<int:id>/', delete_equipment),
    path('equipment/delete-all/', delete_all_equipment),

    # CSV upload
    path('upload/', upload_csv),

    # Summary
    path('summary/', equipment_summary),

    # Upload history (CRITICAL)
    path('upload-batches/', get_upload_batches),
    path('upload-batch/<int:id>/', delete_upload_batch),
    path('upload-batches/', get_upload_batches),

]
