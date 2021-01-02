# The Button

A simple time tracking service.

[![Requirements Status](https://requires.io/github/MashSoftware/the-button/requirements.svg?branch=main)](https://requires.io/github/MashSoftware/the-button/requirements/?branch=main)

## Prerequisites

### Required

- Python 3.6.x or higher
- Postgres 9.5.x or higher

### Optional

- Redis 5.0.x or higher (for rate limiting, otherwise in-memory storage is used)

## Getting started

### Create local Postgres database

```shell
sudo service postgresql start
sudo su - postgres -c "create user mash with password mash"
sudo su - postgres -c "createdb button"
sudo -u postgres psql
grant all privileges on database button to mash;
```

### Create venv and install requirements

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Run database migrations

```shell
flask db upgrade
```

### Run app

```shell
flask run
```

## Testing

Run the test suite

```shell
python tests.py
```
