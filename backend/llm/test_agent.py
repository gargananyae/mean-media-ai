from backend.llm.agent import generate_ai_analysis


scores = {
    "overall": 68,
    "seo": 45.4,
    "content": 70,
    "technical": 61.25,
    "geo": 80
}


features = {
    "seo": {
        "title_exists": True,
        "title_length": 5,
        "meta_description_exists": False,
        "h1_count": 1
    },
    "content": {
        "word_count": 1076,
        "paragraph_count": 33
    },
    "technical": {
        "uses_https": True,
        "structured_data_present": True
    },
    "geo": {
        "question_answer_coverage": 0,
        "definition_signal": True
    }
}


recommendations = [
    {
        "category": "SEO",
        "priority": "MEDIUM",
        "recommendation":
            "Expand the page title to provide more context."
    },
    {
        "category": "CONTENT",
        "priority": "MEDIUM",
        "recommendation":
            "Expand the page with useful, relevant content where appropriate."
    }
]


result = generate_ai_analysis(
    url="https://www.apple.com",
    scores=scores,
    features=features,
    recommendations=recommendations
)

print(result)