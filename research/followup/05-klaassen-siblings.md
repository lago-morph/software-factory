# Klaassen's Chain-of-Thought Sibling Trilogy — Research Report

**Round-3 Thread 5** per `research/PLAN.md` §11.5. Extends `research/03-every-compound-engineering.md` with three sibling Every.to pieces that add (a) "spec authorship as meta-skill" framing, (b) fidelity-tiered research strategies for "senior-engineer thinking," and (c) the Opus 4.5 model-floor argument.

**Date:** 2026-05-11
**Fanout run:** 20260511-054258, sub-08

---

## Sources covered

| URL | Author / date | Direct fetch | Indirect material |
|-----|---------------|--------------|-------------------|
| https://every.to/chain-of-thought/stop-coding-and-start-planning | Klaassen, Nov 6 2025 | **BLOCKED** (HTTP 403, Cloudflare) | WebSearch snippets |
| https://every.to/source-code/stop-coding-and-start-planning-be0b4fd1-5898-4b09-bfda-0b00ea0004fd | canonical alias | **BLOCKED** | same |
| https://every.to/chain-of-thought/teach-your-ai-to-think-like-a-senior-engineer | Klaassen | **BLOCKED** | WebSearch snippets + HN #45850475 (also blocked) |
| https://every.to/chain-of-thought/how-every-is-harnessing-the-world-changing-shift-of-opus-4-5 | Klaassen / Every | **BLOCKED** | WebSearch snippets + Klaassen X posts |

**Status: PARTIAL.** Direct WebFetch returns 403 (same Cloudflare gating as Rounds 1–2 per `research/blocked-urls.md`); Wayback Machine is also blocked from this sandbox. WebSearch surfaces snippet-level material including direct quotes, named frameworks (the "fidelity levels"), worked examples (Cora email-bankruptcy / Figma case; 30-minute churn feature; 10-Thanksgiving-projects swarm), and the "compounding engineering" thesis. Verbatim quotes are marked with quotation marks; reconstructions are flagged.

**No fetch issue filed:** prior round-2 fetch issues (`research/blocked-urls-round-2.md`) already cover the every.to host pattern; the manual-cookie workflow used for the four already-drained Every articles is the canonical resolution path. Flag for synthesis: this report's claims are second-hand and should be re-verified against manual fetches before being treated as canonical.

---

## 1. "Stop Coding and Start Planning" (Klaassen, Nov 6 2025)

### Thesis

*"The fastest way to teach is not through code you write, but through plans you review."* Planning is reframed from cost to **leverage** — it teaches the system, then compounds across every future feature.

### Spec authorship as meta-skill — the angle this article adds

The canonical guide says "Plans are the new code." This article makes the stronger meta-claim: **the spec is the artifact that teaches the AI how you think.**

- *"AI made us sloppy because it made us forget how to plan. Planning used to be a non-negotiable part of the work: sketching screens, prototyping flows, and writing problem statements."*
- The decision flip: *"One approach ships a feature… the other ships a feature and teaches the system how you think for next time."*

The instructional shape for plan-prompts is explicit and copyable:

> *"Research how we handle validation elsewhere in the codebase, check if our email library has built-in validation, look up best practices for user-friendly error messages, then create a plan showing three approaches with tradeoffs."*

Four clauses: (1) survey internal patterns, (2) survey local tooling, (3) survey external best-practices, (4) **produce N alternatives with tradeoffs.** "Three approaches with tradeoffs" is the most concrete spec-authorship primitive in any Every article: it forces the AI to externalize judgment so the human can rule.

### The Figma → five-screens → Puppeteer-review worked example

The Cora **email-bankruptcy feature** — *"a free service that clears users' inbox for them without deleting anything important."* Five Figma screens, one hour of planning, then *"did other work"* while the agent built.

> "After completing the plan, he added a second agent to review the work by comparing the Figma screenshot to what got built using Puppeteer, noting every difference, and iterating until they match."

Result: *"five screens, pixel-perfect, including mobile layouts that were never even designed for."*

The new primitive: **plan → build → visual-diff review → iterate** as a single chained unit, not three loose agents.

### "Spend an hour teaching AI how you think" — concretely

1. **Write plan instructions in your voice.** The plan is the *meta-prompt* — which patterns to mine, which libraries to prefer, which alternatives to surface for your review.
2. **Spell out the survey scope:** internal codebase, local tooling, external best practices.
3. **Demand alternatives with tradeoffs.**
4. **Append a review-agent** that checks the build against the spec (Puppeteer/Figma-diff is the example).
5. **Keep the plan and review-agent around** — they become reusable across subsequent features in the same surface area.

The "an hour" claim is load-bearing: planning is a **one-time setup cost per surface area** that amortizes across many features. The engineer's output scales with the quality of the *plan corpus*, not typing speed.

Search snippets reference a *"framework for deciding when to plan versus when to prototype"* — full framework not visible; likely overlaps with article 2's fidelity tiers. **Mark provisional.**

---

## 2. "Teach Your AI to Think Like a Senior Engineer" (Klaassen)

### Angle this article adds

A **tiered research methodology**. Don't run heavy planning machinery on every task — match planning depth to the task's *fidelity*. This converts "planning is leverage" (article 1) into "planning is a graded tool."

### The three fidelity levels

| Fidelity | Description | Examples |
|----------|-------------|----------|
| **One** | Quick fixes | One-line changes, obvious bugs, copy updates |
| **Two** | Multi-file features with clear scope but non-obvious implementation | Validation rule across API + UI |
| **Three** | Major features where you don't even know what you're building yet | New product surface; needs discovery first |

Eight planning strategies map onto these tiers. Snippets confirm only two by name:

- **Reproduction-first** (F1, F2 — especially bug fixes): *"Attempts to reproduce bugs or issues before planning fixes."* A small agent writes the failing test before the plan begins.
- **Parallel research before code** (all tiers): *"Running multiple specialized research agents in parallel before writing any code helps prevent building the wrong solution entirely."*

The remaining six are not visible in snippets. Likely candidates (from the canonical researcher roster in `research/03-…`): repo-research-analyst, framework-docs-researcher, best-practices-researcher, spec-flow-analyzer, learnings-researcher, git-history-analyzer, issue-intelligence-analyst, session-historian, slack-researcher, web-researcher. **Mark provisional.**

### Persona shape that produces senior-engineer thinking

1. **Parallel specialization, not one big-brain model.** *"Multiple specialized research agents in parallel… the human contributes judgment and taste."*
2. **Taste accumulation as a first-class output.** *"These agents accumulate your taste over time—every time you indicate 'I don't like this' or 'Good catch,' the system gets smarter."* Persistent-memory persona, not stateless prompt.
3. **Judgment-vs-implementation split.** *"The human's contribution is taste, judgment, and context about what matters for your product and users."* Senior-engineer thinking is defined by what the human *withholds* (typing) and *contributes* (rulings).

### New primitives not in the main guide

- **Fidelity tiering** as a triage discipline at plan-entry. The canonical guide has "Lightweight / Standard / Deep" ceremony but does not name the three tiers as *fidelity levels* or pin them to a research-strategy set. Cleaner naming = the new primitive.
- **Reproduction-first as canonical F1/F2 entry point.** For any bug-class task, the first research agent writes the failing reproduction; only then does planning proceed. Narrows the plan's job to "fix this reproduction" instead of "diagnose then fix."
- **Copy-don't-build invitation.** *"The article includes GitHub links throughout so readers can copy and adapt the exact agents and commands used."* The article *is* the documentation for adopters of the public plugin.

The canonical guide already says *"Every codebase reflects the taste of the developers… The solution is to extract and document these choices."* This sibling is the operating manual for that extraction: fidelity-tier, parallel-research, let the human rule, capture rulings as future agent instructions.

---

## 3. "How Every Is Harnessing the World-changing Shift of Opus 4.5"

### Angle: the model-floor argument

Compound engineering's parallel-agent architecture only works above a model-capability floor. The claim: **Opus 4.5 cleared that floor** — and "what compound engineering can do" should be re-read every time the floor moves.

### Klaassen's framing

- *"Opus 4.5 is insane. Just shipped v2 of my compounding engineering plugin… This wouldn't have worked a week ago. Previous models would derail after the second parallel [thread]."*
- *"By far the most exciting model, maybe ever."*
- Thanksgiving anecdote: *"started 10 projects at once and kept sneaking away from Thanksgiving dinner to prompt more."*

### Capabilities Klaassen relies on

1. **Parallel-context coherence beyond two lanes.** Previous models *"would derail after the second parallel thread"*; Opus 4.5 *"held the context, made the right decisions, and shipped clean pull requests to both repos"* across more than two lanes. Unlocks the **agent-swarm** mode vs. the canonical three-lane setup.
2. **Decision-making without prompting back.** *"Opus 4.5 finished a churn detection feature in 30 minutes by making decisions and pushing forward rather than waiting for detailed specifications."*
3. **Cross-project orchestration.** While building **Every Board**, Klaassen *"realized the compound engineering plugin needed a fourth research agent for design work."* He created `/modify-plugin` that *"let the AI work on both the Every Board project and making changes to the compound engineering framework simultaneously."* Agent improves its own toolchain while shipping the feature.
4. **Sustained swarm reliability.** *"Stress-tested it by running 11 projects in roughly six hours, with none of them derailing."* Later: *"44 AI agents across multiple projects, with each one being just a model pointed at a folder."*
5. **End-to-end `/lfg` finally working.** *"With Opus 4.5, end-to-end flows from idea to PR are actually working, with the /lfg command handling planning, implementation, review, testing, screenshots, and PR creation without manual intervention."* The canonical guide describes `/lfg` aspirationally; this article says Opus 4.5 makes it real.

### New compound-engineering primitives

- **`/modify-plugin`** — a command whose explicit job is to let an agent extend the compound-engineering plugin itself *during* a feature build. Agent-modifies-tooling at finer grain than the canonical "agent rewrites prompt" pattern. The plugin's own surface area becomes a compounding target.
- **"The folder is the agent"** — *"44 AI agents… each one being just a model pointed at a folder."* The folder-as-agent claim collapses the agent-definition cost: a folder of files (prompts, knowledge, scripts) *is* the agent; scale by replicating folders.
- **Model-floor as a planning input.** When a new model raises the floor, re-evaluate which orchestration patterns become viable — parallel-lane count, unattended-autonomy depth, agent-self-modification scope.

### Model-floor as a design principle

Every compound-engineering architecture should be **dated to a model floor**. Klaassen's v2 plugin is dated to Opus 4.5. A factory on Opus 4.1 plateaus at ≤2 parallel lanes; Opus 4.5 unlocks swarms of 10–44; Opus 4.7 (referenced elsewhere in `research/03-…`) shifts again. Two design implications:

1. **Architecture variants pinned to model-class.** Don't ship one architecture — ship "this above this floor; this fallback below it."
2. **Re-validate when the floor moves.** Every new model release is a deliberate re-test of unattended-autonomy depth, parallel-lane count, agent-self-modification scope.

---

## Cross-article synthesis: three additions to compound engineering

1. **Spec authorship is the meta-skill** (Article 1). The spec teaches the system. Plan-prompts are higher-leverage than implementation prompts. "Three approaches with tradeoffs" is a portable primitive.
2. **Fidelity tiering with named research strategies** (Article 2). The human's first job is to tier the task. Reproduction-first for bugs; parallel research for novel features; taste-rulings flow back into every tier's library.
3. **Model-floor architecture** (Article 3). Plugins are versioned not just by feature but by the model floor they assume. Above-floor: large-N parallel swarms, agent-modifies-plugin self-extension, `/lfg` autonomy. Below-floor: degrade explicitly to the canonical three-lane setup.

Most actionable for `architectures/02-compound-atelier.md`: adopt fidelity tiering as plan-entry triage, name the eight research strategies (after a direct fetch confirms the full list), and commit to a model-floor declaration in the architecture preamble.

---

## Unfetched / open items

- **Full text of all three articles** — manual cookie-fetch (same workflow as `every.to/source-code/my-ai-had-already-fixed-…`) would resolve.
- **The six other planning strategies in article 2** — snippets only confirm reproduction-first and parallel research.
- **Article 1's full plan-vs-prototype decision framework.**
- **The `/modify-plugin` command spec from article 3.**
- **Cross-check against `Compound Engineering Camp` and `Opus 4.5 Collapsed Six Months…`** — likely contain overlapping detail.

## Suggested next actions

1. Add these three URLs to the next manual-fetch drain alongside the next round of every.to cookie-fetches.
2. Once full text arrives, fold the eight strategies and plan/prototype framework into `research/03-every-compound-engineering.md` §Workflows and cycles.
3. Consider whether `architectures/02-compound-atelier.md` should adopt **fidelity tiering** as an explicit plan-entry rule, replacing/refining Lightweight/Standard/Deep ceremony.
4. Add a **model-floor preamble** to all four candidate architectures in `architectures/00-comparison.md` — a one-line statement of which model class each architecture assumes.

---

## Sources

- [Stop Coding and Start Planning — Every](https://every.to/chain-of-thought/stop-coding-and-start-planning) (canonical alias https://every.to/source-code/stop-coding-and-start-planning) — Klaassen, Nov 6 2025. 403-gated; partial via search snippets.
- [Teach Your AI to Think Like a Senior Engineer — Every](https://every.to/chain-of-thought/teach-your-ai-to-think-like-a-senior-engineer) (canonical alias https://every.to/source-code/teach-your-ai-to-think-like-a-senior-engineer) — Klaassen. 403-gated; partial via search snippets and HN #45850475.
- [How Every Is Harnessing the World-changing Shift of Opus 4.5 — Every](https://every.to/chain-of-thought/how-every-is-harnessing-the-world-changing-shift-of-opus-4-5) — Klaassen / Every. 403-gated; partial via search snippets and Klaassen X posts (status/1993054059520217395, status/2019482153541915097).
- Related Every pieces referenced for cross-check: [Compound Engineering: How Every Codes With Agents](https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents), [Compound Engineering Guide](https://every.to/guides/compound-engineering), [Opus 4.5 Collapsed Six Months of Development Work Into One Week](https://every.to/chain-of-thought/opus-4-5-collapsed-six-months-of-development-work-into-one-week), [The Folder Is the Agent](https://every.to/source-code/the-folder-is-the-agent).
