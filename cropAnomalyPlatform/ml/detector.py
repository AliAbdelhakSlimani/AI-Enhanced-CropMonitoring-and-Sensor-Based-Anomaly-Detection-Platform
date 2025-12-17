# crop/ml/detector.py – VERSION FINALE 100% PROPRE (aucun warning)
import os
import joblib
import numpy as np
import pandas as pd
from django.conf import settings
from crop.models import SensorReading, AnomalyEvent
from agent.engine import generate_smart_recommendation

# Chemin ABSOLU qui marche sur TON PC (Windows) ET en Docker
CURRENT_FILE = os.path.abspath(__file__)                    # → /app/ml/detector.py en Docker
ML_DIR = os.path.dirname(CURRENT_FILE)                      # → /app/ml
BASE_DIR = os.path.dirname(ML_DIR)                          # → /app
MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "isolation_forest.joblib")

print(f"[DEBUG] Chemin détecté : {MODEL_PATH}")
print(f"[DEBUG] Fichier existe ? {os.path.exists(MODEL_PATH)}")

NORMAL_RANGES = {
    "soil_moisture":   (45.0, 75.0),
    "air_temperature": (18.0, 28.0),
    "air_humidity":    (45.0, 75.0),
}

def _calculate_confidence(value: float, min_val: float, max_val: float) -> float:
    if value < min_val:
        deviation = min_val - value
        threshold = min_val * 0.15
    else:
        deviation = value - max_val
        threshold = max_val * 0.15
    if deviation <= 0:
        return 0.6
    confidence = 0.7 + (deviation / (deviation + threshold)) * 0.3
    return round(min(1.0, confidence), 3)

def _get_anomaly_type_and_severity(sensor_type: str, value: float) -> tuple[str, str]:
    if sensor_type == "soil_moisture":
        if value < 35: return "irrigation_leak", "high"
        else: return "dry_stress", "medium"
    elif sensor_type == "air_temperature":
        if value > 32: return "heat_stress", "high"
        else: return "cold_stress", "medium"
    elif sensor_type == "air_humidity":
        if value < 30: return "dry_stress", "medium"
        else: return "excess_moisture", "high"
    return "unknown_anomaly", "low"

def load_model():
    print("--------------------------------------------------")
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        
        print(f"[ML] Isolation Forest chargé : {MODEL_PATH}")
        return model
    print("[ML] Pas de modèle → fallback threshold")
    return None

def detect_anomaly(reading: SensorReading):
    value = float(reading.value)
    sensor_type = reading.sensor_type
    plot_id = reading.plot.id

    print(f"\n[ML ENGINE] Analyse → Plot {plot_id} | {sensor_type} = {value}")

    if sensor_type not in NORMAL_RANGES:
        return

    min_val, max_val = NORMAL_RANGES[sensor_type]

    # 1. Threshold rapide (obvious anomalies)
    if value < min_val or value > max_val:
        anomaly_type, severity = _get_anomaly_type_and_severity(sensor_type, value)
        confidence = _calculate_confidence(value, min_val, max_val)
        print(f"[ANOMALIE DÉTECTÉE] {sensor_type} = {value} → {anomaly_type} | confiance = {confidence}")

        event = AnomalyEvent.objects.create(
            plot=reading.plot,
            anomaly_type=anomaly_type,
            severity=severity,
            model_confidence=confidence
        )
        generate_smart_recommendation(event)
        return

    # 2. Isolation Forest pour anomalies subtiles
    model = load_model()
    if model is None:
        print(f"[NORMAL] {sensor_type} = {value}")
        return

    recent = SensorReading.objects.filter(
        plot=reading.plot,
        timestamp__gte=reading.timestamp - pd.Timedelta(hours=48)
    ).order_by('-timestamp')[:200].values('timestamp', 'sensor_type', 'value')

    if len(recent) < 20:
        print(f"[NORMAL] Pas assez de contexte")
        return

    df = pd.DataFrame(list(recent))
    
    # CORRECTION FUTURE WARNING – VERSION MODERNE
    pivot = (
        df.pivot(index='timestamp', columns='sensor_type', values='value')
          .ffill()
          .bfill()
    )
    
    X = pivot[['air_temperature', 'air_humidity', 'soil_moisture']].values

    scores = model.decision_function(X)
    is_anomaly = model.predict([X[-1]])[0] == -1

    if is_anomaly:
        confidence = _calculate_confidence(scores[-1] * -50, 0, 100)
        anomaly_type, severity = _get_anomaly_type_and_severity(sensor_type, value)
        print(f"[ANOMALIE DÉTECTÉE] {sensor_type} = {value} → {anomaly_type} | confiance = {confidence}")

        event = AnomalyEvent.objects.create(
            plot=reading.plot,
            anomaly_type=anomaly_type,
            severity=severity,
            model_confidence=confidence
        )
        generate_smart_recommendation(event)
    else:
        print(f"[NORMAL] {sensor_type} = {value}")
