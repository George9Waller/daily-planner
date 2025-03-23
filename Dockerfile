# syntax=docker/dockerfile:1

FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    gettext \
    build-essential \
    libpq-dev \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN bash /app/scripts/translations

RUN chmod +x /app/scripts/start-hosted
RUN chmod +x /app/scripts/migrate
RUN chmod +x /app/scripts/listen-for-print
