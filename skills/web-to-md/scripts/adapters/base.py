"""Adapter base class.

An adapter handles one *kind* of website (docsify, mkdocs, sphinx, a specific
blog platform, etc.). The crawler iterates registered adapters in order; the
first whose ``detect()`` returns True owns the page.
"""
from __future__ import annotations

from typing import Optional, TypedDict


class FetchResult(TypedDict, total=False):
    markdown: str         # Page content as Markdown.
    title: Optional[str]  # Page title (for filenames).
    links: list[str]      # Absolute URLs to consider following.
    source_url: str       # The URL we actually got the markdown from
                          # (may differ from the input URL — e.g. docsify
                          # fetches a sibling .md file).


class Adapter:
    """Subclass and override what you need.

    Required: ``name``, ``detect``, ``fetch``.
    Optional: ``clean``, ``extra_followable_extensions``.
    """

    #: Short identifier reported in crawl results. Lowercase, no spaces.
    name: str = "base"

    def detect(self, url: str, body: str) -> bool:
        """Return True if this adapter should handle the given page."""
        raise NotImplementedError

    def fetch(self, url: str, body: str) -> Optional[FetchResult]:
        """Extract markdown + links from the page.

        Return None to decline the page after detection (the crawler will then
        try the next adapter, falling back to :class:`GenericHtml`).
        """
        raise NotImplementedError

    def clean(self, markdown: str) -> str:
        """Optional post-processing for this adapter's markdown output.

        Run after extraction, before internal-link rewriting. Default: no-op.
        """
        return markdown

    def extra_followable_extensions(self) -> tuple[str, ...]:
        """File extensions the crawler should follow even though they aren't HTML.

        Example: docsify sidebars sometimes link directly to ``.md`` files.
        """
        return ()
