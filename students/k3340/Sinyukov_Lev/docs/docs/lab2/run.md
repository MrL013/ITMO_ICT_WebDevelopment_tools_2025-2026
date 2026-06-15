# Запуск проекта

## 1. Установка зависимостей

Для `task1` достаточно стандартного Python.

Для `task2` установите зависимости:

```bash
pip install -r task2/requirements.txt
```

## 2. Настройка окружения

Для `task2` заполните файл `task2/.env`.

Пример:

```env
DATABASE_URL=postgresql+psycopg2://postgres:0000@localhost:5432/travel_buddy_db
PARSER_USER_EMAIL=parser@travel-buddy.local
PARSER_USERNAME=web_parser
PARSER_TRIP_TITLE=Web parsing results
```

База данных должна совпадать с той, которая использовалась в лабораторной работе 1.

## 3. Запуск `task1`

```bash
cd task1
python threading_sum.py
python multiprocessing_sum.py
python async_sum.py
python compare.py
```

Проверка:

- все три программы должны вернуть одинаковую сумму
- `compare.py` должен вывести итоговое сравнение времени

## 4. Запуск `task2`

```bash
cd task2
python threading_parser.py
python multiprocessing_parser.py
python async_parser.py
python compare.py
python inspect_database.py
```

Проверка:

- в терминале должны печататься URL и заголовки страниц
- `compare.py` должен вывести время выполнения каждого подхода
- `inspect_database.py` должен показать записи в базе данных

## 5. Что смотреть в результатах

### Для `task1`

- корректность итоговой суммы
- различие во времени между `threading`, `multiprocessing` и `asyncio`

### Для `task2`

- успешное подключение к базе данных
- наличие служебного пользователя и служебной поездки
- добавление новых записей в таблицу `messages`
- сравнение времени выполнения трёх подходов
