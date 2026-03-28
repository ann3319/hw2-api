import requests
import json
import csv
import xml.etree.ElementTree as ET

url = "https://api.nlsc.gov.tw/other/MapLayerInfo"
response = requests.get(url)

content_type = response.headers.get("Content-Type", "")
print("Content-Type:", content_type)

data = None

# 嘗試解析 JSON
if "application/json" in content_type:
    try:
        data = response.json()
        print("Parsed as JSON")
    except Exception as e:
        print("JSON parse failed:", e)

# 如果不是 JSON → 嘗試 XML
if data is None:
    try:
        root = ET.fromstring(response.text)
        print("Parsed as XML")

        data = []
        for item in root.findall(".//MapLayer"):
            record = {}
            for child in item:
                record[child.tag] = child.text
            data.append(record)

    except Exception as e:
        print("XML parse failed:", e)

# 儲存 JSON
with open("maplayer.json", "w", encoding="utf-8") as f:
    if data is not None:
        json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        f.write(response.text)

# 儲存 CSV
if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
    with open("maplayer.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print("CSV created successfully")
else:
    print("No structured data → creating empty CSV")
    with open("maplayer.csv", "w", encoding="utf-8") as f:
        f.write("no data\n")
