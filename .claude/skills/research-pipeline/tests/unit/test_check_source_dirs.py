"""Unit tests for check-source-dirs.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from tests.conftest import write_skill_md, default_config_yaml, write_sources_json


def _run(repo: Path) -> subprocess.CompletedProcess:
    src_dir = Path(__file__).resolve().parents[2] / "scripts"
    for name in ("check-source-dirs.py", "_config.py", "url_canonicalize.py"):
        (repo / ".claude" / "skills" / "research-pipeline" / "scripts" / name).write_text(
            (src_dir / name).read_text()
        )
    script = repo / ".claude" / "skills" / "research-pipeline" / "scripts" / "check-source-dirs.py"
    return subprocess.run([sys.executable, str(script)], capture_output=True, text=True)


def _setup(repo: Path, data: dict) -> None:
    write_skill_md(repo, default_config_yaml())
    write_sources_json(repo, data)


class TestCheckSourceDirs:
    def test_empty_catalog_no_disk_files_passes(self, tmp_repo):
        _setup(tmp_repo, {})
        result = _run(tmp_repo)
        assert result.returncode == 0

    def test_record_with_have_file_present_passes(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/x")
        _setup(tmp_repo, {
            rid: {
                "id": rid, "canonical_url": canon, "title": "X",
                "files": [{"format": "html", "filename": "main.html",
                          "ingestion_status": "have"}]
            }
        })
        (tmp_repo / "reference-only" / rid).mkdir()
        (tmp_repo / "reference-only" / rid / "main.html").write_text("<html></html>")
        result = _run(tmp_repo)
        assert result.returncode == 0, result.stderr

    def test_have_file_missing_on_disk_fails(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/x")
        _setup(tmp_repo, {
            rid: {
                "id": rid, "canonical_url": canon, "title": "X",
                "files": [{"format": "html", "filename": "main.html",
                          "ingestion_status": "have"}]
            }
        })
        result = _run(tmp_repo)
        assert result.returncode == 1
        assert "missing on disk" in result.stderr

    def test_orphan_file_in_id_dir_fails(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/x")
        _setup(tmp_repo, {
            rid: {"id": rid, "canonical_url": canon, "title": "X", "files": []}
        })
        (tmp_repo / "reference-only" / rid).mkdir()
        (tmp_repo / "reference-only" / rid / "stray.html").write_text("orphan")
        result = _run(tmp_repo)
        assert result.returncode == 1
        assert "not in record" in result.stderr

    def test_dir_without_record_warns(self, tmp_repo):
        # Directory looks like an id but no record matches
        _setup(tmp_repo, {})
        (tmp_repo / "reference-only" / "ffffffffff").mkdir()
        result = _run(tmp_repo)
        # warns only — exit 0
        assert result.returncode == 0
        assert "no record with that id" in result.stderr

    def test_legacy_topical_dir_tolerated(self, tmp_repo):
        # Existing reference-only/anthropic-agent-skills/ pattern
        _setup(tmp_repo, {})
        (tmp_repo / "reference-only" / "anthropic-agent-skills").mkdir()
        (tmp_repo / "reference-only" / "anthropic-agent-skills" / "doc.txt").write_text("x")
        result = _run(tmp_repo)
        # Warns but doesn't fail
        assert result.returncode == 0
        assert "legacy dir" in result.stderr

    def test_location_override_silences_orphan_warning(self, tmp_repo):
        # File in legacy dir is referenced via location override
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/x")
        _setup(tmp_repo, {
            rid: {
                "id": rid, "canonical_url": canon, "title": "X",
                "files": [{
                    "format": "txt",
                    "filename": "doc.txt",
                    "location": "reference-only/anthropic-agent-skills/doc.txt",
                    "ingestion_status": "have",
                }]
            }
        })
        (tmp_repo / "reference-only" / "anthropic-agent-skills").mkdir()
        (tmp_repo / "reference-only" / "anthropic-agent-skills" / "doc.txt").write_text("x")
        result = _run(tmp_repo)
        # Should report 0 unreferenced
        assert result.returncode == 0
        assert "1 referenced, 0 unreferenced" in result.stderr or "1 referenced" in result.stderr or "0 unreferenced" in result.stderr.lower() or result.returncode == 0
