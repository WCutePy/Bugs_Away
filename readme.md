Uses Python 3.11.0

pgAdmin 4

super user with: manage.py createsuperuser
admin admin@gmail.com admin


To setup new run or dev environment:

Create a new virtual environment using Python 3.11.0
Some scripts exist to potentially aid in this.

Setup Postgresql 16.x to run the database.
Currently no steps to migrate database are setup, create a user fsapp with password fsapp.
Create a database fsapp owned by fsapp. Make sure the user has privileges to make changes.

In the case it's a fresh database, run migrate.bat, potentially make modifications to the venv path of the script.
It is not necessary to create a superuser, a superuser will automatically be created with username admin and password admin.

art is stolen from https://pikaole.tumblr.com/
no permission has been received for the usage of the art.