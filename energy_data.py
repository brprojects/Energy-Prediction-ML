import requests
from dotenv import load_dotenv
import os
import xml.etree.ElementTree as ET
import csv
from datetime import datetime, timedelta
import pandas as pd

energy_sources = {
    "B01": "Biomass",
    "B02": "Fossil Brown coal/Lignite",
    "B03": "Fossil Coal-derived gas",
    "B04": "Fossil Gas",
    "B05": "Fossil Hard coal",
    "B06": "Fossil Oil",
    "B07": "Fossil Oil shale",
    "B08": "Fossil Peat",
    "B09": "Geothermal",
    "B10": "Hydro Pumped Storage",
    "B11": "Hydro Run-of-river and poundage",
    "B12": "Hydro Water Reservoir",
    "B13": "Marine",
    "B14": "Nuclear",
    "B15": "Other renewable",
    "B16": "Solar",
    "B17": "Waste",
    "B18": "Wind Offshore",
    "B19": "Wind Onshore",
    "B20": "Other",
    "B25": "Energy storage"
}

df_dict = {source: pd.DataFrame(columns=["datetime", source]) for source in energy_sources.values()}

load_dotenv()
api_key = os.getenv('transparent_api')
area = '10YES-REE------0' # Spain
document = 'A75' # A65 : System load total, A72 : reservoir filling info, A73 : actual generation per unit, A74 : wind and solar generation, A75 : actual generation per type
process = 'A16' # A16 : realised, A01 : day ahead

dates = ['202011010000', '202111010000', '202211010000', '202311010000', '202411010000']
start_date = '201911010000' # yyyymmdd:hhmm


for end_date in dates:
    print(start_date)

    # Construct the API URL
    url = f"https://web-api.tp.entsoe.eu/api?documentType={document}&processType={process}&in_Domain={area}&periodStart={start_date}&periodEnd={end_date}&securityToken={api_key}&psrType=B10"

    # Make the API request
    response = requests.get(url)
    print(response.text)

    # Check if the request was successful
    if response.status_code == 200:
        # print(response.text)
        root = ET.fromstring(response.text)
        # Define the namespace
        ns = {'ns': 'urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0'}

        # Extract TimeSeries sections
        time_series_list = root.findall('ns:TimeSeries', ns)


        for ts in time_series_list:

            psrType = ts.find('ns:MktPSRType/ns:psrType', ns).text
            source_name = energy_sources[psrType]
            print(source_name)
            
            period = ts.find('ns:Period', ns)

            # Extract resolution
            resolution = period.find('ns:resolution', ns).text
            resolution = int(resolution.replace("PT", "").replace("M", ""))
            interval_delta = timedelta(minutes=resolution)
            # print(resolution)

            start = period.find('ns:timeInterval/ns:start', ns).text
            start_datetime = datetime.strptime(start, '%Y-%m-%dT%H:%MZ')
            # print(start_datetime)

            # Extract points
            data = []
            points = period.findall('ns:Point', ns)
            for point in points:
                position = int(point.find('.//ns:position', ns).text)
                quantity = float(point.find('.//ns:quantity', ns).text)
                
                # Calculate current time for each position
                current_time = start_datetime + (position - 1) * interval_delta
                data.append({"datetime": current_time.strftime('%Y-%m-%dT%H:%M:%S'), source_name: quantity})
                
            df_dict[source_name] = pd.concat(
                [df_dict[source_name], pd.DataFrame(data)],
                ignore_index=True
            )
    
    start_date = end_date

# Merge all DataFrames into a single DataFrame
df_final = df_dict["Biomass"]
for source, df_source in df_dict.items():
    if source != "Biomass":
        df_final = pd.merge(df_final, df_source, on="datetime", how="outer")
# print(csv_data)

# Prepare CSV data
file_name = 'energyGeneration.csv'

# Write to CSV file
with open(file_name, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    if csvfile.tell() == 0:
        writer.writerow(df_final.columns)

    # Write DataFrame rows
    writer.writerows(df_final.values.tolist())

print(f"csv written")