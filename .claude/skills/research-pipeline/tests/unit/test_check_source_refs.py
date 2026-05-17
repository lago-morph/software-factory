"""Unit tests for check-source-refs.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from tests.conftest import write_skill_md, default_config_yaml, write_sources_json


def _run(repo: Path) -> subprocess.CompletedProcess:
    src_dir = Path(__file__).resolve().parents[2] / "scripts"
    for name in ("check-source-refs.py", "_config.py", "url_canonicalize.py"):
        (repo / ".claude" / "skills" / "research-pipeline" / "scripts" / name).write_text(
            (src_dir / name).read_text()
        )
    script = repo / ".claude" / "skills" / "research-pipeline" / "scripts" / "check-source-refs.py"
    return subprocess.run([sys.executable, str(script)], capture_output=True, text=True)


def _setup(repo: Path, data: dict, reports: dict[str, str] = None) -> None:
    write_skill_md(repo, default_config_yaml())
    write_sources_json(repo, data)
    if reports:
        for path, content in reports.items():
            full = repo / path
            full.parent.mkdir(parents=True, exist_ok=True)
            full.write_text(content, encoding="utf-8")


class TestCheckRefs:
    def test_no_reports_no_records_passes(self, tmp_repo):
        _setup(tmp_repo, {})
        result = _run(tmp_repo)
        assert result.returncode == 0

    def test_url_in_report_and_in_catalog_passes(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/cited")
        _setup(tmp_repo, {
            rid: {"id": rid, "canonical_url": canon, "title": "X"}
        }, {
            "research/01-test.md": "See https://example.com/cited for details.\n"
        })
        result = _run(tmp_repo)
        assert result.returncode == 0, result.stderr

    def test_url_in_report_not_in_catalog_fails(self, tmp_repo):
        _setup(tmp_repo, {}, {
            "research/01-test.md": "Cites https://example.com/orphan but no record.\n"
        })
        result = _run(tmp_repo)
        assert result.returncode == 1
        assert "no record in catalog" in result.stderr

    def test_url_with_tracking_params_canonicalized(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/p")
        _setup(tmp_repo, {
            rid: {"id": rid, "canonical_url": canon, "title": "X"}
        }, {
            "research/01-test.md": "Read https://example.com/p?utm_source=twitter for more.\n"
        })
        result = _run(tmp_repo)
        # Should match after canonicalization
        assert result.returncode == 0

    def test_punctuation_after_url_handled(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/article")
        _setup(tmp_repo, {
            rid: {"id": rid, "canonical_url": canon, "title": "X"}
        }, {
            "research/01-test.md": "See https://example.com/article, which is great.\n"
        })
        result = _run(tmp_repo)
        assert result.returncode == 0

    def test_url_in_multiple_reports(self, tmp_repo):
        _setup(tmp_repo, {}, {
            "research/01-a.md": "Cite https://example.com/x.\n",
            "research/02-b.md": "Also https://example.com/x.\n",
        })
        result = _run(tmp_repo)
        assert result.returncode == 1
        # Should mention this URL once with multi-report count
        assert "1 other report" in result.stderr or "other report(s)" in result.stderr

    def test_record_with_original_url_also_matches(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/new")
        _setup(tmp_repo, {
            rid: {
                "id": rid, "canonical_url": canon, "title": "X",
                "original_url": "https://example.com/old",
            }
        }, {
            "research/01-test.md": "Old link https://example.com/old.\n"
        })
        result = _run(tmp_repo)
        # original_url should also count
        assert result.returncode == 0, result.stderr
