from __future__ import annotations

from html.parser import HTMLParser

import requests

from app.services.parser_storage import save_parsed_page

REQUEST_TIMEOUT = 10


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._inside_title = False
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self._inside_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._inside_title = False

    def handle_data(self, data: str) -> None:
        if self._inside_title:
            self._parts.append(data.strip())

    @property
    def title(self) -> str:
        return " ".join(part for part in self._parts if part).strip()


def extract_title(html: str) -> str:
    parser = TitleParser()
    parser.feed(html)
    parser.close()
    return parser.title or "Title not found"


def fetch_title_sync(url: str) -> str:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    if response.encoding is None:
        response.encoding = response.apparent_encoding or "utf-8"
    return extract_title(response.text)


def parse_and_store_url(url: str, parser_type: str) -> dict[str, object]:
    title = fetch_title_sync(url)
    result = save_parsed_page(url, title, parser_type)
    result["message"] = "Parsing completed"
    return result
