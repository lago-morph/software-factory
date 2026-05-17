"""Install the three pipeline workflow YAMLs into .github/workflows/.

Reads templates from resources/_workflows/, substitutes __SKILL_PATH__ with
the value from the SKILL.md config block, and writes to .github/workflows/.
Skips files that already exist unless --force is passed.

Usage:
    python install-workflows.py            # install missing ones
    python install-workflows.py --force    # overwrite any existing ones
    python install-workflows.py --dry-run  # show what would happen

Idempotent: running twice with no --force is a no-op on the second run.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import load_config, repo_root, ConfigError  # noqa: E402

WORKFLOW_FILES = [
    "regen-sources-md-auto.yml",
    "regen-sources-md-manual.yml",
    "test-research-pipeline.yml",
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="overwrite existing workflow files")
    ap.add_argument("--dry-run", action="store_true", help="just print what would happen")
    ap.add_argument("--no-commit", action="store_true", help="don't git-add+commit installed files")
    args = ap.parse_args()

    try:
        cfg = load_config()
    except ConfigError as e:
        print(f"✗ Config error: {e}", file=sys.stderr)
        return 1

    skill_path_str = cfg["skill_path"]
    root = repo_root()
    skill_dir = root / skill_path_str
    templates_dir = skill_dir / "resources" / "_workflows"
    workflows_dir = root / ".github" / "workflows"

    if not templates_dir.exists():
        print(f"✗ Templates directory not found: {templates_dir}", file=sys.stderr)
        return 1

    workflows_dir.mkdir(parents=True, exist_ok=True)

    installed = []
    skipped = []
    overwrote = []

    for name in WORKFLOW_FILES:
        template = templates_dir / name
        target = workflows_dir / name

        if not template.exists():
            print(f"✗ Template missing: {template}", file=sys.stderr)
            return 1

        if target.exists() and not args.force:
            skipped.append(name)
            continue

        # Read template, substitute placeholder, write
        content = template.read_text(encoding="utf-8")
        rendered = content.replace("__SKILL_PATH__", skill_path_str)

        if args.dry_run:
            action = "OVERWRITE" if target.exists() else "INSTALL"
            print(f"  {action}: .github/workflows/{name}")
            continue

        if target.exists():
            overwrote.append(name)
        else:
            installed.append(name)
        target.write_text(rendered, encoding="utf-8")

    if args.dry_run:
        print("(dry run — no changes made)")
        return 0

    # Summary
    if installed:
        print(f"✓ installed: {', '.join(installed)}")
    if overwrote:
        print(f"✓ overwrote: {', '.join(overwrote)}")
    if skipped:
        print(f"  skipped (already present, use --force to replace): {', '.join(skipped)}")

    # Optional git add + commit
    if (installed or overwrote) and not args.no_commit:
        files_to_add = [str(workflows_dir / n) for n in installed + overwrote]
        subprocess.run(["git", "add"] + files_to_add, cwd=root, check=False)
        msg = f"Install research-pipeline workflows: {', '.join(installed + overwrote)}"
        result = subprocess.run(
            ["git", "commit", "-m", msg],
            cwd=root, capture_output=True, text=True, check=False,
        )
        if result.returncode == 0:
            print("\n✓ committed; remember to push")
        else:
            # Probably nothing staged; not fatal
            print(f"\n(skipped commit: {result.stderr.strip()})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
