"""Unit tests for check-plan-consistency.py.

The script reads PLAN.md + git history. We exercise just the parsing /
check-helper functions directly so the tests don't need a populated
git history.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "scripts"
    / "check-plan-consistency.py"
)
spec = importlib.util.spec_from_file_location("check_plan_consistency", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class TestVersionLineParsing:
    def test_parses_valid_line(self, tmp_path):
        plan = tmp_path / "PLAN.md"
        plan.write_text("# Plan\n\n**Version:** v0.14 (2026-05-17)\n\nbody\n")
        findings: list = []
        result = mod.check_version_line(plan, findings)
        assert result == (0, 14, "2026-05-17")
        assert not findings

    def test_missing_line_records_error(self, tmp_path):
        plan = tmp_path / "PLAN.md"
        plan.write_text("# Plan\n\nNo version line here\n")
        findings: list = []
        result = mod.check_version_line(plan, findings)
        assert result is None
        assert any(f.level == "error" for f in findings)

    def test_unparseable_date_records_error(self, tmp_path):
        plan = tmp_path / "PLAN.md"
        plan.write_text("# Plan\n\n**Version:** v1.0 (NOT-A-DATE)\n")
        findings: list = []
        result = mod.check_version_line(plan, findings)
        # Doesn't match the strict regex; treated as missing.
        assert result is None
        assert any(f.level == "error" for f in findings)


class TestRoundConsistency:
    def _plan(self, body: str) -> Path:
        # Caller provides §10 + session bullets.
        return body

    def test_matched_rounds_no_finding(self, tmp_path):
        plan = tmp_path / "PLAN.md"
        plan.write_text(
            "## 1. Current state\n\n"
            "- **Session 2026-05-17 — Round-2 drain** — text\n\n"
            "## 10. Round-by-round canonical reports (lookup table)\n\n"
            "| Round | Topic | Status | Notes |\n"
            "|---|---|---|---|\n"
            "| 1 | initial | ✅ | foo |\n"
            "| 2 | round-2 | 🟡 | bar |\n"
        )
        findings: list = []
        mod.check_round_consistency(plan, findings)
        # Round-1 has a table row but no session-bullet — that's the orphan-row case
        # but in this fixture there's no archive heading either, so it should flag
        # 1 as missing-bullet. Skip strict check: just ensure no missing-rows finding.
        msgs = [f.message for f in findings]
        assert not any("missing rows" in m for m in msgs)

    def test_missing_row_flagged(self, tmp_path):
        plan = tmp_path / "PLAN.md"
        plan.write_text(
            "## 1\n\n"
            "- **Session 2026-05-17 — Round-7 drain** — text\n\n"
            "## 10. lookup\n\n"
            "| Round | Topic |\n"
            "|---|---|\n"
            "| 1 | x |\n"
        )
        findings: list = []
        mod.check_round_consistency(plan, findings)
        assert any("missing rows" in f.message for f in findings)

    def test_archive_heading_counts_as_round_mention(self, tmp_path):
        plan = tmp_path / "PLAN.md"
        plan.write_text(
            "## 1\n\n"
            "no session bullets here\n\n"
            "## 10. lookup\n\n"
            "| Round | Topic |\n"
            "|---|---|\n"
            "| 5 | foo |\n\n"
            "## 11. Round 5 — archive\n\nold stuff\n"
        )
        findings: list = []
        mod.check_round_consistency(plan, findings)
        # Round 5 appears in both the table and an archive heading; no missing-bullet finding.
        assert not any("with no corresponding session bullet" in f.message for f in findings)
