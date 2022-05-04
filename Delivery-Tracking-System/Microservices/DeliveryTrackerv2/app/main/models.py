from django.db import models

class DeliveryVehicle(models.Model):
    vehiclename = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)