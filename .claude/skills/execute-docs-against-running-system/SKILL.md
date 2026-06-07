---
name: execute-docs-against-running-system
description: Validate user-facing documentation by executing every runnable command it contains against the real running system before publishing, treating any divergence between documented and observed behavior as a defect to fix immediately. Hand-authored and reasoned-about docs routinely contain wrong flags, wrong working directories, non-existent targets, name-translation gaps, and commands that need a service that isn't running — defects invisible on the page and obvious on the first real run. Triggers on phrases like "test the docs", "did you actually run these", "does this actually work", "execute the README", "verify the getting-started", "the tutorial is broken"; and proactively any time you write or edit a README / GETTING-STARTED / quickstart / runbook with runnable commands before declaring it done, or whenever a doc's commands target a system that is now bootable in this session. Skip for pure prose/reference docs with no runnable commands; for production-destructive commands with no safe environment, flag them instead of running blind.
---

# Execute docs against the running system

Validate user-facing documentation by **executing every command it contains
against the real running system before publishing**, treating any divergence
between documented and observed behavior as a defect to fix immediately.

Hand-authored and reasoned-about docs routinely contain wrong flags, wrong
working directories, non-existent targets, name-translation gaps, and commands
that depend on a service that isn't running — defects that are **invisible on
the page and obvious on the first real run**. This skill is grounded in a
session where five tutorial commands shipped wrong and were caught only by
running each one in the live container.

---

## When to use this skill

**Activate when:**

- You're writing or editing a user-facing doc (README, GETTING-STARTED,
  quickstart, runbook) that contains runnable shell/CLI commands, before
  declaring the doc done.
- A doc's commands target a system that is now bootable or reachable in this
  session.
- The user says "test the docs", "did you actually run these", "does this
  actually work", "execute the README", "verify the getting-started", or
  "the tutorial is broken".

**Do not activate for:**

- Pure prose / reference docs with no runnable commands.
- Commands that are destructive in production with no safe environment to run
  them in — flag those explicitly instead of running blind.

---

## Inputs

- The documentation file(s) under edit or review.
- A way to boot or reach the real running system the docs describe
  (`docker compose up`, a live container, a deployed service).
- Any credentials the commands legitimately require — handled without printing
  (see the credentials discipline in `AGENTS.md`).
- The target working directory / environment each command assumes.

## Outputs

- A per-command verdict log: **PASS / DOCBUG / NEEDS-CREDENTIAL**.
- Corrected documentation, reconciled verbatim to observed behavior.
- Re-verification evidence that each corrected command now runs clean.

---

## Workflow

1. **Boot the real system the docs target** — the shipped artifact, not a
   proxy (see the `verify-the-shipped-config-not-a-proxy` skill). Wait until it
   is healthy.
2. **Extract every runnable command** from the doc, in document order,
   preserving the working directory and any prerequisite each command assumes.
3. **Run each command exactly as written**, from the directory the doc tells
   the reader to be in.
4. **Classify each result:**
   - **PASS** — runs and produces what the doc claims.
   - **DOCBUG** — wrong flag, wrong dir, non-existent target, name-translation
     gap, missing prerequisite, or output that contradicts the doc.
   - **NEEDS-CREDENTIAL** — fails only for lack of a credential; rerun with the
     credential loaded (never printed) before classifying.
5. **For each DOCBUG**, find the correct command by inspection on the live
   system, fix the doc, then **re-run the corrected command verbatim and
   confirm PASS**.
6. **Do not mark the doc done** until every command is PASS (or explicitly
   annotated as requiring an unavailable service, with that stated in the doc).

---

## Concrete examples

### Example 1: a command run from the wrong directory

A README told the reader to run `gc bd list` from the rig directory. Run live,
it failed: `gc bd` resolves its scope from the city dir and needs the `--rig`
flag to target a rig. Fix: the doc was corrected to run from the city directory
with `--rig rig1`, and the corrected command was re-run to confirm a clean bead
list. On the page this looked authoritative; only execution surfaced it.

### Example 2: a target that does not exist

GETTING-STARTED instructed `gc sling rig1/polecat`. Live, the target did not
resolve — at that point the worker role was registered as `rig1/claude` (and
later `rig1/gastown.polecat`). The non-existent target produced an error
invisible to anyone reading the doc. Fix: corrected to the real, live-verified
target name and re-run.

### Example 3: a name-translation gap

The docs told readers to `tmux attach` to a session named as `gc session list`
displays it (`gastown.mayor`), but tmux's actual session name is the translated
form `gastown__mayor`. The documented `tmux` command failed to find the
session. Fix: switched the docs to `gc session peek/attach <id>`, which is
name-translation-agnostic, and verified live.

---

## Anti-patterns

- **Assuming a command works because it reads correctly.** Five commands read
  perfectly and all failed on first run; correctness on the page is no evidence
  of correctness on the system.
- **Running a near-equivalent instead of the verbatim command.** A "morally
  equivalent" command can pass while the literal documented command fails
  (wrong dir, wrong flag) — run exactly what the reader will paste.
- **Stopping at the first failure.** Run every command; doc bugs cluster, and
  later commands often depend on the corrected earlier ones.
- **Treating a NEEDS-CREDENTIAL failure as a PASS-by-assumption.** Load the
  credential and actually run it.

---

## Acceptance criteria

- [ ] Every runnable command in the doc has a recorded PASS / DOCBUG /
      NEEDS-CREDENTIAL verdict.
- [ ] Every DOCBUG has a fix that was re-run verbatim and confirmed PASS.
- [ ] Commands were run from the working directory the doc specifies, on the
      shipped/booted system.
- [ ] The doc is not declared done while any command is unresolved.

---

## Files this skill creates / modifies

- The documentation file(s) under review (e.g. `README.md`,
  `GETTING-STARTED.md`) — reconciled to observed behavior.
- An optional verdict log captured in the PR description or retro —
  per-command PASS/DOCBUG record.

---

## See also

- `verify-the-shipped-config-not-a-proxy` — boot the exact shipped artifact and
  config (not a convenience proxy) so the system you execute the docs against is
  the one users actually get.
