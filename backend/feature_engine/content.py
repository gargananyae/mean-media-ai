import re
from collections import Counter


def extract_content_features(soup):
    """
    Extract content-related features from a webpage.

    These features measure content depth, structure,
    readability, question/answer signals, and lexical diversity.
    """

    # -------------------------
    # PARAGRAPHS
    # -------------------------

    paragraphs = soup.find_all("p")

    paragraph_texts = [
        p.get_text(" ", strip=True)
        for p in paragraphs
    ]

    paragraph_texts = [
        text for text in paragraph_texts
        if text
    ]

    paragraph_count = len(paragraph_texts)

    # -------------------------
    # MAIN TEXT
    # -------------------------

    all_text = soup.get_text(" ", strip=True)

    words = all_text.split()

    word_count = len(words)

    # -------------------------
    # SENTENCES
    # -------------------------

    sentences = re.split(
        r"[.!?]+",
        all_text
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    sentence_count = len(sentences)

    # -------------------------
    # AVERAGE SENTENCE LENGTH
    # -------------------------

    if sentence_count > 0:
        average_sentence_length = (
            word_count / sentence_count
        )
    else:
        average_sentence_length = 0

    # -------------------------
    # AVERAGE PARAGRAPH LENGTH
    # -------------------------

    if paragraph_count > 0:
        average_paragraph_length = (
            word_count / paragraph_count
        )
    else:
        average_paragraph_length = 0

    # -------------------------
    # HEADINGS
    # -------------------------

    h1_count = len(soup.find_all("h1"))
    h2_count = len(soup.find_all("h2"))
    h3_count = len(soup.find_all("h3"))

    total_heading_count = (
        h1_count +
        h2_count +
        h3_count
    )

    # -------------------------
    # LISTS
    # -------------------------

    ul_count = len(soup.find_all("ul"))
    ol_count = len(soup.find_all("ol"))

    list_count = ul_count + ol_count

    # -------------------------
    # QUESTIONS
    # -------------------------

    question_count = all_text.count("?")

    question_density = (
        question_count /
        max(word_count, 1)
    )

    # -------------------------
    # NUMBERS / DATA SIGNAL
    # -------------------------

    numeric_tokens = re.findall(
        r"\b\d+(?:\.\d+)?%?\b",
        all_text
    )

    numeric_token_count = len(numeric_tokens)

    # -------------------------
    # ANSWER-LIKE PARAGRAPHS
    # -------------------------

    answer_like_paragraph_count = 0

    for paragraph in paragraph_texts:

        paragraph_words = paragraph.split()

        if 20 <= len(paragraph_words) <= 100:
            answer_like_paragraph_count += 1

    # -------------------------
    # DEFINITION SIGNAL
    # -------------------------

    definition_patterns = [
        r"\bis defined as\b",
        r"\brefers to\b",
        r"\bmeans\b",
        r"\bis a\b",
        r"\bis an\b"
    ]

    definition_signal = any(
        re.search(
            pattern,
            all_text,
            re.IGNORECASE
        )
        for pattern in definition_patterns
    )

    # -------------------------
    # ACTIONABLE LANGUAGE
    # -------------------------

    action_words = [
        "how",
        "use",
        "create",
        "build",
        "choose",
        "learn",
        "start",
        "improve",
        "increase",
        "reduce",
        "compare",
        "install",
        "follow",
        "apply"
    ]

    lowercase_text = all_text.lower()

    actionable_word_count = sum(
        lowercase_text.count(
            word
        )
        for word in action_words
    )

    # -------------------------
    # LEXICAL DIVERSITY
    # -------------------------

    normalized_words = re.findall(
        r"\b[a-zA-Z]+\b",
        lowercase_text
    )

    unique_words = set(
        normalized_words
    )

    if normalized_words:
        lexical_diversity = (
            len(unique_words) /
            len(normalized_words)
        )
    else:
        lexical_diversity = 0

    # -------------------------
    # REPEATED WORD SIGNAL
    # -------------------------

    word_counts = Counter(
        normalized_words
    )

    repeated_words = [
        word
        for word, count
        in word_counts.items()
        if count >= 5
    ]

    repeated_word_count = len(
        repeated_words
    )

    # -------------------------
    # TABLES
    # -------------------------

    table_count = len(
        soup.find_all("table")
    )

    # -------------------------
    # RETURN FEATURES
    # -------------------------

    return {

        "word_count":
            word_count,

        "sentence_count":
            sentence_count,

        "average_sentence_length":
            round(
                average_sentence_length,
                2
            ),

        "paragraph_count":
            paragraph_count,

        "average_paragraph_length":
            round(
                average_paragraph_length,
                2
            ),

        "h1_count":
            h1_count,

        "h2_count":
            h2_count,

        "h3_count":
            h3_count,

        "total_heading_count":
            total_heading_count,

        "unordered_list_count":
            ul_count,

        "ordered_list_count":
            ol_count,

        "total_list_count":
            list_count,

        "question_count":
            question_count,

        "question_density":
            round(
                question_density,
                5
            ),

        "numeric_token_count":
            numeric_token_count,

        "answer_like_paragraph_count":
            answer_like_paragraph_count,

        "definition_signal":
            definition_signal,

        "actionable_word_count":
            actionable_word_count,

        "lexical_diversity":
            round(
                lexical_diversity,
                3
            ),

        "repeated_word_count":
            repeated_word_count,

        "table_count":
            table_count
    }