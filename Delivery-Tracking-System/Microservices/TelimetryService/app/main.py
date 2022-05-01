import logging
import sys, os, traceback
from packages import Consumer
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
    logger.setLevel(logging.INFO)
    # fhandler = logging.FileHandler('app.logs')
    # fhandler.setFormatter(logging.Formatter(LOG_FORMAT))
    # logger.addHandler(handler)
    
    mq_client = Consumer.RabbitMQConsumer(mq_url, queuename, persist_data=True, mongo_dest=mongo_endpt)
    mq_client.connect()
    mq_client.start_consumer()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        excp = sys.exc_info()
        tb = sys.exc_info()[-1]
        stk = traceback.extract_tb(tb, 2)
        fname = stk[-1][2]
        logger.info("The program exited with the following error message at "+str(fname)+": \n")
        logger.error(e)
