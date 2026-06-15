# API

## Базовый функционал Travel Buddy

В проекте сохранены endpoint-ы из лабораторной работы 1:

- `POST /api/v1/auth/register` — регистрация пользователя
- `POST /api/v1/auth/login` — вход в систему
- `POST /api/v1/auth/change-password` — смена пароля
- `GET /api/v1/users/me` — получение текущего пользователя
- `GET /api/v1/users` — получение списка пользователей
- `POST /api/v1/profiles/me` — создание профиля
- `PUT /api/v1/profiles/me` — обновление профиля
- `GET /api/v1/profiles/me` — получение профиля
- `POST /api/v1/trips/` — создание поездки
- `GET /api/v1/trips/` — список поездок
- `GET /api/v1/trips/{trip_id}` — получение поездки
- `PUT /api/v1/trips/{trip_id}` — обновление поездки
- `DELETE /api/v1/trips/{trip_id}` — удаление поездки
- `POST /api/v1/trips/search` — поиск поездок
- `POST /api/v1/trips/{trip_id}/join` — заявка на участие
- `PATCH /api/v1/trips/{trip_id}/participants/{user_id}` — изменение статуса участника
- `GET /api/v1/trips/{trip_id}/messages/` — список сообщений
- `POST /api/v1/trips/{trip_id}/messages/` — создание сообщения
- `PUT /api/v1/trips/{trip_id}/messages/{message_id}` — обновление сообщения
- `DELETE /api/v1/trips/{trip_id}/messages/{message_id}` — удаление сообщения

## Новые endpoint-ы парсинга

### Синхронный вызов через основное API

- `POST /api/v1/parser/parse`

Основное приложение принимает URL, обращается к отдельному сервису парсера и возвращает клиенту результат.

Пример тела запроса:

```json
{
  "url": "https://www.python.org"
}
```

Пример ответа:

```json
{
  "message": "Parsing completed",
  "url": "https://www.python.org/",
  "title": "Welcome to Python.org",
  "parser_type": "http-parser",
  "trip_id": 1,
  "author_id": 1,
  "message_id": 1,
  "created_at": "2026-06-14T22:08:14.265791Z"
}
```

### Асинхронный вызов через Celery и Redis

- `POST /api/v1/parser/parse-async`

Этот endpoint принимает URL и ставит задачу на парсинг в очередь.

Пример ответа:

```json
{
  "task_id": "3b4163e8-a1b0-46bf-b10e-40b2f6f042b9",
  "status": "PENDING",
  "message": "Parsing task has been queued"
}
```

### Проверка статуса фоновой задачи

- `GET /api/v1/parser/tasks/{task_id}`

Позволяет узнать состояние задачи:

- `PENDING` — задача поставлена в очередь
- `STARTED` — задача выполняется
- `SUCCESS` — задача завершена успешно
- `FAILURE` — задача завершилась ошибкой

Пример успешного результата:

```json
{
  "task_id": "3b4163e8-a1b0-46bf-b10e-40b2f6f042b9",
  "status": "SUCCESS",
  "result": {
    "message": "Parsing completed",
    "url": "https://docs.python.org/3/",
    "title": "3.14.6 Documentation",
    "parser_type": "celery",
    "trip_id": 1,
    "author_id": 1,
    "message_id": 1,
    "created_at": "2026-06-14T22:12:46.6Z"
  },
  "error": null
}
```

## Отдельный сервис парсера

Парсер также доступен напрямую в отдельном контейнере:

- `GET /` — healthcheck
- `POST /parse` — прямой вызов парсинга

Этот сервис используется основным API для синхронного сценария.
