FROM debian:8.3
RUN apt-get update

# install prerequisites for micca
RUN apt-get install -y \
    build-essential \
    python2.7 \
    python-pip \
    python-dev \
    python-numpy \
    python-scipy \
    python-matplotlib
RUN pip install --upgrade pip
RUN pip install 'setuptools >=14.0'

# install the RDP classifier
RUN apt-get install -y zip wget default-jre
ENV RDPZIP=rdp_classifier_2.11.zip
ENV RDPPATH=/rdp_classifier_2.11
ENV RDPDOWNLOAD=https://sourceforge.net/projects/rdp-classifier/files/rdp-classifier/$RDPZIP/download
RUN wget $RDPDOWNLOAD -O /tmp/$RDPZIP && \
    unzip /tmp/$RDPZIP -d /

# install micca
RUN apt-get install -y git
RUN git clone https://github.com/compmetagen/micca.git /tmp/micca/
RUN pip install /tmp/micca/

RUN rm -rf /var/lib/apt/lists/* /tmp/*

MAINTAINER Davide Albanese <davide.albanese@gmail.com>
