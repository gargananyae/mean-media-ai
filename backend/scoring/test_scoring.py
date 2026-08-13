from backend.scoring.seo_score import calculate_seo_score
from backend.scoring.content_score import calculate_content_score
from backend.scoring.technical_score import calculate_technical_score
from backend.scoring.geo_score import calculate_geo_score
from backend.scoring.overall import calculate_overall_score


seo_features = {
    "title_exists": True,
    "title_length": 13,
    "meta_description_exists": True,
    "meta_description_length": 36,
    "h1_count": 1,
    "h2_count": 2,
    "h3_count": 0,
    "canonical_exists": True,
    "robots_meta_exists": True,
    "og_title_exists": True,
    "og_description_exists": True,
    "twitter_card_exists": True
}


content_features = {
    "word_count": 61,
    "paragraph_count": 3,
    "average_paragraph_length": 20.33,
    "h1_count": 1,
    "h2_count": 2,
    "h3_count": 0,
    "total_heading_count": 3,
    "unordered_list_count": 1,
    "ordered_list_count": 0,
    "total_list_count": 1
}


technical_features = {
    "uses_https": True,
    "language_declared": True,
    "language": "en",
    "charset_declared": False,
    "viewport_declared": True,
    "structured_data_present": True,
    "structured_data_count": 1,
    "favicon_present": True
}


geo_features = {
    "question_mark_count": 3,
    "question_density": 0.04918,
    "answer_like_paragraph_count": 1,
    "list_count": 1,
    "table_count": 0,
    "faq_signal": True,
    "definition_signal": True,
    "heading_count": 3
}


seo = calculate_seo_score(seo_features)

content = calculate_content_score(
    content_features
)

technical = calculate_technical_score(
    technical_features
)

geo = calculate_geo_score(
    geo_features
)

overall = calculate_overall_score(
    seo,
    content,
    technical,
    geo
)


print("SEO:", seo)
print("Content:", content)
print("Technical:", technical)
print("GEO:", geo)
print("Overall:", overall)