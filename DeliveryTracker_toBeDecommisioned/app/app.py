'''
This code performs below steps:
1. Expose endpoint /api/v1/vehicles/<vehiclename> to send current vehicle coordinates.
2. Expose endpoint /api/v1/vehicles/ to send known vehicles.
'''

from flask_cors import CORS
from flask import Flask, request
import json
from datetime import datetime
import os, sys
import pymongo
from pymongo import MongoClient
from bson import json_util
import logging

app = Flask(__name__)
CORS(app)

kafka_endpt = os.environ.get('KAFKA_BROKER_ENDPT')
mongo_endpt = os.environ.get('MONGO_DB_ENDPT')

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

@app.route('/api/v1/vehicles/<vehiclename>', methods=['GET'])
def sendCoords(vehiclename):
    logger.debug(request.headers)
    mydb=client["Delivery"]
    logger.info('Sending most recent coordinates for vehicle {}'.format(vehiclename))
    record = mydb[str(vehiclename)].find().sort([('$natural', -1)]).limit(1)[0]
    return json.loads(json_util.dumps(record))

@app.route('/api/v1/vehicles', methods=['GET'])
def sendVehicle():
    logger.debug(request.headers)
    mydb = client["Delivery"]
    vehicles = mydb.list_collection_names()
    logger.debug('Got data:')
    logger.debug(vehicles)
    return { "data":vehicles }

@app.route('/api/v1/health', methods=['GET'])
def healthCheck():
    logger.debug(request.headers)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == '__main__':
    initLogger()
    app.debug = True
    app.run(host='0.0.0.0', port=5000)