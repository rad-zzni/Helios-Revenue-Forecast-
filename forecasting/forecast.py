import requests
import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime, timedelta

# Load trained model
model = joblib.load("model.joblib")

# Fetch weather forecast (Open-Meteo free API)
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 37.97,
    "longitude": -104.18,
    "hourly": "shortwave_radiation,temperature_2m,cloudcover,relativehumidity_2m,windspeed_10m,pressure_msl",
    "forecast_days": 2,
    "timezone": "UTC"
}
resp = requests.get(url, params=params)
data = resp.json()["hourly"]

# Extract next 24 hours
hours = data["time"][:24]
irr = data["shortwave_radiation"][:24]
temp = data["temperature_2m"][:24]
cloud = data["cloudcover"][:24]
humidity = data["relativehumidity_2m"][:24]
wind = data["windspeed_10m"][:24]
press = data["pressure_msl"][:24]

# Build DataFrame for forecasting
df = pd.DataFrame({
    "timestamp": hours,
    "irradiance": irr,
    "cloud_cover": cloud,
    "temperature": temp,
    "humidity": humidity,
    "wind_speed": wind,
    "pressure": press
})

df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour
df["roll3"] = df["irradiance"].rolling(3).mean().fillna(df["irradiance"])
df["roll24"] = df["irradiance"].rolling(24).mean().fillna(df["irradiance"])

# Features for model
X_future = df[[
    "irradiance",
    "cloud_cover",
    "temperature",
    "humidity",
    "wind_speed",
    "pressure",
    "hour",
    "roll3",
    "roll24"
]]

# Predict kWh
pred_kwh = model.predict(X_future)

# Revenue (configurable)
rate = 0.12
revenue = pred_kwh * rate

# Uncertainty estimate
uncertainty = np.std(pred_kwh) * np.ones_like(pred_kwh)

# Summary for SpoonOS
analysis_text = f"Peak output: {pred_kwh.max():.3f} kWh. Low point: {pred_kwh.min():.3f} kWh."

# Build final output JSON
forecast = {
    "generated_at": datetime.utcnow().isoformat(),
    "hours": hours,
    "kwh": pred_kwh.round(4).tolist(),
    "revenue": revenue.round(4).tolist(),
    "uncertainty": uncertainty.round(4).tolist(),
    "analysis_input": analysis_text
}

with open("forecast.json", "w") as f:
    json.dump(forecast, f, indent=2)

print("forecast.json generated successfully")