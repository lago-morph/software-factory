# Spec: `self-bootstrapping-skill`

## Intent

Many skills ship with derived artifacts the consumer repo needs installed: GitHub Actions workflows, config files, scripts wired into CI, schemas. The traditional pattern asks the user "do you want to install these?" on first run, which adds friction and leaves repos inconsistent if users skip. This skill bakes in a different contract: **copy the skill directory and setup is automatic** — the skill detects missing or drifted artifacts on every invocation and installs/syncs them without asking. The install must be mechanical and recoverable (every artifact regenerated from a template; nothing custom is destroyed). This pattern emerged from PR #85 of the `software-factory` project, where the research-pipeline skill ships 3 workflow YAMLs that must stay in lockstep with templates inside the skill directory.

## Trigger

Use this pattern when authoring a skill that:
- Ships GitHub Actions workflows that need to be in `.github/workflows/`
- Ships a JSON schema, config file, or other data-shape definition the consumer repo needs at a fixed path
- Has any "installation artifact" that derives mechanically from a template

Do NOT use this pattern for:
- Skills whose only artifacts are markdown documentation (no installation needed)
- Files that contain user-edited content (auto-regen would clobber)
- Anything that requires user-specific values the skill can't know (e.g., API keys)

## Inputs

Skill template files under `resources/<artifact-class>/` (e.g., `resources/_workflows/*.yml`). Templates use `__PLACEHOLDER__` tokens for repo-specific values (skill path, repo owner, etc.) substituted from the skill's config.

## Outputs

Installed/synced artifact files at their canonical consumer locations. Auto-commit with a clear message ("Install <skill> artifacts: …" or "Sync <skill> artifacts (template drift)").

## Workflow

1. **Write an installer script** (`scripts/install-<artifacts>.py`) with three modes:
   - **No flags** (default): install missing, leave existing alone, warn on drift.
   - **`--check`**: read-only audit. Exit 0 if all installed and identical to templates (after placeholder substitution). Exit 1 if any missing or drifted. Exit 2 if template missing (skill-install defect).
   - **`--force`**: install all, overwriting any existing. Auto-commit on changes.
2. **Implement drift detection**: compare rendered template content (with placeholders substituted using current config) against installed file content byte-for-byte. Don't rely on hashes — substitution is deterministic.
3. **Add `render_template(template_path, **substitutions) -> str` helper** so check and install share rendering logic.
4. **Write SKILL.md pre-flight section**:
   ```markdown
   ## Pre-flight — self-syncing
   Before any operation:
   ```bash
   python scripts/install-<artifacts>.py --check
   ```
   Exit 1 → run `--force` *without asking the user*. The install is mechanical and recoverable.
   ```
5. **Document the why**: a paragraph in pre-flight explaining the no-prompt contract — install is deterministic, every file regenerated from template, nothing custom is destroyed.
6. **Test it**: a CI workflow (one of the artifacts the skill installs!) runs `--check` as a gate. Template edits that don't propagate to installed files block the PR.
7. **One-time bootstrap**: in the skill's first commit, run the installer once. The auto-commit lands the initial artifacts alongside the skill itself.

## Concrete examples

### Example 1: install-workflows.py for the research-pipeline skill

```python
WORKFLOW_FILES = ["regen-sources-md-auto.yml", "regen-sources-md-manual.yml", "test-research-pipeline.yml"]

def render_template(template: Path, skill_path_str: str) -> str:
    return template.read_text().replace("__SKILL_PATH__", skill_path_str)

# --check mode
if args.check:
    missing, drifted = [], []
    for name in WORKFLOW_FILES:
        template = templates_dir / name
        target = workflows_dir / name
        if not target.exists():
            missing.append(name); continue
        if render_template(template, skill_path) != target.read_text():
            drifted.append(name)
    if missing or drifted:
        for n in missing: print(f"  missing: {n}", file=sys.stderr)
        for n in drifted: print(f"  drifted: {n}", file=sys.stderr)
        return 1
    print(f"✓ all {len(WORKFLOW_FILES)} in sync")
    return 0
```

SKILL.md pre-flight:
> Run `python scripts/install-workflows.py --check`. On exit 1, run `--force` **without asking the user**. The install is mechanical and recoverable.

### Example 2: bootstrap categories.json from skill template

A schema or config file the consumer needs at a fixed path can use the same pattern. Template at `resources/_catalog/categories.bootstrap.json`; check that `reference-only/categories.json` exists and matches; if missing or empty, install from the bootstrap; if user has edited it (drift), DO NOT auto-overwrite (this is the exception — config files contain user choices that shouldn't be clobbered). For config files, `--check` reports drift but `--force` refuses to overwrite without an additional `--clobber` flag.

## Anti-patterns

- **Asking the user "install now?" on every run** — the whole point is to bypass that question. The user already opted in by copying the skill into the repo.
- **Hardcoding the installed paths** — templates use placeholders substituted from the skill's config (which knows the skill's own location, repo identity, etc.) so the skill is portable to any repo layout.
- **Skipping the CI gate** — without a workflow that runs `--check` on every PR, template edits silently desync from installed files. The CI gate is what enforces the lockstep.
- **Auto-overwriting user-editable files** — drift detection is fine; auto-overwrite is dangerous for anything the user might have customized. Reserve `--force` for genuinely-derived artifacts.
- **Confusing "drift" with "intentional manual edit"** — if users are expected to edit the installed file, it's not a derived artifact and this pattern doesn't apply. Move it to a `.example` template they copy manually.

## Acceptance criteria

1. `--check` correctly distinguishes missing / drifted / in-sync.
2. `--force` installs and auto-commits with a clear message.
3. SKILL.md pre-flight section documents the no-prompt contract with rationale.
4. A CI workflow runs `--check` on every PR touching the skill.
5. Copying the skill into a fresh repo + running the LLM-driven first invocation results in fully-installed artifacts with no user prompts.
6. Editing a template + running the LLM-driven next invocation results in `--force` re-install with drift visible in the commit diff.

## Files this skill creates / modifies

- `scripts/install-<artifacts>.py` — the installer with --check/--force/--dry-run/--no-commit flags.
- `resources/<artifact-class>/*.template` — template files with `__PLACEHOLDER__` tokens.
- SKILL.md — pre-flight section using the self-syncing pattern.
- A CI workflow that runs `--check` as a merge gate.
