import pandas as pd
import glob

# 1. find all csv files downloaded
files = glob.glob("dataset/*.csv")

dfs = []

for f in files:
    print("Loading:", f)
    df = pd.read_csv(f)

    # ---- 2. Keep only columns we care about ----
    df = df[[
        "Year", "Month", "Day", "Hour", "Minute",
        "GHI", "DHI", "DNI", "CloudType",
        "Temperature", "RelativeHumidity",
        "WindSpeed", "Pressure"
    ]]

    # ---- 3. Build timestamp ----
    df["timestamp"] = pd.to_datetime(df[["Year","Month","Day","Hour","Minute"]])

    # ---- 4. Compute synthetic solar output (kWh) ----
    df["kwh"] = df["GHI"] * 0.2 / 1000.0

    dfs.append(df)

# 5. Combine all years
combined = pd.concat(dfs, ignore_index=True)

# 6. Sort by timestamp to avoid time jumps
combined = combined.sort_values("timestamp")

# 7. Save final history file
combined.to_csv("history.csv", index=False)

print("Created history.csv with", len(combined), "rows")