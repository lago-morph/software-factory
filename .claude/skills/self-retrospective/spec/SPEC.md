# `self-retrospective` — Implementation Spec

This is the reference specification. `../SKILL.md` is the executable
operational form (loaded by the harness on skill activation); this file
adds rationale, full templates, and edge-case handling.

The skill has **two modes**:

- **Forward mode** (default) — harvest the active session into a
  filesystem package. Steps §3 through §7.10.
- **Reprocess mode** (§13) — walk one or more existing retrospectives,
  back-fill durable hash IDs onto their skill specs, and try to author
  their deferred ADRs from retro report + specs + PR evidence. STOPS
  with a placeholder file when evidence is insufficient — never
  guesses.

---

## 1. Intent

Harvest the knowledge accumulated in a session before context truncation
erases it. A session typically produces:

- Bug fixes and the lessons that motivated them.
- Workarounds for tool / sandbox limitations.
- Subagent prompt patterns that worked or failed.
- Operational mishaps and recoveries.
- Hard-won runtime discoveries.
- Scope decisions and the reasoning behind them.
- Binding architectural choices that affect multiple files (proposed-ADR
  candidates — now captured as **full drafts**, not just titles).

Without a structured harvest, all of this is lost when the session
window closes. This skill captures it as a filesystem artifact tree the
next agent / human can consume.

A session can produce multiple retrospectives; the **session-scope
check** (§3.5) narrows each retro to the commit range since the previous
retro in the same session, so they tile without overlap.

---

## 2. Output structure (the spine)

The retrospective produces a filesystem package under
`retrospective/`:

```
retrospective/
├── YYYY-MM-DD-PPP.md                              # main report
└── YYYY-MM-DD-PPP/                                # sibling dir (same base name, no .md)
    ├── <skill-id-1>-SKILL-SPEC-<hash>.md          # one per suggested skill, hash-IDd
    ├── <skill-id-2>-SKILL-SPEC-<hash>.md
    ├── ...
    ├── <kebab-title-1>-ADR-<hash>.md              # one full ADR draft per proposed decision
    ├── <kebab-title-2>-ADR-<hash>.md
    ├── ADR-DRAFT-<kebab-title>.md                 # reprocess-mode placeholder (insufficient evidence)
    └── AGENTS-suggestions.md                      # one section per rule
```

Legacy retros (predating the durable-ID convention) use
`<skill-id>-spec.md` filenames without the `SKILL-SPEC-<hash>` token.
Reprocess mode (§13) renames them in-place and inserts the ID.

Plus a short inline summary in chat that points at the files. The full
report content is **never** echoed inline — that would defeat the
on-disk artifact.

### 2.1 Filename rules

- `YYYY-MM-DD` is the **UTC date**, verified via a tool call before
  writing (see §3).
- `PPP` is the **highest PR number covered by the retro** (variable
  width; no zero padding). E.g., if the session's covered PRs are
  `#39, #41, #42`, the file is `retrospective/2026-05-14-42.md`.
- **No-PR fallback**: if the session has no PRs (purely local commits,
  no PR opened yet), fall back to the legacy two-digit day-sequence
  scheme — `YYYY-MM-DD-NN.md`, where `NN` starts at `01` and counts the
  retrospectives written that day. Prefer opening a PR over using this
  fallback.
- **Collision rule**: if a file at the computed path already exists,
  append a lowercase letter suffix (`-a`, `-b`, `-c`, …) — e.g.,
  `2026-05-14-42-a.md`. Letter suffixes are append-only; never renumber
  an existing file.
- Names are never reused, even if a retrospective is later deleted.
- Sibling directory has the same name minus `.md` extension.

### 2.2 Main report contents

```markdown
# Retrospective — <one-line description of the session's work>

- **UTC date**: YYYY-MM-DD (verified via `<tool used>`)
- **Last PR**: #PPP (highest PR number covered by this retro; or `Sequence: NN` under the no-PR fallback)
- **Branch at write time**: <branch name>
- **Sibling artifacts**: [./YYYY-MM-DD-PPP/](./YYYY-MM-DD-PPP/)

## Commit hashes by PR

### PR #N — <branch-name> (<state>)
- `<short-hash>` <subject>
- ...

## Part 1 — what happened
(Phase-by-phase narrative + metrics table.)

## Part 2 — skills summary
(Table only; full per-skill specs are in the sibling directory.)

## Part 3 — agents-file suggestions
(Pointer only; the actual suggestions live in
./YYYY-MM-DD-PPP/AGENTS-suggestions.md.)

## Part 4 — proposed ADRs

| ID | Title | Draft |
|----|-------|-------|
| ADR-<hash> | <Title> | [./YYYY-MM-DD-PPP/<kebab-title>-ADR-<hash>.md](...) |

(Full ADR drafts in the sibling dir — Context, Decision, Alternatives
considered, Consequences, References. The user can adopt any draft into
`docs/adr/NNNN-kebab-title.md` via the `adr` skill, which preserves the
hash ID.)

## Scope

- **Scope**: full session | since <commit> (previous retrospective in this session)
```

Hard cap: ~3500 words. The detail lives in the sibling directory.

### 2.3 Per-skill spec contents

Each per-skill spec file is **self-contained**: a fresh-context agent
given only this file as a brief should be able to build the skill
without seeing the session.

Filename: `<skill-id>-SKILL-SPEC-<hash>.md` (see §2.5 for the hash
mechanic). Legacy retros use `<skill-id>-spec.md`; reprocess mode
renames them.

Mandatory metadata bullets directly under the H1:

- `**ID**: SKILL-SPEC-<hash>` — durable identifier, frozen on first assignment.
- `**Source retrospective**: ../<retro-basename>.md`

Mandatory sections:

- `## Intent` — what problem the skill solves, grounded in a real session moment.
- `## Trigger` — direct user phrases + proactive triggers + negative triggers.
- `## Inputs` — what the skill receives at invocation.
- `## Outputs` — what the skill produces (files, commits, side effects).
- `## Workflow` — numbered, executable steps.
- `## Concrete examples` — at least TWO worked examples, end-to-end.
- `## Anti-patterns` — specific things NOT to do.
- `## Acceptance criteria` — 3–5 testable properties.
- `## Files this skill creates / modifies` — paths with one-line descriptions.

Target length: 400–1200 words per spec. The skill's complexity sets the
actual length.

### 2.4 AGENTS-suggestions.md contents

One file, one section per proposed rule. Aim for 5–15 rules — more is
noise.

```markdown
# AGENTS.md suggestions — YYYY-MM-DD-PPP

These are proposed additions to the project's agents file (typically
`AGENTS.md` at the repo root). Each section contains:

1. **Proposed addition** — the exact text to paste.
2. **Why this earns its place in your agents file** — the argument for
   doing it, grounded in something that happened (or nearly happened).

Decide each on its own merits. Skip ones that don't apply to your
operating posture; copy-paste the ones that do.

---

## Suggestion 1: <Rule name>

### Proposed addition

> **<Rule name>.** "<The rule, phrased as a do/don't statement, ready
> to paste verbatim.>"
>
> *Grounded in: <one-phrase session-event reference>.*

### Why this earns its place in your agents file

(Persuasion. Name the event. Quantify the cost of not having the rule.
State the marginal cost of adopting it. Make the asymmetry vivid.)

---

## Suggestion 2: ...
```

The **proposed-addition block must be self-contained** — no
back-references to the session, no "see above". The user is making an
editorial decision per section and may copy only the proposed text.

### 2.5 Durable identifiers (`SKILL-SPEC-<hash>` and `ADR-<hash>`)

Every per-skill spec and every proposed-ADR artifact (full draft or
`ADR-DRAFT-…` placeholder) carries a durable, hash-based identifier.

#### Format

- `SKILL-SPEC-<hash>` — per-skill specs.
- `ADR-<hash>` — proposed-ADR drafts (forward mode) and placeholders
  (reprocess mode).

`<hash>` is the **first 10 hex characters of the SHA256 of a stable
canonical form** of the artifact's content at the moment the identifier
is first assigned.

#### Canonical form

```
<TITLE>\n\n<INTENT_OR_DECISION_PARAGRAPH>\n
```

- `<TITLE>` — proposed title verbatim, no number or prefix.
- `<INTENT_OR_DECISION_PARAGRAPH>`:
  - For skill specs: the one-paragraph Intent.
  - For full ADR drafts: the one-sentence Decision.
  - For `ADR-DRAFT-…` placeholders (reprocess mode, insufficient
    evidence): the retrospective's Part 4 one-liner — the only stable
    text available before the ADR is completed. **This means the
    pre-computed hash equals the hash the full ADR will carry once
    completed only if the future agent uses the same canonical
    input** — which is why the placeholder's "Completion checklist"
    explicitly tells the completing agent to preserve the hash without
    recomputing it.

#### Compute

```bash
printf '%s\n\n%s\n' "$TITLE" "$INTENT_OR_DECISION" \
  | sha256sum | head -c 10
```

#### Immutability rule

Once written into the file, the ID is **frozen**. Never recompute on:

- Title copy-edits.
- Body rewrites.
- Status transitions (Proposed → Accepted → Deprecated).
- Reference list updates.
- File renames (incl. the placeholder → full-draft rename, incl. the
  full-draft → `docs/adr/NNNN-…` adoption rename).

The hash exists for uniqueness and durable cross-reference. It is not a
content checksum and not provenance tracking. If an editor accidentally
regenerates one, restore the original from git history.

#### Location of the ID inside files

Skill spec:

```markdown
# Spec: `<skill-id>`

- **ID**: SKILL-SPEC-<hash>
- **Source retrospective**: ../<retro-basename>.md
```

ADR draft:

```markdown
# ADR: <Title in Sentence Case>

- **ID**: ADR-<hash>
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: YYYY-MM-DD
- **Source retrospective**: ../<retro-basename>.md
- **PRs covered**: #N, #M
```

When adopted to `docs/adr/NNNN-kebab-title.md` via the `adr` skill, the
`**ID**` line is preserved verbatim. The `NNNN` is a separate
human-friendly sequence; the hash is the durable identifier.

### 2.6 ADR draft contents

Each `<kebab-title>-ADR-<hash>.md` (forward mode) or the body of an
`ADR-DRAFT-<kebab-title>.md` (reprocess mode, once completed) uses the
canonical ADR section structure so adoption is a file-move + number
assignment, not a rewrite:

- `## Context` — evidence-driven problem statement.
- `## Decision` — chosen option in one sentence at top; expand below.
- `## Alternatives considered` — what else was on the table, why rejected.
- `## Consequences` — what we accept; what becomes easier / harder.
- `## References` — relative links to retro, specs, PRs; absolute URLs
  only for external sources.

Word count: 400–1000 words per draft. ADRs are decision records, not
design docs.

ADR drafts go to the sibling directory, **not** to `docs/adr/`. The
user adopts them explicitly when ready, preserving the curated-log
discipline of the `adr` skill.

---

## 3. Mandatory: UTC date verification

Never trust the model's internal notion of "today's date". Always
verify via a tool call before writing anything:

```bash
date -u +%Y-%m-%d
```

```bash
python3 -c "import datetime; print(datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d'))"
```

```bash
node -e "console.log(new Date().toISOString().slice(0,10))"
```

Prefer running two if available and confirming they agree. Record the
tool used in the report header. Date drift in filenames silently breaks
the date-grouping of retros against the PR stream and obscures the
chronological audit trail.

---

## 3.5 Session-scope check (forward mode only)

If a retrospective was already committed earlier in the active session,
the new retro must scope to material produced since that commit — not
re-cover the whole session.

Implementation:

```bash
LAST_RETRO_COMMIT=$(git log origin/main..HEAD --format='%H' \
  -- retrospective/ | head -1)

if [ -n "$LAST_RETRO_COMMIT" ]; then
  SCOPE_FROM="$LAST_RETRO_COMMIT"
  SCOPE_LABEL="since ${LAST_RETRO_COMMIT:0:7} (previous retrospective in this session)"
else
  SCOPE_FROM="$(git merge-base origin/main HEAD)"
  SCOPE_LABEL="full session (from branch divergence)"
fi
```

Record the scope label in the report header so two retros from the same
session tile audibly without overlap.

Flags that adjust this:

- `--since "YYYY-MM-DD"` — wall-clock override.
- `--full-session` — disable the auto-narrowing entirely.

Edge cases:

- If the narrowed scope yields fewer than two non-retrospective
  commits, warn the user inline and ask whether to proceed. Do not
  abort.
- If the session has rebased over a prior retrospective commit, the
  `origin/main..HEAD` query may miss it — use `git log HEAD --
  retrospective/ | head -10` as a sanity check.

---

## 4. Commit hashes grouped by PR

The main report enumerates which commits the session produced. Strategy
depends on tool availability.

### 4.1 Strategy A — `gh` CLI available

```bash
gh pr list --state all --search "author:@me" --limit 25 \
  --json number,title,headRefName,state,mergedAt,baseRefName
# For each PR, list its commits:
gh pr view <N> --json commits --jq '.commits[].oid'
```

### 4.2 Strategy B — fallback via git log

Parse `main`'s merge commits to map PR numbers to branches:

```bash
git log origin/main --merges --pretty='%H %s' \
  | grep -E "Merge pull request #[0-9]+ from"
```

For each (PR, branch) pair the agent touched in this session:

```bash
# For open PRs (working branch):
git log origin/main..HEAD --pretty='%h %s'
# For merged PRs:
git log <merge-base>..<pr-tip> --pretty='%h %s'
```

### 4.3 Scope rule

"This session's PRs" = PRs the current agent authored or substantially
modified. Err toward over-inclusion; the reviewer can prune. Skip PRs
predating the `--since` cutoff if one was supplied.

---

## 5. The scan checklist (what to harvest)

Walk the session systematically for these categories. The scan
populates the material; the report organizes it.

### 5.1 Bugs fixed

- **Implementation defects** — code did the wrong thing. → skill candidate (if generalizable).
- **Spec defects** — the design itself was broken. → skill candidate.
- **Transport / environment quirks** — runtime surprised you. → agents-file rule.

### 5.2 Workarounds invented

Any time a tool didn't work and you went around it. Project-specific →
agents-file rule. Generalizable → skill candidate.

### 5.3 Recurring micro-patterns

Anything done >2 times. Worth doing twice → worth templating.

### 5.4 Operational mishaps

Near-misses and mistakes that required recovery. Each becomes a
"don't do X" rule. Do not soften. The mishap IS the lesson.

### 5.5 Subagent prompts

Which brief structures produced good output vs. vague / overly long.
Meta-skill material for future briefs.

### 5.6 Scope decisions

What was skipped, deferred, or cut, and *why*. The why is the lesson.

### 5.7 Runtime discoveries

Auth boundaries, identity quirks, rate limits, naming collisions,
sandbox restrictions. Almost always worth an agents-file rule.

### 5.8 Effective workflows

Workflows that evolved during the session and had measurable benefit.

---

## 6. What NOT to include

- Step-by-step replay of routine work.
- Self-evaluation or praise.
- Speculation about features the system "should" have.
- Code beyond illustrative snippets (the skill files hold code).
- Internal subagent transcripts (just summaries).
- The string `CLAUDE.md` — use `AGENTS.md` / "agents file" instead.
  This skill targets the generic agents-file convention; a project that
  uses a different filename can adapt.

---

## 7. Forward-mode workflow (full)

1. **Verify UTC date** via tool call.
2. **Compute session scope** per §3.5 (`origin/main..HEAD -- retrospective/`).
3. **Collect commit hashes by PR** within the chosen scope (gh or git log).
4. **Determine the last-PR number** = `max(PRs covered)`. The filename
   is `retrospective/YYYY-MM-DD-${PR}.md`. If no PR exists, fall back
   to the legacy `-NN` day-sequence scheme. If the path already exists,
   append `-a`, `-b`, … (collision rule).
5. **Scan the session** using the §5 checklist (including §5.9 below
   for proposed-ADR candidates).
6. **Write the main report** at `retrospective/YYYY-MM-DD-PPP.md`,
   including the Part 4 proposed-ADRs table linking to draft files.
7. **Write per-skill specs** at
   `retrospective/YYYY-MM-DD-PPP/<id>-SKILL-SPEC-<hash>.md`, with
   `**ID**: SKILL-SPEC-<hash>` under the H1.
8. **Write per-ADR full drafts** at
   `retrospective/YYYY-MM-DD-PPP/<kebab-title>-ADR-<hash>.md`, with
   `**ID**: ADR-<hash>` under the H1 and the canonical ADR section
   structure (Context, Decision, Alternatives considered, Consequences,
   References).
9. **Write AGENTS-suggestions.md** at
   `retrospective/YYYY-MM-DD-PPP/AGENTS-suggestions.md`.
10. **Echo a short inline summary** with paths AND the proposed-ADR
    `ADR-<hash>` IDs.
11. **Commit** on the current branch.
12. **If `--pr`**: push and open a PR.

### 5.9 Proposed-ADR scan

In addition to §5.1–5.8, walk the session for **architectural decisions
made** — binding choices that affect multiple files / outlive the
session. Each becomes a proposed-ADR candidate. Write a **full draft**
in the sibling directory per §2.6 — Context, Decision, Alternatives
considered, Consequences, References. The user decides per ADR whether
to adopt the draft into `docs/adr/` via the `adr` skill; the draft's
`ADR-<hash>` ID follows it into its permanent home.

Rationale for full drafts (vs. the prior title-only convention):
context-truncated session restarts cannot recover the decision from a
one-line rationale, but can from a full draft. The cost of writing the
draft now (when context is fresh) is small; the cost of reconstructing
it later (without context) is large or impossible.

---

## 8. Tone

- **Honest about misses.** A retrospective with no "I would do this
  differently" entries is incomplete.
- **Concrete about scope.** List what's in, what's out, why.
- **Suggest, don't prescribe.** The user decides what survives and what
  to build next.

---

## 9. Anti-patterns

- **Trusting the model's notion of today's date.** Always verify via a
  tool call.
- **Implementing while retrospecting.** Wait for explicit "now build it".
- **One giant unstructured document.** The on-disk structure is what
  makes the output consumable.
- **Generic advice.** Ground all rules in specific session events.
- **Forgetting the agents-file suggestions.** They're often the
  highest-ROI output.
- **Capping at "what went well."** The misses ARE the lessons.
- **Per-skill specs that defer to the session.** Specs must stand alone.
- **Title-only proposed ADRs (the old format).** Proposed ADRs now
  require a full draft body. The user still decides whether to adopt
  the draft into `docs/adr/`; this only changes the on-disk capture.
- **Writing ADR drafts to `docs/adr/` directly.** Drafts live in the
  sibling dir until the user explicitly adopts them via the `adr` skill.
- **Regenerating an immutable hash ID.** Once `SKILL-SPEC-<hash>` or
  `ADR-<hash>` is in a file, it is frozen. Restore from `git log -p` if
  one accidentally drifts.
- **Reprocess-mode guessing.** In reprocess mode (§13), if the evidence
  pool is insufficient for a complete ADR, STOP and write the
  placeholder. Never fabricate Decision / Alternatives / Consequences
  content from "what the decision must have been".
- **Ignoring the session-scope check.** When a prior retrospective
  commit exists in `origin/main..HEAD`, scope to that commit forward by
  default; otherwise two retros redundantly cover the same range.
- **A nested `report/` subdirectory under `retrospective/`.** Canonical
  path is `retrospective/YYYY-MM-DD-PPP.md` directly (or `-NN.md` only
  under the no-PR fallback). The earlier `retrospective/report/` form
  was redundant — drop it.
- **Bulk-committing without verifying intra-package links.** If the
  project has a link checker (e.g.,
  `.claude/skills/adr/scripts/check_adr_links.py`), run it on the new
  retrospective files before committing.
- **Calling the agents file `CLAUDE.md`.** Use `AGENTS.md` /
  "agents file".

---

## 10. Skill invocation

| Invocation | Behavior |
|------------|----------|
| `/retrospective` | Default forward mode — full on-disk package + inline summary. |
| `/retrospective --no-skills` | Skip per-skill specs. |
| `/retrospective --no-adrs` | Skip ADR drafts; emit Part 4 title list only (legacy behaviour). |
| `/retrospective --pr` | Push branch and open a PR after writing. |
| `/retrospective --since "YYYY-MM-DD"` | Scope material to after this point. |
| `/retrospective --full-session` | Disable session-scope auto-narrowing. |
| `/retrospective reprocess <retro>` | Reprocess one retro (basename or path). See §13. |
| `/retrospective reprocess --all` | Reprocess every legacy retro. See §13. |
| `/retrospective reprocess --since YYYY-MM-DD` | Reprocess retros on/after this date. |

---

## 11. Test plan

Forward mode:

- Run on a known session transcript.
- Verify the report file is created at the correct UTC-dated,
  PR-anchored path (or `-NN`-sequenced path under the no-PR fallback).
- Verify the sibling directory has one spec file per suggested skill,
  each named `<skill-id>-SKILL-SPEC-<hash>.md` with the ID in metadata.
- Verify each per-skill spec contains all required sections (§2.3).
- Verify each proposed-ADR draft (`<kebab-title>-ADR-<hash>.md`)
  contains Context, Decision, Alternatives considered, Consequences,
  References, and the frozen `**ID**: ADR-<hash>` line.
- Verify computed hashes are stable: re-running the canonical-form
  command with the same TITLE + INTENT_OR_DECISION inputs produces the
  same 10-character string.
- Verify `AGENTS-suggestions.md` has the section structure of §2.4 for
  every rule.
- Verify the inline chat summary is <20 lines and points at files
  rather than dumping content.
- If a link checker is available, verify all intra-package links resolve.
- Session-scope: run two retros in one session; verify the second one's
  `**Scope**` header reads `since <commit>` and its commit-hashes table
  excludes the first retro's range.

Reprocess mode (§13):

- Run on a legacy retro whose per-skill specs lack IDs. Verify each
  spec is renamed to `<skill-id>-SKILL-SPEC-<hash>.md` and the
  retrospective's Part 2 table is rewritten to point at the new
  filenames.
- Run on a retro with sufficient evidence for one ADR and insufficient
  for another. Verify the first produces `<kebab-title>-ADR-<hash>.md`
  with full content, and the second produces
  `ADR-DRAFT-<kebab-title>.md` with the pre-computed ID, "What I know"
  and "What I need to know" sections, and the completion checklist.
- Idempotency: a second reprocess run on the same retro is a no-op
  (no file renames, no new commits, no ID drift).
- Verify the chat summary lists every `ADR-DRAFT-…` placeholder with
  its path — that list is the user's action item.

---

## 12. Living document

Add new scan-checklist items as new kinds of valuable lessons surface
in future sessions. New output sections can be added but must
preserve the §2 spine (main report + sibling dir).

---

## 13. Reprocess mode

Reprocess mode walks one or more **existing** retrospectives and brings
them up to the current durable-ID + full-ADR-draft convention. It is
the mechanism for back-filling legacy retros without re-running their
sessions.

### 13.1 Invocation

- `/retrospective reprocess <retro>` — single retro, basename
  (`2026-05-14-42`) or path (`retrospective/2026-05-14-42.md`).
- `/retrospective reprocess --all` — every retro under `retrospective/`
  whose per-skill specs lack the `SKILL-SPEC-<hash>` ID.
- `/retrospective reprocess --since YYYY-MM-DD` — retros on or after
  this date.

### 13.2 Two responsibilities

1. **Rename the skill specs.** Add `SKILL-SPEC-<hash>` to each legacy
   `<skill-id>-spec.md`; rename to `<skill-id>-SKILL-SPEC-<hash>.md`;
   update Part 2 links in the report.
2. **Back-fill the ADRs.** For each Part 4 proposed-ADR title, try to
   author a complete ADR draft from the evidence pool. If insufficient,
   write the placeholder. **Never guess.**

### 13.3 Evidence pool

For each retrospective being reprocessed, the evidence pool consists
of:

- The retrospective's main report (especially Part 1 narrative + Part 4
  proposed-ADR rationale lines).
- All per-skill spec files in the sibling directory.
- The PRs the retro covered (commit-hashes table in the report). Pull
  via `gh pr view <N> --json title,body,commits` or
  `mcp__github__pull_request_read` / `mcp__github__list_commits`. Also
  pull the diff at high level (`git show <merge-commit> --stat`) where
  available.
- Any existing ADRs under `docs/adr/` (this candidate may already be
  recorded under a different title; check before authoring).

### 13.4 Sufficiency check (the STOP rule)

An ADR can be authored confidently only if **all five** of the
following are recoverable from the evidence pool:

1. **Decision** — one-sentence declarative chosen-option statement, no
   remaining ambiguity.
2. **Context** — specific motivating problem, grounded in at least one
   PR or skill spec (the retro's one-liner alone is insufficient).
3. **At least one Alternative considered** — meaningfully evaluated and
   rejected, with the reason.
4. **Consequences** — at least one concrete trade-off knowingly
   accepted, traceable to the evidence.
5. **Two References** — relative-link-able artifacts (the source retro
   plus at least one other: a spec, a PR, a code path, a research
   report).

If any are missing or speculative, **STOP for that ADR** and write the
placeholder per §13.6. Never paraphrase or extrapolate from "what the
decision must have been". The user retains the original session
context and can finish the draft from there.

### 13.5 Pre-computing the UID hash

Every back-fill attempt (full draft OR placeholder) **computes the hash
first**, before any sufficiency decision:

```bash
TITLE="<verbatim Part 4 title>"
DECISION="<verbatim Part 4 one-liner>"
HASH=$(printf '%s\n\n%s\n' "$TITLE" "$DECISION" | sha256sum | head -c 10)
```

This hash is the durable ID for the rest of the ADR's life. The
placeholder file declares it prominently so the completing agent does
not regenerate it.

### 13.6 Placeholder file format

When the sufficiency check fails, write
`${SIBLING_DIR}/ADR-DRAFT-<kebab-title>.md` with this exact structure:

```markdown
# ADR-DRAFT: <Title in Sentence Case>

> **This is an incomplete ADR draft.** The reprocess pass did not find
> enough evidence in the retrospective + skill specs + PR information
> to author a complete ADR. The user is expected to return to the
> source session (or another session with full context) to finish it.

## Pre-computed UID hash (DO NOT REGENERATE)

- **Reserved ID**: `ADR-<hash>`

This hash was computed from the proposed title and the retrospective's
one-line rationale at reprocess time. **It is the durable identifier
for this ADR.** When this draft is filled out, the completing agent
MUST:

1. Keep this hash on the `**ID**` metadata line. Do not recompute.
2. Rename the file from `ADR-DRAFT-<kebab-title>.md` to
   `<kebab-title>-ADR-<hash>.md` (sibling-dir form) — OR adopt it
   directly into `docs/adr/NNNN-<kebab-title>.md` via the `adr` skill,
   keeping `**ID**: ADR-<hash>` in the metadata.
3. Update the retrospective's Part 4 link to point at the new filename.

## Source retrospective

- [`../<retro-basename>.md`](../<retro-basename>.md)
- **PRs covered by the source retro**: #N, #M, …

## Proposed title (verbatim from retro Part 4)

<title>

## One-line rationale (verbatim from retro Part 4)

<one-liner>

## What I know (from the evidence pool)

(Verifiable facts only. Cite the source inline. Do not paraphrase;
quote where possible. If a bullet is empty, leave it as `- (nothing
recovered)` rather than fabricating.)

- Context fragments recovered: …
- Decision sentence (if recoverable, else blank): …
- Alternatives mentioned anywhere in the evidence: …
- Consequences mentioned: …

## What I need to know (specific questions for the original session)

(Concrete questions the completing agent should be able to answer from
their session context in one or two sentences each.)

- What was the actual decision sentence?
- Which alternatives were genuinely on the table vs. dismissed offhand?
- What concrete trade-off was knowingly accepted?
- Are there code paths, files, or PRs that should be referenced?
- Does this decision supersede or relate to any existing ADR?

## Evidence pool consulted (provenance)

- Retrospective: `../<retro-basename>.md`
- Skill specs in sibling dir: <list>
- PRs read: #N (title), #M (title), …
- Existing ADRs cross-checked: <list>

## Completion checklist (for the future agent)

- [ ] Replace this preamble with the canonical ADR section structure
      (`Context`, `Decision`, `Alternatives considered`, `Consequences`,
      `References`).
- [ ] Keep the `**ID**: ADR-<hash>` metadata line unchanged.
- [ ] Set `**Status**` to `Proposed` or `Accepted`.
- [ ] Rename the file per the "Pre-computed UID hash" section above.
- [ ] Update the source retrospective's Part 4 link.
- [ ] If adopted into `docs/adr/`, run
      `python3 .claude/skills/adr/scripts/check_adr_links.py docs/adr/`.
```

### 13.7 Idempotency

A second reprocess run on the same retrospective must be a no-op:

- Skill specs with an existing `**ID**` line are skipped.
- Proposed-ADRs whose Part 4 link target already exists (as full draft
  or placeholder) are skipped.
- No new commit is created if the working tree is unchanged.

### 13.8 Commit and chat summary

```bash
git add retrospective/
git commit -m "Reprocess retros: <N> ADRs back-filled, <M> placeholders"
```

The chat summary **must list every `ADR-DRAFT-…` placeholder** with its
path and the one-sentence "what I need to know" headline. That list is
the user's primary action item from the reprocess run; bury it and the
user can't act on it.

### 13.9 Anti-patterns specific to reprocess

- **Guessing missing fields.** If the Decision sentence isn't
  recoverable, write the placeholder. Don't author a paraphrase.
- **Regenerating the hash later.** The hash is fixed at reprocess time.
- **Editing the retro's narrative.** Reprocess only touches Part 4
  link targets and spec metadata. Part 1, Part 2 row contents, Part 3
  pointer, and AGENTS-suggestions are immutable.
- **Skipping the existing-ADR cross-check.** A candidate may already
  exist in `docs/adr/` under a different title. If so, link to it from
  the retro and skip authoring.
- **Burying the placeholder list in chat.** It is the user's action
  item; surface it prominently.
