# Adding a new adapter

The `web-to-md` skill is structured around a small registry of **adapters**.
Each adapter handles one *kind* of website (a docs framework, a blog
platform, a specific host). The crawler tries adapters in order; the first
one whose `detect()` returns `True` owns the page. `GenericHtml` always sits
last as the catch-all.

This guide is for **pi extending the skill itself** when it encounters a new
site type. Follow it end-to-end.

## When you need a new adapter

You probably need one if any of these are true for a target site:

- The page is a JS-rendered SPA, so `trafilatura` returns near-empty content.
- The site has a non-standard markdown dialect (custom alert/admonition syntax,
  templating directives, attribute lists) that survives into the output as
  visible noise.
- Internal navigation lives in a structured file (`sitemap.xml`, `nav.yml`,
  `_sidebar.md`, `toc.yaml`) that you want to use instead of scraping `<a>` tags.
- You want to bypass the rendered HTML entirely and pull the markdown source
  directly (works for docsify, Docusaurus, mkdocs when the source is exposed).

If trafilatura already handles the site cleanly, **don't add an adapter** —
the `GenericHtml` fallback is doing its job.

## Anatomy

```
scripts/
├── _common.py              ← generic utils only; DO NOT add site-specific logic here
├── _dispatch.py            ← picks an adapter; you don't edit this
├── adapters/
│   ├── __init__.py         ← ADAPTERS list (registry)
│   ├── base.py             ← Adapter base class
│   ├── docsify.py          ← reference implementation
│   └── generic_html.py     ← catch-all (must stay last)
```

## Steps

### 1. Reconnaissance

Before writing code, characterize the site by hand:

```bash
# What's in the raw HTML? (look for generators, framework markers)
curl -sL <url> | grep -iE 'generator|docsify|mkdocs|docusaurus|vitepress|sphinx|gitbook' | head

# Is there a sitemap?
curl -sIL <url-host>/sitemap.xml | head -3

# Is the source markdown exposed at a predictable location?
curl -sIL <url>.md
curl -sIL <url-host>/docs/<route>.md
```

Decide:

- **Detection signal**: a unique substring/regex in the HTML that won't false-positive on unrelated sites.
- **Content source**: rendered HTML (use trafilatura), or a bypass URL (raw `.md`, JSON API, etc.).
- **Link source**: page anchors, `_sidebar.md`-style nav file, `sitemap.xml`, or the rendered HTML.
- **Cleanup needed**: any framework-specific markdown noise to strip or convert.

### 2. Create the adapter module

Copy `adapters/docsify.py` as a template. Implement at minimum:

```python
from .base import Adapter, FetchResult

class MyAdapter(Adapter):
    name = "mkdocs"   # short, lowercase, no spaces

    def detect(self, url: str, body: str) -> bool:
        # Be specific. Prefer the framework's own marker over guesses.
        return '<meta name="generator" content="mkdocs"' in body.lower()

    def fetch(self, url: str, body: str) -> FetchResult | None:
        # Return {markdown, title, links, source_url}, or None to decline.
        ...

    def clean(self, markdown: str) -> str:
        # Optional: remove framework-only markdown artefacts.
        return markdown

    def extra_followable_extensions(self) -> tuple[str, ...]:
        # Optional: extensions the crawler should follow even if they aren't HTML.
        return ()
```

Reuse helpers from `_common.py` instead of reinventing:

- `fetch_url(url)` — HTTP GET via trafilatura.
- `first_h1(md)` — clean title extraction from a markdown body.
- `parse_markdown_links(md, base_url)` — pull absolute URLs from markdown.
- `looks_like_html(body)` — guard against SPA-shell responses when fetching a `.md` bypass URL.
- `FENCE_RE`, `MD_LINK_RE` — pre-compiled regexes you'll likely want.

### 3. Register it

Edit `adapters/__init__.py`:

```python
from .docsify import Docsify
from .my_adapter import MyAdapter
from .generic_html import GenericHtml

ADAPTERS = [
    Docsify(),
    MyAdapter(),
    GenericHtml(),   # ALWAYS last
]
```

Order matters: more specific first. If two adapters could both claim a page,
put the one with the more specific detection signal earlier.

### 4. Test on the real site

```bash
# Clear any stale Python bytecode after editing adapter code:
find ~/.pi/agent/skills/web-to-md -name __pycache__ -exec rm -rf {} +

# One-page smoke test:
~/.pi/agent/skills/web-to-md/scripts/run.sh fetch.py <url> --out /tmp/test
# Confirm: result["mode"] is your adapter's name, content looks right, links present.

# Then a small crawl:
~/.pi/agent/skills/web-to-md/scripts/run.sh crawl.py <start-url> \
    --out /tmp/test --depth 1 --max-pages 5

# Verify the per-mode counts in the summary's "by_mode" field.
```

### 5. Verify with read-md

Use the `read-md` skill to sanity-check the output dir for hidden artefacts
(framework leftovers in headings, broken cross-links, garbage files):

```bash
python3 ~/.pi/agent/skills/read-md/scripts/md-index.py /tmp/test --format table
```

If you see junk in H1 titles or unexpected files, extend `clean()` and
re-run.

## Rules of thumb

- **Don't touch `_common.py` for site-specific logic.** If you feel tempted,
  the heuristic probably belongs in `clean()` or `fetch()` on your adapter.
- **`detect()` must be cheap and conservative.** It runs on every page. Match
  on a string the framework actually emits (a `<meta generator>` tag, a
  unique global JS variable name, etc.), not on URL patterns alone.
- **Prefer raw markdown sources over HTML→md conversion** when the source is
  exposed. You get the original formatting, code fences, and links intact.
- **Return `None` from `fetch()` to decline a page after detection.** The
  dispatcher will then try the next adapter (typically `GenericHtml`).
- **Adapter names should be lowercase identifiers** — they appear in crawl
  summaries as `by_mode` keys.
- If the new adapter needs a Python dependency, add it to `scripts/setup.sh`
  and document the requirement in `SKILL.md`'s `compatibility:` field.

## Worked reference

`adapters/docsify.py` is the canonical worked example. It demonstrates:

- A regex-based `detect()` matching multiple docsify markers.
- A `fetch()` that bypasses the SPA shell to pull `<route>.md`, with a
  fallback to `None` when the route has no underlying source.
- Sidebar-driven link discovery via `_sidebar.md`, with multiple candidate
  locations tried in order.
- A `clean()` that strips `{docsify-...}` heading attributes and converts
  `!>` / `?>` alerts to GitHub-flavored `> [!WARNING]` / `> [!TIP]` blocks,
  carefully skipping fenced code blocks.
- `extra_followable_extensions = (".md",)` because docsify sidebars sometimes
  link directly to `.md` files.

When in doubt, mirror its structure.
