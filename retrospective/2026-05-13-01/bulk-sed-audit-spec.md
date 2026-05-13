# Spec: `bulk-sed-audit`

## Intent

Bulk `sed -i` operations on multiple files (for path renames, terminology updates, link migrations) are fast but easy to over-reach. A regex like `s|research/manual/|reference-only/|g` will match every occurrence, including ones in narrative prose that documented historical state. Once committed, the damage propagates: a future reader sees `reference-only/The Dark Factory How Software Is Le.txt` and tries to open a path that doesn't exist.

This skill solves a specific failure pattern from the 2026-05-13 session: a bulk sed for path rewriting was committed without per-file diff inspection. The first audit pass caught four mangled citations in `research/07-dark-factory.md` whose original `research/manual/<file>` paths had been historical-provenance references (pointing at temporary cache files that no longer existed). The mangled paths read `reference-only/<file>` — but the file was at `reference-only/dark-factory-article.txt` after a rename. Recovery required restoring three files from git history with new names + four targeted re-edits.

The cost of running this skill on a planned bulk sed is one extra `git diff` review. The cost of NOT running it is a sed regression that propagates through every audit pass until a careful reader catches it.

## Trigger

**Direct user phrases:**
- "Rename this path everywhere"
- "Bulk replace X with Y"
- "Migrate all references from A to B"

**Proactive triggers (run without being asked):**
- Before any `sed -i` invocation with a `g` (global) flag across >2 files.
- Before any `find ... -exec sed -i` or piped `xargs sed -i`.
- When migrating paths after `git mv` of a directory.

**Negative triggers:**
- Single-file targeted edits (use `Edit` tool instead).
- Replacements with unique target strings unlikely to false-match (e.g., a UUID or a fully-qualified URL).

## Inputs

- The replacement pattern (`sed` script or before/after strings).
- The file set to apply it to (explicit list or glob).
- Optional: paths to preserve unchanged (historical narrative).

## Outputs

- A list of files matched by the search but skipped per "preserve" rule.
- A list of changes applied per file, with line numbers.
- A `git diff` for review before committing.

## Workflow

1. **Identify the search pattern's match set.** Run grep first, without sed:

   ```bash
   grep -nE "<pattern>" <file-glob> | sort
   ```

   This gives you every line that would be modified. Read the output. Look for:
   - Lines where the match is **inside narrative prose** (historical "we used to have X at this path") — these should typically NOT be modified.
   - Lines where the match is **in a literal path context** (after `` ` ``, in a list of files, in a citation) — these SHOULD be modified.

2. **Decide the scope per file.** Classify each grep hit:
   - **Apply** — the match is in live code or live citation.
   - **Preserve** — the match is historical narrative.
   - **Edit individually** — the match needs case-by-case judgment (e.g., a path that was moved AND renamed).

3. **For "Apply" files: run sed, then verify diff per file.**

   ```bash
   for f in <apply-list>; do
     sed -i 's|<pattern>|<replacement>|g' "$f"
   done
   git diff -- <apply-list>
   ```

   Read every diff hunk. Flag any that looks off (e.g., a match inside a sentence that now reads ungrammatically).

4. **For "Edit individually" files: use `Edit` tool with sufficient unique context** to target only the intended line.

5. **For "Preserve" files: skip.** Re-grep them to confirm no accidental changes.

6. **Verify forward references resolve.** After all changes, for every new path introduced, test existence:

   ```bash
   grep -oE '`<new-path-pattern>`' --include="*.md" -r . | tr -d '`' | sort -u | while read p; do
     [ -e "$p" ] && echo "OK $p" || echo "MISS $p"
   done
   ```

   Any `MISS` is either:
   - A forward-looking instruction (path the user is told to create) — annotate accordingly.
   - A bug — fix.

7. **Commit only after the diff has been read in full.**

## Concrete examples

### Example 1: over-reach during the 2026-05-13 cleanup pass

**Original sed (RAN WITHOUT AUDIT):**

```bash
grep -rln "research/manual/multi\|research/external-syntheses" --include="*.md" --include="*.sh" 2>/dev/null \
  | grep -v ".git/" \
  | xargs sed -i 's|research/manual/multi/|reference-only/el-kaim-book/|g; \
                  s|research/external-syntheses/chatgpt-deep-research-2026-05-11/|reference-only/chatgpt-deep-research-2026-05-11/|g; \
                  s|research/external-syntheses/|reference-only/|g; \
                  s|research/external-syntheses|reference-only|g; \
                  s|research/manual/|reference-only/|g'
```

**What went wrong:** the last substitution `s|research/manual/|reference-only/|g` was too broad. It caught:

- `research/manual/multi/Chapter 1 ...` → `reference-only/Chapter 1 ...` — wrong, should be `reference-only/el-kaim-book/Chapter 1 ...` (caught by the FIRST substitution before this one, OK)
- `research/manual/The Dark Factory How Software Is Le.txt` (in report 07's citation) → `reference-only/The Dark Factory How Software Is Le.txt` — **wrong**, that file was actually deleted and the content needed re-restoration with new name `reference-only/dark-factory-article.txt`
- Historical narrative like "dropped into `research/manual/`" → "dropped into `reference-only/`" — wrong (changes the historical claim)

**What the skill would have done:**

1. Run `grep -nE "research/manual/" --include="*.md" -r .` first.
2. Inspect output. Notice that report 07 has citations to specific filenames that don't exist post-cleanup. Notice that blocked-urls-round-2.md has narrative ("dropped into research/manual/...") that's historical.
3. Apply targeted sed only to the file-path citations whose targets EXIST in the new layout.
4. For citations whose targets were renamed (e.g., Dark Factory txt → dark-factory-article.txt), use targeted `Edit` instead of sed.
5. For narrative mentions of `research/manual/` as a directory concept, decide per-instance whether to update.

### Example 2: safe bulk rename of a renamed module

You're renaming `import old_module` → `import new_module` across all Python files. The pattern is unique (`old_module` is unlikely to appear in comments). Workflow:

```bash
# Step 1: grep first
grep -nE "old_module" --include="*.py" -r src/ | head -20

# Step 2: inspect — confirm all matches are imports/references, no false positives.

# Step 3: apply
find src/ -name "*.py" -exec sed -i 's|old_module|new_module|g' {} +

# Step 4: per-file diff
git diff -- src/

# Step 5: forward-reference verification
python -c "import new_module"  # if it imports cleanly, the rename succeeded

# Step 6: commit
```

Low-risk because `old_module` is unique. The audit step is still required (sed could have caught a substring in a docstring or comment).

## Anti-patterns

- **Piping `grep -rln` into `xargs sed -i` without reading the diff.** This is exactly how the 2026-05-13 over-reach happened. The grep produces a file list; sed applies blindly; nothing alerts you to mismatched-context matches.
- **Using sed for path renames when paths might appear in historical narrative.** Prefer targeted `Edit` tool calls when ambiguity exists.
- **Multi-substitution sed scripts where one substitution can stomp on another.** In the example above, the final `s|research/manual/|reference-only/|g` was a catch-all that bypassed the more targeted earlier substitutions for cases the earlier didn't catch. This is exactly the danger pattern.
- **Skipping forward-reference verification.** A `sed` can leave a path string that no longer resolves to a file; the only way to catch this is to test existence of every cited path after the bulk operation.
- **Treating "the regex compiled" as evidence of correctness.** Sed always runs; the question is whether it ran on the right text.

## Acceptance criteria

1. Before any sed, the grep output has been read in full.
2. Each grep hit has been classified Apply / Preserve / Edit individually.
3. After sed, the per-file `git diff` has been read in full.
4. Forward references have been verified — every new path that the sed introduced resolves to an existing file (or is annotated as a forward-looking instruction).
5. Re-grep for the OLD pattern returns no unexpected matches.

## Files this skill creates / modifies

- Modifies the target files in place per the planned substitution.
- Does NOT commit until the audit (step 3 + step 6) passes.
- Optionally: produces a `bulk-rename-audit-<UTC-date>.md` recording the Apply/Preserve/Edit classification per file (for PR review).
