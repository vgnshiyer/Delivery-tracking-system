import logging
import sys, os, traceback
from pymongo import MongoClient
import random

#VARS
mongo_endpt = os.environ.get('MONGO_DB_ENDPT')
mongo_port = '27017'
mq_url = os.environ.get('RABBITMQ_URL')
queuename = os.environ.get('QUEUE')

LOG_FORMAT = '%(asctime)s - %(lineno)s:%(funcName)s - %(levelname)s - %(message)s'
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(handler)

def CalSpeed():
    logger.info('Caluclating vehhicle speed.')
    speed = random.randrange(20,100,3)
    return speed

def main():
    mongo_client = MongoClient(str(mongo_endpt)+':'+mongo_port)
    logger.info('Established connection with mongo client on {}:{}'.format(mongo_endpt,mongo_port))
    mydb=client["Delivery"]
    
    mq_client = Consumer.RabitMQConsumer(mq_url, queuename, mydb)
    mq_client.connect()
    mq_client.start_consumer()

if __name__ == '__main__':
    try:
        main()
    except:
        excp = sys.exc_info()
        tb = sys.exc_info()[-1]
        stk = traceback.extract_tb(tb, 2)
        fname = stk[-1][2]
        logger.info("The program exited with the following error message at "+str(fname)+": \n")
        logger.error(e)
