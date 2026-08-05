def extract_title(soup):

    if soup.title:

        return soup.title.string

    return ""


def extract_meta_description(soup):

    meta = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if meta:

        return meta.get("content", "")

    return ""


def extract_headings(soup):

    headings = []

    for tag in soup.find_all(["h1", "h2", "h3"]):

        headings.append(
            tag.get_text(strip=True)
        )

    return headings


def extract_paragraphs(soup):

    paragraphs = []

    for p in soup.find_all("p"):

        paragraphs.append(
            p.get_text(strip=True)
        )

    return paragraphs