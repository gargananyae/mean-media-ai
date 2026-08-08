from backend.crawler.client import fetch_html
from backend.crawler.parser import create_soup
from backend.feature_engine.technical import extract_technical_features


url = "https://www.apple.com"

html = fetch_html(url)

soup = create_soup(html)

features = extract_technical_features(
    soup,
    url
)

print(features)