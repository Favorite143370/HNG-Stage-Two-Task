import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Profile

db = SessionLocal()

# Get correct file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "profiles.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# ✅ FIX: handle stringified JSON items safely
for item in data:

    # If item is a string, convert it into dict
    if isinstance(item, str):
        try:
            item = json.loads(item)
        except json.JSONDecodeError:
            continue  # skip bad record

    # Validate structure before inserting
    if not isinstance(item, dict) or "name" not in item:
        continue

    exists = db.query(Profile).filter(Profile.name == item["name"]).first()

    if not exists:
        profile = Profile(**item)
        db.add(profile)

db.commit()
db.close()

print("Seeding complete")