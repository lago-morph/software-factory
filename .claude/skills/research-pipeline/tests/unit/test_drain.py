"""Unit tests for drain.py."""

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
SCRIPT_FILES = [
    "_config.py", "url_canonicalize.py", "extract_url.py", "extract_title.py",
    "classify_text.py",
    "validate-sources.py", "validate-config.py",
    "check-source-refs.py", "check-source-dirs.py",
    "check-fetch-provenance.py", "sanity-check-record.py",
    "audit-records.py", "lint-sources.sh", "drain.py", "youtube_urls.py",
]


def _setup_repo(tmp_path: Path) -> Path:
    """Build a temp repo with scripts."""
    skill_dir = tmp_path / ".claude" / "skills" / "research-pipeline" / "scripts"
    skill_dir.mkdir(parents=True)
    (tmp_path / "reference-only").mkdir()
    (tmp_path / "research" / "manual").mkdir(parents=True)
    (tmp_path / "research" / "fetched").mkdir()
    write_skill_md(tmp_path, default_config_yaml())
    write_schema(tmp_path)
    write_sources_json(tmp_path, {})
    src_dir = REPO_ROOT / ".claude/skills/research-pipeline/scripts"
    for name in SCRIPT_FILES:
        src = src_dir / name
        if src.exists():
            dst = skill_dir / name
            dst.write_bytes(src.read_bytes())
            if name.endswith(".sh"):
                dst.chmod(0o755)
    # Init git so git mv works
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@test"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=tmp_path, check=True)
    return tmp_path


def _run_drain(repo: Path, *args) -> subprocess.CompletedProcess:
    script = repo / ".claude/skills/research-pipeline/scripts/drain.py"
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True, text=True, cwd=str(repo),
    )


class TestDrainNoCandidates:
    def test_empty_drops_passes(self, tmp_path):
        repo = _setup_repo(tmp_path)
        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0
        assert "0 candidate file(s)" in result.stderr


class TestDrainUrlList:
    def test_url_list_creates_wanted_records(self, tmp_path):
        repo = _setup_repo(tmp_path)
        url_file = repo / "research" / "manual" / "urls.txt"
        url_file.write_text("https://example.com/a\nhttps://example.com/b\n")
        subprocess.run(["git", "add", str(url_file)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0, result.stderr
        data = json.loads((repo / "reference-only" / "sources.json").read_text())
        assert len(data) == 2
        # URL file should be deleted
        assert not url_file.exists()


class TestDrainNewSource:
    def test_extractable_url_creates_new_record(self, tmp_path):
        repo = _setup_repo(tmp_path)
        f = repo / "research" / "manual" / "test.html"
        f.write_text(
            '<html><head><link rel="canonical" href="https://example.com/test">'
            '<title>Test Page</title></head><body>content</body></html>'
        )
        subprocess.run(["git", "add", str(f)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0, result.stderr
        data = json.loads((repo / "reference-only" / "sources.json").read_text())
        assert len(data) == 1
        record = next(iter(data.values()))
        assert record["canonical_url"] == "https://example.com/test"
        assert len(record["files"]) == 1
        assert record["files"][0]["filename"] == "test.html"
        # File should be moved to reference-only/<id>/
        assert (repo / "reference-only" / record["id"] / "test.html").exists()
        assert not f.exists()


class TestDrainNoUrlFlag:
    def test_no_url_in_drop_dir_flagged(self, tmp_path):
        repo = _setup_repo(tmp_path)
        # HTML file with no canonical URL anywhere
        f = repo / "research" / "manual" / "anonymous.html"
        f.write_text("<html><body>no url here</body></html>")
        subprocess.run(["git", "add", str(f)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0
        assert "Flagged files" in result.stdout
        # File should stay where it was
        assert f.exists()


class TestDrainDeduplicates:
    def test_sha_match_skips_already_registered(self, tmp_path):
        repo = _setup_repo(tmp_path)
        # Set up an existing record with a file
        rid = "0000000000"
        existing_dir = repo / "reference-only" / rid
        existing_dir.mkdir()
        content = "<html><body>x</body></html>"
        existing_path = existing_dir / "main.html"
        existing_path.write_text(content)
        import hashlib
        sha = hashlib.sha256(content.encode()).hexdigest()
        # Pre-existing record points to this file
        # But the id doesn't match — we need a real URL/id pair
        # Skip the registration check; just verify dup detection by content
        # The real test: when a file in drop dir has the same content AS something
        # that would be added, the drain should detect the existing record's file.

        # Better test: drop a file that triggers the SAME record we already have
        # via URL extraction.
        from url_canonicalize import canonicalize_and_id
        canon, real_rid = canonicalize_and_id("https://example.com/x")
        real_dir = repo / "reference-only" / real_rid
        real_dir.mkdir()
        existing_content = (
            '<html><head><link rel="canonical" href="https://example.com/x">'
            '<title>X</title></head><body>existing</body></html>'
        )
        (real_dir / "page.html").write_text(existing_content)
        existing_sha = hashlib.sha256(existing_content.encode()).hexdigest()
        write_sources_json(repo, {
            real_rid: {
                "id": real_rid, "canonical_url": canon, "title": "X",
                "files": [{
                    "format": "html", "filename": "page.html",
                    "sha256": existing_sha, "ingestion_status": "have",
                    "completeness": "complete",
                }]
            }
        })
        # Drop a duplicate (same content) in research/manual/
        dup_file = repo / "research" / "manual" / "dup.html"
        dup_file.write_text(existing_content)
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
        # Skip commit (signing infra interferes in sandbox)
        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0
        # The duplicate file should be deleted from drop dir
        assert not dup_file.exists()
        # The original file should still exist
        assert (real_dir / "page.html").exists()


class TestDrainDryRun:
    def test_dry_run_no_changes(self, tmp_path):
        repo = _setup_repo(tmp_path)
        f = repo / "research" / "manual" / "test.html"
        f.write_text(
            '<html><head><link rel="canonical" href="https://example.com/test"></head>'
            '<body>content</body></html>'
        )
        subprocess.run(["git", "add", str(f)], cwd=repo, check=True)
        result = _run_drain(repo, "--dry-run", "--no-lint")
        assert result.returncode == 0
        # File should still be in original location
        assert f.exists()
        # sources.json should still be empty
        data = json.loads((repo / "reference-only" / "sources.json").read_text())
        assert data == {}


class TestDrainImageInDrop:
    def test_image_in_drop_flagged(self, tmp_path):
        repo = _setup_repo(tmp_path)
        f = repo / "research" / "manual" / "image.png"
        f.write_bytes(b"\x89PNG\r\n\x1a\n")
        subprocess.run(["git", "add", str(f)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0
        # Image stays in drop dir, gets flagged
        assert f.exists()
        assert "image in drop dir" in result.stdout.lower() or "image" in result.stdout.lower()


class TestDrainExtractsTitle:
    def test_html_title_lands_on_new_record(self, tmp_path):
        repo = _setup_repo(tmp_path)
        f = repo / "research" / "manual" / "post.html"
        f.write_text(
            '<html><head><link rel="canonical" href="https://example.com/post">'
            '<title>My Real Title</title></head><body>x</body></html>'
        )
        subprocess.run(["git", "add", str(f)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint", "--audit-mode", "never")
        assert result.returncode == 0, result.stderr
        data = json.loads((repo / "reference-only" / "sources.json").read_text())
        record = next(iter(data.values()))
        assert record["title"] == "My Real Title"

    def test_url_list_records_keep_unknown_title(self, tmp_path):
        # URL lists create wanted records with no file content yet, so the
        # title stays "(unknown)" — audit will flag them, by design.
        repo = _setup_repo(tmp_path)
        url_file = repo / "research" / "manual" / "urls.txt"
        url_file.write_text("https://example.com/x\n")
        subprocess.run(["git", "add", str(url_file)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint", "--audit-mode", "never")
        assert result.returncode == 0
        data = json.loads((repo / "reference-only" / "sources.json").read_text())
        record = next(iter(data.values()))
        assert record["title"] == "(unknown)"


class TestDrainAuditIntegration:
    def test_always_mode_invokes_audit(self, tmp_path):
        repo = _setup_repo(tmp_path)
        f = repo / "research" / "manual" / "post.html"
        f.write_text(
            '<html><head><link rel="canonical" href="https://example.com/post">'
            '<title>T</title></head><body>x</body></html>'
        )
        subprocess.run(["git", "add", str(f)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint", "--audit-mode", "always")
        assert result.returncode == 0
        # Audit section appears in summary
        assert "## Audit" in result.stdout
        assert "audit_after_ingestion" in result.stdout
        # Drain stderr shows the audit ran
        assert "Stage 4b" in result.stderr

    def test_never_mode_skips_audit(self, tmp_path):
        repo = _setup_repo(tmp_path)
        f = repo / "research" / "manual" / "post.html"
        f.write_text(
            '<html><head><link rel="canonical" href="https://example.com/post">'
            '<title>T</title></head><body>x</body></html>'
        )
        subprocess.run(["git", "add", str(f)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint", "--audit-mode", "never")
        assert result.returncode == 0
        assert "Audit skipped" in result.stdout
        # The "always-mode footer" should NOT appear, but the "skipped" note
        # legitimately mentions the config key — check for the footer text instead.
        assert "Configure in" not in result.stdout

    def test_sometimes_mode_skips_url_list_only(self, tmp_path):
        # Only a URL list, no actual file ingestion → "sometimes" skips audit
        repo = _setup_repo(tmp_path)
        url_file = repo / "research" / "manual" / "urls.txt"
        url_file.write_text("https://example.com/x\n")
        subprocess.run(["git", "add", str(url_file)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint", "--audit-mode", "sometimes")
        assert result.returncode == 0
        # Audit didn't run (no material file changes)
        assert "## Audit" not in result.stdout

    def test_no_audit_flag_overrides(self, tmp_path):
        repo = _setup_repo(tmp_path)
        f = repo / "research" / "manual" / "post.html"
        f.write_text(
            '<html><head><link rel="canonical" href="https://example.com/post">'
            '<title>T</title></head><body>x</body></html>'
        )
        subprocess.run(["git", "add", str(f)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint", "--no-audit")
        assert result.returncode == 0
        assert "## Audit" not in result.stdout


# ---------------- YouTube transcript handling ----------------

YT_VID = "dQw4w9WgXcQ"
YT_URL = f"https://www.youtube.com/watch?v={YT_VID}"


class TestDrainYoutubeEmbedSurfaces:
    def test_embed_in_html_appears_as_candidate(self, tmp_path):
        repo = _setup_repo(tmp_path)
        f = repo / "research" / "manual" / "post.html"
        f.write_text(
            '<html><head><link rel="canonical" href="https://example.com/post">'
            '<title>T</title></head>'
            f'<body>Watch this: <a href="https://youtu.be/{YT_VID}">video</a></body></html>'
        )
        subprocess.run(["git", "add", str(f)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0, result.stderr
        assert "YouTube embed candidates" in result.stdout
        assert YT_URL in result.stdout

    def test_existing_transcript_entry_suppresses_candidate(self, tmp_path):
        # Set up an existing record (matching example.com/post id) with a
        # youtube-transcript entry already, so the next drain run's embed
        # scanner should skip it.
        repo = _setup_repo(tmp_path)
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/post")
        sources_p = repo / "reference-only" / "sources.json"
        sources_p.write_text(json.dumps({
            rid: {
                "id": rid,
                "canonical_url": canon,
                "title": "T",
                "files": [
                    # Existing have html file matching the doc
                    # (sha not validated here)
                    {"format": "youtube-transcript", "filename": None,
                     "ingestion_status": "want", "youtube_url": YT_URL},
                ],
            }
        }, indent=2, sort_keys=True))
        f = repo / "research" / "manual" / "post.html"
        f.write_text(
            '<html><head><link rel="canonical" href="https://example.com/post">'
            '<title>T</title></head>'
            f'<body>Watch this: <a href="https://youtu.be/{YT_VID}">video</a></body></html>'
        )
        subprocess.run(["git", "add", str(f)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0, result.stderr
        # Embed is already covered → candidates count is 0 and no
        # section header is rendered.
        assert "## YouTube embed candidates" not in result.stdout


class TestDrainTranscriptDelivery:
    def test_transcript_promotes_wanted_entry(self, tmp_path):
        repo = _setup_repo(tmp_path)
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/post")
        sources_p = repo / "reference-only" / "sources.json"
        sources_p.write_text(json.dumps({
            rid: {
                "id": rid,
                "canonical_url": canon,
                "title": "T",
                "files": [
                    {"format": "youtube-transcript", "filename": None,
                     "ingestion_status": "want", "youtube_url": YT_URL},
                ],
            }
        }, indent=2, sort_keys=True))

        # Deliver a transcript .txt in the drop dir
        tx = repo / "research" / "manual" / "talk-transcript.txt"
        tx.write_text(YT_URL + "\n\n[0:00] hello\n", encoding="utf-8")
        subprocess.run(["git", "add", str(tx)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0, result.stderr
        assert "YouTube transcripts delivered" in result.stdout

        data = json.loads(sources_p.read_text())
        entry = data[rid]["files"][0]
        assert entry["ingestion_status"] == "have"
        assert entry["filename"] == "talk-transcript.txt"
        assert entry["youtube_url"] == YT_URL
        # File moved into <id>/
        moved = repo / "reference-only" / rid / "talk-transcript.txt"
        assert moved.exists()
        assert not tx.exists()

    def test_transcript_with_no_match_is_flagged(self, tmp_path):
        repo = _setup_repo(tmp_path)
        # No wanted entry in catalog
        tx = repo / "research" / "manual" / "orphan-transcript.txt"
        tx.write_text(YT_URL + "\nbody\n", encoding="utf-8")
        subprocess.run(["git", "add", str(tx)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0
        assert "Transcript files with no matching wanted entry" in result.stdout
        # File stays where it is
        assert tx.exists()
