#!/usr/bin/env python3
"""Markdown navigation helpers for the read-md-file skill.

No third-party dependencies. Parses Markdown headings while ignoring fenced code blocks,
then exposes a compact table of contents and section extraction primitives.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Optional


ATX_RE = re.compile(r"^( {0,3})(#{1,6})(?:[ \t]+|$)(.*)$")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
SETEXT_RE = re.compile(r"^ {0,3}(=+|-+)\s*$")


@dataclass
class Heading:
    index: int
    level: int
    title: str
    id: str
    path: str
    start_line: int
    heading_end_line: int
    end_line: int
    start_offset: int
    heading_end_offset: int
    end_offset: int
    chars: int
    body_chars: int


def read_text(path: str | Path) -> str:
    p = Path(path).expanduser()
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return p.read_text(encoding="utf-8-sig")


def line_offsets(text: str) -> list[int]:
    offsets = [0]
    for m in re.finditer(r"\n", text):
        offsets.append(m.end())
    return offsets


def line_end_offsets(lines: list[str]) -> list[int]:
    ends = []
    pos = 0
    for line in lines:
        pos += len(line)
        ends.append(pos)
    return ends


def clean_atx_title(raw: str) -> str:
    # Remove optional closing sequence of # characters preceded by whitespace.
    title = raw.rstrip()
    title = re.sub(r"[ \t]+#+[ \t]*$", "", title)
    return title.strip()


def slugify(title: str) -> str:
    slug = title.strip().lower()
    slug = re.sub(r"[`*_~\[\](){}<>]", "", slug)
    slug = re.sub(r"[^a-z0-9 _.-]+", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-.")
    return slug or "heading"


def unique_slug(base: str, seen: dict[str, int]) -> str:
    n = seen.get(base, 0) + 1
    seen[base] = n
    return base if n == 1 else f"{base}-{n}"


def iter_heading_markers(text: str) -> Iterable[tuple[int, int, str, int]]:
    """Yield (level, start_line, title, heading_end_line), one-indexed lines."""
    lines = text.splitlines(keepends=True)
    in_fence = False
    fence_marker = ""
    prev_content_line: Optional[tuple[int, str]] = None
    frontmatter_until = 0
    if lines and lines[0].rstrip("\r\n") == "---":
        for j, candidate in enumerate(lines[1:], start=2):
            if candidate.rstrip("\r\n") == "---":
                frontmatter_until = j
                break

    for i, line in enumerate(lines, start=1):
        if i <= frontmatter_until:
            continue
        stripped_newline = line.rstrip("\r\n")
        fence = FENCE_RE.match(stripped_newline)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker[0]
            elif marker.startswith(fence_marker * 3):
                in_fence = False
                fence_marker = ""
            prev_content_line = None
            continue

        if in_fence:
            continue

        atx = ATX_RE.match(stripped_newline)
        if atx:
            yield (len(atx.group(2)), i, clean_atx_title(atx.group(3)), i)
            prev_content_line = None
            continue

        setext = SETEXT_RE.match(stripped_newline)
        if setext and prev_content_line is not None:
            prev_line_no, prev_text = prev_content_line
            level = 1 if setext.group(1).startswith("=") else 2
            yield (level, prev_line_no, prev_text.strip(), i)
            prev_content_line = None
            continue

        # Candidate setext title: a non-blank line that is not indented as code.
        if stripped_newline.strip() and not stripped_newline.startswith(("    ", "\t")):
            prev_content_line = (i, stripped_newline)
        elif not stripped_newline.strip():
            prev_content_line = None


def parse_headings(text: str) -> list[Heading]:
    lines = text.splitlines(keepends=True)
    starts = line_offsets(text)
    ends = line_end_offsets(lines)
    markers = list(iter_heading_markers(text))
    seen: dict[str, int] = {}
    counters = [0] * 7
    headings: list[Heading] = []

    for idx, (level, start_line, title, heading_end_line) in enumerate(markers):
        for deeper in range(level + 1, 7):
            counters[deeper] = 0
        counters[level] += 1
        path = ".".join(str(counters[n]) for n in range(1, level + 1) if counters[n] > 0)
        start_offset = starts[start_line - 1]
        heading_end_offset = ends[heading_end_line - 1] if heading_end_line - 1 < len(ends) else len(text)

        # Section subtree ends at the next heading of same or higher level.
        end_line = len(lines)
        end_offset = len(text)
        for next_level, next_start_line, _next_title, _next_end_line in markers[idx + 1 :]:
            if next_level <= level:
                end_line = next_start_line - 1
                end_offset = starts[next_start_line - 1]
                break

        chars = max(0, end_offset - start_offset)
        body_chars = max(0, end_offset - heading_end_offset)
        headings.append(
            Heading(
                index=idx + 1,
                level=level,
                title=title,
                id=unique_slug(slugify(title), seen),
                path=path,
                start_line=start_line,
                heading_end_line=heading_end_line,
                end_line=end_line,
                start_offset=start_offset,
                heading_end_offset=heading_end_offset,
                end_offset=end_offset,
                chars=chars,
                body_chars=body_chars,
            )
        )
    return headings


def format_toc(path: str | Path, text: str, headings: list[Heading], max_depth: int = 6) -> str:
    p = Path(path).expanduser()
    out = []
    out.append(f"File: {p}")
    out.append(f"Document: {len(text)} chars, {len(text.splitlines())} lines, {len(headings)} headings")
    out.append("")
    out.append("Columns: path | heading | lines | chars in section subtree | body chars | id")
    out.append("-" * 88)
    for h in headings:
        if h.level > max_depth:
            continue
        indent = "  " * (h.level - 1)
        title = h.title or "(untitled)"
        out.append(
            f"{h.path:>8} | {indent}H{h.level} {title} | "
            f"{h.start_line}-{h.end_line} | {h.chars} | {h.body_chars} | {h.id}"
        )
    if not headings:
        out.append("No Markdown headings found. Use line-based reading for this file.")
    return "\n".join(out)


def select_heading(headings: list[Heading], args: argparse.Namespace) -> Heading:
    matches: list[Heading]
    selector_count = sum(
        bool(x)
        for x in [
            getattr(args, "id", None),
            getattr(args, "path", None),
            getattr(args, "title", None),
            getattr(args, "line", None),
        ]
    )
    if selector_count != 1:
        raise SystemExit("Specify exactly one selector: --id, --path, --title, or --line")

    if args.id:
        matches = [h for h in headings if h.id == args.id]
    elif args.path:
        matches = [h for h in headings if h.path == args.path]
    elif args.title:
        title = args.title.strip().lower()
        matches = [h for h in headings if h.title.strip().lower() == title]
        if args.occurrence < 1:
            raise SystemExit("--occurrence must be >= 1")
        if len(matches) >= args.occurrence:
            return matches[args.occurrence - 1]
        raise SystemExit(f"No occurrence {args.occurrence} for title {args.title!r}; found {len(matches)}")
    else:
        line = int(args.line)
        # Prefer the deepest section containing the line.
        matches = [h for h in headings if h.start_line <= line <= h.end_line]
        matches.sort(key=lambda h: (h.level, h.start_line), reverse=True)
        if matches:
            return matches[0]
        raise SystemExit(f"No heading section contains line {line}")

    if not matches:
        raise SystemExit("No matching heading found. Run the toc command to see valid ids/paths.")
    if len(matches) > 1:
        raise SystemExit("Ambiguous selector. Use --id from toc output or --title with --occurrence.")
    return matches[0]


def section_text(text: str, h: Heading, body_only: bool = False, no_subsections: bool = False, headings: Optional[list[Heading]] = None) -> tuple[str, int, int]:
    start_offset = h.heading_end_offset if body_only else h.start_offset
    start_line = h.heading_end_line + 1 if body_only else h.start_line
    end_offset = h.end_offset
    end_line = h.end_line
    if no_subsections and headings is not None:
        for n in headings:
            if n.start_line > h.start_line and n.start_line <= h.end_line and n.level > h.level:
                end_offset = n.start_offset
                end_line = n.start_line - 1
                break
    return text[start_offset:end_offset], start_line, end_line


def cmd_toc(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Print a Markdown table of contents with section character counts.")
    ap.add_argument("file", help="Markdown file to inspect")
    ap.add_argument("--max-depth", type=int, default=6, choices=range(1, 7), metavar="1-6")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = ap.parse_args(argv)

    text = read_text(args.file)
    headings = parse_headings(text)
    if args.json:
        print(json.dumps({"file": str(Path(args.file).expanduser()), "chars": len(text), "lines": len(text.splitlines()), "headings": [asdict(h) for h in headings if h.level <= args.max_depth]}, indent=2))
    else:
        print(format_toc(args.file, text, headings, args.max_depth))
    return 0


def cmd_read(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Read one section from a Markdown file by heading id, path, title, or line.")
    ap.add_argument("file", help="Markdown file to read")
    group = ap.add_argument_group("selectors")
    group.add_argument("--id", help="Heading id from md-toc output, e.g. installation or installation-2")
    group.add_argument("--path", help="Outline path from md-toc output, e.g. 1.2.1")
    group.add_argument("--title", help="Exact heading title, case-insensitive")
    group.add_argument("--occurrence", type=int, default=1, help="Occurrence to use with --title (default: 1)")
    group.add_argument("--line", type=int, help="Read the deepest heading section containing this line")
    ap.add_argument("--body-only", action="store_true", help="Omit the selected heading line(s)")
    ap.add_argument("--no-subsections", action="store_true", help="Stop before the first child subsection")
    ap.add_argument("--metadata", action="store_true", help="Print section metadata before content")
    args = ap.parse_args(argv)

    text = read_text(args.file)
    headings = parse_headings(text)
    if not headings:
        raise SystemExit("No Markdown headings found in this file.")
    h = select_heading(headings, args)
    content, start_line, end_line = section_text(text, h, args.body_only, args.no_subsections, headings)
    if args.metadata:
        print(f"File: {Path(args.file).expanduser()}")
        print(f"Section: {h.path} H{h.level} {h.title}")
        print(f"ID: {h.id}")
        print(f"Lines: {start_line}-{end_line}")
        print(f"Chars returned: {len(content)}")
        print("---")
    sys.stdout.write(content)
    if content and not content.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    prog = Path(sys.argv[0]).name
    if "toc" in prog:
        raise SystemExit(cmd_toc())
    if "read" in prog:
        raise SystemExit(cmd_read())

    ap = argparse.ArgumentParser(description="Markdown navigation utility")
    sub = ap.add_subparsers(dest="command", required=True)
    toc = sub.add_parser("toc", help="Print a table of contents with character counts")
    toc.add_argument("file")
    toc.add_argument("--max-depth", type=int, default=6, choices=range(1, 7), metavar="1-6")
    toc.add_argument("--json", action="store_true")
    read = sub.add_parser("read", help="Read one heading section")
    read.add_argument("file")
    read.add_argument("--id")
    read.add_argument("--path")
    read.add_argument("--title")
    read.add_argument("--occurrence", type=int, default=1)
    read.add_argument("--line", type=int)
    read.add_argument("--body-only", action="store_true")
    read.add_argument("--no-subsections", action="store_true")
    read.add_argument("--metadata", action="store_true")
    ns = ap.parse_args()
    if ns.command == "toc":
        raise SystemExit(cmd_toc([ns.file] + (["--json"] if ns.json else []) + (["--max-depth", str(ns.max_depth)] if ns.max_depth != 6 else [])))
    raise SystemExit(cmd_read([ns.file] + (["--id", ns.id] if ns.id else []) + (["--path", ns.path] if ns.path else []) + (["--title", ns.title] if ns.title else []) + (["--occurrence", str(ns.occurrence)] if ns.occurrence != 1 else []) + (["--line", str(ns.line)] if ns.line else []) + (["--body-only"] if ns.body_only else []) + (["--no-subsections"] if ns.no_subsections else []) + (["--metadata"] if ns.metadata else [])))
