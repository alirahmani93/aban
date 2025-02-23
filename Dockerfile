FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING=utf-8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client netcat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
ADD . /code
