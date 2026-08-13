PRIORITY_WEIGHT = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}


def prioritize_recommendations(
    recommendations
):
    """
    Sort recommendations based on
    priority and estimated impact.
    """

    return sorted(
        recommendations,
        key=lambda item: (
            PRIORITY_WEIGHT[
                item["priority"]
            ],
            item["impact"]
        ),
        reverse=True
    )