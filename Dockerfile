# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY . .
RUN chmod a+x boot.sh

ENV FLASK_APP trippy.py
ARG FLASK_ENV
ENV FLASK_ENV=${FLASK_ENV}



EXPOSE 8000

ENTRYPOINT ["./boot.sh"]