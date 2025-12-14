from rest_framework import serializers
from .models import FarmProfile, FieldPlot, SensorReading, AnomalyEvent, AgentRecommendation

# crop/serializers.py – AJOUTE ÇA À LA FIN
class FieldPlotSerializer(serializers.ModelSerializer):
    farm_name = serializers.CharField(source='farm.name', read_only=True)

    class Meta:
        model = FieldPlot
        fields = ['id', 'name', 'farm_name', 'area_hectares', 'crop_variety']
class SensorReadingSerializer(serializers.ModelSerializer):
    plot = serializers.PrimaryKeyRelatedField(queryset=FieldPlot.objects.all())

    class Meta:
        model = SensorReading
        fields = '__all__'
        read_only_fields = ('timestamp', 'source')

class AnomalyEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnomalyEvent
        fields = '__all__'

class AgentRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentRecommendation
        fields = '__all__'