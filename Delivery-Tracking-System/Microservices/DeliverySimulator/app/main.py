'''
This code performs below steps:
1. Parses json data on dir public/delivery-vans
2. Produces messages with map coordinates to kafka topics/ActiveMQ queue.
3. Topics/Queues have the same name as the json file names.
4. Producer is run as a thread for each vehicle parallely and produces messages in an infinite loop.
'''
import time, sys, os, traceback
import logging
from packages.VehicleDataGenerator import getDeliveryVehicleData
from packages.kafkaSimulator import startParallelProducer
from kafka import KafkaProducer

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

# producer = KafkaProducer(bootstrap_servers=[str(kafka_endpt)+':9071'],value_serializer=lambda x:json.dumps(x).encode('utf-8'))
logger.debug('Opened connection with kafka broker {} for producing data.'.format(kafka_endpt))

if __name__ == "__main__":
    try:
        vehicle_data = getDeliveryVehicleData(jsonpath)
        logger.debug('Found following vehicle data {}'.format(*vehicle_data.keys()))
        
        for vehicle in vehicle_data.values():
            ## dont forget to pass the producer client object
            startParallelProducer(logger, vehicle)
            
    except Exception as e:
        excp = sys.exc_info()
        tb = sys.exc_info()[-1]
        stk = traceback.extract_tb(tb, 2)
        fname = stk[-1][2]
        logger.info("The program exited with the following error message at "+str(fname)+": \n")
        logger.error(e)