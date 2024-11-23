import pandas as pd
from datetime import timedelta

file_path = "energyGeneration.csv"
output_file = "energyGeneration2.csv"

# Load the CSV file
data = pd.read_csv(file_path)

# Ensure datetime column is properly parsed
data['datetime'] = pd.to_datetime(data['datetime'], format='%Y-%m-%dT%H:%M:%S', errors='coerce')

# Drop rows with invalid or non-hourly datetime values
data = data[data['datetime'].dt.minute == 0].reset_index(drop=True)

# Add 1 hour to convert from UTC to CEST
data['datetime'] = data['datetime'] + pd.Timedelta(hours=1)

prev_datetime = data['datetime'].iloc[0]
error_count = 0
for i in range(1, len(data)):
    current_datetime = data['datetime'].iloc[i]

    if prev_datetime + timedelta(hours=1) != current_datetime:
        print(f'Missing data around: {prev_datetime}')
        error_count += 1

    prev_datetime = current_datetime

if error_count == 0:
    data['datetime'] = data['datetime'].dt.strftime('%Y-%m-%dT%H:%M:%S')
    data.to_csv(output_file, index=False)


