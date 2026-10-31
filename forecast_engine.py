import json
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import joblib
import numpy as np
import pandas as pd
import requests

BASE = Path(__file__).parent
MODEL_DIR = BASE / "models"
DATA_DIR = BASE / "data"
FORECAST_FILE = DATA_DIR / "forecast.json"
TZ = ZoneInfo("Asia/Karachi")

def api(url, params):
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def pm25_to_aqi(pm):
    c = np.floor(float(pm) * 10) / 10
    breaks = [
        (0, 9.0, 0, 50),
        (9.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 125.4, 151, 200),
        (125.5, 225.4, 201, 300),
        (225.5, 325.4, 301, 500)
    ]
    for lo, hi, alo, ahi in breaks:
        if lo <= c <= hi:
            return round((ahi-alo)/(hi-lo)*(c-lo)+alo)
    return 500 if c > 325.4 else 0

def aqi_details(aqi):
    if aqi <= 50:
        return "Good", "Low", "green", "Enjoy outdoor activities as normal. No special precautions are needed."
    if aqi <= 100:
        return "Moderate", "Moderate", "yellow", "Sensitive individuals should reduce prolonged or intense outdoor activity if symptoms occur."
    if aqi <= 150:
        return "Unhealthy for Sensitive Groups", "High", "orange", "Sensitive groups should limit outdoor activity, keep medication available if needed, and monitor symptoms."
    if aqi <= 200:
        return "Unhealthy", "High", "red", "Reduce prolonged outdoor activities, avoid strenuous exercise outdoors, and consider wearing a well-fitting N95 mask if spending extended time outside."
    if aqi <= 300:
        return "Very Unhealthy", "Very High", "purple", "Stay indoors where possible, keep windows and doors closed, use an air purifier if available, and avoid unnecessary outdoor activities."
    return "Hazardous", "Extreme", "black", "Avoid outdoor activities unless absolutely necessary. Wear a high-quality mask if you must go outside and follow official public health advisories."


def get_inputs():
    lat, lon = 31.5204, 74.3587

    weather = api(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_mean,relative_humidity_2m_mean,wind_speed_10m_mean,wind_direction_10m_dominant",
            "forecast_days": 4,
            "timezone": "Asia/Karachi"
        }
    )["daily"]

    air = api(
        "https://air-quality-api.open-meteo.com/v1/air-quality",
        {
            "latitude": lat,
            "longitude": lon,
            "current": "pm2_5",
            "timezone": "Asia/Karachi"
        }
    )

    pm = air.get("current", {}).get("pm2_5")

    if pm is None:
        raise ValueError("No current PM2.5 data returned.")

    days = []

    for i in range(1, 4):
        values = {
            "PM2.5": float(pm),
            "Temperature": weather["temperature_2m_mean"][i],
            "Relative Humidity": weather["relative_humidity_2m_mean"][i],
            "Wind Speed": weather["wind_speed_10m_mean"][i],
            "Wind Direction": weather["wind_direction_10m_dominant"][i]
        }

        if any(v is None for v in values.values()):
            raise ValueError("Incomplete weather data.")

        days.append((weather["time"][i], values))

    return days


def predict(model, values):

    if hasattr(model, "feature_names_in_"):
        aliases = {
            "pm2.5": values["PM2.5"],
            "pm25": values["PM2.5"],
            "temperature": values["Temperature"],
            "relative humidity": values["Relative Humidity"],
            "relativehumidity": values["Relative Humidity"],
            "humidity": values["Relative Humidity"],
            "wind speed": values["Wind Speed"],
            "wind_speed": values["Wind Speed"],
            "wind direction": values["Wind Direction"],
            "wind_direction": values["Wind Direction"]
        }

        row = {}

        for name in model.feature_names_in_:
            key = str(name).strip().lower()

            if key not in aliases:
                raise ValueError(
                    f"Unknown model feature: {name}"
                )

            row[name] = aliases[key]

        X = pd.DataFrame([row])

    else:
        if getattr(model, "n_features_in_", 5) != 5:
            raise ValueError("Unexpected model feature count.")

        X = pd.DataFrame(
            [values],
            columns=[
                "PM2.5",
                "Temperature",
                "Relative Humidity",
                "Wind Speed",
                "Wind Direction"
            ]
        )

    result = float(np.asarray(model.predict(X)).ravel()[0])

    if not np.isfinite(result):
        raise ValueError("Invalid model prediction.")

    return max(0, result)


def generate_forecast(force=False):

    DATA_DIR.mkdir(exist_ok=True)

    if FORECAST_FILE.exists() and not force:
        old = json.loads(
            FORECAST_FILE.read_text(encoding="utf-8")
        )

        updated = datetime.fromisoformat(
            old["last_updated"]
        )

        if datetime.now(TZ) - updated < timedelta(hours=72):
            return old

    inputs = get_inputs()

    names = [
        "pm25_day1_model.pkl",
        "pm25_day2_model.pkl",
        "pm25_day3_model.pkl"
    ]

    results = []
    previous_pm = inputs[0][1]["PM2.5"]

    for i, name in enumerate(names):

        path = MODEL_DIR / name

        if not path.exists():
            raise FileNotFoundError(
                f"Missing model: {path}"
            )

        model = joblib.load(path)

        date, values = inputs[i]
        values["PM2.5"] = previous_pm

        pm = predict(model, values)
        aqi = pm25_to_aqi(pm)

        category, risk, colour, advice = aqi_details(aqi)

        results.append({
            "date": date,
            "pm25": round(pm, 2),
            "aqi": aqi,
            "category": category,
            "risk": risk,
            "colour": colour,
            "advice": advice
        })

        previous_pm = pm

    current = datetime.now(TZ)

    result = {
        "city": "Lahore",
        "last_updated": current.isoformat(),
        "next_update": (
            current + timedelta(hours=72)
        ).isoformat(),
        "forecasts": results
    }

    temp = FORECAST_FILE.with_suffix(".tmp")

    temp.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8"
    )

    temp.replace(FORECAST_FILE)

    return result


if __name__ == "__main__":
    import sys

    result = generate_forecast(
        force="--force" in sys.argv
    )

    print(json.dumps(result, indent=2))

