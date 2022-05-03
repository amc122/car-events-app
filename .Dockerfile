ARG BASE_IMAGE=ubuntu:20.04
ARG PYTHON_VERSION=3.8

RUN apt-get update && apt-get install -y \
    python3-pip \
    wget \
    git

RUN mkdir /apps
RUN cd /apps

RUN git clone https://github.com/amc122/car-events-app

RUN cd car-events-app
RUN pip install -r requirements.txt

WORKDIR .

CMD python3 app.py
