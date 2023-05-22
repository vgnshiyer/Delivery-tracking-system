import logging
import sys
import pika
import json
from pymongo import MongoClient

logger = logging.getLogger(__name__)

class RabbitMQConsumer(object):
    """ This consumer class will handle messages of type json and consume them to a calling object.
    .   
    .
    """
    
    CONNECTION_PORT = 5672
    CREDS = pika.PlainCredentials('admin','admin')
    CONTENT_TYPE = 'application/json'
    
    def __init__(self, url, queuename, persist_data=False, mongo_dest="NA"):
        """ Create an instance of producer class
        :param str url: Broker DNS for rabbitmq svc
        
        :param str queuename: Name of Queue
        
        :param str mongo_dest: DB object for mongo collection to store data
        """
        if persist_data == True and mongo_dest == "NA":
            raise Exception("Mongo DB destination is required when persist_data is set.")
        if persist_data == True and mongo_dest != "NA":
            self.mongo_client = MongoClient(str(mongo_dest)+':27017')
            logger.info('Established connection with mongo client on {}:{}'.format(mongo_dest,'27017'))
            self.mydb=self.mongo_client["Delivery"]
        
        self.url = url
        self.queuename = queuename
        self.properties = pika.BasicProperties(content_type=self.CONTENT_TYPE)
        self.persist_data = persist_data
        
    def connect(self):
        """ This method connects to RabbitMQ broker, and returns the connection handle.
        """
        logger.info('Connecting to {}'.format(self.url))
        self.channel = pika.BlockingConnection(pika.ConnectionParameters(self.url,self.CONNECTION_PORT,'/',self.CREDS)).channel()
        self.channel.queue_declare(queue=self.queuename, durable=True)
        logger.info('Waiting for messages. To exit press Ctrl+C')
        
    def start_consumer(self):
        """
        This method initiates a consumer to given queue. 
        Uses the on_message method as callback on a message arrival for 
        acknowledgement.
        """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queuename, on_message_callback=self.on_msg, auto_ack=True)
        logger.info('Starting Consumer.')
        self.channel.start_consuming()
        
    def on_msg(self, ch, method, properties, body):
        """
        This method prints the message received by the consumer.
        """
        logger.debug('Received a message.')
        logger.info(body.decode())
        logger.debug('Storing data to persistent data store.')
        if (self.persist_data):
            self.store_msg(eval(body.decode()))
        
    def store_msg(self, msg):
        """
        This method stores the data recvd from queue to 
        persisitent mongo db pod.
        """
        
        self.mytab = self.mydb[msg['truck-type']]
        self.mytab.insert_one(msg)