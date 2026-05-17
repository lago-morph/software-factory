"""Unit tests for process-url-list.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from tests.conftest import write_skill_md, default_config_yaml, write_sources_json


def _run(repo: Path, url_file: Path, *args) -> subprocess.CompletedProcess:
    src_dir = Path(__file__).resolve().parents[2] / "scripts"
    for name in ("process-url-list.py", "_config.py", "url_canonicalize.py", "classify_text.py"):
        (repo / ".claude" / "skills" / "research-pipeline" / "scripts" / name).write_text(
            (src_dir / name).read_text()
        )
    script = repo / ".claude" / "skills" / "research-pipeline" / "scripts" / "process-url-list.py"
    return subprocess.run(
        [sys.executable, str(script), str(url_file), *args],
        capture_output=True, text=True,
    )


def _setup(repo: Path, data: dict = None) -> Path:
    write_skill_md(repo, default_config_yaml())
    write_sources_json(repo, data or {})
    return repo


class TestProcessUrlList:
    def test_adds_new_records_from_url_list(self, tmp_repo):
        _setup(tmp_repo)
        url_file = tmp_repo / "research" / "manual" / "urls.txt"
        url_file.parent.mkdir(parents=True)
        url_file.write_text(
            "https://example.com/a\n"
            "https://example.com/b\n"
            "https://example.com/c\n"
        )
        result = _run(tmp_repo, url_file)
        assert result.returncode == 0, result.stderr
        data = json.loads((tmp_repo / "reference-only" / "sources.json").read_text())
        assert len(data) == 3
        for record in data.values():
            assert record["title"] == "(unknown)"
            assert record["canonical_url"].startswith("https://example.com/")

    def test_skips_existing_urls(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/existing")
        _setup(tmp_repo, {
            rid: {"id": rid, "canonical_url": canon, "title": "Already Here"}
        })
        url_file = tmp_repo / "research" / "manual" / "urls.txt"
        url_file.parent.mkdir(parents=True)
        url_file.write_text("https://example.com/existing\nhttps://example.com/new\n")
        result = _run(tmp_repo, url_file)
        assert result.returncode == 0
        data = json.loads((tmp_repo / "reference-only" / "sources.json").read_text())
        assert len(data) == 2  # one existing, one new
        # The existing record should keep its original title
        assert data[rid]["title"] == "Already Here"

    def test_rejects_non_url_list(self, tmp_repo):
        _setup(tmp_repo)
        f = tmp_repo / "research" / "manual" / "mixed.txt"
        f.parent.mkdir(parents=True)
        f.write_text(
            "URL: https://example.com/source\n"
            "Title: A Page\n"
            "Body content...\n"
        )
        result = _run(tmp_repo, f)
        assert result.returncode == 1
        assert "not a pure URL list" in result.stderr

    def test_dry_run_doesnt_modify(self, tmp_repo):
        _setup(tmp_repo)
        f = tmp_repo / "research" / "manual" / "urls.txt"
        f.parent.mkdir(parents=True)
        f.write_text("https://example.com/x\n")
        _run(tmp_repo, f, "--dry-run")
        data = json.loads((tmp_repo / "reference-only" / "sources.json").read_text())
        assert data == {}

    def test_delete_after_removes_file(self, tmp_repo):
        _setup(tmp_repo)
        f = tmp_repo / "research" / "manual" / "urls.txt"
        f.parent.mkdir(parents=True)
        f.write_text("https://example.com/x\n")
        _run(tmp_repo, f, "--delete-after")
        assert not f.exists()
        data = json.loads((tmp_repo / "reference-only" / "sources.json").read_text())
        assert len(data) == 1

    def test_output_is_sorted_by_id(self, tmp_repo):
        _setup(tmp_repo)
        f = tmp_repo / "research" / "manual" / "urls.txt"
        f.parent.mkdir(parents=True)
        # Write in non-alphabetical URL order
        f.write_text(
            "https://example.com/zebra\n"
            "https://example.com/aardvark\n"
            "https://example.com/middle\n"
        )
        _run(tmp_repo, f)
        raw = (tmp_repo / "reference-only" / "sources.json").read_text()
        data = json.loads(raw)
        keys = list(data.keys())
        assert keys == sorted(keys), "keys should be sorted alphabetically"
