import requests
import json
import csv

url = "https://api.nlsc.gov.tw/other/MapLayerInfo"
response = requests.get(url)

try:
    data = response.json()   # 嘗試解析 JSON
except Exception:
    print("API did not return JSON, saving raw text instead.")
    with open("maplayer.json", "w", encoding="utf-8") as f:
        f.write(response.text)
    exit(0)

# 儲存成 JSON
with open("maplayer.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# 如果 data 是 list 才存 CSV
if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
    with open("maplayer.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
else:
    print("Data is not a list of dicts, skipping CSV.")
