import os
import csv
import requests
from datetime import datetime, timedelta
from pathlib import Path

OZ_DOMAIN = os.environ["OZONETEL_DOMAIN"]
OZ_API_KEY = os.environ["OZONETEL_API_KEY"]
OZ_USERNAME = os.environ["OZONETEL_USERNAME"]

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

def fetch_ozonetel_data():
    url = f"https://{OZ_DOMAIN}/ca_reports/summaryReport"

    headers = {
        "Content-Type": "application/json",
        "apiKey": OZ_API_KEY
    }

    to_date = datetime.utcnow()
    from_date = to_date - timedelta(days=1)

    payload = {
        "fromDate": from_date.strftime("%Y-%m-%d %H:%M:%S"),
        "toDate": to_date.strftime("%Y-%m-%d %H:%M:%S"),
        "userName": OZ_USERNAME
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()

    data = response.json()
    if data.get("status") != "success":
        raise Exception(data)

    return data.get("data", [])

def write_csv(rows):
    if not rows:
        print("No data returned from API")
        return None

    date_tag = datetime.utcnow().strftime("%Y-%m-%d")
    file_path = OUTPUT_DIR / f"ozonetel_summary_{date_tag}.csv"

    headers = rows[0].keys()

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV written: {file_path}")
    return file_path

def main():
    print("Fetching Ozonetel data…")
    data = fetch_ozonetel_data()

    print("Writing CSV…")
    write_csv(data)

if __name__ == "__main__":
    main()
