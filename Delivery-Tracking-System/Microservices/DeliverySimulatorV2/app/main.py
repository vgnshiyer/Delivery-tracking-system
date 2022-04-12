'''
This code performs below steps:
1. Parses json data on dir public/delivery-vans
2. Produces messages with map coordinates to kafka topics/ActiveMQ queue.
3. Topics/Queues have the same name as the json file names.
4. Producer is run as a thread for each vehicle parallely and produces messages in an infinite loop.
'''

import logging
import os

## VARS
jsonpath = 'public/delivery-vans'
## ENV vars


# setting custom logger format
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        # logger.removeHandler(handler)
        handler.setFormatter(logging.Formatter(FORMAT))
else:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(FORMAT))
        logger.addHandler(handler)
# setting logger mode
logger.setLevel(logging.DEBUG)

def getDeliveryVehicleData(dir):
    vehicles=os.listdir(dir)
    vehicle_data = {}
    for vehicle in vehicles:
        temp = {}
        if vehicle != "readme.txt":
            f = open(dir+"/"+i)
            data = json.load(f)
            f.close()
            temp['kafka-topic-name'] = data['kafkaTopicName']
            temp['truck-number'] = data['truckNumber']
            temp['truck-type'] = data['truckType']
            temp['truck-coordinates'] = data['features'][0]['geometry']['coordinates']
            vehicle_data[vehicle] = temp
            del temp
            
    logger.debug('Found following vehicle data {}'.format(*vehicle_data.values()))
    logger.debug(vehicle_data)
    return vehicle_data

if __name__ == "__main__":
    vehicle_data = getDeliveryVehicleData(jsonpath)
    '''
    {
        vehicle_name(filename): {
            kafkatopicname: something,
            queuename: someotherthing,
            trucknumber: #,
            trucktype: sometype,
            truckCoords: [
                [
                    72.9715347290039,
                    19.1967292074432
                ],
                ...
            ]
        },
        ...
    }
    '''
    ## vehicle_name.vehicle_name.truckcoords[*]
    ## now we pass this data as it is to vehicle simulator package to simulate vehicle movement