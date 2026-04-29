# Insighta Labs — Intelligence Query Engine (Stage 2)

## Overview

A FastAPI backend that powers an intelligent demographic query engine. Enables filtering, sorting, pagination, and natural language search on demographic profiles.

## Tech Stack

- **Python** (FastAPI)
- **SQLite** (database)
- **SQLAlchemy** (ORM)
- **Uvicorn** (server)

## Project Structure

```
HNG_Stage_Two_Task/
├── app/
│   ├── main.py        # FastAPI app & endpoints
│   ├── database.py    # DB connection
│   ├── models.py      # SQLAlchemy models
│   ├── schemas.py     # Pydantic schemas
│   └── parser.py      # Natural language parser
├── seed/
│   ├── profiles.json  # Seed data
│   └── seed.py        # Seeder script
├── requirements.txt
└── Procfile
```

## Database Schema

| Field               | Type    | Description                       |
|---------------------|---------|-----------------------------------|
| id                  | UUID    | Primary key                       |
| name                | VARCHAR | Unique full name                  |
| gender              | VARCHAR | male / female                     |
| gender_probability  | FLOAT   | Confidence score                  |
| age                 | INT     | Exact age                         |
| age_group           | VARCHAR | child / teenager / adult / senior |
| country_id          | VARCHAR | ISO country code                  |
| country_name        | VARCHAR | Full country name                 |
| country_probability | FLOAT   | Confidence score                  |
| created_at          | TIMESTAMP | UTC timestamp                   |

## API Endpoints

### GET `/api/profiles`

Filter, sort, and paginate profiles.

**Query Parameters:**
- `gender` — male / female
- `age_group` — child / teenager / adult / senior
- `country_id` — ISO country code
- `min_age` / `max_age` — Age range
- `sort_by` — age / created_at / gender_probability
- `order` — asc / desc
- `page` — Page number (default: 1)
- `limit` — Items per page (default: 10, max: 50)

**Example:**
```
/api/profiles?gender=male&country_id=NG&min_age=25&sort_by=age&order=desc&page=1&limit=10
```

### GET `/api/profiles/search`

Natural language search (rule-based parser).

**Example:**
```
/api/profiles/search?q=young males from nigeria
```

Supported keywords: male, female, young, above X, child, teenager, adult, senior, country names (nigeria, kenya, angola).

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

# Access docs
http://127.0.0.1:8000/docs
```

## Features

- ✅ CORS enabled
- ✅ Pagination (max 50)
- ✅ Duplicate-safe seeding
- ✅ Combined filtering (AND logic)
- ✅ Structured JSON responses

---

**Backend Wizards Stage 2 Submission**
