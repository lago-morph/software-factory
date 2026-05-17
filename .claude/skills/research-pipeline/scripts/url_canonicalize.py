"""Canonicalize URLs and compute source IDs.

Canonical form drives the record ID via:
    id = sha256(canonical_url)[:10]

Rules (applied in order):
    1. Strip leading/trailing whitespace.
    2. Lowercase the scheme and host (paths and query values are case-sensitive).
    3. Drop the fragment (everything after #).
    4. Drop default ports (:80 for http, :443 for https).
    5. Drop trailing slash from path (but only if path != "/", to preserve site roots).
    6. Drop common tracking query params (utm_*, fbclid, gclid, mc_eid, mc_cid,
       ref, ref_src, etc.). See TRACKING_PARAMS for the full list.
    7. Sort remaining query params alphabetically by name.
    8. Re-assemble.

Idempotent: canonicalize(canonicalize(u)) == canonicalize(u).

CLI:
    python url_canonicalize.py <url>
        Prints canonical_url and id, one per line.

API:
    canonicalize_url(url: str) -> str
    compute_id(url: str) -> str
    canonicalize_and_id(url: str) -> tuple[str, str]
"""

from __future__ import annotations

import hashlib
import sys
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

# Tracking params to strip. Lowercase comparison.
TRACKING_PARAMS = frozenset({
    # Google / generic analytics
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "utm_id", "utm_name",
    "gclid", "gclsrc", "dclid",
    # Facebook
    "fbclid", "_ga",
    # Mailchimp
    "mc_cid", "mc_eid",
    # Yandex
    "yclid",
    # Twitter / X
    "twclid",
    # Salesforce / Marketo
    "mkt_tok",
    # Hubspot
    "_hsenc", "_hsmi", "__hssc", "__hstc", "hsctatracking",
    # Substack
    "publication_id", "post_id", "isfreemail", "r", "triedredirect",
    # Generic referrer tags
    "ref", "ref_src", "ref_url", "referrer", "source",
})

DEFAULT_PORTS = {
    "http": 80,
    "https": 443,
    "ftp": 21,
    "ws": 80,
    "wss": 443,
}

ID_LENGTH = 10


def canonicalize_url(url: str) -> str:
    """Apply the canonicalization rules and return the canonical URL."""
    url = url.strip()
    if not url:
        raise ValueError("empty URL")

    parts = urlsplit(url)

    if not parts.scheme:
        raise ValueError(f"URL has no scheme: {url!r}")
    if not parts.netloc:
        raise ValueError(f"URL has no host: {url!r}")

    scheme = parts.scheme.lower()
    host = parts.hostname or ""
    host = host.lower()
    port = parts.port

    # Drop default port
    if port is not None and DEFAULT_PORTS.get(scheme) == port:
        port = None

    # Reconstruct netloc, preserving userinfo if present (rare)
    userinfo = ""
    if parts.username:
        userinfo = parts.username
        if parts.password:
            userinfo += ":" + parts.password
        userinfo += "@"
    netloc = userinfo + host
    if port is not None:
        netloc += f":{port}"

    # Normalize path: strip trailing slash unless root
    path = parts.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path.rstrip("/")
    # Empty path becomes /
    if path == "":
        path = "/"

    # Filter and sort query params
    query_pairs = parse_qsl(parts.query, keep_blank_values=True)
    filtered = [(k, v) for (k, v) in query_pairs if k.lower() not in TRACKING_PARAMS]
    filtered.sort(key=lambda kv: (kv[0], kv[1]))
    query = urlencode(filtered, doseq=False)

    # Drop fragment entirely
    fragment = ""

    return urlunsplit((scheme, netloc, path, query, fragment))


def compute_id(url: str) -> str:
    """Compute the 10-char source ID from a URL (canonicalizes first)."""
    canonical = canonicalize_url(url)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:ID_LENGTH]


def canonicalize_and_id(url: str) -> tuple[str, str]:
    """Return (canonical_url, id) in one call."""
    canonical = canonicalize_url(url)
    record_id = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:ID_LENGTH]
    return canonical, record_id


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: url_canonicalize.py <url>", file=sys.stderr)
        return 2
    url = argv[1]
    try:
        canonical, record_id = canonicalize_and_id(url)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"canonical_url: {canonical}")
    print(f"id:            {record_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
