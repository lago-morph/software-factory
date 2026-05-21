# Research → Action Plan

How we get from "lots of research" to "a running lights-out software factory for greenfield applications." This is a recommendation, not a settled plan.

## The three-layer pipeline

The repo is already structured as a funnel; the funnel just isn't closed yet.

1. **Reports (provenance layer)** — files under `research/` and `research/followup/`. These stay as individual documents forever. Their job is to anchor every claim to a primary source so future-us can audit any decision. We do not act off these directly.
2. **Synthesis (condensation layer)** — files under `research/synthesis/`. Ten rounds of material now sit between Round 2 and the present with no unified synthesis covering them. This is a real gap. The failure-mode catalog is fragmented across reports and the two existing syntheses.
3. **Architectures (action layer)** — files under `architectures/`. This is where we commit to *what to build*. v2 already names a single recommended path: **Compound Atelier as baseline**, build shared infrastructure first (§7.4), selective borrows from Refinery / Foundry / Tournament. But v2 is anchored only on Round-1 material — it has not absorbed any of the later rounds' findings. `research/PLAN.md` §3.2 carries this as an open task.

**Failure-mode footprint across the corpus (no counts; pointers only).** F1–F20 live in `research/synthesis/00-synthesis.md`; F21–F33 in `research/synthesis/13-round-2-synthesis.md`; F34 in `research/followup/12-brier-pace-layers.md`; F35 in `research/24-el-kaim-book-product-line-variability.md`; F40–F49 are distributed across reports 28, 30, 31, 32, 33, 34, 36, and 37; the F36–F39 collision (reports 25 and 26) is unresolved (see `research/PLAN.md` §3.6).

## What "enough research" should trigger

When we decide to stop fetching, the condensation flow is:

1. **Cut a single unified synthesis.** Either a v3 of `research/synthesis/00-synthesis.md` that supersedes 13 + folds in followups, or a new file at `research/synthesis/final.md`. One canonical failure-mode catalog (F1 through F49 plus the unresolved F36/F37 collision), one consensus list, one tensions list, one open-questions list. The two-synthesis-plus-scattered-followups state is a hazard now; it will be a worse hazard six months from now.
2. **Revise the architectures to v3** against that unified synthesis. The four specs probably do not all need to survive. For a *lights-out greenfield* mandate specifically, Tournament and Foundry are unlikely fits. v3 likely collapses to **one chosen architecture** — probably Atelier + Refinery's layered-spec discipline on top, since greenfield means the spec is the load-bearing artifact and Atelier alone assumes an existing issue queue — plus an explicit "rejected alternatives" appendix.
3. **Promote the chosen path into ADRs and a build plan.** The architecture doc says *what* the factory looks like; we will need ADRs for the binding choices (substrate, sandbox model, scenario storage, knowledge format, manager-loop primitive) and a sequencing plan for §7.4's shared infrastructure.
4. **Run the §6 lean evaluation first** — the 1-day manual run of the discipline before building any orchestration. Do not skip this. It is the cheapest way to learn the methodology is wrong.

## What stays as individual documents vs gets folded

- **Reports + followups: stay individual.** They are evidence; they age but do not expire.
- **Failure modes: get consolidated** into the unified synthesis. Right now they are scattered across the two existing syntheses, individual followup reports, and many of the round-9 and round-10 numbered reports — that should hurt.
- **Architecture specs: probably consolidate** down from four to one (or one-plus-extensions) once we commit. The other three become "alternatives considered" in an ADR.
- **`spec-driven-ai-dev.md`**: pending update per `research/PLAN.md` §3.2. Once v3 architectures land, this should be rewritten as the methodology document for the chosen architecture, not as a fifth competing view.

## One specific risk for the greenfield mandate

The four architectures were designed against a "general execution environment, solo→small team" brief. *Lights-out greenfield* is a different shape — no existing issue queue, no codebase to learn from, no prior scenarios. Atelier's strongest assets (the queue, the workpad, accumulated `docs/solutions/`) do not exist on day one. The cold-start problem for a greenfield factory is its own design question and is not directly addressed in the current comparison. Worth a dedicated synthesis section before v3 of the architectures.

Rounds 9–11 added an RE/SE-methodology thread (reports 25/26) and a governance thread (followup/10 + reports 30/31) that weren't on the radar when this doc was first written; both should feed the cold-start treatment.

## Short version

The architecture doc is where this lands. The reports stay as evidence; the synthesis collapses into one canonical doc; the architectures collapse into one chosen path + alternatives-considered; ADRs and a sequencing plan come out the bottom; then we run the §6 lean evaluation and start building shared infrastructure.
