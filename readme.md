Twitter Streaming API Learning
==============================

Repo that sets up twitter stream api readers. Uses
Docker containers!

The plan is to use:

* RabbitMQ for a message queue
* Python to read twitter stream data
* Python to parse relevant twitter data
 * Tweets with links
 * Tweets with hashtags
 * Tweet emoji
* One of [Logstash, Graylog, statsd, etc] to do data aggregation and graphing

Requirements:
-------------

* Docker 0.8.1
* Fig 0.3.2

This project was created using these versions. It may
work with newer versions. I'll upgrade when I get a chance.

Running
-------

Once `docker` and `fig` are installed and configured:

```bash
$ fig up -d rabbit
```

Navigate to `http://localhost:8888` to view the running
rabbitmq instance.

```bash
$ fig up -d reader
```

On the rabbitmq webpage, view the messages per second.

```bash
$ fig scale reader=4
```

Watch the messages per second rise!

Tasks
-----

 - [x] Pipe Twitter stream to a message queue (`fig up -d reader`)
 - [ ] Pull from queue and parse data (`fig up worker`)
 - [ ] Graph live data
