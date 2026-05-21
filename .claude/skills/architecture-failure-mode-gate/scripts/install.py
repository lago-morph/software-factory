#!/usr/bin/env python3
"""Install architecture-failure-mode-gate workflow into .github/workflows/.

Reads templates from resources/_workflows/, substitutes __SKILL_PATH__ with
this skill's mount path, and writes to .github/workflows/. Mirrors the
research-pipeline install-workflows.py contract:

    python install.py            # install missing ones
    python install.py --check    # exit non-zero if installed != templates
    python install.py --force    # overwrite any existing ones
    python install.py --dry-run  # show what would happen
    python install.py --no-commit  # don't git-add+commit installed files

The skill's self-syncing pre-flight uses --check + --force to keep
.github/workflows/ in lockstep with resources/_workflows/ automatically.

Exit codes:
    0 — in sync (--check) or install succeeded
    1 — missing or drifted (--check) or install error
    2 — template missing from skill (skill-installation defect)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_PATH = ".claude/skills/architecture-failure-mode-gate"
REPO = Path(__file__).resolve().parents[4]
TEMPLATES_DIR = SKILL_DIR / "resources" / "_workflows"
WORKFLOWS_DIR = REPO / ".github" / "workflows"

WORKFLOW_FILES = ["failure-modes-gate.yml"]

# Files INSIDE the skill that other components (CI workflow, agent CLI)
# reference by path. If any is missing, the skill installation is broken
# and --check returns exit 2. We do NOT regenerate these — they ship with
# the skill itself; their absence means the skill was incompletely copied.
REQUIRED_SKILL_FILES = [
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "scripts" / "lint-failure-modes.py",
    SKILL_DIR / "scripts" / "install.py",
    SKILL_DIR / "resources" / "_workflows" / "failure-modes-gate.yml",
]


def check_skill_intact() -> list[str]:
    missing = [p for p in REQUIRED_SKILL_FILES if not p.exists()]
    return [str(p.relative_to(REPO)) for p in missing]


def render_template(template: Path) -> str:
    return template.read_text(encoding="utf-8").replace("__SKILL_PATH__", SKILL_PATH)


def cmd_check() -> int:
    skill_missing = check_skill_intact()
    if skill_missing:
        print("✗ Skill installation is incomplete. Missing skill-internal files:",
              file=sys.stderr)
        for m in skill_missing:
            print(f"  - {m}", file=sys.stderr)
        print(
            "\nThis is a skill-install defect (not a workflow-drift issue) — "
            "the skill directory was copied incompletely or a file was deleted. "
            "Re-copy the skill from its source.",
            file=sys.stderr,
        )
        return 2
    missing: list[str] = []
    drifted: list[str] = []
    for name in WORKFLOW_FILES:
        template = TEMPLATES_DIR / name
        target = WORKFLOWS_DIR / name
        if not template.exists():
            print(f"✗ Template missing: {template.relative_to(REPO)}", file=sys.stderr)
            return 2
        if not target.exists():
            missing.append(name)
            continue
        expected = render_template(template)
        actual = target.read_text(encoding="utf-8")
        if expected != actual:
            drifted.append(name)
    if missing or drifted:
        for n in missing:
            print(f"  missing: {n}", file=sys.stderr)
        for n in drifted:
            print(f"  drifted: {n} (template ≠ installed)", file=sys.stderr)
        print(
            f"\n{len(missing)} missing, {len(drifted)} drifted. "
            f"Fix with: python {SKILL_PATH}/scripts/install.py --force",
            file=sys.stderr,
        )
        return 1
    print(f"✓ all {len(WORKFLOW_FILES)} workflow(s) in sync with templates")
    return 0


def cmd_install(force: bool, dry_run: bool, no_commit: bool) -> int:
    skill_missing = check_skill_intact()
    if skill_missing:
        print("✗ Skill installation is incomplete. Missing skill-internal files:",
              file=sys.stderr)
        for m in skill_missing:
            print(f"  - {m}", file=sys.stderr)
        return 2
    WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    skipped: list[str] = []
    overwrote: list[str] = []

    for name in WORKFLOW_FILES:
        template = TEMPLATES_DIR / name
        target = WORKFLOWS_DIR / name
        if not template.exists():
            print(f"✗ Template missing: {template.relative_to(REPO)}", file=sys.stderr)
            return 2

        if target.exists() and not force:
            expected = render_template(template)
            actual = target.read_text(encoding="utf-8")
            if expected != actual:
                print(f"  {name}: DRIFT (use --force to overwrite)", file=sys.stderr)
            skipped.append(name)
            continue

        rendered = render_template(template)
        if dry_run:
            action = "OVERWRITE" if target.exists() else "INSTALL"
            print(f"  {action}: .github/workflows/{name}")
            continue

        (overwrote if target.exists() else installed).append(name)
        target.write_text(rendered, encoding="utf-8")

    if dry_run:
        print("(dry run — no changes made)")
        return 0

    if installed:
        print(f"✓ installed: {', '.join(installed)}")
    if overwrote:
        print(f"✓ overwrote: {', '.join(overwrote)}")
    if skipped:
        print(f"  skipped (already present, use --force to replace): {', '.join(skipped)}")

    if (installed or overwrote) and not no_commit:
        paths = [str((WORKFLOWS_DIR / n).relative_to(REPO)) for n in installed + overwrote]
        subprocess.run(["git", "add", *paths], cwd=REPO, check=False)
        msg = f"Install architecture-failure-mode-gate workflow: {', '.join(installed + overwrote)}"
        result = subprocess.run(
            ["git", "commit", "-m", msg],
            cwd=REPO, capture_output=True, text=True, check=False,
        )
        if result.returncode == 0:
            print("\n✓ committed; remember to push")
        else:
            print(f"\n(skipped commit: {result.stderr.strip()})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-commit", action="store_true")
    args = ap.parse_args()
    if args.check:
        return cmd_check()
    return cmd_install(force=args.force, dry_run=args.dry_run, no_commit=args.no_commit)


if __name__ == "__main__":
    sys.exit(main())
