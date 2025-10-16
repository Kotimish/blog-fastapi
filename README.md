## Веб-приложение Блог на FastAPI

### Установка

1. **Клонируем репозиторий и переходим в папку проекта**
    - По HTTP
    ```bash
    git clone https://github.com/Kotimish/blog-fastapi.git
    ```
   - Или по SSH
    ```bash
    git clone git@github.com:Kotimish/blog-fastapi.git
    ```
    - Переходим в созданную папку проекта
    ```bash
    cd blog-fastapi
    ```
2. **Создаем виртуальное окружение**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    Примечание: Убедитесь, что ваша версия Python не ниже 3.12.
    При необходимости указывайте явно версию Python при создании окружения.

    К примеру (для Python3.12)
    ```bash
    python3.12 -m venv .venv
    source .venv/bin/activate
    ```
3. **Устанавливаем необходимые пакеты с помощью poetry**
    ```bash
    poetry install
    ```
   Если poetry отсутствует, то установите его по следующей инструкции: [ссылка](https://python-poetry.org/docs/#installation)
4. **Копируем файл окружения**
   ```bash
   cp .env.default .env
   ```
    По необходимости измените параметры файла
5. **Запуск локальной БД PostgresQL**
   - **Запускаем Docker-Compose**
       ```bash
       docker compose up -d
       ```
   - **Инициализация таблиц**
       ```bash
       alembic upgrade head
       ```