from django.db import models

class FarmProfile(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    total_size_hectares = models.DecimalField(max_digits=8, decimal_places=2)
    primary_crop = models.CharField(max_length=50)

    def __str__(self): return f"{self.name} ({self.owner})"

class FieldPlot(models.Model):
    farm = models.ForeignKey(FarmProfile, on_delete=models.CASCADE, related_name='plots')
    name = models.CharField(max_length=100)
    crop_variety = models.CharField(max_length=100)
    area_hectares = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self): return f"{self.farm.name} - {self.name}"

class SensorReading(models.Model):
    SENSOR_CHOICES = [
        ('soil_moisture', 'Soil Moisture'),
        ('air_temperature', 'Air Temperature'),
        ('air_humidity', 'Air Humidity'),
    ]
    plot = models.ForeignKey(FieldPlot, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    sensor_type = models.CharField(max_length=20, choices=SENSOR_CHOICES)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    source = models.CharField(max_length=20, default='simulator')

    class Meta:
        indexes = [models.Index(fields=['plot', '-timestamp'])]
        unique_together = ('plot', 'timestamp', 'sensor_type')

class AnomalyEvent(models.Model):
    ANOMALY_TYPES = [
        ('irrigation_leak', 'Irrigation Leak'),
        ('heat_stress', 'Heat Stress'),
        ('cold_stress', 'Cold Stress'),
        ('dry_stress', 'Dry Stress'),
        ('excess_moisture', 'Excess Moisture'),
        ('sensor_spike', 'Sensor Spike'),
        ('sensor_drift', 'Sensor Drift'),
        ('sensor_offline', 'Sensor Offline'),
    ]
    plot = models.ForeignKey(FieldPlot, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    anomaly_type = models.CharField(max_length=30, choices=ANOMALY_TYPES)
    severity = models.CharField(max_length=10, choices=[('low','Low'),('medium','Medium'),('high','High')])
    model_confidence = models.FloatField()

class AgentRecommendation(models.Model):
    anomaly = models.OneToOneField(AnomalyEvent, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    explanation_text = models.TextField()
    recommended_action = models.TextField()
    confidence = models.CharField(max_length=10, choices=[('low','Low'),('medium','Medium'),('high','High')])