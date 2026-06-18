"""Adapter for HL7 FHIR specification pages on hl7.org.

The generic trafilatura conversion works, but these pages often lose heading
structure and include table artefacts/punctuation glitches. This adapter adds
FHIR-specific cleanup to improve readability for local prototyping docs.
"""
from __future__ import annotations

import re
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlparse

import trafilatura

from .base import Adapter, FetchResult


class _LinkTitleExtractor(HTMLParser):
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
    p = _LinkTitleExtractor()
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


_TEMPLATE_LINE_RE = re.compile(r'^(<\[xmlns="http://hl7\.org/fhir">\]|\{\["resourceType"\s*:|@prefix fhir:)', re.IGNORECASE)


class Hl7Fhir(Adapter):
    name = "hl7_fhir"

    def detect(self, url: str, body: str) -> bool:
        p = urlparse(url)
        host = (p.netloc or "").lower()
        path = (p.path or "").lower()
        return ("hl7.org" in host) and ("/fhir/" in path)

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

        # Guarantee at least one heading for md navigation tools.
        if title and not re.search(r"^#\s+", md, flags=re.MULTILINE):
            md = f"# {title}\n\n{md}"

        return {
            "markdown": md,
            "title": title,
            "links": links,
            "source_url": url,
        }

    def clean(self, markdown: str) -> str:
        text = markdown or ""

        # Remove standalone table artefacts produced by conversion.
        lines: list[str] = []
        for line in text.splitlines():
            s = line.strip()
            if s in {"|", "|---|"}:
                continue
            if s.endswith("|") and "|" in s and len(s) <= 48:
                continue
            if _TEMPLATE_LINE_RE.match(s):
                continue
            lines.append(line)
        text = "\n".join(lines)

        # Remove release-box boilerplate line for readability.
        text = "\n".join(
            line for line in text.splitlines()
            if not line.startswith("This page is part of the FHIR Specification")
            and not line.startswith("This page has been approved as part of an")
        )

        # Promote standalone bold labels into real headings.
        out: list[str] = []
        for line in text.splitlines():
            m = re.match(r"^\*\*([^*][^*]*?)\*\*\s*$", line.strip())
            if m:
                out.append(f"## {m.group(1).strip()}")
            else:
                out.append(line)
        text = "\n".join(out)

        # Common punctuation/link spacing glitches from conversion.
        text = re.sub(r"\)and\[", ") and [", text)
        text = re.sub(r"\]and\[", "] and [", text)
        text = re.sub(r"(?<=\])(?=[A-Za-z0-9])", " ", text)
        text = re.sub(r"(?<=\))(?=[A-Za-z0-9])", " ", text)
        text = re.sub(r"(?<=\))(?=`)", "\n", text)
        text = re.sub(r"(?<=[A-Za-z0-9])(?=`[A-Za-z0-9_-]+`)", " ", text)
        text = re.sub(r"(?<=[A-Za-z0-9])(?=\[)", " ", text)
        text = re.sub(r"([.!?])\s+-\s+", r"\1\n- ", text)
        text = re.sub(r"([A-Za-z])\-\s+(?=[A-Z])", r"\1\n- ", text)
        text = re.sub(r"\.\-\s*", ".\n- ", text)
        text = re.sub(r"\n-\s*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip() + "\n"
