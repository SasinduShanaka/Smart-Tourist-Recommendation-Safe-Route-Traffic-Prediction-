import pandas as pd
import os
from season_utils import get_season
from activity_utils import get_activities

# Get the correct path to the CSV file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(base_dir, 'data', 'places.csv')
df = pd.read_csv(csv_path)

def recommend_places_scored(
    weather,
    travel_style,
    month,
    budget,
    trip_duration,
    crowd_level
):
    season = get_season(month)
    activities = get_activities(travel_style)

    scored_places = []

    for _, row in df.iterrows():
        score = 0

        if row["weather"] == weather:
            score += 2
        if row["travel_style"] == travel_style:
            score += 2
        if row["budget"] == budget:
            score += 1
        if row["trip_duration"] == trip_duration:
            score += 1
        if row["crowd_level"] == crowd_level:
            score += 1
        if row["best_season"] == season:
            score += 2

        score += row["rating"]  # rating bonus

        scored_places.append({
            "place": row["place"],
            "score": score
        })

    # Sort by score
    ranked = sorted(scored_places, key=lambda x: x["score"], reverse=True)

    top_places = [p["place"] for p in ranked[:5]]
    
    # Get activities from recommended places
    recommended_activities = set()
    for place_name in top_places:
        place_row = df[df["place"] == place_name]
        if not place_row.empty:
            place_activities = place_row.iloc[0]["activities"]
            if pd.notna(place_activities):
                # Split activities if multiple are comma-separated
                activities_list = [a.strip() for a in str(place_activities).split(",")]
                recommended_activities.update(activities_list)
    
    # Convert set to comma-separated string
    activities_str = ", ".join(sorted(recommended_activities)) if recommended_activities else get_activities(travel_style)

    return {
        "season": season,
        "activities": activities_str,
        "places": top_places
    }
