# `self-retrospective` — Implementation Spec

This is the reference specification. `../SKILL.md` is the executable
operational form (loaded by the harness on skill activation); this file
adds rationale, full templates, and edge-case handling.

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

Without a structured harvest, all of this is lost when the session
window closes. This skill captures it as a filesystem artifact tree the
next agent / human can consume.

---

## 2. Output structure (the spine)

The retrospective produces a filesystem package under
`retrospective/`:

```
retrospective/
├── YYYY-MM-DD-PPP.md                 # main report
└── YYYY-MM-DD-PPP/                   # sibling dir (same base name, no .md)
    ├── <skill-id-1>-spec.md          # one per suggested skill
    ├── <skill-id-2>-spec.md
    ├── ...
    └── AGENTS-suggestions.md         # one section per rule
```

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
- **<Title>** — <one-line rationale, grounded in a session moment>.
- **<Title>** — <one-line rationale>.
(Titles + one-line rationales only. NO specs. User decides per ADR
whether to author it via the `adr` skill.)
```

Hard cap: ~3500 words. The detail lives in the sibling directory.

### 2.3 Per-skill spec contents

Each `<skill-id>-spec.md` is **self-contained**: a fresh-context agent
given only this file as a brief should be able to build the skill
without seeing the session.

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

## 7. Workflow (full)

1. **Verify UTC date** via tool call.
2. **Collect commit hashes by PR** (gh or git log).
3. **Determine the last-PR number** = `max(PRs covered)`. The filename
   is `retrospective/YYYY-MM-DD-${PR}.md`. If no PR exists, fall back
   to the legacy `-NN` day-sequence scheme. If the path already exists,
   append `-a`, `-b`, … (collision rule).
4. **Scan the session** using the §5 checklist (including §5.9 below
   for proposed-ADR candidates).
5. **Write the main report** at `retrospective/YYYY-MM-DD-PPP.md`,
   including the Part 4 proposed-ADRs section.
6. **Write per-skill specs** at
   `retrospective/YYYY-MM-DD-PPP/<id>-spec.md`.
7. **Write AGENTS-suggestions.md** at
   `retrospective/YYYY-MM-DD-PPP/AGENTS-suggestions.md`.
8. **Echo a short inline summary** with paths AND the proposed-ADRs
   title list.
9. **Commit** on the current branch.
10. **If `--pr`**: push and open a PR.

### 5.9 Proposed-ADR scan

In addition to §5.1–5.8, walk the session for **architectural decisions
made** — binding choices that affect multiple files / outlive the
session. Each becomes a proposed-ADR candidate. List in the report's
Part 4 with title + one-line rationale only. **Do not** write specs;
the user decides per ADR whether to author one via the `adr` skill.

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
- **Writing specs for proposed ADRs.** Proposed ADRs are titles +
  one-line rationale only. The user decides per ADR whether to invest;
  the `adr` skill is the right tool when they do.
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
| `/retrospective` | Default — full on-disk package + inline summary. |
| `/retrospective --no-skills` | Skip per-skill specs. |
| `/retrospective --pr` | Push branch and open a PR after writing. |
| `/retrospective --since "YYYY-MM-DD"` | Scope material to after this point. |

---

## 11. Test plan

- Run on a known session transcript.
- Verify the report file is created at the correct UTC-dated, PR-anchored path (or `-NN`-sequenced path under the no-PR fallback).
- Verify the sibling directory has one spec file per suggested skill.
- Verify each per-skill spec contains all required sections (§2.3).
- Verify `AGENTS-suggestions.md` has the section structure of §2.4 for
  every rule.
- Verify the inline chat summary is <20 lines and points at files
  rather than dumping content.
- If a link checker is available, verify all intra-package links resolve.

---

## 12. Living document

Add new scan-checklist items as new kinds of valuable lessons surface
in future sessions. New output sections can be added but must
preserve the §2 spine (main report + sibling dir).
