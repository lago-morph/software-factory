# `self-retrospective` — Implementation Spec

This is the reference specification. `../SKILL.md` is the executable
operational form (loaded by the harness on skill activation); this file
adds rationale, full templates, and edge-case handling.

The skill has **two modes**:

- **Forward mode** (default) — harvest the active session into a
  filesystem package. Steps §3 through §7.10.
- **Reprocess mode** (§13) — walk one or more existing retrospectives,
  migrate spec / ADR / agents-rule filenames to the
  `TYPE-<hash>-<name>.md` convention, split any legacy
  `AGENTS-suggestions.md` into per-rule `AGENT-<hash>-<name>.md`
  files (relocating the persuasion paragraphs into the source retro's
  Part 3 and deleting the consolidated file), and try to author the
  deferred ADRs from retro report + specs + PR evidence. STOPS with a
  placeholder file when evidence is insufficient — never guesses.

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
├── YYYY-MM-DD-PPP.md                              # main report (Part 3 has the agents-rule persuasion paragraphs)
└── YYYY-MM-DD-PPP/                                # sibling dir (same base name, no .md)
    ├── SKILL-SPEC-<hash>-<skill-id-1>.md          # one per suggested skill, TYPE-HASH-NAME order
    ├── SKILL-SPEC-<hash>-<skill-id-2>.md
    ├── ...
    ├── ADR-<hash>-<kebab-title-1>.md              # one full ADR draft per proposed decision
    ├── ADR-<hash>-<kebab-title-2>.md
    ├── ADR-DRAFT-<kebab-title>.md                 # reprocess-mode placeholder (insufficient evidence; no hash in filename — reserved hash is inside)
    ├── AGENT-<hash>-<kebab-rule-name-1>.md        # one per agents-file rule; body only, no ## headers
    ├── AGENT-<hash>-<kebab-rule-name-2>.md
    └── ...
```

All three primary artifact types share the **uniform
`TYPE-<hash>-<name>.md` filename convention**: type token first, durable
hash second, descriptive kebab name last. This clusters same-type
artifacts on alphabetical sort and gives the hash a constant position
for CI/CD tooling.

Legacy on-disk forms that reprocess mode (§13) migrates:

- `<skill-id>-spec.md` (predates durable IDs) → `SKILL-SPEC-<hash>-<skill-id>.md`.
- `<skill-id>-SKILL-SPEC-<hash>.md` (older name-first order) → `SKILL-SPEC-<hash>-<skill-id>.md`.
- `<kebab-title>-ADR-<hash>.md` (older name-first order) → `ADR-<hash>-<kebab-title>.md`.
- `AGENTS-suggestions.md` (consolidated, multi-section) → split into
  per-rule `AGENT-<hash>-<kebab-rule-name>.md` files; the persuasion
  paragraphs from each `### Why this earns its place …` block are
  relocated into the source retro's Part 3; the consolidated file is
  deleted.

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
(Table only; full per-skill specs are in the sibling directory at
`./YYYY-MM-DD-PPP/SKILL-SPEC-<hash>-<skill-id>.md`.)

## Part 3 — agents-file suggestions
Inline expansion: one sub-section per proposed rule, each carrying
(a) a link to the per-rule `AGENT-<hash>-<kebab-rule-name>.md` in the
sibling directory, (b) the verbatim "Proposed addition" blockquote so
the reviewer can read the rule without leaving the report, and
(c) the "Why this earns its place" persuasion paragraph(s). The
per-rule files themselves are body-only (no `##` headers); Part 3 is
where the persuasion text lives.

## Part 4 — proposed ADRs

| ID | Title | Draft |
|----|-------|-------|
| ADR-<hash> | <Title> | [./YYYY-MM-DD-PPP/ADR-<hash>-<kebab-title>.md](...) |

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

Filename: `SKILL-SPEC-<hash>-<skill-id>.md` (TYPE-HASH-NAME order; see
§2.5 for the hash mechanic). Legacy retros use either
`<skill-id>-spec.md` (no hash) or `<skill-id>-SKILL-SPEC-<hash>.md`
(name-first order); reprocess mode (§13) migrates both to the canonical
order.

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

### 2.4 Per-rule agents file contents (`AGENT-<hash>-<kebab-name>.md`)

One file per proposed rule, in the sibling directory. Aim for 5–15
rules per retro — more is noise.

**Purpose**: a CI/CD pipeline picks per-rule files up mix-and-match and
concatenates them into the canonical `AGENTS.md`. Concatenation is the
expected assembly step, so each file must be body-only — no `##`
section headers that would create awkward subsections in the assembled
output.

Filename: `AGENT-<hash>-<kebab-rule-name>.md` (TYPE-HASH-NAME order; see
§2.5 for the hash mechanic).

File contents:

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
  top is fine (it identifies the file). The body below the metadata
  bullets is the verbatim rule blockquote — nothing else.
- No persuasion paragraph inside this file. The "why this earns its
  place" paragraph lives in Part 3 of the source retro's main report,
  not here.
- No back-references to the session ("see above", "as discussed in
  Phase 4"). The rule must stand alone once concatenated into
  `AGENTS.md`.

#### Why the persuasion lives in the retro, not in the file

The per-rule files are designed for downstream CI/CD assembly into
`AGENTS.md`. Persuasion text inside those files would either (a) leak
editorial commentary into the final `AGENTS.md` or (b) require the
assembler to parse + strip a "why" section — fragile and convention-
dependent.

By contrast, Part 3 of the retrospective report is where a human
reviewer chooses which rules to adopt. They have the persuasion at
decision time and the per-rule files stay assembly-clean.

#### Legacy `AGENTS-suggestions.md` (consolidated)

Prior to this convention, the skill emitted a single
`${SIBLING_DIR}/AGENTS-suggestions.md` with `## Suggestion N: …`
sections, each containing both the rule and its persuasion. That file
is **no longer written in forward mode**. Reprocess mode (§13) splits
any existing `AGENTS-suggestions.md` into per-rule files, relocates the
persuasion into Part 3 of the source retro, and deletes the
consolidated file.

### 2.5 Durable identifiers (`SKILL-SPEC-<hash>`, `ADR-<hash>`, `AGENT-<hash>`) and uniform filename convention

Every per-skill spec, every proposed-ADR artifact (full draft or
`ADR-DRAFT-…` placeholder), and every per-rule agents-file addition
carries a durable, hash-based identifier.

#### ID format

- `SKILL-SPEC-<hash>` — per-skill specs.
- `ADR-<hash>` — proposed-ADR drafts (forward mode) and placeholders
  (reprocess mode).
- `AGENT-<hash>` — per-rule agents-file addition (one rule per file).

#### Filename convention (uniform across all three)

```
<TYPE>-<hash>-<kebab-name>.md
```

Concretely:

- `SKILL-SPEC-<hash>-<skill-id>.md`
- `ADR-<hash>-<kebab-title>.md`
- `AGENT-<hash>-<kebab-rule-name>.md`

Rationale: TYPE-first ordering clusters same-type artifacts on
alphabetical sort and gives the durable hash a constant position
(characters 11-20 for AGENT-, 5-14 for ADR-, 12-21 for SKILL-SPEC-) so
CI/CD tooling can parse without regex magic. The
`ADR-DRAFT-<kebab-title>.md` placeholder is the one exception — its
reserved hash is inside the file because the future completing agent
may discover the file under a different title than was forecast.

`<hash>` is the **first 10 hex characters of the SHA256 of a stable
canonical form** of the artifact's content at the moment the identifier
is first assigned.

#### Canonical form

```
<TITLE>\n\n<INTENT_OR_DECISION_OR_RULE_BODY>\n
```

- `<TITLE>` — proposed title verbatim, no number or prefix.
- The second component depends on type:
  - **Skill specs**: the one-paragraph Intent.
  - **Full ADR drafts**: the one-sentence Decision.
  - **`ADR-DRAFT-…` placeholders** (reprocess mode, insufficient
    evidence): the retrospective's Part 4 one-liner — the only stable
    text available before the ADR is completed. **This means the
    pre-computed hash equals the hash the full ADR will carry once
    completed only if the future agent uses the same canonical
    input** — which is why the placeholder's "Completion checklist"
    explicitly tells the completing agent to preserve the hash without
    recomputing it.
  - **Per-rule agents files**: the verbatim rule body (the
    `**<Rule name>.** "…"` blockquote content, plus the `*Grounded in:
    …*` line), trimmed of surrounding whitespace.

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
  full-draft → `docs/adr/NNNN-…` adoption rename, incl. the
  reprocess-mode `<name>-TYPE-<hash>.md` → `TYPE-<hash>-<name>.md`
  filename migration — copy the hash byte-for-byte from the old
  filename into the new one).

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

Per-rule agents file:

```markdown
# AGENTS rule: <Rule name>

- **ID**: AGENT-<hash>
- **Source retrospective**: ../<retro-basename>.md
```

When an ADR draft is adopted to `docs/adr/NNNN-kebab-title.md` via the
`adr` skill, the `**ID**` line is preserved verbatim. The `NNNN` is a
separate human-friendly sequence; the hash is the durable identifier.
The same rule applies when a CI/CD pipeline assembles per-rule agents
files into the canonical `AGENTS.md` — the `AGENT-<hash>` ID stays
attached to its rule (typically as an HTML comment in the assembled
output) so each line in the assembled file traces back to its source
retrospective.

### 2.6 ADR draft contents

Each `ADR-<hash>-<kebab-title>.md` (forward mode; or the body of an
`ADR-DRAFT-<kebab-title>.md` placeholder once completed via reprocess)
uses the canonical ADR section structure so adoption is a file-move +
number assignment, not a rewrite:

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
   including Part 3's expanded agents-rule suggestions (each rule
   linked to its per-rule file in the sibling dir, with the
   "Proposed addition" blockquote inline and the "Why this earns its
   place" persuasion paragraph(s) below) and Part 4's proposed-ADRs
   table linking to draft files.
7. **Write per-skill specs** at
   `retrospective/YYYY-MM-DD-PPP/SKILL-SPEC-<hash>-<skill-id>.md`, with
   `**ID**: SKILL-SPEC-<hash>` under the H1.
8. **Write per-ADR full drafts** at
   `retrospective/YYYY-MM-DD-PPP/ADR-<hash>-<kebab-title>.md`, with
   `**ID**: ADR-<hash>` under the H1 and the canonical ADR section
   structure (Context, Decision, Alternatives considered, Consequences,
   References).
9. **Write per-rule agents files** at
   `retrospective/YYYY-MM-DD-PPP/AGENT-<hash>-<kebab-rule-name>.md`,
   one per proposed rule, each containing only the H1, the `**ID**` +
   `**Source retrospective**` metadata bullets, and the verbatim rule
   blockquote (no `##` headers, no persuasion). The persuasion lives
   in Part 3 of the main report (step 6).
10. **Echo a short inline summary** with paths AND the proposed-ADR
    `ADR-<hash>` IDs AND the per-rule `AGENT-<hash>` IDs.
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
- **Writing a consolidated `AGENTS-suggestions.md` in forward mode.**
  That format is legacy. Forward mode emits one
  `AGENT-<hash>-<name>.md` per rule plus persuasion paragraphs in
  Part 3 of the main report. Reprocess mode (§13) is the only path
  that touches a legacy consolidated file — and only to split it apart
  and delete it.
- **`##` section headers inside a per-rule `AGENT-<hash>-<name>.md`
  file.** The per-rule files are designed for concatenation into
  `AGENTS.md` by a CI/CD assembler. Section headers inside the file
  would create awkward subsections in the assembled output.
- **Putting persuasion inside the per-rule agents file.** The per-rule
  file is the verbatim rule text only. The persuasion lives in Part 3
  of the main report.
- **The old `<name>-TYPE-<hash>.md` filename order.** Use
  `TYPE-<hash>-<name>.md` uniformly across skill specs, ADR drafts,
  and per-rule agents files. Reprocess mode migrates legacy filenames;
  do not re-introduce the old order in new retros.
- **Regenerating an immutable hash ID.** Once `SKILL-SPEC-<hash>`,
  `ADR-<hash>`, or `AGENT-<hash>` is in a file, it is frozen — even
  through filename-convention migrations. Restore from `git log -p` if
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
| `/retrospective --no-agents` | Skip per-rule agents files and Part 3 suggestions. |
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
  each named `SKILL-SPEC-<hash>-<skill-id>.md` with the ID in metadata.
- Verify each per-skill spec contains all required sections (§2.3).
- Verify each proposed-ADR draft (`ADR-<hash>-<kebab-title>.md`)
  contains Context, Decision, Alternatives considered, Consequences,
  References, and the frozen `**ID**: ADR-<hash>` line.
- Verify each per-rule agents file (`AGENT-<hash>-<kebab-rule-name>.md`)
  has the H1 + `**ID**` + `**Source retrospective**` metadata + the
  verbatim rule blockquote, **and no `##` headers in the body**.
- Verify Part 3 of the main report carries the persuasion paragraph
  for every per-rule agents file (one `### Suggestion N: …` block per
  rule), and that no `AGENTS-suggestions.md` exists in the sibling
  directory.
- Verify computed hashes are stable: re-running the canonical-form
  command with the same TITLE + INTENT_OR_DECISION_OR_RULE_BODY inputs
  produces the same 10-character string.
- Verify the inline chat summary is <20 lines and points at files
  rather than dumping content.
- If a link checker is available, verify all intra-package links resolve.
- Session-scope: run two retros in one session; verify the second one's
  `**Scope**` header reads `since <commit>` and its commit-hashes table
  excludes the first retro's range.

Reprocess mode (§13):

- Run on a legacy retro whose per-skill specs lack IDs. Verify each
  spec is renamed to `SKILL-SPEC-<hash>-<skill-id>.md` and the
  retrospective's Part 2 table is rewritten to point at the new
  filenames.
- Run on a retro whose specs are in the older `<skill-id>-SKILL-SPEC-<hash>.md`
  name-first form. Verify each is renamed to
  `SKILL-SPEC-<hash>-<skill-id>.md` with the hash preserved
  byte-for-byte and the metadata unchanged.
- Run on a retro whose ADR drafts are in the older
  `<kebab-title>-ADR-<hash>.md` form. Verify each is renamed to
  `ADR-<hash>-<kebab-title>.md` with the hash preserved and Part 4
  links rewritten.
- Run on a retro whose sibling dir contains `AGENTS-suggestions.md`.
  Verify (a) one `AGENT-<hash>-<kebab-rule-name>.md` is produced per
  `## Suggestion N: …` section with hash computed from the rule
  blockquote, (b) the persuasion paragraphs are relocated into Part 3
  of the main report verbatim, (c) the consolidated
  `AGENTS-suggestions.md` is deleted (staged via `git rm`), and
  (d) Part 3's old `See [./…/AGENTS-suggestions.md]` pointer is
  replaced with the expanded per-rule + persuasion structure.
- Run on a retro with sufficient evidence for one ADR and insufficient
  for another. Verify the first produces `ADR-<hash>-<kebab-title>.md`
  with full content, and the second produces
  `ADR-DRAFT-<kebab-title>.md` with the pre-computed ID, "What I know"
  and "What I need to know" sections, and the completion checklist.
- Idempotency: a second reprocess run on the same retro is a no-op —
  no file renames, no new commits, no ID drift, no re-relocation of
  persuasion paragraphs (Part 3 already in the new layout, no
  `AGENTS-suggestions.md` to split).
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
  that predates any of the current conventions (filename ordering,
  durable IDs, per-rule agents files).
- `/retrospective reprocess --since YYYY-MM-DD` — retros on or after
  this date.

### 13.2 Four responsibilities

1. **Migrate skill specs to the `SKILL-SPEC-<hash>-<skill-id>.md`
   convention.** Two cases:
   - Legacy `<skill-id>-spec.md` (no hash, no metadata): read the file,
     extract title + Intent, compute the hash, rename to
     `SKILL-SPEC-<hash>-<skill-id>.md`, insert `**ID**` +
     `**Source retrospective**` bullets under the H1.
   - Older `<skill-id>-SKILL-SPEC-<hash>.md` (hash present in
     name-first order): rename to `SKILL-SPEC-<hash>-<skill-id>.md`
     preserving the hash byte-for-byte; file contents unchanged.
   - Already `SKILL-SPEC-<hash>-<skill-id>.md`: skip (idempotent).

   In all non-skip cases, rewrite Part 2 links in the main report to
   point at the new filenames.

2. **Migrate ADR drafts to the `ADR-<hash>-<kebab-title>.md`
   convention.** For each `<kebab-title>-ADR-<hash>.md`, rename to
   `ADR-<hash>-<kebab-title>.md` (hash preserved). `ADR-DRAFT-…`
   placeholders keep their existing filename. Rewrite Part 4 table
   links to the renamed files.

3. **Split any legacy `AGENTS-suggestions.md` into per-rule files.**
   For each `${SIBLING_DIR}/AGENTS-suggestions.md`:
   - Parse each `## Suggestion N: <Rule name>` section into three
     components: rule name, "Proposed addition" blockquote, "Why this
     earns its place" persuasion paragraph(s).
   - Compute the hash from `TITLE\n\nRULE_BODY\n` (rule name as TITLE;
     blockquote body as RULE_BODY, trimmed). Freeze it.
   - Write `${SIBLING_DIR}/AGENT-<hash>-<kebab-rule-name>.md` with
     only the H1 + `**ID**` + `**Source retrospective**` metadata
     bullets + verbatim rule blockquote — no `##` headers, no
     persuasion.
   - Replace Part 3 of the main report (which previously was a
     pointer to `AGENTS-suggestions.md`) with the expanded forward-mode
     format: one `### Suggestion N: <Rule name> — \`AGENT-<hash>\``
     block per rule, each containing the per-rule file link, the
     verbatim rule blockquote, and the persuasion paragraph(s) (moved
     unchanged from the original file).
   - Delete `${SIBLING_DIR}/AGENTS-suggestions.md` via `git rm`.
   - If no `AGENTS-suggestions.md` exists but per-rule files already
     do, skip (idempotent).

4. **Back-fill the ADRs.** For each Part 4 proposed-ADR title, try to
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

- Skill specs already named `SKILL-SPEC-<hash>-<skill-id>.md` are skipped.
- ADR drafts already named `ADR-<hash>-<kebab-title>.md` are skipped.
- Sibling dirs with no `AGENTS-suggestions.md` and one or more
  `AGENT-<hash>-<name>.md` files are treated as already-split.
- Proposed-ADRs whose Part 4 link target already exists (as full draft
  or placeholder) are skipped.
- No new commit is created if the working tree is unchanged.

### 13.8 Commit and chat summary

```bash
git add retrospective/
# AGENTS-suggestions.md deletions are picked up by `git add -A
# retrospective/` or by an explicit `git rm`.
git commit -m "Reprocess retros: <R> spec renames, <S> ADR renames, <A> AGENTS splits, <N> ADRs back-filled, <M> placeholders"
```

The chat summary **must list every `ADR-DRAFT-…` placeholder** with its
path and the one-sentence "what I need to know" headline, alongside
counts for each migration class (spec renames, ADR renames, AGENTS
splits). The placeholder list is the user's primary action item from a
reprocess run; bury it and the user can't act on it.

### 13.9 Anti-patterns specific to reprocess

- **Guessing missing fields.** If the Decision sentence isn't
  recoverable, write the placeholder. Don't author a paraphrase.
- **Regenerating the hash later.** The hash is fixed at reprocess time
  — and the spec / ADR hashes carried over from the legacy filenames
  are preserved byte-for-byte through the rename.
- **Editing the retro's narrative.** Reprocess touches three specific
  things in the main report: Part 2 link targets (spec rename), Part 3
  (replaced with the expanded agents-rules + persuasion layout when an
  `AGENTS-suggestions.md` is split), and Part 4 link targets (ADR
  rename + back-fill). Part 1 narrative, Part 2 row contents (skill
  names, IDs, priorities, scopes), Part 4 row contents (titles,
  one-liners), and the metrics table are immutable.
- **Deleting `AGENTS-suggestions.md` without relocating its persuasion
  paragraphs into Part 3.** The persuasion is the user-facing value of
  those paragraphs; losing them on the way to per-rule files defeats
  half the point of the format. Always rewrite Part 3 *before* the
  `git rm`.
- **Re-introducing the old `<name>-TYPE-<hash>.md` order during
  reprocess.** Both spec and ADR renames produce
  `TYPE-<hash>-<name>.md`. Do not invert them.
- **Skipping the existing-ADR cross-check.** A candidate may already
  exist in `docs/adr/` under a different title. If so, link to it from
  the retro and skip authoring.
- **Burying the placeholder list in chat.** It is the user's action
  item; surface it prominently.
