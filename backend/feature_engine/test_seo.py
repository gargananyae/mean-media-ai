from backend.crawler.client import fetch_html
from backend.crawler.parser import create_soup
from backend.feature_engine.seo import extract_seo_features


url = "https://www.apple.com"

html = fetch_html(url)

soup = create_soup(html)

features = extract_seo_features(soup)

print(features)