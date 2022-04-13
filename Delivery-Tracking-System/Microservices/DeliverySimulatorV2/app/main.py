'''
This code performs below steps:
1. Parses json data on dir public/delivery-vans
2. Produces messages with map coordinates to kafka topics/ActiveMQ queue.
3. Topics/Queues have the same name as the json file names.
4. Producer is run as a thread for each vehicle parallely and produces messages in an infinite loop.
'''

import logging
import os
from packages.vehicle-data-generator import getDeliveryVehicleData
import threading

## VARS
jsonpath = 'public/delivery-vans'
## ENV vars
kafka_endpt = os.environ.get('KAFKA_BROKER_ENDPT')

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


def startParallelProducer(vehicle):
    p = threading.Thread(target=sendData, args=(topicname,))
    p.start()

if __name__ == "__main__":
    vehicle_data = getDeliveryVehicleData(logger,jsonpath)
    logger.debug('Found following vehicle data {}'.format(*vehicle_data.values()))
    logger.debug(vehicle_data)
    
    # for vehicle in vehicle_data.values():
    #     startParallerProducer(vehicle)