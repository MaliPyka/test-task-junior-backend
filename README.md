# Instagram Sync Service

Сервис для синхронизации постов из Instagram Graph API.

## Технологии
* Python 3.12, Django, DRF
* Celery, Redis
* PostgreSQL
* Docker, Docker Compose

## Запуск проекта

### 1. Склонируйте репозиторий:
```bash
git clone <repository_url>
cd <project_dir>
```

### 2. Создайте файл .env в корне проекта и заполните его своими данными:
```
# База данных
POSTGRES_DB=test_task_db
POSTGRES_USER=test_user
POSTGRES_PASSWORD=super_secret_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Instagram API
IG_TOKEN=твой_инстаграм_токен

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
```


### 3. Запустите сборку и контейнеры:


```bash
docker-compose up --build
```

## Эндпоинты

### GET /api/posts/ — вывод всех сохраненных постов из БД.

### POST /api/sync/ — запуск задачи на синхронизацию постов.

### POST /api/posts/{id}/comment/ — добавление комментария к посту.
