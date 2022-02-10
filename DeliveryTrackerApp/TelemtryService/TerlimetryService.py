from kafka import KafkaConsumer
import json
from datetime import datetime
import os
import sys
from pymongo import MongoClient
import random
import threading

kafka_endpt = os.environ.get('KAFKA_BROKER_ENDPT')
mongo_endpt = os.environ.get('MONGO_DB_ENDPT')
# topicname = os.environ.get('KAFKA_TOPIC_NAME')
topicNames = ["nano-delivery-truck","cargo-delivery-truck"]

# initialize consumer and mongo client
consumer = KafkaConsumer(bootstrap_servers=[str(kafka_endpt)+':9071'],value_deserializer=lambda x:json.loads(x.encode('utf-8')))
client = MongoClient(str(mongo_endpt)+':27017')
# sample data
# #{
#         "truckType": truckType,
#         "truckNumber": truckNumber,
#         "timestamp": (datetime.utcnow()).strftime("%d/%m/%Y %H:%M:%S"),
#         "coordinates": { "latitude": coordinates[0], "longitude": coordinates[1]}
#     }

def InitMongoDB(topicname):
    # dblist = client.list_database_names()
    # if "Delivery" not in dblist:
    mydb=client["Delivery"]
    mytab = mydb[topicname]
    return mytab

def CalSpeed():
    speed = random.randrange(20,100,3)
    return speed

def GetData(topicname):
    mytab = InitMongoDB(topicname)
    consumer.subscribe([topicname])
    consumer.poll()
    consumer.seek_to_end()
    for msg in consumer:
        data=eval(msg)
        speed = CalSpeed()
        data['speed']=speed
        print(data)
        mytab.insert_one(data)
    ## store data in mongo db pod

def startParallerConsumer(topicname):
    p = threading.Thread(target=GetData, args=(topicname,))
    p.start()

try:
    for topicname in topicNames:
        startParallerConsumer(topicname)
except Exception as e:
    excp = sys.exc_info()
    print("The program exited with the following error message at line "+str(excp[2].tb_lineno)+": \n")
    print(e)
finally:
    print("If this line executed, there is really something wrong with the code")
