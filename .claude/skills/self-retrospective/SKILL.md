---
name: self-retrospective
description: Harvest the knowledge accumulated in a session before it's lost to context truncation. Produce a structured retrospective covering what happened, which skills are worth extracting, and which repo conventions belong in AGENTS.md. Use when the user says "do a retrospective", "what did we learn?", "what skills could we extract?", "lessons learned?", or "anything to add to AGENTS.md?", or proactively when a session spanned multiple distinct phases, surfaced unexpected real-world findings, used many subagents, ran long, or the user signals session-wrap ("we're done", "good work", "let's stop here").
---

# Skill: self-retrospective

Harvest the knowledge accumulated in a session before it's lost to context
truncation. Produce a structured retrospective: what happened, which skills
are worth extracting, and which repo conventions belong in `AGENTS.md`.

---

## Trigger detection

### Direct triggers — activate immediately

- "Do a retrospective"
- "What did we learn?"
- "What skills could we extract?"
- "Lessons learned?"
- "Anything to add to AGENTS.md?"
- `/retrospective` (and flag variants — see below)

### Proactive triggers — offer the skill without being asked

Offer when **any** of these apply:

- Session spanned multiple distinct phases or pivots
- Session surfaced unexpected real-world findings (bugs, transport quirks, spec contradictions)
- Session used ≥5 subagents or required novel orchestration
- Session discovered workarounds for tool or sandbox limitations
- Session ran >2 hours of total agent time
- User says something session-wrapping: "OK we're done", "good work", "let's stop here"

**Do NOT offer for:**
- Routine sessions that exercised a known pattern with no surprises
- Sessions where the user hasn't done substantive work yet

### Flag variants

| Invocation | Behavior |
|------------|----------|
| `/retrospective` | Default — Mode A, all three parts |
| `/retrospective --no-skills` | Skip Part 2; produce only narrative + AGENTS.md rules |
| `/retrospective --output-dir ./retro/` | Mode B at a custom path |
| `/retrospective --since "2025-01-15"` | Scope to material after this point |

---

## Step 0 — determine mode

Before producing any output, decide which mode to use.

**Mode A (chat-only)** is the default. Deliver inline markdown, three parts,
final summary table. Cap at ~5000 words.

**Mode B (package)** creates a filesystem directory tree, commits to a feature
branch, and opens a PR. Use when:

- The user mentions "feature branch", "package these", "capture for later",
  "create specs and READMEs", or "I want to implement these later"
- The session has 5+ skill candidates
- The user wants to dispatch each skill build as a separate subsequent task

**If it's not obvious which mode the user wants, ask before producing output.**
A one-sentence question suffices: "Do you want the retrospective inline (Mode A)
or packaged into a feature branch with per-skill READMEs and SPECs (Mode B)?"

---

## Step 1 — scan the session (the harvest)

Walk the session systematically using this checklist. Do NOT start writing the
retrospective until the scan is complete. The scan populates the material; the
parts organize it.

### 3.1 Bugs fixed

Classify each bug found and fixed during the session:

- **Implementation defects** — code did the wrong thing. Generalizable → skill candidate.
- **Spec defects** — the design itself was broken. Generalizable → skill candidate.
- **Transport / environment quirks** — the runtime surprised you (escaping, identity, permissions, naming collisions). Usually → AGENTS.md rule.

### 3.2 Workarounds invented

Any time a tool didn't do what was needed and you went around it. Each
workaround is reusable. Ask: is this workaround project-specific (AGENTS.md
rule) or general enough to apply elsewhere (skill candidate)?

### 3.3 Recurring micro-patterns

Anything done more than twice. If it was worth doing twice, it's worth
templating. Examples: a prompt structure reused across steps, a file-naming
convention applied repeatedly, a verification pattern run after every deploy.

### 3.4 Operational mishaps (especially valuable)

Near-misses and mistakes that required recovery. Each becomes a "don't do X"
rule. Examples:
- Force-pushed feature branch back to main → PR auto-closed
- Subagent ran out of usage mid-task → recovery from local commit
- Marker comments didn't appear → workflow YAML wasn't on main yet

Do not soften these. The mishap IS the lesson.

### 3.5 Subagent prompts that worked vs didn't

What brief structures produced good output? What structures produced vague
or overly long output? This is meta-skill material for briefing future agents.

### 3.6 Scope decisions

What was explicitly skipped, deferred, or cut? The *why* is the lesson.
"We skipped X because Y" is more valuable than a list of what shipped.

### 3.7 Runtime discoveries

Hard-won facts about the execution environment: auth boundaries, identity
quirks, rate limits, naming collisions, sandbox restrictions. Almost always
worth an AGENTS.md rule.

### 3.8 Effective or innovative workflows

Workflows that emerged or evolved during the session and had measurable
benefit. Only include if the workflow was actually useful — not just novel.

---

## Mode A — execution

Produce a markdown document inline. Three parts, in order. Every part is
mandatory; skipping one leaves significant value on the table.

---

### Part 1 — what happened (narrative + metrics)

Write a **phase-by-phase narrative**. Each distinct phase gets a named heading
(`### Phase N — <name>`) and 1–3 paragraphs covering:

1. What was the goal of this phase?
2. What was the planned approach?
3. What actually happened — especially deviations from the plan?
4. What was unplanned but mattered (mishaps, recoveries, surprises)?

After the narrative, append the **metrics table**:

```markdown
| Metric | Value |
|--------|-------|
| Subagents dispatched | N (by category if useful) |
| PRs opened / merged | M / K |
| Real-world bugs discovered + fixed | B |
| Tests added (before / after) | X / Y |
| Spec amendments | S |
| Scenarios driven / skipped | D / Sk |
| Files touched at major refactors | F |
```

Fill in actual values from the scan. If a metric is zero, include the row
anyway — absence is information.

---

### Part 2 — skills to extract

For each skill candidate identified in the scan, use this exact template:

```markdown
### Skill N: `<skill-id>` — <one-line summary>

**Purpose.** <One sentence: what problem this skill solves.>

**Trigger.** <When this skill should activate — be specific.>

**Core content.** <Numbered list of 5-10 substantive teachings derived
from the session. "Write good prompts" is not a teaching. Ground each
item in something that happened.>

**Anti-patterns.** <What NOT to do, based on session misses. Each
anti-pattern should be traceable to a specific moment.>

**Example/template.** <Concrete code, prompt, or text where useful.
Omit if nothing concrete applies.>
```

Target 200–500 words per skill. Enough detail that a future agent could
build from this spec without the original session; not so much that the
retrospective becomes the implementation.

**If `--no-skills` was passed, skip Part 2 entirely.**

---

### Part 3 — AGENTS.md / repo conventions

Write 5–15 one-line rules. Each rule must be:
- Grounded in something that actually went wrong (or nearly did) in this session
- Phrased as a concrete do/don't statement
- Ready to drop into `AGENTS.md` verbatim

Use this format for each rule:

```markdown
N. **<Rule name>.**
   "<The rule as a do/don't statement.>"
   *Grounded in: <one-phrase reference to the session event that motivated it>.*
```

More than 15 rules is noise. If you have 20 candidates, pick the 15 with the
highest signal. The grounding line makes it easy for the user to evaluate each.

---

### Final summary table

After Parts 1–3, append this table:

```markdown
| Skill | Priority | Approx scope |
|-------|----------|--------------|
| `<skill-id>` | high / med / low | <1-3 word estimate, e.g. "2-day build"> |
```

Priority guidance:
- **high** — generalizes broadly, would have helped multiple times in this session
- **med** — useful but narrow scope or requires specific context
- **low** — nice to have, low reuse potential

This is the user's pick-list for what to build next. Do not recommend an order
or prescribe which ones to fund — that's the user's call.

---

## Mode B — execution

Mode B creates an implementation-grade package in a feature branch.

### Step B-1 — create the feature branch

```
git checkout -b feat/retrospective-<YYYYMMDD>
```

Use today's date for `YYYYMMDD`.

### Step B-2 — create the directory tree

At repo root:

```
retrospective/
  README.md                          # top-level index
  <skill-name-1>/
    README.md                        # human motivation
    SPEC.md                          # implementation-grade detail
    excerpts.jsonl                   # session evidence (optional)
    examples/                        # concrete templates (optional)
  <skill-name-2>/
    ...
  agents-md-template/
    README.md
    SPEC.md
```

### Step B-3 — write `retrospective/README.md`

Contents:
1. Why this directory exists (one paragraph)
2. Skill-index table with links, priority, and one-line summary per skill
3. "How to consume this package" — how a future agent should use these files

### Step B-4 — for each skill, write `README.md` and `SPEC.md`

**Each `README.md`** must cover:
- Why this skill matters
- When it would have helped — a concrete session example
- What "good looks like" when the skill runs correctly
- Cousin skills (related, complementary)
- Status: "Spec only — no code yet"

**Each `SPEC.md`** must cover:
- Trigger conditions (direct + proactive)
- Inputs (parameters and defaults)
- Outputs (what the skill produces)
- Workflow steps (numbered, detailed)
- Templates (verbatim prompt or code structures)
- Anti-patterns
- Implementation notes
- Test plan
- Living document note

Quality bar: each `SPEC.md` must be detailed enough that a future builder
agent, given only that file as a brief, can produce the skill without access
to the original session.

### Step B-5 — write `excerpts.jsonl` where valuable

One JSONL record per session excerpt that illustrates a skill or rule. Each
record has at minimum: `id`, `kind`, `phase`, `demonstration`. Use verbatim
error messages and code — not paraphrases. The value is fidelity.

### Step B-6 — write `agents-md-template/README.md` and `SPEC.md`

This sub-directory holds the proposed AGENTS.md additions as a spec of their
own — so a future agent can review, amend, and apply them.

### Step B-7 — DO NOT implement the skills

This branch is spec only. If you find yourself writing implementation code,
stop. That work belongs in a separate task after the user reviews and approves
the package.

### Step B-8 — commit, push, open PR

```
git add retrospective/
git commit -m "docs: retrospective skill specs — <N> skills + AGENTS.md template"
git push -u origin feat/retrospective-<YYYYMMDD>
```

Open a PR. Body should include the skill-index table. Do not merge unless the
user explicitly requests it.

---

## Tone rules

- **Honest about misses.** A retrospective with no "I would do this
  differently" entries is incomplete. Do not soften or omit mishaps.
- **Concrete about scope.** Name what's in, what's out, and why.
- **Suggest, don't prescribe.** The user decides what survives and what to
  build next.

---

## Anti-patterns (never do these)

- **Implementing while retrospecting.** If the user says "build it", that is
  a separate task. Wait for an explicit instruction before writing code.
- **One giant unstructured document.** The Part 1/2/3 split is not optional —
  it makes the output skimmable.
- **Generic advice.** "Write good prompts" is useless without a session anchor.
  Every teaching must be traceable to something that actually happened.
- **Forgetting Part 3.** AGENTS.md rules are often the highest-ROI output of
  a retrospective. They can be applied immediately, without building anything.
- **Capping at "what went well."** The misses ARE the lessons. If the session
  had no mishaps worth recording, look harder.
- **Skipping the mode question.** If it's ambiguous whether the user wants
  inline markdown or a packaged feature branch, ask first. Producing the
  wrong mode wastes everyone's time.
- **Producing speculative skill candidates.** Only propose skills that have
  direct evidence in the scan. If nothing in the session demonstrates the need,
  leave it out.
