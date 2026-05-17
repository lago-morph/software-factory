"""Check that PLAN.md is in step with the catalog and recent drains.

The research-pipeline runs ingestion actions (drain, catalog edits, manual
additions) that should each leave a footprint in PLAN.md — a new "Session"
bullet, an updated `**Version:**` line, sometimes a new §10 lookup-table row.
History shows this often gets skipped. This script flags the drift.

Checks (each is one of [`error`, `warn`, `info`]):

  1. error: PLAN.md exists and its `**Version:** vX.Y (YYYY-MM-DD)` line parses.
  2. warn:  PLAN.md was not updated in the same commit as the most-recent
            commit that touched `sources.json`.
  3. warn:  Within the last N commits (default 10), every commit that
            modified `sources.json` also modified PLAN.md. Lists offenders.
  4. warn:  The `Round-N` rounds named in session bullets match the
            numbered rows in the §10 lookup table (no orphan rows; no
            orphan bullets).
  5. info:  The date in the `**Version:**` line is not older than the most
            recent commit touching the catalog.

Exit code:
    0 — all checks ok (warnings reported informationally)
    1 — at least one `error` check failed
    2 — `--strict` was passed and any `warn` check fired
    3 — script invocation problem (missing files, git not available, ...)

CLI:
    python check-plan-consistency.py            # report, exit 0 unless error
    python check-plan-consistency.py --strict   # exit 2 on warnings
    python check-plan-consistency.py --window N # check last N commits
    python check-plan-consistency.py --quiet    # only print failures
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import (  # noqa: E402
    ConfigError, data_path, load_config, repo_root, resolve,
)


# ---------- finding files via config ------------------------------------

def plan_path() -> Path:
    """The PLAN.md path, with a sensible default if not in config."""
    cfg = load_config()
    return resolve(cfg.get("plan_path", "research/PLAN.md"))


# ---------- helpers -----------------------------------------------------

def _safe_rel(p: Path) -> Path | str:
    """Path relative to repo root if possible, else the path itself.
    Tests construct PLAN.md outside the repo tree; don't crash on those."""
    try:
        return p.relative_to(repo_root())
    except ValueError:
        return p


VERSION_LINE_RE = re.compile(
    r"^\*\*Version:\*\*\s+v(\d+)\.(\d+)\s+\((\d{4}-\d{2}-\d{2})\)\s*$",
    re.MULTILINE,
)

ROUND_TABLE_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|", re.MULTILINE)
ROUND_BULLET_RE = re.compile(r"Round[\s-](\d+)", re.IGNORECASE)
SECTION_10_RE = re.compile(
    r"^## 10\..*?(?=^##\s|\Z)", re.MULTILINE | re.DOTALL,
)


def git_log_paths(path: Path, n: int) -> list[str]:
    """Return the last n commit SHAs that touched `path` (newest first)."""
    root = repo_root()
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path
    out = subprocess.run(
        ["git", "log", f"-{n}", "--format=%H", "--", str(rel)],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if out.returncode != 0:
        return []
    return out.stdout.split()


def git_recent_catalog_commits(window: int) -> list[str]:
    """The last `window` commits touching reference-only/* (sources.json or
    any record file). Newest first.
    """
    root = repo_root()
    cfg = load_config()
    lib = cfg.get("library_path", "reference-only")
    out = subprocess.run(
        ["git", "log", f"-{window}", "--format=%H", "--", lib],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if out.returncode != 0:
        return []
    return out.stdout.split()


def git_commit_touched_path(sha: str, path: Path) -> bool:
    root = repo_root()
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path
    out = subprocess.run(
        ["git", "show", "--stat", "--format=", sha, "--", str(rel)],
        cwd=root, capture_output=True, text=True, check=False,
    )
    return out.returncode == 0 and bool(out.stdout.strip())


def git_commit_subject(sha: str) -> str:
    root = repo_root()
    out = subprocess.run(
        ["git", "show", "-s", "--format=%s", sha],
        cwd=root, capture_output=True, text=True, check=False,
    )
    return out.stdout.strip() if out.returncode == 0 else "(unknown)"


def git_commit_date(sha: str) -> str:
    root = repo_root()
    out = subprocess.run(
        ["git", "show", "-s", "--format=%ci", sha],
        cwd=root, capture_output=True, text=True, check=False,
    )
    if out.returncode != 0:
        return ""
    # %ci is e.g. "2026-05-17 21:28:34 +0000"
    return out.stdout.strip().split(" ")[0]


# ---------- the checks --------------------------------------------------

class Finding:
    def __init__(self, level: str, check: str, message: str):
        self.level = level   # "error" | "warn" | "info"
        self.check = check
        self.message = message

    def format(self) -> str:
        glyph = {"error": "✗", "warn": "⚠", "info": "ℹ"}.get(self.level, "?")
        return f"{glyph} [{self.check}] {self.message}"


def check_version_line(plan: Path, findings: list[Finding]) -> tuple[int, int, str] | None:
    text = plan.read_text(encoding="utf-8")
    m = VERSION_LINE_RE.search(text[:4000])  # header area
    if not m:
        findings.append(Finding(
            "error", "version-line",
            f"no parseable '**Version:** vX.Y (YYYY-MM-DD)' line in the "
            f"first 4 KB of {_safe_rel(plan)}",
        ))
        return None
    major, minor, date = m.group(1), m.group(2), m.group(3)
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        findings.append(Finding(
            "error", "version-line",
            f"version line has an unparseable date: {date!r}",
        ))
        return None
    return (int(major), int(minor), date)


def check_latest_catalog_commit_touched_plan(
    plan: Path, catalog: Path, findings: list[Finding],
) -> None:
    catalog_commits = git_log_paths(catalog, 1)
    if not catalog_commits:
        findings.append(Finding(
            "info", "latest-catalog",
            "no git history for the catalog — fresh repo? skipping freshness check.",
        ))
        return
    latest = catalog_commits[0]
    if not git_commit_touched_path(latest, plan):
        subject = git_commit_subject(latest)
        date = git_commit_date(latest)
        findings.append(Finding(
            "warn", "latest-catalog",
            f"the most recent catalog commit ({latest[:8]} {date} \"{subject}\") "
            f"did not also touch {_safe_rel(plan)}. "
            f"Expectation: every catalog mutation accompanies a PLAN.md edit.",
        ))


def check_recent_window(
    plan: Path, catalog: Path, window: int, findings: list[Finding],
) -> None:
    catalog_commits = git_recent_catalog_commits(window)
    if not catalog_commits:
        return
    orphans = []
    for sha in catalog_commits:
        if not git_commit_touched_path(sha, plan):
            orphans.append(sha)
    if orphans:
        lines = [
            f"{len(orphans)} of the last {len(catalog_commits)} catalog-touching "
            f"commit(s) did not also touch {_safe_rel(plan)}:",
        ]
        for sha in orphans[:10]:
            date = git_commit_date(sha)
            subject = git_commit_subject(sha)
            lines.append(f"    - {sha[:8]} {date} \"{subject}\"")
        if len(orphans) > 10:
            lines.append(f"    - … {len(orphans) - 10} more")
        findings.append(Finding("warn", "recent-window", "\n".join(lines)))


def check_round_consistency(plan: Path, findings: list[Finding]) -> None:
    text = plan.read_text(encoding="utf-8")

    # Rounds named in a Session bullet OR an archive section heading.
    # Older rounds (1, 2, 3, 4, 5, 6) live as ## headings rather than Session
    # bullets; modern rounds (7+) live as Session bullets. Both count.
    rounded: set[int] = set()
    for line in text.splitlines():
        stripped = line.lstrip()
        is_session_bullet = stripped.startswith("- **Session")
        is_archive_heading = stripped.startswith("## ") and "Round" in stripped
        if not (is_session_bullet or is_archive_heading):
            continue
        for m in ROUND_BULLET_RE.finditer(line):
            rounded.add(int(m.group(1)))

    # Rounds present as table rows inside §10.
    s10 = SECTION_10_RE.search(text)
    if s10 is None:
        findings.append(Finding(
            "warn", "round-consistency",
            "no §10 round-by-round lookup table found in PLAN.md",
        ))
        return
    table_rounds: set[int] = set()
    for m in ROUND_TABLE_ROW_RE.finditer(s10.group(0)):
        n = int(m.group(1))
        # Defensive: numbers > 100 are unlikely round numbers (column-width hits)
        if n < 100:
            table_rounds.add(n)

    bullet_rounds = rounded

    missing_rows = bullet_rounds - table_rounds
    missing_bullets = table_rounds - bullet_rounds
    if missing_rows:
        findings.append(Finding(
            "warn", "round-consistency",
            f"§10 table is missing rows for round(s) named in session bullets: "
            f"{sorted(missing_rows)}",
        ))
    if missing_bullets:
        findings.append(Finding(
            "warn", "round-consistency",
            f"§10 table lists round(s) with no corresponding session bullet: "
            f"{sorted(missing_bullets)}",
        ))


def check_version_date_not_stale(
    plan: Path, catalog: Path, version_info: tuple[int, int, str] | None,
    findings: list[Finding],
) -> None:
    if version_info is None:
        return
    _, _, plan_date = version_info
    latest = git_log_paths(catalog, 1)
    if not latest:
        return
    catalog_date = git_commit_date(latest[0])
    if not catalog_date:
        return
    if plan_date < catalog_date:
        findings.append(Finding(
            "info", "version-date",
            f"PLAN.md Version date ({plan_date}) is older than the most recent "
            f"catalog commit ({catalog_date}). Bump the Version line if this "
            f"PR touches catalog state.",
        ))


# ---------- main --------------------------------------------------------

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero on warnings as well as errors")
    ap.add_argument("--quiet", action="store_true",
                    help="only print findings, not the header")
    ap.add_argument("--window", type=int, default=10,
                    help="how many recent catalog-touching commits to inspect")
    args = ap.parse_args(argv[1:])

    try:
        plan = plan_path()
        catalog = data_path()
    except ConfigError as e:
        print(f"✗ config error: {e}", file=sys.stderr)
        return 3

    if not plan.exists():
        print(f"✗ PLAN.md not found at {plan}", file=sys.stderr)
        return 1

    findings: list[Finding] = []
    version_info = check_version_line(plan, findings)
    check_latest_catalog_commit_touched_plan(plan, catalog, findings)
    check_recent_window(plan, catalog, args.window, findings)
    check_round_consistency(plan, findings)
    check_version_date_not_stale(plan, catalog, version_info, findings)

    errors = [f for f in findings if f.level == "error"]
    warns = [f for f in findings if f.level == "warn"]
    infos = [f for f in findings if f.level == "info"]

    if not args.quiet:
        print(f"plan-consistency: {len(errors)} error(s), {len(warns)} warning(s), "
              f"{len(infos)} info note(s) on {_safe_rel(plan)}")
    for f in findings:
        print(f.format())
    if not findings and not args.quiet:
        print("✓ PLAN.md consistent with catalog and recent history.")

    if errors:
        return 1
    if args.strict and warns:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
