#!/bin/bash
echo "Creating Migrations users..."
python manage.py makemigrations authuser
echo "==================================="

echo "Creating Migrations todo_list..."
python manage.py makemigrations todo_list
echo "==================================="

echo "Starting Migrations..."
python manage.py migrate
echo "==================================="

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000
echo "update host http://localhost:8000/"