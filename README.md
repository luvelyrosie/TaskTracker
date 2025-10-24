# TaskTracker

TaskTracker — это веб-приложение для управления задачами, построенное с использованием FastAPI и PostgreSQL. Приложение позволяет создавать, редактировать и удалять задачи, а также управлять пользователями с полной авторизацией.

## Требования

* Docker и Docker Compose
* Python 3.11 (опционально, если хотите запускать без Docker)
* PostgreSQL (через Docker)

## Установка и запуск

1. Склонируйте репозиторий:

```bash
git clone https://github.com/luvelyrosie/TaskTracker.git
cd TaskTracker
```

2. Запустите приложение через Docker:

```bash
docker-compose up --build
```

## Доступ к приложению

* Главная страница: [http://localhost:8000/](http://localhost:8000/)
* Dashboard задач: [http://localhost:8000/tasks](http://localhost:8000/tasks)
* SwaggerUI: [http://localhost:8000/docs](http://localhost:8000/docs)
* Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Использование

* На Dashboard вы можете:

  * Создавать новые задачи
  * Просматривать детали задачи
  * Редактировать задачи
  * Удалять задачи

## Авторизация и API

* Для доступа к административному API необходимо создать пользователя с ролью `admin`.
* После аутентификации вы можете использовать SwaggerUI для работы со всеми доступными API.
* Основные маршруты:

  * `/users/register-page` — регистрация пользователя
  * `/users/login-page` — вход и получение JWT токена
  * `/users/me` — информация о текущем пользователе
  * `/users/logout` — выход

## Технологии и особенности

* FastAPI с асинхронными маршрутами
* SQLAlchemy ORM с PostgreSQL
* Хранение паролей в виде хэша (bcrypt / passlib)
* JWT-токены для авторизации
* Docker для простого развертывания
* SwaggerUI и Redoc для удобной документации API