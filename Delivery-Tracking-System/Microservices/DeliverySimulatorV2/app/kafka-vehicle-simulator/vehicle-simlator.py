import kafka
from kafka import KafkaProducer
import json
from datetime import datetime
import time
import threading
import os, sys, traceback
import logging

# setting custom logger format
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        # logger.removeHandler(handler)
        handler.setFormatter(logging.Formatter(FORMAT))
else:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(FORMAT))
        logger.addHandler(handler)
# setting logger mode
logger.setLevel(logging.DEBUG)