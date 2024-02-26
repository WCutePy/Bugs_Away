@echo off
call venv\Scripts\activate
python manage.py makemigrations
python manage.py migrate
deactivate