def parse_query(q: str):
    q = q.lower()
    filters = {}

    # Gender
    if "male" in q:
        filters["gender"] = "male"
    if "female" in q:
        filters["gender"] = "female"

    # Age logic
    if "young" in q:
        filters["min_age"] = 16
        filters["max_age"] = 24

    if "above" in q:
        try:
            num = int(q.split("above")[1].strip().split()[0])
            filters["min_age"] = num
        except:
            pass

    # Age group
    if "child" in q:
        filters["age_group"] = "child"
    if "teenager" in q:
        filters["age_group"] = "teenager"
    if "adult" in q:
        filters["age_group"] = "adult"
    if "senior" in q:
        filters["age_group"] = "senior"

    # Countries
    countries = {
        "nigeria": "NG",
        "kenya": "KE",
        "angola": "AO"
    }

    for name, code in countries.items():
        if name in q:
            filters["country_id"] = code

    return filters