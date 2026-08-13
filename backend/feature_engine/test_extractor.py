from bs4 import BeautifulSoup

from backend.feature_engine.extractor import (
    extract_all_features
)


html = """
<html lang="en">

<head>

<title>Mean Media AI</title>

<meta
    name="description"
    content="AI powered SEO and GEO intelligence."
>

<meta
    name="robots"
    content="index, follow"
>

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<link
    rel="canonical"
    href="https://example.com"
>

<meta
    property="og:title"
    content="Mean Media AI"
>

<meta
    property="og:description"
    content="Website intelligence platform"
>

<meta
    name="twitter:card"
    content="summary"
>

<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Mean Media"
}
</script>

<link rel="icon" href="/favicon.ico">

</head>

<body>

<h1>What is GEO?</h1>

<p>
GEO refers to Generative Engine Optimization.
It helps businesses make their content easier
for AI systems to understand and retrieve.
</p>

<h2>How does GEO work?</h2>

<p>
GEO focuses on clear, structured and
answer-oriented content that provides
useful information to users.
</p>

<h2>Frequently Asked Questions</h2>

<p>
What is GEO and why does it matter?
</p>

<ul>

<li>Clear answers</li>
<li>Structured content</li>
<li>Explicit definitions</li>

</ul>

</body>

</html>
"""


soup = BeautifulSoup(
    html,
    "lxml"
)


features = extract_all_features(
    soup,
    "https://example.com"
)


for category, values in features.items():

    print("\n")
    print("=" * 40)
    print(category.upper())
    print("=" * 40)

    for key, value in values.items():

        print(f"{key}: {value}")