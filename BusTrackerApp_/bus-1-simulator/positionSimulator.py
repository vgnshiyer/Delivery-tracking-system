import kafka
from kafka import KafkaProducer
import json
from datetime import datetime
import time

f = open('bus_data.json')
busData = json.load(f)

busData = busData['features'][0]['geometry']['coordinates']

def generateBusRecord(coordinates):
    busRecord = {
        "name": "Ghansoli-Vashi",
        "busNumber": 9,
        "timestamp": (datetime.utcnow()).strftime("%d/%m/%Y %H:%M:%S"),
        "coordinates": { "latitude": coordinates[0], "longitude": coordinates[1]}
    }
    return busRecord

producer = KafkaProducer(bootstrap_servers=['kafka:9071'],value_serializer=lambda x:json.dumps(x).encode('utf-8'))

print("Producing bus coordinates..")
i=0
#produce coordinates infinitely
while(i<len(busData)):
    busRecord=generateBusRecord(busData[i])
    time.sleep(5)
#    print(busRecord)
    producer.send('vignesh-test-topic', value=busRecord)
    i+=1
    if i==len(busData):
        i=0

