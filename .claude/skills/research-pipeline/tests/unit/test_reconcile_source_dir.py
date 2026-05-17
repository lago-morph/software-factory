"""Unit tests for reconcile-source-dir.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from tests.conftest import write_skill_md, default_config_yaml, write_sources_json


def _run(repo: Path, *args) -> subprocess.CompletedProcess:
    src_dir = Path(__file__).resolve().parents[2] / "scripts"
    for name in ("reconcile-source-dir.py", "_config.py", "url_canonicalize.py", "extract_url.py"):
        (repo / ".claude" / "skills" / "research-pipeline" / "scripts" / name).write_text(
            (src_dir / name).read_text()
        )
    script = repo / ".claude" / "skills" / "research-pipeline" / "scripts" / "reconcile-source-dir.py"
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True, text=True,
    )


def _setup(repo: Path, rid: str, url: str, existing_files: list = None) -> Path:
    write_skill_md(repo, default_config_yaml())
    files = existing_files or []
    write_sources_json(repo, {
        rid: {"id": rid, "canonical_url": url, "title": "Test", "files": files}
    })
    return repo / "reference-only" / rid


class TestReconcile:
    def test_no_dir_no_change(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/x")
        _setup(tmp_repo, rid, canon)
        result = _run(tmp_repo, rid)
        assert result.returncode == 0
        data = json.loads((tmp_repo / "reference-only" / "sources.json").read_text())
        assert data[rid]["files"] == []

    def test_adds_new_file_to_record(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/x")
        dir_path = _setup(tmp_repo, rid, canon)
        dir_path.mkdir()
        (dir_path / "main.html").write_text("<html></html>")
        result = _run(tmp_repo, rid)
        assert result.returncode == 0
        data = json.loads((tmp_repo / "reference-only" / "sources.json").read_text())
        assert len(data[rid]["files"]) == 1
        f = data[rid]["files"][0]
        assert f["filename"] == "main.html"
        assert f["format"] == "html"
        assert f["ingestion_status"] == "have"
        assert "sha256" in f

    def test_skips_already_registered_file(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/x")
        dir_path = _setup(tmp_repo, rid, canon, [{
            "format": "html", "filename": "main.html",
            "ingestion_status": "have", "completeness": "complete"
        }])
        dir_path.mkdir()
        (dir_path / "main.html").write_text("x")
        result = _run(tmp_repo, rid)
        assert result.returncode == 0
        data = json.loads((tmp_repo / "reference-only" / "sources.json").read_text())
        # Still just one entry
        assert len(data[rid]["files"]) == 1

    def test_image_gets_pending_summary_marker(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/x")
        dir_path = _setup(tmp_repo, rid, canon)
        dir_path.mkdir()
        (dir_path / "diagram.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        _run(tmp_repo, rid)
        data = json.loads((tmp_repo / "reference-only" / "sources.json").read_text())
        f = data[rid]["files"][0]
        assert f["format"] == "image/png"
        assert "pending summary" in (f.get("comment") or "")

    def test_dry_run_doesnt_modify(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/x")
        dir_path = _setup(tmp_repo, rid, canon)
        dir_path.mkdir()
        (dir_path / "new.html").write_text("x")
        _run(tmp_repo, rid, "--dry-run")
        data = json.loads((tmp_repo / "reference-only" / "sources.json").read_text())
        assert data[rid]["files"] == []

    def test_all_flag_scans_every_record(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon1, r1 = canonicalize_and_id("https://example.com/a")
        canon2, r2 = canonicalize_and_id("https://example.com/b")
        write_skill_md(tmp_repo, default_config_yaml())
        write_sources_json(tmp_repo, {
            r1: {"id": r1, "canonical_url": canon1, "title": "A", "files": []},
            r2: {"id": r2, "canonical_url": canon2, "title": "B", "files": []},
        })
        for r in (r1, r2):
            d = tmp_repo / "reference-only" / r
            d.mkdir()
            (d / "file.txt").write_text(f"content for {r}")
        result = _run(tmp_repo, "--all")
        assert result.returncode == 0
        data = json.loads((tmp_repo / "reference-only" / "sources.json").read_text())
        assert len(data[r1]["files"]) == 1
        assert len(data[r2]["files"]) == 1
