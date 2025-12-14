from django.test import TestCase

# test_ml.py – TEST FINAL ISOLATION FOREST
import requests
import time

API_URL = "http://127.0.0.1:8000/api/sensor-readings/"
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1NTcxMTE1LCJpYXQiOjE3NjU0ODQ3MTUsImp0aSI6ImY4MWViY2RjOGY4ZDQ1ODJiNjg1NzI5Y2JiZTJjNTFiIiwidXNlcl9pZCI6IjIifQ.28wV3KxJuvZFsEZn4lDAkiCcbv3ZYsqW_R9EIWpJ4gM"

headers = {"Authorization": f"Bearer {JWT_TOKEN}", "Content-Type": "application/json"}

# 1. Envoie une lecture NORMALE
normal = [
    {"plot": 1, "sensor_type": "soil_moisture", "value": 60.0},
    {"plot": 1, "sensor_type": "air_temperature", "value": 24.0},
    {"plot": 1, "sensor_type": "air_humidity", "value": 65.0},
]
print("Envoi lecture NORMALE...")
requests.post(API_URL, json=normal, headers=headers)
time.sleep(2)

# 2. Envoie une lecture ANORMALE (fuite + canicule)
anomaly = [
    {"plot": 1, "sensor_type": "soil_moisture", "value": 18.0},   # fuite
    {"plot": 1, "sensor_type": "air_temperature", "value": 38.0}, # canicule
    {"plot": 1, "sensor_type": "air_humidity", "value": 22.0},    # air sec
]
print("Envoi lecture ANORMALE (fuite + canicule)...")
requests.post(API_URL, json=anomaly, headers=headers)

print("Test terminé – regarde les logs du serveur !")