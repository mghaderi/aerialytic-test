from django.urls import path
from .views import SolarCalculationView

urlpatterns = [
    path('calculate/', SolarCalculationView.as_view(), name='calculate_solar_angles'),
]