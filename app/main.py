from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Profile
from fastapi.middleware.cors import CORSMiddleware
from app.parser import parse_query
from app.schemas import ProfileResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Insighta API is running"}

# CORS (REQUIRED)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ENDPOINT
@app.get("/api/profiles")
def get_profiles(
    gender: str = None,
    age_group: str = None,
    country_id: str = None,
    min_age: int = None,
    max_age: int = None,
    min_gender_probability: float = None,
    min_country_probability: float = None,
    sort_by: str = "created_at",
    order: str = "asc",
    page: int = 1,
    limit: int = 10
):
    db: Session = SessionLocal()

    query = db.query(Profile)

    # Filters
    if gender:
        query = query.filter(Profile.gender == gender)

    if age_group:
        query = query.filter(Profile.age_group == age_group)

    if country_id:
        query = query.filter(Profile.country_id == country_id)

    if min_age:
        query = query.filter(Profile.age >= min_age)

    if max_age:
        query = query.filter(Profile.age <= max_age)

    if min_gender_probability:
        query = query.filter(Profile.gender_probability >= min_gender_probability)

    if min_country_probability:
        query = query.filter(Profile.country_probability >= min_country_probability)

    # Sorting
    if order == "desc":
        query = query.order_by(getattr(Profile, sort_by).desc())
    else:
        query = query.order_by(getattr(Profile, sort_by))

    total = query.count()

    results = query.offset((page - 1) * limit).limit(limit).all()

    db.close()

    return {
        "status": "success",
        "page": page,
        "limit": limit,
        "total": total,
        "data": [ProfileResponse.model_validate(r) for r in results]
    }

# SEARCH ENDPOINT
@app.get("/api/profiles/search")
def search_profiles(q: str, page: int = 1, limit: int = 10):
    db = SessionLocal()

    filters = parse_query(q)
    query = db.query(Profile)

# STRUCTURED FILTERS

    query = db.query(Profile)

    if "gender" in filters:
        query = query.filter(Profile.gender == filters["gender"])

    if "age_group" in filters:
        query = query.filter(Profile.age_group == filters["age_group"])

    if "min_age" in filters:
        query = query.filter(Profile.age >= filters["min_age"])

    if "max_age" in filters:
        query = query.filter(Profile.age <= filters["max_age"])

    if "country_id" in filters:
        query = query.filter(Profile.country_id == filters["country_id"])

# FREE-TEXT SEARCH
    if q:
            query = query.filter(Profile.name.ilike(f"%{q}%"))    

    total = query.count()

    results = query.offset((page - 1) * limit).limit(limit).all()

    db.close()

    return {
        "status": "success",
        "page": page,
        "limit": limit,
        "total": total,
        "data": [ProfileResponse.model_validate(r) for r in results]
    }