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
2. **Копируем файл окружения**
   ```bash
   cp .env.default .env
   ```
    По необходимости измените параметры файла

3. **Запуск приложения через docker-compose**
   ```bash
   docker compose up
   ```
   
### Заполнение БД демо-данными (опционально)

Для удобства разработки и тестирования можно загрузить демо-данные из [JSONPlaceholder](https://jsonplaceholder.typicode.com):
 
```bash
python -m scripts.seed_db
```
Скрипт запускается в контейнере
