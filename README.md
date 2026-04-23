# Insighta Labs — Intelligence Query Engine (Stage 2)

## Overview

This project is a backend API built with Python (FastAPI) that powers an **intelligent demographic query engine** for Insighta Labs.

It enables clients (marketing teams, product teams, analysts) to:

* Filter demographic data efficiently
* Sort and paginate results
* Query data using **plain English (natural language)**

The system transforms raw stored data into a **searchable, flexible, and intelligent API**.

---

## Tech Stack

* **Python (FastAPI)**
* **PostgreSQL**
* **SQLAlchemy (ORM)**
* **Uvicorn (ASGI server)**

---

## Database Schema

Table: `profiles`

| Field               | Type       | Description                       |
| ------------------- | ---------- | --------------------------------- |
| id                  | UUID v7    | Primary key                       |
| name                | VARCHAR    | Unique full name                  |
| gender              | VARCHAR    | male / female                     |
| gender_probability  | FLOAT      | Confidence score                  |
| age                 | INT        | Exact age                         |
| age_group           | VARCHAR    | child / teenager / adult / senior |
| country_id          | VARCHAR(2) | ISO country code                  |
| country_name        | VARCHAR    | Full country name                 |
| country_probability | FLOAT      | Confidence score                  |
| created_at          | TIMESTAMP  | UTC ISO 8601                      |

---

## Data Seeding

The database is seeded with **2026 profiles from a JSON file**.

### Key Behavior:

* Prevents duplicate records using:

  * Unique constraint on `name`
  * Pre-insert existence check

### Run Seeder:

```bash
python seed/seed.py
```

---

## API Endpoints

---

###  GET `/api/profiles`

Supports **filtering, sorting, and pagination** in one request.

#### Supported Filters

* `gender`
* `age_group`
* `country_id`
* `min_age`
* `max_age`
* `min_gender_probability`
* `min_country_probability`

####  Sorting

* `sort_by`: `age` | `created_at` | `gender_probability`
* `order`: `asc` | `desc`

####  Pagination

* `page` (default: 1)
* `limit` (default: 10, max: 50)

####  Example:

```
/api/profiles?gender=male&country_id=NG&min_age=25&sort_by=age&order=desc&page=1&limit=10
```

---

### GET `/api/profiles/search`

Performs **natural language query parsing** and converts it into filters.

#### Example:

```
/api/profiles/search?q=young males from nigeria
```

---

#  Natural Language Parsing Approach

This system uses a **rule-based parser** (no AI/LLMs).

The query string is:

1. Converted to lowercase
2. Matched against predefined keywords
3. Translated into structured filters

---

##  Supported Keywords & Mappings

### Gender

| Keyword | Filter          |
| ------- | --------------- |
| male    | `gender=male`   |
| female  | `gender=female` |

---

### Age Logic

| Phrase  | Mapping                    |
| ------- | -------------------------- |
| young   | `min_age=16`, `max_age=24` |
| above X | `min_age=X`                |

Example:

* "females above 30" → `gender=female`, `min_age=30`

---

### Age Group

| Keyword  | Filter               |
| -------- | -------------------- |
| child    | `age_group=child`    |
| teenager | `age_group=teenager` |
| adult    | `age_group=adult`    |
| senior   | `age_group=senior`   |

---

###  Country Mapping

A dictionary maps country names to ISO codes:

| Country | Code |
| ------- | ---- |
| nigeria | NG   |
| kenya   | KE   |
| angola  | AO   |

Example:

* "people from angola" → `country_id=AO`

---

##  Combined Queries

All extracted filters are **combined using AND logic**.

Example:

```
"adult males from kenya"
```

Becomes:

```
gender=male AND age_group=adult AND country_id=KE
```

---

##  Unrecognized Queries

If no valid keywords are found:

```json
{
  "status": "error",
  "message": "Unable to interpret query"
}
```

---

#  Limitations of the Parser

This is a **rule-based system**, so it has some constraints:

###  Not Supported

* Complex sentence structures
* Synonyms (e.g., "guys", "ladies")
* Misspellings (e.g., "nigerai")
* Multiple countries in one query
* Ranges like "between 20 and 30"
* Logical OR conditions
* Advanced NLP understanding

---

### Edge Cases

* "male and female" → may override one gender
* "above" parsing depends on correct number format
* Only predefined countries are recognized

---

# ⚙️ Error Handling

All errors follow this format:

```json
{
  "status": "error",
  "message": "..."
}
```

### Error Types:

* **400** → Missing parameter
* **422** → Invalid type
* **404** → Not found
* **Invalid query parameters** → Wrong filters

---

# Additional Requirements Implemented

* CORS enabled:

```
Access-Control-Allow-Origin: *
```

* ✅ Pagination limit capped at 50
* ✅ UTC ISO 8601 timestamps
* ✅ Duplicate-safe seeding
* ✅ Combined filtering logic
* ✅ Structured response format

---

#  Performance Considerations

* Query filtering is done at the database level (no full-table scans)
* Indexed fields (e.g., name) improve lookup speed
* Pagination prevents large data loads

---

#  Running the Project

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Run server:

```bash
uvicorn app.main:app --reload
```

### Access docs:

```
http://127.0.0.1:8000/docs
```

---

# Deployment

The API is deployed on a cloud platform (AWS).

---

# Summary

This project successfully delivers:

* Advanced filtering
* Multi-condition querying
* Sorting and pagination
* Rule-based natural language search
* Clean and consistent API responses

It transforms static demographic data into a **fully queryable intelligence system**.

---

# 👨‍💻 Author

Backend Wizards Stage 2 Submission
Insighta Labs Assessment
