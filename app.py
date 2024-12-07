from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Use environment variables for security (or replace with your API key)
API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_openweathermap_api_key")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    
    if not city and not (lat and lon):
        return jsonify({"error": "City name or coordinates are required"}), 400

    # Determine endpoint based on input
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"appid": API_KEY, "units": "metric"}
    if city:
        params["q"] = city
    elif lat and lon:
        params["lat"] = lat
        params["lon"] = lon

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching weather data: {e}"}), 503

@app.route("/air_quality", methods=["GET"])
def get_air_quality():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not (lat and lon):
        return jsonify({"error": "Coordinates are required for air quality data"}), 400

    url = f"http://api.openweathermap.org/data/2.5/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": API_KEY}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching air quality data: {e}"}), 503

@app.route("/forecast", methods=["GET"])
def get_forecast():
    city = request.args.get("city")
    
    if not city:
        return jsonify({"error": "City name is required for the forecast"}), 400

    url = f"http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching forecast data: {e}"}), 503

if __name__ == "__main__":
    app.run(debug=True)
import requests
from flask import jsonify, request

API_KEY = "your_openweathermap_api_key"

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City name is required"}), 400
    
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.json().get("message", "Unable to fetch weather data")}), response.status_code
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Ensure `index.html` is in a "templates" folder
