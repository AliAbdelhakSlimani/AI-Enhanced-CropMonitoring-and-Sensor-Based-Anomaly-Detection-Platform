# crop/ml/apps.py
from django.apps import AppConfig

class MlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml'

    def ready(self):
        # Cette ligne est OBLIGATOIRE pour que les signals fonctionnent
        import ml.signals
        print("[ML APP] Application ML chargée – signaux activés")