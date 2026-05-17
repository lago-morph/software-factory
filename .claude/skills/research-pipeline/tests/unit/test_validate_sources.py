"""Unit tests for validate-sources.py.

Tests use the actual script as a subprocess so they cover the full main()
path including its config loading. The conftest sets up a sandboxed repo
under tmp_path, and we configure the test environment so the script's
config loader points there.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tests.conftest import (
    write_skill_md, default_config_yaml, write_sources_json, write_schema,
)

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "validate-sources.py"


def _run(repo: Path) -> subprocess.CompletedProcess:
    """Run validate-sources.py inside the temp repo."""
    env = os.environ.copy()
    # Tell the script's config loader to look at the temp repo's SKILL.md
    # by running with PYTHONPATH including a stub that overrides _config.
    # Simpler: just symlink the real script with adjusted SKILL.md location
    # via a wrapper. But the script uses `Path(__file__).parents[4]` for
    # repo_root. So we copy the script and config into the temp repo.
    script_target = repo / ".claude" / "skills" / "research-pipeline" / "scripts" / "validate-sources.py"
    config_target = repo / ".claude" / "skills" / "research-pipeline" / "scripts" / "_config.py"
    canon_target = repo / ".claude" / "skills" / "research-pipeline" / "scripts" / "url_canonicalize.py"
    src_dir = Path(__file__).resolve().parents[2] / "scripts"
    script_target.write_text((src_dir / "validate-sources.py").read_text())
    config_target.write_text((src_dir / "_config.py").read_text())
    canon_target.write_text((src_dir / "url_canonicalize.py").read_text())
    return subprocess.run(
        [sys.executable, str(script_target)],
        capture_output=True, text=True, env=env,
    )


def _setup_baseline(repo: Path, records: dict | None = None) -> None:
    write_skill_md(repo, default_config_yaml())
    write_schema(repo)
    write_sources_json(repo, records or {})


class TestEmptyData:
    def test_empty_dict_validates(self, tmp_repo):
        _setup_baseline(tmp_repo, {})
        result = _run(tmp_repo)
        assert result.returncode == 0, result.stderr


class TestSingleRecord:
    def test_minimal_record_validates(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/test")
        _setup_baseline(tmp_repo, {
            rid: {"id": rid, "canonical_url": canon, "title": "Test"}
        })
        result = _run(tmp_repo)
        assert result.returncode == 0, result.stderr + result.stdout

    def test_id_mismatch_fails(self, tmp_repo):
        # Use an id that doesn't match the canonical_url's hash
        _setup_baseline(tmp_repo, {
            "0000000000": {
                "id": "0000000000",
                "canonical_url": "https://example.com/test",
                "title": "Test",
            }
        })
        result = _run(tmp_repo)
        assert result.returncode == 1
        assert "doesn't match" in result.stderr

    def test_id_key_mismatch_fails(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/test")
        _setup_baseline(tmp_repo, {
            rid: {
                "id": "9999999999",  # wrong; key is correct
                "canonical_url": canon,
                "title": "Test",
            }
        })
        result = _run(tmp_repo)
        assert result.returncode == 1
        assert "doesn't match map key" in result.stderr

    def test_missing_title_fails(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/test")
        _setup_baseline(tmp_repo, {
            rid: {"id": rid, "canonical_url": canon, "title": ""}
        })
        result = _run(tmp_repo)
        assert result.returncode == 1


class TestPointerTo:
    def test_pointer_to_existing_record(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        c1, r1 = canonicalize_and_id("https://example.com/old")
        c2, r2 = canonicalize_and_id("https://example.com/new")
        _setup_baseline(tmp_repo, {
            r1: {"id": r1, "canonical_url": c1, "title": "Old", "pointer_to": r2},
            r2: {"id": r2, "canonical_url": c2, "title": "New"},
        })
        result = _run(tmp_repo)
        assert result.returncode == 0, result.stderr + result.stdout

    def test_pointer_to_missing_target_fails(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        c1, r1 = canonicalize_and_id("https://example.com/old")
        _setup_baseline(tmp_repo, {
            r1: {"id": r1, "canonical_url": c1, "title": "Old", "pointer_to": "ffffffffff"},
        })
        result = _run(tmp_repo)
        assert result.returncode == 1
        assert "doesn't exist" in result.stderr

    def test_self_pointer_fails(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        c1, r1 = canonicalize_and_id("https://example.com/x")
        _setup_baseline(tmp_repo, {
            r1: {"id": r1, "canonical_url": c1, "title": "X", "pointer_to": r1},
        })
        result = _run(tmp_repo)
        assert result.returncode == 1
        assert "points to itself" in result.stderr

    def test_circular_pointer_fails(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        c1, r1 = canonicalize_and_id("https://example.com/a")
        c2, r2 = canonicalize_and_id("https://example.com/b")
        _setup_baseline(tmp_repo, {
            r1: {"id": r1, "canonical_url": c1, "title": "A", "pointer_to": r2},
            r2: {"id": r2, "canonical_url": c2, "title": "B", "pointer_to": r1},
        })
        result = _run(tmp_repo)
        assert result.returncode == 1
        assert "circular" in result.stderr


class TestFiles:
    def test_filename_with_path_separator_fails(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/test")
        _setup_baseline(tmp_repo, {
            rid: {
                "id": rid, "canonical_url": canon, "title": "Test",
                "files": [{
                    "format": "html",
                    "filename": "subdir/foo.html",  # invalid: contains /
                    "ingestion_status": "want",
                }]
            }
        })
        result = _run(tmp_repo)
        assert result.returncode == 1
        assert "path separator" in result.stderr

    def test_have_file_missing_on_disk_fails(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/test")
        _setup_baseline(tmp_repo, {
            rid: {
                "id": rid, "canonical_url": canon, "title": "Test",
                "files": [{
                    "format": "html",
                    "filename": "main.html",
                    "ingestion_status": "have",
                }]
            }
        })
        # Don't actually create the file
        result = _run(tmp_repo)
        assert result.returncode == 1
        assert "not on disk" in result.stderr

    def test_have_file_with_sha_mismatch_fails(self, tmp_repo):
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/test")
        _setup_baseline(tmp_repo, {
            rid: {
                "id": rid, "canonical_url": canon, "title": "Test",
                "files": [{
                    "format": "html",
                    "filename": "main.html",
                    "ingestion_status": "have",
                    "sha256": "f" * 64,  # bogus
                }]
            }
        })
        # Create the file with different content
        target = tmp_repo / "reference-only" / rid / "main.html"
        target.parent.mkdir(parents=True)
        target.write_text("<html></html>")
        result = _run(tmp_repo)
        assert result.returncode == 1
        assert "sha256 mismatch" in result.stderr


class TestOrdering:
    def test_unsorted_keys_warns_not_errors(self, tmp_repo):
        # Write a sources.json that's deliberately out-of-order
        from url_canonicalize import canonicalize_and_id
        c1, r1 = canonicalize_and_id("https://example.com/aaa")  # likely later alpha
        c2, r2 = canonicalize_and_id("https://example.com/bbb")
        if r1 >= r2:
            r1, r2 = r2, r1
            c1, c2 = c2, c1
        # Write in REVERSE order: r2 first, r1 second
        data = {
            r2: {"id": r2, "canonical_url": c2, "title": "B"},
            r1: {"id": r1, "canonical_url": c1, "title": "A"},
        }
        write_skill_md(tmp_repo, default_config_yaml())
        write_schema(tmp_repo)
        # Write raw to preserve key order
        (tmp_repo / "reference-only" / "sources.json").write_text(
            json.dumps(data, indent=2), encoding="utf-8"
        )
        result = _run(tmp_repo)
        # Should warn (exit 2) not error (exit 1)
        assert result.returncode in (0, 2), result.stderr
