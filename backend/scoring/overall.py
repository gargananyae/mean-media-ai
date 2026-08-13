def calculate_overall_score(
    seo_score,
    content_score,
    technical_score,
    geo_score
):
    """
    Calculate the overall Mean Media score.

    Current weighting:
        SEO         = 30%
        Content     = 25%
        Technical   = 20%
        GEO         = 25%
    """

    overall = (
        seo_score * 0.30
        + content_score * 0.25
        + technical_score * 0.20
        + geo_score * 0.25
    )

    return round(overall, 2)