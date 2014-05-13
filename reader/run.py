import os
import tweepy
import pika

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_key = os.environ['ACCESS_KEY']
access_secret = os.environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser)

connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBIT_1_PORT_5672_TCP_ADDR']))
channel = connection.channel()
channel.queue_declare(queue='default')


class RabbitStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        channel.basic_publish(
            exchange='',
            routing_key='default',
            body=status.text
        )


def run():
    sapi = tweepy.streaming.Stream(auth, RabbitStreamListener())
    sapi.sample()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        connection.close()
