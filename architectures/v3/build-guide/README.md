# Build guide — v3 candidates in plain English

This directory translates the v3 synthesis output into something a human engineer can actually read in one sitting. The pipeline output (the per-candidate specs at `architectures/v3/specs/`, the lean-eval briefs at `architectures/v3/lean-evals/`, the back-fill notes, the audits) is structurally normalized for an AI agent re-entering cold. This guide is for a person deciding what to build.

## Read order

1. **[`01-vocabulary.md`](01-vocabulary.md)** — corpus terms used in this guide + translation table from v3-pipeline-jargon to plain names. Read this first. Everything else uses this vocabulary.
2. **[`02-paradigm.md`](02-paradigm.md)** — where the 10 candidates sit on the "Five Levels" axis (Shapiro) and which of the "12 principles" (El Kaim's synthesis) they each commit to. This is the discipline layer.
3. **[`03-substrate.md`](03-substrate.md)** — the existing open-source landscape and what each piece does. Where each candidate's substrate is already a solved problem (most of it is) vs. where you'd actually have to build something.
4. **[`04-candidates.md`](04-candidates.md)** — the 10 candidates side-by-side. For each: the distinctive bet in one sentence, methodology shape, substrate composition (which OSS in each slot), what's custom, rough buildability estimate, what could kill it.

## What this guide is NOT

It is not a per-candidate methodology diagram or a per-candidate spec walkthrough. Those are coming in items 5-6 (still pending). This guide is the **framework** for reading those diagrams when they arrive — and may be enough on its own to make a build decision.

It also does not pre-judge which candidate(s) to ship. The final recommendation is a separate artifact.

## Underlying sources

This guide leans heavily on three documents from `reference-only/`:

- **Shapiro, "The Five Levels"** (`reference-only/99b58be420/`) — the maturity model.
- **El Kaim, "The Dark Factory"** (`reference-only/f675af7d98/`) — the full paradigm synthesis with the 12 principles and the substrate-component naming convention.
- **Willison, "How StrongDM's AI team build serious software"** (`reference-only/303c8ff4e8/`) — outside observation of the StrongDM team's actual practice.

Plus the project READMEs for Kilroy, Fabro, Gas City, OpenHands, Overstory.

When this guide says "the corpus says X," it means one of these (or a closely-related source in the same canon). When it says "the v3 pipeline says Y," it means the candidate-registry, spec files, or lean-eval briefs under `architectures/v3/`.
