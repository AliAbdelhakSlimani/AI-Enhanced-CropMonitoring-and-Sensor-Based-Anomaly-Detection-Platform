# ml/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from crop.models import SensorReading
from .threshold_detector import detect_and_create_anomaly

@receiver(post_save, sender=SensorReading)
def trigger_anomaly_detection(sender, instance, created, **kwargs):
    if created:  # seulement sur nouvelle lecture
        detect_and_create_anomaly(instance)