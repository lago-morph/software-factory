"""YouTube URL detection helpers.

Used by drain.py (surface candidate transcripts from ingested documents),
reconcile-source-dir.py (recognize a delivered transcript .txt by its
first-line URL), and audit-records.py (verify transcript files keep their
first-line URL invariant).

Public API:
    is_youtube_url(url: str) -> bool
        Quick host-pattern match.

    canonicalize_youtube_url(url: str) -> str
        Normalize watch/youtu.be/embed/shorts forms to the canonical
        ``https://www.youtube.com/watch?v=<ID>`` form. Strips tracking
        params and timestamps. Raises ValueError on unrecognized inputs.

    extract_youtube_urls_from_file(path: Path) -> list[YoutubeMention]
        Scan a file for YouTube URLs. Returns each canonicalized URL once,
        with a short snippet of surrounding text for human/agent judgement.

    first_line_youtube_url(path: Path) -> str | None
        Return the canonical YouTube URL if the file's first line is one,
        else None.

A YoutubeMention is a small dataclass-like object with:
    url:      canonical YouTube URL
    snippet:  short string of surrounding text (best-effort, plain text)
    raw_url:  the URL as it appeared in the source file
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


YOUTUBE_HOST_RE = re.compile(
    r"^https?://(?:www\.|m\.)?(?:youtube\.com|youtu\.be|youtube-nocookie\.com)(?:/|$)",
    re.IGNORECASE,
)

# URL extractor for arbitrary text. We look for full http(s)://… URLs and
# also for youtu.be shortened forms.
_URL_IN_TEXT = re.compile(
    r"""https?://
        (?:www\.|m\.)?
        (?:youtube\.com|youtu\.be|youtube-nocookie\.com)
        /[^\s"'<>)]*
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Video ID is 11 chars of [A-Za-z0-9_-] in modern YouTube. We accept that
# pattern strictly so we don't confuse channel/playlist IDs with video IDs.
_VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


@dataclass(frozen=True)
class YoutubeMention:
    url: str           # canonical https://www.youtube.com/watch?v=<ID>
    raw_url: str       # the URL as found in the source
    snippet: str       # short surrounding-text snippet (plain text)


def is_youtube_url(url: str) -> bool:
    """True if the URL appears to be a YouTube link."""
    if not isinstance(url, str):
        return False
    return bool(YOUTUBE_HOST_RE.match(url.strip()))


def _video_id_from_parts(parts) -> str | None:
    """Best-effort video ID extraction from a urlsplit result.

    Handles:
        youtube.com/watch?v=<ID>
        youtu.be/<ID>
        youtube.com/embed/<ID>
        youtube.com/shorts/<ID>
        youtube.com/v/<ID>
        youtube-nocookie.com/embed/<ID>
    Returns None if no 11-char ID is found.
    """
    host = (parts.hostname or "").lower()
    path = parts.path or ""

    if host.endswith("youtu.be"):
        candidate = path.strip("/").split("/", 1)[0]
        return candidate if _VIDEO_ID_RE.match(candidate) else None

    # youtube.com or youtube-nocookie.com
    q = parse_qs(parts.query)
    if "v" in q and q["v"]:
        v = q["v"][0]
        if _VIDEO_ID_RE.match(v):
            return v

    # path-based IDs (embed/, shorts/, v/, live/)
    for prefix in ("/embed/", "/shorts/", "/v/", "/live/"):
        if path.startswith(prefix):
            candidate = path[len(prefix):].split("/", 1)[0].split("?", 1)[0]
            if _VIDEO_ID_RE.match(candidate):
                return candidate

    return None


def canonicalize_youtube_url(url: str) -> str:
    """Return a canonical ``https://www.youtube.com/watch?v=<ID>`` URL.

    Raises ValueError if the URL isn't a recognizable YouTube video link
    (e.g. channel pages, playlists without a video, mistyped IDs).
    """
    if not url or not is_youtube_url(url):
        raise ValueError(f"not a YouTube URL: {url!r}")
    parts = urlsplit(url.strip())
    vid = _video_id_from_parts(parts)
    if not vid:
        raise ValueError(f"YouTube URL has no recognizable video ID: {url!r}")
    return f"https://www.youtube.com/watch?v={vid}"


def first_line_youtube_url(path: Path) -> str | None:
    """If the file's first non-blank line is a YouTube URL, return its
    canonical form; else None."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                if is_youtube_url(stripped):
                    try:
                        return canonicalize_youtube_url(stripped)
                    except ValueError:
                        return None
                # First non-blank line is not a URL — that's a definitive no.
                return None
    except OSError:
        return None
    return None


def _strip_html(text: str) -> str:
    """Crude HTML/MHTML tag stripper for snippet extraction."""
    # Drop <script> and <style> blocks
    text = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>",  " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _snippet_around(text: str, start: int, end: int, window: int = 180) -> str:
    """Pull ``window`` chars of plain-text context around [start:end]."""
    left = max(0, start - window)
    right = min(len(text), end + window)
    s = text[left:right]
    s = _strip_html(s)
    return s


def extract_youtube_urls_from_file(path: Path) -> list[YoutubeMention]:
    """Scan a file for YouTube URL mentions and return unique canonical
    URLs with surrounding-text snippets.

    Supported formats: .html, .htm, .mhtml, .md, .txt, .ipynb. Other
    formats return an empty list. Reads at most ~2MB to keep it cheap.
    """
    if not path.exists():
        return []
    suffix = path.suffix.lower()
    if suffix not in {".html", ".htm", ".mhtml", ".md", ".txt", ".ipynb"}:
        return []
    try:
        raw = path.read_bytes()[: 2 * 1024 * 1024]
    except OSError:
        return []
    text = raw.decode("utf-8", errors="replace")

    seen: dict[str, YoutubeMention] = {}
    for m in _URL_IN_TEXT.finditer(text):
        raw_url = m.group(0).rstrip(".,);]\"'>")
        try:
            canon = canonicalize_youtube_url(raw_url)
        except ValueError:
            continue
        if canon in seen:
            continue
        snippet = _snippet_around(text, m.start(), m.end())
        seen[canon] = YoutubeMention(url=canon, raw_url=raw_url, snippet=snippet)
    return list(seen.values())


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: youtube_urls.py <file>", file=sys.stderr)
        return 2
    p = Path(argv[1])
    mentions = extract_youtube_urls_from_file(p)
    if not mentions:
        print("(no YouTube URLs found)")
        return 1
    for m in mentions:
        print(f"{m.url}")
        print(f"  raw: {m.raw_url}")
        print(f"  ctx: {m.snippet[:240]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
