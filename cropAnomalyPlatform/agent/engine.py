# crop/agent/engine.py  ← VERSION FINALE COMPATIBLE AVEC TON MODÈLE ACTUEL
from crop.models import AnomalyEvent, AgentRecommendation
from .templates import TEMPLATES

def generate_smart_recommendation(anomaly_event: AnomalyEvent):
    """
    Fonction appelée automatiquement après détection d'une anomalie
    → crée une AgentRecommendation intelligente et explicable
    Compatible avec le modèle existant (pas de champs priority/priority_color)
    """
    # Récupère le template correspondant au type d'anomalie
    template = TEMPLATES.get(anomaly_event.anomaly_type, TEMPLATES["default"])

    # Récupère les noms pour personnaliser le message
    plot_name = anomaly_event.plot.name
    farm_name = anomaly_event.plot.farm.name

    # Personnalisation du texte d'action avec les noms réels
    recommended_action = template["action"].format(
        plot_name=plot_name,
        farm_name=farm_name
    )

    # Détermination de la confiance affichée (low/medium/high) selon model_confidence
    if anomaly_event.model_confidence >= 0.90:
        confidence_level = "high"
    elif anomaly_event.model_confidence >= 0.75:
        confidence_level = "medium"
    else:
        confidence_level = "low"

    # Création ou mise à jour de la recommandation
    recommendation, created = AgentRecommendation.objects.update_or_create(
        anomaly=anomaly_event,
        defaults={
            "title": template["title"],
            "explanation_text": template["explanation"],
            "recommended_action": recommended_action,
            "confidence": confidence_level,  # ← respecte exactement tes choices
        }
    )

    status = "créée" if created else "mise à jour"
    print(f"[AI AGENT] Recommandation {status} → {template['title']} (confiance: {confidence_level})")

    return recommendation