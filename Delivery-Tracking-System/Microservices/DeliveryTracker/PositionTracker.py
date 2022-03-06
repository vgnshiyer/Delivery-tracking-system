from pydoc_data.topics import topics
from flask_cors import CORS
from flask import Flask
import json
from datetime import datetime
import os, sys
import pymongo
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)
CORS(app)

kafka_endpt = os.environ.get('KAFKA_BROKER_ENDPT')
mongo_endpt = os.environ.get('MONGO_DB_ENDPT')

client = MongoClient(str(mongo_endpt)+':27017')

@app.route('/api/v1/vehicles/<topicname>', methods=['GET'])
def sendCoords(topicname):
    mydb=client["Delivery"]
    record = mydb[topicname.replace("-","_")].find().sort([('$natural', -1)]).limit(1)[0]
    return json.loads(json_util.dumps(record))

@app.route('/api/v1/vehicles', methods=['GET'])
def sendVehicle():
    mydb = client["Delivery"]
    vehicles = mydb.list_collection_names()
    vehicles = [vehicle.replace("_","-") for vehicle in vehicles]
    return { "data":vehicles }

@app.route('/api/v1/healthz', methods=['GET'])
def healthCheck():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

# to implement
# endpoint to return track of a vehicle.

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)