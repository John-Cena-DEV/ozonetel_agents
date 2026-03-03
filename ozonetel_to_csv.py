import requests
import pandas as pd
import os
from datetime import datetime, timedelta

# 1. Get API Key from GitHub Secrets
api_key = os.environ.get("OZONETEL_API_KEY")
url = "https://in1-ccaas-api.ozonetel.com/ca_reports/summaryReport"

# 2. Calculate yesterday's date
yesterday = datetime.now()-timedelta(days=1)

from_date = yesterday.strftime('%Y-%m-%d 00:00:00')
to_date = yesterday.strftime('%Y-%m-%d 23:59:59')

# 3. Create payload properly
payload = {
    "fromDate": from_date,
    "toDate": to_date,
    "userName": "qht_regrow"
}

headers = {
    "accept": "application/json",
    "apiKey": api_key,
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()

    # If API returns nested structure like {"data": [...]}
    if isinstance(data, dict) and "data" in data:
        df = pd.DataFrame(data["data"])
    else:
        df = pd.DataFrame(data)

    df.to_csv("report.csv", index=False)
    print("CSV file created successfully.")
else:
    print(f"Failed to fetch data: {response.status_code}")
    print(response.text)
    exit(1)
