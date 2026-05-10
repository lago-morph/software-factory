#!/usr/bin/env python3
"""Fetch URLs listed in a GitHub issue body and save them at the repo root.

Reads:
- ISSUE_BODY (env)        — markdown; one URL per line, with or without list markers
- ISSUE_NUMBER (env)      — used only for the result file's heading
- ISSUE_TITLE (env)       — used only for the result file's heading
- GITHUB_WORKSPACE (env)  — repo root; defaults to "."

Writes:
- <repo-root>/<sanitized-filename>.html  for each successfully fetched URL
- <repo-root>/.github/fetch-result.md    — markdown summary the workflow posts as a comment

Behaviour:
- One URL per line. Lines without a URL are skipped silently.
- Filenames match the existing repo convention:
    https://example.com/                  -> example.com.html
    https://example.com/foo/bar           -> example.com__foo__bar.html
    https://example.com/foo?id=42         -> example.com__foo__q__id_eq_42.html
    https://medium.com/@user/about        -> medium.com___at_user__about.html
- A realistic browser User-Agent is sent. Cloudflare-protected sites may still
  return challenge pages; we save what we got and flag it in the result.
- Fetch errors are recorded but do not fail the job.
"""

from __future__ import annotations

import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(os.environ.get("GITHUB_WORKSPACE", "."))
RESULT_PATH = REPO_ROOT / ".github" / "fetch-result.md"

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
TIMEOUT_S = 30
MAX_BYTES = 25 * 1024 * 1024  # 25 MB cap per file

URL_RE = re.compile(r"https?://[^\s<>\"'`]+")
SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._-]")


def sanitize_filename(url: str) -> str:
    """Convert a URL into a repo-root filename matching the existing convention."""
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    query = parsed.query

    segments = [s for s in path.split("/") if s]
    # `@user` -> `_at_user` (matches existing medium.com files)
    segments = [s.replace("@", "_at_") for s in segments]

    parts = [host] + segments
    name = "__".join(parts) if parts else host or "page"

    if query:
        # ?id=42&foo=bar  ->  __q__id_eq_42_amp_foo_eq_bar
        kv_pairs = []
        for k, v in urllib.parse.parse_qsl(query, keep_blank_values=True):
            kv_pairs.append(f"{k}_eq_{v}")
        if kv_pairs:
            name += "__q__" + "_amp_".join(kv_pairs)

    name = SAFE_NAME_RE.sub("_", name)
    # Collapse runs of underscores to keep filenames readable.
    name = re.sub(r"_{4,}", "___", name)
    # Cap length so we don't trip filesystem limits.
    if len(name) > 200:
        name = name[:200]
    return name + ".html"


def extract_urls(body: str) -> list[str]:
    """Find URLs in the issue body. Allow markdown list markers and inline use."""
    if not body:
        return []
    seen: dict[str, None] = {}
    for line in body.splitlines():
        for match in URL_RE.finditer(line):
            url = match.group(0).rstrip(".,;:)>]\"'`")
            seen.setdefault(url, None)
    return list(seen.keys())


def fetch(url: str) -> tuple[bytes, str | None]:
    """Fetch a URL. Returns (content_bytes, error_string_or_None)."""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "identity",  # avoid gzip; we want raw bytes
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            data = resp.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                return b"", f"response exceeds {MAX_BYTES // (1024 * 1024)} MB cap"
            return data, None
    except urllib.error.HTTPError as e:
        return b"", f"HTTP {e.code} {e.reason}"
    except urllib.error.URLError as e:
        return b"", f"URL error: {e.reason}"
    except TimeoutError:
        return b"", f"timeout after {TIMEOUT_S}s"
    except Exception as e:  # noqa: BLE001 — we want to report any fetch failure
        return b"", f"{type(e).__name__}: {e}"


CLOUDFLARE_MARKERS = (
    "just a moment",
    "challenge-platform",
    "cf_chl_opt",
    "checking your browser",
    "enable cookies",
)


def classify(content: bytes) -> tuple[str, str]:
    """Return (status_emoji, note) for a successful fetch."""
    if not content:
        return "❌", "empty response"
    text = content[:8192].decode("utf-8", errors="ignore").lower()
    if any(marker in text for marker in CLOUDFLARE_MARKERS):
        return "⚠️", "Cloudflare challenge page — likely not useful content"
    if len(content) < 2048:
        return "⚠️", f"small response ({len(content)} bytes) — may be a block page"
    return "✅", ""


def main() -> int:
    body = os.environ.get("ISSUE_BODY", "")
    issue_number = os.environ.get("ISSUE_NUMBER", "?")
    issue_title = os.environ.get("ISSUE_TITLE", "")

    urls = extract_urls(body)

    lines: list[str] = [f"_Issue #{issue_number}: {issue_title}_", ""]

    if not urls:
        lines.append(
            "No URLs found in the issue body. List one URL per line, "
            "each starting with `http://` or `https://`."
        )
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return 0

    lines.append(f"Found {len(urls)} URL(s). Results:")
    lines.append("")

    for url in urls:
        filename = sanitize_filename(url)
        content, error = fetch(url)

        if error:
            lines.append(f"- `{url}` → ❌ fetch failed: {error}")
            continue

        out_path = REPO_ROOT / filename
        out_path.write_bytes(content)
        status, note = classify(content)
        size_kb = max(1, len(content) // 1024)
        suffix = f" — {note}" if note else ""
        lines.append(f"- `{url}` → `{filename}` {status} ({size_kb} KB){suffix}")

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
