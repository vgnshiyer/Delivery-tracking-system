from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('add_vehicle/', views.add_vehicle)
]