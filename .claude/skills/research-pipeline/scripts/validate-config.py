"""Validate the embedded YAML config block in SKILL.md.

Checks:
    - YAML parses cleanly (delegated to _config.load_config)
    - All required fields are present and of the right type
    - All path fields resolve to existing paths on disk (warns if not)
    - github.owner/repo matches the git remote origin

Exit codes:
    0 = OK
    1 = errors
    2 = warnings only

Run before any catalog/drain operation if the config "looks off".
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# Sibling import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import load_config, repo_root, ConfigError  # noqa: E402

REQUIRED_STRING_FIELDS = [
    "skill_path", "library_path", "schema_path",
    "data_path", "md_path", "trigger_path",
]
REQUIRED_LIST_FIELDS = ["report_paths", "ingestion_paths"]
REQUIRED_GITHUB_FIELDS = [
    "owner", "repo", "fetch_branch_prefix", "fetch_issue_label",
]

PATHS_MUST_EXIST = ["skill_path", "library_path"]
PATHS_SHOULD_EXIST = ["schema_path", "data_path"]
PATHS_OK_IF_MISSING = ["md_path", "trigger_path"]


def main() -> int:
    try:
        cfg = load_config()
    except ConfigError as e:
        print(f"✗ Config load failed: {e}", file=sys.stderr)
        return 1

    errors = []
    warnings = []

    # Required string fields
    for field in REQUIRED_STRING_FIELDS:
        if field not in cfg:
            errors.append(f"missing required field: {field}")
        elif not isinstance(cfg[field], str):
            errors.append(f"field {field} must be a string, got {type(cfg[field]).__name__}")

    # Required list fields
    for field in REQUIRED_LIST_FIELDS:
        if field not in cfg:
            errors.append(f"missing required field: {field}")
        elif not isinstance(cfg[field], list):
            errors.append(f"field {field} must be a list, got {type(cfg[field]).__name__}")
        elif not all(isinstance(x, str) for x in cfg[field]):
            errors.append(f"all items in {field} must be strings")

    # GitHub block
    if "github" not in cfg:
        errors.append("missing required field: github")
    elif not isinstance(cfg["github"], dict):
        errors.append("field github must be an object")
    else:
        gh = cfg["github"]
        for field in REQUIRED_GITHUB_FIELDS:
            if field not in gh:
                errors.append(f"missing required field: github.{field}")
            elif not isinstance(gh[field], str):
                errors.append(f"field github.{field} must be a string")

    # Path existence
    root = repo_root()
    for field in PATHS_MUST_EXIST:
        if field in cfg and isinstance(cfg[field], str):
            p = root / cfg[field]
            if not p.exists():
                errors.append(f"{field}={cfg[field]} does not exist (resolved: {p})")

    for field in PATHS_SHOULD_EXIST:
        if field in cfg and isinstance(cfg[field], str):
            p = root / cfg[field]
            if not p.exists():
                warnings.append(
                    f"{field}={cfg[field]} does not exist yet — expected after PR #79 lands"
                )

    for field in ["report_paths", "ingestion_paths"]:
        if isinstance(cfg.get(field), list):
            for p_str in cfg[field]:
                if isinstance(p_str, str):
                    p = root / p_str
                    if not p.exists():
                        warnings.append(f"{field} entry {p_str!r} does not exist on disk")

    # GitHub remote check (best-effort; skip if no git available)
    if "github" in cfg and isinstance(cfg["github"], dict):
        gh = cfg["github"]
        expected_owner = gh.get("owner")
        expected_repo = gh.get("repo")
        if expected_owner and expected_repo:
            try:
                result = subprocess.run(
                    ["git", "remote", "get-url", "origin"],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,
                )
                if result.returncode == 0:
                    remote_url = result.stdout.strip()
                    expected = f"{expected_owner}/{expected_repo}"
                    if expected not in remote_url:
                        warnings.append(
                            f"github.owner/repo={expected!r} not found in git origin {remote_url!r}"
                        )
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass  # git not available; skip check

    # Report
    if errors:
        for e in errors:
            print(f"✗ {e}", file=sys.stderr)
    if warnings:
        for w in warnings:
            print(f"⚠ {w}", file=sys.stderr)

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    if warnings:
        print(f"\n✓ Config OK with {len(warnings)} warning(s)")
        return 0  # warnings don't block (lint-sources.sh treats non-zero as fail)
    print("✓ Config valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
