FROM debian:8.3
RUN apt-get update && apt-get install -y \
    build-essential \
    python2.7 \
    python-pip \
    python-dev \
    python-numpy \
    python-scipy \
    python-matplotlib
RUN rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install 'setuptools >=14.0'
RUN pip install micca==1.2.0

MAINTAINER Davide Albanese <davide.albanese@gmail.com>