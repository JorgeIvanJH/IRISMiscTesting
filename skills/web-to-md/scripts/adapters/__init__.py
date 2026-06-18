"""Site-type adapters for web-to-md.

To add support for a new docs framework or site type, drop a new file in this
directory implementing :class:`Adapter` and append it to ``ADAPTERS`` below.
See ``references/adding-adapters.md`` in the skill for a full walkthrough.
"""
from __future__ import annotations

from .docsify import Docsify
from .hl7_fhir import Hl7Fhir
from .generic_html import GenericHtml

# Order matters: more specific adapters first. ``GenericHtml`` is the
# last-resort fallback and should always remain at the end.
ADAPTERS = [
    Docsify(),
    Hl7Fhir(),
    GenericHtml(),
]
