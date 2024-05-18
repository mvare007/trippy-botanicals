# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

# Install ODBC drivers for SQL Server
RUN apt-get update && \
    apt-get install -y curl && \
    curl https://packages.microsoft.com/keys/microsoft.asc > /etc/apt/trusted.gpg.d/microsoft.asc && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    ACCEPT_EULA=Y apt-get install -y mssql-tools18 && \
    apt-get clean

ENV PATH="${PATH}:/opt/mssql-tools/bin"

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY . .
RUN chmod a+x boot.sh

ENV FLASK_APP trippy.py

ARG FLASK_ENV
ENV FLASK_ENV=${FLASK_ENV}

ARG FLASK_SECRET_KEY
ENV FLASK_SECRET_KEY=${FLASK_SECRET_KEY}

ARG WTF_CSRF_SECRET_KEY
ENV WTF_CSRF_SECRET_KEY=${WTF_CSRF_SECRET_KEY}

ARG AZURE_STORAGE_CONTAINER_NAME
ENV AZURE_STORAGE_CONTAINER_NAME=${AZURE_STORAGE_CONTAINER_NAME}
ARG AZURE_STORAGE_CONNECTION_STRING
ENV AZURE_STORAGE_CONNECTION_STRING=${AZURE_STORAGE_CONNECTION_STRING}

ARG AZURE_DB_DRIVER
ENV AZURE_DB_DRIVER=${AZURE_DB_DRIVER}

ARG AZURE_DB_SERVER
ENV AZURE_DB_SERVER=${AZURE_DB_SERVER}

ARG AZURE_DB_NAME
ENV AZURE_DB_NAME=${AZURE_DB_NAME}

ARG AZURE_DB_USERNAME
ENV AZURE_DB_USERNAME=${AZURE_DB_USERNAME}

ARG AZURE_DB_PASSWORD
ENV AZURE_DB_PASSWORD=${AZURE_DB_PASSWORD}

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]