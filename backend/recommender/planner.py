from backend.recommender.rules import RULES
from backend.recommender.priority import (
    prioritize_recommendations
)


def generate_recommendations(features):
    """
    Evaluate recommendation rules against
    extracted website features.
    """

    recommendations = []

    for rule in RULES:

        try:
            triggered = rule["condition"](features)

        except (KeyError, TypeError):
            triggered = False

        if triggered:

            try:
                evidence = rule["evidence"](features)
            except (KeyError, TypeError):
                evidence = {}

            recommendations.append({

                "id": rule["id"],

                "category":
                    rule["category"],

                "priority":
                    rule["priority"],

                "impact":
                    rule["impact"],

                "recommendation":
                    rule["message"],

                "evidence":
                    evidence
            })

    return prioritize_recommendations(
        recommendations
    )