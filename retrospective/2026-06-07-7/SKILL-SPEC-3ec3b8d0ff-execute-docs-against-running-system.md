# Spec: `execute-docs-against-running-system`

- **ID**: SKILL-SPEC-3ec3b8d0ff
- **Source retrospective**: ../2026-06-07-7.md

## Intent

Validate user-facing documentation by executing every command it contains against the real running system before publishing, treating any divergence between documented and observed behavior as a defect to fix immediately. Authored by hand and reasoned-about docs routinely contain wrong flags, wrong working directories, non-existent targets, name-translation gaps, and commands that need a service that isn't running — defects that are invisible on the page and obvious on the first real run. Grounded in a session where five tutorial commands shipped wrong and were only caught by running each one in the live container.

## Trigger

- **Direct phrases**: "test the docs", "did you actually run these", "does this actually work", "execute the README", "verify the getting-started", "the tutorial is broken".
- **Proactive**: any time you write or edit a user-facing doc (README, GETTING-STARTED, quickstart, runbook) that contains runnable shell/CLI commands, before declaring the doc done; any time a doc's commands target a system that is now bootable in this session.
- **Negative triggers**: pure prose/reference docs with no runnable commands; commands that are destructive in production with no safe environment to run them in (flag those instead of running blind).

## Inputs

- The documentation file(s) under edit or review.
- A way to boot or reach the real running system the docs describe (e.g. `docker compose up`, a live container, a deployed service).
- Any credentials the commands legitimately require (handled without printing — see the credentials rule).
- The target working directory / environment each command assumes.

## Outputs

- A per-command verdict log (PASS / DOCBUG / NEEDS-CREDENTIAL).
- Corrected documentation, reconciled verbatim to observed behavior.
- Re-verification evidence that each corrected command now runs clean.

## Workflow

1. Boot the real system the docs target (the shipped artifact, not a proxy). Wait until it is healthy.
2. Extract every runnable command from the doc, in document order, preserving the working directory and any prerequisite each command assumes.
3. Run each command exactly as written, from the directory the doc tells the reader to be in.
4. Classify each result:
   - **PASS** — runs and produces what the doc claims.
   - **DOCBUG** — wrong flag, wrong dir, non-existent target, name-translation gap, missing prerequisite, or output that contradicts the doc.
   - **NEEDS-CREDENTIAL** — fails only for lack of a credential; rerun with the credential loaded (never printed) before classifying.
5. For each DOCBUG, find the correct command by inspection on the live system, fix the doc, then re-run the corrected command verbatim and confirm PASS.
6. Do not mark the doc done until every command is PASS (or explicitly annotated as requiring an unavailable service, with that stated in the doc).

## Concrete examples

### Example 1: `gc bd` run from the wrong directory

The README told the reader to run `gc bd list` from the rig directory. Run live, it failed: `gc bd` resolves its scope from the city dir and needs the `--rig` flag to target a rig. Fix: the doc was corrected to run from the city directory with `--rig rig1`, and the corrected command was re-run to confirm a clean bead list. On the page this looked authoritative; only execution surfaced it.

### Example 2: a sling target that does not exist

GETTING-STARTED instructed `gc sling rig1/polecat`. Live, the target did not resolve — at that point the worker role was registered as `rig1/claude` (and later `rig1/gastown.polecat`). The non-existent target produced an error invisible to anyone reading the doc. Fix: the doc was corrected to the real, live-verified target name and re-run.

### Example 3: tmux session-name translation gap

The docs told readers to `tmux attach` to a session named as `gc session list` displays it (`gastown.mayor`), but tmux's actual session name is the translated form `gastown__mayor`. Running the documented `tmux` command failed to find the session. Fix: the docs were switched to `gc session peek/attach <id>`, which is name-translation-agnostic, and verified live.

## Anti-patterns

- **Assuming a command works because it reads correctly.** Five commands read perfectly and all failed on first run; correctness on the page is no evidence of correctness on the system.
- **Running a near-equivalent instead of the verbatim command.** A "morally equivalent" command can pass while the literal documented command fails (wrong dir, wrong flag) — run exactly what the reader will paste.
- **Stopping at the first failure.** Run every command; doc bugs cluster, and later commands often depend on the corrected earlier ones.
- **Treating a NEEDS-CREDENTIAL failure as a PASS-by-assumption.** Load the credential and actually run it.

## Acceptance criteria

- [ ] Every runnable command in the doc has a recorded PASS/DOCBUG/NEEDS-CREDENTIAL verdict.
- [ ] Every DOCBUG has a fix that was re-run verbatim and confirmed PASS.
- [ ] Commands were run from the working directory the doc specifies, on the shipped/booted system.
- [ ] The doc is not declared done while any command is unresolved.

## Files this skill creates / modifies

- The documentation file(s) under review (e.g. `README.md`, `GETTING-STARTED.md`) — reconciled to observed behavior.
- An optional verdict log captured in the PR description or retro — per-command PASS/DOCBUG record.
