"""Shared test fixtures and path setup.

Adds the scripts/ directory to sys.path so tests can `import url_canonicalize`
etc. directly. Also provides helpers for building fixture catalogs and
sandbox directories.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pytest

# Make scripts/ importable as flat modules
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    """A fake repo structure with .claude/skills/research-pipeline/ layout.

    Returns the temp repo root. The caller can write a SKILL.md, sources.json,
    schema, and reference-only/<id>/ trees inside it.
    """
    # Create skill dir + scripts dir (empty — we don't copy actual scripts)
    skill_dir = tmp_path / ".claude" / "skills" / "research-pipeline"
    (skill_dir / "scripts").mkdir(parents=True)
    (skill_dir / "resources" / "_workflows").mkdir(parents=True)
    (tmp_path / "reference-only").mkdir()
    (tmp_path / "research").mkdir()
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    return tmp_path


def write_skill_md(repo: Path, config_yaml: str) -> Path:
    """Write a minimal SKILL.md with the given YAML config block."""
    skill_md = repo / ".claude" / "skills" / "research-pipeline" / "SKILL.md"
    skill_md.write_text(
        "---\nname: research-pipeline\n---\n\n"
        "# Test SKILL.md\n\n"
        "<!-- BEGIN PIPELINE CONFIG -->\n"
        "```yaml\n"
        + config_yaml.strip() + "\n"
        "```\n"
        "<!-- END PIPELINE CONFIG -->\n",
        encoding="utf-8",
    )
    return skill_md


def default_config_yaml(repo: Path | None = None) -> str:
    """Standard config block. repo is unused but kept for API symmetry."""
    return """
skill_path:   .claude/skills/research-pipeline
library_path: reference-only
schema_path:  reference-only/sources.schema.json
data_path:    reference-only/sources.json
md_path:      reference-only/sources.md
trigger_path: reference-only/.regen-trigger
report_paths:
  - research
ingestion_paths:
  - research/manual
github:
  owner: test-owner
  repo:  test-repo
  fetch_branch_prefix: fetched/issue-
  fetch_issue_label:   fetch-urls
"""


def write_sources_json(repo: Path, data: dict[str, Any]) -> Path:
    """Write a sources.json with the given record map."""
    p = repo / "reference-only" / "sources.json"
    p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return p


def write_schema(repo: Path) -> Path:
    """Write the actual sources.schema.json into the temp repo."""
    real_schema = Path(__file__).resolve().parents[3] / "reference-only" / "sources.schema.json"
    target = repo / "reference-only" / "sources.schema.json"
    if real_schema.exists():
        target.write_text(real_schema.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        # Fallback minimal schema (shouldn't happen in normal test runs)
        target.write_text('{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}', encoding="utf-8")
    return target


def write_file_with_sha(path: Path, content: str | bytes) -> str:
    """Write a file and return its sha256 (so test data and record agree)."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return hashlib.sha256(content).hexdigest()


def make_minimal_record(rid: str, url: str = None, title: str = "Test", files: list = None) -> dict:
    """Build a minimal valid record."""
    rec = {"id": rid, "title": title}
    if url is not None:
        rec["canonical_url"] = url
    if files is not None:
        rec["files"] = files
    return rec
