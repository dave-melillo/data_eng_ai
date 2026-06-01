# Listing 12.3 Agent 1: URL discovery
import os

import openai
import requests
from pydantic import BaseModel

SERPAPI_KEY = os.getenv("SERPAPI_KEY")  #A


class URLRanking(BaseModel):  #B
    best_url: str
    confidence: str
    reasoning: str


URL_RANKING_SYSTEM_PROMPT = """
You are a data engineering assistant building a product database.
Given a product search key and candidate URLs, pick the single best
URL for extracting structured product data.
Prefer manufacturer/official pages and individual product pages.
Avoid review sites, forums, and category pages.
Return the best URL, a confidence level (high/medium/low), and a
brief reason.
"""  #C


@with_retries(max_attempts=3, exceptions=(requests.RequestException,))  #D
def _search(search_key, num_results=5):
    params = {
        "q": search_key,
        "api_key": SERPAPI_KEY,
        "num": num_results,
        "engine": "google",
    }
    resp = requests.get(
        "https://serpapi.com/search", params=params, timeout=15
    )
    resp.raise_for_status()
    return [
        {
            "title": r.get("title", ""),
            "url": r.get("link", ""),
            "snippet": r.get("snippet", ""),
        }
        for r in resp.json().get("organic_results", [])
    ]


def discover_url(search_key: str):  #E
    """Agent: find candidate URLs and let an LLM pick the best."""
    candidates = _search(search_key)  #F
    if not candidates:
        return None  #G
    listing = "\n".join(
        f"- {c['title']} | {c['url']} | {c['snippet']}"
        for c in candidates
    )
    user_prompt = (
        f"Product search key: {search_key}\n\n"
        f"Candidate URLs:\n{listing}"
    )
    completion = openai.beta.chat.completions.parse(  #H
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": URL_RANKING_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format=URLRanking,
    )
    return completion.choices[0].message.parsed  #I

#A Read the SerpAPI key from the environment (see sample.env)
#B The structured ranking contract, identical to Chapter 11
#C Decision rules that tell the model what a good source looks like
#D The search call wears the retry decorator from Listing 12.2
#E The agent: one job, search key in, a ranked URL out
#F Step 1, get candidate URLs from the search API
#G No candidates means nothing to rank; signal failure with None
#H Step 2, ask the cheap model to rank and justify its pick
#I Return the validated URLRanking object for the next agent
