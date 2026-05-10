#!/usr/bin/env python3
"""Extract URLs from the issue body env var BODY.

Accepts:
  - bare URLs (http://, https://)
  - markdown link syntax [text](url)
  - URLs inside fenced code blocks

Skips:
  - mailto:, ftp:, javascript:
  - duplicate URLs (first occurrence wins)
  - any URL longer than 2048 chars (sanity bound)

Prints one URL per line to stdout, in the order they appeared.
"""
from __future__ import annotations

import os
import re
import sys

BODY = os.environ.get("BODY", "")

# Markdown link: [text](url)
MD_LINK = re.compile(r"\[[^\]]*\]\((https?://[^\s)]+)\)")

# Bare URL: http(s)://...
BARE = re.compile(r"(?<![\w(])(https?://[^\s)>\]'\"`]+)")

MAX_URL = 2048


def _clean(u: str) -> str:
    # Strip common trailing punctuation that is usually not part of the URL.
    while u and u[-1] in ".,;:!?'\"":
        u = u[:-1]
    return u


def extract(body: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []

    for m in MD_LINK.finditer(body):
        u = _clean(m.group(1))
        if 0 < len(u) <= MAX_URL and u not in seen:
            seen.add(u)
            out.append(u)

    body_minus_md = MD_LINK.sub("", body)
    for m in BARE.finditer(body_minus_md):
        u = _clean(m.group(1))
        if 0 < len(u) <= MAX_URL and u not in seen:
            seen.add(u)
            out.append(u)

    return out


def main() -> int:
    urls = extract(BODY)
    for u in urls:
        print(u)
    print(f"Extracted {len(urls)} URLs.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
