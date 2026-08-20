# Expense Tracker API

A RESTful Expense Tracker API built with **FastAPI**, **SQLModel**, and **PostgreSQL**. The application provides secure JWT-based authentication, expense management, category management, expense summaries, and bulk CSV import functionality.

## Features

- JWT Authentication
- User registration and login
- CRUD operations for expenses
- CRUD operations for expense categories
- Role-based authorization (Admin/User)
- Expense filtering with query parameters
- Expense summary and analytics
- Bulk expense upload using CSV
- Background task support for large CSV uploads
- SQLModel ORM
- PostgreSQL database
- Alembic database migrations

---

## Tech Stack

- FastAPI
- SQLModel
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- OAuth2 Password Flow
- JWT Authentication

---

## Project Structure

```text
expense_tracker/
│
├── app/
│   ├── auth/
│   ├── users/
│   ├── purchases/
│   ├── categories/
│   ├── database/
│   └── main.py
│
├── alembic/
├── config.py
├── alembic.ini
└── .env
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/expense_tracker.git

cd expense_tracker
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate

Linux/Mac

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```env
database_user=postgres
database_password=password
database_host=localhost
database_port=5432
database_db=expense_tracker

secret_key=YOUR_SECRET_KEY
algorithm=HS256
time_to_expire=30
```

---

## Database Migration

Generate migration

```bash
alembic revision --autogenerate -m "Initial migration"
```

Apply migration

```bash
alembic upgrade head
```

---

## Run the API

```bash
fastapi dev app/main.py
```

The API will be available at

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# Authentication

## Register

```
POST /signup
```

Creates a new user account.

---

## Login

```
POST /token
```

Returns a JWT access token.

Authorize subsequent requests using

```
Authorization: Bearer <token>
```

---

# Users

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/users` | List users |
| GET | `/users/{id}` | Get user |
| PATCH | `/users/me` | Update logged-in user |
| DELETE | `/users/me` | Delete account |
| GET | `/users/me/purchases` | Get current user's purchases |

---

# Categories

| Method | Endpoint |
|---------|----------|
| GET | `/categories` |
| GET | `/categories/{id}` |
| POST | `/categories` *(Admin)* |
| PATCH | `/categories/{id}` *(Admin)* |
| DELETE | `/categories/{id}` *(Admin)* |
| GET | `/categories/purchases/{id}` *(Admin)* |

---

# Purchases

| Method | Endpoint |
|---------|----------|
| GET | `/purchases/me` |
| GET | `/purchases/me/{id}` |
| POST | `/purchases/me` |
| PATCH | `/purchases/me/{id}` |
| DELETE | `/purchases/me/{id}` |
| GET | `/purchases/summary` |

---

## Expense Filtering

The purchases endpoint supports filtering using query parameters.

Examples

```
GET /purchases/me?category_id=2
```

```
GET /purchases/me?min_amount=100&max_amount=500
```

```
GET /purchases/me?item_name=Milk
```

```
GET /purchases/me?purchased_in_or_after=2026-07-01
```

Supported filters include:

- Purchase ID
- Category
- Item name
- Minimum amount
- Maximum amount
- Purchase date range
- Entry date range

---

# Expense Summary

The summary endpoint aggregates expenses into useful insights.

```
GET /purchases/summary
```

Returns information such as:

- Total spending by category
- Monthly spending
- Top spending categories

---

# Bulk CSV Upload

The application supports importing expenses from CSV files.

CSV upload is processed using FastAPI Background Tasks so the API can return immediately while processing continues in the background.

Example CSV

```csv
item_name,amount,purchased_at,category_id
Rice,1200,2026-07-10,1
Milk,45,2026-07-10,1
Chair,2500,2026-07-15,2
```

---

## Security

- Passwords are securely hashed before storage.
- JWT access tokens are used for authentication.
- Protected endpoints require authentication.
- Administrative operations require admin privileges.

---

## Future Improvements

- Docker support
- CI/CD pipeline
- Unit and integration testing
- Expense budgets
- Spending alerts
- Charts and dashboards
- Export reports to CSV/PDF
- Email notifications

---

## Author

**Aabin Joseph**

B.Tech Computer Science (AI & ML)

Backend & AI Engineering Enthusiast