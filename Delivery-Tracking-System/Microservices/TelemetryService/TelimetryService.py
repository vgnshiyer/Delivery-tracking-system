from kafka import KafkaConsumer
from kafka import TopicPartition
import json
from datetime import datetime
import os
import sys
from pymongo import MongoClient
import random
import threading
import logging

kafka_endpt = os.environ.get('KAFKA_BROKER_ENDPT')
mongo_endpt = os.environ.get('MONGO_DB_ENDPT')
# topicname = os.environ.get('KAFKA_TOPIC_NAME')
topicNames = ["nano-delivery-truck","cargo-delivery-truck"]

client = MongoClient(str(mongo_endpt)+':27017')

def initLogger():
    global logger
    # setting custom logger format
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logger = logging.getLogger()
    if logger.handlers:
        for handler in logger.handlers:
            # logger.removeHandler(handler)
            handler.setFormatter(logging.Formatter(FORMAT))
    
    # setting logger mode
    logger.setLevel(logging.INFO)
'''
sample data
    {
        "truckType": truckType,
        "truckNumber": truckNumber,
        "timestamp": (datetime.utcnow()).strftime("%d/%m/%Y %H:%M:%S"),
        "coordinates": { "latitude": coordinates[0], "longitude": coordinates[1]}
    }
'''

def InitMongoDB(topicname):
    # dblist = client.list_database_names()
    # if "Delivery" not in dblist:
    logger.debug('Opening collection {}'.format(topicname))
    mydb=client["Delivery"]
    mytab = mydb[topicname]
    return mytab

def CalSpeed():
    logger.info('Caluclating vehhicle speed.')
    speed = random.randrange(20,100,3)
    return speed

def GetData(topicname):
    mytab = InitMongoDB(topicname.replace("-","_"))
    # initialize consumer and mongo client
    consumer = KafkaConsumer(bootstrap_servers=[str(kafka_endpt)+':9071'],value_deserializer=lambda x:json.loads(x.decode('utf-8')))
    consumer.assign([TopicPartition(str(topicname), 0)])
    consumer.poll()
    logger.info('Getting most recent offset to log.')
    consumer.seek_to_end()
    for msg in consumer:
        data=msg.value
        speed = CalSpeed()
        data['speed']=speed
        logger.debug('Inserting data:')
        logger.debug(data)
        mytab.insert_one(data)
    ## store data in mongo db pod

def startParallerConsumer(topicname):
    p = threading.Thread(target=GetData, args=(topicname,))
    p.start()

try:
    initLogger()
    for topicname in topicNames:
        startParallerConsumer(topicname)
except Exception as e:
    excp = sys.exc_info()
    logger.info("The program exited with the following error message at line "+str(excp[2].tb_lineno)+": \n")
    logger.error(e)
finally:
    logger.info('Executing finally block.')
