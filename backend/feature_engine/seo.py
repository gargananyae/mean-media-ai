def extract_seo_features(soup):
    """
    Extract measurable on-page SEO features from a webpage.
    """

    # =========================================================
    # TITLE
    # =========================================================

    title = ""

    if soup.title and soup.title.string:
        title = soup.title.string.strip()

    title_exists = bool(title)
    title_length = len(title)
    title_word_count = len(title.split())

    # =========================================================
    # META DESCRIPTION
    # =========================================================

    meta_description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    meta_content = ""

    if meta_description:
        meta_content = meta_description.get(
            "content",
            ""
        ).strip()

    meta_description_exists = bool(meta_content)
    meta_description_length = len(meta_content)
    meta_word_count = len(meta_content.split())

    # =========================================================
    # HEADINGS
    # =========================================================

    h1_count = len(soup.find_all("h1"))
    h2_count = len(soup.find_all("h2"))
    h3_count = len(soup.find_all("h3"))

    headings = soup.find_all(
        ["h1", "h2", "h3"]
    )

    heading_sequence = [
        int(tag.name[1:])
        for tag in headings
    ]

    # =========================================================
    # HEADING HIERARCHY
    # =========================================================

    heading_hierarchy_valid = True

    previous_level = None

    for level in heading_sequence:

        if previous_level is not None:

            if level - previous_level > 1:
                heading_hierarchy_valid = False
                break

        previous_level = level

    # =========================================================
    # CANONICAL
    # =========================================================

    canonical = soup.find(
        "link",
        attrs={"rel": "canonical"}
    )

    canonical_exists = canonical is not None

    canonical_url = ""

    if canonical:
        canonical_url = canonical.get(
            "href",
            ""
        ).strip()

    canonical_is_absolute = (
        canonical_url.startswith("http://")
        or canonical_url.startswith("https://")
    )

    # =========================================================
    # ROBOTS META
    # =========================================================

    robots = soup.find(
        "meta",
        attrs={"name": "robots"}
    )

    robots_meta_exists = robots is not None

    robots_content = ""

    if robots:
        robots_content = robots.get(
            "content",
            ""
        ).lower()

    robots_blocks_indexing = (
        "noindex" in robots_content
    )

    # =========================================================
    # OPEN GRAPH
    # =========================================================

    og_title = soup.find(
        "meta",
        attrs={"property": "og:title"}
    )

    og_description = soup.find(
        "meta",
        attrs={"property": "og:description"}
    )

    og_image = soup.find(
        "meta",
        attrs={"property": "og:image"}
    )

    og_title_exists = og_title is not None
    og_description_exists = og_description is not None
    og_image_exists = og_image is not None

    # =========================================================
    # TWITTER / X CARD
    # =========================================================

    twitter_card = soup.find(
        "meta",
        attrs={"name": "twitter:card"}
    )

    twitter_title = soup.find(
        "meta",
        attrs={"name": "twitter:title"}
    )

    twitter_description = soup.find(
        "meta",
        attrs={"name": "twitter:description"}
    )

    twitter_image = soup.find(
        "meta",
        attrs={"name": "twitter:image"}
    )

    twitter_card_exists = twitter_card is not None
    twitter_title_exists = twitter_title is not None
    twitter_description_exists = twitter_description is not None
    twitter_image_exists = twitter_image is not None

    # =========================================================
    # IMAGES
    # =========================================================

    images = soup.find_all("img")

    image_count = len(images)

    images_with_alt = 0
    images_without_alt = 0

    for image in images:

        alt = image.get("alt")

        if alt is not None and alt.strip():
            images_with_alt += 1
        else:
            images_without_alt += 1

    if image_count > 0:
        alt_text_coverage = round(
            images_with_alt / image_count,
            3
        )
    else:
        alt_text_coverage = 1.0

    # =========================================================
    # LINKS
    # =========================================================

    links = soup.find_all("a")

    internal_link_count = 0
    external_link_count = 0
    nofollow_link_count = 0

    for link in links:

        href = link.get("href", "")

        if not href:
            continue

        if link.get("rel"):

            rel_values = [
                value.lower()
                for value in link.get("rel")
            ]

            if "nofollow" in rel_values:
                nofollow_link_count += 1

        if href.startswith(
            (
                "http://",
                "https://"
            )
        ):
            external_link_count += 1

        else:
            internal_link_count += 1

    # =========================================================
    # RETURN
    # =========================================================

    return {

        "title_exists": title_exists,
        "title_length": title_length,
        "title_word_count": title_word_count,

        "meta_description_exists":
            meta_description_exists,

        "meta_description_length":
            meta_description_length,

        "meta_word_count":
            meta_word_count,

        "h1_count": h1_count,
        "h2_count": h2_count,
        "h3_count": h3_count,

        "heading_sequence":
            heading_sequence,

        "heading_hierarchy_valid":
            heading_hierarchy_valid,

        "canonical_exists":
            canonical_exists,

        "canonical_is_absolute":
            canonical_is_absolute,

        "robots_meta_exists":
            robots_meta_exists,

        "robots_blocks_indexing":
            robots_blocks_indexing,

        "og_title_exists":
            og_title_exists,

        "og_description_exists":
            og_description_exists,

        "og_image_exists":
            og_image_exists,

        "twitter_card_exists":
            twitter_card_exists,

        "twitter_title_exists":
            twitter_title_exists,

        "twitter_description_exists":
            twitter_description_exists,

        "twitter_image_exists":
            twitter_image_exists,

        "image_count":
            image_count,

        "images_with_alt":
            images_with_alt,

        "images_without_alt":
            images_without_alt,

        "alt_text_coverage":
            alt_text_coverage,

        "internal_link_count":
            internal_link_count,

        "external_link_count":
            external_link_count,

        "nofollow_link_count":
            nofollow_link_count
    }