FROM python:3.13.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x ./scripts/*.sh