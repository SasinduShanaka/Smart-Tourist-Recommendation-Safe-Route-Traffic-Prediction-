from flask import Flask, render_template, request, redirect, url_for, session
from recommendation_engine import recommend_places_scored
from location_utils import PLACE_COORDINATES

app = Flask(__name__, 
            template_folder="../frontend/templates",
            static_folder="../frontend/static")
app.secret_key = 'your-secret-key-here-change-in-production'

@app.route("/", methods=["GET"])
def index():
    result = session.pop('result', None)
    places_map = session.pop('places_map', [])
    form_data = session.pop('form_data', {})
    return render_template("index.html", result=result, places_map=places_map, form_data=form_data)

@app.route("/recommend", methods=["POST"])
def recommend():
    weather = request.form["weather"]
    travel_style = request.form["travel_style"]
    month = request.form["month"]
    budget = request.form["budget"]
    trip_duration = request.form["trip_duration"]
    crowd_level = request.form["crowd_level"]

    result = recommend_places_scored(
        weather, travel_style, month,
        budget, trip_duration, crowd_level
    )
    
    # Prepare places data for map
    places_map = []
    if result and "places" in result:
        for place in result["places"]:
            if place in PLACE_COORDINATES:
                lat, lng = PLACE_COORDINATES[place]
                places_map.append({
                    "name": place,
                    "lat": lat,
                    "lng": lng
                })
    
    # Store form data to preserve selections
    form_data = {
        'weather': weather,
        'travel_style': travel_style,
        'month': month,
        'budget': budget,
        'trip_duration': trip_duration,
        'crowd_level': crowd_level
    }
    
    # Store in session and redirect to GET
    session['result'] = result
    session['places_map'] = places_map
    session['form_data'] = form_data
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
