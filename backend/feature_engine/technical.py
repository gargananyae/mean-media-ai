from urllib.parse import urlparse


def extract_technical_features(soup, url):
    """
    Extract technical website features.
    """

    parsed_url = urlparse(url)

    # -------------------------
    # HTTPS
    # -------------------------

    uses_https = parsed_url.scheme == "https"

    # -------------------------
    # LANGUAGE
    # -------------------------

    html_tag = soup.find("html")

    language = ""

    if html_tag:
        language = html_tag.get("lang", "")

    language_declared = bool(language)

    # -------------------------
    # CHARSET
    # -------------------------

    charset = soup.find("meta", charset=True)

    charset_declared = charset is not None

    # -------------------------
    # VIEWPORT
    # -------------------------

    viewport = soup.find(
        "meta",
        attrs={"name": "viewport"}
    )

    viewport_declared = viewport is not None

    # -------------------------
    # STRUCTURED DATA
    # -------------------------

    json_ld = soup.find_all(
        "script",
        attrs={"type": "application/ld+json"}
    )

    structured_data_count = len(json_ld)

    structured_data_present = structured_data_count > 0

    # -------------------------
    # FAVICON
    # -------------------------

    favicon = soup.find(
        "link",
        attrs={
            "rel": lambda value:
            value and "icon" in value
        }
    )

    favicon_present = favicon is not None

    # -------------------------
    # ROBOTS META
    # -------------------------

    robots_meta = soup.find(
        "meta",
        attrs={"name": "robots"}
    )

    robots_meta_present = robots_meta is not None

    robots_content = ""

    if robots_meta:
        robots_content = robots_meta.get(
            "content",
            ""
        ).lower()

    noindex = "noindex" in robots_content
    nofollow = "nofollow" in robots_content

    # -------------------------
    # CANONICAL
    # -------------------------

    canonical = soup.find(
        "link",
        attrs={"rel": "canonical"}
    )

    canonical_present = canonical is not None

    canonical_url = ""

    if canonical:
        canonical_url = canonical.get(
            "href",
            ""
        ).strip()

    canonical_absolute = (
        canonical_url.startswith("http://")
        or canonical_url.startswith("https://")
    )

    # -------------------------
    # HREFLANG
    # -------------------------

    hreflang_tags = soup.find_all(
        "link",
        attrs={"hreflang": True}
    )

    hreflang_count = len(hreflang_tags)

    hreflang_present = hreflang_count > 0

    # -------------------------
    # SITEMAP SIGNAL
    # -------------------------

    sitemap_link = soup.find(
        "link",
        attrs={
            "rel": lambda value:
            value and "sitemap" in value
        }
    )

    sitemap_link_present = sitemap_link is not None

    # -------------------------
    # RESOURCE SIGNALS
    # -------------------------

    script_count = len(soup.find_all("script"))
    stylesheet_count = len(
        soup.find_all("link", attrs={"rel": "stylesheet"})
    )

    image_count = len(soup.find_all("img"))

    # -------------------------
    # MOBILE SIGNAL
    # -------------------------

    mobile_meta_present = viewport_declared

    # -------------------------
    # RETURN FEATURES
    # -------------------------

    return {

        "uses_https": uses_https,

        "language_declared": language_declared,
        "language": language,

        "charset_declared": charset_declared,

        "viewport_declared": viewport_declared,
        "mobile_meta_present": mobile_meta_present,

        "structured_data_present":
            structured_data_present,

        "structured_data_count":
            structured_data_count,

        "favicon_present":
            favicon_present,

        "robots_meta_present":
            robots_meta_present,

        "noindex": noindex,

        "nofollow": nofollow,

        "canonical_present":
            canonical_present,

        "canonical_absolute":
            canonical_absolute,

        "hreflang_present":
            hreflang_present,

        "hreflang_count":
            hreflang_count,

        "sitemap_link_present":
            sitemap_link_present,

        "script_count":
            script_count,

        "stylesheet_count":
            stylesheet_count,

        "image_count":
            image_count
    }