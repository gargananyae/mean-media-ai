from backend.crawler.client import fetch_html

from backend.crawler.parser import create_soup

from backend.crawler.content_extractor import (
    extract_title,
    extract_meta_description,
    extract_headings,
    extract_paragraphs
)


def crawl(url):

    html = fetch_html(url)

    soup = create_soup(html)

    return {

        "title":
            extract_title(soup),

        "meta_description":
            extract_meta_description(soup),

        "headings":
            extract_headings(soup),

        "paragraphs":
            extract_paragraphs(soup)
    }