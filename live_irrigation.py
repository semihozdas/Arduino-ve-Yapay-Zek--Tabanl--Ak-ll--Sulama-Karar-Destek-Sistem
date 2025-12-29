import time
import serial
import requests
import pandas as pd
import joblib

# ================== AYARLAR ==================
PORT = "COM5"
BAUD = 9600

# Muş koordinatları
LAT = 38.7432
LON = 41.5064

MODEL_FILE = "irrigation_model.pkl"

FEATURES = [
    "soil", "light", "temperature", "humidity",
    "temp_out", "humidity_out", "rain"
]

LOOP_INTERVAL = 0.5
WEATHER_UPDATE_INTERVAL = 60

# ================== MODEL ==================
model = joblib.load(MODEL_FILE)
print("🧠 Model yüklendi")

# ================== SERIAL ==================
ser = serial.Serial(PORT, BAUD, timeout=0.1)
time.sleep(2)
ser.reset_input_buffer()
print("🔌 Akıllı Sulama Sistemi Çalışıyor")

# ================== HAVA DURUMU ==================
last_weather = 0
temp_out = 0
humidity_out = 0
rain = 0

def update_weather():
    global temp_out, humidity_out, rain, last_weather
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={LAT}&longitude={LON}"
            "&current=temperature_2m,relative_humidity_2m,precipitation"
        )
        w = requests.get(url, timeout=5).json()["current"]
        temp_out = w["temperature_2m"]
        humidity_out = w["relative_humidity_2m"]
        rain = w["precipitation"]
        last_weather = time.time()
    except:
        pass

# ================== ANA DÖNGÜ ==================
while True:
    try:
        now = time.time()
        if now - last_weather > WEATHER_UPDATE_INTERVAL:
            update_weather()

        line = ser.readline().decode().strip()
        if not line:
            time.sleep(LOOP_INTERVAL)
            continue

        soil, light = map(float, line.split(","))

        # 🔴 TOPRAK ÖNCELİĞİ
        if soil > 600:
            decision = 1
            reason = "SOIL-ÖNCELİK"
        else:
            sample = pd.DataFrame([[ 
                soil, light, 24.0, 40.0,
                temp_out, humidity_out, rain
            ]], columns=FEATURES)

            decision = model.predict(sample)[0]
            reason = "ML"

        ser.write(b"1" if decision == 1 else b"0")

        if decision == 1:
            print(f"🟢 Soil:{soil:.0f} | Temp:{temp_out:.1f}°C | Rain:{rain} → EVET ({reason})")
        else:
            print(f"🔴 Soil:{soil:.0f} | Temp:{temp_out:.1f}°C | Rain:{rain} → HAYIR ({reason})")

        time.sleep(LOOP_INTERVAL)

    except Exception as e:
        print("⚠️ Hata:", e)
        time.sleep(LOOP_INTERVAL)
