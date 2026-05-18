"""Unit tests for extract_title."""

from extract_title import _decode_rfc2047, extract_title


class TestRfc2047Decode:
    def test_plain_string_passthrough(self):
        assert _decode_rfc2047("Plain title") == "Plain title"

    def test_quoted_printable_decode(self):
        encoded = "=?utf-8?Q?Hamel=20Husain=E2=80=99s=20Blog?="
        assert _decode_rfc2047(encoded) == "Hamel Husain’s Blog"

    def test_bullet_glyph_decode(self):
        encoded = "=?utf-8?Q?Writing=20=E2=80=A2=20Eugene=20Yan?="
        assert _decode_rfc2047(encoded) == "Writing • Eugene Yan"

    def test_base64_decode(self):
        # "Hello, world" in utf-8 base64
        import base64
        b64 = base64.b64encode("Hello, world".encode()).decode()
        encoded = f"=?utf-8?B?{b64}?="
        assert _decode_rfc2047(encoded) == "Hello, world"


class TestExtractTitleMhtml:
    def test_mhtml_subject_with_rfc2047(self, tmp_path):
        content = (
            "From: <Saved by Blink>\n"
            "Snapshot-Content-Location: https://example.com/p\n"
            "Subject: =?utf-8?Q?Hamel=20Husain=E2=80=99s=20Blog?=\n"
            "MIME-Version: 1.0\n\nbody\n"
        )
        p = tmp_path / "test.mhtml"
        p.write_text(content, encoding="utf-8")
        assert extract_title(p) == "Hamel Husain’s Blog"

    def test_mhtml_plain_subject(self, tmp_path):
        content = (
            "From: <Saved by Blink>\n"
            "Subject: A Plain Title\n"
            "MIME-Version: 1.0\n\nbody\n"
        )
        p = tmp_path / "test.mhtml"
        p.write_text(content, encoding="utf-8")
        assert extract_title(p) == "A Plain Title"
