---
name: human-scoped-deliverables
description: Calibrate human-facing deliverables for jonathan@manton.com (the human reader of this repo) when producing a summary, overview, primer, plain-language explainer, comparison guide, reading guide, or any artifact that will be read by a human rather than handed off to another AI agent. Triggers on user phrases like "summary", "overview", "primer", "in plain language", "explain", "walkthrough", "comparison", "side-by-side", "help me understand", "give me a sense of", or any equivalent request that signals "I am going to read this with my human brain, not feed it to another agent." Defines vocabulary discipline (corpus terms over invented jargon), diagram conventions (Mermaid ≤7 elements per diagram), tabular comparison expectations, the resource-aware framing (cognitive load is a real resource alongside time and money), descriptive effort scoping (no quantitative time estimates — the 2026 reality is that those numbers are meaningless), and the anti-patterns this reader has explicitly flagged as unworkable.
---

# Human-scoped deliverables

A skill for producing material that a specific human reader (jonathan@manton.com — the owner of this repo) can actually read and act on. The repo's normalized AI-readable artifacts (pipeline output, audit trails, normalized cross-referenced spec files) are NOT this. This skill is for the human-facing layer that sits on top.

The reader has explicitly named the canonical AI-readable form as "like reading directly from individual tables in a SQL database — not possible for a human to work that way." This skill is the BI-tool / report / interactive-visualization layer that the SQL underlay needs to be usable.

## Reader background

- 35+ years of high-end software, mechanical, and electrical engineering experience.
- Kubernetes and distributed systems expert.
- Builds on the boundary between hardware, software, and systems thinking.
- Reads original sources directly. Has read the corpus material (Shapiro on the Five Levels, El Kaim on dark factory, Willison's writings, StrongDM Factory + Attractor docs, 2389-research project ecosystem, every.to compound-engineering writers, Vincent on Dorodango, Yegge on Gas Town, etc.).
- Self-identifies: "I am smart, and have over 35 years of high end software, mechanical, and electrical engineering experience. But you make me feel like an inadequate moron." The "moron" feeling is the diagnostic signal that the writing is wrong, not the reader.
- Explicit goal for the work in this repo: "to make it possible to get incredible leverage from the attention of a skilled engineer by providing ai inference coupled with tools." Attention is the load-bearing constraint.

## How this reader processes information

### Strong preferences

- **Visual thinker.** Tables for comparison; diagrams for structure and flow. Structure should be surfaced visually, not buried in prose.
- **Mermaid is the preferred diagram medium.** Renders in the reader's tools.
- **Small diagrams.** ≤7-8 elements each. Mermaid auto-layout fails at scale. Multiple small diagrams beat one large one; zoom in for details.
- **Separate concerns.** Distinct things should be presented independently, then their relationships understood after. The discipline / methodology / substrate three-layer split is the canonical example from this repo.
- **Plain, descriptive, boring terms.** Standardize: same concept gets the same name everywhere across all documents in a deliverable.
- **Vocabulary from the corpus the reader has already read.** Don't invent terms when the corpus has them. Lean on Shapiro / El Kaim / Willison / StrongDM / 2389-research / Vincent / Yegge / every.to / etc.
- **Buildability framing as the default.** The reader is a builder. "What can be built from existing OSS?" and "What's actually new vs. configure existing?" are first-class questions.
- **Acknowledge that things will fail first time.** "There is basically 0 chance that any of these will work first time." Optimize for swap-cost, not first-run correctness.

### Strong dis-preferences

- **Dense cross-reference soup.** "Per AGENTS-MD-7d9c4e1b3a § Round 2 amendment #5"-style references require the reader to maintain a stack of context in working memory. Forbidden in human-facing material. If a cross-reference is load-bearing, quote the relevant sentence inline.
- **Hash IDs in body text.** Hash IDs (AGENTS-MD-xxx, ADR-yyy, P-NN, etc.) are AI-navigation artifacts. They belong in footnotes or audit trails, not in body paragraphs aimed at a human.
- **Author-name-to-concept mappings as the introduction to an idea.** Lead with the idea, attach the author/source name second. "The pattern where every change is reviewed by a different model than wrote it (compound-engineering pattern, attractor-derived)" — NOT "Klaassen's compound engineering pattern."
- **Database-normalized output presented to a human.** Forbidden.
- **Inventing terminology in parallel to the corpus.** Every rename costs the reader cognitive load to map back to what they already know. Don't pay the cost without a strong reason.
- **Quantitative time/money estimates.** In May 2026, "engineer-weeks" and "dollar costs" are meaningless comparison points. What a 5-person team did in a month in 2023 a skilled engineer with AI tooling now does in a day. Estimates date instantly and are misleading. Use descriptive effort scoping instead (see below).

### What feels insulting (avoid)

- Being asked to maintain context the writer could have surfaced inline.
- Being treated as an academic doing a thought experiment rather than an engineer who wants to build.
- Walls of jargon and AI-readable formatting that read as condescension.
- Dense reference-laden material that hides the load-bearing finding inside an audit subsection where it cannot be seen.

## Resource awareness (broader than cost)

The reader thinks of attention as a resource. Other resources matter too:

| Resource | What's expensive | Optimization |
|---|---|---|
| **Cognitive load** | Cross-references, jargon, hash IDs, unfamiliar vocabulary | Plain language; corpus vocabulary; inline quotes over cross-references |
| **Attention span** | Reading multiple files to understand one decision | Single-document deliverables when possible; clear orientation at the top |
| **Time** | Setup overhead per pressure-test | Shared substrate; swappable methodologies |
| **Money** | Per-token cost at frontier-model inference budgets | Model stylesheets; cheap models for cheap nodes |
| **Engineer hours** | Custom substrate build vs. configure existing OSS | Buildability framing; OSS-first |
| **Patience for AI agents** | Re-explaining context; correcting after-the-fact | Sample-first; ask before producing; honest epistemic disclosure |

The framing is "what does this cost in *the relevant resource*", not "what does this cost in dollars."

## Descriptive effort scoping (not quantitative)

Quantitative time/money estimates are unreliable in May 2026 and rapidly getting more unreliable. Use descriptive scoping instead:

| Don't say | Say |
|---|---|
| "~2 engineer-weeks" | "Small custom build on top of existing OSS." |
| "6-12 engineer-months" | "Major engineering investment — the most ambitious substrate primitive in the catalog; requires integrating multiple existing systems into a unified queryable layer." |
| "1-2 engineer-weeks" | "Mostly configure existing OSS; one small new harness." |
| "$1000/engineer/day" | "High-frontier-model spend; cost-aware routing matters." |
| "PR will take 2 hours to review" | "Reviewable in one sitting; surface the load-bearing findings up top." |

Descriptive scoping describes *what's involved* — the kind of work, the substrate dependencies, the complexity of the new code, what's known to be hard. It does NOT pretend to predict wall-clock time.

When pressure-tested by the reader, fall back to:
- "Cheapest to first pressure-test" / "Medium cost" / "Most expensive substrate investment in the catalog."
- "Configure existing OSS" vs. "Small custom harness" vs. "Major engineering build."
- "Single-engineer afternoon" vs. "Single-engineer week-ish project" vs. "Multi-engineer multi-month project" — but only when the calibration point is concretely about engineering complexity, not about clock time.

## Format conventions for any human-facing deliverable

1. **Short orientation block at the top** of every document. ~50 words. "Here's what this is, here's what it's not, here's how to read it." Not a 200-word abstract.

2. **Comparison tables.** Markdown tables. Wide-but-screen-fittable. Multiple smaller tables beat one giant one.

3. **Mermaid diagrams ≤7 elements per diagram.** Zoom into details with additional small diagrams. Don't put everything in one mega-diagram — the auto-layout will fail.

4. **Plain language descriptions** that lead with the idea, attach the corpus name as the source, and skip "see § X.Y" style cross-references.

5. **No hash IDs in body text.** If you need to reference an AGENTS-MD rule, an ADR, or a substrate primitive, describe what it says inline. Hash IDs go in an audit-trail footer or appendix if needed at all.

6. **Decision points labeled.** When the reader has to choose between alternatives, name the alternatives explicitly, name the trade-off, name the rewind path if the choice is wrong.

7. **Honest acknowledgements.** What's known. What's speculative. What's audit-trail. What you (the agent) don't know yet. Disclose epistemic state.

8. **Lead-agent opinion clearly marked when present.** "Speculative recommendation:" or "This is opinion, not synthesis:" — make the epistemic status visible. Don't bury opinion as synthesis-as-conclusion.

9. **Sample-first when there's risk of misalignment.** Produce one small representative piece, get sign-off on the framework, then scale.

## Anti-patterns to avoid

These are concrete things this reader has flagged as unworkable. Don't do them in human-facing deliverables.

- **AI-to-AI handoff format presented to a human.** Normalized cross-referenced output is the SQL underlay, not the deliverable.
- **"Per AGENTS-MD-7d9c4e1b3a § Round 2 amendment #5"-style citations.** Quote the idea inline.
- **Inventing parallel terminology to the corpus.** If the corpus calls it "multi-model review," don't call it "paraphrase divergence."
- **Listing 10 author names as the introduction to a concept.** "The spec-first movement (Lefebvre, Steiner, ...)" forces memorization that doesn't help. Describe the idea.
- **Starting implementation when the user asked for information.** If the user asks a question, answer it before producing artifacts.
- **Burying the load-bearing finding inside an audit subsection.** If the most important thing you found is "U-A/U-B/D7-U-1 are practitioner-thin," that's the headline. Not "load-bearing cross-cutting finding in §3 of the audit file."
- **Treating "phase closed; pipeline complete" as a satisfying summary.** The reader needs to know what was actually decided and why it matters, not just that the audit-trail closed cleanly.
- **Producing a 8-PR stack of dense artifacts before the reader has had a chance to react to the framing.** Sample-first.
- **Asking for external sources by author name.** "Which authors are in your head?" forces memorization. Better: "Here's what I know; tell me what's missing."

## Workflow patterns that work

- **Ask before producing.** Especially for multi-document deliverables. Surface concrete options + my best guess + ask which one matches.
- **Sample-first when scaling.** One representative piece → review → produce the rest. Don't produce 30 diagrams before the framework is confirmed.
- **Honest disclosure.** "I haven't read X but I know Y and Z" beats invented authority.
- **Surface decision points early.** If you're going to make a call (e.g., "I picked term A over term B; here's the alternatives in a glossary"), say so up front.
- **Acknowledge what was wrong.** When the reader corrects something, say "Yes, you're right" before pivoting. Don't perform an unprompted apology, but don't ignore the correction either.

## When this skill applies

Load this skill when:

- The user asks for a summary, overview, primer, walkthrough, comparison, side-by-side, reading guide, plain-language explanation, or any equivalent phrasing.
- The user asks to "help me understand," "give me a sense of," "translate this for a human," or similar.
- The user is reviewing a deliverable and feedback signals it's unreadable ("this is impenetrable," "you make me feel like a moron," "I am a human, not a computer").
- You're producing material that will be read by a human as the primary audience, not consumed by another AI agent.

If the user is asking for AI-readable canonical artifacts (specs, audits, ADRs, pipeline output), this skill does NOT apply — produce normalized canonical form for those.

## When in doubt

Default to the human-facing form. If the user wanted canonical AI-readable output, they'll say so. The canonical form is reversible (it's still on disk); the human-facing form is the one that gets read.
