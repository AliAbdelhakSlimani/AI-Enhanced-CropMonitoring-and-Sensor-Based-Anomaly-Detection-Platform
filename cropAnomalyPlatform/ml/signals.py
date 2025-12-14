# crop/ml/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from crop.models import SensorReading
from .detector import detect_anomaly  # ← ton nouveau détecteur hybride

@receiver(post_save, sender=SensorReading)
def trigger_anomaly_detection(sender, instance, created, **kwargs):
    if created:
        print(f"[SIGNAL] Nouvelle lecture reçue → Plot {instance.plot.id} | {instance.sensor_type} = {instance.value}")
        detect_anomaly(instance)  # ← appelle le système hybride