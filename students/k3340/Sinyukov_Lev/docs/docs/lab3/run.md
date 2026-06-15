# Запуск проекта

## 1. Установка зависимостей для локального запуска

```bash
pip install -r requirements.txt
```

## 2. Настройка окружения

Пример:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/travel_buddy_db
SECRET_KEY=replace-with-long-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
PARSER_SERVICE_URL=http://parser:8001
PARSER_REQUEST_TIMEOUT=30
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
PARSER_USER_EMAIL=parser@travel-buddy.local
PARSER_USERNAME=web_parser
PARSER_TRIP_TITLE=Web parsing results
POSTGRES_DB=travel_buddy_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

## 3. Важное замечание по `DATABASE_URL`

Для Docker Compose в `DATABASE_URL` должен использоваться хост `db`, а не `localhost`, потому что подключение происходит между контейнерами внутри одной сети Docker.

Правильно:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/travel_buddy_db
```

## 4. Запуск через Docker Compose

```bash
docker compose up --build
```

## 5. Какие сервисы должны подняться

После старта должны работать следующие контейнеры:

- `db`
- `redis`
- `api`
- `parser`
- `celery_worker`

## 6. Доступные адреса

- основное API: `http://127.0.0.1:8000`
- Swagger основного API: `http://127.0.0.1:8000/docs`
- сервис парсера: `http://127.0.0.1:8001`

## 7. Основной способ тестирования

Для проекта подготовлен файл `test_main.http`, в котором уже собраны основные сценарии проверки:

- healthcheck основного API
- healthcheck отдельного сервиса парсера
- прямой вызов `parser`
- синхронный вызов парсера через основное API
- асинхронный вызов через Celery
- проверка статуса фоновой задачи
- базовые сценарии Travel Buddy из лабораторной работы 1

Если ваш редактор поддерживает `.http`-файлы, этот способ удобнее, чем вручную писать все команды в PowerShell.

## 8. Что проверить после запуска

### Основной API

- должен отвечать на `GET /`
- должен запускаться после выполнения Alembic миграций

### Парсер

- должен отвечать на `GET /`
- должен обрабатывать `POST /parse`

### Celery worker

- должен подключиться к Redis
- должен регистрировать задачу `app.tasks.parse_url_task`

## 9. Проверка логов

Если сервис не поднимается, проверьте логи:

```bash
docker compose logs api parser db celery_worker --tail=200
```

## 10. Альтернативный способ проверки

Если нужно тестировать не через `.http`-файл, подробные команды для PowerShell вынесены на отдельную страницу `PowerShell`.
