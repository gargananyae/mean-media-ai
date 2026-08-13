from fastapi import APIRouter

from backend.api.schemas import Website

from backend.crawler.crawler import crawl

from backend.feature_engine.seo import extract_seo_features
from backend.feature_engine.content import extract_content_features
from backend.feature_engine.technical import extract_technical_features
from backend.feature_engine.geo import extract_geo_features

from backend.scoring.seo_score import calculate_seo_score
from backend.scoring.content_score import calculate_content_score
from backend.scoring.technical_score import calculate_technical_score
from backend.scoring.geo_score import calculate_geo_score
from backend.scoring.overall import calculate_overall_score

from backend.recommender.planner import generate_recommendations

from backend.llm.agent import generate_ai_analysis


router = APIRouter()


@router.post("/analyze")
def analyze(website: Website):

    # --------------------------------
    # 1. CRAWL WEBSITE
    # --------------------------------

    data = crawl(website.url)

    soup = data["soup"]

    # --------------------------------
    # 2. EXTRACT FEATURES
    # --------------------------------

    seo_features = extract_seo_features(soup)

    content_features = extract_content_features(soup)

    technical_features = extract_technical_features(
        soup,
        website.url
    )

    geo_features = extract_geo_features(soup)

    # --------------------------------
    # 3. COMBINE FEATURES
    # --------------------------------

    features = {
        "seo": seo_features,
        "content": content_features,
        "technical": technical_features,
        "geo": geo_features
    }

    # --------------------------------
    # 4. CALCULATE INDIVIDUAL SCORES
    # --------------------------------

    seo_score = calculate_seo_score(
        seo_features
    )

    content_score = calculate_content_score(
        content_features
    )

    technical_score = calculate_technical_score(
        technical_features
    )

    geo_score = calculate_geo_score(
        geo_features
    )

    # --------------------------------
    # 5. CALCULATE OVERALL SCORE
    # --------------------------------

    overall_score = calculate_overall_score(
        seo_score,
        content_score,
        technical_score,
        geo_score
    )

    # --------------------------------
    # 6. GENERATE RECOMMENDATIONS
    # --------------------------------

    recommendations = generate_recommendations(
        features
    )

    # --------------------------------
    # 7. GENERATE AI ANALYSIS
    # --------------------------------

    scores = {
        "overall": overall_score,
        "seo": seo_score,
        "content": content_score,
        "technical": technical_score,
        "geo": geo_score
    }

    ai_analysis = generate_ai_analysis(
        url=website.url,
        scores=scores,
        features=features,
        recommendations=recommendations
    )

    # --------------------------------
    # 8. RETURN COMPLETE ANALYSIS
    # --------------------------------

    return {
        "url": website.url,

        "scores": scores,

        "features": features,

        "recommendations": recommendations,

        "ai_analysis": ai_analysis
    }