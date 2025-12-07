# test_anomaly_now.py  ← à mettre à la racine DS2/
import requests
from datetime import datetime

# CONFIG – CHANGE UNIQUEMENT CES 2 LIGNES
URL = "http://127.0.0.1:8000/api/sensor-readings/"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0OTQ4MjM5LCJpYXQiOjE3NjQ4NjE4MzksImp0aSI6IjA1Zjg5NTE0NGY2YjRiNmM5MDZhZjI5OWEyYmY2OTZkIiwidXNlcl9pZCI6IjIifQ.P8KlECm1vytUiP6GerxMud-hB_tkkMIzx9DyCsSH6qY"

# Données qui FORCENT une anomalie (irrigation_leak + heat_stress)
data = [
    {"plot": 1, "sensor_type": "soil_moisture",   "value": 19.5},   # < 35 → fuite
    {"plot": 1, "sensor_type": "air_temperature", "value": 37.8},   # > 32 → canicule
    {"plot": 1, "sensor_type": "air_humidity",    "value": 28.0},
]

headers = {
    "Authorization": f"Bearer {JWT_TOKEN}",
    "Content-Type": "application/json"
}

print(f"[{datetime.now().strftime('%H:%M:%S')}] Envoi de 3 lectures avec 2 anomalies FORCÉES...")
response = requests.post(URL, json=data, headers=headers)

print(f"Status code : {response.status_code}")
if response.status_code == 201:
    print("SUCCÈS ! Données envoyées → l'app ml va créer les anomalies dans < 1 seconde")
    print("Va voir dans http://127.0.0.1:8000/admin → Anomaly Events")
else:
    print("ERREUR :")