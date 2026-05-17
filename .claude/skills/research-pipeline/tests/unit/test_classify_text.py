"""Unit tests for classify_text."""

from classify_text import classify


class TestClassify:
    def test_empty_string(self):
        result = classify("")
        assert result["kind"] == "empty"
        assert result["urls"] == []

    def test_whitespace_only(self):
        result = classify("   \n  \n\t\n")
        assert result["kind"] == "empty"

    def test_only_comments(self):
        result = classify("# just a comment\n// another\n")
        assert result["kind"] == "empty"

    def test_pure_url_list(self):
        text = """
https://example.com/a
https://example.com/b
https://example.com/c
"""
        result = classify(text)
        assert result["kind"] == "url_list"
        assert len(result["urls"]) == 3

    def test_url_list_with_comments(self):
        text = """# my urls
https://example.com/a
# comment in middle
https://example.com/b
"""
        result = classify(text)
        assert result["kind"] == "url_list"
        assert len(result["urls"]) == 2

    def test_single_url(self):
        text = "https://example.com/lone\n"
        result = classify(text)
        assert result["kind"] == "url_list"
        assert result["urls"] == ["https://example.com/lone"]

    def test_source_with_first_url(self):
        text = """https://example.com/source
Title: My Page
Some body content here.
More content.
"""
        result = classify(text)
        assert result["kind"] == "source_with_first_url"
        assert result["extracted_url"] == "https://example.com/source"

    def test_source_with_header_url_label_URL(self):
        text = """Title: My Document
URL: https://example.com/page
Author: Someone
Body...
"""
        result = classify(text)
        assert result["kind"] == "source_with_header_url"
        assert result["extracted_url"] == "https://example.com/page"

    def test_source_with_header_url_label_source(self):
        text = """Source: https://example.com/page
Some content.
"""
        result = classify(text)
        assert result["kind"] == "source_with_header_url"

    def test_source_with_header_url_label_link(self):
        text = """Link: https://example.com/page
Body.
"""
        result = classify(text)
        assert result["kind"] == "source_with_header_url"

    def test_mixed_error(self):
        # First line is non-URL so source_with_first_url doesn't match.
        text = """some random non-URL line
https://example.com/a
https://example.com/b
another random line
https://example.com/c
"""
        result = classify(text)
        assert result["kind"] == "mixed_error"

    def test_unrecognized_with_embedded_url(self):
        text = """This is prose about https://example.com/foo and other things.
More prose. Nothing structured here at all.
"""
        result = classify(text)
        assert result["kind"] == "unrecognized"
        assert "https://example.com/foo" in result["urls"]

    def test_unrecognized_no_urls(self):
        text = "Just random text with no urls at all.\nMore text.\n"
        result = classify(text)
        assert result["kind"] == "unrecognized"
        assert result["urls"] == []

    def test_http_and_https_both_accepted(self):
        text = "http://example.com/a\nhttps://example.com/b\n"
        result = classify(text)
        assert result["kind"] == "url_list"
        assert len(result["urls"]) == 2

    def test_blank_lines_in_url_list_ok(self):
        text = """
https://a.com/x

https://b.com/y


https://c.com/z
"""
        result = classify(text)
        assert result["kind"] == "url_list"
        assert len(result["urls"]) == 3
