from flask import Flask, render_template, request, redirect, url_for, session

from recommendation_engine import recommend_places_scored
from location_utils import PLACE_COORDINATES
from nlp_parser import parse_user_text

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

app.secret_key = "change-this-secret-key"

# ======================
# HOME PAGE
# ======================
@app.route("/", methods=["GET"])
def index():
    result = session.pop("result", None)
    places_map = session.pop("places_map", [])
    form_data = session.pop("form_data", {})
    user_text = session.pop("user_text", "")

    return render_template(
        "index.html",
        result=result,
        places_map=places_map,
        form_data=form_data,
        user_text=user_text
    )

# ======================
# STRUCTURED FORM INPUT
# ======================
@app.route("/recommend", methods=["POST"])
def recommend():
    weather = request.form["weather"]
    travel_style = request.form["travel_style"]
    month = request.form["month"]
    budget = request.form["budget"]
    trip_duration = request.form["trip_duration"]
    crowd_level = request.form["crowd_level"]

    result = recommend_places_scored(
        weather,
        travel_style,
        month,
        budget,
        trip_duration,
        crowd_level
    )

    places_map = build_places_map(result)

    session["result"] = result
    session["places_map"] = places_map
    session["form_data"] = request.form

    return redirect(url_for("index"))

# ======================
# NLP FREE-TEXT INPUT
# ======================
@app.route("/nlp", methods=["POST"])
def nlp_recommendation():
    user_text = request.form["user_text"]

    prefs = parse_user_text(user_text)

    result = recommend_places_scored(
        weather=prefs["weather"],
        travel_style=prefs["travel_style"],
        month=prefs["month"],
        budget=prefs["budget"],
        trip_duration=prefs["trip_duration"],
        crowd_level=prefs["crowd_level"]
    )

    places_map = build_places_map(result)

    session["result"] = result
    session["places_map"] = places_map
    session["user_text"] = user_text

    return redirect(url_for("index"))

# ======================
# HELPER FUNCTION
# ======================
def build_places_map(result):
    places_map = []
    missing_coordinates = []

    if result and "places" in result:
        for place in result["places"]:
            if place in PLACE_COORDINATES:
                lat, lng = PLACE_COORDINATES[place]
                places_map.append({
                    "name": place,
                    "lat": lat,
                    "lng": lng
                })
            else:
                missing_coordinates.append(place)
                print(f"WARNING: No coordinates found for place: {place}")

    if missing_coordinates:
        print(f"Total places missing coordinates: {len(missing_coordinates)}")
        print(f"Missing places: {', '.join(missing_coordinates)}")

    return places_map

# ======================
# RUN APP
# ======================
if __name__ == "__main__":
    app.run(debug=True)
