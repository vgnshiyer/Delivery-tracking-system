import os


def getDeliveryVehicleData(logger,dir):
    vehicles=os.listdir(dir)
    vehicle_data = {}
    for vehicle in vehicles:
        temp = {}
        if vehicle != "Readme.md":
            f = open(dir+"/"+i)
            data = json.load(f)
            f.close()
            temp['kafka-topic-name'] = data['kafkaTopicName']
            temp['truck-number'] = data['truckNumber']
            temp['truck-type'] = data['truckType']
            temp['truck-coordinates'] = data['features'][0]['geometry']['coordinates']
            vehicle_data[vehicle] = temp
            del temp
    return vehicle_data

def genTruckRecord(truckType,truckNumber,coordinates):
    truckRecord = {
        "truckType": truckType,
        "truckNumber": truckNumber,
        "timestamp": (datetime.utcnow()).strftime("%d/%m/%Y %H:%M:%S"),
        "coordinates": { "latitude": coordinates[0], "longitude": coordinates[1]}
    }
    return truckRecord
