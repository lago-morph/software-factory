"""Cross-check URLs in the catalog against URLs cited in research reports.

Two-way diff:
    - URLs in reports but NOT in any catalog record → flag (catalog is missing)
    - URLs in catalog where references_from lists a report that doesn't actually
      cite the URL → flag (stale references_from)

Reports scanned: all `.md` files under `report_paths` (recursive).
URL match is on canonical form (canonicalize before comparison).

Exit:
    0 = both sides match
    1 = mismatches found
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import data_path, report_paths, repo_root, ConfigError  # noqa: E402
from url_canonicalize import canonicalize_url  # noqa: E402

# Liberal URL extraction from reports
URL_RE = re.compile(r"https?://[^\s<>\"'\)\]\}`,]+")


def _strip_trailing_punctuation(url: str) -> str:
    """Remove punctuation like .,;:!?] that markdown might tail on a URL."""
    while url and url[-1] in ".,;:!?)]}>\"'`":
        url = url[:-1]
    return url


def _collect_report_urls() -> dict[str, list[str]]:
    """Return {canonical_url: [report_path, ...]} from all reports."""
    out: dict[str, set[str]] = {}
    for report_dir in report_paths():
        if not report_dir.exists():
            continue
        for md_file in sorted(report_dir.rglob("*.md")):
            text = md_file.read_text(encoding="utf-8", errors="replace")
            for m in URL_RE.finditer(text):
                raw = _strip_trailing_punctuation(m.group(0))
                try:
                    canon = canonicalize_url(raw)
                except ValueError:
                    continue
                rel = str(md_file.relative_to(repo_root()))
                out.setdefault(canon, set()).add(rel)
    return {url: sorted(paths) for url, paths in out.items()}


def _collect_catalog_urls(data: dict) -> dict[str, str]:
    """Return {canonical_url: record_id}."""
    out: dict[str, str] = {}
    for record_id, record in data.items():
        if not isinstance(record, dict):
            continue
        url = record.get("canonical_url")
        if url:
            try:
                canon = canonicalize_url(url)
                out[canon] = record_id
            except ValueError:
                pass
        # Also accept original_url
        orig = record.get("original_url")
        if orig:
            try:
                canon = canonicalize_url(orig)
                out.setdefault(canon, record_id)
            except ValueError:
                pass
    return out


def main() -> int:
    try:
        data_p = data_path()
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

    report_urls = _collect_report_urls()
    catalog_urls = _collect_catalog_urls(data)

    errors = []
    warnings = []

    # URLs cited in reports but not in catalog
    missing_in_catalog = sorted(set(report_urls) - set(catalog_urls))
    for url in missing_in_catalog:
        # Show the first report path that cites it
        report_list = report_urls[url][:3]
        errors.append(
            f"URL cited in {report_list[0]} (and {len(report_urls[url])-1} other report(s)) "
            f"but no record in catalog: {url}"
        )

    # Stale references_from on catalog records
    for record_id, record in data.items():
        if not isinstance(record, dict):
            continue
        refs = record.get("references_from", [])
        if not isinstance(refs, list):
            continue
        url = record.get("canonical_url")
        if not url:
            continue
        try:
            canon = canonicalize_url(url)
        except ValueError:
            continue
        actual_reports = set(report_urls.get(canon, []))
        listed_reports = set(refs)
        # references_from says X but X doesn't actually cite this URL
        stale = listed_reports - actual_reports
        for s in sorted(stale):
            warnings.append(
                f"{record_id}: references_from lists {s!r} but URL not found in that file"
            )
        # report cites but references_from doesn't include
        missing = actual_reports - listed_reports
        for m in sorted(missing):
            warnings.append(
                f"{record_id}: {m} cites this URL but it's not in references_from"
            )

    # Report
    for e in errors:
        print(f"✗ {e}", file=sys.stderr)
    for w in warnings:
        print(f"⚠ {w}", file=sys.stderr)

    n_report = len(report_urls)
    n_cat = len(catalog_urls)
    if errors:
        print(
            f"\n{n_report} URL(s) in reports, {n_cat} URL(s) in catalog; "
            f"{len(errors)} error(s), {len(warnings)} warning(s)",
            file=sys.stderr,
        )
        return 1
    if warnings:
        print(f"\n✓ {n_report} report URLs covered by {n_cat} catalog records ({len(warnings)} warning(s))")
        return 0  # warnings only — still a pass
    print(f"✓ {n_report} report URLs covered by {n_cat} catalog records")
    return 0


if __name__ == "__main__":
    sys.exit(main())
