import kafka
from kafka import KafkaConsumer
import json
from datetime import datetime
import time

consumer = KafkaConsumer(bootstrap_servers=['kafka:9071'],value_deserializer=lambda x:json.loads(x.encode('utf-8')))
consumer.subscribe(['vignesh-test-topic-2'])

for message in consumer:
    print(message)

