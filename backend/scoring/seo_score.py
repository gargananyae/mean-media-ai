from backend.scoring.normalizer import (
    clamp,
    binary_score,
    range_score
)

from backend.scoring.weights import SEO_WEIGHTS


def calculate_seo_score(features):
    """
    Calculate the Mean Media SEO score.

    Each SEO signal is normalized to 0-100
    and combined using weighted scoring.
    """

    # ---------------------------------
    # TITLE
    # ---------------------------------

    title_score = 0

    if features.get("title_exists", False):

        title_score = range_score(
            features.get("title_length", 0),
            0,
            30,
            60,
            100
        )

    # ---------------------------------
    # META DESCRIPTION
    # ---------------------------------

    meta_score = 0

    if features.get("meta_description_exists", False):

        meta_score = range_score(
            features.get(
                "meta_description_length",
                0
            ),
            0,
            120,
            160,
            250
        )

    # ---------------------------------
    # HEADINGS
    # ---------------------------------

    h1_score = (
        100
        if features.get("h1_count", 0) == 1
        else 0
    )

    h2_score = (
        100
        if features.get("h2_count", 0) > 0
        else 0
    )

    h3_score = (
        100
        if features.get("h3_count", 0) > 0
        else 0
    )

    heading_score = (
        h1_score * 0.60
        + h2_score * 0.25
        + h3_score * 0.15
    )

    # ---------------------------------
    # HEADING HIERARCHY
    # ---------------------------------

    hierarchy_score = binary_score(
        features.get(
            "heading_hierarchy_valid",
            False
        )
    )

    # ---------------------------------
    # CANONICAL
    # ---------------------------------

    canonical_score = binary_score(
        features.get(
            "canonical_exists",
            features.get(
                "canonical_present",
                False
            )
        )
    )

    # ---------------------------------
    # INDEXABILITY
    # ---------------------------------

    robots_blocks = features.get(
        "robots_blocks_indexing",
        False
    )

    indexability_score = (
        0
        if robots_blocks
        else 100
    )

    # ---------------------------------
    # IMAGES
    # ---------------------------------

    image_count = features.get(
        "image_count",
        0
    )

    alt_coverage = features.get(
        "alt_text_coverage",
        0
    )

    # Basic image presence score
    #
    # A page without images isn't
    # automatically considered bad.
    #
    # We give it a neutral score.

    if image_count == 0:
        image_score = 50
    else:
        image_score = 100

    # Alt-text coverage

    alt_text_score = clamp(
        alt_coverage * 100
    )

    # ---------------------------------
    # INTERNAL LINKS
    # ---------------------------------

    internal_links = features.get(
        "internal_link_count",
        0
    )

    internal_link_score = range_score(
        internal_links,
        0,
        10,
        50,
        100
    )

    # ---------------------------------
    # SOCIAL METADATA
    # ---------------------------------

    social_signals = [
        features.get(
            "og_title_exists",
            False
        ),

        features.get(
            "og_description_exists",
            False
        ),

        features.get(
            "og_image_exists",
            False
        ),

        features.get(
            "twitter_card_exists",
            False
        )
    ]

    social_score = (
        sum(social_signals)
        / len(social_signals)
    ) * 100

    # ---------------------------------
    # FINAL WEIGHTED SCORE
    # ---------------------------------

    score = (

        title_score
        * SEO_WEIGHTS["title"]

        + meta_score
        * SEO_WEIGHTS["meta_description"]

        + heading_score
        * SEO_WEIGHTS["headings"]

        + canonical_score
        * SEO_WEIGHTS["canonical"]

        + indexability_score
        * SEO_WEIGHTS["indexability"]

        + image_score
        * SEO_WEIGHTS["images"]

        + internal_link_score
        * SEO_WEIGHTS["internal_links"]

        + social_score
        * SEO_WEIGHTS["social_metadata"]

        + hierarchy_score
        * SEO_WEIGHTS["heading_hierarchy"]

        + alt_text_score
        * SEO_WEIGHTS["alt_text"]
    )

    return round(
        clamp(score),
        2
    )