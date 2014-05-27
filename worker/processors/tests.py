from unittest import TestCase

from processors import timestamp, hashtags
from datetime import datetime
import pytz


class TimestampProcessorTest(TestCase):

    def test_happy_path(self):
        data = {'created_at': 'Sun May 25 14:55:05 +0000 2014'}

        returned = timestamp(data)

        date = datetime(2014, 5, 25, 14, 55, 5)
        date = date.replace(tzinfo=pytz.utc)

        self.assertTrue('@timestamp' in returned)
        self.assertEqual(returned['@timestamp'], date.isoformat())


class HashtagProcessorTest(TestCase):

    def test_single_hashtag(self):
        data = {'text': 'Hi there! #yolo'}

        returned = hashtags(data)

        self.assertTrue('hashtags' in returned)
        self.assertEqual([u'yolo'], returned['hashtags'])

    def test_multiple_hashtags(self):
        data = {'text': 'Hi there! #yolo #anotherone'}

        returned = hashtags(data)

        self.assertTrue('hashtags' in returned)
        self.assertEqual(set([u'yolo', u'anotherone']), set(returned['hashtags']))
