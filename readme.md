# Bugs Away README

This Django application is designed to run with Python 3.11.5 and utilizes a PostgreSQL 16 database.

## Prerequisites

- Python 3.11.5
- PostgreSQL 16.x

## Initial Setup

1. **Virtual Environment Setup:**
   
   Before proceeding, create and activate a virtual environment using the provided YAML configuration file.

2. **PostgreSQL Setup:**
   
   Ensure PostgreSQL 16.x is installed and configured to run the database. Perform the following steps:

   - Create a PostgreSQL user `fsapp` with password `fsapp`.
   - Create a database named `fsapp` owned by the `fsapp` user.
   - Grant necessary privileges to the `fsapp` user to make changes.

   There are no available steps to create a populated database. 

## Database Migration

If setting up a fresh database, follow these steps:

1. Activate the virtual environment
2. Run the following commands to migrate the database schema. 
   
```bash
python manage.py makemigrations
python manage.py migrate
```

A default superuser will automatically be created with the following credentials:
   
- Username: `admin`
- Password: `admin`
   
This superuser account grants administrative privileges for managing the application.

## Running the Server

To start the server, execute the following command with the virtual environment active:

```bash
python manage.py runserver
```

Once the server is active, access the application via the following URL:

http://127.0.0.1:8000/