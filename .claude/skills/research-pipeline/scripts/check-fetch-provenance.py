"""Check fetch_provenance hygiene against the catalog.

Rules:
    - If any file in a record has completeness=complete AND that file has
      fetch_provenance with status=open, that's an error: the issue/PR should
      be closed/merged and the branch deleted.
    - Files marked have but with fetch_provenance.status=open are warnings
      (the work is mid-flight; should resolve soon).
    - fetch_provenance with issue_number set but no branch is a warning
      (the issue was filed but the action hasn't produced a branch yet).

Exit:
    0 = clean
    1 = errors
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _config import data_path, ConfigError  # noqa: E402


def main() -> int:
    try:
        data_p = data_path()
    except ConfigError as e:
        print(f"✗ Config error: {e}", file=sys.stderr)
        return 1

    if not data_p.exists():
        print(f"✗ {data_p} does not exist", file=sys.stderr)
        return 1
    try:
        data = json.loads(data_p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"✗ JSON parse error: {e}", file=sys.stderr)
        return 1

    errors = []
    warnings = []

    for record_id, record in data.items():
        if not isinstance(record, dict):
            continue
        files = record.get("files", []) or []
        for i, f in enumerate(files):
            if not isinstance(f, dict):
                continue
            prov = f.get("fetch_provenance")
            if not prov or not isinstance(prov, dict):
                continue
            status = prov.get("status")
            completeness = f.get("completeness")
            ingestion = f.get("ingestion_status")

            issue = prov.get("issue_number")
            pr = prov.get("pr_number")
            branch = prov.get("branch")

            label = f"{record_id} files[{i}]"

            if completeness == "complete" and status == "open":
                actions = []
                if issue:
                    actions.append(f"close issue #{issue}")
                if pr:
                    actions.append(f"merge or close PR #{pr}")
                if branch:
                    actions.append(f"delete branch {branch}")
                action_str = "; ".join(actions) if actions else "review fetch_provenance"
                errors.append(
                    f"{label}: completeness=complete but fetch_provenance.status=open. "
                    f"Suggested: {action_str}"
                )
            elif ingestion == "have" and status == "open":
                warnings.append(
                    f"{label}: file present but fetch_provenance.status=open — resolve soon"
                )

            if issue and not branch and status == "open":
                warnings.append(
                    f"{label}: fetch_provenance has issue #{issue} but no branch — action may not have completed"
                )

    for e in errors:
        print(f"✗ {e}", file=sys.stderr)
    for w in warnings:
        print(f"⚠ {w}", file=sys.stderr)

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)", file=sys.stderr)
        return 1
    if warnings:
        print(f"\n✓ fetch_provenance OK ({len(warnings)} warning(s))")
        return 0
    print("✓ fetch_provenance OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
