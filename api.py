import requests
import json
import csv

url = "https://api.nlsc.gov.tw/other/MapLayerInfo"
response = requests.get(url)

# 嘗試解析 JSON
try:
    data = response.json()
except Exception:
    print("⚠️ API did not return JSON, saving raw text instead.")
    with open("maplayer.json", "w", encoding="utf-8") as f:
        f.write(response.text)
    # 至少產生一個檔案，避免 workflow 出錯
    exit(0)

# 儲存成 JSON
with open("maplayer.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# 嘗試存成 CSV（僅當 data 是 list of dict）
if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
    with open("maplayer.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
else:
    print("⚠️ Data is not a list of dicts, skipping CSV.")
    # 建立一個空的 CSV 檔，避免 workflow 出錯
    with open("maplayer.csv", "w", newline="", encoding="utf-8") as f:
        f.write("no data")

