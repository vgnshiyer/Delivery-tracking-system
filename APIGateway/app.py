from flask import Flask
import flask
import time
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

def initialize():
    f = open('bus_data.json')
    busData = json.load(f)
    busData = busData['features'][0]['geometry']['coordinates']
    return busData

def generateBusRecord(coordinates):
    busRecord = {
        "name": "Ghansoli-Vashi",
        "busNumber": 9,
        "timestamp": (datetime.utcnow()).strftime("%d/%m/%Y %H:%M:%S"),
        "coordinates": { "latitude": coordinates[0], "longitude": coordinates[1]}
    }
    return busRecord

def sendEvents(busData):
    i=0
    #produce coordinates infinitely
    while(i<len(busData)):
        busRecord=generateBusRecord(busData[i])
        time.sleep(3)
        yield 'data:{0}\n\n'.format(json.dumps(busRecord))
        i+=1
        if i==len(busData):
            busData = busData[::-1]
            i=0       

@app.route('/messages', methods=['GET'])
def stream():
    busData = initialize()
    return flask.Response(sendEvents(busData), mimetype='text/event-stream')

@app.route('/', methods=['GET'])
def index():
    return '<H3>Please hit /messages path to get message streams.</H3>'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)