from django.db import models
import utils
import json

class DeliveryVehicle(models.Model):
    vehiclename = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)
    
db_handle, client = utils.get_db_handle('Delivery', 'mongo', '27017')

def getDeliveryVehicles():
    # logger.debug(request.headers)
    vehicles  = db_handle.list_collection_names()
    vehicles  = [vehicle.replace("_","-") for vehicle in vehicles]
    # logger.debug('Got data:')
    # logger.debug(vehicles)
    return json.loads(json_util.dumps({ "data":vehicles }))

def getVehiclePosition(vehiclename):
    # logger.info('Sending most recent coordinates for vehicle {}'.format(topicname))
    record = db_handle[vehiclename].find().sort([('$natural', -1)]).limit(1)[0]
    return json.loads(json_util.dumps({ "data":record }))
