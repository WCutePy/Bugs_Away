@echo off
call C:\pythonVenvs\FrameShooter\Scripts\activate 
python manage.py makemigrations
python manage.py migrate
deactivate