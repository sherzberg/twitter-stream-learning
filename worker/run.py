import os
import tweepy
import json

import tasks

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_key = os.environ['ACCESS_KEY']
access_secret = os.environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


class RabbitStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        tasks.process_tweet.delay(json.dumps(status._json))


def run():
    sapi = tweepy.streaming.Stream(auth, RabbitStreamListener())
    sapi.sample()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        pass
