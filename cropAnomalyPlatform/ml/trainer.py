# crop/ml/trainer.py – VERSION FINALE QUI MARCHE À 100%
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cropAnomalyPlatform.settings')
django.setup()

from crop.models import SensorReading
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "ml", "models", "isolation_forest.joblib")

def train_isolation_forest():
    print("[TRAINER] Démarrage de l'entraînement Isolation Forest...")

    cutoff = pd.Timestamp.now() - pd.Timedelta(days=30)
    readings = SensorReading.objects.filter(timestamp__gte=cutoff)

    if readings.count() < 100:
        print(f"[TRAINER] Pas assez de données ({readings.count()} lectures) → annulé")
        return

    # ON AJOUTE 'timestamp' ICI
    data = readings.values('plot_id', 'sensor_type', 'value', 'timestamp')
    df = pd.DataFrame(list(data))

    # Pivot avec timestamp
    df_pivot = df.pivot_table(
        index=['plot_id', 'timestamp'],
        columns='sensor_type',
        values='value',
        aggfunc='mean'
    ).reset_index()

    df_pivot = df_pivot[['plot_id', 'air_temperature', 'air_humidity', 'soil_moisture']]
    df_final = df_pivot.groupby('plot_id').mean()
    df_final = df_final.fillna(method='ffill').fillna(method='bfill')
    df_final = df_final.dropna()

    X = df_final.values

    if len(X) == 0:
        print("[TRAINER] Aucune parcelle complète → annulé")
        return

    print(f"[TRAINER] {len(X)} parcelles utilisées")

    model = IsolationForest(contamination=0.05, n_estimators=100, random_state=42)
    model.fit(X)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"[TRAINER] Modèle sauvegardé : {MODEL_PATH}")

if __name__ == "__main__":
    train_isolation_forest()