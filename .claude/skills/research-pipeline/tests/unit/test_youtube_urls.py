"""Unit tests for youtube_urls.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from youtube_urls import (
    canonicalize_youtube_url,
    extract_youtube_urls_from_file,
    first_line_youtube_url,
    is_youtube_url,
)


VID = "dQw4w9WgXcQ"
CANON = f"https://www.youtube.com/watch?v={VID}"


class TestIsYoutubeUrl:
    @pytest.mark.parametrize("url", [
        "https://www.youtube.com/watch?v=" + VID,
        "https://youtube.com/watch?v=" + VID,
        "http://youtu.be/" + VID,
        "https://m.youtube.com/watch?v=" + VID,
        "https://www.youtube-nocookie.com/embed/" + VID,
    ])
    def test_yes(self, url):
        assert is_youtube_url(url) is True

    @pytest.mark.parametrize("url", [
        "https://example.com/watch?v=abc",
        "https://vimeo.com/12345",
        "not a url",
        "",
        None,
    ])
    def test_no(self, url):
        assert is_youtube_url(url) is False


class TestCanonicalize:
    @pytest.mark.parametrize("raw", [
        f"https://www.youtube.com/watch?v={VID}",
        f"https://www.youtube.com/watch?v={VID}&t=42s",
        f"https://www.youtube.com/watch?v={VID}&feature=share",
        f"https://youtu.be/{VID}",
        f"https://youtu.be/{VID}?t=10",
        f"https://www.youtube.com/embed/{VID}",
        f"https://www.youtube.com/shorts/{VID}",
        f"https://www.youtube.com/v/{VID}",
        f"https://m.youtube.com/watch?v={VID}",
        f"http://www.youtube.com/watch?v={VID}",  # http → still canonicalizes
    ])
    def test_canonicalizes_variants(self, raw):
        assert canonicalize_youtube_url(raw) == CANON

    def test_idempotent(self):
        assert canonicalize_youtube_url(CANON) == CANON

    @pytest.mark.parametrize("bad", [
        "https://www.youtube.com/channel/UCfoo",       # channel, not a video
        "https://www.youtube.com/playlist?list=PLfoo",  # playlist only
        "https://example.com/watch?v=" + VID,           # wrong host
        "https://youtu.be/short",                       # video id too short
    ])
    def test_invalid(self, bad):
        with pytest.raises(ValueError):
            canonicalize_youtube_url(bad)


class TestFirstLineYoutubeUrl:
    def test_first_line_is_canonical(self, tmp_path: Path):
        p = tmp_path / "t.txt"
        p.write_text(CANON + "\n\nthe transcript body\n", encoding="utf-8")
        assert first_line_youtube_url(p) == CANON

    def test_first_line_youtu_be_normalized(self, tmp_path: Path):
        p = tmp_path / "t.txt"
        p.write_text(f"https://youtu.be/{VID}?t=12\nbody\n", encoding="utf-8")
        assert first_line_youtube_url(p) == CANON

    def test_blank_lines_skipped(self, tmp_path: Path):
        p = tmp_path / "t.txt"
        p.write_text(f"\n\n{CANON}\nbody\n", encoding="utf-8")
        assert first_line_youtube_url(p) == CANON

    def test_no_url_first_line(self, tmp_path: Path):
        p = tmp_path / "t.txt"
        p.write_text("some heading\n" + CANON + "\n", encoding="utf-8")
        assert first_line_youtube_url(p) is None

    def test_missing_file(self, tmp_path: Path):
        assert first_line_youtube_url(tmp_path / "no.txt") is None


class TestExtractYoutubeUrlsFromFile:
    def test_finds_url_in_html(self, tmp_path: Path):
        p = tmp_path / "f.html"
        p.write_text(
            f"<p>Watch this: <a href='https://youtu.be/{VID}'>video</a> for context.</p>",
            encoding="utf-8",
        )
        mentions = extract_youtube_urls_from_file(p)
        assert len(mentions) == 1
        assert mentions[0].url == CANON
        assert "Watch this" in mentions[0].snippet

    def test_dedupe_canonical(self, tmp_path: Path):
        p = tmp_path / "f.html"
        p.write_text(
            f"first <a href='https://youtu.be/{VID}'>x</a> "
            f"second <a href='https://www.youtube.com/watch?v={VID}&t=10'>y</a>",
            encoding="utf-8",
        )
        mentions = extract_youtube_urls_from_file(p)
        assert len(mentions) == 1
        assert mentions[0].url == CANON

    def test_unrecognized_format_returns_empty(self, tmp_path: Path):
        p = tmp_path / "f.pdf"
        p.write_bytes(b"%PDF garbage")
        assert extract_youtube_urls_from_file(p) == []

    def test_ignores_non_youtube_urls(self, tmp_path: Path):
        p = tmp_path / "f.md"
        p.write_text("See https://example.com/post and https://vimeo.com/123", encoding="utf-8")
        assert extract_youtube_urls_from_file(p) == []

    def test_finds_in_markdown_link(self, tmp_path: Path):
        p = tmp_path / "f.md"
        p.write_text(
            f"Highly recommended: [the talk](https://www.youtube.com/watch?v={VID}) "
            f"covers the foundations.",
            encoding="utf-8",
        )
        mentions = extract_youtube_urls_from_file(p)
        assert len(mentions) == 1
        assert mentions[0].url == CANON
