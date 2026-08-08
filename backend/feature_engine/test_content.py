from backend.crawler.client import fetch_html
from backend.crawler.parser import create_soup
from backend.feature_engine.content import extract_content_features


url = "https://www.apple.com"

html = fetch_html(url)

soup = create_soup(html)

features = extract_content_features(soup)

print(features)