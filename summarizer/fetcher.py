from __future__ import annotations

from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER_AGENT = "ClaudeTextSummarizer/1.0"
REQUEST_TIMEOUT = 20
MAX_CHARS = 80_000


def fetch_text_from_url(url: str) -> str:
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned = "\n".join(lines)
    return cleaned[:MAX_CHARS]


def read_text_file(path: str | Path) -> str:
    text = Path(path).read_text(encoding="utf-8")
    return text[:MAX_CHARS]
