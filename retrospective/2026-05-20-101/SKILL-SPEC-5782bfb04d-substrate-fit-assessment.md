# Spec: `substrate-fit-assessment`

- **ID**: SKILL-SPEC-5782bfb04d
- **Source retrospective**: ../2026-05-20-101.md

## Intent

When the user asks "can X be the runtime for Y?" or "would Y work as a substrate for X?" — produce a structured feasibility assessment that maps primitives, walks deployment shape, identifies gaps honestly, and proposes a middle-path incremental adoption. Replaces the failure mode of returning either a confident "yes" or a hedged "maybe" without showing the work. This session produced three instances of the assessment shape — Dark Factory on Gas City + Compound Engineering on Gas City + this repo on Gas City — and the user's response on all three was to treat the structured output as decision-ready, not as a starting point to iterate against.

## Trigger

### Direct triggers

- "Assess the feasibility of running X on Y."
- "Could we use Y as the runtime / substrate / execution layer for X?"
- "Would X be a good substrate for Y?"
- "Map X onto Y."
- "Is Y mature enough to host X?"
- "What would it take to deploy X on Y?"

### Proactive triggers

Offer the skill when:

- A research session has just deeply analyzed a candidate substrate (a tool / SDK / framework with named primitives) and a candidate methodology (a discipline with named primitives, e.g., a research-report subject) — the natural next question is "do they fit together?"
- The user is sizing up candidate execution substrates as part of a larger architecture decision.
- A synthesis report (corpus pattern `research/NN-<slug>.md`) just landed that ties a substrate to a methodology, and the natural follow-up is "what about applying that mapping to our own repo?"

### Negative triggers — do NOT use the skill for

- Generic "would X work for Y?" where neither side has explicit named primitives (the structured mapping needs both sides to be analyzable in primitive terms).
- "Is X better than Z?" — that is comparative methodology evaluation, not substrate-fit. Use a comparison-matrix shape instead.

## Inputs

- **The substrate**: a tool / SDK / framework whose primitives are documented. Typical sources: a deep-dive followup in `research/followup/`, a vendor README, an architecture doc.
- **The workload**: a methodology, a corpus, a repo's existing processes, or a specific deliverable. Sources: a research report (`research/NN-<slug>.md`), a `PLAN.md`, the user's own description.
- **(Optional) The user's adoption tolerance**: are they sizing up the substrate as a long-lived runtime, or as a one-shot tool for a specific deliverable? Default to producing both framings if not specified.

## Outputs

- **A structured assessment** written to the chat (or to a new `research/NN-<slug>.md` if the user asks for a file). The assessment is a single document, not a series of bullet points, and follows the canonical section structure described under Workflow.
- **No file commits by default.** If the assessment is rich enough to merit corpus inclusion, ask the user whether to commit it. The substrate-fit shape is normally a recommendation-grade artifact, not a corpus-grade artifact.

## Workflow

1. **Establish both inventories.** Read or recall the primitive set on both sides. The substrate primitives should be named and (ideally) documented as a layered or numbered architecture (e.g., Gas City's "Nine Concepts"). The workload primitives should be named in the methodology or in the repo's existing PLAN.md.
2. **Write the verdict first.** One sentence: highly feasible / feasible with caveats / awkward / infeasible. Two-to-three-sentence elaboration. The verdict is the headline; the reader should be able to stop after the verdict if they choose.
3. **Decompose the workload.** Walk the actual pending work — not the abstract methodology — into 3–6 buckets with parallelism + decision-vs-build labels. This is the load-bearing step: it surfaces which parts of the workload benefit from the substrate's parallel-orchestration features vs. which parts are sequential decision work the substrate cannot help with.
4. **Build the primitive-mapping table.** Rows: substrate primitives. Columns: which workload primitive it implements, fit grade (✅ direct / 🟡 needs convention / ❌ engine-level missing), and a one-line rationale. Aim for one row per substrate primitive, not one row per workload primitive — the substrate is the spine.
5. **Enumerate what's awkward.** Three to five honest gaps. Each gap names a specific substrate feature missing for a specific methodology requirement, with a sentence on how it could be bridged (Order-driven extension, pack-level lint, methodology-level discipline).
6. **Write the concrete deployment sketch.** Show enough config-file content (`city.toml` / `pack.toml` / formula TOML / order TOML) that the reader can mentally execute the deployment. Cite real primitive names from the substrate.
7. **State the cost-benefit explicitly.** Costs (install dependencies, migration work, ongoing maintenance) and benefits (named capabilities the workload gains). Be specific about scale-of-effort — "a half-day for a polecat" or "1-3 PRs/day cadence."
8. **Propose a middle path.** Especially important when the substrate is heavyweight. Identify the single highest-leverage subset of the substrate that captures most of the benefit at a fraction of the cost. The middle path is often what the user actually wants.
9. **Give a recommendation.** Specific enough to act on: "Adopt Beads only" / "Build the full pack" / "Don't deploy; the workload doesn't benefit."

## Concrete examples

### Example 1: Dark Factory on Gas City

(From PR #101 §4 of `research/38-gas-systems-substrate.md`.) Inputs: the Gas City deep-dive (`research/followup/13-gas-city-deep-dive.md`) and the Dark Factory methodology (`research/07-dark-factory.md`). Output: a `darkfactory` pack on Gas City with rigs for `product` / `scenarios` / DTU services; scenarios isolated by `prefix = "scn-"` in `routes.jsonl`; codergen + judge + healer pack agents; an Attractor-shaped convergence formula. Three honest gaps named (no first-class LLM-as-judge primitive, no DOT pipeline parser, no context-fidelity slider). Cost-benefit: methodology-supplied judge scaffolding has to be built; substrate provides convergence loop + event bus + bead store + parallel fan-out. Recommendation: feasible; the three gaps are bridgeable as pack-level engineering work, not substrate-level blockers.

### Example 2: Running this repo's research-synthesis pipeline as a Gas City rig

(From the Q&A phase of session 2026-05-20.) Inputs: the Gas City deep-dive plus `research/PLAN.md` (538 lines) and `research-plan.md`. Workload decomposed into 5 buckets: cross-corpus sweeps (A); three §3.2 curated edits (B); F36/F37 numbering collision (C); synthesis collapse + v3 architecture (D); retro + ADR + housekeeping (E); deferred stage-5 drains (F). What maps cleanly: Mayor / Polecat / Convoy / Beads / Orders. What's awkward: Refinery (PR cadence too low to benefit); Wasteland (single-org); the unified-synthesis bucket D is genuinely sequential and doesn't parallelize. Middle-path proposal: adopt Beads only (without the rest of the Gastown pack), to capture the largest single benefit (state durability for `PLAN.md`'s stale tables) without paying full substrate-adoption cost. Recommendation: phased — Beads first; rest of the substrate as a future option.

## Anti-patterns

- **Confident "yes" without showing the work.** PR #101's §4 + §5 deployment sketches are what make the mapping verifiable; without them, "Gas City could host the Dark Factory" is a slogan, not an assessment. Always produce the concrete deployment sketch.
- **Skipping the workload decomposition.** Jumping straight to "X maps to Y" hides the failure mode where the workload is mostly sequential decision work and the substrate's parallelism doesn't help. The 5-bucket decomposition in Example 2 surfaced this directly for the unified-synthesis bucket.
- **Hiding the gaps.** Every assessment has gaps; surfacing 3–5 honest ones is what makes the assessment trustworthy. Hiding gaps to claim "feasibility" produces an artifact the user has to discount.
- **One-size-fits-all middle path.** The middle path should be specific to the workload — "adopt Beads only" works for this repo because PLAN.md's stale-table problem is the largest pain point; a different workload would have a different highest-leverage subset.
- **Treating "feasible" as a binary.** Use the verdict scale (highly feasible / feasible with caveats / awkward / infeasible). "Highly feasible but the cost/benefit pivots on which subset of the substrate you actually need" is the kind of nuance the structured output is for.

## Acceptance criteria

- [ ] The assessment opens with a verdict the reader can act on after reading just one paragraph.
- [ ] The workload is decomposed into 3–6 buckets with parallelism and decision-vs-build labels.
- [ ] The primitive-mapping table has one row per substrate primitive (not per workload primitive).
- [ ] At least three honest gaps are surfaced, each with a bridging mechanism.
- [ ] The deployment sketch cites real primitive names from the substrate (not generic placeholders).
- [ ] A middle-path / incremental-adoption option is proposed.
- [ ] The recommendation is specific enough to act on (specifies *what subset* to adopt, not just "yes" or "no").

## Files this skill creates / modifies

- (none by default) — the assessment is normally a chat-output artifact. If the user asks for a committed file, follow the corpus pattern of `research/NN-<slug>-assessment.md` plus an INDEX row.
