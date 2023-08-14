'''
This code does below:
1. Expose endpoint /api/vehicles/<topicname> to stream vehicle coordinates.
2. Expose endpoint /api/vehicles/ to give list of vehicles.
'''

from flask import Flask, request
import flask
from flask_cors import CORS
import json
import os
import requests
import time
import logging

app = Flask(__name__)
CORS(app)

delivery_tracker_endpt = os.environ.get('DELIVERY_TRACKER_ENDPT')

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

def sendEvents(topicname):
    while(1):
        res = requests.get('http://'+str(delivery_tracker_endpt)+':5000/api/v1/vehicles/'+str(topicname)) ## convert to rpc later
        time.sleep(3)
        yield 'data:{0}\n\n'.format(res.json())

@app.route('/api/vehicles/<vehiclename>', methods=['GET'])
def stream(vehiclename):
    logger.info('Sending most recent coordinates every 3 seconds.')
    return flask.Response(sendEvents(vehiclename), mimetype='text/event-stream')

@app.route('/api/vehicles', methods=['GET'])
def getVehicles():
    logger.debug(request.headers)
    res = requests.get('http://'+str(delivery_tracker_endpt)+':5000/api/v1/vehicles')
    res.raise_for_status()
    if res.status_code != 204:
        return res.json()

@app.route('/', methods=['GET'])
def index():
    logger.debug(request.headers)
    return '<H3>Welcome To Delivery Tracking System API. Please hit /api/vehicles/<vehicle-name> path to get vehicle coordinates.</H3>'

if __name__ == '__main__':
    initLogger()
    app.debug = True
    app.run(host='0.0.0.0', port=5000)