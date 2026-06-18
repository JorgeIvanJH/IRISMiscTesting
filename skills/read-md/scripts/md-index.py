#!/usr/bin/env python3
"""Index a directory tree of Markdown files for efficient agent navigation."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

# Import shared parser from this script directory.
from mdnav import parse_headings, read_text


def iter_markdown_files(root: Path):
    patterns = ("*.md", "*.markdown")
    seen: set[Path] = set()
    for pattern in patterns:
        for p in root.rglob(pattern):
            if p.is_file() and p not in seen:
                seen.add(p)
                yield p


def build_index(root: Path, max_headings: int = 3):
    rows = []
    for p in sorted(iter_markdown_files(root)):
        try:
            text = read_text(p)
        except Exception as e:  # keep indexing robust
            rows.append({
                "file": str(p.relative_to(root)),
                "error": str(e),
            })
            continue
        headings = parse_headings(text)
        h1 = next((h.title for h in headings if h.level == 1), p.stem)
        preview = [
            {"level": h.level, "title": h.title, "id": h.id, "chars": h.chars}
            for h in headings[:max_headings]
        ]
        rows.append({
            "file": str(p.relative_to(root)),
            "chars": len(text),
            "lines": len(text.splitlines()),
            "headings": len(headings),
            "h1": h1,
            "preview_headings": preview,
        })
    return rows


def print_tree(root: Path, rows: list[dict], include_stats: bool = True):
    print(f"Root: {root}")
    print(f"Markdown files: {len(rows)}")
    total_chars = sum(r.get("chars", 0) for r in rows)
    total_lines = sum(r.get("lines", 0) for r in rows)
    print(f"Total: {total_chars} chars, {total_lines} lines")
    print("")

    # Group by directory for readable tree-like output.
    by_dir: dict[str, list[dict]] = {}
    for r in rows:
        rel = Path(r["file"])
        by_dir.setdefault(str(rel.parent) if str(rel.parent) != "." else "", []).append(r)

    for directory in sorted(by_dir):
        depth = 0 if not directory else len(Path(directory).parts)
        if directory:
            print(f"{'  ' * (depth - 1)}{Path(directory).name}/")
        for r in sorted(by_dir[directory], key=lambda x: x["file"]):
            name = Path(r["file"]).name
            indent = "  " * depth
            if "error" in r:
                print(f"{indent}- {name} [ERROR: {r['error']}]")
                continue
            if include_stats:
                print(
                    f"{indent}- {name} | {r['chars']} chars, {r['lines']} lines, "
                    f"{r['headings']} headings | H1: {r['h1']}"
                )
            else:
                print(f"{indent}- {name}")


def print_table(root: Path, rows: list[dict]):
    print(f"Root: {root}")
    print(f"Markdown files: {len(rows)}")
    print("")
    print("chars | lines | headings | file | H1")
    print("-" * 100)
    for r in sorted(rows, key=lambda x: x.get("chars", 0), reverse=True):
        if "error" in r:
            print(f"ERROR | {r['file']} | {r['error']}")
        else:
            print(f"{r['chars']:>5} | {r['lines']:>5} | {r['headings']:>8} | {r['file']} | {r['h1']}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Index a directory tree of Markdown files.")
    ap.add_argument("root", help="Directory containing Markdown files")
    ap.add_argument("--format", choices=["tree", "table", "json"], default="tree", help="Output format")
    ap.add_argument("--plain", action="store_true", help="With --format tree, omit stats and print file tree only")
    ap.add_argument("--max-headings", type=int, default=3, help="Number of heading previews to include in JSON")
    args = ap.parse_args(argv)

    root = Path(args.root).expanduser()
    if not root.exists():
        raise SystemExit(f"Root does not exist: {root}")
    if not root.is_dir():
        raise SystemExit(f"Root is not a directory: {root}")

    rows = build_index(root, args.max_headings)
    if args.format == "json":
        print(json.dumps({"root": str(root), "files": rows}, indent=2))
    elif args.format == "table":
        print_table(root, rows)
    else:
        print_tree(root, rows, include_stats=not args.plain)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
