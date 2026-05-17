"""Extract the canonical URL from a saved-page file.

Format-specific strategies (best-effort):
    .mhtml  : Snapshot-Content-Location: or Content-Location: MIME header
    .html   : <link rel="canonical">, <meta property="og:url">, <meta name="...">
    .pdf    : /URL or /Source in metadata (best-effort, no PDF lib required)
    .txt    : URL: / Source: / Link: header; first-line URL fallback
    .md     : YAML frontmatter `url:`, then first-line URL fallback
    .ipynb  : first markdown cell scanned for URL
    .json   : look for top-level "url" or "canonical_url" key
    image/* : not supported (always returns None)

Returns None if no URL can be extracted (e.g. raw binary, image).

CLI:
    python extract_url.py <path>
        Prints the extracted URL, or "(none)" if not found.

API:
    extract_url(path: Path) -> str | None
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico"}
VIDEO_EXTS = {".mp4", ".mov", ".webm", ".avi", ".mkv"}
AUDIO_EXTS = {".mp3", ".m4a", ".wav", ".ogg"}


def extract_url(path: Path) -> str | None:
    """Best-effort URL extraction. None if not recoverable from this format."""
    if not path.exists():
        return None
    suffix = path.suffix.lower()

    if suffix in IMAGE_EXTS or suffix in VIDEO_EXTS or suffix in AUDIO_EXTS:
        return None

    if suffix == ".mhtml":
        return _from_mhtml(path)
    if suffix in {".html", ".htm"}:
        return _from_html(path)
    if suffix == ".pdf":
        return _from_pdf(path)
    if suffix == ".txt":
        return _from_text(path)
    if suffix == ".md":
        return _from_markdown(path)
    if suffix == ".ipynb":
        return _from_ipynb(path)
    if suffix == ".json":
        return _from_json(path)
    return None


# -- MHTML --------------------------------------------------------------

def _from_mhtml(path: Path) -> str | None:
    """Read MIME headers; look for Snapshot-Content-Location or Content-Location."""
    try:
        # Read first ~10KB - headers are always near the top.
        with open(path, "rb") as f:
            head = f.read(20480).decode("utf-8", errors="replace")
    except OSError:
        return None
    # Snapshot-Content-Location: is the URL Chrome saved-as-MHTML uses.
    m = re.search(r"^Snapshot-Content-Location:\s*(\S+)", head, re.IGNORECASE | re.MULTILINE)
    if m:
        return m.group(1).strip()
    m = re.search(r"^Content-Location:\s*(\S+)", head, re.IGNORECASE | re.MULTILINE)
    if m:
        return m.group(1).strip()
    return None


# -- HTML ---------------------------------------------------------------

CANONICAL_LINK_RE = re.compile(
    r'<link[^>]*\brel\s*=\s*["\']?canonical["\']?[^>]*\bhref\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE,
)
CANONICAL_LINK_RE_REV = re.compile(
    r'<link[^>]*\bhref\s*=\s*["\']([^"\']+)["\'][^>]*\brel\s*=\s*["\']?canonical["\']?',
    re.IGNORECASE,
)
OG_URL_RE = re.compile(
    r'<meta[^>]*\bproperty\s*=\s*["\']og:url["\'][^>]*\bcontent\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE,
)
OG_URL_RE_REV = re.compile(
    r'<meta[^>]*\bcontent\s*=\s*["\']([^"\']+)["\'][^>]*\bproperty\s*=\s*["\']og:url["\']',
    re.IGNORECASE,
)
TWITTER_URL_RE = re.compile(
    r'<meta[^>]*\bname\s*=\s*["\']twitter:url["\'][^>]*\bcontent\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE,
)


def _from_html(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    # Only scan the <head> section if possible
    head_match = re.search(r"<head[^>]*>(.*?)</head>", text, re.DOTALL | re.IGNORECASE)
    scan = head_match.group(1) if head_match else text[:50000]

    for regex in (CANONICAL_LINK_RE, CANONICAL_LINK_RE_REV, OG_URL_RE, OG_URL_RE_REV, TWITTER_URL_RE):
        m = regex.search(scan)
        if m:
            return m.group(1).strip()
    return None


# -- PDF ----------------------------------------------------------------

def _from_pdf(path: Path) -> str | None:
    """Best-effort: look for /URL or /Source in PDF info dict via byte scan.

    Not a full PDF parser; just searches the first 64KB for common patterns.
    """
    try:
        with open(path, "rb") as f:
            head = f.read(65536)
    except OSError:
        return None
    text = head.decode("latin-1", errors="replace")
    # PDF info dict /URL (PdfWriter) or /Source (custom)
    m = re.search(r"/(?:URL|Source)\s*\(([^)]+)\)", text)
    if m:
        candidate = m.group(1).strip()
        if candidate.startswith("http"):
            return candidate
    # Embedded URI annotations
    m = re.search(r"/URI\s*\(([^)]+)\)", text)
    if m:
        candidate = m.group(1).strip()
        if candidate.startswith("http"):
            return candidate
    return None


# -- TXT ----------------------------------------------------------------

TXT_HEADER_RE = re.compile(
    r"^\s*(?:URL|Source|Link)\s*[:=]\s*(https?://\S+)",
    re.IGNORECASE | re.MULTILINE,
)
URL_LINE_RE = re.compile(
    r"^\s*(https?://\S+)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def _from_text(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    head = "\n".join(text.splitlines()[:30])
    m = TXT_HEADER_RE.search(head)
    if m:
        return m.group(1).strip()
    # First non-blank line is a URL?
    for line in text.splitlines()[:5]:
        if line.strip() and (mm := URL_LINE_RE.match(line)):
            return mm.group(1).strip()
    return None


# -- Markdown -----------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FM_URL_RE = re.compile(r'^\s*(?:url|source|canonical_url)\s*:\s*["\']?([^"\'\s]+)', re.IGNORECASE | re.MULTILINE)


def _from_markdown(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    fm = FRONTMATTER_RE.match(text)
    if fm:
        m = FM_URL_RE.search(fm.group(1))
        if m:
            return m.group(1).strip()
    # Fall back to txt strategies
    head = "\n".join(text.splitlines()[:30])
    m = TXT_HEADER_RE.search(head)
    if m:
        return m.group(1).strip()
    for line in text.splitlines()[:5]:
        if line.strip() and (mm := URL_LINE_RE.match(line)):
            return mm.group(1).strip()
    return None


# -- Notebook -----------------------------------------------------------

def _from_ipynb(path: Path) -> str | None:
    try:
        nb = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return None
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "markdown":
            src = "".join(cell.get("source", []))
            m = TXT_HEADER_RE.search(src) or URL_LINE_RE.search(src)
            if m:
                return m.group(1).strip()
            break  # only check first markdown cell
    return None


# -- JSON ---------------------------------------------------------------

def _from_json(path: Path) -> str | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return None
    if isinstance(data, dict):
        for key in ("canonical_url", "url", "source", "link"):
            v = data.get(key)
            if isinstance(v, str) and v.startswith("http"):
                return v.strip()
    return None


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: extract_url.py <path>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    url = extract_url(path)
    if url is None:
        print("(none)")
        return 1
    print(url)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
