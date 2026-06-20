from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

# Base URL for the TVmaze API
TVMAZE_BASE_URL = "https://api.tvmaze.com"

@app.route('/')
def index():
    # Capture country code filter (defaults to 'US') and date (defaults to today)
    country = request.args.get('country', 'US')
    date_str = request.args.get('date', datetime.today().strftime('%d. %m. %Y.'))

    # Endpoint for the schedule: /schedule?country=US&date=2026-06-20
    schedule_url = f"{TVMAZE_BASE_URL}/schedule"
    params = {
        'country': country,
        'date': date_str
    }
    
    episodes_list = []
    error_message = None

    try:
        response = requests.get(schedule_url, params=params, timeout=10)
        # Check if rate limit (20 requests per 10 seconds) or another issue occurs
        if response.status_code == 200:
            episodes_list = response.json()
        elif response.status_code == 429:
            error_message = "Rate limit exceeded. Please wait a moment and try again."
        else:
            error_message = f"Failed to retrieve data from TVmaze (Status: {response.status_code})"
    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred while connecting to the API: {str(e)}"

    return render_template(
        'index.html', 
        episodes=episodes_list, 
        current_date=date_str, 
        current_country=country,
        error=error_message
    )

if __name__ == '__main__':
    # Run development server
    app.run(debug=True)
