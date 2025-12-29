import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

DATA_FILE = "gul_sensor_weather.csv"
MODEL_FILE = "irrigation_model.pkl"

FEATURES = [
    "soil", "light", "temperature", "humidity",
    "temp_out", "humidity_out", "rain"
]

# ---------------- VERİ ----------------
df = pd.read_csv(DATA_FILE)
df[FEATURES] = df[FEATURES].apply(pd.to_numeric, errors="coerce")
df.dropna(inplace=True)

# ---------------- ETİKET ----------------
def irrigation_label(row):
    if row["soil"] > 600 and row["rain"] == 0 and row["temperature"] > 22:
        return 1
    return 0

df["irrigation"] = df.apply(irrigation_label, axis=1)

# ---------------- MODEL ----------------
X = df[FEATURES]
y = df["irrigation"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

joblib.dump(model, MODEL_FILE)
print("✅ Model hazır ve kaydedildi")
