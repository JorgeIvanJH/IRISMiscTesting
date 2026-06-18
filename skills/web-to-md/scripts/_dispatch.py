"""Adapter dispatch: pick the right adapter for a URL and run it."""
from __future__ import annotations

from typing import Optional

from _common import fetch_url
from adapters import ADAPTERS
from adapters.base import Adapter


def fetch_page(url: str) -> dict:
    """Fetch one URL and return a result dict.

    On success::

        {
            "markdown": str,
            "title": str | None,
            "links": list[str],
            "source_url": str,
            "mode": str,            # adapter.name
            "adapter": Adapter,     # the adapter instance (for .clean())
        }

    On failure::

        {"error": "fetch_failed" | "no_content", "url": url}
    """
    body = fetch_url(url)
    if body is None:
        return {"error": "fetch_failed", "url": url}

    for adapter in ADAPTERS:
        if not adapter.detect(url, body):
            continue
        result = adapter.fetch(url, body)
        if result is None:
            continue  # adapter declined; try the next one
        result["mode"] = adapter.name
        result["adapter"] = adapter
        return result

    return {"error": "no_content", "url": url}


def all_extra_followable_extensions() -> tuple[str, ...]:
    """Union of every registered adapter's extra followable extensions."""
    exts: set[str] = set()
    for a in ADAPTERS:
        exts.update(a.extra_followable_extensions())
    return tuple(exts)
