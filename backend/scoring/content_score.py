def calculate_content_score(features):
    """
    Calculate a 0-100 content quality score
    from measurable structural signals.
    """

    score = 0

    # -------------------------
    # WORD COUNT
    # -------------------------

    word_count = features["word_count"]

    if word_count >= 300:
        score += 20

    elif word_count >= 150:
        score += 15

    elif word_count >= 75:
        score += 10

    elif word_count > 0:
        score += 5

    # -------------------------
    # PARAGRAPHS
    # -------------------------

    paragraph_count = features[
        "paragraph_count"
    ]

    if paragraph_count >= 5:
        score += 15

    elif paragraph_count >= 3:
        score += 10

    elif paragraph_count > 0:
        score += 5

    # -------------------------
    # PARAGRAPH LENGTH
    # -------------------------

    avg_length = features[
        "average_paragraph_length"
    ]

    if 20 <= avg_length <= 100:
        score += 20

    elif avg_length > 0:
        score += 10

    # -------------------------
    # HEADING STRUCTURE
    # -------------------------

    if features["h1_count"] == 1:
        score += 15

    if features["h2_count"] >= 2:
        score += 10

    # -------------------------
    # LISTS
    # -------------------------

    if features["total_list_count"] > 0:
        score += 10

    return min(score, 100)