
# simulator/simulator.py – VERSION RÉALISTE ET LOGIQUE (recommandée pour soutenance)
import time
import requests
import numpy as np
from datetime import datetime
import yaml
import os

# ================== CONFIG ==================
API_URL = "http://127.0.0.1:8000/api/sensor-readings/"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0OTQ4MjM5LCJpYXQiOjE3NjQ4NjE4MzksImp0aSI6IjA1Zjg5NTE0NGY2YjRiNmM5MDZhZjI5OWEyYmY2OTZkIiwidXNlcl9pZCI6IjIifQ.P8KlECm1vytUiP6GerxMud-hB_tkkMIzx9DyCsSH6qY"
FREQUENCY_MINUTES = 10
PLOTS = [1, 2]

SCENARIO_FILE = "simulator/scenarios/demo.yaml"

# Chargement scénario réaliste
SCENARIOS = {}
if os.path.exists(SCENARIO_FILE):
    with open(SCENARIO_FILE, 'r') as f:
        SCENARIOS = yaml.safe_load(f) or {}
    print(f"Scénario réaliste chargé : {SCENARIO_FILE}")
else:
    print("Fichier demo.yaml manquant → anomalies désactivées")

# ================== GÉNÉRATION RÉALISTE ==================
def generate_reading(plot_id):
    now = datetime.now()
    hour = now.hour + now.minute / 60.0
    day_of_week = now.weekday()  # 0 = lundi

    # --- Baseline réaliste (toujours dans plage normale par défaut) ---
    temp = 22 + 7 * np.sin(np.pi * (hour - 6) / 12) + np.random.normal(0, 1.2)
    humidity = 60 - 15 * np.sin(np.pi * (hour - 6) / 12) + np.random.normal(0, 4)
    moisture = 70 - (hour % 24) * 0.8 + np.random.normal(0, 3)  # décroît lentement

    # Clip de base (on autorise les dépassements seulement via injection logique)
    temp = np.clip(temp, 16, 30)
    humidity = np.clip(humidity, 40, 80)
    moisture = np.clip(moisture, 40, 85)

    # --- INJECTION LOGIQUE D'ANOMALIES (seulement si conditions réalistes) ---
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%Y-%m-%d")

    injected = False
    anomaly_type = None

    # --- INJECTION D'ANOMALIES À L'HEURE EXACTE (SANS DATE) ---
    print(SCENARIOS["plots"][plot_id].get("events", []))
    for event in SCENARIOS["plots"][plot_id].get("events", []):
        target_time = event["time"]           # ex: "15:10"
        current_time_str = now.strftime("%H:%M")  # ex: "15:10"
        print(f"DEBUG → plot {plot_id} | cible: {target_time} | actuel: {current_time_str}")
        # Comparaison EXACTE de l'heure (minute par minute)
        if current_time_str == target_time:
            print(f"ANOMALIE DÉCLENCHÉE À L'HEURE EXACTE → {event['type']} sur plot {plot_id}")

            if event["type"] == "irrigation_leak":
                moisture = 18.0
            elif event["type"] == "heat_stress":
                temp = 36.0
            elif event["type"] == "excess_moisture":
                moisture = 94.0
            elif event["type"] == "cold_stress":
               temp = 6.0
            elif event["type"] == "dry_stress":
                moisture = 25.0

            injected = True
            anomaly_type = event["type"]
            break  # important : on arrête après la première anomalie déclenchée

    # --- Anomalies naturelles rares (sans YAML) ---
    if not injected:
        # Fuite nocturne aléatoire (1 chance sur 200 → ~1 fois tous les 3 jours)
        if 2 <= now.hour <= 5 and np.random.rand() < 0.005:
            moisture = 22.0
            print("Fuite nocturne naturelle détectée")
            injected = True
            anomaly_type = "irrigation_leak"

        # Canicule l’après-midi (seulement si déjà chaud)
        if hour > 13 and temp > 26 and np.random.rand() < 0.01:
            temp = 35.0
            print("Canicule naturelle")
            injected = True
            anomaly_type = "heat_stress"

    return [
        {"plot": plot_id, "sensor_type": "air_temperature", "value": round(temp, 2)},
        {"plot": plot_id, "sensor_type": "air_humidity",    "value": round(humidity, 2)},
        {"plot": plot_id, "sensor_type": "soil_moisture",   "value": round(moisture, 2)},
    ], injected

# ================== BOUCLE ==================
print("Simulateur RÉALISTE démarré – 1 à 3 anomalies par jour")
headers = {"Authorization": f"Bearer {JWT_TOKEN}", "Content-Type": "application/json"}

try:
    while True:
        for plot_id in PLOTS:
            readings, anomaly = generate_reading(plot_id)
            r = requests.post(API_URL, json=readings, headers=headers)
            status = "OK" if r.status_code == 201 else f"ERREUR {r.status_code}"
            print(f"[{datetime.now().strftime('%H:%M')}] Plot {plot_id} → {status} | Anomalie: {anomaly}")
        time.sleep(FREQUENCY_MINUTES * 60)
except KeyboardInterrupt:
    print("\nSimulateur arrêté.")