import requests
import pandas as pd
import os

# 1. Get API Key from GitHub Secrets
api_key = os.environ.get("OZONETEL_API_KEY")
url = "https://in1-ccaas-api.ozonetel.com/ca_reports/summaryReport"

payload = {
    "fromDate": "2026-02-01 01:00:00",
    "toDate": "2026-02-01 18:00:00",
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
    # Assuming the data is in a list under a specific key, adjust 'data' if needed
    df = pd.DataFrame(data) 
    df.to_csv("report.csv", index=False)
    print("CSV file created successfully.")
else:
    print(f"Failed to fetch data: {response.status_code}")
    exit(1)
