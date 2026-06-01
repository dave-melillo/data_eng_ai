# Listing 12.4 Agent 2: fetch and clean
import requests
from bs4 import BeautifulSoup

REMOVE_TAGS = [  #A
    "script", "style", "nav", "footer", "header",
    "iframe", "noscript", "svg", "form",
]
REMOVE_CLASSES = [
    "breadcrumb", "related-products", "recently-viewed",
    "newsletter", "cookie-banner", "site-footer", "site-header",
    "cart-drawer", "search-modal", "review", "reviews", "ratings",
]

SESSION = requests.Session()  #B
SESSION.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
})


@with_retries(max_attempts=3, exceptions=(requests.RequestException,))  #C
def _fetch(url):
    resp = SESSION.get(url, timeout=20)
    resp.raise_for_status()
    return resp.text


def clean_html_aggressive(html: str) -> str:  #D
    """Strip non-product noise; returns extraction-ready text."""
    soup = BeautifulSoup(html, "html.parser")
    for tag_name in REMOVE_TAGS:
        for element in soup.find_all(tag_name):
            element.decompose()
    for pattern in REMOVE_CLASSES:
        for element in soup.find_all(
            class_=lambda c: c and pattern in " ".join(c).lower()
        ):
            element.decompose()
    return " ".join(soup.stripped_strings)


def fetch_and_clean(url: str) -> str:  #E
    """Agent: fetch a URL and return cleaned page text."""
    raw_html = _fetch(url)  #F
    cleaned = clean_html_aggressive(raw_html)  #G
    if len(cleaned) < 200:  #H
        raise ValueError("page too small after cleaning")
    return cleaned

#A The tag and class noise lists, carried over from Chapter 11
#B One reused Session with browser-like headers for every fetch
#C Network calls are flaky, so the fetch retries with backoff
#D The aggressive cleaner from Chapter 11, unchanged
#E The agent: a URL in, clean extraction-ready text out
#F Step 1, fetch raw HTML (with retries handled for us)
#G Step 2, strip the noise so we send fewer tokens downstream
#H Guard: a near-empty page usually means a block or JS-only render
