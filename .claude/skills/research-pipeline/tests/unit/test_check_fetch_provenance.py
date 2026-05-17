"""Unit tests for check-fetch-provenance.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from tests.conftest import write_skill_md, default_config_yaml, write_sources_json


def _run(repo: Path) -> subprocess.CompletedProcess:
    src_dir = Path(__file__).resolve().parents[2] / "scripts"
    for name in ("check-fetch-provenance.py", "_config.py", "url_canonicalize.py"):
        (repo / ".claude" / "skills" / "research-pipeline" / "scripts" / name).write_text(
            (src_dir / name).read_text()
        )
    script = repo / ".claude" / "skills" / "research-pipeline" / "scripts" / "check-fetch-provenance.py"
    return subprocess.run([sys.executable, str(script)], capture_output=True, text=True)


def _record(files: list[dict]) -> dict:
    return {
        "0000000000": {
            "id": "0000000000",
            "canonical_url": "https://example.com/x",
            "title": "X",
            "files": files,
        }
    }


def _setup(repo: Path, data: dict) -> None:
    write_skill_md(repo, default_config_yaml())
    write_sources_json(repo, data)


class TestProvenance:
    def test_no_provenance_passes(self, tmp_repo):
        _setup(tmp_repo, _record([
            {"format": "html", "filename": "m.html", "ingestion_status": "have"}
        ]))
        result = _run(tmp_repo)
        assert result.returncode == 0

    def test_complete_with_open_provenance_fails(self, tmp_repo):
        _setup(tmp_repo, _record([{
            "format": "html", "filename": "m.html", "ingestion_status": "have",
            "completeness": "complete",
            "fetch_provenance": {
                "issue_number": 42, "pr_number": 99,
                "branch": "fetched/issue-42", "status": "open",
            }
        }]))
        result = _run(tmp_repo)
        assert result.returncode == 1
        assert "close issue #42" in result.stderr
        assert "merge or close PR #99" in result.stderr
        assert "delete branch" in result.stderr

    def test_complete_with_merged_provenance_passes(self, tmp_repo):
        _setup(tmp_repo, _record([{
            "format": "html", "filename": "m.html", "ingestion_status": "have",
            "completeness": "complete",
            "fetch_provenance": {
                "issue_number": 42, "pr_number": 99,
                "branch": None, "status": "merged",
            }
        }]))
        result = _run(tmp_repo)
        assert result.returncode == 0

    def test_have_but_not_complete_warns_not_errors(self, tmp_repo):
        _setup(tmp_repo, _record([{
            "format": "html", "filename": "m.html", "ingestion_status": "have",
            "completeness": "unknown",
            "fetch_provenance": {"issue_number": 42, "status": "open"}
        }]))
        result = _run(tmp_repo)
        # have + open is warning only
        assert result.returncode == 0

    def test_open_issue_no_branch_warns(self, tmp_repo):
        _setup(tmp_repo, _record([{
            "format": "html", "filename": "m.html", "ingestion_status": "want",
            "fetch_provenance": {"issue_number": 42, "status": "open"}
        }]))
        result = _run(tmp_repo)
        # want + issue open is just a warning
        assert result.returncode == 0
        assert "no branch" in result.stderr
