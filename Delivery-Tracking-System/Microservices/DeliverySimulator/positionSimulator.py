import kafka
from kafka import KafkaProducer
import json
from datetime import datetime
import time
import threading
import os, sys, traceback

kafka_endpt = os.environ.get('KAFKA_BROKER_ENDPT')

def getTruckData(jsonfile):
    f = open(jsonfile)
    truckData = json.load(f)
    truckCoords = truckData['features'][0]['geometry']['coordinates']
    truckNumber = truckData['truckNumber']
    truckType = truckData['truckType']
    f.close()
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
    producer = KafkaProducer(bootstrap_servers=[str(kafka_endpt)+':9071'],value_serializer=lambda x:json.dumps(x).encode('utf-8'))
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
        # print(truckRecord)
        producer.send(topicname, value=truckRecord)
        i+=1
        if i==len(truckCoords):
            truckCoords = truckCoords[::-1]
            i=0

def getDeliveryVans(dir):
    vehicles=os.listdir(dir)
    kafkatopics=[]
    for i in vehicles:
        if i != "readme.txt":
            f = open(dir+"/"+i)
            data = json.load(f)
            f.close()
            kafkatopics.append(data['kafkaTopicName'])
    vehicles.remove("readme.txt")
    return vehicles, kafkatopics
    
def startParallerProducer(topicname, jsonfile):
    p = threading.Thread(target=sendData, args=(topicname,jsonfile,))
    p.start()

try:
    vehicles, kafkatopics = getDeliveryVans("DeliveryVans")
    for i,vehiclename in enumerate(vehicles):
        startParallerProducer(kafkatopics[i],"DeliveryVans/"+str(vehiclename))
    
except Exception as e:
    excp = sys.exc_info()
    tb = sys.exc_info()[-1]
    stk = traceback.extract_tb(tb, 2)
    fname = stk[-1][2]
    print("The program exited with the following error message at "+str(fname)+": \n")
    print(e)
finally:
    print("If this line executed, there is really something wrong with the code")
