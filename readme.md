Uses Python 3.11.5
Uses a postgresql 16 database. 

admin admin@gmail.com admin


To setup new run or dev environment:

Create a new virtual environment using the yml

Setup Postgresql 16.x to run the database.
Currently no steps to migrate database are setup, create a user fsapp with password fsapp.
Create a database fsapp owned by fsapp. Make sure the user has privileges to make changes.

In the case it's a fresh database, run migrate.bat, potentially make modifications to the venv path of the script.
It is not necessary to create a superuser, a superuser will automatically be created with username admin and password admin.


The server can be run by running 
python manage.py runserver

Once the server is active the app is usable on
http://127.0.0.1:8000/


