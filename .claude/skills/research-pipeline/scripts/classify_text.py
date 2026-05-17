"""Classify a text/markdown file by its content shape.

Used by the drain pipeline to decide how to ingest a .txt or .md file dropped
into research/manual/ or research/fetched/.

Returns one of:
    - "url_list"               — every non-blank, non-comment line is a URL.
                                  Process as a list of "want this" URLs.
    - "source_with_first_url"  — first non-blank line is a URL, rest is content.
                                  That URL is the source's canonical_url.
    - "source_with_header_url" — file has "URL: <url>" header line near the top.
                                  That URL is the source's canonical_url.
    - "mixed_error"            — mostly URLs but with non-URL lines mixed in.
                                  Ambiguous; surface to user.
    - "unrecognized"           — no URLs at all, no recognizable structure.
                                  Surface to user.
    - "empty"                  — file is empty or only blank/comment lines.

CLI:
    python classify_text.py <path>
        Prints the classification + extracted URL (if any) as JSON.

API:
    classify(text: str) -> dict
        Returns {"kind": <category>, "urls": [...], "extracted_url": <url or None>}
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Liberal URL regex — accepts http/https URLs anywhere in a line.
URL_RE = re.compile(
    r"https?://[^\s<>\"'\)\]\}]+",
    re.IGNORECASE,
)

# A line is "URL-only" if after stripping it's a single URL.
URL_LINE_RE = re.compile(
    r"^\s*https?://[^\s<>\"'\)\]\}]+\s*$",
    re.IGNORECASE,
)

# URL header conventions used by various manual uploads.
HEADER_RE = re.compile(
    r"^\s*(?:URL|Source|Link)\s*[:=]\s*(https?://\S+)",
    re.IGNORECASE | re.MULTILINE,
)


def _is_comment(line: str) -> bool:
    s = line.strip()
    return s.startswith("#") or s.startswith("//")


def _is_blank(line: str) -> bool:
    return not line.strip()


def classify(text: str) -> dict:
    """Classify the text content. Returns a dict with kind + URL info."""
    if not text or not text.strip():
        return {"kind": "empty", "urls": [], "extracted_url": None}

    lines = text.splitlines()
    significant = [l for l in lines if not _is_blank(l) and not _is_comment(l)]

    if not significant:
        return {"kind": "empty", "urls": [], "extracted_url": None}

    # Classify each significant line
    url_only_lines = [l for l in significant if URL_LINE_RE.match(l)]
    n_sig = len(significant)
    n_url_only = len(url_only_lines)

    # All-URL case: every significant line is a URL → url_list
    if n_url_only == n_sig and n_sig >= 1:
        urls = [URL_LINE_RE.match(l).group(0).strip() for l in url_only_lines]
        return {"kind": "url_list", "urls": urls, "extracted_url": None}

    # Header URL: scan first ~30 lines for URL: <url> pattern
    head = "\n".join(lines[:30])
    header_match = HEADER_RE.search(head)
    if header_match:
        return {
            "kind": "source_with_header_url",
            "urls": [header_match.group(1)],
            "extracted_url": header_match.group(1),
        }

    # First non-blank line is a URL? → source_with_first_url
    first_match = URL_LINE_RE.match(significant[0])
    if first_match:
        return {
            "kind": "source_with_first_url",
            "urls": [first_match.group(0).strip()],
            "extracted_url": first_match.group(0).strip(),
        }

    # Some URL content but also non-URL → mixed_error
    if n_url_only > 0:
        urls = [URL_LINE_RE.match(l).group(0).strip() for l in url_only_lines]
        return {"kind": "mixed_error", "urls": urls, "extracted_url": None}

    # Embedded URLs (inside lines) but no URL-only lines
    embedded = []
    for line in significant[:50]:
        for m in URL_RE.finditer(line):
            embedded.append(m.group(0))
    if embedded:
        return {
            "kind": "unrecognized",
            "urls": embedded,
            "extracted_url": None,
        }

    return {"kind": "unrecognized", "urls": [], "extracted_url": None}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: classify_text.py <path>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8", errors="replace")
    result = classify(text)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
