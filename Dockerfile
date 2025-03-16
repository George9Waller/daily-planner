# syntax=docker/dockerfile:1

FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y gettext

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN bash /app/scripts/translations
