# Compound Knowledge plugin — deep dive

**Round:** 3, Thread 11 (PLAN.md §11.11)
**Author:** subagent on `claude/parallelize-with-subagents-SO0nR--sub-15`
**Date:** 2026-05-11
**Primary source-of-truth:** `github.com/EveryInc/compound-knowledge-plugin` (README.md, plugins/compound-knowledge/AGENTS.md, CHANGELOG.md, 6 SKILL.md files, 5 agents/*.md files — all fetched via raw.githubusercontent.com)
**Secondary:** every.to essay "The Agent That Saved My Brain" (Cloudflare-blocked, see §7)

---

## 1. The one-line claim and what changes

Tedesco's Compound Knowledge plugin (CK) is the knowledge-work twin of the Compound Engineering plugin (CE). Same loop, same Git-tracked Markdown substrate, same parallel research-then-write rhythm — but operating on plans, briefs, strategies and analyses rather than bug fixes and features. CK is at v1.0.0 (2026-03-22); v0.1.0 (2026-02-19) shipped the five core skills as commands, v0.2.0 (2026-02-23) added `kw:confidence`, and v1.0.0 migrated `commands/kw/` to `skills/kw-*/SKILL.md` and introduced the three research agents.

Architecture 2's knowledge layer was modelled on CE. CK reveals two things CE does not, and one thing CE does more cleanly:

- **A four-way classification of learnings** (insight / playbook / correction / pattern) that is strictly typed and lives in frontmatter — replacing CE's two-track (bug / knowledge) distinction.
- **A "no silent overwrites" rule** stated explicitly inside the orchestrator skill (`kw:compound` §3.5), with the agent / orchestrator division of write authority spelled out in a `<critical_requirement>` block.
- **A confidence-check primitive** (`kw:confidence`) that is a *first-class skill*, callable from anywhere in the loop, rather than an inline rule baked into individual reviewers.

These are not stylistic differences. They sharpen Architecture 2 §3.2 (knowledge-document shape), §3.4 (Curator role), and §7 (knowledge architecture).

## 2. The skill loop and its analogues to CE

The README defines the loop as:

```
/kw:brainstorm  -->  Brain dump, pull references, find the shape
/kw:plan        -->  Structure into an actionable plan
/kw:confidence  -->  Gut-check what you know vs. don't (callable at any point)
/kw:review      -->  Strategic alignment + data accuracy check
/kw:work        -->  Execute the plan, produce deliverables
/kw:compound    -->  Save learnings for next time
```

The CE analog is `/ce:plan` → `/ce:work` → `/ce:review` → `/ce:compound` plus the separate `ce-compound-refresh` cadence. The mapping is one-to-one with three notable additions on the CK side:

| CK skill | CE analog | Notes |
|---|---|---|
| `kw:brainstorm` | (no direct analog — closest is the inline ideation in `ce:plan`) | CK promotes brain-dump-into-origin-document to a first-class step, producing `plans/brainstorm-{name}.md` files that `kw:plan` later treats as the **origin document**. |
| `kw:plan` | `ce:plan` | CK adds two-axis typing: **work type** (Strategy / Campaign / Brief / Research / Operations) and **detail tier** (Quick / Standard / Deep). |
| `kw:confidence` | (no direct analog) | A standalone non-destructive interrupt skill. See §6. |
| `kw:review` | `ce:review` | Two parallel reviewer agents instead of CE's 14-agent army. Same P1/P2/P3 grouping. |
| `kw:work` | `ce:work` | Same batch-then-execute discipline; the execution log is appended to the plan file as a `## Execution Log` section so `kw:compound` has concrete material. |
| `kw:compound` | `ce:compound` | Identical loop-closing role. CK adds explicit `kw:refresh`-style stale-detection *inline* (not as a separate skill). |

**Important divergence:** CK does *not* ship a separate `kw:refresh` skill. Where CE runs `ce-compound-refresh` on a weekly cadence with five outcomes (Keep / Update / Consolidate / Replace / Delete), CK folds the staleness check *into every `kw:compound` invocation* via the `stale-knowledge-checker` agent. The CK design is tighter — no drift between learnings and curation — but has no batch consolidation pass. This is the most consequential divergence for Architecture 2: §3.4 currently has both a Knowledge Curator (per-cycle) and a Refresh Curator (separate cadence). CK suggests the Refresh Curator's *contradiction-detection* responsibility belongs inline with the Curator; only *batch consolidation* warrants the separate cadence.

## 3. The four-way classification

CK frontmatter is strictly typed. Every `docs/knowledge/*.md` file declares one of four `type:` values, set when `kw:compound` extracts the learning:

| Type | Signal (from kw:compound §1) | Example |
|---|---|---|
| **insight** | "We discovered…", surprising finding, counter-intuitive result | "Trial Conversion Timing" — extended trials net positive after 60 days |
| **playbook** | Repeatable process that worked, step-by-step that others could follow | "How to run a Q-launch campaign in week 1" |
| **correction** | Wrong assumption fixed, data source clarified, definition updated | "Revenue metrics come from dashboard A, not dashboard B" |
| **pattern** | Something that keeps recurring, systemic observation | "Q1 launches always under-perform in week 2" |

Other typed fields in the frontmatter: `tags` (list, used by the knowledge-base-researcher's grep), `confidence: high | medium | low`, `created` (date), `source` (free-text description of what triggered the learning).

**Comparison to CE's two-track scheme.** CE distinguishes only `problem_type: bug | knowledge` (Architecture 2 §3.2). CK's four-way split is *not* a refinement of CE's knowledge track — it operates one level up. In CE, corrections are caught implicitly via the five-dimensional overlap check; in CK, *correction* is a first-class type.

**Why this matters for Architecture 2.** §3.2 should add a `learning_type: insight | playbook | correction | pattern` axis for the knowledge track. The correction type deserves first-class status — the stale-knowledge-checker rule says: "Corrections always win. If the new learning is a correction (type: correction), it takes precedence over older entries on the same topic." That precedence rule is impossible to express without typed corrections.

## 4. The stale-knowledge-checker

The agent (`agents/research/stale-knowledge-checker.md`) defines a discipline Architecture 2 currently underspecifies.

**Trigger:** runs inside `kw:compound` *after* the user has approved the draft learning but *before* the orchestrator writes any file.

**Procedure.** (1) Read the new learning. (2) Search `docs/knowledge/` for entries with overlapping tags, similar titles, same domain. (3) For each match, classify the relationship:
- **Contradicts?** → Update / Remove / Merge.
- **Supersedes?** New learning covers the same ground with more/better information. → Archive or remove.
- **Complements?** Different aspects of the same topic. → No action.

Output is structured text (no file writes). The agent prefers Update or Merge over Remove ("Knowledge is expensive to recreate"); flags old `confidence: low` entries as cleanup candidates but never deletes them.

**Compared to Architecture 2's Refresh Curator.** §3.4 / §7 say the Refresh Curator runs *over the entire store* on a schedule with five outcomes. The CK stale-knowledge-checker runs *over candidates overlapping a single new learning* with three outcomes. These are complementary, not substitutes: CK handles *contradictions at write time*; a Refresh Curator still has work at *consolidation time* (merging three insights about the same topic into one).

## 5. The two reviewers — what they catch

CK ships exactly two review agents, both invoked in parallel by `kw:review`. This is a deliberately small army compared to CE's 14 reviewers.

### 5.1 strategic-alignment-reviewer

Frame: "If a skeptical executive reads this, will they trust that we're solving the right problem the right way?" Seven-item checklist: **Goal clarity** (explicit, measurable outcome — not "improve engagement" but "increase trial-to-paid conversion from X% to Y%"); **Hypothesis falsifiability** ("If we do X, then Y will change by Z" — if it can't be wrong, it's not useful); **Success metrics** (measurable and connected to goal; flag vanity metrics); **Scope proportionality** (flag building a platform for a one-off); **Resource awareness** (time, people, tools, budget stated); **Strategic consistency** (matches the project's CLAUDE.md); **Opportunity cost** (what we are NOT doing). Findings: `[P1|P2|P3] [Strategic]: …` with `→ Suggestion:` line.

### 5.2 data-accuracy-reviewer

Frame: "Would this survive a stakeholder asking 'Where'd you get that?'" Seven-item checklist: **Source citation** (dashboard / file path / API / calculation); **Comparison baselines** ("+32%" is incomplete; "+32% WoW" is complete); **Canonical definitions** (match the project's data context file); **Freshness** (>48h stale = warning, >7 days = P2); **Caveats acknowledged**; **Hardcoded vs live** (flag hardcoded "current MRR" in a plan that will be re-read later); **Baseline appropriateness** (weekend skew, anomalous periods). The agent verifies values against sources where it can ("Verify, don't assume"). Its precision-vs-accuracy distinction is sharp: "A number can be precisely stated and completely wrong. Check the source, not just the format."

### 5.3 What this implies for Architecture 2

Architecture 2 currently has a long roster of CE-style review personas. CK suggests two of them are load-bearing for *any* knowledge artifact independent of the language (code or prose): **strategic alignment** and **data accuracy**. These are not CE reviewer types. The CE army is mostly code-focused (security, performance, schema, etc.) plus a few cross-cutting ones (consistency, naming). Architecture 2 may want to add the strategic-alignment and data-accuracy roles explicitly when applying the architecture to artefacts that include non-code content (ADRs, design docs, postmortems, customer-facing docs).

## 6. The confidence primitive (`kw:confidence`)

This is the cleanest design move in CK and the one with no CE analog.

**Shape.** A standalone skill, callable at any point in any workflow. Non-destructive: if invoked mid-`kw:work` at task 3, it pauses, runs the assessment, and after the user decides "Proceed," explicitly re-anchors with "Resuming `/kw:work` at Task 3."

**Procedure.** Identify what's being assessed (active task / plan / file). Internally assess task understanding, information sufficiency, approach certainty, risk awareness — but *do not output as a checklist*. Produce a plain-prose check with three sections: **Confident about** (specific — name files, patterns, prior experience), **Less confident about** (specific gaps), **My recommendation** (one of "Proceed.", "Proceed, but [caveat].", "Pause for [specific thing]."). High confidence → two sentences, no forced breakdown. If user picks "Increase confidence," produce a *ranked* list of executable actions ("Read `data/q4-results.csv` to confirm the $50K benchmark", not "gather more data").

**The Important Rules** encode a discipline Architecture 2 doesn't currently name:

- **Never give a number.** No percentages, no 1-10 scales. Prose only.
- **Don't hedge on what you know.** "Confidence theater — hedging on everything to seem careful — is worse than overconfidence."
- **Actions must be executable.** No "gather more data" — only "read file X."
- **Non-destructive interrupt.** Resume the parent workflow exactly where you left off.
- **This is not `/kw:review`.** Confidence assesses *what you know and don't know* — your epistemic state. Review assesses whether a *finished artifact* is good enough.

**Implication for Architecture 2.** The atelier currently has implicit confidence-checking inside review. CK suggests promoting this to an orthogonal skill. The epistemic-state vs artifact-state distinction is real: a planner producing a deeply-uncertain plan and a planner producing a polished plan about poorly-grounded data are *different failure modes*. The "no number" rule deliberately avoids false precision — aligned with §3.2's three-bucket categorical `confidence: high | medium | low`.

## 7. The "no silent overwrites" stance

Stated most clearly in `kw:compound` §3.5, in a `<critical_requirement>` block:

> Agents return TEXT only. They must NOT write or delete files. Only the orchestrating compound skill writes files — both new learnings and updates to stale entries.

The same rule appears in every research agent's Rules section: "Return text only. Never write files." This is a *capability-restriction* discipline: agents *could* write files (their tool permissions allow it), but the contract forbids it. The orchestrator is the only place file writes happen.

**Why this matters.** Every write is auditable through one chokepoint. The user can read the skill source to know exactly what gets written and when. No agent can silently mutate the knowledge store; every mutation is traceable to a skill invocation.

**Architecture 2 currently does not specify this.** §3.4 names the Knowledge Curator as a persona; §7 describes the store as flat markdown files. There is no rule that says *only the orchestrating skill writes; agents return text.* CK's `<critical_requirement>` block is a one-line spec that closes a real gap in §4 and §7.

## 8. Architecture 2 sharpenings

Concrete edits suggested by reading CK:

1. **§3.2 frontmatter:** add a `learning_type: insight | playbook | correction | pattern` axis for the knowledge track. Specify that corrections take precedence over older entries on the same topic.
2. **§3.4 Refresh Curator:** split into (a) inline contradiction-detection at write time (CK's stale-knowledge-checker pattern), (b) batched consolidation on a schedule (CE's existing pattern). §3.4 currently conflates the two.
3. **§4 Persona panel:** add a `kw:confidence`-style **Confidence Auditor** — callable at any point, returns prose, no numbers, non-destructive. Distinguish epistemic-state from artifact-state review.
4. **§4 Reviewer roster:** for non-code artefacts, explicitly call out strategic-alignment and data-accuracy as load-bearing. CE's reviewer army is code-flavored; CK shows the two universal ones.
5. **§7 Write authority:** add — "Agent personas return structured text. Only orchestrator skills write files." Codifies CK's `<critical_requirement>`.
6. **§3 Origin documents:** brainstorm artefacts as first-class — `plans/brainstorm-*.md` survives across the loop as the *origin document* that the planner references and cross-checks.

## 9. Sources and status

| Source | Status |
|---|---|
| README.md, AGENTS.md, CHANGELOG.md (plugin root) | FULL |
| 6 SKILL.md files (kw-brainstorm, kw-plan, kw-confidence, kw-review, kw-work, kw-compound) | FULL |
| 2 review agents (strategic-alignment, data-accuracy) | FULL |
| 3 research agents (knowledge-base, past-work, stale-knowledge-checker) | FULL |
| every.to "Agent That Saved My Brain" | BLOCKED (Cloudflare 403) — background-only; plugin files are source-of-truth |
| api.github.com tree listing | RATE-LIMITED — worked around via raw.githubusercontent.com |

**Blocked URLs:** every.to/p/the-agent-that-saved-my-brain. **Fetch issue filed:** none — the essay is background-only; the plugin's GitHub files are the source-of-truth per the brief and were fully fetchable.

## 10. Open follow-ups

- The CHANGELOG mentions "Push to Proof" integration at every handoff. "Proof" is an Every-internal product (not part of the plugin). The hook points exist in every kw skill's final AskUserQuestion. Worth one-line note in Architecture 2 if/when external knowledge-sharing endpoints are added.
- The `kw:work` skill writes `## Execution Log` sections to the plan file. This is the bridge that lets `kw:compound` find concrete material to learn from. Architecture 2 currently has `pulse reports` (§6, mentioned but not specified) — recommend matching the CK pattern: execution log lives in the plan file, not in a separate location.
- The `kw:plan` skill's auto-classification of work type (Strategy / Campaign / Brief / Research / Operations) is the only CK skill that uses a typed work-type axis. Worth examining whether Architecture 2's planner should similarly auto-classify problem statements by track at intake.

---

**Status:** SUCCESS — all GitHub source-of-truth files were fetched in full; the Cloudflare-gated essay was redundant to the brief's extraction targets and is documented as background-only.
