from rest_framework import serializers
from .models import FarmProfile, FieldPlot, SensorReading, AnomalyEvent, AgentRecommendation

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