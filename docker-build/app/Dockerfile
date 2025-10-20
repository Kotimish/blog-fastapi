# Базовый образ
FROM python:3.12-trixie

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем poetry
RUN pip install --upgrade pip wheel poetry
RUN poetry config virtualenvs.create false

# Копируем файлы зависимостей
COPY poetry.lock pyproject.toml ./

# Устанавливаем зависимости
RUN poetry install --no-root

# Копируем остальную часть приложения
COPY app ./
COPY docker-build/app/entrypoint.sh ./


RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
