def parse_user_text(text):
    text = text.lower()

    # Defaults (safe fallbacks)
    preferences = {
        "weather": "Warm",
        "travel_style": "Relaxation",
        "budget": "Medium",
        "trip_duration": "Short",
        "crowd_level": "Moderate",
        "month": "January"
    }

    # Weather
    if any(word in text for word in ["cool", "chill", "cold", "hill"]):
        preferences["weather"] = "Cool"
    elif any(word in text for word in ["hot", "warm", "beach"]):
        preferences["weather"] = "Warm"

    # Travel style
    if any(word in text for word in ["adventure", "hiking", "trek", "climb"]):
        preferences["travel_style"] = "Adventure"
    elif any(word in text for word in ["relax", "calm", "peace"]):
        preferences["travel_style"] = "Relaxation"
    elif any(word in text for word in ["culture", "temple", "heritage"]):
        preferences["travel_style"] = "Cultural"
    elif any(word in text for word in ["wildlife", "safari", "animals"]):
        preferences["travel_style"] = "Wildlife"

    # Budget
    if any(word in text for word in ["low budget", "cheap", "budget"]):
        preferences["budget"] = "Low"
    elif any(word in text for word in ["luxury", "high budget", "expensive"]):
        preferences["budget"] = "High"

    # Trip duration
    if any(word in text for word in ["week", "7 days", "long trip"]):
        preferences["trip_duration"] = "Long"
    elif any(word in text for word in ["few days", "short trip", "2 days", "3 days"]):
        preferences["trip_duration"] = "Short"

    # Crowd preference
    if any(word in text for word in ["no crowd", "less crowd", "quiet"]):
        preferences["crowd_level"] = "Low"
    elif any(word in text for word in ["crowded", "busy"]):
        preferences["crowd_level"] = "Crowded"

    # Month detection
    months = [
        "january","february","march","april","may","june",
        "july","august","september","october","november","december"
    ]
    for month in months:
        if month in text:
            preferences["month"] = month.capitalize()

    return preferences
