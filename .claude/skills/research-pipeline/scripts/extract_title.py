"""Best-effort title extraction from ingested file content.

Used by drain.py (to populate the title field on new records so the audit's
title-not-placeholder check passes) and by sanity-check-record.py / audit-records.py
(to compare extracted vs. recorded titles).

Each extractor reads at most ~50KB to keep the cost bounded.

Public API:
    extract_title(path: Path) -> str | None
        Returns a cleaned title string or None if nothing usable was found.
"""

from __future__ import annotations

import re
from email.header import decode_header, make_header
from pathlib import Path


# Detects a Subject-line value that's still wrapped in an RFC 2047
# encoded-word (`=?charset?Q-or-B?...?=`). MHTML files saved by Chrome use
# this form for non-ASCII characters in the page title.
_RFC2047_RE = re.compile(r"=\?[^?]+\?[BbQq]\?[^?]+\?=")

TITLE_HTML_RE = re.compile(r"<title[^>]*>([^<]+)</title>", re.IGNORECASE | re.DOTALL)
TITLE_H1_RE = re.compile(r"<h1[^>]*>([^<]+)</h1>", re.IGNORECASE | re.DOTALL)
TITLE_MHTML_RE = re.compile(r"^Subject:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
TITLE_MD_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
TITLE_TXT_RE = re.compile(r"^\s*(?:TITLE|Title)\s*[:=]\s*(.+)$", re.MULTILINE)


def _decode_rfc2047(s: str) -> str:
    """Decode any RFC 2047 encoded-words in `s` to their unicode form. If
    `s` doesn't contain any, returns it unchanged. Best-effort: decode
    errors leave the original substring in place."""
    if not _RFC2047_RE.search(s):
        return s
    try:
        return str(make_header(decode_header(s)))
    except (UnicodeDecodeError, LookupError, ValueError):
        return s


def _clean(s: str) -> str:
    s = _decode_rfc2047(s)
    s = s.strip()
    s = s.replace("&amp;", "&").replace("&#x27;", "'").replace("&quot;", '"')
    s = s.replace("&lt;", "<").replace("&gt;", ">")
    return re.sub(r"\s+", " ", s)


def extract_title(path: Path) -> str | None:
    """Best-effort title extraction. Returns None if nothing recognizable found."""
    if not path.exists():
        return None
    suffix = path.suffix.lower()
    try:
        if suffix == ".mhtml":
            head = path.read_bytes()[:20480].decode("utf-8", errors="replace")
            m = TITLE_MHTML_RE.search(head)
            return _clean(m.group(1)) if m else None
        if suffix in {".html", ".htm"}:
            text = path.read_text(encoding="utf-8", errors="replace")[:50000]
            m = TITLE_HTML_RE.search(text)
            if m:
                return _clean(m.group(1))
            m = TITLE_H1_RE.search(text)
            return _clean(m.group(1)) if m else None
        if suffix == ".md":
            text = path.read_text(encoding="utf-8", errors="replace")
            m = TITLE_MD_RE.search(text)
            return _clean(m.group(1)) if m else None
        if suffix == ".txt":
            text = path.read_text(encoding="utf-8", errors="replace")[:5000]
            m = TITLE_TXT_RE.search(text)
            return _clean(m.group(1)) if m else None
    except OSError:
        return None
    return None
