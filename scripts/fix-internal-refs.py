#!/usr/bin/env python3
"""Transform backtick-wrapped paths into markdown links.

Companion to `scripts/check-internal-refs.py`. For every match of
`` `<path>.<ext>` `` in a markdown file:

  - Skip if the match is inside a fenced code block.
  - Skip if the match is inside an inline code span that itself contains
    a markdown link (e.g. `` `[`X`](Y)` `` — already a link).
  - Skip if the path contains wildcards or template placeholders
    (`*`, `<>`, `{}`).
  - Interpret the path as repo-root-relative.
  - Confirm the target file exists.
  - Compute the path relative to the source file's parent directory.
  - Rewrite as ``[`<label>`](<rel-path>)`` where `<label>` is the path's
    basename, minus extension for known extensions (`.md`, `.py`).

Pass `--apply` to write the changes. By default, prints a diff to stdout.

Usage:
    python scripts/fix-internal-refs.py path/to/file.md             # dry-run
    python scripts/fix-internal-refs.py path/to/file.md --apply     # write
    python scripts/fix-internal-refs.py --include research          # batch
"""

from __future__ import annotations

import argparse
import difflib
import os
import re
import sys
from pathlib import Path

BACKTICK_PATH = re.compile(
    r"(?<!`)`([A-Za-z0-9_./-][A-Za-z0-9_./<>-]*\."
    r"(?:md|py|sh|json|yaml|yml|toml|txt|html|mhtml|pdf|ipynb))`(?!`)"
)

EXT_STRIPPED_FOR_LABEL = {".md", ".py", ".sh", ".json", ".yaml", ".yml"}


def find_fenced_ranges(text: str) -> list[tuple[int, int]]:
    """Find (start, end) char offsets of fenced code blocks."""
    ranges: list[tuple[int, int]] = []
    in_fence = False
    pos = 0
    start = -1
    for line in text.split("\n"):
        line_end = pos + len(line)
        if line.lstrip().startswith("```"):
            if not in_fence:
                start = pos
                in_fence = True
            else:
                ranges.append((start, line_end + 1))
                in_fence = False
        pos = line_end + 1
    return ranges


def in_any_range(offset: int, ranges: list[tuple[int, int]]) -> bool:
    return any(s <= offset < e for s, e in ranges)


def already_in_link(text: str, match_start: int, match_end: int) -> bool:
    """Is the backtick-path match inside an existing markdown link?

    Heuristic: look for `](` immediately before the match (within the
    same line and after the last `[`). If so, the backtick path is the
    link target portion already, and we should leave it alone.
    """
    line_start = text.rfind("\n", 0, match_start) + 1
    prefix = text[line_start:match_start]
    # Quick reject: no `[` on the line before us means we're not in
    # the text part of a link.
    if "[" not in prefix:
        return False
    # If the most-recent `[` is followed by `](` somewhere before our
    # match, we're inside link text after the `]` — which means the
    # backtick path is in the URL slot. Skip.
    last_open = prefix.rfind("[")
    after_open = prefix[last_open:]
    if "](" in after_open:
        return True
    # If our match is preceded by `[` with no `]` before it, we're in
    # the link text — the backtick-path is being used as a label, not a
    # URL target. We should still consider it (the rewrite turns the
    # raw filename into a labelled link), but the outer link wraps it,
    # so skip to avoid producing `[[`label`](...)](outer)`.
    if "]" not in after_open:
        return True
    return False


def label_for(path_str: str) -> str:
    """Compute the link label for a path."""
    name = Path(path_str).name
    if any(name.endswith(ext) for ext in EXT_STRIPPED_FOR_LABEL):
        return Path(name).stem
    return name


def compute_relative(src_file: Path, target_repo_relative: str, repo_root: Path) -> str | None:
    """Compute the file-relative path from src_file's parent to the
    target file. Returns None if the target does not exist.

    target_repo_relative may itself be a relative path. We resolve it
    against the source file's parent first; if that resolves to an
    existing file, treat the input as already file-relative. Otherwise
    treat it as repo-root-relative.
    """
    # Strip anchor for existence checking
    anchor = ""
    raw_target = target_repo_relative
    if "#" in target_repo_relative:
        raw_target, anchor = target_repo_relative.split("#", 1)
        anchor = "#" + anchor

    # Try as file-relative first
    candidate_file_rel = (src_file.parent / raw_target).resolve()
    if candidate_file_rel.exists():
        target_abs = candidate_file_rel
    else:
        # Treat as repo-root-relative
        candidate_repo_rel = (repo_root / raw_target).resolve()
        if not candidate_repo_rel.exists():
            return None
        target_abs = candidate_repo_rel

    src_dir = src_file.parent.resolve()
    try:
        rel = os.path.relpath(target_abs, src_dir)
    except ValueError:
        return None
    # On non-posix this might use backslashes; normalize.
    return rel.replace(os.sep, "/") + anchor


def transform(text: str, src_file: Path, repo_root: Path) -> tuple[str, int]:
    """Return (new_text, n_changes)."""
    fenced_ranges = find_fenced_ranges(text)

    pieces: list[str] = []
    last_end = 0
    changes = 0
    for m in BACKTICK_PATH.finditer(text):
        path_str = m.group(1)
        # Skip if inside fenced code
        if in_any_range(m.start(), fenced_ranges):
            continue
        # Skip wildcard/template paths
        if any(c in path_str for c in "*<>{}"):
            continue
        # Bare filename with no slash — likely a tool name, not a path
        if "/" not in path_str:
            continue
        # Skip if already inside a markdown link
        if already_in_link(text, m.start(), m.end()):
            continue
        # Compute file-relative path; skip if target doesn't exist
        rel = compute_relative(src_file, path_str, repo_root)
        if rel is None:
            continue
        label = label_for(path_str)
        # Emit everything up to the match, then the rewrite
        pieces.append(text[last_end:m.start()])
        pieces.append(f"[`{label}`]({rel})")
        last_end = m.end()
        changes += 1
    pieces.append(text[last_end:])
    return "".join(pieces), changes


def process_file(
    path: Path, repo_root: Path, apply: bool, show_diff: bool
) -> int:
    raw = path.read_text(encoding="utf-8")
    new, n = transform(raw, path, repo_root)
    if n == 0:
        return 0
    if show_diff:
        diff = difflib.unified_diff(
            raw.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=str(path.relative_to(repo_root)),
            tofile=str(path.relative_to(repo_root)) + " (transformed)",
            n=1,
        )
        sys.stdout.write("".join(diff))
    if apply:
        path.write_text(new, encoding="utf-8")
        print(f"✓ {path.relative_to(repo_root)}: {n} change(s)", file=sys.stderr)
    return n


DEFAULT_EXCLUDES = [
    "node_modules/",
    ".git/",
    "research/manual/",
    "research/fetched/",
    "reference-only/",
    "retrospective/",
    "harness/runs/",
    ".claude/skills/issue-management/templates/",
    ".claude/skills/self-retrospective/resources/",
    ".claude/skills/parallel-subagent-fanout/spec/",
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="*", help="files or directories to process")
    ap.add_argument("--include", action="append", default=[],
                    help="include prefix (used when paths is empty)")
    ap.add_argument("--apply", action="store_true",
                    help="write changes in place (otherwise print diff)")
    ap.add_argument("--no-diff", action="store_true",
                    help="suppress diff output")
    ap.add_argument("--root", default=".", help="repo root")
    args = ap.parse_args()

    repo_root = Path(args.root).resolve()

    files: list[Path] = []
    if args.paths:
        for p in args.paths:
            pp = Path(p).resolve()
            if pp.is_dir():
                files.extend(sorted(pp.rglob("*.md")))
            elif pp.is_file() and pp.suffix == ".md":
                files.append(pp)
    else:
        for f in sorted(repo_root.rglob("*.md")):
            rel = f.relative_to(repo_root).as_posix()
            if any(rel.startswith(e) for e in DEFAULT_EXCLUDES):
                continue
            if args.include and not any(
                rel.startswith(p.rstrip("/") + "/") or rel == p
                for p in args.include
            ):
                continue
            files.append(f)

    total = 0
    touched = 0
    for f in files:
        n = process_file(f, repo_root, args.apply, not args.no_diff)
        total += n
        if n > 0:
            touched += 1

    print(f"\n{total} change(s) across {touched} file(s) (of {len(files)} scanned)",
          file=sys.stderr)
    return 0 if not total else (0 if args.apply else 1)


if __name__ == "__main__":
    sys.exit(main())
