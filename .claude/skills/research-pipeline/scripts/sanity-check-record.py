"""Semantic sanity check on a single record's files.

For each text-extractable file in a record:
    - Compare its extracted title (HTML <title>, MHTML Subject, MD #heading) to
      the record's title. Low similarity → warning ("file may not match record").
    - Compare its extracted URL to the record's canonical_url. Different host → warning.

For records with 2+ text files, compare their text content:
    - Low word-set overlap (<20%) → warning (possible misplacement, like the
      mhtml-with-wrong-content cases we saw earlier).

This script is warnings-only — it never blocks. The user makes judgement calls
on flagged records.

Usage:
    python sanity-check-record.py [record_id ...]
        If no record_id given, checks all records.

Exit:
    0 = always (warnings don't fail)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import data_path, library_path, repo_root, ConfigError  # noqa: E402
from extract_url import extract_url  # noqa: E402
from extract_title import extract_title  # noqa: E402
from url_canonicalize import canonicalize_url  # noqa: E402

ID_RE = re.compile(r"^[0-9a-f]{10}$")


def extract_text(path: Path, limit_chars: int = 50000) -> str:
    """Plain text from a file (best-effort, strips HTML/MHTML markup)."""
    if not path.exists():
        return ""
    suffix = path.suffix.lower()
    try:
        if suffix in {".html", ".htm", ".mhtml"}:
            raw = path.read_text(encoding="utf-8", errors="replace")[:limit_chars * 4]
            # Strip script and style
            raw = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.DOTALL | re.IGNORECASE)
            raw = re.sub(r"<style[^>]*>.*?</style>", " ", raw, flags=re.DOTALL | re.IGNORECASE)
            raw = re.sub(r"<[^>]+>", " ", raw)
            text = re.sub(r"\s+", " ", raw)
            return text[:limit_chars]
        if suffix in {".txt", ".md"}:
            return path.read_text(encoding="utf-8", errors="replace")[:limit_chars]
    except OSError:
        return ""
    return ""


def token_overlap(a: str, b: str) -> float:
    """Jaccard similarity of word sets, ignoring stopwords and short tokens."""
    sa = _tokenize(a)
    sb = _tokenize(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


STOPWORDS = frozenset(
    "the a an of to in for on at by with from as is are was were be been being "
    "and or but not no this that these those it its their our we you they i "
    "have has had do does did will would could should may might can".split()
)


def _tokenize(s: str) -> set[str]:
    return {
        w for w in re.findall(r"[A-Za-z]{3,}", s.lower())
        if w not in STOPWORDS
    }


def host_of(url: str) -> str | None:
    m = re.match(r"https?://([^/]+)", url)
    return m.group(1).lower() if m else None


def check_record(record_id: str, record: dict, lib: Path, root: Path) -> list[str]:
    """Return list of warning messages for this record."""
    warnings = []
    record_title = record.get("title", "")
    record_url = record.get("canonical_url")

    files = record.get("files", []) or []
    file_paths = []
    for f in files:
        if not isinstance(f, dict) or f.get("ingestion_status") != "have":
            continue
        location = f.get("location")
        filename = f.get("filename")
        if location:
            p = root / location
        elif filename:
            p = lib / record_id / filename
        else:
            continue
        if p.exists():
            file_paths.append((p, f))

    # Title + URL consistency per file
    for p, f in file_paths:
        # Skip images/binary
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".webp"}:
            continue
        ft = extract_title(p)
        if ft and record_title and record_title != "(unknown)":
            overlap = token_overlap(ft, record_title)
            if overlap < 0.15:
                warnings.append(
                    f"{record_id}: file '{p.name}' title '{ft[:80]}' "
                    f"has only {overlap:.0%} token overlap with record title '{record_title[:80]}'"
                )
        fu = extract_url(p)
        if fu and record_url:
            fh = host_of(fu)
            rh = host_of(record_url)
            if fh and rh and fh != rh:
                warnings.append(
                    f"{record_id}: file '{p.name}' has URL host {fh!r}, "
                    f"record canonical_url host is {rh!r}"
                )

    # Cross-file text similarity
    if len(file_paths) >= 2:
        text_paths = [
            (p, f) for (p, f) in file_paths
            if p.suffix.lower() in {".html", ".htm", ".mhtml", ".txt", ".md"}
        ]
        for i in range(len(text_paths)):
            for j in range(i + 1, len(text_paths)):
                ti = extract_text(text_paths[i][0])
                tj = extract_text(text_paths[j][0])
                if not ti or not tj:
                    continue
                overlap = token_overlap(ti, tj)
                if overlap < 0.20:
                    warnings.append(
                        f"{record_id}: files '{text_paths[i][0].name}' and "
                        f"'{text_paths[j][0].name}' have only {overlap:.0%} word overlap "
                        f"— possible misplacement"
                    )

    return warnings


def main(argv: list[str]) -> int:
    try:
        data_p = data_path()
        lib = library_path()
    except ConfigError as e:
        print(f"✗ Config error: {e}", file=sys.stderr)
        return 1

    if not data_p.exists():
        print(f"✗ {data_p} does not exist", file=sys.stderr)
        return 1
    try:
        data = json.loads(data_p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"✗ JSON parse error: {e}", file=sys.stderr)
        return 1

    root = repo_root()
    target_ids = argv[1:] if len(argv) > 1 else list(data.keys())
    all_warnings = []
    for rid in target_ids:
        record = data.get(rid)
        if not isinstance(record, dict):
            print(f"⚠ {rid}: not a record (skipped)", file=sys.stderr)
            continue
        all_warnings.extend(check_record(rid, record, lib, root))

    for w in all_warnings:
        print(f"⚠ {w}")

    if all_warnings:
        print(f"\n{len(all_warnings)} sanity warning(s) on {len(target_ids)} record(s)")
    else:
        print(f"✓ {len(target_ids)} record(s) checked, no sanity issues")
    return 0  # always exit 0 — warnings only


if __name__ == "__main__":
    sys.exit(main(sys.argv))
