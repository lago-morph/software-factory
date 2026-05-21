#!/usr/bin/env python3
"""Install the issue-management PreToolUse gates.

Two hooks ship with this skill:

  1. The hard gate: `require-issue-management-skill.sh`, matched on
     `mcp__github__issue_*` / `add_issue_comment` / `list_issues` /
     `search_issues` / `sub_issue_write`. Blocks issue-touching MCP
     calls unless the skill has been loaded in this session.
  2. The AskUserQuestion reminder:
     `remind-questions-on-askuserquestion.sh`, matched on
     `AskUserQuestion`. Fires once per call when the skill is loaded,
     exiting 2 with a short reminder so the agent considers whether the
     question is about an in-flight issue (and therefore a QUESTIONS
     event needing an issue-thread comment + `question` label).

Each is two artifacts living outside the skill directory:

  .claude/hooks/<script>.sh         (hook script)
  .claude/settings.json             (hook registration)

Both are installed from templates that ship with this skill. Idempotent
by design — running with --check tells you whether anything is drifted
or missing; running with --force regenerates the scripts and merges the
hook entries into settings.json without disturbing other entries.

Also touches the per-session marker at
    /tmp/.claude-skill-loaded-issue-management
when --check returns 0 (or when --force completes successfully). That
marker is what both hooks look for. Touching it here means: every time
the agent runs the skill's pre-flight, the skill is signalled "loaded
for this session", and the hard gate trusts the next issue-touching
tool call (while the AskUserQuestion reminder begins firing).

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

SETTINGS_PATH = REPO / ".claude" / "settings.json"

MARKER = Path("/tmp/.claude-skill-loaded-issue-management")


class HookSpec:
    """One PreToolUse hook entry: script template + matcher + description."""

    def __init__(
        self,
        *,
        template_name: str,
        target_rel: str,
        matcher: str,
        description: str,
    ) -> None:
        self.template = SKILL_DIR / "resources" / "hooks" / template_name
        self.target_rel = target_rel
        self.target = REPO / target_rel
        self.matcher = matcher
        self.command = target_rel
        self.description = description


# The hard gate. Covers every MCP tool that names or lists an issue.
HARD_GATE = HookSpec(
    template_name="require-issue-management-skill.sh",
    target_rel=".claude/hooks/require-issue-management-skill.sh",
    matcher=(
        "mcp__github__("
        "issue_read|issue_write|add_issue_comment|"
        "list_issues|search_issues|sub_issue_write"
        ")"
    ),
    description="issue-management: require skill load before issue tools",
)

# AskUserQuestion reminder. Fires once per call when the skill is
# loaded, so the agent has to actively consider whether a question is
# about an in-flight issue (the QUESTIONS behavior).
ASK_REMINDER = HookSpec(
    template_name="remind-questions-on-askuserquestion.sh",
    target_rel=".claude/hooks/remind-questions-on-askuserquestion.sh",
    matcher="AskUserQuestion",
    description="issue-management: remind AskUserQuestion-is-QUESTIONS rule",
)

HOOKS: list[HookSpec] = [HARD_GATE, ASK_REMINDER]

REQUIRED_SKILL_FILES = [
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "scripts" / "install.py",
    *(h.template for h in HOOKS),
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


def hook_script_matches(spec: HookSpec) -> bool:
    if not spec.target.exists():
        return False
    expected = spec.template.read_text(encoding="utf-8")
    actual = spec.target.read_text(encoding="utf-8")
    return expected == actual


def hook_script_executable(spec: HookSpec) -> bool:
    if not spec.target.exists():
        return False
    return bool(spec.target.stat().st_mode & stat.S_IXUSR)


def load_settings() -> dict:
    if not SETTINGS_PATH.exists():
        return {}
    try:
        return json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"✗ {_rel(SETTINGS_PATH)} is not valid JSON: {e}")


def settings_have_hook(settings: dict, spec: HookSpec) -> bool:
    pre = settings.get("hooks", {}).get("PreToolUse", [])
    for entry in pre:
        if entry.get("matcher") != spec.matcher:
            continue
        for h in entry.get("hooks", []):
            if h.get("type") == "command" and h.get("command") == spec.command:
                return True
    return False


def merge_hook_into_settings(settings: dict, spec: HookSpec) -> dict:
    hooks_root = settings.setdefault("hooks", {})
    pre = hooks_root.setdefault("PreToolUse", [])

    # Remove any prior entry with our exact matcher so we can write a
    # canonical one. This keeps the file deterministic even after a
    # template edit.
    pre = [
        entry for entry in pre
        if entry.get("matcher") != spec.matcher
    ]

    pre.append({
        "matcher": spec.matcher,
        "hooks": [
            {
                "type": "command",
                "command": spec.command,
                "description": spec.description,
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
    settings = load_settings()
    for spec in HOOKS:
        if not spec.target.exists():
            problems.append(f"missing: {spec.target_rel}")
        elif not hook_script_matches(spec):
            problems.append(f"drifted: {spec.target_rel} (template ≠ installed)")
        elif not hook_script_executable(spec):
            problems.append(f"not executable: {spec.target_rel}")

        if not settings_have_hook(settings, spec):
            problems.append(
                f"missing hook entry for matcher `{spec.matcher}` in {_rel(SETTINGS_PATH)}"
            )

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
    print(f"✓ issue-management gates installed and in sync ({len(HOOKS)} hook(s))")
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

    # 1. Each hook script
    for spec in HOOKS:
        need_script = (
            not spec.target.exists()
            or not hook_script_matches(spec)
            or not hook_script_executable(spec)
        )
        if need_script:
            if dry_run:
                action = "OVERWRITE" if spec.target.exists() else "INSTALL"
                print(f"  {action}: {spec.target_rel}")
            else:
                spec.target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(spec.template, spec.target)
                mode = spec.target.stat().st_mode
                spec.target.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                changed.append(spec.target_rel)
        elif force:
            pass

    # 2. settings.json hook entries (one per spec)
    settings = load_settings()
    settings_changed = False
    new_settings = dict(settings)
    for spec in HOOKS:
        if not settings_have_hook(new_settings, spec) or force:
            if dry_run:
                print(
                    f"  MERGE hook entry (matcher `{spec.matcher}`) into: "
                    f"{_rel(SETTINGS_PATH)}"
                )
            else:
                before = json.dumps(new_settings, sort_keys=True)
                new_settings = merge_hook_into_settings(new_settings, spec)
                after = json.dumps(new_settings, sort_keys=True)
                if before != after:
                    settings_changed = True
    if settings_changed and not dry_run:
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
