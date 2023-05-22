from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview),
    path('vehicles/', views.getVehicles),
    path('vehicles/<str:vehiclename>', views.getVehicleData)
]