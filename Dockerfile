FROM ubuntu:20.04
# python
RUN apt-get update && apt-get install -y \
    python3-pip
# create parent directories
RUN mkdir /app
RUN mkdir /data_rootdir
RUN mkdir /data_augmented
# install requirements
COPY requirements.txt /app
RUN pip3 install -r app/requirements.txt
# this is needed by soundfile
RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \
    libsndfile1
# create subdirs and copy project source code
RUN mkdir assets
RUN mkdir assets/dataset
RUN mkdir cache
COPY assets/header.css /app/assets/
COPY assets/typography.css /app/assets/
COPY config /app/config
COPY callbacks /app/callbacks
COPY utils /app/utils
COPY views /app/views
COPY app.py /app
COPY AudioDataAugmentator.py /app
# start at /app directory when running
WORKDIR /app
# run the app with gunicorn