import os
from celery import Celery
import json

host = os.environ['RABBIT_1_PORT_5672_TCP_ADDR']
app = Celery('tasks', broker='amqp://guest:guest@{host}'.format(host=host))


@app.task
def process_tweet(message):
    print json.loads(message)
    return True
