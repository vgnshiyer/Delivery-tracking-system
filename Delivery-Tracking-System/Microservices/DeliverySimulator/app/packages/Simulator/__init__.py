import logging
import sys
import pika
import json

logger = logging.getLogger(__name__)

class RabitMQProducer(object):
    """ This producer class will handle messages of type json and produce them to a RabbitMQ queue.
    .
    .
    """
    
    CONNECTION_PORT = 5672
    CREDS = pika.PlainCredentials('admin','admin')
    CONTENT_TYPE = 'application/json'
    
    def __init__(self, url, queuename):
        """ Create an instance of producer class
        pass aqmp_url to open a connection with RabitMQ.
        
        :param str url: Broker DNS for rabbitmq svc
        
        pass queuename to produce messages.
        
        : param str queuename: Name of Queue
        """
        self.url = url
        self.queuename = queuename
        self.properties = pika.BasicProperties(content_type=self.CONTENT_TYPE)
            
    def connect(self):
        """ This method connects to RabbitMQ broker, and returns the connection handle.
        """
        logger.info('Connecting to {}'.format(self.url))
        self.channel = pika.BlockingConnection(pika.ConnectionParameters(self.url,self.CONNECTION_PORT,'/',self.CREDS)).channel()
    
    def send_message(self, msg):
        """This method gets the json data and sends it as a payload to RabbitMQ broker.    
    
        :param dict msg: vehicle data to send
        """
        logging.debug('Sending data to queue {}'.format(self.queuename))
        self.channel.basic_publish(exchange='', routing_key=self.queuename, body=json.dumps(msg),properties=self.properties)