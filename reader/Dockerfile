FROM stackbrew/ubuntu:14.04

WORKDIR /app

RUN apt-get update -qq
RUN apt-get install python-dev python-pip -y

ADD . /app

RUN pip install -r requirements.txt
