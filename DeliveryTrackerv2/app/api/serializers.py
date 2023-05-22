from rest_framework import serializers
from main.models import DeliveryVehicle

class DeliveryVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryVehicle
        fields = '__all__'