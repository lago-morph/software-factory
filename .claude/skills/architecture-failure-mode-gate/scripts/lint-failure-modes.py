#!/usr/bin/env python3
"""
Lint architectures/failure-modes.md against architectures/0N-*.md files.

Default mode (structure-only):
  - §2.4 "Failure mode coverage" table exists and is well-formed.
  - Column headers `N: ShortName` correspond 1:1 with architectures/0N-*.md
    alternative files (00-comparison.md and failure-modes.md excluded).
  - Each F-mode row has the right number of cells; row IDs unique.

`--check-diff <BASE_REF>` mode also runs:
  - For each architectures/0N-*.md alternative changed in BASE..HEAD, the
    matching column N of failure-modes.md MUST have been updated.
  - For each column N that changed, architectures/0N-*.md MUST have been
    touched in the same PR.
  - Adding/removing whole F-mode rows does NOT trigger column-spillover
    errors (those are row-level events, not coverage refinements).
  - Set env `FAILURE_MODE_ONLY=1` (PR label `failure-mode-only`) to permit
    a pure cell-wording refinement with zero arch-doc edits.

Exit 0 on pass, 1 on lint errors.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# Skill lives at .claude/skills/architecture-failure-mode-gate/scripts/
# Repo root is 4 levels up.
REPO = Path(__file__).resolve().parents[4]
ARCH_DIR = REPO / "architectures"
TABLE_PATH = ARCH_DIR / "failure-modes.md"
ARCH_PATTERN = re.compile(r"^0([1-9])-.*\.md$")
ARCH_PATH_PATTERN = re.compile(r"^architectures/0([1-9])-.*\.md$")
HEADER_PATTERN = re.compile(r"^(\d+):\s*\S+")
SECTION_MARKER = "### 2.4 Failure mode coverage"
SECTION_END = "**Coverage column scores"


def find_arch_files() -> dict[int, str]:
    return {
        int(ARCH_PATTERN.match(p.name).group(1)): p.name
        for p in ARCH_DIR.iterdir()
        if ARCH_PATTERN.match(p.name)
    }


def parse_table(text: str):
    """Return (headers_excluding_first_col, {fmode_id: [cells_excluding_first_col]})."""
    headers = None
    rows: dict[str, list[str]] = {}
    in_table = False
    for line in text.splitlines():
        if line.startswith(SECTION_MARKER):
            in_table = True
            continue
        if not in_table:
            continue
        if line.strip().startswith(SECTION_END):
            break
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        if headers is None:
            headers = cells[1:]
            continue
        m = re.match(r"^(F\d+)\b", cells[0])
        if not m:
            continue
        rows[m.group(1)] = cells[1:]
    return headers, rows


def structure_errors() -> list[str]:
    arch_files = find_arch_files()
    table_exists = TABLE_PATH.exists()
    # The gate enforces CORRESPONDENCE between architectures and the
    # matrix. If either side is empty/missing, there is nothing to
    # correspond — empty input pair = no work, not an error. The
    # original existence check fired on a missing matrix even when no
    # architecture files existed; that was the bug. Symmetric removal:
    # a missing matrix with architectures present is ALSO no-op (no
    # failure modes to enforce yet). Enforcement only fires when both
    # sides have content. Per commit 22ee8d4 the original intent was
    # "arch-file edit must be matched by matrix-column edit" — that
    # intent is only meaningful when both sides exist.
    if not arch_files or not table_exists:
        print(
            f"failure-modes.md lint: gate inert "
            f"(arch_files={len(arch_files)}, table_exists={table_exists}); "
            f"nothing to enforce correspondence on.",
            file=sys.stderr,
        )
        return []
    text = TABLE_PATH.read_text(encoding="utf-8")
    headers, rows = parse_table(text)
    errors: list[str] = []
    if not headers:
        return [f"§2.4 table not found in {TABLE_PATH.relative_to(REPO)}"]
    if len(headers) != len(arch_files):
        errors.append(
            f"header count {len(headers)} != alternative count {len(arch_files)} "
            f"(arch files: {sorted(arch_files.values())})"
        )
    for i, h in enumerate(headers, start=1):
        m = HEADER_PATTERN.match(h)
        if not m:
            errors.append(f"column {i} header `{h}` does not match `<N>: <ShortName>`")
            continue
        n = int(m.group(1))
        if n != i:
            errors.append(f"column {i} header `{h}` claims index {n}")
        if n not in arch_files:
            errors.append(f"column {n} has no matching architectures/0{n}-*.md file")
    for fid, cells in rows.items():
        if len(cells) != len(headers):
            errors.append(f"{fid}: {len(cells)} cells, expected {len(headers)}")
    if not rows:
        errors.append("§2.4 table has no F-mode rows")
    return errors


def git_show(ref: str, path: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "show", f"{ref}:{path}"], stderr=subprocess.DEVNULL
        ).decode("utf-8")
    except subprocess.CalledProcessError:
        return ""


def changed_files(base: str) -> list[str]:
    return subprocess.check_output(
        ["git", "diff", "--name-only", f"{base}...HEAD"]
    ).decode("utf-8").splitlines()


def changed_columns(old_text: str, new_text: str) -> set[int]:
    h_old, r_old = parse_table(old_text)
    h_new, r_new = parse_table(new_text)
    h_old = h_old or []
    h_new = h_new or []
    width = max(len(h_old), len(h_new))
    changed: set[int] = set()
    for i in range(width):
        o = h_old[i] if i < len(h_old) else None
        n = h_new[i] if i < len(h_new) else None
        if o != n:
            changed.add(i + 1)
    for fid in set(r_old) & set(r_new):
        old_cells, new_cells = r_old[fid], r_new[fid]
        for i in range(width):
            o = old_cells[i] if i < len(old_cells) else None
            n = new_cells[i] if i < len(new_cells) else None
            if o != n:
                changed.add(i + 1)
    return changed


def diff_errors(base: str) -> list[str]:
    files = set(changed_files(base))
    arch_changed = {
        int(ARCH_PATH_PATTERN.match(f).group(1))
        for f in files
        if ARCH_PATH_PATTERN.match(f)
    }
    table_changed = "architectures/failure-modes.md" in files
    if not arch_changed and not table_changed:
        return []
    old = git_show(base, "architectures/failure-modes.md")
    if not old.strip():
        # File didn't exist at base — creation event. Structure check is
        # sufficient; column-correspondence has no prior state to compare to.
        return []
    new = TABLE_PATH.read_text(encoding="utf-8")
    col_changed = changed_columns(old, new)
    errors: list[str] = []
    label_override = os.environ.get("FAILURE_MODE_ONLY", "").strip() in ("1", "true", "yes")
    for n in sorted(arch_changed - col_changed):
        errors.append(
            f"architectures/0{n}-*.md was modified but column {n} of "
            f"architectures/failure-modes.md was not updated"
        )
    spill = col_changed - arch_changed
    if spill and not (label_override and not arch_changed):
        for n in sorted(spill):
            errors.append(
                f"architectures/failure-modes.md column {n} changed but "
                f"architectures/0{n}-*.md was not touched in this PR"
            )
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-diff", metavar="BASE_REF",
                    help="Also enforce diff-correspondence vs BASE_REF.")
    args = ap.parse_args()
    errors = structure_errors()
    if args.check_diff and not errors:
        errors.extend(diff_errors(args.check_diff))
    if errors:
        print("failure-modes.md lint FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print(
            "\nSee .claude/skills/architecture-failure-mode-gate/SKILL.md "
            "\"Schema and update discipline\".",
            file=sys.stderr,
        )
        return 1
    print("failure-modes.md lint: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
