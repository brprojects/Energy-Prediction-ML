import requests
import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('weather_api_key')
location = 'madrid'
base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
file_name = 'weather_data_madrid.csv'

# Function to get the new start and end dates
def get_new_date_range(csv_file):
    if os.path.isfile(csv_file):
        # Read the existing CSV to get the last date
        df = pd.read_csv(csv_file)
        last_date = pd.to_datetime(df['datetime'].iloc[-1])  # Assuming the date column is named 'datetime'
        new_start_date = last_date + timedelta(days=1)
    else:
        # Default to the first date if the file does not exist
        new_start_date = datetime(2019, 11, 1)

    # Calculate the new end date (41 days after the new start date)
    new_end_date = new_start_date + timedelta(days=40)
    return new_start_date.strftime('%Y-%m-%d'), new_end_date.strftime('%Y-%m-%d')

# Get start and end dates
start_date, end_date = get_new_date_range(file_name)

# Construct the API URL
url = f"{base_url}{location}/{start_date}/{end_date}?key={api_key}&unitGroup=metric&include=hours&contentType=csv"

# Make the API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    
    # Check if the file exists to determine whether to write the header
    file_exists = os.path.isfile(file_name)
    
    # Append the response content to the CSV file
    with open(file_name, 'a', newline='') as file:
        # If the file already exists, skip the first line (header)
        if file_exists:
            data_lines = response.text.splitlines()[1:]  # Skip header line
        else:
            data_lines = response.text.splitlines()  # Include header line
        
        # Write the data lines to the file
        file.write("\n".join(data_lines) + "\n")
    
    print(f"Weather data successfully appended to '{file_name}'")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}, Reason: {response.reason}")
