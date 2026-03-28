import requests
import json
import csv
import xml.etree.ElementTree as ET

url = "https://api.nlsc.gov.tw/other/MapLayerInfo"

# 發送請求
try:
    response = requests.get(url, timeout=10)
    print("Status Code:", response.status_code)
except Exception as e:
    print("Request failed:", e)

    # 保證檔案存在
    with open("maplayer.json", "w", encoding="utf-8") as f:
        f.write("request failed")

    with open("maplayer.csv", "w", encoding="utf-8") as f:
        f.write("request failed\n")

    exit(0)

content_type = response.headers.get("Content-Type", "")
print("Content-Type:", content_type)

data = None

# 嘗試解析 JSON
try:
    data = response.json()
    print("Parsed as JSON")
except Exception:
    print("Not JSON")


# 不是JSON → 嘗試 XML
if data is None:
    try:
        root = ET.fromstring(response.text)
        print("Parsed as XML")

        data = []
        for item in root.iter():
            record = {}
            for child in item:
                record[child.tag] = child.text
            if record:
                data.append(record)

    except Exception as e:
        print("XML parse failed:", e)

# 儲存 JSON
with open("maplayer.json", "w", encoding="utf-8") as f:
    if data:
        json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        f.write(response.text)

# 儲存 CSV
try:
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):

        # 收集所有欄位
        fieldnames = set()
        for row in data:
            fieldnames.update(row.keys())
        fieldnames = list(fieldnames)

        with open("maplayer.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            for row in data:
                writer.writerow(row)

        print("CSV created successfully")

    else:
        raise Exception("Data not suitable for CSV")

except Exception as e:
    print("CSV error:", e)

    
    with open("maplayer.csv", "w", encoding="utf-8") as f:
        f.write("no data\n")
