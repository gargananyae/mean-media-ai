import requests
from bs4 import BeautifulSoup


def scrape_website(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    title = soup.title.string if soup.title else ""

    meta = soup.find("meta", attrs={"name": "description"})

    meta_description = ""

    if meta:
        meta_description = meta.get("content", "")

    headings = []

    for tag in soup.find_all(["h1", "h2", "h3"]):
        headings.append(tag.get_text(strip=True))

    paragraphs = []

    for p in soup.find_all("p"):
        paragraphs.append(p.get_text(strip=True))

    return {
        "title": title,
        "meta_description": meta_description,
        "headings": headings,
        "paragraphs": paragraphs
    }