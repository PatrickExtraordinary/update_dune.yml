import requests, csv, datetime, io
from datetime import datetime

# === 1. Fetch data from Alternative.me ===
url = "https://api.alternative.me/fng/?limit=730&format=json"
data = requests.get(url).json()['data']

# === 2. Normalize ===
rows = []
for item in data:
    dt = datetime.utcfromtimestamp(int(item['timestamp'])).strftime('%Y-%m-%d')
    rows.append([dt, int(item['value'])])

# === 3. Write CSV in memory ===
csv_buffer = io.StringIO()
writer = csv.writer(csv_buffer)
writer.writerow(["date", "fear_and_greed_index"])
writer.writerows(rows)
csv_bytes = csv_buffer.getvalue().encode("utf-8")

# === 4. Upload to Dune ===
# (Use Dune's Uploads API; requires an API key)
import requests

dune_api_key = "sHXBTuxvtVHDh12WRP1kYZ24y4HRT9CI"
upload_id = "gulfquant.dataset_fear_and_greed_index_daily"   # your Dune Upload ID
endpoint = f"https://api.dune.com/api/v1/uploads/{upload_id}/replace-file"

files = {"file": ("fear_and_greed_index.csv", csv_bytes, "text/csv")}
headers = {"X-Dune-API-Key": dune_api_key}
r = requests.post(endpoint, headers=headers, files=files)

print("Upload status:", r.status_code, r.text)