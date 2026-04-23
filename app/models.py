from sqlalchemy import Column, String, Integer, Float, TIMESTAMP
from .database import Base
from datetime import datetime
import uuid

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    gender = Column(String)
    gender_probability = Column(Float)
    age = Column(Integer)
    age_group = Column(String)
    country_id = Column(String(2))
    country_name = Column(String)
    country_probability = Column(Float)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)