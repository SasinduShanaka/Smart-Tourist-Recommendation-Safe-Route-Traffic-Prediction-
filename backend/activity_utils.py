def get_activities(travel_style):
    mapping = {
        "Adventure": ["Hiking", "Surfing"],
        "Relaxation": ["Relaxing"],
        "Cultural": ["Sightseeing"],
        "Wildlife": ["Safari"]
    }
    return mapping.get(travel_style, [])
