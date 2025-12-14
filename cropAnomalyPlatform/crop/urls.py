# crop/urls.py – MODIFIE COMME ÇA
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'readings', views.SensorReadingViewSet)
router.register(r'anomalies', views.AnomalyEventViewSet)
router.register(r'recommandations', views.AgentRecommendationViewSet)
router.register(r'fieldplot', views.FieldPlotViewSet, basename='fieldplot')  

urlpatterns = [
    path('sensor-readings/', views.SensorReadingIngestionView.as_view(), name='ingest'),
    path('', include(router.urls)),
]