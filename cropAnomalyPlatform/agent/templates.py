# crop/agent/templates.py
TEMPLATES  = {
    "irrigation_leak": {
        "title": "Fuite d’irrigation détectée",
        "explanation": "L’humidité du sol a chuté brutalement de plus de 30 % en moins de 2 heures.",
        "action": "Vérifiez immédiatement les tuyaux, vannes et la pompe de la parcelle {plot_name}.",
        "priority": "Urgent"
    },
    "heat_stress": {
        "title": "Stress thermique élevé",
        "explanation": "La température dépasse 32 °C depuis plus de 3 heures consécutives.",
        "action": "Augmentez la fréquence d’irrigation ou installez un ombrage temporaire.",
        "priority": "Haute"
    },
    "cold_stress": {
        "title": "Risque de gel",
        "explanation": "Température inférieure à 10 °C détectée.",
        "action": "Protégez les cultures sensibles (bâches, chauffage si possible).",
        "priority": "Haute"
    },
    "dry_stress": {
        "title": "Sécheresse modérée",
        "explanation": "L’humidité du sol est entre 35 % et 45 % depuis plus de 12 heures.",
        "action": "Lancez un cycle d’arrosage supplémentaire dans les prochaines heures.",
        "priority": "Moyenne"
    },
    "excess_moisture": {
        "title": "Excès d’humidité – risque fongique",
        "explanation": "Humidité du sol supérieure à 85 % pendant plus de 8 heures.",
        "action": "Améliorez le drainage et réduisez l’arrosage.",
        "priority": "Moyenne"
    },
    "sensor_spike": {
        "title": "Valeur aberrante détectée",
        "explanation": "Une lecture a varié de plus de 40 % en une seule mesure.",
        "action": "Vérifiez le capteur – possible dysfonctionnement.",
        "priority": "Moyenne"
    },
    "default": {
        "title": "Anomalie détectée",
        "explanation": "Valeur hors plage normale.",
        "action": "Inspectez la parcelle pour identifier la cause.",
        "priority": "Moyenne"
    }
}