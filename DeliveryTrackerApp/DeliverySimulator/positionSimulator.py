import kafka
from kafka import KafkaProducer
import json
from datetime import datetime
import time
import threading
import sys

def getTruckData(jsonfile):
    f = open(jsonfile)
    truckData = json.load(f)
    truckCoords = truckData['features'][0]['geometry']['coordinates']
    truckNumber = truckData['truckNumber']
    truckType = truckData['truckType']
    return truckNumber,truckType,truckCoords

def generateTruckRecord(coordinates,truckNumber,truckType):
    truckRecord = {
        "truckType": truckType,
        "truckNumber": truckNumber,
        "timestamp": (datetime.utcnow()).strftime("%d/%m/%Y %H:%M:%S"),
        "coordinates": { "latitude": coordinates[0], "longitude": coordinates[1]}
    }
    return truckRecord

def initProducer():
    producer = KafkaProducer(bootstrap_servers=['kafka:9071'],value_serializer=lambda x:json.dumps(x).encode('utf-8'))
    return producer

def sendData(topicname,jsonfile):
    print("Producing truck coordinates..")
    truckNumber,truckType,truckCoords = getTruckData(jsonfile)
    i=0
    producer = initProducer()
    #produce coordinates infinitely
    while(i<len(truckCoords)):
        truckRecord=generateTruckRecord(truckCoords[i],truckNumber, truckType)
        time.sleep(3)
        producer.send(topicname, value=truckRecord)
        i+=1
        if i==len(truckCoords):
            i=0

try:
    ## can add any number of producers
    p1 = threading.Thread(target=sendData, args=('vign-test-topic','truck1_data.json',))
    p2 = threading.Thread(target=sendData, args=('vign-test-topic-2','truck2_data.json',))

    p1.start()
    p2.start()
except Exception as e:
    excp = sys.exc_info()
    print("The program exited with the following error message at line "+str(excp[2].tb_lineno)+": \n")
    print(e)
finally:
    print("If this line executed, there is really something wrong with the code")
