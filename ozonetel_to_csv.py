import requests
import csv
from datetime import datetime
import json
import sys
import os

def fetch_agent_summary():
    """Fetch Agent Summary data from Ozonetel API"""

    API_URL = "https://in1-ccaas-api.ozonetel.com/ca_reports/summaryReport"
    API_KEY = os.environ.get("OZONETEL_API_KEY")
    USERNAME = os.environ.get("OZONETEL_USERNAME")

    # FULL DAY (same pattern as your CDR script)
    today = datetime.now()
    from_date = today.strftime("%Y-%m-%d 00:00:00")
    to_date = today.strftime("%Y-%m-%d 23:59:59")

    print("👤 Fetching Agent Summary")
    print(f"From: {from_date}")
    print(f"To  : {to_date}")
    print(f"User: {USERNAME}")

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "apiKey": API_KEY.strip()
    }

    payload = {
        "fromDate": from_date,
        "toDate": to_date,
        "userName": USERNAME.strip()
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

        print("Status:", response.status_code)

        if response.status_code != 200:
            print("❌ API Error")
            print(response.text[:500])
            return None

        data = response.json()
        print("Response keys:", list(data.keys()))

        if data.get("status") != "success":
            print("❌ API returned failure")
            print(json.dumps(data, indent=2))
            return None

        rows = data.get("data", [])
        print(f"📊 Records returned: {len(rows)}")

        return rows

    except Exception as e:
        print("❌ Request failed:", e)
        return None


def save_to_csv(data, filename="agent_summary_master.csv"):
    """Overwrite single CSV (same behavior as your CDR script)"""

    if not data:
        print("⚠️ No data to save — creating empty CSV")
        open(filename, "w").close()
        return filename

    if not isinstance(data, list) or not isinstance(data[0], dict):
        print("⚠️ Unexpected data format")
        json.dump(data, open("agent_summary_debug.json", "w"), indent=2)
        return None

    headers = data[0].keys()

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ Saved {len(data)} rows to {filename}")
    return filename


def main():
    print("=" * 60)
    print("🚀 Agent Summary Fetch")
    print("=" * 60)

    data = fetch_agent_summary()

    result = save_to_csv(data)

    if result:
        print("✅ Done")
        sys.exit(0)
    else:
        print("❌ Failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
