# syntax=docker/dockerfile:1

FROM python:3.11-slim-bookworm

WORKDIR /app

# Install ODBC drivers for SQL Server
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        gnupg \
        unixodbc-dev && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    curl -fsSL https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 mssql-tools18 && \
    apt-get purge -y --auto-remove curl gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="${PATH}:/opt/mssql-tools18/bin"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY . .
RUN chmod a+x docker_entrypoint.sh

# Static configuration only - no secrets at build time
ENV FLASK_APP=trippy.py

EXPOSE 8000

ENTRYPOINT ["./docker_entrypoint.sh"]
