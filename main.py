from flask import Flask, request, jsonify
from app import getliveTemp # Import your existing weather function from app.py
import os

app = Flask(__name__) # Create a new Flask web application instance

# Define a route that your Cloud Run service will expose
# When someone visits your Cloud Run URL/weather?latitude=X&longitude=Y, this function runs
@app.route("/weather", methods=["GET"])
def get_weather_data():
    # Get latitude and longitude from the URL query parameters
    latitude = request.args.get("latitude", type=float)
    longitude = request.args.get("longitude", type=float)

    # Basic validation
    if latitude is None or longitude is None:
        return jsonify({"error": "Latitude and longitude parameters are required."}), 400

    try:
        # Call your existing weather data retrieval function from app.py
        weather_data = getliveTemp(latitude, longitude)

        if weather_data:
            return jsonify(weather_data), 200 # Return the data as JSON with success status
        else:
            return jsonify({"error": "Could not retrieve weather data."}), 500 # Handle cases where getliveTemp returns None
    except Exception as e:
        # Catch any unexpected errors and return an error message
        print(f"Error processing request: {e}") # Print to logs for debugging
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

# This block runs when the script is executed directly
if __name__ == "__main__":
    # Cloud Run provides the port via the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    # Run the Flask app
    app.run(host="0.0.0.0", port=port)