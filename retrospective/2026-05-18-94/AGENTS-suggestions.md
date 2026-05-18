# AGENTS.md suggestions — 2026-05-18-94

These are proposed additions to the project's agents file (`AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for doing it, grounded in something that happened (or nearly happened).

Decide each on its own merits. Skip ones that don't apply to your operating posture; copy-paste the ones that do.

---

## Suggestion 1: Never hand-edit JSON data files

### Proposed addition

> **JSON data files are edited via tooling, never directly.** Use `jq` (with a `/tmp/new.json` → `mv` atomic pattern) or the project's canonical helper script. Never use `Edit`, `Write`, `sed`, `awk`, or shell heredocs against a JSON file the project treats as data. Direct edits drift from whatever normalizer the project uses, produce non-canonical output, and silently corrupt sort order.
>
> *Grounded in: PR #94's e588b9bb1a → 24ca29ee98 record migration (jq + pointer_to), and the merge conflict on sources.json caused by hand-set keys landing in the wrong order.*

### Why this earns its place in your agents file

In this session, fixing record `e588b9bb1a` required setting a `pointer_to` field. The natural reach is `Edit`. Doing so would have produced a record with `pointer_to` in some arbitrary position (likely at the end of the object, mirroring my mental model) — different from what the project's normalizer produced. The same hand-edited diff would then have conflicted with the auto-regen workflow's output on main, AND failed the byte-equivalence test added in commit `207f544`. By going through jq + the normalizer, the edit was absorbed cleanly into the project's canonical form.

The marginal cost is one tool call: `jq <expr> "$F" > /tmp/new.json && mv /tmp/new.json "$F"`. The cost of not having the rule, when violated, is the kind of cosmetic-but-real merge conflict that PR #94 hit on `sources.json` — five minutes of cleanup plus the loss of confidence about whether other records drifted silently.

---

## Suggestion 2: When N records are broken by a now-fixed bug, sweep — don't hand-fix

### Proposed addition

> **Data fixes flow through the skill, not jq scripts.** When a code bug has left N records in a broken state, add a sweep mode to the skill itself (typically `--tidy-foo` or `--reconcile-bar`) that applies the now-fixed logic to existing records, run it with `--dry-run` first, then live. Do not hand-write a jq script to clean up the records. The sweep mode is idempotent, repeatable, and traceable to the same code path future ingestion will use.
>
> *Grounded in: PR #94's `drain.py --tidy-wants` sweep, which fixed 14 stale `[want]` records using the same `_purge_satisfied_wants` function the live drain attach path now calls.*

### Why this earns its place in your agents file

In this session, after fixing the want-promotion bug, 14 records carried stale `[want]` entries. The temptation was to write a single jq expression: `del(.[] | .files[] | select(.ingestion_status == "want" and .filename == null))` — quick, surgical, done in two minutes. The chosen path took 20 minutes: factor the rule into `_purge_satisfied_wants`, add `--tidy-wants` flag, add `_run_tidy_wants` handler, add tests, dry-run, run live.

The 18 extra minutes bought:
- A sweep mode that's there next time. The same bug class will recur in some form.
- A test that locks the rule's behavior, including the subtle "transcript wants are preserved" edge case.
- A dry-run that surfaced the rule's incompleteness — the first version caught only 11 of 14 records, not 14. A jq one-liner would have papered over the gap; the dry-run made me investigate and tighten the rule.

The marginal cost is real but bounded. The cost of not having the rule: every recurrence of the bug class burns the same 2 minutes, the fixes drift across hand-written jq variants, and the catalog ends up in subtly inconsistent shapes that lints can't catch.

---

## Suggestion 3: Two normalizers for the same file = inevitable drift

### Proposed addition

> **One file, one normalizer.** When a file is mutated by more than one tool (a Python script + a shell command + a workflow + ad-hoc jq edits), consolidate the normalization step into ONE helper script. Every other writer either calls the helper directly or carries a contract docstring naming it as the reference. Lock byte-equivalence with a regression test.
>
> *Grounded in: PR #94's merge conflict on sources.json caused by `drain.py`'s `normalize_and_write` (Python `sort_keys=True`) and the auto-regen workflow's `jq -S 'to_entries | sort_by(.key) | from_entries'` producing subtly different output on partial mutations. Fix landed in commit 207f544: `scripts/normalize-sources-json.sh` is now the single source of truth.*

### Why this earns its place in your agents file

Two normalizers that "obviously produce the same output" almost never produce the same output on every edge case. In this session, the divergence was: jq's `=` operator inserts new keys at the end of an object, even when `-S` re-sorts on output. A `pointer_to` field set via jq landed alphabetically in some code paths and at the end in others. Five places in the project all wrote `sources.json`; three different invocations.

The proposed rule says: when you find yourself with two normalizers, the answer is consolidation, not careful alignment. Careful alignment regresses the next time someone adds a third writer. The byte-equivalence regression test (`tests/unit/test_normalize_sources.py` — 3 tests across 6 fixtures) is what makes consolidation durable.

Marginal cost: a 30-line shell script, an updated SKILL.md rule, a regression test. Cost of not having the rule: silent drift like the one that produced our merge conflict, which would have compounded over time as more inline jq edits accumulated.

---

## Suggestion 4: Write a dotfile progress plan when scope grows mid-session

### Proposed addition

> **When the user adds 3+ new requirements mid-work, or you catch yourself losing track of what's done, write a dotfile progress plan.** Path: `.<feature-tag>-progress.md` at the repo root. Required sections: `## Confirmed scope`, `## Progress` (checkbox table), `## Cleanup before commit` (delete reminder). The dot prefix signals "tooling, not content"; delete the file before staging.
>
> *Grounded in: PR #94's `.plan-discipline-progress.md`, which tracked 8+ sub-tasks across two work layers as the user expanded scope. Deleted before commit; PR diff is clean.*

### Why this earns its place in your agents file

In this session, the user's initial ask was "plan-update discipline." Through subsequent messages, the scope expanded to:
- Auto-emit mechanism (drain.py Stage 4c)
- Plan-audit subskill (`check-plan-consistency.py` + `_plan/` resources)
- README skip-list
- PDF /URL ordering
- MIME title decode
- Want-promotion bug fix via format-final rule
- Sweep mode for 14 stale records
- The CaMeL PDF migration (e588b9bb1a → 24ca29ee98)

That's 8 distinct deliverables, several with sub-deliverables (tests, lint, docs). At the point the user mentioned writing a progress file, I had been working for ~30 messages. Without the file, I would have started forgetting items. The file took 60 seconds to write, 5 seconds per task update, and prevented the failure mode of "user pings me about the README skip-list because I forgot it."

The dotfile naming convention is the small but critical detail: it visually flags as scratch tooling (like `.gitignore`, `.env`) and makes accidental commits unlikely. The `## Cleanup before commit` section is the safety net — re-read the file before staging and the deletion is impossible to forget.

---

## Suggestion 5: Verify "today's date" before writing any date-stamped artifact

### Proposed addition

> **Never trust the model's notion of today's date for date-stamped output.** Always run `date -u +%Y-%m-%d` (or a Python / Node equivalent) as a tool call before writing the date into a retrospective filename, ADR header, commit message, or any other persistent artifact. CLAUDE.md's `currentDate` is human-editable and can be stale; the model's training-data date is not relevant. The cost of verification is one bash call; the cost of date drift is permanently miss-stamped artifacts that fall out of chronological tools.
>
> *Grounded in: the self-retrospective skill's mandatory Step 0 — and the fact that this retrospective explicitly verifies the date via two independent tool calls.*

### Why this earns its place in your agents file

This wasn't a session bug — the verification happened correctly — but the discipline generalizes far beyond retrospectives. Anywhere a date stamp shows up in a long-lived artifact (PLAN.md Version bump, ADR Date header, retrospective filename, commit message context, GitHub issue labels), trusting the in-context date is a silent failure. Tool verification is cheap, deterministic, and audit-traceable.

The session's auto-PLAN-update (drain.py Stage 4c) explicitly uses `datetime.date.today()` for the same reason — the agent doesn't decide the date; the system does.

---

## Suggestion 6: Every catalog mutation updates the narrative file in the same commit

### Proposed addition

> **Every mutation to a structured-data store must update its human-readable narrative companion in the same commit.** In this project: every `reference-only/sources.json` change ships with a `research/PLAN.md` Session bullet (handled automatically by `drain.py` Stage 4c; manual mutations must do it by hand). In other projects: same idea applies to `docs/CHANGELOG.md`, `ARCHITECTURE.md`, `STATUS.md`, or whatever the equivalent is. Without the discipline, the narrative goes stale; with it, the narrative IS the audit trail.
>
> *Grounded in: PR #94 — established as SKILL.md Hard rule #10 in the research-pipeline skill, enforced by `drain.py`'s automatic Stage 4c PLAN.md update + advisory `check-plan-consistency.py` audit.*

### Why this earns its place in your agents file

`check-plan-consistency.py` reported 9 of the last 10 catalog-touching commits on main did not also touch PLAN.md. That's a 90% drift rate on a soft policy. The fix wasn't "remember harder"; it was structural — make the right thing automatic.

The generalization beyond research-pipeline: any project where the data and the narrative live in different files has this risk. The mitigation is the same: automate the narrative update from the data mutator (or its CI), gate on consistency in the lint, surface drift loudly. Marginal cost: a hundred lines of "auto-append a bullet" code per project. Cost of not having it: stale narrative files that future readers (and future versions of yourself) can't trust.

---

## Suggestion 7: Don't `cd` between Bash tool calls

### Proposed addition

> **Working directory does NOT persist between Bash tool calls.** Each invocation starts fresh. If a command needs to run from a subdirectory, either use an absolute path (`python /abs/path/to/script.py`) or chain it inside the same call (`cd subdir && cmd`). Do not assume `cd subdir` in one tool call carries to the next.
>
> *Grounded in: multiple "No such file or directory" failures in this session where I `cd`'d into `.claude/skills/research-pipeline` in one Bash call, then ran `python -m pytest` in the next, which started from `/home/user/software-factory` again and couldn't find `tests/`.*

### Why this earns its place in your agents file

This is a generic harness behavior, not project-specific. In this session it bit me twice — once when re-running pytest after a fix, once when checking lint output. Each time cost a tool call. The fix is to either chain `cd && cmd` in the same Bash invocation, or to use absolute paths from the start.

The marginal cost of the rule is zero; the discipline is "always assume each Bash starts at the same cwd as the first one." A nice side benefit: absolute paths are also clearer in tool-call review than "wait, what dir was I in?"

---

## Suggestion 8: Run dry-run before any data mutation that touches more than one record

### Proposed addition

> **For any data-mutating operation that touches more than one record, run `--dry-run` first.** The dry-run output is the sanity check: do the touched records match your mental model? If the count surprises you, the rule is wrong (or your understanding of it is wrong) — investigate before running for real.
>
> *Grounded in: PR #94's `drain.py --tidy-wants --dry-run` — which surfaced "11 records to touch" when the bug report said 14, leading me to tighten the rule from format-final-only to format-final-OR-same-format-have. Without the dry-run, I would have run the sweep, gotten 11/14, and shipped a half-fix.*

### Why this earns its place in your agents file

The dry-run isn't just for safety — it's a forcing function. It makes you state, in concrete output, what the operation will do, and then makes you reconcile that output with your expectations. In this session, the gap between "11" and "14" was the bug.

Generalizes to: migrations, bulk renames, refactors via `sed -i`, GitHub bulk operations. Any time the answer is "I think this will affect N things", dry-run first.

---

## Suggestion 9: Advisory lint + `--strict` for CI

### Proposed addition

> **Lint checks that flag emerging best practices should be advisory by default and gated by `--strict` for CI.** Local `lint-sources.sh` (or equivalent) prints warnings but exits 0; CI invokes the same script with `--strict` and treats warnings as fatal. This pattern lets the warning teach without blocking unrelated work, while still gating new contributions on the rule once it's stable.
>
> *Grounded in: PR #94's `check-plan-consistency.py` integration — advisory in `lint-sources.sh`, `--strict` for CI gates.*

### Why this earns its place in your agents file

When `check-plan-consistency.py` was first added, 9 historical commits violated the rule. Making it a hard fail would have blocked every local lint run for weeks while the historical drift was back-filled. Making it pure logging would have given no enforcement against new violations.

The advisory + `--strict` pattern threads the needle: the warning is visible (it teaches), but the local agent isn't blocked by historical drift; CI gates new PRs on the strict version. Generalizes to any new style rule, schema check, or migration audit being rolled out incrementally.

---

## Suggestion 10: Drop a regression test the same commit you do a consolidation

### Proposed addition

> **When consolidating two-or-more code paths into one (a refactor, a single-source-of-truth move, a deduplication), include a regression test in the SAME commit.** The test asserts the consolidated path produces output equivalent to what the redundant paths used to produce. Don't trust "they're obviously equivalent now" — lock it.
>
> *Grounded in: PR #94 commit 207f544 ("Single canonical normalizer for sources.json"), which added `test_normalize_sources.py` in the same commit as the consolidation, locking Python ↔ jq byte-equivalence.*

### Why this earns its place in your agents file

A consolidation without a regression test invites the next contributor to add a third writer that produces "almost the same output." The test is the contract; without it, the consolidation is just current code that happens to work today.

The marginal cost is one test file. The cost of not having it: the same consolidation work, redone in 6 months when drift inevitably recurs.

---

## Suggestion 11: `AskUserQuestion` early, broad, batched

### Proposed addition

> **When facing 3+ design questions at once, batch them into ONE `AskUserQuestion` call rather than asking one at a time.** A batched question is one round-trip; sequential questions are N round-trips and tend to lose context between asks ("wait, what did you decide about X again?"). Use the multi-question form. Include enough context per question that the user can answer without re-reading the conversation.
>
> *Grounded in: this session's 4-question scope-clarification batch at the start of the plan-discipline work, which got 4 crisp answers in one round-trip and unblocked the work immediately.*

### Why this earns its place in your agents file

Sequential clarification questions are death by a thousand cuts. Each one pauses the user, requires them to context-load, and only resolves one decision. A batched question shows the structure of the problem (here are the design axes, here are the options on each) and gets the user thinking holistically.

The session's batch covered: plan-update mechanism, subset of small fixes, bug-fix timing, scope of subskills. Four distinct decisions, one click-through. Generalizes to: feature flag scopes, API design choices, refactor depth, when a session pivots from "implement" to "design."

---

## Suggestion 12: Investigate before acting on a "X is broken" report

### Proposed addition

> **When the user reports "X is broken," investigate the actual file/data/code state before acting.** Don't assume the bug is what they describe; the description may be the symptom, not the cause. A 60-second `cat`/`grep`/`jq` is cheaper than fixing the wrong thing and undoing it.
>
> *Grounded in: this session's investigation of the "regenerated sources.md still asks for URLs we have files for" report — which turned out to be 14 stale records caused by a drain.py bug, not by a sources.md renderer bug as I initially considered.*

### Why this earns its place in your agents file

The user reported a symptom in `sources.md`. The instinct was to fix `sources.md` (rendering). The investigation found the root cause was in `sources.json` (the catalog), which was upstream of the renderer. Fixing the renderer would have masked the catalog bug; fixing the catalog made the renderer output correct automatically.

Marginal cost: a few jq queries (~30 seconds). Cost of not investigating: solving the wrong problem, missing 13 other records affected by the same root cause, and leaving a latent bug for the next drain to re-trigger.
