"""Render reference-only/sources.md from reference-only/sources.json.

Output structure (top to bottom):

  1. Header (auto-generated banner)
  2. Manual-fetch table — records with want files that the fetch action couldn't
     auto-grab (HTTP 404s, JS-rendered shells, paywalls). Includes save-as-MHTML
     instructions and the drop location.
  3. By category — one section per category tag, with each matching record
     rendered in full. A record with N tags appears in N sections (deliberate).
  4. By status — fallback section for records with no category tag, plus the
     traditional status buckets (complete / partial / wanted / superseded).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

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


def render_record(rid: str, rec: dict) -> str:
    """Full per-record block."""
    title = rec.get("title", "(untitled)")
    if rec.get("pointer_to"):
        return f"### {rid} ~~{title}~~ → see [{rec['pointer_to']}](#{rec['pointer_to']})"

    lines = [f'### {rid} — {title} <a id="{rid}"></a>', ""]
    if rec.get("canonical_url"):
        lines.append(f"<{rec['canonical_url']}>")
    else:
        lines.append("*(no canonical URL)*")
    lines.append("")
    if rec.get("short_summary"):
        lines.append(f"*{rec['short_summary']}*")
        lines.append("")

    files = rec.get("files") or []
    if files:
        chips = " · ".join(file_chip(f) for f in files if isinstance(f, dict))
        lines.append(f"- **Files:** {chips}")
    else:
        lines.append("- **Files:** *(none registered)*")

    if rec.get("tags"):
        lines.append("- **Tags:** " + " · ".join(f"`{t}`" for t in rec["tags"]))
    if rec.get("references_from"):
        refs = rec["references_from"]
        ref_str = " · ".join(f"`{r}`" for r in refs[:5])
        if len(refs) > 5:
            ref_str += f" *(+{len(refs)-5} more)*"
        lines.append(f"- **Cited in:** {ref_str} *({len(refs)})*")
    if rec.get("has_useful_diagrams") and rec["has_useful_diagrams"] != "unknown":
        lines.append(f"- **Diagrams:** {rec['has_useful_diagrams']}")
    return "\n".join(lines)


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
        "| Record | Title | URL | Reason want | Drop as |",
        "|---|---|---|---|---|",
    ]
    for rid, title, url, reason, drop in rows:
        # Truncate fields
        t = title.replace("|", "\\|")[:60]
        u = url
        if u != "(no URL)":
            u = f"[{u[:60]}]({url})"
        r = reason.replace("|", "\\|")[:80]
        lines.append(f"| `{rid}` | {t} | {u} | {r} | {drop} |")
    lines.append("")
    return "\n".join(lines)


def by_category_section(data: dict) -> str:
    """Render by-category sections. A record appears in every category it's tagged with."""
    lines = ["## By category", ""]
    no_category = []
    for cat, blurb in CATEGORY_ORDER:
        members = [
            (rid, rec) for rid, rec in data.items()
            if isinstance(rec, dict) and cat in (rec.get("tags") or [])
        ]
        members.sort(key=lambda x: (x[1].get("title") or "").lower())
        lines.append(f"### {cat} *({len(members)} record{'s' if len(members) != 1 else ''})*")
        lines.append("")
        lines.append(f"*{blurb}*")
        lines.append("")
        if not members:
            lines.append("*(no records yet)*")
            lines.append("")
            continue
        for rid, rec in members:
            lines.append(render_record(rid, rec))
            lines.append("")
        lines.append("")

    # Records with no recognized category tag
    for rid, rec in data.items():
        if not isinstance(rec, dict):
            continue
        tags = rec.get("tags") or []
        if not any(t in CATEGORIES for t in tags):
            no_category.append((rid, rec))
    no_category.sort(key=lambda x: (x[1].get("title") or "").lower())
    if no_category:
        lines.append(f"### (no category) *({len(no_category)} record{'s' if len(no_category) != 1 else ''})*")
        lines.append("")
        lines.append("*Records that don't yet have any of the 15 canonical category tags.*")
        lines.append("")
        for rid, rec in no_category:
            lines.append(render_record(rid, rec))
            lines.append("")

    return "\n".join(lines)


def by_status_section(data: dict) -> str:
    """Traditional status grouping as a navigation aid."""
    sections = {
        "complete":     ("§ 1 — Complete",          "Every registered file is present and complete."),
        "partial":      ("§ 2 — Partial",           "Has some content, but also files that are wanted, partial, or had fetch errors."),
        "wanted_url":   ("§ 3a — Wanted (URL known)", "URL is known but no content acquired yet."),
        "wanted_title": ("§ 3b — Wanted (title only)", "Title + search hints only; no URL yet."),
        "superseded":   ("§ 4 — Superseded",        "Records replaced by another; `pointer_to` is set."),
    }
    by_state = {k: [] for k in sections}
    for rid, rec in data.items():
        if not isinstance(rec, dict):
            continue
        by_state[status(rec)].append((rid, rec))
    for k in by_state:
        by_state[k].sort(key=lambda x: (x[1].get("title") or "").lower())

    lines = ["## By status (cross-cutting view)", ""]
    for state, (title, blurb) in sections.items():
        members = by_state[state]
        lines.append(f"### {title} *({len(members)} record{'s' if len(members) != 1 else ''})*")
        lines.append("")
        lines.append(f"*{blurb}*")
        lines.append("")
        if not members:
            lines.append("*(none)*")
            lines.append("")
            continue
        # Just a compact link list — no full render (avoid 3rd copy of every record)
        for rid, rec in members:
            t = rec.get("title", "(untitled)")
            if rec.get("pointer_to"):
                lines.append(f"- `{rid}` ~~{t}~~ → [{rec['pointer_to']}](#{rec['pointer_to']})")
            else:
                lines.append(f"- [`{rid}` — {t}](#{rid})")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    try:
        data = load()
    except ConfigError as e:
        print(f"✗ Config error: {e}", file=sys.stderr)
        return 1

    import datetime as _dt
    out = [
        "# Source catalog — browse view",
        "",
        "Auto-generated from `reference-only/sources.json` by `scripts/render-sources-md.py`.",
        "Do not edit by hand — your changes will be overwritten on next push to `main`.",
        "",
        f"**Records:** {len(data)} · **Generated:** {_dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        "",
    ]

    # 1. Manual fetch banner (if anything wants fetching)
    mf = manual_fetch_section(data)
    if mf:
        out.append(mf)
        out.append("")

    # 2. By category (the primary navigation)
    out.append(by_category_section(data))

    # 3. By status (cross-cutting summary)
    out.append(by_status_section(data))

    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
