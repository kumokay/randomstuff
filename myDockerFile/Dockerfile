# Use an official Python runtime as a parent image
FROM ubuntu:trusty
RUN apt-get update 
#&& apt-get install -y --no-install-recommends apt-utils

# install some tools
RUN apt-get -y install git wget

# install python packages
RUN apt-get -y install python-pip
RUN pip install --upgrade pip
RUN pip install msgpack-rpc-python
RUN pip install numpy

RUN mkdir -p /opt/github
WORKDIR /opt/github
RUN git clone https://github.com/kumokay/sharescript.git

# RUN apt-get -y install iputils-ping

# assign entrypoint workdir
WORKDIR /opt/github/sharescript/airsim
RUN date > date.txt

