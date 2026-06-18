"""Generic utilities shared by all adapters.

This module must stay free of site-specific logic. Anything tied to a
particular docs framework (docsify, mkdocs, sphinx, ...) belongs in an
adapter under ``scripts/adapters/``.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote, urldefrag, urljoin, urlparse, urlunparse

import trafilatura

# ---------- HTTP ----------

def fetch_url(url: str) -> str | None:
    """Download a URL. Returns the body as a string, or None on failure."""
    return trafilatura.fetch_url(url)


# ---------- URL handling ----------

SKIP_EXTS = {
    ".pdf", ".zip", ".tar", ".gz", ".tgz", ".rar", ".7z",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
    ".mp3", ".mp4", ".mov", ".avi", ".webm", ".wav",
    ".css", ".js", ".json", ".xml", ".rss",
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
}


def is_probably_html(url: str) -> bool:
    """Quick filter: is this URL plausibly an HTML page worth crawling?"""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    if not parsed.netloc:
        return False
    if any(c in parsed.path for c in "<>\""):
        return False
    path = parsed.path.lower()
    for ext in SKIP_EXTS:
        if path.endswith(ext):
            return False
    return True


def canonicalize_url(url: str) -> str:
    """Normalize a URL so equivalent routes collapse to one key.

    Heuristics that work well for documentation sites in general:
    - Drops fragments and ``?id=`` anchor-style query params (common in-page
      anchor convention used by docsify and a few others).
    - Strips a trailing ``.md`` suffix (so ``/foo`` and ``/foo.md`` collapse).
    - Removes trailing slash on non-root paths.

    If you ever need different behavior per site, prefer extending an adapter
    rather than adding flags here.
    """
    p = urlparse(url)
    path = p.path or "/"
    if path.lower().endswith(".md"):
        path = path[:-3] or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")
    query = p.query
    if query:
        kept = [kv for kv in query.split("&") if not kv.startswith("id=")]
        query = "&".join(kept)
    return urlunparse((p.scheme, p.netloc, path, "", query, ""))


_SLUG_RE = re.compile(r"[^a-z0-9._-]+")


def slug_from_url(url: str) -> str:
    """Last-resort filename stem when no page title is available."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    frag = parsed.fragment.lstrip("/").strip()
    combined = "/".join([p for p in [path, frag] if p])
    if not combined:
        stem = "index"
    else:
        combined = re.sub(r"\.html?$", "", combined, flags=re.IGNORECASE)
        combined = re.sub(r"\.md$", "", combined, flags=re.IGNORECASE)
        stem = combined.replace("/", "__")
    if parsed.query:
        stem += "__" + parsed.query
    stem = stem.lower()
    stem = _SLUG_RE.sub("-", stem)
    stem = stem.strip("-._") or "index"
    return stem[:120]


# ---------- Filesystem ----------

def unique_path(directory: Path, stem: str, suffix: str = ".md") -> Path:
    p = directory / f"{stem}{suffix}"
    i = 2
    while p.exists():
        p = directory / f"{stem}-{i}{suffix}"
        i += 1
    return p


def write_markdown(path: Path, markdown: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text((markdown or "").rstrip() + "\n", encoding="utf-8")


_TITLE_BAD_RE = re.compile(r'[\\/:*?"<>|\x00-\x1f]')
_TITLE_WS_RE = re.compile(r"\s+")


def filename_from_title(title: str | None) -> str | None:
    """Filesystem-safe filename stem derived from a page title (preserves case/spaces)."""
    if not title:
        return None
    t = _TITLE_BAD_RE.sub("", title)
    t = _TITLE_WS_RE.sub(" ", t).strip(" .")
    if not t:
        return None
    return t[:120]


# ---------- Markdown utilities (generic) ----------

FENCE_RE = re.compile(r"^(```|~~~)")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
MD_LINK_FULL_RE = re.compile(r'(\[[^\]]*\])\(([^)\s]+)(\s+"[^"]*")?\)')


def first_h1(md: str) -> str | None:
    """Return the cleaned text of the first H1 in a markdown document, if any."""
    for line in (md or "").splitlines():
        s = line.strip()
        if s.startswith("# "):
            t = re.sub(r"\{[^}]*\}", "", s[2:]).strip()  # strip Pandoc/kramdown {...} attrs
            t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
            t = re.sub(r"__([^_]+)__", r"\1", t)
            t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", t)
            t = re.sub(r"(?<!_)_([^_]+)_(?!_)", r"\1", t)
            t = re.sub(r"`([^`]+)`", r"\1", t)
            t = re.sub(r"\s+", " ", t).strip()
            return t or None
    return None


def parse_markdown_links(md: str, base_url: str) -> list[str]:
    """Extract absolute URLs from markdown link syntax."""
    out: list[str] = []
    seen: set[str] = set()
    for m in MD_LINK_RE.finditer(md or ""):
        href = m.group(1).strip()
        if not href or href.startswith(("javascript:", "mailto:", "tel:", "#")):
            continue
        absolute = urldefrag(urljoin(base_url, href))[0]
        if absolute in seen:
            continue
        seen.add(absolute)
        out.append(absolute)
    return out


def rewrite_internal_links(md: str, url_to_filename: dict[str, str], source_url: str) -> str:
    """Rewrite markdown links pointing at known crawled URLs to local filenames.

    External and unknown links are left as-is. Code blocks are not touched.
    """
    def repl(m: "re.Match[str]") -> str:
        text = m.group(1)
        href = m.group(2)
        title = m.group(3) or ""
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            return m.group(0)
        absolute = urldefrag(urljoin(source_url, href))[0]
        canon = canonicalize_url(absolute)
        if canon in url_to_filename:
            new_href = quote(url_to_filename[canon], safe="/")
            return f"{text}({new_href}{title})"
        return m.group(0)

    out: list[str] = []
    in_fence = False
    for line in (md or "").splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        out.append(MD_LINK_FULL_RE.sub(repl, line))
    return "\n".join(out)


def looks_like_html(body: str) -> bool:
    """True if the body appears to be HTML (used to reject SPA-shell responses)."""
    return bool(body) and body.lstrip().lower().startswith(("<!doctype", "<html"))
