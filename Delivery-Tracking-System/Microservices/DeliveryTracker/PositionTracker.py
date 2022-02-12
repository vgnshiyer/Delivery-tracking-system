from flask_cors import Flask, CORS, Response
import json
from datetime import datetime
import os
import sys

app = Flask(__name__)
CORS(app)

kafka_endpt = os.environ.get('KAFKA_BROKER_ENDPT')
mongo_endpt = os.environ.get('MONGO_DB_ENDPT')
# topicname = os.environ.get('KAFKA_TOPIC_NAME')
topicNames = ["nano-delivery-truck","cargo-delivery-truck"]

client = MongoClient(str(mongo_endpt)+':27017')

def InitMongoDB(topicname):
    # dblist = client.list_database_names()
    # if "Delivery" not in dblist:
    mydb=client["Delivery"]
    mytab = mydb[topicname]
    return mytab

@app.route('/vehicles/'+str(topicname), methods=['GET'])
def sendCoords():
    mytab = InitMongoDB(topicname)
    # or use _id insteade of $natural
    record = mytab.find().sort({$natural:-1}).limit(1):
    return record[0]
    # return last row of mongo db

@app.route('/vehicles', methods=['GET'])
def sendVehicle():
    return {"data":topicNames}

# to implement
# endpoint to return track of a vehicle.

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)