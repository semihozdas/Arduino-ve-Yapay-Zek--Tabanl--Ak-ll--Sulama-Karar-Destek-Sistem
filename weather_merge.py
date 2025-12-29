import pandas as pd
import requests

# ---------------- AYARLAR ----------------
LAT = 38.7437
LON = 41.5064

SENSOR_FILE = "gul_sensor_verileri.csv"
OUT_FILE = "gul_sensor_weather.csv"

# ---------------- SENSOR VERİSİ ----------------
df = pd.read_csv(SENSOR_FILE)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.floor("H")

start = df["hour"].min().strftime("%Y-%m-%d")
end = df["hour"].max().strftime("%Y-%m-%d")

# ---------------- OPEN METEO ----------------
url = (
    "https://api.open-meteo.com/v1/forecast?"
    f"latitude={LAT}&longitude={LON}"
    "&hourly=temperature_2m,relative_humidity_2m,precipitation"
    f"&start_date={start}&end_date={end}"
    "&timezone=auto"
)

weather = requests.get(url, timeout=10).json()

weather_df = pd.DataFrame({
    "hour": pd.to_datetime(weather["hourly"]["time"]),
    "temp_out": weather["hourly"]["temperature_2m"],
    "humidity_out": weather["hourly"]["relative_humidity_2m"],
    "rain": weather["hourly"]["precipitation"]
})

# ---------------- BİRLEŞTİR ----------------
final_df = df.merge(weather_df, on="hour", how="left")
final_df.drop(columns=["hour"], inplace=True)

final_df.to_csv(OUT_FILE, index=False)

print("✅ Sensör + hava durumu verileri birleştirildi")
