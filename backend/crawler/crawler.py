from backend.crawler.client import fetch_html
from backend.crawler.parser import create_soup


def crawl(url):

    html = fetch_html(url)

    soup = create_soup(html)

    return {
        "url": url,
        "html": html,
        "soup": soup
    }