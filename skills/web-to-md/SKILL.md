---
name: web-to-md
description: "Scrape web pages and convert them to clean Markdown using a fully-local trafilatura pipeline. Provides a single-page `fetch` mode (one URL → one .md plus extracted links, agent decides what to follow next) and a recursive `crawl` mode (BFS-follow links from a starting URL up to a depth/page cap). Output goes into a user-specified directory. Architecture is adapter-based; a `docsify` adapter handles JS-rendered docsify SPAs, and a `GenericHtml` adapter handles everything else. New site types can be added by dropping a file into `scripts/adapters/`. Use when the user asks to scrape, mirror, or convert a documentation site or web page to Markdown."
compatibility: Requires Python 3.9+, internet access, and ~/.pi/agent/skills/web-to-md/.venv (created by scripts/setup.sh on first use).
---

# web-to-md

Local HTML→Markdown scraper using [trafilatura](https://trafilatura.readthedocs.io/). No external services.

## Setup (run once)

```bash
bash ~/.pi/agent/skills/web-to-md/scripts/setup.sh
```

Creates a venv inside the skill dir and installs `trafilatura`. Idempotent.

## Modes

### `fetch.py` — one page, agent-driven

Scrape a single URL. Saves one `.md` file and prints a JSON summary including
all outbound links so the agent can pick what to grab next.

```bash
~/.pi/agent/skills/web-to-md/scripts/run.sh fetch.py <url> --out <dir> [--name <filename>]
```

- `--out <dir>`: target directory (created if missing).
- `--name <filename>`: override the auto-derived filename. Default: derived
  from the page's `<h1>`/`<title>`, falling back to a URL slug.

Output: writes `<dir>/<Page Title>.md`. Prints JSON
`{file, title, url, source_url, mode, links: [...]}` to stdout. `mode` is
the name of the adapter that handled the page.

Use this when the user wants a single page, or when iterating selectively
(read page → decide which 2–3 links matter → fetch those).

### `crawl.py` — recursive bulk grab

Scrape a starting URL and follow its links breadth-first.

```bash
~/.pi/agent/skills/web-to-md/scripts/run.sh crawl.py <start-url> --out <dir> \
    [--depth 3] [--max-pages 100] [--same-domain] [--prefix /docs] [--delay 0.5]
```

- `--out <dir>`: target directory.
- `--depth N`: max link-follow depth (default 3; start URL is depth 0).
- `--max-pages N`: hard cap (default 100).
- `--same-domain` / `--no-same-domain`: restrict to the start URL's host (default: on).
- `--prefix <path>`: only follow URLs whose path starts with this. Repeatable.
- `--delay <seconds>`: politeness delay between requests (default 0.5).

Output: one `.md` per page, named after the page title (e.g. `Theme CSS.md`).
Internal links between crawled pages are rewritten to point at the local
filenames. Prints a JSON summary at the end with `pages_written`, a `by_mode`
breakdown, and any failures. **No manifest file**, so re-running into the same
directory creates `Theme CSS-2.md` etc.; clear the directory first if you
want clean output.

## Workflow

1. Confirm the target output directory with the user.
2. Run `setup.sh` if `.venv` doesn't exist in the skill directory.
3. For a docs site: prefer `crawl.py` with `--same-domain` and a `--prefix`
   matching the docs path.
4. For a single article or selective grabs: use `fetch.py`, read the returned
   `links`, decide what to fetch next.
5. After crawling, list the output dir and verify the summary's `failed` list
   is empty (or expected).
6. Optionally use the `read-md` skill to sanity-check the output:
   ```bash
   python3 ~/.pi/agent/skills/read-md/scripts/md-index.py <out-dir> --format table
   ```

## Example: Marpit docs (docsify site)

```bash
~/.pi/agent/skills/web-to-md/scripts/run.sh crawl.py \
    https://marpit.marp.app/markdown \
    --out "Documentation/Marpit Presentations" \
    --same-domain --depth 2 --max-pages 30
```

Produces `Marpit Markdown.md`, `Usage.md`, `Theme CSS.md`, etc. with
docsify-specific syntax (`!>` / `?>` alerts, `{docsify-ignore}` heading
attributes) cleaned up and internal links rewritten to local filenames.

## Architecture

```
scripts/
├── _common.py              # generic URL/markdown/filesystem utils
├── _dispatch.py            # adapter dispatch
├── fetch.py
├── crawl.py
└── adapters/
    ├── __init__.py         # ADAPTERS registry (ordered)
    ├── base.py             # Adapter base class
    ├── docsify.py          # JS-rendered docsify SPAs
    └── generic_html.py     # catch-all via trafilatura (always last)
```

Each adapter implements `detect`, `fetch`, optional `clean` and
`extra_followable_extensions`. The first adapter whose `detect()` matches a
page owns it; `GenericHtml` claims everything as a fallback.

## Extending the skill

**When you encounter a site type the current adapters don't handle well**
(JS-rendered SPA with empty trafilatura output, custom markdown dialect with
visible noise, structured navigation file you want to use, etc.) → read
[references/adding-adapters.md](references/adding-adapters.md) and add a new
adapter. It walks through reconnaissance, implementation, registration, and
testing. The `docsify` adapter is the worked reference.

Do not add site-specific logic to `_common.py`.

## Notes

- Filenames are derived from each page's `<h1>` (preserving case/spaces, with
  filesystem-illegal chars stripped). Falls back to a URL slug only if no
  title is available. Collisions get a numeric suffix.
- Files contain just the page markdown — no frontmatter.
- Binary/non-HTML links (pdf, zip, images, etc.) are skipped by default.
  Adapters can declare extra extensions to follow (e.g. docsify follows `.md`).
- After editing adapter code, clear `__pycache__` directories before testing:
  `find ~/.pi/agent/skills/web-to-md -name __pycache__ -exec rm -rf {} +`.
