from dotenv import load_dotenv
import urllib.request, json 
import ssl, os
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()

api_key = os.getenv('API_KEY')

# Dataset ID for wind power forecast
forecast_dataset_id = 245

# Dataset ID for actual wind power
actual_dataset_id = 181

# Define the time range for the data (UTC format)
start_time = '2025-02-20T00:00:00Z'
end_time = '2025-02-20T00:15:00Z'
# Needed when fetching data for a specific time range 

try:
    # Construct the API URL
    # Construct the API URL with time range filtering
    url_1 = f"https://data.fingrid.fi/api/datasets/{forecast_dataset_id}/data?startTime={start_time}&endTime={end_time}"
    url_2 = f"https://data.fingrid.fi/api/datasets/{actual_dataset_id}/data?startTime={start_time}&endTime={end_time}"

    hdr ={
    # Request headers
    'Cache-Control': 'no-cache',
    'x-api-key': api_key,
    }

    req_1 = urllib.request.Request(url_1, headers=hdr)

    req_1.get_method = lambda: 'GET'
      # Create an unverified SSL context
    context = ssl._create_unverified_context()

    response_1 = urllib.request.urlopen(req_1, context=context)
    #print(response_1.getcode())
    #print(response_1.read().decode('utf-8'))  # Decode the response to handle non-ASCII characters

    req_2 = urllib.request.Request(url_2, headers=hdr)

    req_2.get_method = lambda: 'GET'
      # Create an unverified SSL context
    context = ssl._create_unverified_context()

    response_2 = urllib.request.urlopen(req_2, context=context)
    #print(response_2.getcode())
    #print(response_2.read().decode('utf-8'))  # Decode the response to handle non-ASCII characters

except Exception as e:
    print(e)

# Parse the JSON response
data_1 = json.loads(response_1.read().decode('utf-8'))

# Extract time and value from the 'data' section
for entry in data_1['data']:
    start_time = entry['startTime']
    value = entry['value']
    print(f"Time: {start_time}, Value: {value}")

# Parse the JSON response
data_2 = json.loads(response_2.read().decode('utf-8'))


# Extract time and value from the 'data' section
for entry in data_2['data']:
    start_time = entry['startTime']
    value = entry['value']
    print(f"Time: {start_time}, Value: {value}")