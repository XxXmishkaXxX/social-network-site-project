# Используем официальный образ Python 3.12.3
FROM python:3.12.3-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /backend/core/

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt /backend/core/
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта
COPY . /backend/core/

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Открываем порт
EXPOSE 8000

