"""Regression test: the canonical normalizer is THE single source of truth
for sources.json's on-disk shape. drain.py's Python `normalize_and_write`
and the `normalize-sources-json.sh` shell helper (which runs `jq -S '.'`)
must produce byte-identical output for any input.

If this test fails, one of three places drifted:
  - scripts/drain.py::normalize_and_write
  - scripts/normalize-sources-json.sh
  - the jq version installed in the test environment

The fix is always to bring the Python path into byte-agreement with jq's
output (jq is the reference; the workflow + hand-edits use it), not the
other way around.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT_DIR = Path(__file__).resolve().parents[2] / "scripts"
SH = SCRIPT_DIR / "normalize-sources-json.sh"

# Import normalize_and_write directly from drain.py.
sys.path.insert(0, str(SCRIPT_DIR))
from drain import normalize_and_write  # noqa: E402


def _have_jq() -> bool:
    return shutil.which("jq") is not None


pytestmark = pytest.mark.skipif(not _have_jq(), reason="jq not installed")


@pytest.fixture
def fixtures() -> list[dict]:
    """A spread of catalog shapes that exercise sort_keys, nested arrays,
    unicode, pointer_to fields, transcript wants, and missing fields."""
    return [
        # Single record, keys in non-alphabetical order to stress sort.
        {"abc1234567": {
            "title": "Z then A",
            "canonical_url": "https://example.com/x",
            "id": "abc1234567",
            "files": [],
        }},
        # Multiple records, top-level keys not sorted.
        {
            "zzz9999999": {"id": "zzz9999999", "canonical_url": "https://z.example/", "files": []},
            "aaa0000000": {"id": "aaa0000000", "canonical_url": "https://a.example/", "files": []},
            "mmm5555555": {"id": "mmm5555555", "canonical_url": "https://m.example/", "files": []},
        },
        # Unicode in title.
        {"u1": {
            "id": "u1",
            "canonical_url": "https://example.com/u",
            "title": "Hamel Husain’s Blog – with em-dash",
            "files": [],
        }},
        # Nested structures: files array, tags array, pointer_to.
        {"r1": {
            "id": "r1",
            "canonical_url": "https://example.com/r",
            "title": "Article",
            "tags": ["evals-and-benchmarks", "security-primitives"],
            "files": [
                {"format": "mhtml", "filename": "page.mhtml",
                 "sha256": "deadbeef" * 8, "ingestion_status": "have",
                 "completeness": "unknown"},
                {"format": "html", "ingestion_status": "want", "filename": None},
            ],
            "pointer_to": "r2",
            "short_summary": "summary",
        }},
        # YouTube transcript wants with nested keys.
        {"yt1": {
            "id": "yt1",
            "canonical_url": "https://example.com/post",
            "title": "Post with embed",
            "files": [
                {"format": "youtube-transcript", "ingestion_status": "want",
                 "filename": None,
                 "youtube_url": "https://youtu.be/abc123"},
            ],
        }},
        # Empty catalog.
        {},
    ]


def _via_jq(data: dict, tmp_path: Path) -> bytes:
    p = tmp_path / "in.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    subprocess.run(["bash", str(SH), str(p)], check=True, capture_output=True)
    return p.read_bytes()


def _via_python(data: dict, tmp_path: Path) -> bytes:
    p = tmp_path / "in.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    normalize_and_write(data, p)
    return p.read_bytes()


def test_byte_equivalence_for_all_fixtures(fixtures, tmp_path):
    for i, data in enumerate(fixtures):
        jq_dir = tmp_path / f"case{i}-jq"
        py_dir = tmp_path / f"case{i}-py"
        jq_dir.mkdir()
        py_dir.mkdir()
        jq_bytes = _via_jq(data, jq_dir)
        py_bytes = _via_python(data, py_dir)
        assert jq_bytes == py_bytes, (
            f"fixture {i} diverged:\n"
            f"=== jq ===\n{jq_bytes.decode('utf-8', 'replace')}\n"
            f"=== py ===\n{py_bytes.decode('utf-8', 'replace')}"
        )


def test_normalize_is_idempotent(fixtures, tmp_path):
    """Running the normalizer twice produces the same bytes as running it once."""
    for i, data in enumerate(fixtures):
        case_dir = tmp_path / f"idem{i}"
        case_dir.mkdir()
        p = case_dir / "x.json"
        p.write_text(json.dumps(data), encoding="utf-8")
        subprocess.run(["bash", str(SH), str(p)], check=True, capture_output=True)
        once = p.read_bytes()
        subprocess.run(["bash", str(SH), str(p)], check=True, capture_output=True)
        twice = p.read_bytes()
        assert once == twice, f"fixture {i} not idempotent under normalize-sources-json.sh"


def test_real_catalog_is_canonical():
    """The committed reference-only/sources.json is byte-identical to what
    the helper script would produce — i.e., it's currently in canonical
    form. This catches any future commit that bypasses the normalizer."""
    # tests/unit/test_x.py → parents: [unit, tests, research-pipeline, skills, .claude, REPO]
    repo_root = Path(__file__).resolve().parents[5]
    catalog = repo_root / "reference-only" / "sources.json"
    if not catalog.exists():
        pytest.skip("real catalog not present in this checkout")
    expected = subprocess.run(
        ["jq", "-S", ".", str(catalog)], capture_output=True, check=True,
    ).stdout
    actual = catalog.read_bytes()
    assert actual == expected, (
        "reference-only/sources.json is NOT in canonical form. "
        f"Run: bash {SH} {catalog}"
    )
