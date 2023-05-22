from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import DeliveryVehicle
from main.models import *
from .serializers import DeliveryVehicleSerializer
from django.http import HttpResponse
import os
import markdown

BASE = os.path.dirname(os.path.abspath(__file__))

# @api_view(['GET'])
def apiOverview(request):
    """Present Documentation"""
    
    with open(os.path.join(BASE, "Readme.md"), 'r') as markdown_file:
        content = markdown_file.read()
        return HttpResponse(markdown.markdown(content))

@api_view(['GET'])
def getVehicles(request):
    response = getDeliveryVehicles()
    return response

@api_view(['GET'])
def getVehicleData(request, vehiclename):
    response = getVehiclePosition(vehiclename)
    return response
