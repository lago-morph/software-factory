"""Unit tests for url_canonicalize."""

import pytest

from url_canonicalize import (
    canonicalize_url,
    compute_id,
    canonicalize_and_id,
    ID_LENGTH,
)


class TestCanonicalize:
    def test_strip_trailing_slash_on_path(self):
        assert canonicalize_url("https://example.com/path/") == "https://example.com/path"

    def test_preserve_root_slash(self):
        assert canonicalize_url("https://example.com/") == "https://example.com/"

    def test_empty_path_becomes_root(self):
        assert canonicalize_url("https://example.com") == "https://example.com/"

    def test_lowercase_scheme(self):
        assert canonicalize_url("HTTPS://example.com/foo") == "https://example.com/foo"

    def test_lowercase_host(self):
        assert canonicalize_url("https://Example.COM/Path") == "https://example.com/Path"

    def test_path_case_preserved(self):
        assert canonicalize_url("https://example.com/CaseSensitivePath") == "https://example.com/CaseSensitivePath"

    def test_drop_fragment(self):
        assert canonicalize_url("https://example.com/p#anchor") == "https://example.com/p"

    def test_drop_default_port_http(self):
        assert canonicalize_url("http://example.com:80/p") == "http://example.com/p"

    def test_drop_default_port_https(self):
        assert canonicalize_url("https://example.com:443/p") == "https://example.com/p"

    def test_preserve_nondefault_port(self):
        assert canonicalize_url("https://example.com:8080/p") == "https://example.com:8080/p"

    def test_drop_utm_source(self):
        assert canonicalize_url("https://e.com/p?utm_source=foo") == "https://e.com/p"

    def test_drop_utm_campaign(self):
        assert canonicalize_url("https://e.com/p?utm_campaign=foo") == "https://e.com/p"

    def test_drop_fbclid(self):
        assert canonicalize_url("https://e.com/p?fbclid=abc") == "https://e.com/p"

    def test_drop_gclid(self):
        assert canonicalize_url("https://e.com/p?gclid=abc") == "https://e.com/p"

    def test_drop_substack_tracking(self):
        assert canonicalize_url("https://sub.substack.com/p/x?r=abc&triedRedirect=true") == "https://sub.substack.com/p/x"

    def test_preserve_meaningful_query_param(self):
        assert canonicalize_url("https://e.com/search?q=test") == "https://e.com/search?q=test"

    def test_strip_some_keep_others(self):
        result = canonicalize_url("https://e.com/p?utm_source=foo&id=42&utm_medium=bar")
        assert result == "https://e.com/p?id=42"

    def test_sort_query_params(self):
        assert canonicalize_url("https://e.com/?z=1&a=2&m=3") == "https://e.com/?a=2&m=3&z=1"

    def test_idempotent(self):
        url = "https://Example.com/Path/?utm_source=foo&keep=yes#hash"
        canon = canonicalize_url(url)
        assert canon == canonicalize_url(canon)

    def test_strips_whitespace(self):
        assert canonicalize_url("  https://e.com/  ") == "https://e.com/"

    def test_empty_url_raises(self):
        with pytest.raises(ValueError):
            canonicalize_url("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError):
            canonicalize_url("   ")

    def test_no_scheme_raises(self):
        with pytest.raises(ValueError):
            canonicalize_url("example.com/foo")

    def test_no_host_raises(self):
        with pytest.raises(ValueError):
            canonicalize_url("https:///path")


class TestComputeId:
    def test_id_length(self):
        rid = compute_id("https://example.com/foo")
        assert len(rid) == ID_LENGTH
        assert ID_LENGTH == 10

    def test_id_is_hex(self):
        rid = compute_id("https://example.com/foo")
        assert all(c in "0123456789abcdef" for c in rid)

    def test_id_deterministic(self):
        a = compute_id("https://example.com/foo")
        b = compute_id("https://example.com/foo")
        assert a == b

    def test_id_invariant_under_canonicalization(self):
        a = compute_id("https://Example.COM/foo/?utm_source=x#bar")
        b = compute_id("https://example.com/foo")
        assert a == b

    def test_different_urls_different_ids(self):
        a = compute_id("https://example.com/foo")
        b = compute_id("https://example.com/bar")
        assert a != b


class TestCanonicalizeAndId:
    def test_returns_tuple(self):
        canon, rid = canonicalize_and_id("https://Example.com/?utm_source=x")
        assert canon == "https://example.com/"
        assert len(rid) == ID_LENGTH

    def test_invalid_input_raises(self):
        with pytest.raises(ValueError):
            canonicalize_and_id("not a url")
