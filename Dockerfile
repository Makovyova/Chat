# Используем базовый образ Python
FROM python:3.10.12

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем команду для запуска Django приложения
CMD ["python", "mytelegrambot/manage.py", "runserver", "0.0.0.0:8000"]
