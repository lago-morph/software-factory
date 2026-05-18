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
    "update_plan.py",
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


class TestDrainCompanionUrl:
    def _minimal_pdf(self) -> bytes:
        # PDF bytes with no /URL, /Source, or /URI — forces companion lookup.
        return b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<< /Type /Catalog >>\nendobj\n"

    def test_pdf_with_companion_ingested_and_companion_deleted(self, tmp_path):
        repo = _setup_repo(tmp_path)
        pdf = repo / "research" / "manual" / "Guide.pdf"
        pdf.write_bytes(self._minimal_pdf())
        comp = repo / "research" / "manual" / "URL of Guide.pdf.txt"
        comp.write_text("The URL for the PDF is https://example.com/hub/Guide.pdf\n")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True)

        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0, result.stderr
        # PDF migrated into reference-only/<id>/
        data = json.loads((repo / "reference-only" / "sources.json").read_text())
        assert len(data) == 1
        record = next(iter(data.values()))
        assert record["canonical_url"] == "https://example.com/hub/Guide.pdf"
        assert record["files"][0]["filename"] == "Guide.pdf"
        # Companion file consumed
        assert not comp.exists()
        assert not pdf.exists()
        assert "Companion URL files consumed: **1**" in result.stdout

    def test_companion_without_target_is_flagged_not_consumed(self, tmp_path):
        repo = _setup_repo(tmp_path)
        comp = repo / "research" / "manual" / "URL of Missing.pdf.txt"
        comp.write_text("https://example.com/missing.pdf\n")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True)

        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0
        # Companion left in place
        assert comp.exists()
        assert "Companion URL files left orphaned" in result.stdout

    def test_companion_with_failing_target_left_in_place(self, tmp_path):
        # Target file exists but its companion is empty of URLs: target gets
        # flagged 'no extractable URL', companion stays put.
        repo = _setup_repo(tmp_path)
        pdf = repo / "research" / "manual" / "Bad.pdf"
        pdf.write_bytes(self._minimal_pdf())
        comp = repo / "research" / "manual" / "URL of Bad.pdf.txt"
        comp.write_text("Just prose, no link.\n")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True)

        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0
        # Both files still in research/manual
        assert pdf.exists()
        assert comp.exists()
        assert "no extractable URL" in result.stdout


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


class TestDrainSkipsReadme:
    def test_readme_md_in_drop_dir_is_silently_skipped(self, tmp_path):
        repo = _setup_repo(tmp_path)
        readme = repo / "research" / "manual" / "README.md"
        readme.write_text("# About this directory\n\nNo URLs here.")
        subprocess.run(["git", "add", str(readme)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint", "--no-plan-update")
        assert result.returncode == 0, result.stderr
        # README should still exist (not deleted, not flagged)
        assert readme.exists()
        # Drain output should not list it as flagged
        assert "README.md" not in result.stdout

    def test_other_skip_filenames_also_ignored(self, tmp_path):
        repo = _setup_repo(tmp_path)
        for name in ("AGENTS.md", "NOTES.md", "claude.md"):
            (repo / "research" / "manual" / name).write_text("placeholder")
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint", "--no-plan-update")
        assert result.returncode == 0, result.stderr
        for name in ("AGENTS.md", "NOTES.md", "claude.md"):
            assert (repo / "research" / "manual" / name).exists()


class TestDrainWantPromotion:
    def _existing_record_with_want(self, repo: Path) -> str:
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/article")
        write_sources_json(repo, {
            rid: {
                "id": rid,
                "canonical_url": canon,
                "title": "Article",
                "files": [
                    {"format": "html", "filename": None, "ingestion_status": "want"},
                ],
            },
        })
        return rid

    def test_mhtml_attach_clears_html_want(self, tmp_path):
        repo = _setup_repo(tmp_path)
        rid = self._existing_record_with_want(repo)
        mhtml = repo / "research" / "manual" / "article.mhtml"
        mhtml.write_text(
            "From: <Saved by Blink>\n"
            "Snapshot-Content-Location: https://example.com/article\n"
            "MIME-Version: 1.0\n\nbody\n"
        )
        subprocess.run(["git", "add", str(mhtml)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint", "--no-plan-update")
        assert result.returncode == 0, result.stderr
        data = json.loads((repo / "reference-only" / "sources.json").read_text())
        files = data[rid]["files"]
        wants = [f for f in files if f.get("ingestion_status") == "want"]
        assert not wants, f"want entries should be cleared, got: {wants}"
        haves = [f for f in files if f.get("ingestion_status") == "have"]
        assert any(f.get("format") == "mhtml" for f in haves)

    def test_tidy_wants_sweep(self, tmp_path):
        repo = _setup_repo(tmp_path)
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/article.pdf")
        write_sources_json(repo, {
            rid: {
                "id": rid,
                "canonical_url": canon,
                "title": "Paper",
                "files": [
                    {"format": "pdf", "filename": None, "ingestion_status": "want"},
                    {"format": "pdf", "filename": "paper.pdf",
                     "sha256": "deadbeef" * 8, "ingestion_status": "have"},
                ],
            },
        })
        result = _run_drain(repo, "--tidy-wants")
        assert result.returncode == 0, result.stderr
        data = json.loads((repo / "reference-only" / "sources.json").read_text())
        files = data[rid]["files"]
        assert not any(f.get("ingestion_status") == "want" for f in files)

    def test_youtube_transcript_want_is_preserved(self, tmp_path):
        # A want entry carrying a youtube_url is a transcript want and MUST
        # NOT be cleared by the generic-want purge.
        repo = _setup_repo(tmp_path)
        from url_canonicalize import canonicalize_and_id
        canon, rid = canonicalize_and_id("https://example.com/post")
        write_sources_json(repo, {
            rid: {
                "id": rid,
                "canonical_url": canon,
                "title": "Post",
                "files": [
                    {"format": "youtube-transcript", "filename": None,
                     "ingestion_status": "want",
                     "youtube_url": "https://youtu.be/abc123"},
                ],
            },
        })
        mhtml = repo / "research" / "manual" / "post.mhtml"
        mhtml.write_text(
            "From: <Saved by Blink>\n"
            "Snapshot-Content-Location: https://example.com/post\n"
            "MIME-Version: 1.0\n\nbody\n"
        )
        subprocess.run(["git", "add", str(mhtml)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint", "--no-plan-update")
        assert result.returncode == 0, result.stderr
        data = json.loads((repo / "reference-only" / "sources.json").read_text())
        files = data[rid]["files"]
        transcript_wants = [
            f for f in files
            if f.get("ingestion_status") == "want" and f.get("youtube_url")
        ]
        assert len(transcript_wants) == 1


class TestDrainPlanAutoUpdate:
    def _setup_plan(self, repo: Path) -> Path:
        plan = repo / "research" / "PLAN.md"
        plan.parent.mkdir(parents=True, exist_ok=True)
        plan.write_text(
            "# Research PLAN\n\n"
            "**Version:** v0.1 (2026-01-01)\n\n"
            "## 1. Current state (TL;DR)\n\n"
            "- **Session 2026-01-01 — initial** — bootstrap.\n\n"
            "**Open items live in:**\n- §2\n\n"
            "## 2. Other\n\nstuff\n\n"
            "## 10. Round-by-round canonical reports (lookup table)\n\n"
            "| Round | Topic | Status | Notes |\n"
            "|---|---|---|---|\n"
            "| 1 | bootstrap | ✅ | initial |\n\n"
            "## 11. Archive\n\nstuff\n"
        )
        return plan

    def test_drain_auto_appends_plan_entry(self, tmp_path):
        repo = _setup_repo(tmp_path)
        self._setup_plan(repo)
        f = repo / "research" / "manual" / "auto.html"
        f.write_text(
            '<html><head><link rel="canonical" href="https://example.com/auto">'
            '<title>Auto Post</title></head><body>x</body></html>'
        )
        subprocess.run(["git", "add", str(f)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0, result.stderr
        plan_text = (repo / "research" / "PLAN.md").read_text()
        # New session bullet should mention Round-2
        assert "Round-2" in plan_text
        # §10 should have a row for round 2
        assert "| 2 |" in plan_text
        # Version bumped from v0.1 to v0.2
        assert "**Version:** v0.2" in plan_text

    def test_no_plan_update_flag(self, tmp_path):
        repo = _setup_repo(tmp_path)
        plan_path = self._setup_plan(repo)
        original = plan_path.read_text()
        f = repo / "research" / "manual" / "auto.html"
        f.write_text(
            '<html><head><link rel="canonical" href="https://example.com/auto">'
            '<title>Auto Post</title></head><body>x</body></html>'
        )
        subprocess.run(["git", "add", str(f)], cwd=repo, check=True)
        result = _run_drain(repo, "--no-lint", "--no-plan-update")
        assert result.returncode == 0, result.stderr
        assert plan_path.read_text() == original

    def test_no_material_change_skips_plan_update(self, tmp_path):
        repo = _setup_repo(tmp_path)
        plan_path = self._setup_plan(repo)
        original = plan_path.read_text()
        # Empty drain (no files dropped)
        result = _run_drain(repo, "--no-lint")
        assert result.returncode == 0, result.stderr
        assert plan_path.read_text() == original


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
