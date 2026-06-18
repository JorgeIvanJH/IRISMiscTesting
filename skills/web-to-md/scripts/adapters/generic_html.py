"""Last-resort adapter: any HTTP(S) page, converted via trafilatura.

Always claims pages in ``detect()``; place last in the ADAPTERS list.
"""
from __future__ import annotations

from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin

import trafilatura

from .base import Adapter, FetchResult


class _LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.title: str | None = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    self.links.append(v)
        elif tag == "title" and self.title is None:
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title and self.title is None:
            t = data.strip()
            if t:
                self.title = t


def _extract_links_and_title(html: str, base_url: str) -> tuple[list[str], str | None]:
    p = _LinkExtractor()
    try:
        p.feed(html)
    except Exception:
        pass
    out: list[str] = []
    seen: set[str] = set()
    for href in p.links:
        href = href.strip()
        if not href or href.startswith(("javascript:", "mailto:", "tel:", "#")):
            continue
        absolute = urldefrag(urljoin(base_url, href))[0]
        if absolute in seen:
            continue
        seen.add(absolute)
        out.append(absolute)
    return out, p.title


class GenericHtml(Adapter):
    name = "html"

    def detect(self, url: str, body: str) -> bool:
        return True  # last resort

    def fetch(self, url: str, body: str) -> FetchResult | None:
        links, title = _extract_links_and_title(body, url)
        md = trafilatura.extract(
            body,
            url=url,
            output_format="markdown",
            include_links=True,
            include_tables=True,
            include_formatting=True,
            favor_recall=True,
        ) or ""
        if not md.strip():
            return None
        return {
            "markdown": md,
            "title": title,
            "links": links,
            "source_url": url,
        }
