from django.apps import AppConfig


class MlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml'
    def ready(self):
        import ml.signals  # ← Charge les signals dès que l'app est prête