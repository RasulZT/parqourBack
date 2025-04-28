FROM python:3.11-slim-buster

RUN apt update && apt install -y \
    gcc \
    libpq-dev \
    python3-dev \
    python3-pip \
    nano \
    cmake \
    && apt clean

RUN pip install --upgrade pip wheel setuptools cmake

WORKDIR /django

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Запускаем DAPHNE с нужным портом
CMD ["daphne", "-b", "0.0.0.0", "-p", "8001", "ParqourBotBack.asgi:application"]
