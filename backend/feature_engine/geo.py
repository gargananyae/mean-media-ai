import re


def extract_geo_features(soup):
    """
    Extract Generative Engine Optimization (GEO) signals.

    These features measure content structures that may help
    generative search systems understand, retrieve, and use
    information from a webpage.
    """

    # -------------------------
    # MAIN TEXT
    # -------------------------

    text = soup.get_text(" ", strip=True)

    words = text.split()

    word_count = len(words)

    # -------------------------
    # HEADINGS
    # -------------------------

    headings = soup.find_all(
        ["h1", "h2", "h3"]
    )

    heading_count = len(headings)

    heading_texts = [
        heading.get_text(" ", strip=True)
        for heading in headings
    ]

    # -------------------------
    # QUESTIONS
    # -------------------------

    question_patterns = [
        r"\?",
        r"\bwhat is\b",
        r"\bwhat are\b",
        r"\bhow does\b",
        r"\bhow do\b",
        r"\bwhy is\b",
        r"\bwhy are\b",
        r"\bhow to\b",
        r"\bcan i\b",
        r"\bshould i\b",
        r"\bwhich\b"
    ]

    question_signal_count = 0

    for pattern in question_patterns:

        question_signal_count += len(
            re.findall(
                pattern,
                text,
                re.IGNORECASE
            )
        )

    question_mark_count = text.count("?")

    # -------------------------
    # QUESTION HEADINGS
    # -------------------------

    question_headings = []

    for heading in heading_texts:

        heading_lower = heading.lower()

        if (
            "?" in heading
            or heading_lower.startswith("what ")
            or heading_lower.startswith("why ")
            or heading_lower.startswith("how ")
            or heading_lower.startswith("when ")
            or heading_lower.startswith("where ")
            or heading_lower.startswith("which ")
            or heading_lower.startswith("can ")
            or heading_lower.startswith("should ")
        ):
            question_headings.append(
                heading
            )

    question_heading_count = len(
        question_headings
    )

    # -------------------------
    # PARAGRAPHS
    # -------------------------

    paragraphs = soup.find_all("p")

    paragraph_texts = [
        p.get_text(" ", strip=True)
        for p in paragraphs
    ]

    paragraph_texts = [
        p for p in paragraph_texts
        if p
    ]

    paragraph_count = len(
        paragraph_texts
    )

    # -------------------------
    # ANSWER-LIKE PARAGRAPHS
    # -------------------------

    answer_like_paragraph_count = 0

    for paragraph in paragraph_texts:

        paragraph_words = (
            paragraph.split()
        )

        if 20 <= len(paragraph_words) <= 100:

            answer_like_paragraph_count += 1

    # -------------------------
    # QUESTION → ANSWER SIGNAL
    # -------------------------

    question_answer_pairs = 0

    for index, heading in enumerate(
        headings
    ):

        heading_text = heading.get_text(
            " ",
            strip=True
        )

        heading_lower = heading_text.lower()

        is_question = (
            "?" in heading_text
            or heading_lower.startswith("what ")
            or heading_lower.startswith("why ")
            or heading_lower.startswith("how ")
            or heading_lower.startswith("when ")
            or heading_lower.startswith("where ")
            or heading_lower.startswith("which ")
            or heading_lower.startswith("can ")
            or heading_lower.startswith("should ")
        )

        if not is_question:
            continue

        # Find the next paragraph after the heading
        next_element = heading.find_next("p")

        if next_element:

            answer_text = next_element.get_text(
                " ",
                strip=True
            )

            answer_words = answer_text.split()

            if 10 <= len(answer_words) <= 150:
                question_answer_pairs += 1

    # -------------------------
    # QUESTION ANSWER COVERAGE
    # -------------------------

    if question_heading_count > 0:

        question_answer_coverage = (
            question_answer_pairs /
            question_heading_count
        )

    else:

        question_answer_coverage = 0

    # -------------------------
    # DEFINITIONS
    # -------------------------

    definition_patterns = [
        r"\bis defined as\b",
        r"\brefers to\b",
        r"\bmeans\b",
        r"\bis a\b",
        r"\bis an\b",
        r"\bis the\b"
    ]

    definition_signal_count = 0

    for pattern in definition_patterns:

        definition_signal_count += len(
            re.findall(
                pattern,
                text,
                re.IGNORECASE
            )
        )

    definition_signal = (
        definition_signal_count > 0
    )

    # -------------------------
    # LISTS
    # -------------------------

    unordered_lists = soup.find_all("ul")
    ordered_lists = soup.find_all("ol")

    list_count = (
        len(unordered_lists) +
        len(ordered_lists)
    )

    # -------------------------
    # TABLES
    # -------------------------

    table_count = len(
        soup.find_all("table")
    )

    # -------------------------
    # FAQ SIGNAL
    # -------------------------

    faq_keywords = [
        "faq",
        "frequently asked questions",
        "common questions",
        "questions and answers"
    ]

    page_text_lower = text.lower()

    faq_signal = any(
        keyword in page_text_lower
        for keyword in faq_keywords
    )

    # -------------------------
    # EVIDENCE / CITATION SIGNAL
    # -------------------------

    links = soup.find_all("a")

    external_link_count = 0

    for link in links:

        href = link.get("href", "")

        if (
            href.startswith("http://")
            or href.startswith("https://")
        ):
            external_link_count += 1

    evidence_signal = (
        external_link_count > 0
    )

    # -------------------------
    # AUTHOR SIGNAL
    # -------------------------

    author_patterns = [
        "author",
        "written by",
        "by ",
        "published by"
    ]

    author_signal = any(
        pattern in page_text_lower
        for pattern in author_patterns
    )

    # -------------------------
    # DATE SIGNAL
    # -------------------------

    date_patterns = [
        r"\b20\d{2}\b",
        r"\bjan(?:uary)?\b",
        r"\bfeb(?:ruary)?\b",
        r"\bmar(?:ch)?\b",
        r"\bapr(?:il)?\b",
        r"\bmay\b",
        r"\bjun(?:e)?\b",
        r"\bjul(?:y)?\b",
        r"\baug(?:ust)?\b",
        r"\bsep(?:tember)?\b",
        r"\boct(?:ober)?\b",
        r"\bnov(?:ember)?\b",
        r"\bdec(?:ember)?\b"
    ]

    date_signal = any(
        re.search(
            pattern,
            text,
            re.IGNORECASE
        )
        for pattern in date_patterns
    )

    # -------------------------
    # STRUCTURED DATA
    # -------------------------

    json_ld = soup.find_all(
        "script",
        attrs={
            "type": "application/ld+json"
        }
    )

    structured_data_count = len(
        json_ld
    )

    structured_data_present = (
        structured_data_count > 0
    )

    # -------------------------
    # CONTENT STRUCTURE
    # -------------------------

    structure_signal = (
        heading_count >= 2
        and (
            paragraph_count > 0
            or list_count > 0
        )
    )

    # -------------------------
    # QUESTION DENSITY
    # -------------------------

    question_density = (
        question_signal_count /
        max(word_count, 1)
    )

    # -------------------------
    # RETURN FEATURES
    # -------------------------

    return {

        "question_mark_count":
            question_mark_count,

        "question_signal_count":
            question_signal_count,

        "question_density":
            round(
                question_density,
                5
            ),

        "question_heading_count":
            question_heading_count,

        "answer_like_paragraph_count":
            answer_like_paragraph_count,

        "question_answer_pairs":
            question_answer_pairs,

        "question_answer_coverage":
            round(
                question_answer_coverage,
                3
            ),

        "definition_signal":
            definition_signal,

        "definition_signal_count":
            definition_signal_count,

        "list_count":
            list_count,

        "table_count":
            table_count,

        "faq_signal":
            faq_signal,

        "external_link_count":
            external_link_count,

        "evidence_signal":
            evidence_signal,

        "author_signal":
            author_signal,

        "date_signal":
            date_signal,

        "structured_data_present":
            structured_data_present,

        "structured_data_count":
            structured_data_count,

        "structure_signal":
            structure_signal,

        "heading_count":
            heading_count
    }