# Запуск проекта

## 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 2. Настройка окружения

Создайте `.env`

Пример:

```env
DATABASE_URL=postgresql+psycopg2://postgres:0000@localhost:5432/travel_buddy_db
SECRET_KEY=replace-with-long-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 3. Миграции

```bash
alembic upgrade head
```

## 4. Запуск приложения

```bash
uvicorn app.main:app --reload
```

## 5. Swagger

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)