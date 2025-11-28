from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SensorReading, AnomalyEvent, AgentRecommendation
from .serializers import (
    SensorReadingSerializer,
    AnomalyEventSerializer,
    AgentRecommendationSerializer,
)
from .permissions import IsDevice


# POST pour recevoir les données du simulateur (bulk support)
class SensorReadingIngestionView(APIView):
    permission_classes = [IsDevice]

    def post(self, request):
        data = request.data
        many = isinstance(data, list)
        serializer = SensorReadingSerializer(data=data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET pour récupérer les lectures (filtrable par plot)
class SensorReadingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SensorReading.objects.all().order_by('-timestamp')
    serializer_class = SensorReadingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        plot_id = self.request.query_params.get('plot')
        if plot_id:
            return self.queryset.filter(plot=plot_id)
            
        return self.queryset


# GET anomalies
class AnomalyEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AnomalyEvent.objects.all().order_by('-timestamp')
    serializer_class = AnomalyEventSerializer
    permission_classes = [IsAuthenticated]


# GET recommandations
class AgentRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AgentRecommendation.objects.all().order_by('-timestamp')
    serializer_class = AgentRecommendationSerializer
    permission_classes = [IsAuthenticated]