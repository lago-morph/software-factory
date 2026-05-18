"""Unit tests for extract_url."""

from pathlib import Path
import pytest

from extract_url import companion_path, extract_url


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


class TestCompanionFile:
    def test_companion_path_construction(self, tmp_path):
        target = tmp_path / "Foo.pdf"
        assert companion_path(target).name == "URL of Foo.pdf.txt"
        assert companion_path(target).parent == tmp_path

    def test_pdf_with_companion_freeform_sentence(self, tmp_path):
        pdf = tmp_path / "guide.pdf"
        pdf.write_bytes(b"%PDF-1.4 fake content no url metadata")
        (tmp_path / "URL of guide.pdf.txt").write_text(
            "The URL for the PDF is https://example.com/hub/guide.pdf\n"
        )
        assert extract_url(pdf) == "https://example.com/hub/guide.pdf"

    def test_companion_trims_trailing_punctuation(self, tmp_path):
        pdf = tmp_path / "g.pdf"
        pdf.write_bytes(b"%PDF nothing here")
        (tmp_path / "URL of g.pdf.txt").write_text("See https://example.com/x.")
        assert extract_url(pdf) == "https://example.com/x"

    def test_primary_extraction_wins_over_companion(self, write, tmp_path):
        # HTML has its own canonical URL; companion should be ignored.
        html = '<head><link rel="canonical" href="https://primary.example/"></head>'
        page = write("page.html", html)
        (tmp_path / "URL of page.html.txt").write_text("https://wrong.example/")
        assert extract_url(page) == "https://primary.example/"

    def test_no_companion_returns_none(self, tmp_path):
        pdf = tmp_path / "alone.pdf"
        pdf.write_bytes(b"%PDF without url")
        assert extract_url(pdf) is None

    def test_empty_companion_returns_none(self, tmp_path):
        pdf = tmp_path / "empty.pdf"
        pdf.write_bytes(b"%PDF")
        (tmp_path / "URL of empty.pdf.txt").write_text("no link here just prose\n")
        assert extract_url(pdf) is None


class TestPdfUrlPreference:
    def _pdf_with_urls(self, write, name: str, *urls: str):
        body = b"%PDF-1.4\n"
        for u in urls:
            body += b"/URL (" + u.encode() + b")\n"
        body += b"%%EOF\n"
        return write(name, body)

    def test_arxiv_wins_over_github(self, write):
        p = self._pdf_with_urls(
            write, "paper.pdf",
            "https://github.com/x/y", "https://arxiv.org/abs/1234.56789",
        )
        assert extract_url(p) == "https://arxiv.org/abs/1234.56789"

    def test_doi_wins_over_github(self, write):
        p = self._pdf_with_urls(
            write, "paper.pdf",
            "https://github.com/x/y", "https://doi.org/10.1000/xyz",
        )
        assert extract_url(p) == "https://doi.org/10.1000/xyz"

    def test_only_github_falls_back_to_github(self, write):
        p = self._pdf_with_urls(write, "paper.pdf", "https://github.com/x/y")
        assert extract_url(p) == "https://github.com/x/y"

    def test_single_url_unchanged(self, write):
        p = self._pdf_with_urls(write, "paper.pdf", "https://example.com/x")
        assert extract_url(p) == "https://example.com/x"

    def test_tie_breaks_by_first_seen(self, write):
        # Two equal-priority unmatched URLs — first wins.
        p = self._pdf_with_urls(
            write, "paper.pdf", "https://example.com/a", "https://example.com/b",
        )
        assert extract_url(p) == "https://example.com/a"


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
