import time
import threading
from packages.VehicleDataGenerator import generateTruckRecord

def sendData(logger, vehicle, producer=None):
    logger.info("Producing truck coordinates for {}".format(vehicle['truck-type']))
    count = 0
    while count < len(vehicle['coordinates']):
        msg = generateTruckRecord(vehicle['truck-type'], vehicle['truck-number'], vehicle['coordinates'])
        time.sleep(3)
        logger.debug(msg)
        # producer.send(vehicle['kafka-topic-name'],  value=msg)
        count += 1
        if len(vehicle['coordinates']) == count:
            count = 0
            vehicle['coordinates'] = vehicle['coordinates'][::-1]

def startParallelProducer(logger, vehicle, producer=None):
    p = threading.Thread(target=sendData, args=(logger, vehicle, producer,))
    p.start()
    
if __name__ == '__main__':
    vehicle_data = {
        kafkatopicname: "something",
        queuename: "someotherthing",
        trucknumber: 23,
        trucktype: "sometype",
        truckCoords: [
            [
                72.9715347290039,
                19.1967292074432
            ]
        ]
    }
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    
    startParallelProducer(logger, vehicle_data)