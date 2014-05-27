from dateutil import parser
from twitter_text.extractor import Extractor


def timestamp(data):
    date = parser.parse(data['created_at'])
    stamp = date.isoformat()
    return {'@timestamp': stamp}


def hashtags(data):
    text = data.get('text', '')
    hashtags = Extractor(text).extract_hashtags()
    return {'hashtags': hashtags}
