#!/bin/sh
set -e

wait_for_postgres() {
  echo "Waiting for Postgres..."
  while ! nc -z db 5432; do
    sleep 1
  done
  echo "Postgres is up!"
}

wait_for_postgres

cd backend/

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI app..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload