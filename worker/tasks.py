import os
import uuid
from celery import Celery
import json
import elasticsearch
from datetime import datetime

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
    host = os.environ['LOGSTASH_1_PORT_9200_TCP_ADDR']

    es = elasticsearch.Elasticsearch([host])
    date = datetime.now().strftime("%Y.%m.%d")
    es.index(
        index='logstash-{date}'.format(date=date),
        doc_type='logstash',
        body=data,
        id=uuid.uuid4()
    )
