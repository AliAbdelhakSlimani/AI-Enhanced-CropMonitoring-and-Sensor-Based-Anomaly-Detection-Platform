from django.contrib import admin
from .models import SensorReading, AnomalyEvent, AgentRecommendation, FarmProfile, FieldPlot
# Register your models here.
admin.site.register(FarmProfile)
admin.site.register(FieldPlot)
admin.site.register(SensorReading)
admin.site.register(AnomalyEvent)
admin.site.register(AgentRecommendation)