import os
import json
from datetime import datetime

def getDeliveryVehicleData(dir):
    vehicles=os.listdir(dir)
    vehicle_data = {}
    for vehicle in vehicles:
        temp = {}
        if vehicle != "Readme.md":
            f = open(dir+"/"+vehicle)
            data = json.load(f)
            f.close()
            temp['kafka-topic-name'] = data['kafkaTopicName']
            temp['truck-number'] = data['truckNumber']
            temp['truck-type'] = data['truckType']
            temp['coordinates'] = data['features'][0]['geometry']['coordinates']
            vehicle_data[vehicle] = temp
            del temp

    return vehicle_data

def generateTruckRecord(truckType,truckNumber,coordinates):
    truckRecord = {
        "truck-type": truckType,
        "truck-number": truckNumber,
        "timestamp": (datetime.utcnow()).strftime("%d/%m/%Y %H:%M:%S"),
        "coordinates": { "latitude": coordinates[0], "longitude": coordinates[1]}
    }
    return truckRecord

if __name__ == '__main__':
    dir = 'public/delivery-vans'
    vehicle_data = getDeliveryVehicleData(dir)