def calculate_geo_score(features):
    """
    Calculate a 0-100 Generative Engine Optimization score.

    The score measures structural and content signals
    that may improve AI-search understanding and retrieval.
    """

    score = 0

    # -------------------------
    # QUESTION-BASED CONTENT
    # -------------------------

    question_count = features[
        "question_mark_count"
    ]

    if question_count >= 1:
        score += 10

    if question_count >= 3:
        score += 5

    # -------------------------
    # ANSWER-LIKE CONTENT
    # -------------------------

    answer_paragraphs = features[
        "answer_like_paragraph_count"
    ]

    if answer_paragraphs >= 1:
        score += 15

    if answer_paragraphs >= 3:
        score += 5

    # -------------------------
    # STRUCTURED CONTENT
    # -------------------------

    if features["list_count"] > 0:
        score += 10

    if features["table_count"] > 0:
        score += 10

    # -------------------------
    # FAQ
    # -------------------------

    if features["faq_signal"]:
        score += 15

    # -------------------------
    # DEFINITIONS
    # -------------------------

    if features["definition_signal"]:
        score += 15

    # -------------------------
    # HEADINGS
    # -------------------------

    if features["heading_count"] >= 2:
        score += 10

    # -------------------------
    # FINAL SCORE
    # -------------------------

    return min(score, 100)