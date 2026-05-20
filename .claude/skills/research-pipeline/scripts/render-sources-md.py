"""Render reference-only/sources.md from reference-only/sources.json.

Output structure (top to bottom):

  1. Header (auto-generated banner)
  2. Table of contents — in-page anchors to every section.
  3. Manual-fetch table — records with want files that the fetch action couldn't
     auto-grab (HTTP 404s, JS-rendered shells, paywalls). Includes save-as-MHTML
     instructions and the drop location.
  4. By category — one collapsible <details> block per category tag, each
     containing a table of matching records. A record with N tags appears in
     N sections (deliberate).
  5. By status — fallback cross-cutting view; one collapsible block per status
     bucket (complete / partial / wanted_url / wanted_title / superseded).

The file is generated at reference-only/sources.md, so all relative links are
expressed relative to that location:
  - Per-record directory: `<id>/`
  - Primary file:         `<id>/<filename>`
  - Cited-in report:      `../research/<...>.md`
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import quote as _urlquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import data_path, ConfigError  # noqa: E402

# The 15 canonical categories, in the order they should appear in the MD
CATEGORY_ORDER = [
    ("dark-factory",
     "Dark-Factory canon — Shapiro / El Kaim / StrongDM foundational essays on AI-built software as paradigm."),
    ("intent-driven-architecture",
     "Intent-driven / continuous enterprise architecture, RISE-style automation, product-line variability."),
    ("spec-authorship",
     "Requirements engineering, BMAD, scenario testing, INCOSE primer, spec-as-prompt practice."),
    ("willison-canon",
     "Simon Willison's collected writings + interviews."),
    ("compound-engineering",
     "Compound-engineering workflows, personal harnesses, practitioner accounts (Klaassen / Reed / How I AI)."),
    ("anthropic-substrate",
     "Claude Code substrate, Anthropic engineering posts, Cherny interviews."),
    ("openai-substrate",
     "Codex substrate, OpenAI cookbook, running-codex-safely docs."),
    ("other-vendor-substrate",
     "GitHub Copilot, Replit Agent, Devin, Factory.ai, Tabnine, OpenHands, etc."),
    ("skills-composition",
     "Skills as a composition primitive — agentskills.io, Anthropic Agent Skills, MCP."),
    ("evals-and-benchmarks",
     "SWE-bench, SWE-agent, AlphaCode, CodeGen, evals primers (Husain, Yan, Shankar)."),
    ("academic-foundations",
     "Academic methodology papers: underspecification, multi-task benchmarks, CHI/ICSE studies."),
    ("security-primitives",
     "Threat models, prompt-injection defenses, capability/data-flow security (CaMeL, AgentDojo)."),
    ("governance-and-legal",
     "Stanford CodeX, Caremark / RSI board exposure, NHTSA levels, AUTOSAR, ISO 42010."),
    ("ai-engineering-culture",
     "Team-level dynamics, organisational culture, the social/operational side."),
    ("meta-synthesis",
     "Derived syntheses over the corpus (counterfactual deep-research, QC re-reads)."),
]
CATEGORIES = [c for c, _ in CATEGORY_ORDER]

# Formats considered image-only — skipped when picking the primary file
IMAGE_FORMATS = {
    "image/png", "image/jpeg", "image/svg+xml", "image/gif", "image/webp",
}


def load() -> dict:
    p = data_path()
    return json.loads(p.read_text(encoding="utf-8"))


def status(rec: dict) -> str:
    """Compute one of: superseded / complete / partial / wanted_url / wanted_title."""
    if (rec.get("pointer_to") or None):
        return "superseded"
    files = rec.get("files") or []
    n_have = sum(1 for f in files if isinstance(f, dict) and f.get("ingestion_status") == "have")
    n_want = sum(1 for f in files if isinstance(f, dict) and f.get("ingestion_status") == "want")
    n_problem = sum(1 for f in files if isinstance(f, dict) and f.get("completeness") in ("partial", "error"))
    if n_have == 0:
        if rec.get("canonical_url"):
            return "wanted_url"
        return "wanted_title"
    if n_want or n_problem:
        return "partial"
    return "complete"


def file_chip(f: dict) -> str:
    fmt = f.get("format", "?")
    s = f.get("ingestion_status")
    if s == "have":
        return f"{fmt} ✓"
    if s == "want":
        return f"{fmt} (want)"
    if s == "skip-not-necessary":
        return f"{fmt} (skip)"
    return f"{fmt} (?)"


def primary_file(rec: dict) -> dict | None:
    """Pick the "primary" file for a record.

    Mirrors the heuristic used by the drain pipeline (stage-5): first file
    whose format is not an image and whose ingestion_status is "have". Falls
    back to first non-image file regardless of status, then first file overall.
    """
    files = [f for f in (rec.get("files") or []) if isinstance(f, dict)]
    if not files:
        return None

    def _non_image(f: dict) -> bool:
        return f.get("format") not in IMAGE_FORMATS

    have_non_image = [f for f in files if _non_image(f) and f.get("ingestion_status") == "have"]
    if have_non_image:
        return have_non_image[0]
    non_image = [f for f in files if _non_image(f)]
    if non_image:
        return non_image[0]
    return files[0]


def _cell(s: str) -> str:
    """Escape a string for safe inclusion in a markdown table cell."""
    if s is None:
        return ""
    # Pipes break table rows; <br> keeps multi-line cells working.
    return s.replace("|", "\\|").replace("\n", " ")


def _encode_path(p: str) -> str:
    """URL-encode a relative path while keeping slashes literal."""
    return _urlquote(p, safe="/")


def _dir_link(rid: str) -> str:
    """Link to the record's directory, relative to reference-only/sources.md."""
    return f"[`{rid}`]({_encode_path(rid)}/)"


def _local_source_link(rid: str, rec: dict) -> str:
    """Link with text 'Local Source' to the primary file, or '—' if none on disk."""
    f = primary_file(rec)
    if not f or f.get("ingestion_status") != "have":
        return "—"
    fname = f.get("filename")
    if not fname:
        return "—"
    # `location` overrides the default reference-only/<id>/<filename> path
    location = f.get("location")
    if location:
        # location is repo-relative; sources.md lives in reference-only/ so go up one
        target = f"../{location}"
    else:
        target = f"{rid}/{fname}"
    return f"[Local Source]({_encode_path(target)})"


def _source_url_link(rec: dict) -> str:
    url = rec.get("canonical_url")
    if not url:
        return "—"
    return f"[Source URL]({url})"


def _cited_in_links(rec: dict, max_show: int = 5) -> str:
    refs = rec.get("references_from") or []
    if not refs:
        return "—"
    # Reports live at research/... (repo-relative); sources.md is in reference-only/
    parts = [f"[`{r}`](../{_encode_path(r)})" for r in refs[:max_show]]
    out = " · ".join(parts)
    if len(refs) > max_show:
        out += f" *(+{len(refs) - max_show} more)*"
    out += f" *({len(refs)})*"
    return out


def _files_chips(rec: dict) -> str:
    files = [f for f in (rec.get("files") or []) if isinstance(f, dict)]
    if not files:
        return "*(none registered)*"
    return " · ".join(file_chip(f) for f in files)


def render_record_row(rid: str, rec: dict) -> str:
    """One <tr>-equivalent row in the by-category table."""
    anchor = f'<a id="{rid}"></a>'
    if rec.get("pointer_to"):
        target = rec["pointer_to"]
        title = _cell(rec.get("title", "(untitled)"))
        title_cell = f"~~{title}~~ → [`{target}`](#{target})"
        return (
            f"| {anchor}{_dir_link(rid)} "
            f"| {title_cell} "
            f"| — "
            f"| — "
            f"| — "
            f"| — |"
        )

    title = _cell(rec.get("title", "(untitled)"))
    summary = rec.get("short_summary")
    title_cell = f"**{title}**"
    if summary:
        title_cell += f"<br><em>{_cell(summary)}</em>"

    return (
        f"| {anchor}{_dir_link(rid)} "
        f"| {title_cell} "
        f"| {_source_url_link(rec)} "
        f"| {_local_source_link(rid, rec)} "
        f"| {_cell(_files_chips(rec))} "
        f"| {_cited_in_links(rec)} |"
    )


def _table_header() -> list[str]:
    return [
        "| ID | Title / Summary | Source URL | Local Source | Files | Cited in |",
        "|---|---|---|---|---|---|",
    ]


def manual_fetch_section(data: dict) -> str:
    """Records with want files — surface them for the user to manually fetch."""
    rows = []
    for rid in sorted(data.keys()):
        rec = data[rid]
        if not isinstance(rec, dict):
            continue
        files = rec.get("files") or []
        wants = [f for f in files if isinstance(f, dict) and f.get("ingestion_status") == "want"]
        if not wants:
            continue
        url = rec.get("canonical_url") or "(no URL)"
        title = rec.get("title", "(untitled)")
        # Reason: pull from file comment if any
        reasons = [w.get("comment", "") for w in wants if isinstance(w, dict) and w.get("comment")]
        reason = "; ".join(r for r in reasons if r) or "Not yet fetched"
        # MHTML save instruction: drop into research/manual/ then run drain
        drop = f"`research/manual/{rid}.mhtml`"
        rows.append((rid, title, url, reason, drop))

    if not rows:
        return ""

    lines = [
        '<a id="manual-fetch-needed"></a>',
        "## 🔴 Manual fetch needed",
        "",
        f"**{len(rows)} record(s)** have `ingestion_status=want` file entries — the fetch action couldn't get them automatically (Cloudflare challenge, JS-rendered SPA, paywall, or 404 with no successor).",
        "",
        "### How to fetch manually",
        "",
        "1. Open the URL in your browser (signed in if needed for paywalled content).",
        "2. **File → Save Page As → Webpage, Complete** (saves as MHTML — preserves embedded images + CSS). Chrome/Edge call this *\"Save as MHTML\"*; Firefox calls it *\"Webpage, single file\"* via an extension.",
        "3. Save the file with the suggested name from the **Drop as** column below into `research/manual/`.",
        "4. After all manual fetches are dropped, run:",
        "   ```bash",
        "   python .claude/skills/research-pipeline/scripts/reconcile-source-dir.py --all",
        "   ```",
        "   This will register each file into its catalog record (matching by sha256 + filename) and flip the status to `have`.",
        "",
        "### Records to fetch",
        "",
        "| Record | Title | Source URL | Reason want | Drop as |",
        "|---|---|---|---|---|",
    ]
    for rid, title, url, reason, drop in rows:
        t = _cell(title)[:80]
        if url == "(no URL)":
            u = "—"
        else:
            u = f"[Source URL]({url})"
        r = _cell(reason)[:80]
        lines.append(f"| `{rid}` | {t} | {u} | {r} | {drop} |")
    lines.append("")
    return "\n".join(lines)


def _cat_slug(cat: str) -> str:
    return f"cat-{cat}"


def _category_block(cat: str, blurb: str, members: list[tuple[str, dict]], slug: str | None = None) -> str:
    n = len(members)
    n_word = "record" if n == 1 else "records"
    if slug is None:
        slug = _cat_slug(cat)
    lines = [
        f'<a id="{slug}"></a>',
        "",
        "<details>",
        f"<summary><b>{cat}</b> — {n} {n_word} — <em>{blurb}</em></summary>",
        "",
    ]
    if not members:
        lines.append("*(no records yet)*")
        lines.append("")
        lines.append("</details>")
        return "\n".join(lines)
    lines.extend(_table_header())
    for rid, rec in members:
        lines.append(render_record_row(rid, rec))
    lines.append("")
    lines.append("</details>")
    return "\n".join(lines)


def by_category_section(data: dict) -> tuple[str, list[tuple[str, str, int]]]:
    """Render by-category sections plus return TOC entries (slug, label, count)."""
    lines = ['<a id="by-category"></a>', "## By category", ""]
    toc_entries: list[tuple[str, str, int]] = []

    for cat, blurb in CATEGORY_ORDER:
        members = [
            (rid, rec) for rid, rec in data.items()
            if isinstance(rec, dict) and cat in (rec.get("tags") or [])
        ]
        members.sort(key=lambda x: (x[1].get("title") or "").lower())
        toc_entries.append((_cat_slug(cat), cat, len(members)))
        lines.append(_category_block(cat, blurb, members))
        lines.append("")

    # Records with no recognized category tag
    no_category: list[tuple[str, dict]] = []
    for rid, rec in data.items():
        if not isinstance(rec, dict):
            continue
        tags = rec.get("tags") or []
        if not any(t in CATEGORIES for t in tags):
            no_category.append((rid, rec))
    no_category.sort(key=lambda x: (x[1].get("title") or "").lower())
    if no_category:
        toc_entries.append(("cat-none", "(no category)", len(no_category)))
        lines.append(_category_block(
            "(no category)",
            "Records that don't yet have any of the 15 canonical category tags.",
            no_category,
            slug="cat-none",
        ))
        lines.append("")

    return "\n".join(lines), toc_entries


def _status_slug(key: str) -> str:
    return f"status-{key.replace('_', '-')}"


def by_status_section(data: dict) -> tuple[str, list[tuple[str, str, int]]]:
    """Traditional status grouping as a navigation aid."""
    sections = [
        ("complete",     "§ 1 — Complete",             "Every registered file is present and complete."),
        ("partial",      "§ 2 — Partial",              "Has some content, but also files that are wanted, partial, or had fetch errors."),
        ("wanted_url",   "§ 3a — Wanted (URL known)",  "URL is known but no content acquired yet."),
        ("wanted_title", "§ 3b — Wanted (title only)", "Title + search hints only; no URL yet."),
        ("superseded",   "§ 4 — Superseded",           "Records replaced by another; `pointer_to` is set."),
    ]
    by_state: dict[str, list[tuple[str, dict]]] = {k: [] for k, *_ in sections}
    for rid, rec in data.items():
        if not isinstance(rec, dict):
            continue
        by_state[status(rec)].append((rid, rec))
    for k in by_state:
        by_state[k].sort(key=lambda x: (x[1].get("title") or "").lower())

    lines = ['<a id="by-status"></a>', "## By status (cross-cutting view)", ""]
    toc_entries: list[tuple[str, str, int]] = []
    for key, title, blurb in sections:
        members = by_state[key]
        n = len(members)
        n_word = "record" if n == 1 else "records"
        slug = _status_slug(key)
        toc_entries.append((slug, title, n))
        lines.append(f'<a id="{slug}"></a>')
        lines.append(f"### {title} *({n} {n_word})*")
        lines.append("")
        lines.append(f"*{blurb}*")
        lines.append("")
        if not members:
            lines.append("*(none)*")
            lines.append("")
            continue
        for rid, rec in members:
            t = rec.get("title", "(untitled)")
            if rec.get("pointer_to"):
                lines.append(f"- `{rid}` ~~{t}~~ → [`{rec['pointer_to']}`](#{rec['pointer_to']})")
            else:
                lines.append(f"- [`{rid}` — {t}](#{rid})")
        lines.append("")
    return "\n".join(lines), toc_entries


def render_toc(
    has_manual_fetch: bool,
    cat_entries: list[tuple[str, str, int]],
    status_entries: list[tuple[str, str, int]],
) -> str:
    lines = ["## Table of contents", ""]
    if has_manual_fetch:
        lines.append("- [🔴 Manual fetch needed](#manual-fetch-needed)")
    lines.append("- [By category](#by-category)")
    for slug, label, n in cat_entries:
        lines.append(f"  - [{label}](#{slug}) *({n})*")
    lines.append("- [By status (cross-cutting view)](#by-status)")
    for slug, label, n in status_entries:
        lines.append(f"  - [{label}](#{slug}) *({n})*")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    try:
        data = load()
    except ConfigError as e:
        print(f"✗ Config error: {e}", file=sys.stderr)
        return 1

    import datetime as _dt

    # Build sections first so we know the TOC contents.
    mf = manual_fetch_section(data)
    cat_md, cat_toc = by_category_section(data)
    status_md, status_toc = by_status_section(data)

    out = [
        "# Source catalog — browse view",
        "",
        "Auto-generated from `reference-only/sources.json` by `.claude/skills/research-pipeline/scripts/render-sources-md.py`.",
        "Do not edit by hand — your changes will be overwritten on next push to `main`.",
        "",
        f"**Records:** {len(data)} · **Generated:** {_dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        render_toc(bool(mf), cat_toc, status_toc),
    ]

    if mf:
        out.append(mf)
        out.append("")

    out.append(cat_md)
    out.append(status_md)

    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
