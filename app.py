import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("NUMVERIFY_API_KEY")  # Make sure the .env file contains this key

app = Flask(__name__)

# Function to get details from the API
def get_mobile_details(phone_number):
    url = f"http://apilayer.net/api/validate?access_key={API_KEY}&number={phone_number}"
    response = requests.get(url)
    data = response.json()
    return data  # Returns the response as a JSON object

# Route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    details = None
    error_message = None
    if request.method == "POST":
        phone_number = request.form["phone_number"]
        try:
            details = get_mobile_details(phone_number)
            if not details.get("valid"):  # Check if the phone number is valid
                error_message = "Invalid phone number. Please try again."
        except Exception as e:
            error_message = "Error fetching data. Please check your API key or internet connection."
    return render_template("index.html", details=details, error_message=error_message)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
