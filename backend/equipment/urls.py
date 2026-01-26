from django.urls import path
from .views import CSVUploadView, EquipmentListView

urlpatterns = [
    path('upload/', CSVUploadView.as_view()),
    path('equipment/', EquipmentListView.as_view()),
]
