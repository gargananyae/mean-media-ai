RULES = [

    {
        "id": "missing_title",
        "category": "SEO",
        "condition": lambda f:
            not f["seo"]["title_exists"],
        "priority": "HIGH",
        "impact": 10,
        "message":
            "Add a unique and descriptive page title.",
        "evidence": lambda f: {
            "title_exists": f["seo"]["title_exists"],
            "title_length": f["seo"]["title_length"]
        }
    },

    {
        "id": "title_too_short",
        "category": "SEO",
        "condition": lambda f:
            f["seo"]["title_exists"]
            and f["seo"]["title_length"] < 30,
        "priority": "MEDIUM",
        "impact": 6,
        "message":
            "Expand the page title to provide more context.",
        "evidence": lambda f: {
            "title_length": f["seo"]["title_length"],
            "recommended_minimum": 30
        }
    },

    {
        "id": "title_too_long",
        "category": "SEO",
        "condition": lambda f:
            f["seo"]["title_length"] > 60,
        "priority": "MEDIUM",
        "impact": 6,
        "message":
            "Shorten the page title to keep it concise.",
        "evidence": lambda f: {
            "title_length": f["seo"]["title_length"],
            "recommended_maximum": 60
        }
    },

    {
        "id": "missing_meta_description",
        "category": "SEO",
        "condition": lambda f:
            not f["seo"]["meta_description_exists"],
        "priority": "HIGH",
        "impact": 8,
        "message":
            "Add a unique meta description summarizing the page.",
        "evidence": lambda f: {
            "meta_description_exists":
                f["seo"]["meta_description_exists"],
            "meta_description_length":
                f["seo"]["meta_description_length"]
        }
    },

    {
        "id": "weak_meta_description",
        "category": "SEO",
        "condition": lambda f:
            f["seo"]["meta_description_exists"]
            and f["seo"]["meta_description_length"] < 120,
        "priority": "MEDIUM",
        "impact": 5,
        "message":
            "Improve the meta description so it communicates the page value more clearly.",
        "evidence": lambda f: {
            "meta_description_length":
                f["seo"]["meta_description_length"],
            "recommended_minimum": 120
        }
    },

    {
        "id": "multiple_h1",
        "category": "SEO",
        "condition": lambda f:
            f["seo"]["h1_count"] != 1,
        "priority": "HIGH",
        "impact": 8,
        "message":
            "Use a clear single H1 heading for the primary topic.",
        "evidence": lambda f: {
            "h1_count": f["seo"]["h1_count"],
            "recommended_count": 1
        }
    },

    {
        "id": "missing_canonical",
        "category": "SEO",
        "condition": lambda f:
            not f["seo"]["canonical_exists"],
        "priority": "MEDIUM",
        "impact": 5,
        "message":
            "Add a canonical URL to clarify the preferred page version.",
        "evidence": lambda f: {
            "canonical_exists":
                f["seo"]["canonical_exists"]
        }
    },

    {
        "id": "missing_structured_data",
        "category": "TECHNICAL",
        "condition": lambda f:
            not f["technical"]["structured_data_present"],
        "priority": "MEDIUM",
        "impact": 7,
        "message":
            "Consider adding relevant Schema.org structured data.",
        "evidence": lambda f: {
            "structured_data_present":
                f["technical"]["structured_data_present"],
            "structured_data_count":
                f["technical"]["structured_data_count"]
        }
    },

    {
        "id": "missing_charset",
        "category": "TECHNICAL",
        "condition": lambda f:
            not f["technical"]["charset_declared"],
        "priority": "LOW",
        "impact": 3,
        "message":
            "Declare the page character encoding using a charset meta tag.",
        "evidence": lambda f: {
            "charset_declared":
                f["technical"]["charset_declared"]
        }
    },

    {
        "id": "missing_https",
        "category": "TECHNICAL",
        "condition": lambda f:
            not f["technical"]["uses_https"],
        "priority": "CRITICAL",
        "impact": 15,
        "message":
            "Serve the website over HTTPS.",
        "evidence": lambda f: {
            "uses_https":
                f["technical"]["uses_https"]
        }
    },

    {
        "id": "missing_faq",
        "category": "GEO",
        "condition": lambda f:
            not f["geo"]["faq_signal"],
        "priority": "MEDIUM",
        "impact": 6,
        "message":
            "Add sections that explicitly address common questions users may ask about this topic.",
        "evidence": lambda f: {
            "faq_signal":
                f["geo"]["faq_signal"],
            "question_count":
                f["geo"]["question_mark_count"]
        }
    },

    {
        "id": "missing_definitions",
        "category": "GEO",
        "condition": lambda f:
            not f["geo"]["definition_signal"],
        "priority": "MEDIUM",
        "impact": 6,
        "message":
            "Add explicit definitions for important concepts and entities.",
        "evidence": lambda f: {
            "definition_signal":
                f["geo"]["definition_signal"]
        }
    },

    {
        "id": "no_answer_content",
        "category": "GEO",
        "condition": lambda f:
            f["geo"]["answer_like_paragraph_count"] == 0,
        "priority": "HIGH",
        "impact": 8,
        "message":
            "Add concise, answer-oriented paragraphs that directly address important user questions.",
        "evidence": lambda f: {
            "answer_like_paragraph_count":
                f["geo"]["answer_like_paragraph_count"]
        }
    },

    {
        "id": "low_content_depth",
        "category": "CONTENT",
        "condition": lambda f:
            f["content"]["word_count"] < 300,
        "priority": "MEDIUM",
        "impact": 6,
        "message":
            "Expand the page with useful, relevant content where appropriate.",
        "evidence": lambda f: {
            "word_count":
                f["content"]["word_count"],
            "recommended_minimum": 300
        }
    },

    {
        "id": "low_actionability",
        "category": "CONTENT",
        "condition": lambda f:
            f["content"].get("actionable_word_count", 0) < 5,
        "priority": "LOW",
        "impact": 3,
        "message":
            "Add clearer actionable guidance, instructions, or next steps where appropriate.",
        "evidence": lambda f: {
            "actionable_word_count":
                f["content"].get("actionable_word_count", 0)
        }
    },

    {
        "id": "missing_author_signal",
        "category": "GEO",
        "condition": lambda f:
            not f["geo"].get("author_signal", False),
        "priority": "LOW",
        "impact": 3,
        "message":
            "Consider adding clear author or organization information to strengthen content attribution.",
        "evidence": lambda f: {
            "author_signal":
                f["geo"].get("author_signal", False)
        }
    },

    {
        "id": "missing_date_signal",
        "category": "GEO",
        "condition": lambda f:
            not f["geo"].get("date_signal", False),
        "priority": "LOW",
        "impact": 3,
        "message":
            "Consider displaying relevant publication or update dates where freshness matters.",
        "evidence": lambda f: {
            "date_signal":
                f["geo"].get("date_signal", False)
        }
    }
]