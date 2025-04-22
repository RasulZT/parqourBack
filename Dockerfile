FROM python:3.11-slim-buster

RUN apt update && apt install -y \
    sudo \
    nano \
    gcc \
    libpq-dev \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-wheel \
    cmake \
    && apt clean

# Обновляем pip и связанные инструменты
RUN pip install --upgrade pip wheel setuptools

# Устанавливаем cmake (если нужен через pip)
RUN pip install cmake

WORKDIR /django

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]