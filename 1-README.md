# Expense Tracker API

A FastAPI and PostgreSQL backend for recording purchases, organizing them by category, and returning user-scoped expense summaries.

## What the code demonstrates

- OAuth2 password flow with signed JWT access tokens
- Password hashing and active-user checks
- Admin/user roles, including admin-only category writes
- User-scoped purchase CRUD so authenticated users operate on their own records
- Purchase filters plus per-category and per-month summary queries
- CSV parsing and import through a FastAPI background task
- SQLModel persistence and Alembic migrations

## API areas

| Area | Examples |
| --- | --- |
| Authentication | Register, login, current-user lookup |
| Users | Read and update the authenticated user |
| Categories | Read categories; admin-only create, update, and delete |
| Purchases | Create, list, filter, update, and delete user-owned purchases |
| Reporting | Purchase summary grouped by category and month |
| Imports | Parse CSV rows and queue purchase creation in a background task |

Interactive OpenAPI docs are available at `/docs` while the API is running.

## Run with Docker Compose

```bash
git clone https://github.com/hiddensurf/Expense_Tracker.git
cd Expense_Tracker
cp .env.example .env
docker compose up --build
```

This starts PostgreSQL and the API, applies the Alembic migrations on startup, and serves the interactive docs at http://localhost:8000/docs. Change `DATABASE_PASSWORD` and `SECRET_KEY` in `.env` before using it for anything beyond a local demo.

## Run locally without Docker

```bash
git clone https://github.com/hiddensurf/Expense_Tracker.git
cd Expense_Tracker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

Create a PostgreSQL database that matches the values in `.env` (`TIME_TO_EXPIRE` is the access-token lifetime in minutes), then:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try the routes.

## CSV import

The import route accepts a CSV file. A background task reads rows with `csv.DictReader` and creates purchase records for the authenticated user. Include the purchase fields expected by the database model: `item_name`, `description` (optional), `purchased_at`, `amount`, and `category_id`.

## Project structure

```text
app/
├── auth/          # OAuth2/JWT and password helpers
├── categories/    # category routes and models
├── database/      # SQLModel engine and sessions
├── purchases/     # purchase CRUD, queries, summaries, CSV import
├── users/         # user routes and models
└── main.py        # FastAPI application and routers
alembic/            # migration environment and revisions
config.py           # environment-backed settings
Dockerfile, compose.yaml, .env.example   # one-command local setup
```
