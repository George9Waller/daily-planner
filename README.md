# What is it?
A service that connects to a receipt printer to print a daily planning note. It has modules for the date, a greeting, [Habitica](https://habitica.com/) integration (todos and habits) and notes.

The service is split up into processes for printing, fetching data and a web ui displaying print status and a visual representation of the latest reciept.

I deployed the project in kubernetes on a cluster to learn how all of that works. The helm charts are in this repo and integrate with my global charts in https://github.com/George9Waller/helm

Inspired by https://amanvir.com/guten

<img src="https://github.com/user-attachments/assets/2aa1a3a4-22be-4633-845f-c8949dfb2ea4" width="450">
<img src="https://github.com/user-attachments/assets/d0c84f10-c993-4750-9cc4-859c315bd1f1" width="300">


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
