from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace with your OpenWeatherMap API key
API_KEY = "your_openweathermap_api_key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City name is required"}), 400

    # Build the OpenWeatherMap API URL
    url = f"http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Parse and return the JSON response
        data = response.json()
        if "name" in data:
            return jsonify(data)
        else:
            return jsonify({"error": "Unexpected response from weather API"}), 500
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return jsonify({"error": "City not found"}), 404
        else:
            return jsonify({"error": f"HTTP error occurred: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as req_err:
        return jsonify({"error": f"Network error occurred: {req_err}"}), 503
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

import os
API_KEY = os.getenv("OPENWEATHER_API_KEY")
