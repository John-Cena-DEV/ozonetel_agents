import requests
import csv
from datetime import datetime
import os
import sys
import json

def fetch_agent_summary():
    """
    Fetch Agent Summary report from Ozonetel
    Uses intraday working-hours window (01:00–23:00)
    """

    API_URL = "https://in1-ccaas-api.ozonetel.com/ca_reports/summaryReport"

    API_KEY = os.environ.get("OZONETEL_API_KEY")
    USERNAME = os.environ.get("OZONETEL_USERNAME")

    if not API_KEY or not USERNAME:
        print("❌ Missing environment variables")
        sys.exit(1)

    API_KEY = API_KEY.strip()
    USERNAME = USERNAME.strip()

    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")

    from_date = f"{date_str} 01:00:00"
    to_date   = f"{date_str} 23:00:00"

    print("============================================================")
    print("🚀 Agent Summary Fetch")
    print("============================================================")
    print(f"From: {from_date}")
    print(f"To  : {to_date}")
    print(f"User: {USERNAME}")

    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "apiKey": API_KEY
    }

    payload = {
        "fromDate": from_date,
        "toDate": to_date,
        "userName": USERNAME
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print("❌ API error")
            print(response.text[:500])
            return None

        result = response.json()
        print("Response keys:", list(result.keys()))

        if result.get("status") != "success":
            print("❌ API returned failure")
            print(json.dumps(result, indent=2))
            return None

        rows = result.get("data", [])
        print(f"📊 Records returned: {len(rows)}")

        return rows

    except Exception as e:
        print("❌ Request failed:", e)
        return None


def write_csv(rows):
    """
    Always creates CSV (empty or populated)
    Overwrites file daily
    """

    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{output_dir}/agent_summary_{datetime.now().strftime('%Y-%m-%d')}.csv"

    if not rows:
        print("⚠️ No data returned — creating empty CSV")
        open(filename, "w").close()
        return filename

    if not isinstance(rows, list) or not isinstance(rows[0], dict):
        print("⚠️ Unexpected data format — saving debug JSON")
        with open("agent_summary_debug.json", "w") as f:
            json.dump(rows, f, indent=2)
        return None

    headers = rows[0].keys()

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ CSV written: {filename}")
    return filename


def main():
    rows = fetch_agent_summary()
    result = write_csv(rows)

    if result:
        print("============================================================")
        print("✅ Process completed successfully")
        print("============================================================")
        sys.exit(0)
    else:
        print("============================================================")
        print("❌ Process failed")
        print("============================================================")
        sys.exit(1)


if __name__ == "__main__":
    main()
