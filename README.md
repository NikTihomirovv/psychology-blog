# Psychology Blog API

Backend REST API для блога психолога, разработанный на Django и Django REST Framework.

Проект предоставляет API для публикации статей, категорий и комментариев, а также регистрацию и JWT-аутентификацию пользователей. Контентом можно управлять через Django Admin.

Проект контейнеризирован с помощью Docker и использует PostgreSQL в качестве базы данных.

## Возможности

- публикация и просмотр постов;
- статусы публикаций: `draft`, `published`, `archived`;
- автоматическая установка даты первой публикации;
- категории постов (Many-to-Many);
- несколько изображений для одного поста;
- публичный просмотр опубликованных постов;
- фильтрация постов по категории;
- комментарии только от авторизованных пользователей;
- модерация комментариев;
- регистрация пользователей;
- JWT-аутентификация;
- получение информации о текущем пользователе;
- Django Admin для управления контентом;
- OpenAPI-схема и Swagger UI;
- CORS;
- PostgreSQL;
- Docker Compose;
- Gunicorn;
- WhiteNoise для раздачи статических файлов;
- persistent Docker volumes для PostgreSQL и загруженных изображений;
- автоматические API-тесты.

## Стек

- Python 3.12
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- drf-spectacular
- django-cors-headers
- Gunicorn
- WhiteNoise
- Docker
- Docker Compose

## Структура проекта

```text
psychology_blog/
├── accounts/           # Пользователи, регистрация и аутентификация
├── blog/               # Посты, категории, изображения и комментарии
├── config/             # Настройки Django и корневые URL
├── compose.yaml        # Основная Docker Compose конфигурация
├── compose.dev.yaml    # Конфигурация для разработки
├── Dockerfile
├── entrypoint.sh
├── manage.py
└── requirements.txt
```

## API

### Посты

```text
GET /api/posts/
GET /api/posts/<uuid>/
```

Список содержит только опубликованные посты.

Поддерживается фильтрация по категории:

```text
GET /api/posts/?category=<category_uuid>
```

### Категории

```text
GET /api/categories/
```

### Комментарии

```text
POST /api/posts/<uuid>/comments/
```

Создавать комментарии могут только авторизованные пользователи.

Новые комментарии требуют модерации перед появлением в публичном API.

### Аутентификация

```text
POST /api/auth/register/
POST /api/auth/token/
POST /api/auth/token/refresh/
GET  /api/auth/me/
```

Для защищённых запросов используется JWT:

```text
Authorization: Bearer <access_token>
```

## Документация API

После запуска проекта доступны:

```text
Swagger UI:
http://localhost:8000/api/docs/

OpenAPI schema:
http://localhost:8000/api/schema/
```

## Переменные окружения

Создайте `.env` в корне проекта на основе `.env.example`:

```dotenv
SECRET_KEY=your-secret-key
DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173

DB_NAME=psychology_blog
DB_USER=psychology_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5433
```

Файл `.env` не должен добавляться в Git.

## Запуск через Docker

### Основной запуск

Соберите и запустите контейнеры:

```bash
docker compose up -d --build
```

Проверить состояние:

```bash
docker compose ps
```

Посмотреть логи backend:

```bash
docker compose logs backend
```

API будет доступен по адресу:

```text
http://localhost:8000/
```

При запуске backend автоматически выполняются миграции и сбор статических файлов.

### Режим разработки

Для запуска Django development server с подключением исходного кода:

```bash
docker compose -f compose.yaml -f compose.dev.yaml up -d --build
```

## PostgreSQL

PostgreSQL запускается в отдельном Docker-контейнере.

Данные базы хранятся в Docker volume:

```text
postgres_data
```

Внутри Docker backend подключается к PostgreSQL через:

```text
DB_HOST=db
DB_PORT=5432
```

При локальном запуске Django используется порт PostgreSQL, опубликованный на хосте:

```text
DB_HOST=localhost
DB_PORT=5433
```

## Media

Загруженные пользователями изображения сохраняются отдельно от файловой системы backend-контейнера.

Для этого используется Docker volume:

```text
media_data
```

Благодаря этому изображения сохраняются при пересоздании backend-контейнера.

## Тесты

Тесты покрывают основные сценарии API:

- получение опубликованных постов;
- недоступность черновиков через публичный API;
- фильтрацию по категориям;
- автоматическую дату публикации;
- получение категорий;
- создание комментариев;
- права доступа к комментариям;
- модерацию комментариев;
- регистрацию пользователей;
- хеширование паролей;
- получение JWT;
- доступ к данным текущего пользователя.

Запуск тестов внутри Docker:

```bash
docker compose exec backend python manage.py test blog.tests accounts.tests
```

## Администрирование

Для управления постами, категориями, изображениями и комментариями используется Django Admin:

```text
http://localhost:8000/admin/
```

Создать администратора:

```bash
docker compose exec backend python manage.py createsuperuser
```

## Архитектура

```text
Client
  │
  ▼
Django REST Framework
  │
  ├── Accounts API
  │     └── JWT authentication
  │
  ├── Blog API
  │     ├── Posts
  │     ├── Categories
  │     ├── Images
  │     └── Comments
  │
  ▼
Django ORM
  │
  ▼
PostgreSQL
```

В production-like Docker-конфигурации HTTP-запросы обрабатываются Gunicorn.

Статические файлы Django обслуживаются через WhiteNoise.

## Тестовое покрытие

В проекте реализовано 18 автоматических тестов основных API-сценариев.

```text
Ran 18 tests
OK
```

## Планы развития

- подключение frontend-приложения;
- восстановление пароля;
- расширение профиля пользователя;
- дополнительные API-фильтры;
- CI для автоматического запуска тестов;
- production deployment.