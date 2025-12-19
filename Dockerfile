# Используем официальный лёгкий Python образ
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Копируем код приложения
COPY . .

# Открываем порт
EXPOSE 8000

# Запускаем сервер
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
