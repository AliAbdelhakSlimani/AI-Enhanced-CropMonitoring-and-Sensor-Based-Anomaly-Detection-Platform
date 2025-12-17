
# simulator/simulator.py – VERSION RÉALISTE ET LOGIQUE (recommandée pour soutenance)
import time
import requests
import numpy as np
from datetime import datetime
import yaml
import os

# ================== CONFIG ==================
API_URL = "http://127.0.0.1:8000/api/sensor-readings/"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY2MDgyMzQ2LCJpYXQiOjE3NjU5OTU5NDYsImp0aSI6ImEyNzBlYTc1OGEzMTQ2ZTRiOTIxYzQ2OWQzYTE1MTY2IiwidXNlcl9pZCI6IjIifQ.uKYeLzIwt1I5x2wB4zwz_4yXI7qqAneldXHaNOeFejs"
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
    #print(SCENARIOS["plots"][plot_id].get("events", []))
    for event in SCENARIOS["plots"][plot_id].get("events", []):
        target_time = event["time"]           # ex: "15:10"
        current_time_str = now.strftime("%H:%M")  # ex: "15:10"
        # Comparaison EXACTE de l'heure (minute par minute)
        if current_time_str == target_time:
                # === INJECTION AVEC RANGES RANDOM RÉALISTES ===
                # Explications pour chaque type d’anomalie (basé sur données agricoles réelles : USDA/FAO)
                # - irrigation_leak : sol très sec (10–32 % → chute brutale comme une fuite de pompe ; air légèrement sec par évaporation accélérée)
                # - heat_stress : temp haute (33–42 °C → canicule typique ; air très sec 15–35 % par chaleur ; sol légèrement sec)
                # - excess_moisture : sol saturé (86–98 % → inondation ou pluie lourde ; air saturé 88–98 % par humidité excessive)
                # - cold_stress : temp basse (0–9.9 °C → gel nocturne ; air humide 75–95 % car froid retient l'humidité)
                # - dry_stress : sol sec (25–44 % → sécheresse modérée ; air sec 30–50 % par manque d'eau)
                # Valeurs aléatoires avec np.random.uniform → naturel, non fixe
            if event["type"] == "irrigation_leak":
                moisture = round(np.random.uniform(10.0, 32.0), 2)  # sol très sec (chute brutale comme fuite)
                humidity = round(np.random.uniform(35.0, 55.0), 2)  # air légèrement sec (évaporation accélérée)

            elif event["type"] == "heat_stress":
                temp = round(np.random.uniform(33.0, 42.0), 2)      # temp haute (canicule typique)
                humidity = round(np.random.uniform(15.0, 35.0), 2)  # air très sec (chaleur évapore tout)
                moisture -= np.random.uniform(5.0, 15.0)           # sol légèrement sec (transpiration des plantes accélérée)

            elif event["type"] == "excess_moisture":
                moisture = round(np.random.uniform(86.0, 98.0), 2)  # sol saturé (inondation ou pluie lourde)
                humidity = round(np.random.uniform(88.0, 98.0), 2)  # air saturé (humidité excessive partout)
                temp -= np.random.uniform(2.0, 5.0)                # temp légèrement basse (humidité rafraîchit)

            elif event["type"] == "cold_stress":
                temp = round(np.random.uniform(0.0, 9.9), 2)        # temp basse (gel nocturne)
                humidity = round(np.random.uniform(75.0, 95.0), 2)  # air humide (froid retient l'humidité)
                moisture += np.random.uniform(2.0, 5.0)            # sol légèrement plus humide (condensation)
        
            elif event["type"] == "dry_stress":
                moisture = round(np.random.uniform(25.0, 44.0), 2)  # sol sec (sécheresse modérée)
                humidity = round(np.random.uniform(30.0, 50.0), 2)  # air sec (manque d'eau générale)
                temp += np.random.uniform(2.0, 5.0)                # temp légèrement plus haute (sécheresse chauffe l'air)
            injected = True
            anomaly_type = event["type"]
            break  # important : on arrête après la première anomalie déclenchée

    # --- Anomalies naturelles rares (sans YAML) ---
    if not injected:
        # Fuite nocturne aléatoire (1 chance sur 200 → ~1 fois tous les 3 jours)
        if 2 <= now.hour <= 5 and np.random.rand() < 0.005:
            moisture = round(np.random.uniform(10.0, 32.0), 2)
            humidity = round(np.random.uniform(35.0, 55.0), 2)
            print("Fuite nocturne naturelle détectée")
            injected = True
            anomaly_type = "irrigation_leak"

        # Canicule l’après-midi (seulement si déjà chaud)
        if hour > 13 and temp > 26 and np.random.rand() < 0.01:
            temp = round(np.random.uniform(33.0, 42.0), 2)
            humidity = round(np.random.uniform(15.0, 35.0), 2)
            moisture -= np.random.uniform(5.0, 15.0)
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
            print(f"[{datetime.now().strftime('%H:%M')}] Plot {plot_id} → {status} ")#| Anomalie: {anomaly}"
        time.sleep(FREQUENCY_MINUTES * 60)
except KeyboardInterrupt:
    print("\nSimulateur arrêté.")