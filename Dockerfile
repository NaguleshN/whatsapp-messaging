FROM python:3.12-alpine

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt
COPY . /app
