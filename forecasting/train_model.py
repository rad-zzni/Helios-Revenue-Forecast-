import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Loads cleaned synthetic dataset
df = pd.read_csv("history.csv")

# Features engineering (rolling averages)
df["roll3"] = df["irradiance"].rolling(3).mean().fillna(df["irradiance"])
df["roll24"] = df["irradiance"].rolling(24).mean().fillna(df["irradiance"])

# Features used for training
X = df[[
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

# Targets variable
y = df["kwh"]

# Splits dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

# Trains Random Forest model
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=None,
    random_state=42
)
model.fit(X_train, y_train)

# Saves trained model
joblib.dump(model, "model.joblib")

print("Model trained and saved as model.joblib")