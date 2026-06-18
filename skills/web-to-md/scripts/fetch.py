#!/usr/bin/env python3
"""Fetch a single URL, write Markdown, print JSON summary with extracted links."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _common import filename_from_title, slug_from_url, unique_path, write_markdown
from _dispatch import fetch_page


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch one URL → Markdown + links JSON.")
    ap.add_argument("url")
    ap.add_argument("--out", required=True, help="Output directory.")
    ap.add_argument("--name", help="Filename (with or without .md). Default: derived from page title.")
    args = ap.parse_args()

    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    result = fetch_page(args.url)
    if "error" in result:
        print(json.dumps({k: v for k, v in result.items() if k != "adapter"}))
        return 2

    if args.name:
        stem = args.name[:-3] if args.name.endswith(".md") else args.name
    else:
        stem = filename_from_title(result.get("title")) or slug_from_url(args.url)
    path = unique_path(out_dir, stem)

    md = result["adapter"].clean(result["markdown"])
    write_markdown(path, md)

    print(json.dumps({
        "url": args.url,
        "source_url": result.get("source_url"),
        "mode": result.get("mode"),
        "title": result.get("title"),
        "file": str(path),
        "bytes": path.stat().st_size,
        "links": result.get("links", []),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
