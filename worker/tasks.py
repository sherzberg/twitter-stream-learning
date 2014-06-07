import os
from celery import Celery
import json
import socket
import pika

from processors import timestamp, hashtags, urls, domains

host = os.environ['RABBIT_1_PORT_5672_TCP_ADDR']
app = Celery('tasks', broker='amqp://guest:guest@{host}'.format(host=host))


@app.task
def process_tweet(message):
    data = json.loads(message)

    blob = process_pipeline(data)

    blob['raw'] = data

    send_to_logstash(blob)

    return True


def process_pipeline(data):
    blob = {}
    for function in [timestamp, hashtags, urls, domains]:
        extra = function(data)
        blob = dict(blob.items() + extra.items())

    return blob


def send_to_logstash(data):
    server_address = os.environ['RABBIT_1_PORT_5672_TCP_ADDR']

    connection = pika.BlockingConnection(pika.ConnectionParameters(server_address))
    channel = connection.channel()
    channel.queue_declare(queue='logstash')
    channel.basic_publish(exchange='', routing_key='logstash', body=json.dumps(data))
    connection.close()
