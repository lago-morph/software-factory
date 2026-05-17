"""Auto-update research/PLAN.md after a successful drain.

Called by drain.py (and potentially other catalog-mutators) to keep PLAN.md
in step with the catalog. The function generates a Session bullet under §1
and, if the drain produced new records or attached files, a row in the §10
round-by-round lookup table. The Version line is bumped.

Public API:
    update_plan_after_drain(result, plan_path) -> dict
        Mutates plan_path on disk. Returns a small status dict
        {round_number, version_after, bullet_inserted, row_inserted}.
        Caller passes the drain.DrainResult and a Path to PLAN.md.

If PLAN.md has no `**Version:**` line, or no §10 table, the corresponding
edit is skipped with a warning. The drain itself never fails on a
PLAN-update problem.
"""

from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import Any

VERSION_LINE_RE = re.compile(
    r"^(\*\*Version:\*\*\s+v)(\d+)\.(\d+)(\s+\()(\d{4}-\d{2}-\d{2})(\)\s*)$",
    re.MULTILINE,
)
SECTION_10_RE = re.compile(
    r"(^## 10\..*?\n)(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL,
)
TABLE_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|", re.MULTILINE)
SESSION_BULLET_RE = re.compile(r"^- \*\*Session ", re.MULTILINE)
OPEN_ITEMS_LIVE_IN_RE = re.compile(r"^\*\*Open items live in:\*\*", re.MULTILINE)


def _max_round_in_section_10(s10_body: str) -> int:
    """Highest `| N |` row number inside §10 (excluding header dividers)."""
    nums = [
        int(m.group(1))
        for m in TABLE_ROW_RE.finditer(s10_body)
        if int(m.group(1)) < 100  # defensive: ignore column-width artefacts
    ]
    return max(nums) if nums else 0


def _today() -> str:
    return datetime.date.today().isoformat()


def _is_material(result: Any) -> bool:
    """Did the drain do something worth recording?"""
    return bool(
        getattr(result, "files_added_as_new_records", [])
        or getattr(result, "files_added_to_existing", [])
        or getattr(result, "reconciled_orphans", [])
        or getattr(result, "transcripts_delivered", [])
        or getattr(result, "wants_purged", [])
    )


def _format_session_bullet(result: Any, round_number: int) -> str:
    """The Session bullet that goes under §1. Mirrors the structure of
    historical bullets (date, one-line topic, prose body)."""
    date = _today()
    new_count = len(getattr(result, "files_added_as_new_records", []))
    attached_count = len(getattr(result, "files_added_to_existing", []))
    reconciled_count = len(getattr(result, "reconciled_orphans", []))
    transcript_count = len(getattr(result, "transcripts_delivered", []))
    wants_purged_count = sum(n for _, n in getattr(result, "wants_purged", []))
    no_url_count = len(getattr(result, "errors_no_url", []))

    # Touched record IDs — sorted for stability.
    touched = sorted(getattr(result, "touched_record_ids", set()))
    if len(touched) > 20:
        touched_str = ", ".join(f"`{rid}`" for rid in touched[:20]) + f", … (+{len(touched) - 20} more)"
    else:
        touched_str = ", ".join(f"`{rid}`" for rid in touched) or "(none)"

    summary_parts: list[str] = []
    if new_count:
        summary_parts.append(f"{new_count} new catalog record(s)")
    if attached_count:
        summary_parts.append(f"{attached_count} file(s) attached to existing record(s)")
    if reconciled_count:
        summary_parts.append(f"{reconciled_count} orphan file(s) reconciled")
    if transcript_count:
        summary_parts.append(f"{transcript_count} YouTube transcript(s) delivered")
    summary = " + ".join(summary_parts) if summary_parts else "no material catalog changes"

    bullet = (
        f"- **Session {date} — Round-{round_number} drain (auto-recorded by `drain.py`)** — "
        f"Drain output: **{summary}**. "
        f"Touched record IDs: {touched_str}. "
    )
    if wants_purged_count:
        bullet += (
            f"Stale `want` entries cleared by the format-final rule: **{wants_purged_count}**. "
        )
    if no_url_count:
        bullet += (
            f"Flagged (no extractable URL): **{no_url_count}**. "
        )
    bullet += (
        "Auto-generated skeleton — please replace with a hand-written description "
        "before the next drain. See `.claude/skills/research-pipeline/resources/_plan/update-discipline.md`."
    )
    return bullet


def _format_section_10_row(result: Any, round_number: int) -> str:
    """A new row appended to the §10 lookup table."""
    date = _today()
    new_count = len(getattr(result, "files_added_as_new_records", []))
    attached_count = len(getattr(result, "files_added_to_existing", []))
    if new_count and not attached_count:
        status = "🟡 Ingestion complete, stage 5 deferred"
    elif new_count and attached_count:
        status = "🟡 Ingestion complete, stage 5 deferred"
    elif attached_count:
        status = "🟡 Attachments complete, stage 5 deferred"
    else:
        status = "🟡 No material catalog changes"
    notes = (
        f"Auto-recorded by `drain.py` on {date}: {new_count} new record(s), "
        f"{attached_count} attachment(s). Stage 5 (content extraction into reports) "
        f"deferred. Replace this row with a hand-written summary before the next drain."
    )
    return f"| {round_number} | Auto-recorded drain ({date}) | {status} | {notes} |"


def _insert_session_bullet(text: str, bullet: str) -> str:
    """Insert `bullet` after the last existing `- **Session ` line in §1,
    or immediately before `**Open items live in:**` if no Session bullets
    exist yet, or at the end of §1 as a last resort.
    """
    # Find all existing session bullets; insert after the last one.
    matches = list(SESSION_BULLET_RE.finditer(text))
    if matches:
        last = matches[-1]
        # Find end of that bullet's line (could be multi-line in practice; use \n boundary).
        line_end = text.find("\n", last.end())
        if line_end == -1:
            line_end = len(text)
        return text[: line_end + 1] + bullet + "\n" + text[line_end + 1 :]
    # No session bullets — insert before "**Open items live in:**"
    m = OPEN_ITEMS_LIVE_IN_RE.search(text)
    if m:
        return text[: m.start()] + bullet + "\n\n" + text[m.start() :]
    # Fall back: append to end (script will surface a warning).
    return text + "\n" + bullet + "\n"


def _append_section_10_row(text: str, row: str) -> tuple[str, bool]:
    """Append `row` at the end of §10's table. Returns (new_text, did_append)."""
    m = SECTION_10_RE.search(text)
    if not m:
        return text, False
    s10_full = m.group(0)
    body = m.group(2)
    # Find the last table row position in `body`.
    last_row_iter = list(TABLE_ROW_RE.finditer(body))
    if not last_row_iter:
        return text, False
    last_row_match = last_row_iter[-1]
    # Find end of that row's line within body.
    line_end = body.find("\n", last_row_match.end())
    if line_end == -1:
        line_end = len(body)
    new_body = body[: line_end + 1] + row + "\n" + body[line_end + 1 :]
    new_s10_full = m.group(1) + new_body
    return text[: m.start()] + new_s10_full + text[m.end():], True


def _bump_version(text: str, date: str) -> tuple[str, str | None]:
    """Increment the minor part of the Version line and set its date. Returns
    (new_text, new_version_string|None). If no Version line, returns (text, None).
    """
    def repl(m: re.Match) -> str:
        prefix, major, minor, open_par, _old_date, close_par = m.groups()
        new_minor = str(int(minor) + 1)
        return f"{prefix}{major}.{new_minor}{open_par}{date}{close_par}"

    new_text, n = VERSION_LINE_RE.subn(repl, text, count=1)
    if n == 0:
        return text, None
    new_match = VERSION_LINE_RE.search(new_text)
    if new_match:
        major, minor, date_str = new_match.group(2), new_match.group(3), new_match.group(5)
        return new_text, f"v{major}.{minor} ({date_str})"
    return new_text, None


def update_plan_after_drain(result: Any, plan_path: Path) -> dict:
    """Drop a fresh Session bullet under §1, append a §10 row, and bump
    the Version line of `plan_path`. Returns a status dict; never raises
    (the drain shouldn't fail if PLAN.md is unparseable — surfaces a
    warning instead).
    """
    status = {
        "skipped": False,
        "skipped_reason": None,
        "round_number": None,
        "version_after": None,
        "bullet_inserted": False,
        "row_inserted": False,
    }
    if not _is_material(result):
        status["skipped"] = True
        status["skipped_reason"] = "no material catalog changes"
        return status
    if not plan_path.exists():
        status["skipped"] = True
        status["skipped_reason"] = f"PLAN.md not found at {plan_path}"
        return status

    text = plan_path.read_text(encoding="utf-8")

    # Round number = max in §10 + 1
    s10 = SECTION_10_RE.search(text)
    next_round = (_max_round_in_section_10(s10.group(2)) if s10 else 0) + 1
    status["round_number"] = next_round

    bullet = _format_session_bullet(result, next_round)
    row = _format_section_10_row(result, next_round)

    text2 = _insert_session_bullet(text, bullet)
    status["bullet_inserted"] = text2 != text

    text3, inserted_row = _append_section_10_row(text2, row)
    status["row_inserted"] = inserted_row

    text4, new_version = _bump_version(text3, _today())
    status["version_after"] = new_version

    plan_path.write_text(text4, encoding="utf-8")
    return status
