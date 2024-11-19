import requests
from dotenv import load_dotenv
import os
import xml.etree.ElementTree as ET
import csv
from datetime import datetime, timedelta
import time

# 24-05-2022 8:00

load_dotenv()
api_key = os.getenv('transparent_api')
area = '10YES-REE------0' # Spain
document = 'A65' # A65 : System load total, A72 : reservoir filling info, A73 : actual generation, A74 : wind and solar generation, A75 : actual generation per type
process = 'A16' # A16 : realised, A01 : day ahead

# dates = ['202011010000',]
        #  '202211010000','202311010000','202411010000']

start_date = '202410270045' # yyyymmdd:hhmm
end_date = '202411010000'

# Construct the API URL
url = f"https://web-api.tp.entsoe.eu/api?documentType={document}&processType={process}&outBiddingZone_Domain={area}&periodStart={start_date}&periodEnd={end_date}&securityToken={api_key}"

# Make the API request
response = requests.get(url)

# Check if the request was successful
# if response.status_code == 200:
#     print(response.text)

root = ET.fromstring(response.text)

# Define the namespace
namespace = {'ns': 'urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0'}

# Extract the start time and resolution
period = root.find('.//ns:Period', namespace)

# Calculate time intervals (assuming PT15M means 15 minutes)
interval_delta = timedelta(minutes=15)

# Parse start time
start_datetime = datetime.strptime(start_date, '%Y%m%d%H%M')

# Extract data points
points = period.findall('.//ns:Point', namespace)
print(len(points))

# Prepare CSV data
csv_data = [['datetime', 'Actual Total Load (MW)']]
for point in points:
    position = int(point.find('.//ns:position', namespace).text)
    quantity = float(point.find('.//ns:quantity', namespace).text)
    
    # Calculate current time for each position
    current_time = start_datetime + (position - 1) * interval_delta
    csv_data.append([current_time.strftime('%Y-%m-%dT%H:%M:%S'), quantity])

file_name = 'actualTotalLoad.csv'

# Write to CSV file
with open(file_name, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_data)

print(f"csv written from {start_date} to {end_date}")

    
