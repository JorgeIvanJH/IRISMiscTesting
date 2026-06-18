"""Adapter for docsify-powered docs sites (e.g. marpit.marp.app).

Docsify is a JS-rendered SPA: every route returns the same ``index.html``
shell, and the actual content is fetched client-side from a sibling
``<route>.md`` file. We detect docsify, then bypass the shell and pull the
underlying markdown directly. Navigation comes from ``_sidebar.md``.
"""
from __future__ import annotations

import re
from urllib.parse import urlparse, urlunparse

from _common import (
    FENCE_RE,
    fetch_url,
    first_h1,
    looks_like_html,
    parse_markdown_links,
)

from .base import Adapter, FetchResult

_DETECT_RE = re.compile(r"window\.\$docsify|/docsify(?:@|\.min\.js|\.js)", re.IGNORECASE)
_HEADING_DECOR_RE = re.compile(r"\s*\{docsify[^}]*\}", re.IGNORECASE)
_ALERT_RE = re.compile(r"^(\s*)([!?])>\s?(.*)$")


def _md_url(url: str) -> str:
    """Map a docsify route URL to its underlying ``.md`` URL."""
    p = urlparse(url)
    path = p.path or "/"
    frag = p.fragment

    if frag.startswith("/"):
        # Hash mode (#/route): docsify is mounted at `path`, route is in fragment.
        mount = path if path.endswith("/") else path.rsplit("/", 1)[0] + "/"
        route = frag[1:]
    else:
        mount = ""
        route = path.lstrip("/")

    if route.endswith(".md"):
        md_path = route
    elif route == "" or route.endswith("/"):
        md_path = (route or "") + "README.md"
    else:
        md_path = route + ".md"

    new_path = (mount + md_path) if mount else "/" + md_path
    return urlunparse((p.scheme, p.netloc, new_path, "", "", ""))


def _sidebar_candidates(url: str) -> list[str]:
    """Likely ``_sidebar.md`` locations to try, most-specific first."""
    p = urlparse(url)
    md = _md_url(url)
    md_p = urlparse(md)
    md_dir = md_p.path.rsplit("/", 1)[0] + "/"
    candidates = [
        urlunparse((md_p.scheme, md_p.netloc, md_dir + "_sidebar.md", "", "", "")),
    ]
    root = urlunparse((p.scheme, p.netloc, "/_sidebar.md", "", "", ""))
    if root not in candidates:
        candidates.append(root)
    return candidates


class Docsify(Adapter):
    name = "docsify"

    def detect(self, url: str, body: str) -> bool:
        return bool(body) and bool(_DETECT_RE.search(body))

    def fetch(self, url: str, body: str) -> FetchResult | None:
        md_url = _md_url(url)
        md_body = fetch_url(md_url)
        # Reject SPA-shell responses: when the route has no real .md, the
        # server typically serves index.html for any path.
        if md_body and looks_like_html(md_body):
            md_body = None
        if not md_body:
            return None  # let the crawler record this as no_content

        links: list[str] = []
        seen: set[str] = set()
        for cand in _sidebar_candidates(url):
            sb = fetch_url(cand)
            if sb and not looks_like_html(sb):
                for link in parse_markdown_links(sb, cand):
                    if link not in seen:
                        seen.add(link)
                        links.append(link)
                break
        for link in parse_markdown_links(md_body, md_url):
            if link not in seen:
                seen.add(link)
                links.append(link)

        return {
            "markdown": md_body,
            "title": first_h1(md_body),
            "links": links,
            "source_url": md_url,
        }

    def clean(self, markdown: str) -> str:
        """Strip docsify-only artefacts: ``{docsify-...}`` heading decorations
        and ``!>`` / ``?>`` alert prefixes (converted to GitHub alert blockquotes).
        """
        out: list[str] = []
        in_fence = False
        for line in (markdown or "").splitlines():
            if FENCE_RE.match(line):
                in_fence = not in_fence
                out.append(line)
                continue
            if in_fence:
                out.append(line)
                continue
            if line.lstrip().startswith("#"):
                line = _HEADING_DECOR_RE.sub("", line).rstrip()
            m = _ALERT_RE.match(line)
            if m:
                indent, marker, body = m.groups()
                kind = "WARNING" if marker == "!" else "TIP"
                out.append(f"{indent}> [!{kind}]")
                if body.strip():
                    out.append(f"{indent}> {body}")
                continue
            out.append(line)
        return "\n".join(out)

    def extra_followable_extensions(self) -> tuple[str, ...]:
        # Docsify sidebars sometimes link directly to .md files.
        return (".md",)
