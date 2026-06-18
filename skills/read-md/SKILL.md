---
name: read-md
description: Efficiently navigate Markdown files and Markdown documentation directories without reading everything into context. Use for .md/.markdown files or directories of Markdown docs. Provides tools to index Markdown trees, show a heading table of contents with character counts, and extract specific sections.
compatibility: Requires Python 3.8+; no third-party packages.
---

# Read Markdown Efficiently

Use this skill to conserve context when working with Markdown. Do not read a large Markdown file directly. First find the right file, then inspect its headings, then extract only the needed section.

## Tools

```bash
python3 scripts/md-index.py <docs-dir>
python3 scripts/md-toc.py <file.md>
python3 scripts/md-read-section.py <file.md> --id <id> --metadata
```

All tools are dependency-free Python 3 scripts. They ignore YAML frontmatter and headings inside fenced code blocks.

Use script paths relative to this skill directory (for example, `scripts/md-index.py`) so the skill works when the repo is cloned anywhere.

## Workflow

### If the user gives a directory

1. Index the Markdown tree:

   ```bash
   python3 scripts/md-index.py path/to/docs --format table
   ```

2. Pick likely files from path, H1 title, size, and heading count.
3. Run `md-toc.py` on the best file.
4. Read the relevant section with `md-read-section.py`.

### If the user gives a Markdown file

1. Inspect headings and sizes:

   ```bash
   python3 scripts/md-toc.py path/to/file.md
   ```

2. Choose the smallest relevant heading section.
3. Extract it:

   ```bash
   python3 scripts/md-read-section.py path/to/file.md --id heading-id --metadata
   ```

4. If the section is too large, use the TOC to choose a child subsection.

## Tool Details

### `md-index.py` - index a Markdown directory

```bash
python3 scripts/md-index.py <directory> [--format tree|table|json] [--plain]
```

Use when given a documentation folder. It recursively finds `.md` and `.markdown` files.

Outputs per file:

- relative path
- character count
- line count
- heading count
- H1 title

Recommended modes:

```bash
# Sorted by size; good for choosing likely source files
python3 scripts/md-index.py docs --format table

# Directory-style overview
python3 scripts/md-index.py docs --format tree
```

### `md-toc.py` - inspect one Markdown file

```bash
python3 scripts/md-toc.py <file.md> [--max-depth 1-6] [--json]
```

Outputs one row per heading:

- `path`: outline path, for example `1.2.3`
- heading level and title
- line range
- characters in the full section subtree, including subsections
- body characters, excluding the heading line
- `id`: stable selector for `md-read-section.py`

Use the character counts to avoid reading sections that are too large.

### `md-read-section.py` - extract one section

```bash
python3 scripts/md-read-section.py <file.md> SELECTOR [options]
```

Use exactly one selector:

- `--id <id>`: preferred; use the id from `md-toc.py`
- `--path <path>`: outline path, for example `1.2.3`
- `--title <exact title>`: case-insensitive exact heading title; add `--occurrence N` for duplicates
- `--line <line>`: deepest heading section containing that line

Useful options:

- `--metadata`: show selected section, line range, and returned character count
- `--body-only`: omit the heading itself
- `--no-subsections`: stop before the first child heading

Examples:

```bash
python3 scripts/md-read-section.py docs/guide.md --id installation --metadata
python3 scripts/md-read-section.py docs/guide.md --path 2.1 --metadata
python3 scripts/md-read-section.py docs/guide.md --line 240 --metadata
```

## Rules for Agents

- For directories: run `md-index.py` first.
- For files: run `md-toc.py` before reading content, unless the file is tiny or has no headings.
- Prefer `md-read-section.py --id ... --metadata` over line-based file reading.
- Read the smallest section that can answer the question.
- If a section is too large, read a child section or use `--no-subsections`.
- If no headings exist, fall back to normal line-based reading.
