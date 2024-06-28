FROM python:3.11.9-bookworm

COPY requirements.txt /temp/requirments.txt

COPY config /config

WORKDIR /config
EXPOSE 8088
RUN pip install -r  /temp/requirments.txt 

RUN adduser --disabled-password  service-user

USER service-user