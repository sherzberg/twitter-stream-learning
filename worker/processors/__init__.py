from dateutil import parser
from twitter_text.extractor import Extractor
from urlparse import urlparse
import requests


def timestamp(data):
    date = parser.parse(data['created_at'])
    stamp = date.isoformat()
    return {'@timestamp': stamp}


def hashtags(data):
    text = data.get('text', '')
    hashtags = Extractor(text).extract_hashtags()
    return {'hashtags': hashtags}


def urls(data):
    text = data.get('text', '')
    urls = Extractor(text).extract_urls()
    if urls:
        return {'urls': urls}
    else:
        return {}


def domains(data):
    text = data.get('text', '')
    urls = Extractor(text).extract_urls()

    if urls:
        resolved = [requests.get(url).url for url in urls]
        domains = [urlparse(url)[1] for url in resolved]
        return {'domains': domains}
    else:
        return {}
