import kafka
from kafka import KafkaConsumer
import json
from datetime import datetime
import time
from flask_cors import CORS
from flask import Flask
from flask import Response

app = Flask(__name__)
CORS(app)
# initialize consumer
consumer = KafkaConsumer(bootstrap_servers=['kafka:9071'],value_deserializer=lambda x:json.loads(x.encode('utf-8')))

def get_message(topicname):
    consumer.subscribe([topicname])
    for msg in consumer:
        yield 'data:{0}\n\n'.format(json.dumps(msg))

@app.route('/messages/<string:topicname>/', methods=['GET'])
def stream():
    return Response(get_message(topicname), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

