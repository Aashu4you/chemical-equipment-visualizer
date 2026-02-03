from django.urls import path
from .views import health_check, signup, login

urlpatterns = [
    path('health/', health_check),
    path('signup', signup),
    path('login', login),
]
