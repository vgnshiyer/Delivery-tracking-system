import logging
import sys
import pika
import json

logger = logging.getLogger(__name__)

class RabbitMQConsumer(object):
    """ This consumer class will handle messages of type json and consume them to a calling object.
    .   
    .
    """
    
    CONNECTION_PORT = 5672
    CREDS = pika.PlainCredentials('admin','admin')
    CONTENT_TYPE = 'application/json'
    
    def __init__(self, url, queuename, mongo_dest):
        """ Create an instance of producer class
        :param str url: Broker DNS for rabbitmq svc
        
        :param str queuename: Name of Queue
        
        :param str mongo_dest: DB object for mongo collection to store data
        """
        self.url = url
        self.queuename = queuename
        self.properties = pika.BasicProperties(content_type=self.CONTENT_TYPE)
        self.dest = mongo_dest
        
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
        self.channel.basic_consume(queue=self.queuename, on_message_callback=self.on_msg)
        logger.info('Starting Consumer.')
        self.channel.start_consuming()
        
    def on_msg(self, ch, method, properties, body):
        """
        This method prints the message received by the consumer.
        """
        logger.debug('Received a message.')
        logger.info(body.decode())
        logger.debug('Storing data to persistent data store.')
        # self.store_msg(self.dest, body.decode())
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    def store_msg(self, dest, msg):
        """
        This method stores the data recvd from queue to 
        persisitent mongo db pod.
        """
        self.mytab = dest[msg['truck-type']]
        self.mytab.insert_one(msg)