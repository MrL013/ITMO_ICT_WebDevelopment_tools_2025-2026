# Лабораторная работа 1. Реализация серверного приложения FastAPI

Разработка веб-приложения для поиска партнеров в путешествие.

## Что реализовано

- FastAPI + SQLAlchemy + PostgreSQL
- Alembic миграции
- 5 таблиц и связи:
  - `users`
  - `profiles` (one-to-one с `users`)
  - `trips` (one-to-many: `users -> trips`)
  - `messages` (one-to-many: `trips -> messages`, `users -> messages`)
  - `trip_participants` (many-to-many между `users` и `trips` + поля `status`, `note`, `joined_at`)
- Полный CRUD для поездок и сообщений, профиль пользователя
- Поиск поездок (вручную через SQLAlchemy-фильтры, без сторонних библиотек поиска)
- Регистрация/авторизация
- JWT токены
- Аутентификация через Bearer token
- Хэширование паролей
- API для `me`, списка пользователей и смены пароля

## Технологии

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- JWT (`python-jose`)
- `passlib` + `bcrypt`
