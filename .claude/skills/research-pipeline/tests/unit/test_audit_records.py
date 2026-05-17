"""Unit tests for audit-records.py.

Each test sets up a minimal repo with a sources.json containing one or two
records, then runs the script as a subprocess and asserts on findings.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tests.conftest import (
    write_skill_md, default_config_yaml, write_sources_json, write_schema,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPT_FILES = [
    "_config.py", "url_canonicalize.py", "audit-records.py", "youtube_urls.py",
]


def _setup_repo(tmp_path: Path, records: dict) -> Path:
    skill_dir = tmp_path / ".claude" / "skills" / "research-pipeline" / "scripts"
    skill_dir.mkdir(parents=True)
    (tmp_path / "reference-only").mkdir()
    write_skill_md(tmp_path, default_config_yaml())
    write_schema(tmp_path)
    write_sources_json(tmp_path, records)
    src_dir = REPO_ROOT / ".claude/skills/research-pipeline/scripts"
    for name in SCRIPT_FILES:
        (skill_dir / name).write_bytes((src_dir / name).read_bytes())
    return tmp_path


def _run(repo: Path, *args) -> subprocess.CompletedProcess:
    script = repo / ".claude/skills/research-pipeline/scripts/audit-records.py"
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True, text=True, cwd=str(repo),
    )


def _make_complete_record(rid: str, url: str, title: str = "A Real Title") -> dict:
    return {
        "id": rid,
        "canonical_url": url,
        "title": title,
        "tags": ["dark-factory"],
        "files": [
            {
                "format": "html",
                "filename": "page.html",
                "sha256": "0" * 64,  # caller can override
                "ingestion_status": "want",
                "completeness": "unknown",
            }
        ],
    }


# Use a real URL whose id we can compute.
URL_A = "https://example.com/a"
ID_A = hashlib.sha256(URL_A.encode("utf-8")).hexdigest()[:10]


class TestCleanRecord:
    def test_minimal_clean_record_passes(self, tmp_path):
        repo = _setup_repo(tmp_path, {
            ID_A: _make_complete_record(ID_A, URL_A),
        })
        result = _run(repo, ID_A)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "audit clean" in result.stdout

    def test_all_mode_walks_every_record(self, tmp_path):
        repo = _setup_repo(tmp_path, {
            ID_A: _make_complete_record(ID_A, URL_A),
        })
        result = _run(repo, "--all")
        assert result.returncode == 0
        assert "1 record(s) checked" in result.stdout


class TestTitleCheck:
    def test_unknown_title_is_flagged(self, tmp_path):
        rec = _make_complete_record(ID_A, URL_A, title="(unknown)")
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 1
        assert "title-not-placeholder" in result.stdout

    def test_empty_title_is_flagged(self, tmp_path):
        # Schema requires title; minLength=1. We bypass schema here by
        # writing the catalog directly — audit must still detect it.
        rec = _make_complete_record(ID_A, URL_A)
        rec["title"] = " "  # whitespace only
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 1
        assert "title-not-placeholder" in result.stdout


class TestCategoryTagCheck:
    def test_no_canonical_tag_flagged(self, tmp_path):
        rec = _make_complete_record(ID_A, URL_A)
        rec["tags"] = ["not-a-canonical-category"]
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 1
        assert "has-category-tag" in result.stdout

    def test_canonical_tag_passes(self, tmp_path):
        rec = _make_complete_record(ID_A, URL_A)
        rec["tags"] = ["random-other", "spec-authorship"]
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 0


class TestIdDerivation:
    def test_wrong_id_for_url_flagged(self, tmp_path):
        # Use ID_A as the map key but set canonical_url to something else,
        # producing an id mismatch.
        rec = _make_complete_record(ID_A, "https://example.com/different")
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 1
        assert "id-derivation" in result.stdout


class TestUrlIsCanonical:
    def test_non_canonical_url_flagged(self, tmp_path):
        rec = _make_complete_record(ID_A, URL_A + "?utm_source=foo")
        # The id won't match the noisy URL — but the canonical-form check
        # still fires on the noisy URL itself.
        rid = hashlib.sha256((URL_A + "?utm_source=foo").encode()).hexdigest()[:10]
        rec["id"] = rid
        repo = _setup_repo(tmp_path, {rid: rec})
        result = _run(repo, rid)
        assert result.returncode == 1
        assert "url-is-canonical" in result.stdout


class TestPointerChain:
    def test_pointer_to_missing_target(self, tmp_path):
        rec = {"id": ID_A, "title": "x", "pointer_to": "deadbeef00"}
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 1
        assert "pointer-chain-ok" in result.stdout

    def test_pointer_chain_too_deep(self, tmp_path):
        # A -> B -> C: auditing A should fail because B is itself a pointer
        url_b = "https://example.com/b"
        id_b = hashlib.sha256(url_b.encode()).hexdigest()[:10]
        url_c = "https://example.com/c"
        id_c = hashlib.sha256(url_c.encode()).hexdigest()[:10]
        records = {
            ID_A: {"id": ID_A, "title": "a", "pointer_to": id_b},
            id_b: {"id": id_b, "title": "b", "pointer_to": id_c},
            id_c: _make_complete_record(id_c, url_c),
        }
        repo = _setup_repo(tmp_path, records)
        result = _run(repo, ID_A)
        assert result.returncode == 1
        assert "pointer-chain-ok" in result.stdout


class TestFileOnDisk:
    def test_have_file_missing_on_disk_flagged(self, tmp_path):
        rec = _make_complete_record(ID_A, URL_A)
        rec["files"][0]["ingestion_status"] = "have"
        rec["files"][0]["sha256"] = hashlib.sha256(b"x").hexdigest()
        # Don't create the file on disk
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 1
        assert "file-on-disk" in result.stdout

    def test_have_file_present_passes(self, tmp_path):
        rec = _make_complete_record(ID_A, URL_A)
        content = b"<html>hello</html>"
        rec["files"][0]["ingestion_status"] = "have"
        rec["files"][0]["sha256"] = hashlib.sha256(content).hexdigest()
        repo = _setup_repo(tmp_path, {ID_A: rec})
        (repo / "reference-only" / ID_A).mkdir(exist_ok=True)
        (repo / "reference-only" / ID_A / "page.html").write_bytes(content)
        result = _run(repo, ID_A)
        assert result.returncode == 0, result.stdout

    def test_sha_mismatch_flagged(self, tmp_path):
        rec = _make_complete_record(ID_A, URL_A)
        rec["files"][0]["ingestion_status"] = "have"
        rec["files"][0]["sha256"] = "f" * 64  # wrong
        repo = _setup_repo(tmp_path, {ID_A: rec})
        (repo / "reference-only" / ID_A).mkdir(exist_ok=True)
        (repo / "reference-only" / ID_A / "page.html").write_text("hello")
        result = _run(repo, ID_A)
        assert result.returncode == 1
        assert "file-sha256-matches" in result.stdout


class TestFormatExtension:
    def test_format_mismatch_flagged(self, tmp_path):
        rec = _make_complete_record(ID_A, URL_A)
        rec["files"][0]["format"] = "pdf"
        rec["files"][0]["filename"] = "page.html"  # extension mismatch
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 1
        assert "format-matches-extension" in result.stdout


class TestImageSummary:
    def test_image_without_comment_flagged(self, tmp_path):
        rec = _make_complete_record(ID_A, URL_A)
        rec["files"] = [{
            "format": "image/png",
            "filename": "fig.png",
            "sha256": hashlib.sha256(b"\x89PNG\r\n\x1a\n").hexdigest(),
            "ingestion_status": "have",
            "completeness": "complete",
        }]
        repo = _setup_repo(tmp_path, {ID_A: rec})
        (repo / "reference-only" / ID_A).mkdir(exist_ok=True)
        (repo / "reference-only" / ID_A / "fig.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        result = _run(repo, ID_A)
        assert result.returncode == 1
        assert "image-has-summary" in result.stdout

    def test_image_with_comment_passes(self, tmp_path):
        rec = _make_complete_record(ID_A, URL_A)
        content = b"\x89PNG\r\n\x1a\n"
        rec["files"] = [{
            "format": "image/png",
            "filename": "fig.png",
            "sha256": hashlib.sha256(content).hexdigest(),
            "ingestion_status": "have",
            "completeness": "complete",
            "comment": "a diagram showing X",
        }]
        repo = _setup_repo(tmp_path, {ID_A: rec})
        (repo / "reference-only" / ID_A).mkdir(exist_ok=True)
        (repo / "reference-only" / ID_A / "fig.png").write_bytes(content)
        result = _run(repo, ID_A)
        assert result.returncode == 0, result.stdout


class TestPointerStubsSkipMostChecks:
    """Pointer records are stubs by design — only the chain check runs."""
    def test_pointer_with_clean_target_passes(self, tmp_path):
        url_b = "https://example.com/b"
        id_b = hashlib.sha256(url_b.encode()).hexdigest()[:10]
        records = {
            ID_A: {"id": ID_A, "title": "x", "pointer_to": id_b},
            id_b: _make_complete_record(id_b, url_b),
        }
        repo = _setup_repo(tmp_path, records)
        result = _run(repo, ID_A)
        assert result.returncode == 0, result.stdout


class TestSearchHintsAcceptableWithoutUrl:
    def test_search_hints_record_without_url_passes(self, tmp_path):
        rec = {
            "id": ID_A,
            "title": "Some Title",
            "tags": ["dark-factory"],
            "search_hints": [{"hint": "look on archive.org"}],
            "files": [{"format": "html", "ingestion_status": "want"}],
        }
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 0, result.stdout


class TestJsonOutput:
    def test_json_emits_array(self, tmp_path):
        rec = _make_complete_record(ID_A, URL_A, title="(unknown)")
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A, "--json")
        assert result.returncode == 1
        data = json.loads(result.stdout)
        assert isinstance(data, list)
        assert any(d["check"] == "title-not-placeholder" for d in data)


class TestAlwaysModeFooter:
    def test_always_mode_footer_appended(self, tmp_path):
        rec = _make_complete_record(ID_A, URL_A)
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A, "--always-mode-footer")
        assert result.returncode == 0
        assert "audit_after_ingestion" in result.stdout
        assert "Configure in" in result.stdout

    def test_no_footer_without_flag(self, tmp_path):
        rec = _make_complete_record(ID_A, URL_A)
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 0
        assert "audit_after_ingestion" not in result.stdout


class TestInvalidIdInput:
    def test_unknown_record_id_errors(self, tmp_path):
        repo = _setup_repo(tmp_path, {})
        result = _run(repo, "0000000000")
        assert result.returncode == 2
        assert "no such record" in result.stderr

    def test_malformed_id_errors(self, tmp_path):
        repo = _setup_repo(tmp_path, {})
        result = _run(repo, "not-an-id")
        assert result.returncode == 2
        assert "not a valid 10-hex id" in result.stderr

    def test_no_args_errors(self, tmp_path):
        repo = _setup_repo(tmp_path, {})
        result = _run(repo)
        assert result.returncode == 2


# ---------------- YouTube transcript checks ----------------

VIDEO_ID = "dQw4w9WgXcQ"
VIDEO_URL = f"https://www.youtube.com/watch?v={VIDEO_ID}"


def _record_with_transcript(rid: str, url: str, *, transcript_file_entry: dict,
                            transcript_content: str | None,
                            repo: Path | None) -> dict:
    """Build a record with a transcript file entry. If transcript_content is
    given, write the file to disk so file-on-disk + sha256 checks pass."""
    rec = {
        "id": rid,
        "canonical_url": url,
        "title": "An Embedding Document",
        "tags": ["dark-factory"],
        "files": [transcript_file_entry],
    }
    if transcript_content is not None and repo is not None:
        d = repo / "reference-only" / rid
        d.mkdir(parents=True, exist_ok=True)
        fname = transcript_file_entry["filename"]
        (d / fname).write_text(transcript_content, encoding="utf-8")
        transcript_file_entry["sha256"] = hashlib.sha256(
            transcript_content.encode("utf-8")
        ).hexdigest()
    return rec


class TestYoutubeTranscript:
    def test_wanted_transcript_with_url_passes(self, tmp_path):
        entry = {
            "format": "youtube-transcript",
            "filename": None,
            "ingestion_status": "want",
            "youtube_url": VIDEO_URL,
        }
        rec = {
            "id": ID_A, "canonical_url": URL_A, "title": "Doc",
            "tags": ["dark-factory"], "files": [entry],
        }
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 0, result.stdout

    def test_transcript_without_youtube_url_is_flagged(self, tmp_path):
        entry = {
            "format": "youtube-transcript",
            "filename": "t.txt",
            "sha256": "0" * 64,
            "ingestion_status": "have",
        }
        rec = {
            "id": ID_A, "canonical_url": URL_A, "title": "Doc",
            "tags": ["dark-factory"], "files": [entry],
        }
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 1
        assert "youtube-url-required-when-transcript" in result.stdout

    def test_non_canonical_youtube_url_is_flagged(self, tmp_path):
        entry = {
            "format": "youtube-transcript",
            "filename": None,
            "ingestion_status": "want",
            "youtube_url": f"https://youtu.be/{VIDEO_ID}",
        }
        rec = {
            "id": ID_A, "canonical_url": URL_A, "title": "Doc",
            "tags": ["dark-factory"], "files": [entry],
        }
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 1
        assert "youtube-url-required-when-transcript" in result.stdout

    def test_youtube_url_on_non_transcript_is_flagged(self, tmp_path):
        # We have to write this directly via dict — the schema would reject
        # it at validate-sources time, but audit must catch it too.
        entry = {
            "format": "html",
            "filename": "page.html",
            "sha256": "0" * 64,
            "ingestion_status": "want",
            "youtube_url": VIDEO_URL,
        }
        rec = {
            "id": ID_A, "canonical_url": URL_A, "title": "Doc",
            "tags": ["dark-factory"], "files": [entry],
        }
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        assert result.returncode == 1
        assert "youtube-url-only-on-transcript" in result.stdout

    def test_have_transcript_content_matches_passes(self, tmp_path):
        entry = {
            "format": "youtube-transcript",
            "filename": "transcript.txt",
            "ingestion_status": "have",
            "completeness": "unknown",
            "youtube_url": VIDEO_URL,
        }
        content = VIDEO_URL + "\n\n[0:00] hello world\n"
        repo_root = _setup_repo(tmp_path, {})
        rec = _record_with_transcript(
            ID_A, URL_A, transcript_file_entry=entry,
            transcript_content=content, repo=repo_root,
        )
        write_sources_json(repo_root, {ID_A: rec})
        result = _run(repo_root, ID_A)
        assert result.returncode == 0, result.stdout

    def test_have_transcript_wrong_first_line_is_flagged(self, tmp_path):
        entry = {
            "format": "youtube-transcript",
            "filename": "transcript.txt",
            "ingestion_status": "have",
            "completeness": "unknown",
            "youtube_url": VIDEO_URL,
        }
        # First line is a different URL
        content = f"https://www.youtube.com/watch?v=other_video1\nbody\n"
        repo_root = _setup_repo(tmp_path, {})
        rec = _record_with_transcript(
            ID_A, URL_A, transcript_file_entry=entry,
            transcript_content=content, repo=repo_root,
        )
        write_sources_json(repo_root, {ID_A: rec})
        result = _run(repo_root, ID_A)
        assert result.returncode == 1
        assert "youtube-transcript-content-matches" in result.stdout

    def test_have_transcript_no_first_line_url_is_flagged(self, tmp_path):
        entry = {
            "format": "youtube-transcript",
            "filename": "transcript.txt",
            "ingestion_status": "have",
            "completeness": "unknown",
            "youtube_url": VIDEO_URL,
        }
        content = "TITLE: A talk\nbody only, no url\n"
        repo_root = _setup_repo(tmp_path, {})
        rec = _record_with_transcript(
            ID_A, URL_A, transcript_file_entry=entry,
            transcript_content=content, repo=repo_root,
        )
        write_sources_json(repo_root, {ID_A: rec})
        result = _run(repo_root, ID_A)
        assert result.returncode == 1
        assert "youtube-transcript-content-matches" in result.stdout

    def test_transcript_format_matches_txt_extension(self, tmp_path):
        # format-matches-extension must accept .txt for youtube-transcript.
        entry = {
            "format": "youtube-transcript",
            "filename": "t.txt",
            "ingestion_status": "want",
            "youtube_url": VIDEO_URL,
        }
        rec = {
            "id": ID_A, "canonical_url": URL_A, "title": "Doc",
            "tags": ["dark-factory"], "files": [entry],
        }
        repo = _setup_repo(tmp_path, {ID_A: rec})
        result = _run(repo, ID_A)
        # Want entry without on-disk file → no file-on-disk check fires.
        assert "format-matches-extension" not in result.stdout
