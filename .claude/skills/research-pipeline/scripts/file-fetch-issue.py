"""Read 'want' records from the catalog and file a fetch-blocked-urls issue.

For every record with at least one file entry marked ingestion_status=want,
collect the canonical_url. Then file a single GitHub issue with the
fetch-urls label, listing those URLs in the body. The action picks it up
and produces a fetched/issue-N branch.

Two paths:
    1. `gh` CLI (preferred when available — falls through to MCP if not)
    2. MCP github server (Claude Code on the Web)

Either way, the catalog is the source of truth: this script is just a
formatting + delivery shim.

Usage:
    python file-fetch-issue.py                        # list want URLs (dry-run)
    python file-fetch-issue.py --file                 # actually file the issue
    python file-fetch-issue.py --file --gh            # force gh CLI path
    python file-fetch-issue.py --file --mcp           # print MCP invocation (for AI)
    python file-fetch-issue.py --title "..."          # custom issue title

When --mcp is selected, the script prints the exact mcp__github__issue_write
call the agent should make (since this Python script can't directly invoke MCP
tools — only the agent can).
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import data_path, github_config, ConfigError  # noqa: E402


def collect_wanted_urls() -> list[tuple[str, str]]:
    """Return [(canonical_url, record_id), ...] for records with want files."""
    try:
        data_p = data_path()
    except ConfigError as e:
        print(f"✗ Config error: {e}", file=sys.stderr)
        sys.exit(1)
    if not data_p.exists():
        print(f"✗ {data_p} does not exist", file=sys.stderr)
        sys.exit(1)
    data = json.loads(data_p.read_text(encoding="utf-8"))

    out = []
    for rid, rec in data.items():
        if not isinstance(rec, dict):
            continue
        files = rec.get("files", [])
        if not isinstance(files, list):
            continue
        if not any(isinstance(f, dict) and f.get("ingestion_status") == "want" for f in files):
            continue
        url = rec.get("canonical_url")
        if url:
            out.append((url, rid))
    return out


def build_body(items: list[tuple[str, str]]) -> str:
    """Render the issue body with one URL per line + context."""
    lines = [
        "URLs to fetch — auto-generated from `reference-only/sources.json`",
        "(records with `files[].ingestion_status == \"want\"`).",
        "",
        "The catalog is the source of truth. After this fetch completes, drain.py",
        "will move the results into reference-only/<id>/ and flip status to `have`.",
        "",
        "## URLs",
        "",
    ]
    for url, rid in items:
        lines.append(f"- {url}  (catalog id: `{rid}`)")
    lines.append("")
    lines.append("## After this issue's action completes")
    lines.append("")
    lines.append("1. `git fetch origin fetched/issue-<N>`")
    lines.append("2. Merge into working branch")
    lines.append("3. Run `python .claude/skills/research-pipeline/scripts/drain.py`")
    lines.append("4. Close this issue")
    return "\n".join(lines)


def file_via_gh(title: str, body: str, label: str) -> int:
    """Returns issue number on success, exits non-zero on failure."""
    result = subprocess.run(
        ["gh", "issue", "create",
         "--title", title,
         "--label", label,
         "--body", body],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"✗ gh issue create failed: {result.stderr}", file=sys.stderr)
        sys.exit(2)
    # gh prints the issue URL on success
    out = result.stdout.strip()
    print(f"✓ Created issue: {out}")
    # Parse issue number from URL
    try:
        num = int(out.rsplit("/", 1)[-1])
        return num
    except ValueError:
        return 0


def print_mcp_invocation(title: str, body: str, label: str, owner: str, repo: str) -> None:
    """Print the MCP tool call for the agent to execute."""
    body_repr = textwrap.indent(body, " " * 8)
    print(textwrap.dedent(f'''
        # Agent: execute this MCP call to file the fetch issue:

        mcp__github__issue_write(
            method="create",
            owner={owner!r},
            repo={repo!r},
            title={title!r},
            body=(
        {body_repr!r}
            ),
            labels=[{label!r}],
        )
    ''').strip())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", action="store_true", help="actually file the issue (default: dry-run)")
    ap.add_argument("--gh", action="store_true", help="force gh CLI path")
    ap.add_argument("--mcp", action="store_true", help="print MCP invocation for agent")
    ap.add_argument("--title", default=None, help="custom issue title")
    ap.add_argument("--label", default=None, help="override fetch label (default: from config)")
    args = ap.parse_args()

    try:
        gh = github_config()
    except ConfigError as e:
        print(f"✗ Config error: {e}", file=sys.stderr)
        return 1
    label = args.label or gh.get("fetch_issue_label", "fetch-urls")
    owner = gh["owner"]
    repo = gh["repo"]

    items = collect_wanted_urls()
    if not items:
        print("No want records in catalog. Nothing to file.")
        return 0

    title = args.title or f"[fetch-urls] catalog want-records — {len(items)} URL(s)"
    body = build_body(items)

    if not args.file:
        print(f"Would file issue: {title}")
        print(f"Body ({len(body)} chars):\n")
        print(body)
        print(f"\n({len(items)} URLs collected. Re-run with --file to actually file.)")
        return 0

    # Choose path
    if args.mcp:
        print_mcp_invocation(title, body, label, owner, repo)
        return 0

    if args.gh or (not args.mcp and shutil.which("gh")):
        try:
            num = file_via_gh(title, body, label)
            print(f"Issue #{num} filed. Action should produce fetched/issue-{num} in ~1-3 minutes.")
            return 0
        except SystemExit:
            print("Falling back to MCP path...", file=sys.stderr)

    # MCP fallback
    print("gh CLI unavailable — printing MCP invocation for agent to execute:", file=sys.stderr)
    print_mcp_invocation(title, body, label, owner, repo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
