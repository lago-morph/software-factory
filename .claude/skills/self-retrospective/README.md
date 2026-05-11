# self-retrospective

A skill that harvests session knowledge before it's lost to context truncation.
Turns a completed session into a structured retrospective: what happened,
which skills are worth extracting, and which repo conventions should be added
to `AGENTS.md`.

```
scan session → Part 1: narrative → Part 2: skill candidates → Part 3: AGENTS.md rules
```

## When to use

### Direct triggers

Use this skill when the user says any of:

- "Do a retrospective"
- "What did we learn?"
- "What skills could we extract?"
- "Lessons learned?"
- "Anything to add to AGENTS.md?"

### Proactive triggers

Offer this skill without being asked when:

- The session spanned multiple distinct phases or pivots
- The session surfaced unexpected real-world findings (bugs, transport quirks, spec contradictions)
- The session used ≥5 subagents or required novel orchestration
- The session discovered workarounds for tool or sandbox limitations
- The session ran >2 hours of total agent time
- The user says something session-wrapping: "OK we're done", "good work", "let's stop here"

**Not** for routine sessions that exercised a known pattern, or sessions where
the user hasn't done substantive work yet.

## The 3-part output

Every retrospective has these three parts in order. Skipping any one leaves
significant value on the table.

| Part | Contents |
|------|----------|
| 1 — What happened | Phase-by-phase narrative + metrics table |
| 2 — Skills to extract | Each skill candidate in a uniform template |
| 3 — Repo conventions | AGENTS.md-ready rules, each grounded in a session event |

After all three parts: a final summary table (`Skill | Priority | Approx scope`)
as the user's pick-list for what to build next.

### Part 1: narrative + metrics

Each distinct phase of the session gets a heading with 1-3 paragraphs covering:
the goal, the planned approach, what actually happened (especially deviations),
and anything unplanned that mattered.

Followed by a metrics table:

| Metric | Value |
|--------|-------|
| Subagents dispatched | N |
| PRs opened / merged | M / K |
| Real-world bugs discovered + fixed | B |
| Tests added (before / after) | X / Y |
| Spec amendments | S |
| Scenarios driven / skipped | D / Sk |
| Files touched at major refactors | F |

### Part 2: skill candidates

Each candidate uses this uniform template:

```
### Skill N: `<skill-id>` — <one-line summary>

**Purpose.** <One sentence: what problem this skill solves.>
**Trigger.** <When this skill should activate.>
**Core content.** <Numbered list of 5-10 substantive teachings.>
**Anti-patterns.** <What NOT to do — based on session misses.>
**Example/template.** <Concrete code or text where useful.>
```

Aim for 200-500 words per skill: enough to build from later, not so much
that the retrospective becomes the implementation.

### Part 3: AGENTS.md rules

One-line rules, each grounded in something that went wrong (or nearly did).
5-15 rules; more than 15 is usually noise. Format:

```
N. **<Rule name>.**
   "<The rule, phrased as a do/don't statement.>"
```

## Two modes

### Mode A — chat-only (the default)

A markdown document delivered inline. Use when:

- The user wants to review lessons before deciding what to do with them.
- The session was short or the lessons are few.
- The user asked for "a retrospective" without mentioning files or branches.

Cap output at ~5000 words. If more is needed, recommend Mode B.

### Mode B — package mode

A filesystem directory tree committed to a feature branch and pushed. Use when:

- The user says "create a feature branch", "package these for later",
  "create specs and READMEs", or "I want to capture this for later implementation."
- The session has 5+ skill candidates.
- The user wants to dispatch each skill build as a separate task later.

Directory shape:

```
retrospective/
  README.md                    # top-level index with skill table
  <skill-name-1>/
    README.md                  # why this skill matters
    SPEC.md                    # implementation-grade detail
    excerpts.jsonl             # session evidence (optional)
    examples/                  # concrete templates (optional)
  <skill-name-2>/
    ...
  agents-md-template/
    README.md
    SPEC.md
```

Branch name: `feat/retrospective-<YYYYMMDD>`
Commit message: `docs: retrospective skill specs — N skills + AGENTS.md template`
Open a PR; do not merge unless the user asks.

## The scan checklist

Walk the session systematically for these 8 categories of material:

| # | Category | What to look for |
|---|----------|-----------------|
| 3.1 | Bugs fixed | Implementation defects, spec defects, transport/environment quirks |
| 3.2 | Workarounds invented | Any time a tool didn't work and you went around it |
| 3.3 | Recurring micro-patterns | Anything done >2 times — if worth doing twice, worth templating |
| 3.4 | Operational mishaps | Near-misses become "don't do X" rules — especially valuable |
| 3.5 | Subagent prompts | Which brief structures worked vs didn't |
| 3.6 | Scope decisions | What was skipped and *why* — the why is the lesson |
| 3.7 | Runtime discoveries | Auth boundaries, rate limits, naming collisions, identity quirks |
| 3.8 | Effective workflows | Workflows evolved during the session that had measurable benefit |

## What NOT to include

- Step-by-step replay of routine work
- Self-evaluation or praise
- Speculation about features the system "should" have
- Code beyond illustrative snippets (the skill files hold code)
- Internal subagent transcripts (just summaries)

## Anti-patterns

- **Implementing while retrospecting.** Wait for explicit "now build it."
- **One giant unstructured document.** The Part 1/2/3 split makes it skimmable.
- **Generic advice.** "Write good prompts" is useless. Ground all rules in specific session events.
- **Forgetting Part 3.** Repo conventions are often the highest-ROI output.
- **Capping at "what went well."** The misses ARE the lessons.
- **Skipping the mode question.** If it's not obvious whether the user wants A or B, ask before producing output.

## Integration with other skills

| Skill | Relationship |
|-------|-------------|
| `agent-dispatch-loop` | Complementary — the loop's iteration report goes in the repo; this skill produces input for building new skills from the session |
| `parallel-subagent-fanout` | Frequently surfaces as a skill candidate during retrospectives |

## Files in this skill

```
skills/self-retrospective/
├── README.md            ← this file
├── SKILL.md             ← executable skill instructions
└── spec/
    ├── README.md        ← original overview from the spec
    └── SPEC.md          ← full implementation spec
```
