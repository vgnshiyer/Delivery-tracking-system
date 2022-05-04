from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import DeliveryVehicle
from .serializers import DeliveryVehicleSerializer

@api_view(['GET'])
def getData(request):
    vehicles = DeliveryVehicle.objects.all()
    serializer = DeliveryVehicleSerializer(vehicles, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_vehicle(request):
    serializer = DeliveryVehicleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)