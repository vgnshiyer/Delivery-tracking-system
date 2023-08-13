import logging
from packages import Simulator
import sys, os, traceback, json
import threading, time
from datetime import datetime
import asyncio

#VARS
jsonpath = os.environ.get('DATA_PATH')
mq_url = os.environ.get('RABBITMQ_URL')
queuename = os.environ.get('QUEUE')

LOG_FORMAT = '%(asctime)s - %(lineno)s:%(funcName)s - %(levelname)s - %(message)s'
# LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
            #   '-35s %(lineno) -5d: %(message)s')
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(handler)

def generateTruckRecord(truckType,truckNumber,coordinates):
    """ Generates standard vehicle coordinate record in json format
    """
    truckRecord = {
        "truck-type": truckType,
        "truck-number": truckNumber,
        "timestamp": (datetime.utcnow()).strftime("%d/%m/%Y %H:%M:%S"),
        "coordinates": { "latitude": coordinates[0], "longitude": coordinates[1]}
    }
    return truckRecord

def getDeliveryVehicleData(dir=None):
    if not dir: dir = 'public/delivery-vans'
    """Generating a refined json of all the data available in jsonpath dir in below format
        {
        vehicle_name(filename): {
            trucknumber: #,
            trucktype: sometype,
            truckCoords: [
                [ 72.9715347290039, 19.1967292074432 ],
                ...
            ]},
        ...
        }   
    """
    vehicles=os.listdir(dir)
    vehicle_data = {}
    for vehicle in vehicles:
        temp = {}
        if vehicle != "Readme.md":
            f = open(dir+"/"+vehicle)
            data = json.load(f)
            f.close()
            temp['truck-number'] = data['truckNumber']
            temp['truck-type'] = data['truckType']
            temp['coordinates'] = data['features'][0]['geometry']['coordinates']
            vehicle_data[vehicle] = temp
            del temp

    return vehicle_data

def sendData(client, vehicle):
    """ This method generates the json msg using the generateRecord function and send
    the data as a payload of type application/json to queue.
    
    this function iterates over the list of coordinates and produces them infinitely
    to the queue to simulate vehicle movement.
    """
    logger.info("Producing truck coordinates for {}".format(vehicle['truck-type']))
    count = 0
    while count < len(vehicle['coordinates']):
        msg = generateTruckRecord(vehicle['truck-type'], vehicle['truck-number'], vehicle['coordinates'][count])
        time.sleep(5)
        client.send_message(msg)
        logger.debug("Sent message")
        logger.debug(msg)
        count += 1
        if len(vehicle['coordinates']) == count:
            count = 0
            vehicle['coordinates'] = vehicle['coordinates'][::-1]

def main():
    logger.setLevel(logging.INFO)
    # fhandler = logging.FileHandler('app.logs')
    # fhandler.setFormatter(logging.Formatter(LOG_FORMAT))
    # logger.addHandler(handler)
    try:    
        vehicle_data = getDeliveryVehicleData(jsonpath)

        for vehicle in vehicle_data.values():
            client = Simulator.RabitMQProducer(mq_url, queuename)
            client.connect()
            p = threading.Thread(target=sendData, args=(client,vehicle,))
            p.start()
        
    except Exception as e:
        excp = sys.exc_info()
        tb = sys.exc_info()[-1]
        stk = traceback.extract_tb(tb, 2)
        fname = stk[-1][2]
        logger.info("The program exited with the following error message at "+str(fname)+": \n")
        logger.error(e)

if __name__ == "__main__":
    main()