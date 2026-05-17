---
name: self-bootstrapping-skill
description: Apply the self-bootstrapping pattern when authoring or modifying a skill that ships artifacts the consumer repo needs installed (GitHub Actions workflows, JSON schemas, config files, scripts wired into CI). Use whenever you're building a skill that produces files outside the skill directory, or fixing a skill that requires a manual install step the user keeps forgetting. The pattern: ship templates in the skill, write an install script with --check and --force modes, put a no-prompt pre-flight in SKILL.md, and add a CI gate that detects drift. Triggers on phrases like "skill should install itself", "self-syncing", "copy the skill and setup is automatic", "drift between template and installed", or proactively when authoring a skill whose first line of documentation tells users to "run the install script".
tags: [skill-authoring, infrastructure, ci, self-installing]
allowed-tools: [Bash, Read, Write, Edit]
---

# self-bootstrapping-skill

A pattern (not a single workflow) for skills that ship derived artifacts the consumer repo needs to install. The contract this pattern enforces: **copy the skill directory into a repo, and setup is done automatically — no user prompt, no forgotten install step, no drift between templates and installed copies**.

## When to apply

Use this pattern when the skill you're authoring or modifying:
- Ships GitHub Actions workflows that must live at `.github/workflows/`
- Ships a JSON Schema, config file, or other data-shape definition the consumer needs at a fixed canonical path
- Has any "installation artifact" that derives mechanically from a template

Do **NOT** apply this pattern for:
- Skills whose only artifacts are markdown documentation (no install needed)
- Files containing user-edited content (auto-overwrite would clobber)
- Anything requiring user-specific values the skill can't infer (API keys, account IDs)

## Why this exists

The traditional pattern asks users to run an install script after copying a skill. This fails reliably:
- Users skip it.
- Sessions started before the install fire fail mysteriously.
- When template files change, installed copies drift silently until someone notices.

The `research-pipeline` skill in this repo lived without its workflows installed for 6 PRs (#79-#84) because nobody ran `install-workflows.py`. The render-markdown auto-regen never fired. The user explicitly demanded the pattern be self-syncing.

## The pattern (5 elements)

### 1. Templates under `resources/_<artifact-class>/`

Templates use `__PLACEHOLDER__` tokens for values that vary per consumer repo. Typical placeholders:
- `__SKILL_PATH__` — where the skill is mounted in the consumer (e.g., `.claude/skills/research-pipeline`)
- `__REPO_OWNER__` / `__REPO_NAME__` — for GitHub-specific files

Placeholder substitution comes from the skill's own config (a YAML block in SKILL.md, a JSON config file, etc.).

### 2. Installer script `scripts/install-<artifacts>.py`

Three modes:

| Flag | Behavior |
|------|----------|
| (none) | Install missing files. Don't overwrite existing. Log drift to stderr. |
| `--check` | Read-only audit. Exit 0 if installed == template (after substitution). Exit 1 if missing or drifted. Exit 2 if template itself is missing (skill-install defect). |
| `--force` | Install all, overwriting any existing. Auto-commit on changes. |

`--force` is the recovery mode. The skill's pre-flight runs `--check` and falls back to `--force` on mismatch.

Common helper:
```python
def render_template(template_path: Path, **substitutions) -> str:
    text = template_path.read_text(encoding="utf-8")
    for token, value in substitutions.items():
        text = text.replace(f"__{token.upper()}__", value)
    return text
```

Both `--check` and the install path use the same rendering function.

### 3. SKILL.md pre-flight section

Mandatory section, near the top, before any task-specific content:

```markdown
## Pre-flight check (run this first, every invocation) — self-syncing

The skill is self-syncing. The canonical source for all <artifacts> is
`resources/_<artifact-class>/` inside this skill directory. The copies under
`<consumer-canonical-location>/` must always match the templates.

Before any task:
\`\`\`bash
python <skill-path>/scripts/install-<artifacts>.py --check
\`\`\`

- Exit 0 → proceed.
- Exit 1 → missing or drifted. **Auto-fix by running, without asking the user:**
  \`\`\`bash
  python <skill-path>/scripts/install-<artifacts>.py --force
  \`\`\`
  Then continue. The install auto-commits; push it as part of your work.
- Exit 2 → template missing from the skill itself. Surface to user and stop.

**Do not ask the user before installing/syncing.** The install is mechanical
and recoverable — every artifact is regenerated from a template; nothing
custom is destroyed.
```

The "no user prompt" wording is load-bearing. Without it, future agents reading the skill will revert to the "ask the user" default.

### 4. CI gate workflow

Add a workflow that runs `--check` on every PR touching the skill:

```yaml
name: Test <skill-name>
on:
  pull_request:
    paths: ['.claude/skills/<skill-name>/**']
jobs:
  drift-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
      - name: Workflow drift check
        run: python .claude/skills/<skill-name>/scripts/install-<artifacts>.py --check
```

This gate is *itself* one of the skill's installed artifacts — a satisfying recursion. Template edits that don't propagate to installed files block the PR.

### 5. First-commit bootstrap

The PR that introduces the skill runs the installer once in its commit history. The auto-commit lands the initial artifacts alongside the skill directory. After that first commit, the pattern self-perpetuates — future sessions invoke pre-flight, which keeps things in sync.

## Concrete example — research-pipeline workflows

See `.claude/skills/research-pipeline/scripts/install-workflows.py` for a complete reference implementation. It installs three GitHub Actions workflows from templates in `resources/_workflows/`, substituting `__SKILL_PATH__` from the config block in the skill's own SKILL.md.

## Anti-patterns

- **"Run install.sh after copying the skill"** — relies on user memory. Fails immediately.
- **Asking the user on every invocation** — friction without safety; the user already consented by copying the skill.
- **Auto-overwriting user-editable files with `--force`** — would clobber user edits. Reserve `--force` for templated artifacts only. For files users edit, `--check` reports drift but `--force` refuses without an additional `--clobber` flag.
- **Hardcoded paths in installer** — defeats portability. Always substitute placeholders from config.
- **Skipping the CI gate** — without `--check` running on every PR, template edits silently desync from installed files.
- **Confusing "drift detection" with "intentional manual edit"** — if users are expected to edit the installed file, it's not a derived artifact and this pattern doesn't apply.

## Acceptance criteria

A skill correctly applies this pattern when:

1. `--check` distinguishes missing / drifted / in-sync with three exit codes.
2. `--force` installs and auto-commits with a clear message.
3. SKILL.md pre-flight documents the no-prompt contract explicitly.
4. A CI workflow (itself installed by the script) runs `--check` on every PR touching the skill.
5. Copying the skill into a fresh repo + running an LLM-driven first invocation results in fully-installed artifacts with no user prompts.
6. Editing a template + running an LLM-driven next invocation triggers a `--force` re-install visible in the commit diff.

## Files this pattern creates

In the skill itself:
- `scripts/install-<artifacts>.py` — installer with three modes
- `resources/_<artifact-class>/*.template` — templates with placeholders
- `SKILL.md` — pre-flight section using the no-prompt pattern

In the consumer repo (installed by the script):
- `<canonical-location>/<artifact>` — the installed files
- (one of them: a CI workflow that runs `--check`)

## See also

- [ADR 0006 — skill self-bootstrapping](../../../retrospective/2026-05-17-85/ADR-0006-skill-self-bootstrapping.md) — design rationale
- [ADR 0010 — mechanical recovery autonomous](../../../retrospective/2026-05-17-85/ADR-0010-mechanical-recovery-autonomous.md) — the no-prompt principle
- `.claude/skills/research-pipeline/scripts/install-workflows.py` — reference implementation
