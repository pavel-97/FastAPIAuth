FROM alpine:3.14
WORKDIR /app

# Устанавливаем зависимости приложения.
RUN apk add --no-cache --update nmap-ncat

# Добавляем в образ скрипт для запуска эхо-сервера и устанавливаем разрешение на выполнение.
COPY start.sh .
RUN chmod +x start.sh