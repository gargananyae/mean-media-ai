from backend.feature_engine.seo import (
    extract_seo_features
)

from backend.feature_engine.content import (
    extract_content_features
)

from backend.feature_engine.technical import (
    extract_technical_features
)

from backend.feature_engine.geo import (
    extract_geo_features
)


def extract_all_features(soup, url):
    """
    Run all Mean Media feature extraction modules
    and return one unified feature set.
    """

    seo_features = extract_seo_features(soup)

    content_features = extract_content_features(soup)

    technical_features = extract_technical_features(
        soup,
        url
    )

    geo_features = extract_geo_features(soup)

    return {
        "seo": seo_features,
        "content": content_features,
        "technical": technical_features,
        "geo": geo_features
    }