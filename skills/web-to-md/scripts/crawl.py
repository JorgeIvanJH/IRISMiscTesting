#!/usr/bin/env python3
"""BFS-crawl a site starting at a URL, save each page as Markdown.

Pages are collected into memory first, so internal links can be rewritten to
point at the local filenames after we know what got written.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from collections import deque
from pathlib import Path
from urllib.parse import urlparse

from _common import (
    canonicalize_url,
    filename_from_title,
    is_probably_html,
    rewrite_internal_links,
    slug_from_url,
    write_markdown,
)
from _dispatch import all_extra_followable_extensions, fetch_page


def main() -> int:
    ap = argparse.ArgumentParser(description="BFS-crawl a site to Markdown.")
    ap.add_argument("start_url")
    ap.add_argument("--out", required=True)
    ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--max-pages", type=int, default=100)
    ap.add_argument("--same-domain", action=argparse.BooleanOptionalAction, default=True)
    ap.add_argument("--prefix", action="append", default=[],
                    help="Only follow URLs whose path starts with this. Repeatable.")
    ap.add_argument("--delay", type=float, default=0.5)
    args = ap.parse_args()

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    start_host = urlparse(args.start_url).netloc
    extra_exts = all_extra_followable_extensions()

    def allowed(url: str) -> bool:
        if not (is_probably_html(url) or url.lower().endswith(extra_exts)):
            return False
        p = urlparse(url)
        if not p.netloc:
            return False
        if args.same_domain and p.netloc != start_host:
            return False
        if args.prefix and not any(p.path.startswith(pref) for pref in args.prefix):
            return False
        return True

    start_canon = canonicalize_url(args.start_url)
    queue: deque[tuple[str, int]] = deque([(start_canon, 0)])
    visited: set[str] = {start_canon}

    # Phase 1: fetch.
    results: list[dict] = []
    failed: list[dict] = []
    while queue and len(results) < args.max_pages:
        url, depth = queue.popleft()

        if args.delay and results:
            time.sleep(args.delay)

        sys.stderr.write(f"[{len(results) + 1}/{args.max_pages} d={depth}] {url}\n")
        sys.stderr.flush()

        result = fetch_page(url)
        if "error" in result:
            failed.append({"url": url, "error": result["error"]})
            continue

        results.append({
            "canon_url": url,
            "source_url": result.get("source_url") or url,
            "title": result.get("title"),
            "markdown": result["markdown"],
            "mode": result.get("mode"),
            "adapter": result["adapter"],
        })

        if depth < args.depth:
            for link in result.get("links", []):
                if not allowed(link):
                    continue
                canon = canonicalize_url(link)
                if canon in visited:
                    continue
                visited.add(canon)
                queue.append((canon, depth + 1))

    # Phase 2: assign filenames.
    used: set[str] = set()
    for r in results:
        stem = filename_from_title(r["title"]) or slug_from_url(r["canon_url"])
        name = f"{stem}.md"
        i = 2
        while name in used:
            name = f"{stem}-{i}.md"
            i += 1
        used.add(name)
        r["filename"] = name
    url_to_filename = {r["canon_url"]: r["filename"] for r in results}

    # Phase 3: clean (per-adapter), rewrite links (generic), write.
    for r in results:
        md = r["adapter"].clean(r["markdown"])
        md = rewrite_internal_links(md, url_to_filename, r["source_url"])
        write_markdown(out_dir / r["filename"], md)

    summary = {
        "start_url": args.start_url,
        "out_dir": str(out_dir),
        "pages_written": len(results),
        "by_mode": _counts(r["mode"] for r in results),
        "failed": failed,
    }
    print(json.dumps(summary, indent=2))
    return 0


def _counts(seq):
    out: dict[str, int] = {}
    for x in seq:
        out[x] = out.get(x, 0) + 1
    return out


if __name__ == "__main__":
    sys.exit(main())
