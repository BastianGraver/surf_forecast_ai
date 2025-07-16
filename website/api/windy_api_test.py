import requests
import json
from datetime import datetime, date
from zoneinfo import ZoneInfo

# === Config ===
API_KEY = "kTBW7o2TRW8W9Zk9vWeV8oiv9vGDSsUJ"
LAT = 56.0046
LON = 8.1294
URL = "https://api.windy.com/api/point-forecast/v2"
TARGET_HOURS = {5, 8, 11, 14, 17, 20}
LOCAL_TZ = ZoneInfo("Europe/Copenhagen")


# === Request Payload ===
payload = {
    "lat": LAT,
    "lon": LON,
    "model": "gfsWave",
    "parameters": ["waves", "windWaves", "swell1", "swell2"],
    "levels": ["surface"],
    "key": API_KEY
}

headers = {"Content-Type": "application/json"}

# === Mapping for correct API keys ===
param_keys = {
    "waves": "waves",
    "windWaves": "wwaves",
    "swell1": "swell1",
    "swell2": "swell2"
}

try:
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    data = response.json()

    ts_list = data["ts"]
    today = date.today()

    print("Format:")
    print("[datetime], [waves_height], [waves_period], [waves_direction], "
          "[wwaves_height], [wwaves_period], [wwaves_direction], "
          "[swell1_height], [swell1_period], [swell1_direction], "
          "[swell2_height], [swell2_period], [swell2_direction]\n")

    for i, ts in enumerate(ts_list):
        utc_time = datetime.utcfromtimestamp(ts / 1000).replace(tzinfo=ZoneInfo("UTC"))
        local_time = utc_time.astimezone(LOCAL_TZ)

        if local_time.date() == today and local_time.hour in TARGET_HOURS:
            values = [local_time.strftime('%Y-%m-%d %H:%M')]

            for group in ["waves", "windWaves", "swell1", "swell2"]:
                prefix = param_keys[group]
                for suffix in ["height", "period", "direction"]:
                    key = f"{prefix}_{suffix}-surface"
                    series = data.get(key, [])
                    value = series[i] if i < len(series) and series[i] is not None else ""
                    values.append(f"{value:.2f}" if isinstance(value, (int, float)) else "")

            print(", ".join(values))

except requests.exceptions.HTTPError as e:
    print("HTTP Error:", e)
    print(response.text)
except Exception as e:
    print("Error:", e)