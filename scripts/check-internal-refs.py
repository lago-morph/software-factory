#!/usr/bin/env python3
"""Check internal markdown document references.

Implements the rules from the "Internal document references" section
of [`AGENTS.md`](../AGENTS.md):

  - Internal `.md`/code references should be markdown links with
    descriptive text and a relative path.
  - No bare-text "the X report" / "the X doc" references.
  - No stale paths in markdown links (target must exist relative to
    source file).
  - No backtick-wrapped paths that aren't already inside a markdown
    link (those are references in the typographic sense but not
    clickable; the convention says to wrap them as
    ``[`label`](relative/path)``).

Defaults are tuned to skip directories that hold intentionally raw
material (manual ingestion drops, fetched HTML, retrospective
snapshots, the canonical-source library, harness run outputs).

Usage examples:

  python scripts/check-internal-refs.py
  python scripts/check-internal-refs.py --include architectures
  python scripts/check-internal-refs.py --include research \\
      --no-bare-text --no-broken-links

Exit codes:
  0 — no issues found
  1 — issues found
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

INLINE_LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
BACKTICK_PATH = re.compile(
    r"`([^`\n]+\.(?:md|py|sh|json|yaml|yml|toml|txt|html|mhtml|pdf|ipynb))`"
)
BARE_TEXT_REPORT = re.compile(
    r"\bthe \w+(?:[ -]\w+){0,4} "
    r"(report|file|doc|document|skill|spec|architecture|synthesis|catalog)\b",
    re.IGNORECASE,
)

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


def is_excluded(rel_path: str, excludes: list[str]) -> bool:
    return any(rel_path.startswith(e) for e in excludes)


def strip_fenced_code(text: str) -> str:
    """Blank out fenced code blocks while preserving line numbering."""
    out: list[str] = []
    in_fence = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def strip_inline_code(text: str) -> str:
    """Blank out inline code spans (`...`, ``...``, ```...```)
    while preserving overall length so character offsets stay valid for
    line-number reporting.

    Implements the CommonMark rule that a backtick string of length N
    closes only at the next backtick string of the same length N.
    """
    out = list(text)
    i = 0
    n = len(text)
    while i < n:
        if text[i] != "`":
            i += 1
            continue
        # measure opening run
        j = i
        while j < n and text[j] == "`":
            j += 1
        run_len = j - i
        # find matching close of the same length, on the same logical
        # line — code spans don't cross blank lines and the spec doesn't
        # let backticks cross paragraphs cleanly. We restrict to a
        # single logical paragraph (no double-newline).
        k = j
        match_end = -1
        while k < n:
            if text[k] == "\n" and k + 1 < n and text[k + 1] == "\n":
                break
            if text[k] == "`":
                m = k
                while m < n and text[m] == "`":
                    m += 1
                if m - k == run_len:
                    match_end = m
                    break
                k = m
                continue
            k += 1
        if match_end < 0:
            # no close — emit the opening run as-is and move past it
            i = j
            continue
        # blank out the interior between j and match_end - run_len
        interior_start = j
        interior_end = match_end - run_len
        for p in range(interior_start, interior_end):
            if text[p] != "\n":
                out[p] = " "
        i = match_end
    return "".join(out)


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def check_file(path: Path, root: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    text = strip_fenced_code(raw)
    # Inline-code-stripped view: link detection runs against this so
    # illustrative links inside `` `` `` code spans aren't flagged.
    no_inline_code = strip_inline_code(text)
    # Mask existing markdown links so backtick-path scanning doesn't
    # flag paths that are already linked. (Uses the original `text` so
    # the backtick-path regex can still see paths *inside* code spans —
    # those are the references we want to convert.)
    masked = INLINE_LINK.sub(
        lambda m: "[" + m.group(1) + "](_)", text
    )

    findings: list[str] = []

    # 1) Backtick paths not already inside a link.
    for m in BACKTICK_PATH.finditer(masked):
        line_no = line_of(masked, m.start())
        path_str = m.group(1)
        # Skip obvious non-references: bare filenames with no slash
        # (those tend to be tool/command names, e.g. `install.py`),
        # and "../" segments inside YAML/jq examples are ambiguous.
        if "/" not in path_str:
            continue
        # Skip wildcard / template paths — they aren't real files.
        if any(c in path_str for c in "*<>{}"):
            continue
        findings.append(
            f"{path.relative_to(root)}:{line_no}: "
            f"BACKTICK_PATH `{path_str}` (suggest: "
            f"[`{Path(path_str).stem}`]({path_str}))"
        )

    # 2) Broken / stale markdown link targets. Run against the
    # inline-code-stripped view so illustrative example links inside
    # `` `` `` code spans are skipped.
    for m in INLINE_LINK.finditer(no_inline_code):
        target = m.group(2)
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if "{{" in target or "}}" in target:  # template placeholders
            continue
        if "*" in target or "<" in target or ">" in target:
            continue  # wildcard / placeholder paths
        target_path = target.split("#", 1)[0]
        if not target_path:
            continue
        candidate = (path.parent / target_path).resolve()
        if not candidate.exists():
            line_no = line_of(no_inline_code, m.start())
            findings.append(
                f"{path.relative_to(root)}:{line_no}: "
                f"BROKEN_LINK → {target}"
            )

    # 3) Bare-text "the X report" / "the X doc" patterns.
    for m in BARE_TEXT_REPORT.finditer(text):
        line_no = line_of(text, m.start())
        findings.append(
            f"{path.relative_to(root)}:{line_no}: "
            f"BARE_TEXT '{m.group()}'"
        )

    return findings


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument(
        "--include", action="append", default=[],
        help="restrict scan to paths starting with this prefix (relative to root)",
    )
    ap.add_argument(
        "--exclude", action="append", default=[],
        help="add an extra exclude prefix on top of the defaults",
    )
    ap.add_argument(
        "--no-bare-text", action="store_true",
        help="skip the bare-text heuristic (false positives on prose are common)",
    )
    ap.add_argument(
        "--no-broken-links", action="store_true",
        help="skip the broken-link check",
    )
    ap.add_argument(
        "--only", choices=["BACKTICK_PATH", "BROKEN_LINK", "BARE_TEXT"],
        help="only emit one finding category",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    excludes = DEFAULT_EXCLUDES + [
        e if e.endswith("/") else e + "/" for e in args.exclude
    ]

    md_files = sorted(root.rglob("*.md"))
    issues = 0
    scanned = 0
    for f in md_files:
        rel = f.relative_to(root).as_posix()
        if is_excluded(rel, excludes):
            continue
        if args.include and not any(
            rel.startswith(p.rstrip("/") + "/") or rel == p
            for p in args.include
        ):
            continue
        scanned += 1
        findings = check_file(f, root)
        if args.no_bare_text:
            findings = [x for x in findings if "BARE_TEXT" not in x]
        if args.no_broken_links:
            findings = [x for x in findings if "BROKEN_LINK" not in x]
        if args.only:
            findings = [x for x in findings if args.only in x]
        for line in findings:
            print(line)
            issues += 1

    if issues:
        print(
            f"\n{issues} issue(s) found across {scanned} scanned file(s) "
            f"(of {len(md_files)} total)",
            file=sys.stderr,
        )
        return 1
    print(f"\n✓ no issues found across {scanned} scanned file(s) "
          f"(of {len(md_files)} total)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
