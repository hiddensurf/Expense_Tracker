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

## Local setup

### 1. Clone and create an environment

```bash
git clone https://github.com/hiddensurf/Expense_Tracker.git
cd Expense_Tracker
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install the Python packages used by the project

This repository does not currently include a lock file or requirements file. Install the runtime packages before starting it:

```bash
pip install fastapi "uvicorn[standard]" sqlmodel "psycopg[binary]" alembic pydantic-settings pyjwt pwdlib python-multipart
```

### 3. Configure PostgreSQL

Create a PostgreSQL database, then add a `.env` file in the repository root:

```env
DATABASE_USER=postgres
DATABASE_PASSWORD=replace_me
DATABASE_PORT=5432
DATABASE_DB=expense_tracker
DATABASE_HOST=localhost
SECRET_KEY=replace_with_a_long_random_secret
ALGORITHM=HS256
TIME_TO_EXPIRE=30
```

`TIME_TO_EXPIRE` is read as the access-token lifetime in minutes.

### 4. Run migrations and start the API

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
```
