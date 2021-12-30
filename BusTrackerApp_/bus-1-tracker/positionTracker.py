import kafka
from kafka import KafkaConsumer
import json
from datetime import datetime
import time

from flask import Flask

app = Flask(__name__)
@app.route('/message/<int:number>/', methods=['GET'])
def get_message():
    consumer = KafkaConsumer(bootstrap_servers=['kafka:9071'],value_deserializer=lambda x:json.loads(x.encode('utf-8')))
    consumer.subscribe(['vignesh-test-topic'])
    consumer.seek(0, number)

    for msg in consumer:
        if msg.offset > number:
            break
        else:
            print msg

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

