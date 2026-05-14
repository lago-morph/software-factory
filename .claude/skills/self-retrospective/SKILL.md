---
name: self-retrospective
description: Harvest the knowledge accumulated in a session before it's lost to context truncation. Produces a structured retrospective on disk at `retrospective/YYYY-MM-DD-PPP.md` (where `PPP` is the highest PR number covered by the retro) plus a sibling directory with one self-contained spec per suggested skill and a consolidated `AGENTS-suggestions.md` whose sections each carry exact proposed agents-file text plus a persuasion argument. Also lists proposed ADRs (just titles — the user decides whether to author them) in both the report file and the inline chat summary. Use when the user says "do a retrospective", "what did we learn?", "what skills could we extract?", "lessons learned?", or "anything to add to the agents file?", or proactively when a session spanned multiple distinct phases, surfaced unexpected real-world findings, used many subagents, ran long, or the user signals session-wrap ("we're done", "good work", "let's stop here").
---

# Skill: self-retrospective

Harvest session knowledge before context truncation. Default output is a
**filesystem package** at `retrospective/` plus a short inline summary.
The package is structured so each suggested skill has a self-contained
spec a fresh-context agent can implement from that one file, and the
proposed agents-file additions live in one consolidated, persuasive
document. Proposed ADRs — architectural decisions made in the session
that the user *might* want to record formally — are listed in both the
report file and the chat summary, but **without specs**: the user
decides per ADR whether to author it.

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
| `/retrospective` | Default — full on-disk package + inline summary. |
| `/retrospective --no-skills` | Skip per-skill specs; only narrative, commit log, and `AGENTS-suggestions.md`. |
| `/retrospective --pr` | After writing the package, push the branch and open a PR. |
| `/retrospective --since "YYYY-MM-DD"` | Scope material to after this point. |

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

Do **NOT** write specs for these — the report lists only their titles
plus a one-line rationale. After the retrospective lands, the user
decides per ADR whether to author it (using the `adr` skill).
Speculative proposals are fine to list; the user prunes.

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

| Skill | Priority | Approx scope | Spec |
|-------|----------|--------------|------|
| `<id>` | high/med/low | <1–3 words> | [./${UTC_DATE}-${PR}/<id>-spec.md](./${UTC_DATE}-${PR}/<id>-spec.md) |

(One row per skill candidate. Detailed specs live in the sibling
directory, not inline.)

## Part 3 — agents-file suggestions

See [./${UTC_DATE}-${PR}/AGENTS-suggestions.md](./${UTC_DATE}-${PR}/AGENTS-suggestions.md)
for proposed additions to the project's agents file (`AGENTS.md`), one
section per rule, each with exact text to paste and a persuasion
argument.

## Part 4 — proposed ADRs

Architectural decisions made in this session that the user may want to
record as ADRs. **Titles only — no specs.** Use the `adr` skill to
author any of these if you decide they're worth recording.

- **<Proposed ADR title>** — <one-line rationale grounded in a session moment>.
- **<Proposed ADR title>** — <one-line rationale>.
- ...
````

**Hard cap**: keep the main report under ~3500 words. Detail lives in the
sibling directory.

---

## Step 5 — write per-skill specs

For each skill candidate, write `${SIBLING_DIR}/<skill-id>-spec.md`.

**Each spec must be self-contained.** A fresh-context agent given only
this file as a brief should be able to build the skill without seeing
the session it came from.

Required sections per skill spec:

```markdown
# Spec: `<skill-id>`

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

## Step 6 — write `AGENTS-suggestions.md`

Path: `${SIBLING_DIR}/AGENTS-suggestions.md`

**Purpose**: give the user a single document with proposed agents-file
additions. The user reads each section, decides whether to copy-paste
into their actual `AGENTS.md`, and moves on.

Structure:

````markdown
# AGENTS.md suggestions — ${UTC_DATE}-${PR}

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

(A persuasive paragraph or two. Name the specific session event.
Quantify the cost of not having the rule — "took 20 minutes to undo",
"produced two parallel mechanisms", "five fabrications propagated for
two passes before catching". State the marginal cost of adopting the
rule — "one extra grep at session start", "two tool calls". Make the
asymmetry vivid.)

---

## Suggestion 2: ...
````

Aim for 5–15 suggestions. More than 15 is noise — pick the 15 with the
highest signal.

The **"Proposed addition"** block is the verbatim text the user will
paste. Make sure it's self-contained — no references back to the
session, no "see above". The user is making an editorial decision per
section and only the proposed-addition text leaves the document.

The **"Why this earns its place"** block exists to convince. Be
specific. Be honest about costs. Don't pad.

---

## Step 7 — echo inline summary + commit

After writing all artifacts:

1. **Print a short inline summary** in chat (not the full retrospective):
   - Path to the main report.
   - Skill count + names + paths to specs.
   - AGENTS-suggestions count + path.
   - **Proposed ADRs** — bulleted list of titles only (no specs, no
     detail). One line per proposed ADR. Tell the user they can author
     any of them via the `adr` skill.

2. **Commit the artifacts** on the current branch:

   ```bash
   git add retrospective/
   git commit -m "Retrospective ${UTC_DATE}-${PR}: <N> skills, <M> agents-file suggestions"
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
  report + sibling directory with per-skill specs + `AGENTS-suggestions.md`)
  is not optional — it's what makes the output consumable.
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
- **Writing specs for proposed ADRs.** Proposed ADRs are titles +
  one-line rationale only. **Do not** produce a draft body or a spec
  file per proposed ADR — the user decides per ADR whether to invest.
  The `adr` skill is the right tool when they do; this skill just
  surfaces the candidates.
- **A nested `report/` subdirectory under `retrospective/`.** The
  canonical path is `retrospective/YYYY-MM-DD-PPP.md` directly under
  `retrospective/` (or `-NN.md` only via the no-PR fallback). The
  earlier `retrospective/report/` form was redundant — drop it.
- **Bulk-committing without verifying intra-package links.** If the
  project has a link checker (e.g., `.claude/skills/adr/scripts/check_adr_links.py`),
  run it on the new retrospective files before committing. Broken
  intra-package links erode the artifact's value.

---

## See also

- `spec/SPEC.md` — implementation-grade spec (mirrors this SKILL.md with
  more rationale).
- `retrospective/` — the on-disk artifact tree this skill produces.
- `.claude/skills/adr/SKILL.md` — the skill the user can invoke after
  the retrospective to author any of the proposed ADRs.
