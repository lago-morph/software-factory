#!/usr/bin/env python3
"""Install the issue-management PreToolUse gate.

The gate is two artifacts living outside the skill directory:

  .claude/hooks/require-issue-management-skill.sh   (hook script)
  .claude/settings.json                              (hook registration)

Both are installed from templates that ship with this skill. Idempotent
by design — running with --check tells you whether anything is drifted
or missing; running with --force regenerates the script and merges the
hook entry into settings.json without disturbing other entries.

Also touches the per-session marker at
    /tmp/.claude-skill-loaded-issue-management
when --check returns 0 (or when --force completes successfully). That
marker is what the hook itself looks for. Touching it here means: every
time the agent runs the skill's pre-flight, the skill is signalled
"loaded for this session", and the gate trusts the next tool call.

Usage:
    python install.py            # install missing, leave existing
    python install.py --check    # exit 0 if installed, 1 if drift/missing
    python install.py --force    # overwrite from template
    python install.py --dry-run  # show what would happen
    python install.py --no-commit  # skip the auto-commit after --force

Exit codes:
    0 — in sync (--check) or install succeeded
    1 — missing or drifted (--check) or install error
    2 — template missing from skill (skill-installation defect)
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_PATH = ".claude/skills/issue-management"
REPO = Path(__file__).resolve().parents[4]

HOOK_TEMPLATE = SKILL_DIR / "resources" / "hooks" / "require-issue-management-skill.sh"
HOOK_TARGET_REL = ".claude/hooks/require-issue-management-skill.sh"
HOOK_TARGET = REPO / HOOK_TARGET_REL

SETTINGS_PATH = REPO / ".claude" / "settings.json"

MARKER = Path("/tmp/.claude-skill-loaded-issue-management")

# The matcher regex covers every MCP tool that names or lists an issue.
# Add to this list (and to the docs) if new gated tools surface.
HOOK_MATCHER = (
    "mcp__github__("
    "issue_read|issue_write|add_issue_comment|"
    "list_issues|search_issues|sub_issue_write"
    ")"
)
HOOK_COMMAND = f".claude/hooks/require-issue-management-skill.sh"
HOOK_DESCRIPTION = "issue-management: require skill load before issue tools"

REQUIRED_SKILL_FILES = [
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "scripts" / "install.py",
    SKILL_DIR / "resources" / "hooks" / "require-issue-management-skill.sh",
]


def _rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO))
    except ValueError:
        return str(p)


def check_skill_intact() -> list[str]:
    return [_rel(p) for p in REQUIRED_SKILL_FILES if not p.exists()]


def touch_marker() -> None:
    try:
        MARKER.parent.mkdir(parents=True, exist_ok=True)
        MARKER.touch(exist_ok=True)
    except OSError:
        # Marker is a convenience for the hook; if /tmp isn't writable
        # we can't help, but the install itself succeeded.
        pass


def hook_script_matches() -> bool:
    if not HOOK_TARGET.exists():
        return False
    expected = HOOK_TEMPLATE.read_text(encoding="utf-8")
    actual = HOOK_TARGET.read_text(encoding="utf-8")
    return expected == actual


def hook_script_executable() -> bool:
    if not HOOK_TARGET.exists():
        return False
    return bool(HOOK_TARGET.stat().st_mode & stat.S_IXUSR)


def load_settings() -> dict:
    if not SETTINGS_PATH.exists():
        return {}
    try:
        return json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"✗ {_rel(SETTINGS_PATH)} is not valid JSON: {e}")


def settings_have_hook(settings: dict) -> bool:
    pre = settings.get("hooks", {}).get("PreToolUse", [])
    for entry in pre:
        if entry.get("matcher") != HOOK_MATCHER:
            continue
        for h in entry.get("hooks", []):
            if h.get("type") == "command" and h.get("command") == HOOK_COMMAND:
                return True
    return False


def merge_hook_into_settings(settings: dict) -> dict:
    hooks_root = settings.setdefault("hooks", {})
    pre = hooks_root.setdefault("PreToolUse", [])

    # Remove any prior entry with our exact matcher so we can write a
    # canonical one. This keeps the file deterministic even after a
    # template edit.
    pre = [
        entry for entry in pre
        if entry.get("matcher") != HOOK_MATCHER
    ]

    pre.append({
        "matcher": HOOK_MATCHER,
        "hooks": [
            {
                "type": "command",
                "command": HOOK_COMMAND,
                "description": HOOK_DESCRIPTION,
            }
        ],
    })

    hooks_root["PreToolUse"] = pre
    return settings


def write_settings(settings: dict) -> None:
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_PATH.write_text(
        json.dumps(settings, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def cmd_check() -> int:
    skill_missing = check_skill_intact()
    if skill_missing:
        print("✗ Skill installation is incomplete. Missing skill-internal files:",
              file=sys.stderr)
        for m in skill_missing:
            print(f"  - {m}", file=sys.stderr)
        return 2

    problems: list[str] = []
    if not HOOK_TARGET.exists():
        problems.append(f"missing: {HOOK_TARGET_REL}")
    elif not hook_script_matches():
        problems.append(f"drifted: {HOOK_TARGET_REL} (template ≠ installed)")
    elif not hook_script_executable():
        problems.append(f"not executable: {HOOK_TARGET_REL}")

    settings = load_settings()
    if not settings_have_hook(settings):
        problems.append(f"missing hook entry in {_rel(SETTINGS_PATH)}")

    if problems:
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        print(
            f"\n{len(problems)} issue(s). "
            f"Fix with: python {SKILL_PATH}/scripts/install.py --force",
            file=sys.stderr,
        )
        return 1

    touch_marker()
    print("✓ issue-management gate installed and in sync")
    return 0


def cmd_install(force: bool, dry_run: bool, no_commit: bool) -> int:
    skill_missing = check_skill_intact()
    if skill_missing:
        print("✗ Skill installation is incomplete. Missing skill-internal files:",
              file=sys.stderr)
        for m in skill_missing:
            print(f"  - {m}", file=sys.stderr)
        return 2

    changed: list[str] = []

    # 1. The hook script
    need_script = (
        not HOOK_TARGET.exists()
        or not hook_script_matches()
        or not hook_script_executable()
    )
    if need_script:
        if dry_run:
            action = "OVERWRITE" if HOOK_TARGET.exists() else "INSTALL"
            print(f"  {action}: {HOOK_TARGET_REL}")
        else:
            HOOK_TARGET.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(HOOK_TEMPLATE, HOOK_TARGET)
            mode = HOOK_TARGET.stat().st_mode
            HOOK_TARGET.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            changed.append(HOOK_TARGET_REL)
    elif force:
        # --force regenerates even when content matches — useful when a
        # template edit doesn't change rendered bytes but the test wants
        # a deterministic write.
        pass

    # 2. settings.json hook entry
    settings = load_settings()
    if not settings_have_hook(settings) or force:
        if dry_run:
            print(f"  MERGE hook entry into: {_rel(SETTINGS_PATH)}")
        else:
            new_settings = merge_hook_into_settings(dict(settings))
            if new_settings != settings:
                write_settings(new_settings)
                changed.append(_rel(SETTINGS_PATH))

    if dry_run:
        print("(dry run — no changes made)")
        return 0

    if not changed:
        print("✓ already installed and in sync")
        touch_marker()
        return 0

    for c in changed:
        print(f"✓ wrote: {c}")
    touch_marker()

    if not no_commit:
        subprocess.run(["git", "add", *changed], cwd=REPO, check=False)
        msg = (
            "issue-management: install PreToolUse gate ("
            + ", ".join(changed) + ")"
        )
        result = subprocess.run(
            ["git", "commit", "-m", msg],
            cwd=REPO, capture_output=True, text=True, check=False,
        )
        if result.returncode == 0:
            print("\n✓ committed; remember to push")
        else:
            stderr = result.stderr.strip()
            if "nothing to commit" in stderr.lower():
                print("\n(no commit: working tree clean)")
            else:
                print(f"\n(skipped commit: {stderr})")

    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="exit non-zero if anything is missing or drifted")
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing files from templates")
    ap.add_argument("--dry-run", action="store_true",
                    help="show planned changes without writing")
    ap.add_argument("--no-commit", action="store_true",
                    help="skip auto-commit after install")
    args = ap.parse_args()
    if args.check:
        return cmd_check()
    return cmd_install(
        force=args.force, dry_run=args.dry_run, no_commit=args.no_commit,
    )


if __name__ == "__main__":
    sys.exit(main())
