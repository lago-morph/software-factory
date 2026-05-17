"""Unit tests for extract_url."""

from pathlib import Path
import pytest

from extract_url import extract_url


@pytest.fixture
def write(tmp_path):
    """Helper to write a file and return its path."""
    def _write(name: str, content: str | bytes) -> Path:
        p = tmp_path / name
        if isinstance(content, str):
            p.write_text(content, encoding="utf-8")
        else:
            p.write_bytes(content)
        return p
    return _write


class TestMhtml:
    def test_snapshot_content_location(self, write):
        content = """From: <Saved by Blink>
Snapshot-Content-Location: https://example.com/saved-page
Subject: Some Page Title
MIME-Version: 1.0
Content-Type: multipart/related

body content
"""
        p = write("test.mhtml", content)
        assert extract_url(p) == "https://example.com/saved-page"

    def test_content_location_fallback(self, write):
        content = """From: sender
Content-Location: https://example.com/cl
"""
        p = write("test.mhtml", content)
        assert extract_url(p) == "https://example.com/cl"

    def test_missing_headers_returns_none(self, write):
        p = write("test.mhtml", "From: sender\nNo URL anywhere\n")
        assert extract_url(p) is None


class TestHtml:
    def test_link_canonical(self, write):
        html = """<html><head>
<title>Page</title>
<link rel="canonical" href="https://example.com/canonical">
</head><body>...</body></html>"""
        p = write("test.html", html)
        assert extract_url(p) == "https://example.com/canonical"

    def test_link_canonical_reversed_attrs(self, write):
        html = '<head><link href="https://example.com/canonical" rel="canonical"></head>'
        p = write("test.html", html)
        assert extract_url(p) == "https://example.com/canonical"

    def test_og_url(self, write):
        html = '<head><meta property="og:url" content="https://example.com/og"></head>'
        p = write("test.html", html)
        assert extract_url(p) == "https://example.com/og"

    def test_twitter_url_fallback(self, write):
        html = '<head><meta name="twitter:url" content="https://example.com/tw"></head>'
        p = write("test.html", html)
        assert extract_url(p) == "https://example.com/tw"

    def test_no_url_returns_none(self, write):
        html = "<html><head><title>X</title></head><body>no url</body></html>"
        p = write("test.html", html)
        assert extract_url(p) is None


class TestText:
    def test_url_header(self, write):
        text = "Title: My Page\nURL: https://example.com/page\nBody."
        p = write("test.txt", text)
        assert extract_url(p) == "https://example.com/page"

    def test_first_line_url(self, write):
        text = "https://example.com/page\nMore content.\n"
        p = write("test.txt", text)
        assert extract_url(p) == "https://example.com/page"

    def test_source_label(self, write):
        text = "Source: https://example.com/src\nBody.\n"
        p = write("test.txt", text)
        assert extract_url(p) == "https://example.com/src"

    def test_no_url(self, write):
        p = write("test.txt", "Just prose, no URL.\nMore prose.\n")
        assert extract_url(p) is None


class TestMarkdown:
    def test_frontmatter_url(self, write):
        md = """---
title: My Doc
url: https://example.com/md
---
# Body
"""
        p = write("test.md", md)
        assert extract_url(p) == "https://example.com/md"

    def test_canonical_url_field(self, write):
        md = """---
canonical_url: https://example.com/canon
---
"""
        p = write("test.md", md)
        assert extract_url(p) == "https://example.com/canon"

    def test_fallback_to_url_header(self, write):
        md = "URL: https://example.com/fallback\n# Heading\nBody.\n"
        p = write("test.md", md)
        assert extract_url(p) == "https://example.com/fallback"


class TestUnsupportedFormats:
    def test_png_returns_none(self, write):
        p = write("test.png", b"\x89PNG\r\n\x1a\n")
        assert extract_url(p) is None

    def test_jpg_returns_none(self, write):
        p = write("test.jpg", b"\xff\xd8\xff")
        assert extract_url(p) is None

    def test_mp4_returns_none(self, write):
        p = write("test.mp4", b"\x00\x00\x00")
        assert extract_url(p) is None

    def test_missing_file_returns_none(self, tmp_path):
        assert extract_url(tmp_path / "nope.html") is None


class TestJson:
    def test_canonical_url_field(self, write):
        p = write("test.json", '{"canonical_url": "https://example.com/jc"}')
        assert extract_url(p) == "https://example.com/jc"

    def test_url_field_fallback(self, write):
        p = write("test.json", '{"url": "https://example.com/jurl"}')
        assert extract_url(p) == "https://example.com/jurl"

    def test_no_recognized_field(self, write):
        p = write("test.json", '{"other": "value"}')
        assert extract_url(p) is None
