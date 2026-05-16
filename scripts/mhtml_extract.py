#!/usr/bin/env python3
"""Extract title, URL, text body, and image inventory from MHTML files.

Usage:
  mhtml_extract.py info <file.mhtml>        # JSON: title, url, n_images, image list, text_len
  mhtml_extract.py text <file.mhtml>        # plain text body (HTML stripped)
  mhtml_extract.py save-image <file.mhtml> <index> <out.png|jpg>   # save Nth image
  mhtml_extract.py to-txt <file.mhtml> <out.txt>                   # write plain text
"""
from __future__ import annotations

import email
import email.policy
import html as html_mod
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


def load_message(path: Path):
    with open(path, "rb") as fh:
        return email.message_from_binary_file(fh, policy=email.policy.default)


class _Stripper(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "head", "title"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0
        self.title: str | None = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        if tag in self.SKIP:
            self.skip_depth += 1
        if tag in {"br", "p", "li", "tr", "div", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in self.SKIP and self.skip_depth > 0:
            self.skip_depth -= 1
        if tag in {"p", "li", "tr", "div", "h1", "h2", "h3", "h4"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._in_title and self.title is None:
            t = data.strip()
            if t:
                self.title = t
        if self.skip_depth == 0:
            self.parts.append(data)


def strip_html(html: str) -> tuple[str, str | None]:
    p = _Stripper()
    try:
        p.feed(html)
    except Exception:
        pass
    text = "".join(p.parts)
    # Collapse runs of whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip(), p.title


IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp", "image/svg+xml", "image/bmp"}


def iter_parts(msg):
    if msg.is_multipart():
        for sub in msg.walk():
            if not sub.is_multipart():
                yield sub
    else:
        yield msg


def gather(msg) -> dict:
    snapshot_url = msg.get("Snapshot-Content-Location") or msg.get("Content-Location")
    parts = list(iter_parts(msg))
    html_parts = []
    images = []
    text_parts = []
    for i, p in enumerate(parts):
        ctype = (p.get_content_type() or "").lower()
        cloc = p.get("Content-Location") or ""
        if ctype == "text/html":
            try:
                payload = p.get_content()
            except Exception:
                payload = p.get_payload(decode=True)
                if isinstance(payload, bytes):
                    payload = payload.decode("utf-8", errors="replace")
            html_parts.append({"index": i, "url": cloc, "html": payload or ""})
        elif ctype == "text/plain":
            try:
                payload = p.get_content()
            except Exception:
                payload = p.get_payload(decode=True)
                if isinstance(payload, bytes):
                    payload = payload.decode("utf-8", errors="replace")
            text_parts.append(payload or "")
        elif ctype in IMAGE_TYPES or ctype.startswith("image/"):
            try:
                raw = p.get_payload(decode=True) or b""
            except Exception:
                raw = b""
            images.append({
                "index": i,
                "content_type": ctype,
                "url": cloc,
                "size": len(raw),
            })
    # Pick the largest (i.e. main) html part for title/text extraction
    main_html = ""
    main_url = ""
    if html_parts:
        main = max(html_parts, key=lambda h: len(h["html"]))
        main_html = main["html"]
        main_url = main["url"]
    text, title = strip_html(main_html) if main_html else ("\n".join(text_parts), None)
    return {
        "snapshot_url": snapshot_url,
        "main_url": main_url,
        "title": title,
        "text": text,
        "n_images": len(images),
        "images": images,
        "n_html_parts": len(html_parts),
    }


def cmd_info(path: Path) -> None:
    msg = load_message(path)
    d = gather(msg)
    # Trim text for JSON brevity
    text = d.pop("text", "")
    d["text_len"] = len(text)
    d["text_head"] = text[:1200]
    print(json.dumps(d, indent=2))


def cmd_text(path: Path) -> None:
    msg = load_message(path)
    d = gather(msg)
    sys.stdout.write(d["text"])


def cmd_to_txt(path: Path, out: Path) -> None:
    msg = load_message(path)
    d = gather(msg)
    header = []
    if d.get("title"):
        header.append(f"TITLE: {d['title']}")
    url = d.get("snapshot_url") or d.get("main_url")
    if url:
        header.append(f"URL: {url}")
    body = ("\n".join(header) + "\n\n" if header else "") + d["text"]
    out.write_text(body, encoding="utf-8")
    print(f"wrote {len(body)} chars to {out}")


def cmd_save_image(path: Path, idx: int, out: Path) -> None:
    msg = load_message(path)
    parts = list(iter_parts(msg))
    images = [p for p in parts if (p.get_content_type() or "").lower().startswith("image/")]
    if idx < 0 or idx >= len(images):
        raise SystemExit(f"image index {idx} out of range (0..{len(images)-1})")
    raw = images[idx].get_payload(decode=True) or b""
    out.write_bytes(raw)
    print(f"wrote {len(raw)} bytes to {out}  ({images[idx].get_content_type()})")


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit(2)
    cmd = sys.argv[1]
    path = Path(sys.argv[2])
    if cmd == "info":
        cmd_info(path)
    elif cmd == "text":
        cmd_text(path)
    elif cmd == "to-txt":
        cmd_to_txt(path, Path(sys.argv[3]))
    elif cmd == "save-image":
        cmd_save_image(path, int(sys.argv[3]), Path(sys.argv[4]))
    else:
        raise SystemExit(f"unknown command: {cmd}")


if __name__ == "__main__":
    main()
