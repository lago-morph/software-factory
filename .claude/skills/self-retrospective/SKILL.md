---
name: self-retrospective
description: Harvest the knowledge accumulated in a session before it's lost to context truncation. Produces a structured retrospective on disk at `retrospective/YYYY-MM-DD-PPP.md` (where `PPP` is the highest PR number covered by the retro) plus a sibling directory using a uniform `TYPE-<hash>-<name>.md` filename convention: one self-contained skill spec per suggested skill at `SKILL-SPEC-<hash>-<name>.md` (each carrying a durable `SKILL-SPEC-<hash>` ID), one full ADR draft per proposed architectural decision at `ADR-<hash>-<name>.md` (each carrying a durable `ADR-<hash>` ID), and one verbatim agents-file rule per proposed addition at `AGENT-<hash>-<name>.md` (each carrying a durable `AGENT-<hash>` ID) — the per-rule files are designed to be picked up mix-and-match by a CI/CD pipeline that assembles them into the canonical `AGENTS.md`, so each file contains ONLY the rule text with no `##` section headers; the persuasion arguments live in the retrospective report's Part 3. Session-aware: if a previous retrospective was already committed during the current session, the new retro is scoped to material after that commit. Has a secondary **reprocess** mode (`/retrospective reprocess <retro>`) that walks one or more old retros, migrates their spec/ADR filenames to the `TYPE-<hash>-<name>.md` convention, splits any legacy `AGENTS-suggestions.md` into per-rule `AGENT-<hash>-<name>.md` files (relocating the persuasion paragraphs into the source retro's Part 3 and deleting the consolidated file), and tries to back-fill deferred ADRs from the retro report + skill specs + PR diffs — stopping (and writing an `ADR-DRAFT-<title>.md` with a pre-computed UID hash) when there is not enough context to author a complete ADR. Use when the user says "do a retrospective", "what did we learn?", "what skills could we extract?", "lessons learned?", "anything to add to the agents file?", "reprocess the retro", "back-fill the ADRs", or proactively when a session spanned multiple distinct phases, surfaced unexpected real-world findings, used many subagents, ran long, or the user signals session-wrap ("we're done", "good work", "let's stop here").
---

# Skill: self-retrospective

Harvest session knowledge before context truncation. Default output is a
**filesystem package** at `retrospective/` plus a short inline summary.
The package is structured so each suggested skill has a self-contained
spec a fresh-context agent can implement from that one file, each
proposed architectural decision has a full ADR draft (same level of
detail as a skill spec), and each proposed agents-file addition is its
own per-rule file that a downstream CI/CD pipeline assembles into the
canonical `AGENTS.md`. All three artifact types share a uniform
filename convention: `TYPE-<hash>-<name>.md`
(`SKILL-SPEC-<hash>-<name>.md`, `ADR-<hash>-<name>.md`,
`AGENT-<hash>-<name>.md`). The per-rule `AGENT-…` files contain only the
verbatim rule text (no `##` section headers); the persuasion arguments
for those rules live in Part 3 of the retrospective report body, where
human reviewers see them at decision time.

The skill has two modes:

- **Forward mode** (default) — generate a retrospective for the current
  session. Steps 0 through 7 below.
- **Reprocess mode** (`/retrospective reprocess <retro-name-or-path>`)
  — walk one or more existing retros, back-fill durable IDs onto their
  skill specs, and try to author the deferred ADRs from the retro
  report + specs + PR information. Documented in the "Reprocess mode"
  section near the end of this file. The hard rule for reprocess mode:
  if a proposed ADR can't be authored confidently from the available
  evidence, **STOP** and write an `ADR-DRAFT-<title>.md` placeholder
  instead of guessing — the user can return to the source session to
  fill it in.

---

## Trigger detection

### Direct triggers — activate immediately

- "Do a retrospective"
- "What did we learn?"
- "What skills could we extract?"
- "Lessons learned?"
- "Anything to add to the agents file?" / "...to AGENTS.md?"
- `/retrospective` (and flag variants — see below)

### Proactive triggers — offer the skill without being asked

Offer when **any** of these apply:

- Session spanned multiple distinct phases or pivots.
- Session surfaced unexpected real-world findings (bugs, transport quirks, spec contradictions).
- Session used ≥5 subagents or required novel orchestration.
- Session discovered workarounds for tool or sandbox limitations.
- Session ran >2 hours of total agent time.
- User says something session-wrapping: "OK we're done", "good work", "let's stop here".

**Do NOT offer for:**

- Routine sessions that exercised a known pattern with no surprises.
- Sessions where the user hasn't done substantive work yet.

### Flag variants

| Invocation | Behavior |
|------------|----------|
| `/retrospective` | Default forward mode — full on-disk package + inline summary. |
| `/retrospective --no-skills` | Skip per-skill specs; only narrative, commit log, per-rule agents files, and ADR drafts. |
| `/retrospective --no-adrs` | Skip ADR drafts; emit only Part 4 title list (legacy behaviour). |
| `/retrospective --no-agents` | Skip per-rule agents files and the Part 3 suggestions section. |
| `/retrospective --pr` | After writing the package, push the branch and open a PR. |
| `/retrospective --since "YYYY-MM-DD"` | Force a specific lower bound, overriding session-scope detection. |
| `/retrospective --full-session` | Disable session-scope auto-narrowing — cover the entire session even if a prior retro was committed during it. |
| `/retrospective reprocess <retro>` | Switch to reprocess mode. `<retro>` is a retro basename (e.g. `2026-05-14-42`) or a glob. See "Reprocess mode" below. |
| `/retrospective reprocess --all` | Reprocess every retro under `retrospective/` that predates the durable-ID convention. |

---

## Durable identifiers + filename convention (mandatory)

Every per-skill spec, every proposed ADR (full or draft), and every
per-rule agents-file addition carries a durable, hash-based identifier.
The identifier exists so an artifact can be referenced across sessions,
file renames, and history rewrites without ambiguity.

### ID format

- `SKILL-SPEC-<hash>` — per-skill spec.
- `ADR-<hash>` — proposed ADR (full draft or `ADR-DRAFT-…` placeholder).
- `AGENT-<hash>` — per-rule agents-file addition (one rule per file).

`<hash>` is the **first 10 hex characters of the SHA256 of a stable
canonical form** of the artifact's content at the moment the identifier
is first assigned.

### Filename convention (uniform across all three types)

All three artifact types use the same filename shape in the sibling
directory:

```
<TYPE>-<hash>-<kebab-name>.md
```

Concretely:

- `SKILL-SPEC-<hash>-<skill-id>.md`
- `ADR-<hash>-<kebab-title>.md`
- `AGENT-<hash>-<kebab-rule-name>.md`

Rationale for the TYPE-first ordering: when the sibling directory is
sorted alphabetically, all artifacts of the same type cluster together,
the durable hash is in a constant position for easy parsing by CI/CD
tooling, and the type token immediately tells a reader what they're
looking at.

The `ADR-DRAFT-<kebab-title>.md` placeholder (reprocess mode, §"Reprocess
mode") is the **one exception**: it has no hash in the filename because
its reserved hash is declared inside the file. The completing agent
renames the placeholder to `ADR-<hash>-<kebab-title>.md` when finishing
the draft.

### Canonical form (for hash computation)

```
<TITLE>\n\n<INTENT_OR_DECISION_OR_RULE_BODY>\n
```

- `<TITLE>` — the proposed title verbatim (no number, no prefix).
- The second component depends on type:
  - **Skill specs** — the one-paragraph Intent.
  - **ADRs** — the one-sentence Decision. For `ADR-DRAFT-…`
    placeholders where the decision is still vague, the one-sentence
    problem statement from the retro's Part 4 rationale.
  - **Agents-file rules** — the verbatim rule body that gets pasted into
    `AGENTS.md` (the `**Rule name.** "..."` blockquote content), trimmed
    of surrounding whitespace.

### Compute

```bash
printf '%s\n\n%s\n' "$TITLE" "$INTENT_OR_DECISION_OR_RULE_BODY" \
  | sha256sum | head -c 10
```

Or, equivalently in Python:

```bash
python3 -c '
import hashlib, sys
title = sys.argv[1]
body  = sys.argv[2]
print(hashlib.sha256(f"{title}\n\n{body}\n".encode()).hexdigest()[:10])
' "$TITLE" "$INTENT_OR_DECISION_OR_RULE_BODY"
```

### Immutability rule (critical)

Once the ID is assigned and written into the file, it is **frozen**.
Never recompute the hash on subsequent edits — not when the title is
copy-edited, not when the body is rewritten, not when status flips
Proposed → Accepted, not when references are added, not when a file is
renamed from the old `<name>-TYPE-<hash>.md` order to the new
`TYPE-<hash>-<name>.md` order during reprocess. The hash exists purely
for uniqueness and durable cross-reference; it is not a content checksum.

If an editor accidentally regenerates an ID, restore the original from
git history. The link from a retrospective to its ADRs, specs, and
agents files depends on the IDs not drifting.

### Location of the ID inside the file

The ID lives on a metadata bullet right under the H1.

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
```

Per-rule agents file:

```markdown
# AGENTS rule: <Rule name>

- **ID**: AGENT-<hash>
- **Source retrospective**: ../<retro-basename>.md
```

When an ADR draft is later promoted into `docs/adr/NNNN-kebab.md` via
the `adr` skill, the **ID line is preserved verbatim**. The `NNNN`
number is a separate human-friendly sequence; the hash is the durable
identifier. The same rule applies when a CI/CD pipeline assembles
per-rule agents files into the canonical `AGENTS.md` — the `AGENT-<hash>`
ID stays attached to the rule (typically as an HTML comment in the
assembled output) so it can be traced back to its source retrospective.

---

## Step 0 — verify the UTC date (mandatory tool call)

**The retrospective's filename embeds the UTC date. Never trust the model's
internal notion of "today's date" — always verify via a tool call before
writing anything.**

Run one of:

```bash
date -u +%Y-%m-%d
```

```bash
python3 -c "import datetime; print(datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d'))"
```

```bash
node -e "console.log(new Date().toISOString().slice(0,10))"
```

Use whichever is available. If the agent's environment supports more than
one, prefer running two and confirming they agree. Save the result as
`UTC_DATE`. **The retrospective text must report which tool produced the
date** so a future reader can audit the provenance.

---

## Step 0.5 — session-scope check (forward mode only)

If a retrospective was already committed earlier in the **current
session**, the new retro should cover only material produced since that
prior retro — not re-cover everything from session start. Without this
narrowing, two retros from the same session redundantly analyze the
same commits.

The heuristic is purely git-driven so it works without any session-id
plumbing:

```bash
# Most-recent commit on the current branch (not yet merged to main) that
# touched retrospective/. If empty, no prior retro exists in this session.
LAST_RETRO_COMMIT=$(git log origin/main..HEAD --format='%H' \
  -- retrospective/ | head -1)
```

If `$LAST_RETRO_COMMIT` is non-empty, set the harvest's lower bound to
that commit:

```bash
SCOPE_FROM="$LAST_RETRO_COMMIT"
SCOPE_LABEL="since ${LAST_RETRO_COMMIT:0:7} (previous retrospective in this session)"
```

Otherwise:

```bash
SCOPE_FROM="$(git merge-base origin/main HEAD)"
SCOPE_LABEL="full session (from branch divergence)"
```

The `--since "YYYY-MM-DD"` flag overrides this with a wall-clock lower
bound. The `--full-session` flag disables the auto-narrowing.

Record the chosen scope in the report header:

```markdown
- **Scope**: <SCOPE_LABEL>
```

This makes the audit trail explicit: a future reader can see exactly
which commit range each retro covered, and they tile without overlap.

When the narrowed scope yields fewer than two non-retrospective commits,
**warn the user inline** and ask whether to proceed — a near-empty
retrospective is usually a sign the user invoked it too soon. Do not
abort; just confirm.

---

## Step 1 — determine the last-PR number

The retrospective's filename is anchored to the **highest PR number among
the PRs the retro covers**. This makes the file directly searchable
against the PR stream ("which retro covered PR #42?" → look for any
retro whose name ends in `-42` or whose body lists `#42`).

The PR set is collected in Step 2 below; this step depends on Step 2's
output. The two steps are mutually ordered for narrative reasons (naming
comes first conceptually), but operationally: **run Step 2 before
finalizing the filename in this step**.

```bash
mkdir -p retrospective
# After Step 2 has produced the list of PRs covered by this retro:
#   PRS="<space-separated list of PR numbers covered>"
PR=$(printf '%s\n' $PRS | sort -n | tail -1)   # highest PR number covered
REPORT="retrospective/${UTC_DATE}-${PR}.md"
SIBLING_DIR="retrospective/${UTC_DATE}-${PR}"
```

### Fallback — no PR exists yet

If the session produced only local commits and no PR has been opened
(neither merged nor in-progress), fall back to the **legacy day-sequence
scheme**:

```bash
existing=$(ls retrospective/"$UTC_DATE"-*.md 2>/dev/null | wc -l)
SEQ=$(printf "%02d" $((existing + 1)))
REPORT="retrospective/${UTC_DATE}-${SEQ}.md"
SIBLING_DIR="retrospective/${UTC_DATE}-${SEQ}"
```

The legacy scheme is a fallback only — open a PR if you can, so the
retro can be anchored to it.

### Collision — same date and same last-PR

If `retrospective/${UTC_DATE}-${PR}.md` already exists, append a
lowercase letter suffix (`-a`, `-b`, `-c`, …) to disambiguate:

```bash
suffix=""
for letter in a b c d e f g h i j; do
  if [ ! -e "retrospective/${UTC_DATE}-${PR}${suffix:+-$suffix}.md" ]; then break; fi
  suffix=$letter
done
REPORT="retrospective/${UTC_DATE}-${PR}${suffix:+-$suffix}.md"
SIBLING_DIR="retrospective/${UTC_DATE}-${PR}${suffix:+-$suffix}"
```

So the first collision on `2026-05-14-42` becomes `2026-05-14-42-a.md`,
the second `…-42-b.md`, etc. Letter suffixes are append-only — never
renumber an existing file.

---

## Step 2 — collect commit hashes grouped by PR

The retrospective must record which commits were produced in the session's
work. Group them by pull request so the audit trail is reviewer-friendly.

### Strategy A — `gh` CLI available

```bash
gh pr list --state all --search "author:@me" --limit 25 \
  --json number,title,headRefName,state,mergedAt,baseRefName
# For each PR, list its commits via:
gh pr view <N> --json commits --jq '.commits[].oid'
```

### Strategy B — `gh` not available (fallback via git log)

Parse `main`'s merge commits to map PR numbers to branches, then list
commits per branch:

```bash
git log origin/main --merges --pretty='%H %s' \
  | grep -E "Merge pull request #[0-9]+ from"
# Output lines like:
#   c3b06ef... Merge pull request #9 from lago-morph/claude/round-2-research-consolidation
```

For each (PR-number, branch) pair the agent touched in this session, list
its commits:

```bash
git log <branch> --not origin/main --pretty='%h %s'
# For merged branches, use the merge commit's parent range:
git log <merge-base>..<pr-tip> --pretty='%h %s'
```

Open PRs (not yet merged) are scoped via the current branch:

```bash
git log origin/main..HEAD --pretty='%h %s'
```

### Scope rule

"This session's PRs" = PRs the current agent authored or substantially
modified. If unsure, err toward over-inclusion; the reviewer can prune.
Skip PRs whose work predates the `--since` cutoff if one was supplied.

---

## Step 3 — scan the session (the harvest)

Walk the session systematically using this checklist. **Do NOT start
writing the retrospective until the scan is complete.** The scan
populates the material; the parts organize it.

### 3.1 Bugs fixed

Classify each:
- **Implementation defects** — code did the wrong thing. Generalizable → skill candidate.
- **Spec defects** — the design itself was broken. Generalizable → skill candidate.
- **Transport / environment quirks** — the runtime surprised you (escaping, identity, permissions, naming collisions). Usually → agents-file rule.

### 3.2 Workarounds invented

Any time a tool didn't do what was needed and you went around it. Each
workaround is reusable. Project-specific → agents-file rule.
Generalizable → skill candidate.

### 3.3 Recurring micro-patterns

Anything done more than twice. If it was worth doing twice, it's worth
templating.

### 3.4 Operational mishaps (especially valuable)

Near-misses and mistakes that required recovery. Each becomes a "don't do
X" rule. Do not soften these. The mishap IS the lesson.

### 3.5 Subagent prompts that worked vs didn't

Meta-skill material for briefing future agents.

### 3.6 Scope decisions

What was explicitly skipped, deferred, or cut, and *why*.

### 3.7 Runtime discoveries

Hard-won facts about the execution environment: auth boundaries, identity
quirks, rate limits, naming collisions, sandbox restrictions. Almost
always worth an agents-file rule.

### 3.8 Effective or innovative workflows

Workflows that emerged or evolved and had measurable benefit.

### 3.9 Architectural decisions made (proposed-ADR candidates)

Any binding choice made during the session that affects multiple files or
outlives the session — a default tool / library / pattern, a structural
convention, a security gate, a workflow contract. Each becomes a
**proposed-ADR candidate**.

**Write a full ADR draft for each candidate** in the sibling directory
(see Step 5.5 below). Same level of detail as a skill spec — Context,
Decision, Alternatives considered, Consequences, References. The draft
carries a frozen `ADR-<hash>` ID. The user can later promote any draft
to `docs/adr/NNNN-kebab-title.md` via the `adr` skill, and the ID
follows the file into its permanent home.

Rationale: the title-only convention used to be enough, but on
context-truncated session restarts a one-line rationale doesn't recover
the decision; the full draft does. The user still decides whether to
*adopt* each ADR into `docs/adr/` — but the rich content is captured at
the moment the decision was fresh, not extrapolated months later.

Skip writing a draft only if the "decision" was tactical (single file,
not architectural). The bar for inclusion in the proposed-ADR list is
the same as before; only the artifact format changed.

---

## Step 4 — write the main report

Path: `retrospective/${UTC_DATE}-${PR}.md` (or `retrospective/${UTC_DATE}-${SEQ}.md` under the no-PR fallback)

Section structure:

````markdown
# Retrospective — <one-line description of the session's work>

- **UTC date**: ${UTC_DATE} (verified via `<tool used>`)
- **Last PR**: #${PR} (highest PR number covered by this retro; or `Sequence: NN` if no PR exists yet — see Step 1 fallback)
- **Branch at write time**: <git rev-parse --abbrev-ref HEAD>
- **Sibling artifacts**: [./${UTC_DATE}-${PR}/](./${UTC_DATE}-${PR}/)

## Commit hashes by PR

### PR #N — <branch-name> (<state: open / merged YYYY-MM-DD>)

- `<short-hash>` <subject>
- `<short-hash>` <subject>
- ...

(repeat per PR)

## Part 1 — what happened

(Phase-by-phase narrative. Each distinct phase gets a named heading
(`### Phase N — <name>`) and 1–3 paragraphs covering: goal, planned
approach, what actually happened (especially deviations), what was
unplanned but mattered.)

### Metrics

| Metric | Value |
|--------|-------|
| Subagents dispatched | N (by category if useful) |
| PRs opened / merged | M / K |
| Real-world bugs discovered + fixed | B |
| Tests added (before / after) | X / Y |
| Spec amendments | S |
| Scenarios driven / skipped | D / Sk |
| Files touched at major refactors | F |

## Part 2 — skills summary

| Skill | ID | Priority | Approx scope | Spec |
|-------|----|----------|--------------|------|
| `<id>` | SKILL-SPEC-<hash> | high/med/low | <1–3 words> | [./${UTC_DATE}-${PR}/SKILL-SPEC-<hash>-<id>.md](./${UTC_DATE}-${PR}/SKILL-SPEC-<hash>-<id>.md) |

(One row per skill candidate. Detailed specs live in the sibling
directory, not inline. The ID is the durable hash-based identifier
described in the "Durable identifiers" section above.)

## Part 3 — agents-file suggestions

Proposed additions to the project's agents file (`AGENTS.md`). **Each
rule has its own per-rule file** in the sibling directory at
`./${UTC_DATE}-${PR}/AGENT-<hash>-<kebab-name>.md` — the file contains
only the verbatim rule body that a downstream CI/CD pipeline can
concatenate into the canonical `AGENTS.md`. The persuasion arguments
(why each rule earns its place) live here in Part 3 so the human
reviewer has them at decision time and the per-rule files stay
section-header-free.

### Suggestion 1: <Rule name> — `AGENT-<hash>`

- **File**: [./${UTC_DATE}-${PR}/AGENT-<hash>-<kebab-name>.md](./${UTC_DATE}-${PR}/AGENT-<hash>-<kebab-name>.md)

**Proposed addition (verbatim from the per-rule file)**:

> **<Rule name>.** "<The rule, phrased as a do/don't statement, ready
> to paste verbatim.>"
>
> *Grounded in: <one-phrase session-event reference>.*

**Why this earns its place in your agents file**:

(A persuasive paragraph or two. Name the specific session event.
Quantify the cost of not having the rule — "took 20 minutes to undo",
"produced two parallel mechanisms", "five fabrications propagated for
two passes before catching". State the marginal cost of adopting the
rule — "one extra grep at session start", "two tool calls". Make the
asymmetry vivid.)

### Suggestion 2: ...

(Repeat per rule. Aim for 5–15 rules. More than 15 is noise — pick the
15 with the highest signal.)

## Part 4 — proposed ADRs

Architectural decisions made in this session that the user may want to
record as ADRs. Each candidate has a **full draft** in the sibling
directory, carrying a frozen `ADR-<hash>` ID. The user can adopt any
draft by invoking the `adr` skill, which moves it to
`docs/adr/NNNN-kebab-title.md` while preserving the ID.

| ID | Title | Draft |
|----|-------|-------|
| ADR-<hash> | <Proposed ADR title> | [./${UTC_DATE}-${PR}/ADR-<hash>-<kebab-title>.md](./${UTC_DATE}-${PR}/ADR-<hash>-<kebab-title>.md) |

One-line rationale per draft (the same one-liner the legacy format
used) appears in the draft's `## Context` opening sentence; no need to
duplicate it here.
````

**Hard cap**: keep the main report under ~3500 words. Detail lives in the
sibling directory.

---

## Step 5 — write per-skill specs

For each skill candidate:

1. Compute `HASH = sha256(TITLE\n\nINTENT_PARAGRAPH\n)[:10]` (see the
   "Durable identifiers" section above).
2. Write the spec to
   `${SIBLING_DIR}/SKILL-SPEC-${HASH}-<skill-id>.md` (TYPE-HASH-NAME
   ordering — see filename convention above).
3. Put `**ID**: SKILL-SPEC-${HASH}` on the metadata bullet under the H1.

**Each spec must be self-contained.** A fresh-context agent given only
this file as a brief should be able to build the skill without seeing
the session it came from.

Required sections per skill spec:

```markdown
# Spec: `<skill-id>`

- **ID**: SKILL-SPEC-<hash>
- **Source retrospective**: ../<retro-basename>.md

## Intent

(One paragraph: what problem the skill solves and why it earns its
place in the skill library. Ground in a real session moment.)

## Trigger

(When should this skill activate? Direct user phrases + proactive
triggers + negative triggers. Be specific.)

## Inputs

(What the skill receives at invocation: arguments, current workspace
state, environment variables, recent context.)

## Outputs

(What the skill produces: files, commits, comments, side effects.)

## Workflow

(Numbered steps. Each step is concrete enough to execute. No "consider
doing X" — say "do X" or "if condition, do X; else do Y".)

## Concrete examples

(At least TWO worked examples, end-to-end. Show input, intermediate
state, output. Use the session's actual material where possible —
real file paths, real commit messages, real error text.)

## Anti-patterns

(Specific things NOT to do, each traceable to a session moment.)

## Acceptance criteria

(How to know the skill is done well: 3–5 testable properties.)

## Files this skill creates / modifies

(Paths the skill writes to, with one-line description of each.)
```

**Quality bar**: an agent reading just this file, with no other context,
should be able to produce a working skill. If the spec defers to the
session, it has failed.

Word count target per spec: 400–1200 words. The skill's complexity sets
the actual length.

---

## Step 5.5 — write per-ADR draft files

For each proposed-ADR candidate identified in §3.9, write
`${SIBLING_DIR}/ADR-<hash>-<kebab-title>.md` (TYPE-HASH-NAME ordering —
see filename convention above).

Compute the hash from the canonical form (see the "Durable identifiers"
section): `TITLE\n\nONE_SENTENCE_DECISION\n`. Freeze it the moment it's
assigned.

Each draft follows the same section structure as a real ADR (so
adoption via the `adr` skill is a straight file-move + number
assignment, not a rewrite):

```markdown
# ADR: <Title in Sentence Case>

- **ID**: ADR-<hash>
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: ${UTC_DATE}
- **Source retrospective**: ../<retro-basename>.md
- **PRs covered**: #<N>, #<M>, ...

## Context

What is the issue that motivated this decision? Be evidence-driven. Cite
the session moment, the bug, the workaround, the spec contradiction —
whatever made this a binding architectural call rather than a tactical
implementation choice. One or two short paragraphs.

## Decision

The chosen option in one sentence at the top. Expand below if needed.

## Alternatives considered

For each meaningfully-considered alternative: what it is, why it was
rejected. At least one alternative — if none, justify briefly.

## Consequences

What becomes easier, what becomes harder, what trade-off we accept.

## References

Relative links to the source retrospective and the relevant skill specs
in the sibling directory. Absolute URLs only for external sources.

- [`../<retro-basename>.md`](../<retro-basename>.md) — the source retrospective.
- [`./SKILL-SPEC-<hash>-<skill-id>.md`](./SKILL-SPEC-<hash>-<skill-id>.md) — related skill spec(s).
- PRs the decision was made in: #N, #M, …
```

**Quality bar**: a fresh-context agent reading only this draft should be
able to either (a) adopt it into `docs/adr/` via the `adr` skill or (b)
challenge / supersede it. If the draft defers to the session ("see the
discussion for details"), it has failed.

Word count target per draft: 400–1000 words. ADRs are decision records,
not design documents — keep each section short.

**Do NOT** write to `docs/adr/` from this skill. The draft lives in the
sibling directory until the user explicitly adopts it. This preserves
the user's editorial control over the numbered ADR log.

---

## Step 6 — write per-rule agents files

**Purpose**: capture each proposed agents-file rule as its own
self-contained file so a downstream CI/CD pipeline can pick rules up
mix-and-match and assemble them into the canonical `AGENTS.md` without
any post-processing of section headers. The persuasion argument for
each rule already lives in Part 3 of the main report (see Step 4).

For each proposed rule, identified during the §3 scan:

1. Pick a **rule name** in sentence case (e.g., "Stale-artifact check
   before draining `research/manual/`").
2. Write the **rule body** — the verbatim text that will be pasted into
   `AGENTS.md`. Use the standard form:

   ```
   **<Rule name>.** "<The rule, phrased as a do/don't statement, ready
   to paste verbatim.>"

   *Grounded in: <one-phrase session-event reference>.*
   ```

3. Compute the hash from the canonical form
   `TITLE\n\nRULE_BODY\n` where `TITLE` is the rule name and
   `RULE_BODY` is the verbatim rule text from step 2, trimmed of
   surrounding whitespace. See the "Durable identifiers" section above.
4. Write the file to `${SIBLING_DIR}/AGENT-<hash>-<kebab-rule-name>.md`.

File contents (no `##` section headers — the file is consumed by
concatenation):

```markdown
# AGENTS rule: <Rule name>

- **ID**: AGENT-<hash>
- **Source retrospective**: ../<retro-basename>.md

> **<Rule name>.** "<The rule, phrased as a do/don't statement, ready
> to paste verbatim.>"
>
> *Grounded in: <one-phrase session-event reference>.*
```

Hard constraints:

- The file body **must not contain any `##` headers**. The H1 at the
  top is fine (it identifies the file); the body is the verbatim rule
  blockquote. Use of `###` is also discouraged — keep the file
  section-free so a concatenation-based assembler does the right thing
  without parsing.
- No persuasion argument inside this file. The "why this earns its
  place" paragraph lives in Part 3 of the main report.
- No back-references to the session ("see above", "as discussed in
  Phase 4"). The rule must stand alone once concatenated into
  `AGENTS.md`.

Aim for 5–15 rules across the session. More than 15 is noise — pick
the 15 with the highest signal.

The per-rule files plus the Part 3 persuasion together replace the
legacy consolidated `AGENTS-suggestions.md`. Do **not** write that
file in forward mode; reprocess mode (below) splits any legacy
consolidated file into per-rule files.

---

## Step 7 — echo inline summary + commit

After writing all artifacts:

1. **Print a short inline summary** in chat (not the full retrospective):
   - Path to the main report.
   - Skill count + names + IDs + paths to specs.
   - **Per-rule agents files** — count + one line each:
     `AGENT-<hash> — <rule name> — <path>`. Mention that the persuasion
     for each lives in Part 3 of the main report.
   - **Proposed ADR drafts** — one line each: `ADR-<hash> — <title> — <path>`.
     Tell the user they can adopt any draft into `docs/adr/` via the
     `adr` skill (which preserves the ID).
   - The chosen **scope label** from Step 0.5 — so the user can see at
     a glance whether the retro covered the full session or only the
     tail since the previous retrospective.

2. **Commit the artifacts** on the current branch:

   ```bash
   git add retrospective/
   git commit -m "Retrospective ${UTC_DATE}-${PR}: <N> skills, <M> agents-file rules, <K> ADR drafts"
   ```

3. If `--pr` was passed: push the branch and open a PR.

**Do not** print the entire main report inline — it's on disk; reference
the path. The inline summary should fit in ~20 lines.

---

## Anti-patterns (never do these)

- **Trusting the model's notion of today's date.** Always verify via a
  tool call (`date -u`, Python `datetime.UTC`, Node `new Date().toISOString()`).
  Date drift in filenames silently breaks the date-grouping of retros
  against the PR stream and obscures the chronological audit trail.
- **Implementing while retrospecting.** If the user says "build it",
  that is a separate task. Wait for an explicit instruction.
- **One giant unstructured document.** The on-disk structure (main
  report + sibling directory with per-skill specs + per-ADR drafts +
  per-rule agents files) is not optional — it's what makes the output
  consumable.
- **Writing a consolidated `AGENTS-suggestions.md` in forward mode.**
  That format is legacy. Forward mode emits one `AGENT-<hash>-<name>.md`
  per rule plus persuasion paragraphs in Part 3 of the main report.
  Reprocess mode is the only path that touches a legacy
  `AGENTS-suggestions.md` — and only to split it apart and delete it.
- **`##` section headers inside a per-rule `AGENT-<hash>-<name>.md`
  file.** The per-rule files are designed for concatenation into the
  canonical `AGENTS.md` by a CI/CD assembler. Section headers inside
  the file would create awkward subsections in the assembled output.
  The H1 at the top identifies the file; everything below it is the
  rule blockquote.
- **Putting persuasion ("why this earns its place") inside the per-rule
  agents file.** The per-rule file is the verbatim rule text only. The
  persuasion lives in Part 3 of the main report so reviewers see it at
  decision time and the assembled `AGENTS.md` doesn't carry editorial
  commentary.
- **The old `<name>-TYPE-<hash>.md` filename order.** Use
  `TYPE-<hash>-<name>.md` uniformly across skill specs, ADR drafts,
  and per-rule agents files. The TYPE-first ordering clusters
  same-type artifacts on alphabetical sort and gives the durable hash a
  constant position for tooling. Reprocess mode migrates legacy
  filenames; do not re-introduce the old order in new retros.
- **Generic advice.** "Write good prompts" is useless without a session
  anchor. Every teaching must be traceable to something that happened.
- **Forgetting the agents-file suggestions.** Agents-file rules are
  often the highest-ROI output of a retrospective; they can be applied
  immediately, without building anything.
- **Capping at "what went well."** The misses ARE the lessons. If the
  session had no mishaps worth recording, look harder.
- **Producing speculative skill candidates.** Only propose skills with
  direct evidence in the scan. If nothing in the session demonstrates
  the need, leave it out.
- **Calling the agents file "CLAUDE.md".** This skill targets the
  generic agents-file convention — `AGENTS.md` at the repo root. If a
  project chose a different filename (`AGENT.md`, `.aider`, etc.) the
  user can adapt; the retrospective should not bake in a tool-specific
  name.
- **Per-skill specs that defer to the session.** A spec that says "see
  the session for details" has failed its job. Specs must stand alone.
- **Regenerating an immutable ID hash.** Once `SKILL-SPEC-<hash>`,
  `ADR-<hash>`, or `AGENT-<hash>` is written into a file, it never
  changes — not on title copy-edits, not on body rewrites, not on
  status flips, not on filename migrations (e.g., the old
  `<name>-TYPE-<hash>.md` → `TYPE-<hash>-<name>.md` rename during
  reprocess). If you accidentally regenerate one, restore it from
  `git log -p`. The hash is the durable identifier; if it drifts,
  every cross-reference rots.
- **Title-only proposed ADRs (the old format).** Proposed ADRs must now
  carry a full draft body — Context, Decision, Alternatives, Consequences,
  References. The user still decides whether to *adopt* each draft into
  `docs/adr/`, but the content gets captured at the moment the decision
  was fresh. Single-line rationale alone does not survive a session
  restart.
- **Writing ADR drafts directly to `docs/adr/`.** Drafts live in the
  retrospective sibling directory until the user explicitly adopts
  them. The numbered ADR log is the user's curated record, not an
  auto-emission.
- **Ignoring the session-scope check.** When `git log origin/main..HEAD
  -- retrospective/` is non-empty, the new retro must scope to that
  commit forward by default. Re-covering the same commit range across
  two retros produces stale, redundant output.
- **A nested `report/` subdirectory under `retrospective/`.** The
  canonical path is `retrospective/YYYY-MM-DD-PPP.md` directly under
  `retrospective/` (or `-NN.md` only via the no-PR fallback). The
  earlier `retrospective/report/` form was redundant — drop it.
- **Bulk-committing without verifying intra-package links.** If the
  project has a link checker (e.g., `.claude/skills/adr/scripts/check_adr_links.py`),
  run it on the new retrospective files before committing. Broken
  intra-package links erode the artifact's value.

---

## Reprocess mode

Invocation:

- `/retrospective reprocess <retro-basename>` — e.g.
  `/retrospective reprocess 2026-05-14-42`. Accepts a path
  (`retrospective/2026-05-14-42.md`) or a basename (`2026-05-14-42`).
- `/retrospective reprocess --all` — walk every retro under
  `retrospective/` that predates any of the current conventions
  (filename ordering, durable IDs, per-rule agents files).
- `/retrospective reprocess --since YYYY-MM-DD` — only retros on or
  after this date.

### What reprocess does

For each targeted retrospective, in order:

1. **Migrate skill specs to the `SKILL-SPEC-<hash>-<name>.md` filename
   convention and add IDs where missing.** Two cases:
   - **Legacy `<skill-id>-spec.md` (no hash yet).** Read the file.
     Extract the title (the H1 text after `Spec:` or equivalent) and
     the Intent paragraph. Compute the hash per the "Durable
     identifiers" canonical form. Rename to
     `${SIBLING_DIR}/SKILL-SPEC-<hash>-<skill-id>.md`. Insert the
     `**ID**: SKILL-SPEC-<hash>` and `**Source retrospective**:
     ../<retro-basename>.md` metadata bullets directly under the H1.
   - **Older format `<skill-id>-SKILL-SPEC-<hash>.md` (name-first).**
     Already has the hash and the metadata. Rename the file to
     `${SIBLING_DIR}/SKILL-SPEC-<hash>-<skill-id>.md` — **preserve the
     hash exactly**; do not recompute. Leave file contents untouched.
   - **Already `SKILL-SPEC-<hash>-<skill-id>.md`.** Skip (idempotent).

   Either way, rewrite the Part 2 "skills summary" table links in the
   retrospective's main report to point at the new filenames.

2. **Migrate ADR drafts to the `ADR-<hash>-<name>.md` filename
   convention.** For each `${SIBLING_DIR}/<kebab-title>-ADR-<hash>.md`,
   rename to `${SIBLING_DIR}/ADR-<hash>-<kebab-title>.md` — preserve the
   hash. `ADR-DRAFT-<kebab-title>.md` placeholders keep their existing
   filename (no hash in their filename by design — see "ADR-DRAFT
   placeholder format" below). Rewrite Part 4 table links in the main
   report to point at the renamed files.

3. **Split any legacy `AGENTS-suggestions.md` into per-rule
   `AGENT-<hash>-<name>.md` files.** This is the new third
   responsibility added with the per-rule agents-file convention.

   For each `${SIBLING_DIR}/AGENTS-suggestions.md`:
   - Parse each `## Suggestion N: <Rule name>` section. Within each,
     identify three components:
     - The **rule name** (from the H2 heading after `Suggestion N:`).
     - The **rule body** (the blockquote under `### Proposed addition`).
     - The **persuasion paragraph(s)** (the text under `### Why this
       earns its place in your agents file`).
   - Compute the hash from the canonical form
     `TITLE\n\nRULE_BODY\n` where `TITLE` is the rule name and
     `RULE_BODY` is the blockquote body verbatim (trimmed of surrounding
     whitespace). Freeze the hash.
   - Write `${SIBLING_DIR}/AGENT-<hash>-<kebab-rule-name>.md` containing
     the H1, the `**ID**` + `**Source retrospective**` metadata bullets,
     and the verbatim rule blockquote — **no `##` headers, no
     persuasion**. See "Per-rule agents file format" below for the exact
     template.
   - **Relocate the persuasion paragraphs into the retrospective's
     report.** In the main report file, replace Part 3's existing
     pointer (`See [./…/AGENTS-suggestions.md](...)`) with an expanded
     Part 3 that lists each rule by name with a link to its per-rule
     file followed by the persuasion paragraph(s) verbatim (same format
     as forward-mode Part 3 — see Step 4 template). The persuasion text
     itself is preserved unchanged; only its location moves.
   - **Delete `${SIBLING_DIR}/AGENTS-suggestions.md`** once the per-rule
     files are written and Part 3 has been rewritten. Use `git rm` so
     the deletion is staged for the same commit.
   - If the sibling directory has no `AGENTS-suggestions.md` but does
     have per-rule `AGENT-<hash>-<name>.md` files already, skip
     (idempotent).

4. **Back-fill ADRs.** Read the retrospective's `## Part 4 — proposed
   ADRs` section. For each title:
   - Compute the candidate hash from `TITLE\n\n<Part-4 one-liner>\n` —
     this is the **pre-computed UID** that follows the artifact through
     its lifecycle regardless of whether it ends as a full draft or an
     `ADR-DRAFT-<title>` placeholder.
   - Gather the evidence pool (see "Evidence pool" below).
   - Run the **sufficiency check** (see below).
   - If sufficient → write the full ADR draft at
     `${SIBLING_DIR}/ADR-<hash>-<kebab-title>.md` using the Step 5.5
     template, populated from the evidence.
   - If insufficient → **STOP for this ADR** and write
     `${SIBLING_DIR}/ADR-DRAFT-<kebab-title>.md` (the placeholder
     format below). Do NOT guess; do NOT extrapolate.

5. **Update the retrospective's Part 4 table** to point at whichever
   file got produced (full draft or placeholder). Do not edit Part 4's
   prose; only update the link target.

6. **Print an inline summary** at the end of the reprocess run:
   - Number of retros processed.
   - Number of skill specs renamed and/or ID'd.
   - Number of ADR drafts renamed.
   - Number of `AGENTS-suggestions.md` files split and deleted, plus
     the per-rule file count produced.
   - For each ADR: one line — full draft path OR placeholder path.
   - The list of `ADR-DRAFT-…` placeholders that the user needs to
     return to original sessions for. **Surface this list prominently**
     — it is the primary actionable output for the user.

### Per-rule agents file format (used by reprocess step 3 and forward Step 6)

```markdown
# AGENTS rule: <Rule name>

- **ID**: AGENT-<hash>
- **Source retrospective**: ../<retro-basename>.md

> **<Rule name>.** "<verbatim rule body from the source — the
> `### Proposed addition` blockquote in legacy
> AGENTS-suggestions.md, or the body written in forward-mode Step 6>"
>
> *Grounded in: <one-phrase session-event reference>.*
```

No `##` section headers. No persuasion paragraph. The file is consumed
by concatenation into the canonical `AGENTS.md`.

### Evidence pool

When trying to author or back-fill an ADR, gather:

- The retrospective's main report (especially Part 1 narrative + Part 4
  proposed-ADR section).
- All per-skill specs in the sibling dir (they often contain the
  technical detail that motivated an architectural call).
- The PRs the retrospective covered. Use the commit-hashes table in the
  report. For each PR:
  - PR title + description (via `gh pr view <N> --json title,body` or
    `mcp__github__pull_request_read`).
  - Commit subjects + bodies (`gh pr view <N> --json commits` or `git log`).
  - Diff at a high level (`git show <merge-commit> --stat`).
- Any ADRs already in `docs/adr/` that this candidate might supersede,
  reference, or duplicate.

### Sufficiency check (the STOP rule)

An ADR can be authored confidently if **all five** of these are
recoverable from the evidence pool:

1. **Decision** — a one-sentence statement of the chosen option, in
   declarative form ("Use X for Y"), with no remaining ambiguity.
2. **Context** — the specific problem that motivated the decision,
   grounded in evidence from at least one PR or skill spec (not just
   the retro's one-liner).
3. **At least one Alternative considered** — something that was
   meaningfully evaluated and rejected, with the reason for rejection.
   "We didn't consider any alternatives" is acceptable only when
   explicitly stated in the source material.
4. **Consequences** — at least one concrete trade-off that was
   knowingly accepted, traceable to the evidence.
5. **Two References** — relative-link-able artifacts (the source retro
   plus at least one other: a spec, a PR, a code path, a research
   report).

If **any** of these can't be filled confidently from the evidence,
**STOP** and write the placeholder. **Do not guess. Do not paraphrase.
Do not extrapolate from "what the decision must have been".** The user
retains the original session context and can finish the draft from
there.

### The `ADR-DRAFT-<kebab-title>.md` placeholder format

Path: `${SIBLING_DIR}/ADR-DRAFT-<kebab-title>.md`.

```markdown
# ADR-DRAFT: <Title in Sentence Case>

> **This is an incomplete ADR draft.** The reprocess pass did not find
> enough evidence in the retrospective + skill specs + PR information to
> author a complete ADR. The user is expected to return to the source
> session (or another session with full context) to finish it.

## Pre-computed UID hash (DO NOT REGENERATE)

- **Reserved ID**: `ADR-<hash>`

This hash was computed from the proposed title and the retrospective's
one-line rationale at reprocess time. **It is the durable identifier
for this ADR.** When this draft is filled out, the completing agent
MUST:

1. Keep this hash on the `**ID**` metadata line. Do not recompute.
2. Rename the file from `ADR-DRAFT-<kebab-title>.md` to
   `ADR-<hash>-<kebab-title>.md` (sibling-dir form, TYPE-HASH-NAME
   ordering) — OR adopt it directly into
   `docs/adr/NNNN-<kebab-title>.md` via the `adr` skill, keeping
   `**ID**: ADR-<hash>` in the metadata.
3. Update the retrospective's Part 4 link to point at the new filename.

## Source retrospective

- [`../<retro-basename>.md`](../<retro-basename>.md)
- **PRs covered by the source retro**: #N, #M, …

## Proposed title (verbatim from retro Part 4)

<title>

## One-line rationale (verbatim from retro Part 4)

<one-liner>

## What I know (from the evidence pool)

(Bullets. Each bullet is a verifiable fact pulled from the retro, a
skill spec, or a PR. Cite the source inline. Do not paraphrase; quote
where possible. If a bullet is empty, leave it as `- (nothing
recovered)` rather than fabricating.)

- Context fragments recovered:
  - …
- Decision sentence (if recoverable; otherwise leave blank):
  - …
- Alternatives mentioned anywhere in the evidence:
  - …
- Consequences mentioned:
  - …

## What I need to know (specific questions for the original session)

(Bullets. Each is a concrete question the completing agent should be
able to answer from their session context. Phrase as questions, not
gaps. Be specific enough that the answer is one or two sentences.)

- What was the actual decision sentence? (The retro's one-liner is too
  vague to convert to a binding statement.)
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

- [ ] Replace this preamble with the standard ADR section structure
      (`Context`, `Decision`, `Alternatives considered`, `Consequences`,
      `References`).
- [ ] Keep the `**ID**: ADR-<hash>` metadata line unchanged.
- [ ] Set `**Status**` to `Proposed` or `Accepted`.
- [ ] Rename the file per the "Pre-computed UID hash" section above.
- [ ] Update the source retrospective's Part 4 link.
- [ ] Run `python3 .claude/skills/adr/scripts/check_adr_links.py docs/adr/`
      if the ADR has been adopted into `docs/adr/`.
```

### Reprocess anti-patterns

- **Guessing missing fields.** If the Decision sentence can't be
  recovered confidently, do not invent one. Write the placeholder.
- **Regenerating the hash later.** The hash computed at reprocess time
  is the ID for the rest of the ADR's life. The completing agent must
  preserve it byte-for-byte. The same applies to hashes preserved
  during the filename migrations in steps 1–3: copy the hash
  byte-for-byte from the old filename / metadata into the new filename.
- **Skipping retros that were already partially processed.** Always
  re-check the state of each artifact type before doing work: skill
  specs already in `SKILL-SPEC-<hash>-<name>.md` form are skipped;
  ADRs already in `ADR-<hash>-<name>.md` form are skipped; sibling
  dirs that already contain per-rule `AGENT-<hash>-<name>.md` files
  with no `AGENTS-suggestions.md` are skipped. Idempotency is required
  — a second reprocess run on a fully-migrated retro must be a no-op.
- **Editing the retrospective's narrative prose.** Reprocess touches
  three specific things in the main report: (a) Part 2 link targets
  (skill spec rename), (b) Part 3 — replaced with the expanded
  agents-rules + persuasion layout when an `AGENTS-suggestions.md` is
  split, and (c) Part 4 link targets (ADR rename + back-fill). Part 1
  narrative, Part 2 row contents (skill names, IDs, priorities,
  scopes), Part 4 row contents (titles, one-liners), and the metrics
  table are left exactly as they were.
- **Deleting `AGENTS-suggestions.md` without first relocating its
  persuasion paragraphs into Part 3.** The persuasion is the
  user-facing value of those paragraphs; losing them on the way to
  per-rule files defeats half the point of the format. Always
  rewrite Part 3 *before* the `git rm`.
- **Re-introducing the old `<name>-TYPE-<hash>.md` order during
  reprocess.** Both file renames in steps 1 and 2 produce
  `TYPE-<hash>-<name>.md`. Do not invert them.
- **Bulk-committing reprocessed retros without a final summary.** The
  user's main action item from a reprocess run is the
  `ADR-DRAFT-…` placeholder list. Surface it prominently.

### Commit and surface

Commit the reprocessed retros on the current branch:

```bash
git add retrospective/
# Use git rm for the deleted AGENTS-suggestions.md files (or rely on
# `git add -A retrospective/` if the staged list is otherwise clean).
git commit -m "Reprocess retros: <R> spec renames, <S> ADR renames, <A> AGENTS splits, <N> ADRs back-filled, <M> placeholders"
```

In the chat reply, **list every `ADR-DRAFT-…` placeholder** with its
path and the one-line "what I need to know" summary. The user uses this
list to decide which original session to revisit.

---

## See also

- `spec/SPEC.md` — implementation-grade spec (mirrors this SKILL.md with
  more rationale).
- `retrospective/` — the on-disk artifact tree this skill produces.
- `.claude/skills/adr/SKILL.md` — the skill the user can invoke after
  the retrospective to author any of the proposed ADRs.
