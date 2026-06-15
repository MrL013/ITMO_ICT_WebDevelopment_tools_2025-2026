# PowerShell

На этой странице собраны команды PowerShell для полной проверки работоспособности `lab3`.

## 1. Когда использовать PowerShell

В проекте уже есть файл `test_main.http`, в котором собраны основные сценарии проверки. Если ваш редактор умеет выполнять `.http`-запросы, его удобнее использовать как основной способ тестирования.

PowerShell полезен, если нужно:

- проверить контейнеры и логи
- быстро отправить отдельный запрос вручную
- проверить Celery worker и регистрацию задач

## 2. Проверка контейнеров

```powershell
docker compose ps
```

## 3. Проверка логов

```powershell
docker compose logs api parser db celery_worker --tail=200
```

## 4. Проверка healthcheck основного API

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/" -Method Get
```

Ожидаемый результат:

```text
status
------
ok
```

## 5. Проверка healthcheck парсера

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8001/" -Method Get
```

## 6. Синхронный вызов парсера через основное API

```powershell
$body = @{
    url = "https://www.python.org"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/parser/parse" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

## 7. Прямой вызов отдельного парсер-сервиса

```powershell
$body = @{
    url = "https://www.djangoproject.com/"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8001/parse" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

## 8. Асинхронный вызов через Celery

```powershell
$body = @{
    url = "https://docs.python.org/3/"
} | ConvertTo-Json

$taskResponse = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/v1/parser/parse-async" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

$taskResponse
```

## 9. Проверка статуса асинхронной задачи

```powershell
$taskId = $taskResponse.task_id
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/parser/tasks/$taskId" -Method Get
```

Если задача ещё не завершилась:

```powershell
Start-Sleep -Seconds 2
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/parser/tasks/$taskId" -Method Get
```

## 10. Проверка регистрации Celery-задачи

```powershell
docker compose exec celery_worker celery -A app.celery_app.celery_app inspect registered
```

Ожидаемый результат:

```text
app.tasks.parse_url_task
```

## 11. Массовая проверка синхронного парсинга

```powershell
$urls = @(
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://palletsprojects.com/"
)

foreach ($url in $urls) {
    $body = @{ url = $url } | ConvertTo-Json
    Invoke-RestMethod `
        -Uri "http://127.0.0.1:8000/api/v1/parser/parse" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body
}
```
