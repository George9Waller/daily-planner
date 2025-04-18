# What is it?
todo

# Setup
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

# Services
- A [postgres](https://www.postgresql.org) DB
- A [redis](https://redis.io) server
- An [Open Weather](https://openweathermap.org/api) API key
- A [habitica account](https://habitica.com) with an API token

# Env vars
- `BABEL_DEFAULT_LOCALE` "fr_FR" or "en_GB"
- `DATABASE_URL`
- `OPEN_WEATHER_API_KEY`
- `HABITICA_USER_ID`
- `HABITICA_API_TOKEN`
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_PASSWORD`

# Scripts
## `makemigrations`
Makes a migration to reflect db changes compared to the current state of the db

## `migrate`
Applies all unapplied migrations to the db

## `start`
Locally starts the web server on 127.0.0.1:5000

## `translations`
1. Collects all translatable strings in the project and updates the `.po` files.
2. Compiles the `.po` files into `.mo` files used by the server to inject translations.

## `listen-for-print`
*Only works on linux*

Starts a process listening for the p key to be pressed on a mounted keyboard device and triggers a print job

## `lint`
Lints with black, isort and helm. The same linting is done in GitHub actions on PRs
