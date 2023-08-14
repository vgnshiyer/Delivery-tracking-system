import logging
import sys
import pika
import json
from pymongo import MongoClient
from bson import json_util

logger = logging.getLogger(__name__)

class RabbitMQConsumer(object):
    """ This consumer class will handle messages of type json and consume them to a calling object.
    """
    
    CONNECTION_PORT = 5672
    CREDS = pika.PlainCredentials('admin','admin')
    CONTENT_TYPE = 'application/json'
    
    def __init__(self, url, inputqueue, outputqueue, persist_data=False, mongo_dest="NA"):
        """ Create an instance of producer class
        :param str url: Broker DNS for rabbitmq svc
        
        :param str inputqueue: Name of Queue
        
        :param str mongo_dest: DB object for mongo collection to store data
        """
        if persist_data == True and mongo_dest == "NA":
            raise Exception("Mongo DB destination is required when persist_data is set.")
        if persist_data == True and mongo_dest != "NA":
            self.mongo_client = MongoClient(str(mongo_dest)+':27017')
            logger.info('Established connection with mongo client on {}:{}'.format(mongo_dest,'27017'))
            self.mydb=self.mongo_client["Delivery"]
        
        self.url = url
        self.inputqueue = inputqueue
        self.outputqueue = outputqueue
        self.properties = pika.BasicProperties(content_type=self.CONTENT_TYPE)
        self.persist_data = persist_data
        
    def connect(self):
        """ This method connects to RabbitMQ broker, and returns the connection handle.
        """
        logger.info('Connecting to {}'.format(self.url))
        self.channel = pika.BlockingConnection(pika.ConnectionParameters(self.url,self.CONNECTION_PORT,'/',self.CREDS)).channel()
        self.channel.queue_declare(queue=self.inputqueue, durable=True)
        self.channel.queue_declare(queue=self.outputqueue, durable=True)
        logger.info('Waiting for messages. To exit press Ctrl+C')
        
    def start_consumer(self):
        """
        This method initiates a consumer to given queue. 
        Uses the on_message method as callback on a message arrival for 
        acknowledgement.
        """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.inputqueue, on_message_callback=self.on_msg, auto_ack=False)
        logger.info('Starting Consumer.')
        self.channel.start_consuming()
        
    def on_msg(self, ch, method, properties, body):
        """
        This method prints the message received by the consumer.
        """
        logger.debug('Received a message.')
        logger.info(body.decode())
        logger.debug('Storing data to persistent data store.')
        self.channel.basic_ack(delivery_tag=method.delivery_tag)
        msg = body.decode()
        if (self.persist_data):
            self.store_msg(json_util.loads(msg))
        self.send_message(msg)
        
        
    def store_msg(self, msg):
        """
        This method stores the data recvd from queue to 
        persisitent mongo db pod.
        """
        self.mytab = self.mydb[msg['truck-number']]
        self.mytab.insert_one(msg)

    def send_message(self, msg):
        """
        This method gets the JSON data and sends it as a payload to RabbitMQ broker.
        :param dict msg: vehicle data to send
        """
        try:
            logging.debug('Sending data to queue {}'.format(self.outputqueue))
            self.channel.basic_publish(
                exchange='', routing_key=self.outputqueue, body=json.dumps(msg), properties=self.properties
            )
            logging.debug('Message sent successfully.')
        except Exception as e:
            logging.error('Failed to send message: {}'.format(str(e)))
