from backend.scoring.normalizer import (
    clamp,
    binary_score,
    range_score
)

from backend.scoring.weights import TECHNICAL_WEIGHTS


def calculate_technical_score(features):
    """
    Calculate the Mean Media Technical score.

    The score evaluates technical accessibility,
    indexability, mobile readiness, structured data,
    internationalization, and technical assets.
    """

    # ---------------------------------
    # HTTPS
    # ---------------------------------

    https_score = binary_score(
        features.get("uses_https", False)
    )

    # ---------------------------------
    # LANGUAGE
    # ---------------------------------

    language_score = binary_score(
        features.get("language_declared", False)
    )

    # ---------------------------------
    # CHARSET
    # ---------------------------------

    charset_score = binary_score(
        features.get("charset_declared", False)
    )

    # ---------------------------------
    # VIEWPORT
    # ---------------------------------

    viewport_score = binary_score(
        features.get("viewport_declared", False)
    )

    # ---------------------------------
    # MOBILE META
    # ---------------------------------

    mobile_meta_score = binary_score(
        features.get("mobile_meta_present", False)
    )

    # ---------------------------------
    # STRUCTURED DATA
    # ---------------------------------

    structured_data_count = features.get(
        "structured_data_count",
        0
    )

    if structured_data_count == 0:
        structured_data_score = 0

    elif structured_data_count == 1:
        structured_data_score = 75

    else:
        structured_data_score = 100

    # ---------------------------------
    # CANONICAL
    # ---------------------------------

    canonical_present = features.get(
        "canonical_present",
        features.get("canonical_exists", False)
    )

    canonical_absolute = features.get(
        "canonical_absolute",
        features.get("canonical_is_absolute", False)
    )

    if canonical_present and canonical_absolute:
        canonical_score = 100

    elif canonical_present:
        canonical_score = 60

    else:
        canonical_score = 0

    # ---------------------------------
    # HREFLANG
    # ---------------------------------

    hreflang_present = features.get(
        "hreflang_present",
        False
    )

    hreflang_count = features.get(
        "hreflang_count",
        0
    )

    if not hreflang_present:
        hreflang_score = 50

    elif hreflang_count == 1:
        hreflang_score = 60

    else:
        hreflang_score = 100

    # ---------------------------------
    # INDEXABILITY
    # ---------------------------------

    noindex = features.get(
        "noindex",
        False
    )

    nofollow = features.get(
        "nofollow",
        False
    )

    if noindex:
        indexability_score = 0

    elif nofollow:
        indexability_score = 70

    else:
        indexability_score = 100

    # ---------------------------------
    # TECHNICAL ASSETS
    # ---------------------------------

    script_count = features.get(
        "script_count",
        0
    )

    stylesheet_count = features.get(
        "stylesheet_count",
        0
    )

    # We don't reward more scripts.
    # We simply avoid penalizing normal
    # levels of technical assets.

    script_score = range_score(
        script_count,
        0,
        1,
        30,
        50
    )

    stylesheet_score = range_score(
        stylesheet_count,
        0,
        1,
        15,
        30
    )

    technical_assets_score = (
        script_score * 0.5
        + stylesheet_score * 0.5
    )

    # ---------------------------------
    # FINAL WEIGHTED SCORE
    # ---------------------------------

    score = (

        https_score
        * TECHNICAL_WEIGHTS["https"]

        + language_score
        * TECHNICAL_WEIGHTS["language"]

        + charset_score
        * TECHNICAL_WEIGHTS["charset"]

        + viewport_score
        * TECHNICAL_WEIGHTS["viewport"]

        + structured_data_score
        * TECHNICAL_WEIGHTS["structured_data"]

        + canonical_score
        * TECHNICAL_WEIGHTS["canonical"]

        + hreflang_score
        * TECHNICAL_WEIGHTS["hreflang"]

        + mobile_meta_score
        * TECHNICAL_WEIGHTS["mobile_meta"]

        + indexability_score
        * TECHNICAL_WEIGHTS["indexability"]

        + technical_assets_score
        * TECHNICAL_WEIGHTS["technical_assets"]
    )

    return round(
        clamp(score),
        2
    )