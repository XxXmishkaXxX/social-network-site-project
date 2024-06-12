# Используем официальный образ Node.js
FROM node:20.13.0

# Устанавливаем рабочую директорию
WORKDIR /frontend/frontend/

# Копируем файл с зависимостями и устанавливаем их
COPY package.json /frontend/frontend/
COPY package-lock.json /frontend/frontend/
RUN npm install --force

# Копируем остальные файлы проекта
COPY . /frontend/frontend/

# Открываем порт
EXPOSE 8080

