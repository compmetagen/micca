FROM compmetagen/rdpclassifier:2.11
MAINTAINER Davide Albanese <davide.albanese@gmail.com>

RUN apt-get update && apt-get install -y \
    build-essential \
    python2.7 \
    python-pip \
    python-dev \
    python-numpy \
    python-scipy \
    python-matplotlib \
    git \
  && pip install --upgrade pip \
  && pip install 'setuptools >=14.0' \
  && git clone https://github.com/compmetagen/micca.git /tmp/micca/ \
  && pip install /tmp/micca/ \
  && rm -rf /var/lib/apt/lists/* /tmp/micca
