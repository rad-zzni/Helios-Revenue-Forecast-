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

# Enhanced multi-metric summary for SpoonOS
peak_val = pred_kwh.max()
peak_hour = int(np.argmax(pred_kwh))
min_val = pred_kwh.min()
mean_val = float(np.mean(pred_kwh))
unc_mean = float(np.mean(uncertainty))
trend = "increasing" if pred_kwh[12] < pred_kwh[18] else "decreasing"

analysis_text = (
    f"Peak output is {peak_val:.3f} kWh occurring at hour index {peak_hour}. "
    f"Lowest production is {min_val:.3f} kWh. "
    f"Average hourly output is {mean_val:.3f} kWh. "
    f"Uncertainty averages {unc_mean:.3f}. "
    f"Overall production trend appears {trend}. "
    f"Cloud cover, temperature, and irradiance patterns suggest "
    f"moderate variability in the afternoon period. "
)

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