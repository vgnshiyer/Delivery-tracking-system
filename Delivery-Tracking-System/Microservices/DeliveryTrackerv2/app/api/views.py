from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import DeliveryVehicle
from main.models import *
from .serializers import DeliveryVehicleSerializer

@api_view(['GET'])
def apiOverview(request):
    urls = {
        'vehicles/':'get delivery vehicles'
    }
    return Response(urls)

@api_view(['GET'])
def getVehicles(request):
    response = getDeliveryVehicles()
    return response

@api_view(['GET'])
def getVehicleData(request, vehiclename):
    response = getVehiclePosition(vehiclename)
    return response
