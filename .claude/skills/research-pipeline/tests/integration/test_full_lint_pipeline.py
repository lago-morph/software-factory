"""End-to-end integration tests: run lint-sources.sh against fixture catalogs.

Each fixture under tests/fixtures/ is a complete repo-like tree:
    tests/fixtures/<name>/
        .claude/skills/research-pipeline/SKILL.md     (with config)
        reference-only/sources.json
        reference-only/sources.schema.json
        reference-only/<id>/...
        research/.../*.md

The integration test:
    1. Copies the fixture tree into a tmp_path
    2. Copies the actual scripts/ from the repo into the temp tree
    3. Runs lint-sources.sh
    4. Asserts expected exit code and key patterns in stderr/stdout
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tests.conftest import (
    write_skill_md, default_config_yaml, write_sources_json, write_schema,
)


REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS_SRC = REPO_ROOT / ".claude" / "skills" / "research-pipeline" / "scripts"

LINT = "lint-sources.sh"
SCRIPT_FILES = [
    "_config.py", "url_canonicalize.py", "extract_url.py", "extract_title.py",
    "classify_text.py",
    "validate-config.py", "validate-sources.py",
    "check-source-refs.py", "check-source-dirs.py",
    "check-fetch-provenance.py", "sanity-check-record.py",
    "lint-sources.sh",
]


def _setup_repo(tmp_path: Path) -> Path:
    """Build a minimal repo with scripts + config."""
    skill_dir = tmp_path / ".claude" / "skills" / "research-pipeline" / "scripts"
    skill_dir.mkdir(parents=True)
    (tmp_path / "reference-only").mkdir()
    (tmp_path / "research").mkdir()
    write_skill_md(tmp_path, default_config_yaml())
    write_schema(tmp_path)
    write_sources_json(tmp_path, {})
    # Copy scripts
    for name in SCRIPT_FILES:
        src = SCRIPTS_SRC / name
        if src.exists():
            dst = skill_dir / name
            dst.write_bytes(src.read_bytes())
            if name.endswith(".sh"):
                dst.chmod(0o755)
    return tmp_path


def _run_lint(repo: Path) -> subprocess.CompletedProcess:
    script = repo / ".claude" / "skills" / "research-pipeline" / "scripts" / LINT
    return subprocess.run(
        ["bash", str(script)],
        capture_output=True, text=True, cwd=str(repo),
    )


@pytest.mark.integration
class TestLintPipeline:
    def test_empty_catalog_passes(self, tmp_path):
        repo = _setup_repo(tmp_path)
        result = _run_lint(repo)
        assert result.returncode == 0, result.stderr + result.stdout

    def test_single_complete_record_passes(self, tmp_path):
        repo = _setup_repo(tmp_path)
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/x")
        write_sources_json(repo, {
            rid: {
                "id": rid, "canonical_url": canon, "title": "X",
                "files": [{
                    "format": "html", "filename": "main.html",
                    "ingestion_status": "have", "completeness": "complete"
                }]
            }
        })
        (repo / "reference-only" / rid).mkdir()
        (repo / "reference-only" / rid / "main.html").write_text("<html></html>")
        result = _run_lint(repo)
        assert result.returncode == 0, result.stderr + result.stdout

    def test_have_file_missing_fails(self, tmp_path):
        repo = _setup_repo(tmp_path)
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/x")
        write_sources_json(repo, {
            rid: {
                "id": rid, "canonical_url": canon, "title": "X",
                "files": [{
                    "format": "html", "filename": "main.html",
                    "ingestion_status": "have",
                }]
            }
        })
        result = _run_lint(repo)
        assert result.returncode == 1
        assert "missing on disk" in result.stderr or "not on disk" in result.stderr

    def test_orphan_file_fails(self, tmp_path):
        repo = _setup_repo(tmp_path)
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/x")
        write_sources_json(repo, {
            rid: {"id": rid, "canonical_url": canon, "title": "X", "files": []}
        })
        (repo / "reference-only" / rid).mkdir()
        (repo / "reference-only" / rid / "stray.html").write_text("orphan")
        result = _run_lint(repo)
        assert result.returncode == 1
        assert "not in record" in result.stderr

    def test_url_in_report_not_in_catalog_fails(self, tmp_path):
        repo = _setup_repo(tmp_path)
        (repo / "research" / "01.md").write_text("Cites https://example.com/orphan\n")
        result = _run_lint(repo)
        assert result.returncode == 1
        assert "no record in catalog" in result.stderr

    def test_complete_with_open_provenance_fails(self, tmp_path):
        repo = _setup_repo(tmp_path)
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/x")
        write_sources_json(repo, {
            rid: {
                "id": rid, "canonical_url": canon, "title": "X",
                "files": [{
                    "format": "html", "filename": "main.html",
                    "ingestion_status": "have", "completeness": "complete",
                    "fetch_provenance": {
                        "issue_number": 42, "pr_number": 99,
                        "branch": "fetched/issue-42", "status": "open",
                    }
                }]
            }
        })
        (repo / "reference-only" / rid).mkdir()
        (repo / "reference-only" / rid / "main.html").write_text("<html></html>")
        result = _run_lint(repo)
        assert result.returncode == 1
        assert "close issue #42" in result.stderr
