FROM ubuntu:latest
#FROM python:3.7-alpine
ADD . /code
WORKDIR /code
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
RUN   pip install -r requirements.txt
CMD ["python", "app/main.py"]

#FROM mysql/mysql-server
