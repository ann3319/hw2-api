import requests
import json
import csv

# API URL
url = "https://api.nlsc.gov.tw/other/MapLayerInfo"

# 發送 GET 請求
response = requests.get(url)
data = response.json()

# 儲存成 JSON
with open("maplayer.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# 儲存成 CSV
with open("maplayer.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
