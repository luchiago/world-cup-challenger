FROM python:3

ENV PYTHONBUFFERED 1

RUN mkdir /worldcup-api

WORKDIR /worldcup-api

COPY . /worldcup-api

RUN pip install -r requirements.txt
