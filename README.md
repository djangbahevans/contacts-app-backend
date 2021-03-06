# Contacts App API

Simple Contacts API using FastAPI

## Description

A simple CRUD contacts API using FastAPI

## Getting Started

### Demonstration

This project is hosted on Heroku. You can run a demonstration [here](https://tranquil-river-56095.herokuapp.com).  
You can checkout supported endpoints [here](https://tranquil-river-56095.herokuapp.com/docs).  
A demo of the frontend of this application is available at <https://evans-contacts-app.herokuapp.com>

### Dependencies

* FastAPI
* SQLAlchemy
* Python-Jose
* PostgreSQL

### Installing

* [PostgreSQL](https://www.postgresql.org/download/)
* [Python 3.7+](https://www.python.org/downloads/)

### Executing program

* Clone the project

```bash
git clone https://github.com/djangbahevans/contacts-app-backend.git
cd contacts-app-backend
```

* Create virtual environment and install dependencies

```bash
python -m venv venv

source venv/bin/activate # MacOS/Linux bash
venv/Scripts/Activate.ps1 # Powershell
venv/Scripts/activate.bat # Command prompt

pip3 install -r requirements.txt
```

* Set up .env file and populate these fields

```env
DATABASE_HOSTNAME=database_hostname_name
DATABASE_PORT=database port, typically 5432
DATABASE_PASSWORD=database_password_value
DATABASE_NAME=contacts_app
DATABASE_USERNAME=database_username_value
SECRET_KEY=jwt_secret_key_value
ALGORITHM=jwt_algorithm value, typically HS256
ACCESS_TOKEN_EXPIRE_MINUTES=jwt expire minutes in integers
```

* Run server

```terminal
uvicorn app.main:app --reload
```

## Authors

Evans Djangbah  
[@djangbahevans](https://twitter.com/djangbahevans)

<!-- ## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details -->

## Acknowledgments

<!-- Inspiration, code snippets, etc. -->

* [Python API Development - Comprehensive Course for Beginners](https://www.youtube.com/watch?v=0sOvCWFmrtA)
