import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, accuracy_score
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- VERİ OKU ----------------
df = pd.read_csv("gul_sensor_verileri.csv")

# Sayısal tiplere çevir
cols = ["soil", "light", "temperature", "humidity"]
df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
df.dropna(inplace=True)

print(df.describe())

# ---------------- RİSK ETİKETİ (K-MEANS) ----------------
kmeans = KMeans(n_clusters=3, random_state=42)
df["risk_cluster"] = kmeans.fit_predict(
    df[["soil", "temperature", "humidity"]]
)

cluster_means = df.groupby("risk_cluster")["soil"].mean()
risk_map = cluster_means.sort_values().index.tolist()

mapping = {
    risk_map[0]: "High Risk",
    risk_map[1]: "Medium Risk",
    risk_map[2]: "Normal"
}

df["risk_label"] = df["risk_cluster"].map(mapping)

# ---------------- REGRESYON ----------------
X = df[["light", "temperature", "humidity"]]
y = df["soil"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

reg_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    random_state=42
)

reg_model.fit(X_train, y_train)
y_pred = reg_model.predict(X_test)

print("MAE (Soil Prediction):", mean_absolute_error(y_test, y_pred))

# ---------------- SINIFLANDIRMA ----------------
X_cls = df[["soil", "light", "temperature", "humidity"]]
y_cls = df["risk_label"]

X_train, X_test, y_train, y_test = train_test_split(
    X_cls, y_cls, test_size=0.2, random_state=42
)

clf = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42
)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("Risk Classification Accuracy:", accuracy_score(y_test, y_pred))

# ---------------- GRAFİK ----------------
sns.scatterplot(
    data=df,
    x="temperature",
    y="soil",
    hue="risk_label"
)
plt.title("Soil Moisture vs Temperature (Risk Levels)")
plt.show()
