# Django

A repo to manage database schema, admin panel web-ui and a place to keep all the logic.

## Run With Docker

After cloning the project requirements need to be installed. We use `docker` (`docker compose`) for both development and
deployment and production/staging servings of stateless services.

## Web Service

* Database is PostgreSQL: So uncomment Postgres Database configs in settings
```bash
  docker compose up --build -d
```

## Run with manage.py

Install requirements:

```bash
  pip install -r requirements
```

Export Settings:
```bash
export DJANGO_SETTINGS_MODULE=aban.settings.development
```

Migrate files:

```bash
  ./manage.py migrate
```

Run server:

```bash
  ./manage.py runserver 
```
