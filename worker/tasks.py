import os
from celery import Celery
import json
import socket

from processors import timestamp, hashtags

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
    for function in [timestamp, hashtags]:
        extra = function(data)
        blob = dict(blob.items() + extra.items())

    return blob


def send_to_logstash(data):
    server_address = (os.environ['LOGSTASH_1_PORT_5555_TCP_ADDR'], 5555, )
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    sock.sendall(json.dumps(data))
