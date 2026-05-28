# API

## Аутентификация и пользователи

- `POST /api/v1/auth/register` - регистрация
- `POST /api/v1/auth/login` - вход
- `POST /api/v1/auth/change-password` - смена пароля
- `GET /api/v1/users/me` - текущий пользователь
- `GET /api/v1/users` - список пользователей

## Профили

- `POST /api/v1/profiles/me` - создать профиль
- `PUT /api/v1/profiles/me` - обновить профиль
- `GET /api/v1/profiles/me` - получить профиль

## Поездки

- `POST /api/v1/trips/` - создать поездку
- `GET /api/v1/trips/` - список поездок с вложенными объектами
- `GET /api/v1/trips/{trip_id}` - получить поездку с вложенными объектами
- `PUT /api/v1/trips/{trip_id}` - обновить поездку
- `DELETE /api/v1/trips/{trip_id}` - удалить поездку
- `POST /api/v1/trips/search` - ручной поиск поездок

## Участники поездки

- `POST /api/v1/trips/{trip_id}/join` - заявка на участие
- `PATCH /api/v1/trips/{trip_id}/participants/{user_id}` - изменение статуса участника

## Сообщения

- `GET /api/v1/trips/{trip_id}/messages/` - список сообщений
- `POST /api/v1/trips/{trip_id}/messages/` - создать сообщение
- `PUT /api/v1/trips/{trip_id}/messages/{message_id}` - обновить сообщение
- `DELETE /api/v1/trips/{trip_id}/messages/{message_id}` - удалить сообщение
