# Лабораторная работа 2. Потоки. Процессы. Асинхронность.

В этой лабораторной работе реализованы два задания, посвященные сравнению подходов `threading`, `multiprocessing` и `asyncio`.

## Что реализовано

- `task1` — сравнение трх подходов на задаче вычисления суммы чисел от `1` до `10_000_000_000_000`
- `task2` — параллельный парсинг веб-страниц с сохранением результатов в базу данных из лабораторной работы 1
- отдельные скрипты для каждого подхода: `threading`, `multiprocessing`, `asyncio`
- сценарии `compare.py` для сравнения времени выполнения
- скрипт `inspect_database.py` для проверки подключения к базе данных и просмотра сохранённых записей

## Структура проекта

- `task1/threading_sum.py`
- `task1/multiprocessing_sum.py`
- `task1/async_sum.py`
- `task1/compare.py`
- `task2/threading_parser.py`
- `task2/multiprocessing_parser.py`
- `task2/async_parser.py`
- `task2/compare.py`
- `task2/inspect_database.py`

## Используемые технологии

- `Python`
- `threading`
- `multiprocessing`
- `asyncio`
- `aiohttp`
- `PostgreSQL`
- `SQLAlchemy`
- `pydantic-settings`

## Основные выводы

- для очень лёгких вычислений с формулой наименьшее время показывают `asyncio` и `threading`, а `multiprocessing` проигрывает из-за накладных расходов
- для сетевого I/O-парсинга наиболее эффективным оказался `asyncio`
- `threading` хорошо подходит для задач с ожиданием сетевых ответов
- `multiprocessing` обычно полезнее для тяжёлых CPU-bound вычислений, а не для веб-запросов
