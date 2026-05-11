# `self-retrospective` — Implementation Spec

## 1. Trigger conditions

**Direct user requests:**
- "Do a retrospective"
- "What did we learn?"
- "What skills could we extract?"
- "Lessons learned?"
- "Anything to add to AGENTS.md?"

**Proactive triggers** (skill should offer when):
- Session has spanned multiple distinct phases or pivots
- Session surfaced unexpected real-world findings (bugs, transport quirks, spec contradictions)
- Session used many subagents (≥5) or required novel orchestration
- Session has discovered workarounds for tool / sandbox limitations
- Session has run >2 hours of total agent time
- User says something that suggests session-wrapping ("OK we're done", "good work", "let's stop here")

**Negative triggers:**
- Routine sessions that just exercised a known pattern.
- Sessions where the user hasn't done substantive work yet.

## 2. Output structure (the spine)

The retrospective has three parts in this order. Each part is mandatory; skipping one leaves significant value on the table.

### Part 1 — what happened (narrative)

**Phase-by-phase summary.** Each distinct phase of the session gets a named heading and 1-3 paragraphs:

- What was the goal of this phase?
- What was the planned approach?
- What actually happened (especially deviations)?
- What was unplanned but mattered (operational mishaps, recoveries, surprises)?

**Metrics table** at the end of Part 1:

| Metric | Value |
|--------|-------|
| Subagents dispatched | N (by category if useful) |
| PRs opened / merged | M / K |
| Real-world bugs discovered + fixed | B |
| Tests added (before / after) | X / Y |
| Spec amendments | S |
| Scenarios driven / skipped | D / Sk |
| Files touched at major refactors | F |

### Part 2 — skills to extract

For each skill candidate, use the uniform template:

```markdown
### Skill N: `<skill-id>` — <one-line summary>

**Purpose.** <One sentence: what problem this skill solves.>

**Trigger.** <When this skill should activate.>

**Core content.** <Numbered list of 5-10 substantive teachings.>

**Anti-patterns.** <What NOT to do — based on session misses.>

**Example/template.** <Concrete code or text where useful.>
```

Aim for 200-500 words per skill. Detailed enough that later building from each spec is straightforward; not so detailed that the retrospective becomes the implementation.

### Part 3 — AGENTS.md / repo conventions

One-line rules, each grounded in something that went wrong (or nearly did). Format:

```markdown
N. **<Rule name>.**
   "<The rule, phrased as a do/don't statement, ready to drop into
   AGENTS.md verbatim.>"
```

Aim for 5-15 rules. More than 15 is usually noise.

### Final summary table

After all three parts, a sortable table:

| Skill | Priority | Approx scope |
|-------|----------|--------------|
| ... | high/med/low | ... |

This is the user's pick-list for what to build next.

## 3. The scan checklist (what to harvest)

When walking the session for material, look for:

### 3.1 Bugs you fixed
Each bug is candidate content for either a skill (if generalizable) or an AGENTS.md rule (if project/runtime-specific).

Distinguish three kinds:
- **Implementation defects** — your code did the wrong thing.
- **Spec defects** — the design itself was broken.
- **Transport / environment quirks** — the runtime surprised you (escaping, identity, permissions, naming).

### 3.2 Workarounds you invented
When a tool didn't do what you needed and you went around it, that workaround is reusable.

### 3.3 Recurring micro-patterns
Anything you typed >2 times. If it's worth typing twice, it's worth templating.

### 3.4 Operational mishaps
**Especially valuable.** Each near-miss becomes a "don't do X" rule.
Examples:
- Force-pushed feature branch back to main → PR auto-closed.
- Subagent ran out of usage mid-task → recovery from local commit.
- Marker comments didn't appear → workflow YAML wasn't on main yet.

### 3.5 Subagent prompts that worked vs didn't
Meta-lesson on briefing future subagents.

### 3.6 Scope decisions
What you skipped and *why*. The "why" is the lesson.

### 3.7 Discoveries about the runtime
Auth boundaries, identity quirks, rate limits, naming collisions — hard-won and should be captured.

### 3.8 Effective or innovative workflows
Workflows described by the user and/or evolved in conjunction with the agent as the session evolved. Only include workflows that had some benefit.

## 4. What NOT to include

- Step-by-step replay of routine work.
- Self-evaluation / praise.
- Speculation about features the system "should" have.
- Code (beyond illustrative snippets — the skill files hold code).
- Internal subagent transcripts (just summaries).

## 5. Output deliverable

The skill supports **two deliverable modes**. Ask if it's not obvious which the user wants.

### 5.1 Mode A — chat-only retrospective (the default)

A markdown document delivered inline in the chat, with the three-part structure and the final summary table. Best when:

- The user wants to **review** the lessons before deciding what to do with them.
- The session was short or the lessons are few.
- The user explicitly asks for "a retrospective" without mentioning files or branches.

Cap output at ~5000 words. If more is needed, recommend mode B.

### 5.2 Mode B — package mode (the implementation-grade deliverable)

A **filesystem package** committed to a feature branch and pushed, ready for future skill-build tasks to consume. Best when:

- The user says things like "create a feature branch", "package these for later", "create specs and READMEs", "I want to capture this for later implementation."
- The session was long and lessons are many (5+ skills).
- The user wants to dispatch each skill build as a separate task later.

#### Recipe for mode B

1. Create a feature branch: `git checkout -b feat/retrospective-skill-specs`
2. Create the directory tree at repo root:
   ```
   retrospective/
     README.md                            # top-level index
     <skill-name-1>/
       README.md                          # human motivation
       SPEC.md                            # implementation-grade detail
       excerpts.jsonl                     # session evidence (optional)
       examples/                          # concrete templates (optional)
     <skill-name-2>/
       ...
     agents-md-template/
       README.md
       SPEC.md
   ```
3. Top-level `retrospective/README.md` has: why the directory exists, the skill-index table (priority + one-line summary per skill, with links), and a "How to consume this package" section.
4. For each skill's `README.md`: why this skill matters, when it would have helped (concrete session example), what good looks like, cousins, status ("Spec only — no code yet").
5. For each skill's `SPEC.md`: trigger conditions, inputs, outputs, workflow steps, templates, anti-patterns, implementation notes, test plan, living document note.
6. `excerpts.jsonl` when valuable: JSONL, one record per line, each with `id`, `kind`, `phase`, `demonstration` plus skill-specific fields. Actual error messages, actual fix code — not paraphrases.
7. `examples/` when valuable: concrete templates, good-vs-bad prompts, sample YAML.
8. `agents-md-template/` is special: spec for repo-level convention additions.
9. DO NOT implement the skills in this branch.
10. Commit with message format: `docs: retrospective skill specs — N skills + AGENTS.md template`
11. Open a PR. Body summarizes the index table. Don't merge unless user requests it.

#### Quality bar for mode B

A good package is one where:
- Each `SPEC.md` is detailed enough that a future builder agent, given just that file as a brief, can produce the skill without needing the original session.
- Each `README.md` makes the case clearly enough that a stakeholder can decide whether to fund the build without reading the SPEC.
- Session-specific failures, fixes, and quotes appear in `excerpts.jsonl` — verbatim, not paraphrased.

## 6. Tone

- **Honest about misses.** A retrospective with no "I would do this differently" entries is incomplete.
- **Concrete about scope.** List what's in, what's out, why.
- **Suggest, don't prescribe.** The user picks what survives.

## 7. Anti-patterns

- **Implementing while retrospecting.** Wait for explicit "now build it."
- **One giant unstructured document.** The Part 1/2/3 split makes it skimmable.
- **Generic advice.** "Write good prompts" is useless. Ground all rules in specific session events.
- **Forgetting Part 3.** Repo conventions are often the highest-ROI output.
- **Capping at "what went well."** The misses ARE the lessons.

## 8. Skill invocation

```
/retrospective                           # the default
/retrospective --no-skills               # skip Part 2 (just narrative + AGENTS.md)
/retrospective --output-dir ./retro/     # produce a full directory tree
/retrospective --since "2025-01-15"      # only material since this point in session
```

## 9. Test plan (when built)

- Run on a known session transcript.
- Verify output covers all three parts.
- Verify each skill candidate has the uniform shape.
- Verify each AGENTS.md rule is grounded in a session event.

## 10. Living document

Add new scan-checklist items as new kinds of valuable lessons surface in future sessions.

## 11. Meta-note

This SPEC.md is itself an output of `self-retrospective` being applied to a session. The retrospective in chat → user requested "create the directory" → here we are. If a future agent wants to build this skill, it should study the `retrospective/` directory in the poc-github-ai-sandbox repo as a worked example of what the skill produces.
