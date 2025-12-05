#!/usr/bin/env bash
set -e

echo "Running Alembic migrations..."
cd src
alembic upgrade head

echo "Starting the application..."
uvicorn main:app --host '0.0.0.0' --port 8080
