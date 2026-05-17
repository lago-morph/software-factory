"""Integration tests for render-sources-md.sh.

Renders the markdown view from various fixture catalogs and asserts
section presence + content patterns.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from tests.conftest import write_skill_md, default_config_yaml, write_sources_json


REPO_ROOT = Path(__file__).resolve().parents[5]
RENDER = REPO_ROOT / ".claude" / "skills" / "research-pipeline" / "scripts" / "render-sources-md.sh"


def _setup_repo_with_render(tmp_path: Path) -> Path:
    """Build a temp repo and copy in the render script."""
    skill_dir = tmp_path / ".claude" / "skills" / "research-pipeline" / "scripts"
    skill_dir.mkdir(parents=True)
    (tmp_path / "reference-only").mkdir()
    write_skill_md(tmp_path, default_config_yaml())
    # Copy render script
    target = skill_dir / "render-sources-md.sh"
    target.write_bytes(RENDER.read_bytes())
    target.chmod(0o755)
    return tmp_path


def _render(repo: Path) -> str:
    result = subprocess.run(
        ["bash", str(repo / ".claude/skills/research-pipeline/scripts/render-sources-md.sh")],
        capture_output=True, text=True, cwd=str(repo),
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


@pytest.mark.integration
class TestRenderMarkdown:
    def test_empty_catalog(self, tmp_path):
        repo = _setup_repo_with_render(tmp_path)
        write_sources_json(repo, {})
        md = _render(repo)
        assert "§ 1 — Complete *(0 records)*" in md
        assert "§ 2 — Partial *(0 records)*" in md
        assert "§ 3a — Wanted (URL known) *(0 records)*" in md
        assert "§ 3b — Wanted (title only) *(0 records)*" in md
        assert "§ 4 — Superseded *(0 records)*" in md

    def test_complete_record_in_section_1(self, tmp_path):
        repo = _setup_repo_with_render(tmp_path)
        write_sources_json(repo, {
            "0a7f3b8e00": {
                "id": "0a7f3b8e00",
                "canonical_url": "https://example.com/x",
                "title": "Complete Test",
                "files": [{
                    "format": "html", "filename": "m.html",
                    "ingestion_status": "have", "completeness": "complete",
                }]
            }
        })
        md = _render(repo)
        # Title in § 1
        assert "Complete Test" in md
        assert "§ 1 — Complete *(1 records)*" in md
        # Anchor present
        assert 'id="0a7f3b8e00"' in md

    def test_partial_record_in_section_2(self, tmp_path):
        repo = _setup_repo_with_render(tmp_path)
        write_sources_json(repo, {
            "0000000000": {
                "id": "0000000000",
                "canonical_url": "https://example.com/x",
                "title": "Partial Test",
                "files": [
                    {"format": "html", "filename": "m.html",
                     "ingestion_status": "have", "completeness": "complete"},
                    {"format": "pdf", "ingestion_status": "want"},
                ]
            }
        })
        md = _render(repo)
        assert "§ 2 — Partial *(1 records)*" in md
        # html ✓ and pdf (want) in same chip line
        assert "html ✓" in md
        assert "pdf (want)" in md

    def test_wanted_url_known_in_section_3a(self, tmp_path):
        repo = _setup_repo_with_render(tmp_path)
        write_sources_json(repo, {
            "0000000000": {
                "id": "0000000000",
                "canonical_url": "https://example.com/wanted",
                "title": "Wanted Source",
                "files": []
            }
        })
        md = _render(repo)
        assert "§ 3a — Wanted (URL known) *(1 records)*" in md

    def test_wanted_title_only_in_section_3b(self, tmp_path):
        repo = _setup_repo_with_render(tmp_path)
        write_sources_json(repo, {
            "0000000000": {
                "id": "0000000000",
                "title": "Title Only Source",
                "files": []
            }
        })
        md = _render(repo)
        assert "§ 3b — Wanted (title only) *(1 records)*" in md

    def test_superseded_record_stub(self, tmp_path):
        repo = _setup_repo_with_render(tmp_path)
        write_sources_json(repo, {
            "0000000000": {
                "id": "0000000000",
                "title": "Old Source",
                "pointer_to": "1111111111",
            },
            "1111111111": {
                "id": "1111111111",
                "canonical_url": "https://example.com/new",
                "title": "New Source",
            }
        })
        md = _render(repo)
        assert "§ 4 — Superseded *(1 records)*" in md
        # Stub format
        assert "~~Old Source~~" in md
        assert "1111111111" in md
