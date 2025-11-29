# TaskTracker

TaskTracker is a web application for task management, built using FastAPI and PostgreSQL. The application allows creating, editing, and deleting tasks, as well as managing users with full authorization.

## Requirements

* Docker and Docker Compose
* Python 3.11 (optional, if you want to run without Docker)
* PostgreSQL (via Docker)

## Installation and Running

1. Clone the repository:

```bash
git clone https://github.com/luvelyrosie/TaskTracker.git
cd TaskTracker
```

2. Start the application via Docker:

```bash
docker-compose up --build
```

## Accessing the Application

* Home page: [http://localhost:8000/](http://localhost:8000/)
* Task Dashboard: [http://localhost:8000/tasks](http://localhost:8000/tasks)
* SwaggerUI: [http://localhost:8000/docs](http://localhost:8000/docs)
* Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Usage

* On the Dashboard, you can:

  * Create new tasks
  * View task details
  * Edit tasks
  * Delete tasks

## Authorization and API

* To access the administrative API, you need to create a user with the `admin` role.
* After authentication, you can use SwaggerUI to work with all available APIs.
* Main routes:

  * `/users/register-page` — user registration
  * `/users/login-page` — login and JWT token retrieval
  * `/users/me` — current user information
  * `/users/logout` — logout

## Technologies and Features

* FastAPI with asynchronous routes
* SQLAlchemy ORM with PostgreSQL
* Passwords stored as hashes (bcrypt / passlib)
* JWT tokens for authorization
* Docker for easy deployment
* SwaggerUI and Redoc for convenient API documentation




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