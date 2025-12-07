# ml/threshold_detector.py
from crop.models import SensorReading, AnomalyEvent, AgentRecommendation

# Plages normales (comme dans le cahier des charges)
NORMAL_RANGES = {
    "soil_moisture":   (45.0, 75.0),
    "air_temperature": (18.0, 28.0),
    "air_humidity":    (45.0, 75.0),
}

def _calculate_confidence(value: float, min_val: float, max_val: float) -> float:
    """
    Calcule une confiance réaliste entre 0.6 et 1.0 selon l'écart par rapport à la plage normale.
    Plus l'écart est grand → plus la confiance est élevée.
    """
    if value < min_val:
        deviation = min_val - value
        threshold = min_val * 0.15  # 15% sous la limite = anomalie claire
    else:  # value > max_val
        deviation = value - max_val
        threshold = max_val * 0.15   # 15% au-dessus = anomalie claire

    if deviation <= 0:
        return 0.6  # très proche du seuil → on reste prudent

    # Formule douce et très lisible
    confidence = 0.7 + (deviation / (deviation + threshold)) * 0.3

    # On cap à 1.0 et on arrondit à 3 décimales
    return round(min(1.0, confidence), 3)


def detect_and_create_anomaly(reading: SensorReading):
    value = float(reading.value)
    sensor_type = reading.sensor_type
    print(f"\n[ML ENGINE] Analyse en temps réel → Plot {reading.plot_id} | {sensor_type} = {value} | {reading.timestamp}")

    if sensor_type not in NORMAL_RANGES:
        return

    min_val, max_val = NORMAL_RANGES[sensor_type]

    if value < min_val or value > max_val:
        # === DÉTERMINATION DU TYPE D'ANOMALIE ===
        if sensor_type == "soil_moisture" and value < 35:
            anomaly_type = "irrigation_leak"
            severity = "high"
        elif sensor_type == "soil_moisture":
            anomaly_type = "dry_stress"
            severity = "medium"
        elif sensor_type == "air_temperature" and value > 32:
            anomaly_type = "heat_stress"
            severity = "high"
        elif sensor_type == "air_temperature":
            anomaly_type = "cold_stress"
            severity = "medium"
        elif sensor_type == "air_humidity" and value < 30:
            anomaly_type = "dry_stress"
            severity = "medium"
        elif sensor_type == "air_humidity":
            anomaly_type = "excess_moisture"
            severity = "high"
        else:
            anomaly_type = "unknown_anomaly"
            severity = "low"

        # === CALCUL DE LA CONFIANCE RÉELLE ===
        model_confidence = _calculate_confidence(value, min_val, max_val)

        print(f"[ANOMALIE DÉTECTÉE] {sensor_type} = {value} (hors plage {min_val}–{max_val}) "
              f"→ {anomaly_type} | confiance = {model_confidence} | severity = {severity}")

        # === CRÉATION DE L'ÉVÉNEMENT D'ANOMALIE ===
        event = AnomalyEvent.objects.create(
            plot=reading.plot,
            anomaly_type=anomaly_type,
            severity=severity,
            model_confidence=model_confidence  # ← maintenant c’est dynamique !
        )

        # === RECOMMANDATION AUTOMATIQUE ===
        AgentRecommendation.objects.create(
            anomaly=event,
            title=f"{anomaly_type.replace('_', ' ').title()} détectée",
            explanation_text=f"{sensor_type.replace('_', ' ')} = {value} (plage normale : {min_val}–{max_val})",
            recommended_action="Vérifier immédiatement la parcelle et les équipements.",
            confidence="high" if model_confidence >= 0.9 else "medium"
        )

    else:
        print(f"[NORMAL] {sensor_type} = {value} → dans la plage normale")