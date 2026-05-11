#!/usr/bin/env python3
"""Validate relative links and heading anchors in ADR markdown files.

Walks one or more directories (or files), parses every markdown link of the
form `[text](path)` or `[text](path#anchor)`, and for each link:

  * Skips absolute URLs (http://, https://, mailto:, ftp:) — they are not
    in scope for this check; the ADR skill permits absolute URLs for
    external references.

  * Resolves the relative path against the source file's directory.

  * Verifies the target file exists.

  * If the link has an anchor fragment, derives all heading slugs in the
    target file (using GitHub-Flavored Markdown rules) and verifies the
    anchor matches one of them.

Reports broken links to stderr and exits non-zero if any are broken.

Usage:
    python3 .claude/skills/adr/scripts/check_adr_links.py docs/adr/
    python3 .claude/skills/adr/scripts/check_adr_links.py docs/adr/0001-foo.md
    python3 .claude/skills/adr/scripts/check_adr_links.py docs/adr/ .claude/skills/adr/
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Markdown link with optional fragment:
#   [text](./path/to/file.md#optional-anchor)
# Excludes images (`![...](...)`); excludes reference-style links.
# Captures: text, path-with-optional-fragment.
LINK_RE = re.compile(r"(?<!\!)\[([^\]\n]+)\]\(([^)\s][^)]*)\)")

# Fenced code block delimiter (``` or ~~~) optionally followed by a language tag.
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})", re.MULTILINE)

# Inline code span: backticks; multi-backtick spans need matching count, but
# for "strip links inside inline code" purposes a non-greedy single-backtick
# match is adequate (links inside inline code are not rendered as links).
INLINE_CODE_RE = re.compile(r"`+([^`]+)`+")

# ATX heading: leading hashes, optional trailing hashes ignored.
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$", re.MULTILINE)

# Inline-code regions inside headings must be preserved for slug computation
# (GFM strips the backticks but keeps the contents).
HEADING_INLINE_CODE_RE = re.compile(r"`([^`]+)`")

# Characters allowed in GFM heading slugs after lowercase + space-to-hyphen.
# GFM keeps: a-z, 0-9, hyphen, underscore. Strips everything else.
# Note: GFM does NOT collapse consecutive hyphens — "A — B" becomes "a--b",
# not "a-b". Empirically verified against github.com's rendered TOC.
SLUG_STRIP_RE = re.compile(r"[^a-z0-9\-_]")

ABSOLUTE_SCHEMES = ("http://", "https://", "mailto:", "ftp://", "ftps://", "data:")


def gfm_slug(heading_text: str) -> str:
    """Derive the GitHub-Flavored Markdown anchor slug for a heading.

    Reference behavior:
      1. Strip inline-code backticks but keep the contents.
      2. Strip HTML comments.
      3. Lowercase.
      4. Replace spaces with hyphens.
      5. Strip characters that are not a-z, 0-9, hyphen, or underscore.

    Note: GitHub-Flavored Markdown does NOT collapse consecutive hyphens
    introduced by stripped punctuation. The heading "A — B" produces the
    anchor "a--b" (two hyphens around where the em-dash was, because the
    surrounding spaces became hyphens). Verified against rendered TOCs
    on github.com.
    """
    text = heading_text
    # 1. Inline code: keep contents (text inside `...`).
    text = HEADING_INLINE_CODE_RE.sub(lambda m: m.group(1), text)
    # 2. HTML comments inside headings (rare but legal).
    text = re.sub(r"<!--.*?-->", "", text)
    # 3. Lowercase.
    text = text.lower()
    # 4. Spaces -> hyphens.
    text = text.replace(" ", "-")
    # 5. Strip disallowed characters.
    text = SLUG_STRIP_RE.sub("", text)
    return text


# HTML comments span lines and may contain markdown that should not be parsed.
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _strip_code(markdown: str) -> str:
    """Remove regions whose contents are not "live" markdown references.

    Strips, in order:
      1. HTML comments (`<!-- ... -->`, possibly multi-line).
      2. Fenced code blocks (``` or ~~~).
      3. Inline code spans (`...`).

    Returns a transformed body suitable for link / heading extraction.

    Links inside these regions are illustrative examples or template
    placeholders, not real references, and should be excluded from
    link-resolution checks.
    """
    # Strip HTML comments first (they may contain fence markers).
    markdown = HTML_COMMENT_RE.sub(lambda m: "\n" * m.group(0).count("\n"), markdown)

    lines = markdown.splitlines(keepends=True)
    out: list[str] = []
    in_fence = False
    fence_marker = ""

    for line in lines:
        match = FENCE_RE.match(line)
        if match and not in_fence:
            in_fence = True
            fence_marker = match.group(2)[:3]  # `` ` `` or `~`
            out.append("\n")
            continue
        if in_fence:
            # Closing fence: same character, same or greater length.
            if line.lstrip().startswith(fence_marker):
                in_fence = False
                fence_marker = ""
            out.append("\n")
            continue
        # Outside fences: strip inline code spans.
        out.append(INLINE_CODE_RE.sub(" ", line))

    return "".join(out)


def extract_links(markdown: str) -> list[tuple[str, str]]:
    """Return list of (link_text, target) tuples from the markdown body.

    Links inside fenced code blocks and inline code spans are excluded —
    those are illustrative examples, not real references.
    """
    body = _strip_code(markdown)
    return [(m.group(1), m.group(2)) for m in LINK_RE.finditer(body)]


def extract_heading_slugs(markdown: str) -> set[str]:
    """Return the set of anchor slugs derivable from the document's headings.

    Skips lines inside fenced code blocks so that `# foo` lines in shell
    snippets aren't treated as headings.

    GFM disambiguates duplicates by appending -1, -2, etc. to later occurrences.
    For our purposes we accept any slug whose base form matches; the strict
    duplicate-suffix rule is rarely needed for ADRs and adds complexity. If
    duplicates become a real problem in this repo, extend this function.
    """
    body = _strip_code(markdown)
    slugs: set[str] = set()
    seen: dict[str, int] = {}
    for m in HEADING_RE.finditer(body):
        base = gfm_slug(m.group(2))
        if not base:
            continue
        count = seen.get(base, 0)
        slug = base if count == 0 else f"{base}-{count}"
        slugs.add(slug)
        seen[base] = count + 1
    return slugs


def is_absolute(target: str) -> bool:
    lower = target.lower()
    return any(lower.startswith(scheme) for scheme in ABSOLUTE_SCHEMES)


def check_file(md_path: Path, repo_root: Path) -> list[str]:
    """Check one markdown file. Return list of human-readable error strings."""
    errors: list[str] = []
    try:
        body = md_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{md_path}: unreadable: {exc}"]

    for link_text, target in extract_links(body):
        if is_absolute(target):
            continue
        # Strip in-page anchor-only links like `(#section)` — they resolve
        # against the current file.
        if target.startswith("#"):
            anchor = target[1:]
            slugs = extract_heading_slugs(body)
            if anchor and anchor not in slugs:
                errors.append(
                    f"{md_path}: in-page anchor `#{anchor}` not found "
                    f"(link text: '{link_text}')"
                )
            continue

        # Split path#anchor.
        if "#" in target:
            path_part, anchor = target.split("#", 1)
        else:
            path_part, anchor = target, ""

        # Resolve relative to the source file's directory.
        rel = (md_path.parent / path_part).resolve()

        # Refuse to escape the repo root via ../.. tricks.
        try:
            rel.relative_to(repo_root.resolve())
        except ValueError:
            errors.append(
                f"{md_path}: relative link `{target}` resolves outside "
                f"repo root `{repo_root}`"
            )
            continue

        if not rel.exists():
            errors.append(
                f"{md_path}: target file not found for link `{target}` "
                f"(resolved to {rel}; link text: '{link_text}')"
            )
            continue

        if anchor:
            # Anchors only apply to markdown files.
            if rel.suffix.lower() not in (".md", ".markdown"):
                errors.append(
                    f"{md_path}: anchor `#{anchor}` requested on non-markdown "
                    f"target `{rel}` — anchors are only supported on .md files"
                )
                continue
            try:
                target_body = rel.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                errors.append(f"{md_path}: anchor target unreadable: {exc}")
                continue
            target_slugs = extract_heading_slugs(target_body)
            if anchor not in target_slugs:
                errors.append(
                    f"{md_path}: anchor `#{anchor}` not found in `{rel}` "
                    f"(link text: '{link_text}')"
                )

    return errors


def iter_markdown(paths: list[Path]) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        if p.is_dir():
            out.extend(sorted(p.rglob("*.md")))
        elif p.is_file() and p.suffix.lower() in (".md", ".markdown"):
            out.append(p)
        elif not p.exists():
            print(f"warning: path does not exist: {p}", file=sys.stderr)
    return out


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__, file=sys.stderr)
        return 2

    inputs = [Path(a) for a in argv]
    repo_root = _find_repo_root()
    files = iter_markdown(inputs)
    if not files:
        print("No markdown files to check.", file=sys.stderr)
        return 0

    total_errors: list[str] = []
    for f in files:
        total_errors.extend(check_file(f, repo_root))

    if total_errors:
        print(f"{len(total_errors)} broken link(s) found:", file=sys.stderr)
        for err in total_errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    print(f"OK: {len(files)} file(s) checked, all relative links resolve.")
    return 0


def _find_repo_root() -> Path:
    """Walk up from CWD looking for a .git directory; default to CWD."""
    here = Path.cwd().resolve()
    for parent in (here, *here.parents):
        if (parent / ".git").exists():
            return parent
    return here


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
