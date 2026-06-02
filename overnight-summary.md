# Overnight run — morning summary (2026-06-01)

## TL;DR

- I took the **safe self-build spine** — the smallest set of pieces that lets the factory safely build a piece of *itself* — from "we know what each piece is" to "an engineer could start building it." That's all twenty-five pieces, grouped into the seven products you build them as.
- I did the **two you wanted to start on first, first and deepest**: adopting and configuring Gas City (one install that brings up eleven of the pieces), and standing up Claude Code under your Max subscription as the worker. Both come with a concrete, copy-paste **install-and-configure runbook** and, for Gas City, a **verify-before-you-build checklist**.
- Everything landed as a **stack of pull requests you merge bottom-to-top** (the order is below). Each one was checked by an independent reviewer whose only job was to attack the seams between pieces — and that paid off: they caught several mistakes that would have silently broken the build, including one that would have made the quality score permanently read as zero.
- **One thing genuinely needs your decision** before the factory is ever allowed to build the first piece of itself: *how we decide that first self-built piece is good enough to keep.* I've written up a recommendation and the argument around it; it just needs your sign-off.
- **One thing is still owed and can't be done here**: actually running Gas City to confirm it *blocks* (not just notices) an agent reaching outside its sandbox. That needs a machine with Docker, which this environment doesn't have. Until it's run, the factory stays human-supervised — which is the safe default we already agreed on.

## The one decision I need from you

When the factory builds a component for itself, a held-out test set is run against it and a judge scores how well it met the spec — producing a spread of scores. **The question is which features of that spread are allowed to say "good enough, ship it"** for the very first self-build.

- The simplest answer ("the average is high enough") lets a piece with a consistently bad tail sneak through.
- My recommendation, after a panel of reviewers and a second round of critique, is a **three-part test**: the bottom of the spread must clear a floor, the average must clear a floor, **and** the spread must not be too wide (so erratic, all-over-the-place behaviour is caught) — plus two guards: enough test cases to be meaningful, and a human spot-check that the judge itself is trustworthy before we believe its scores. And one piece the first draft was missing entirely: **after** the new component is slotted into the factory, the factory's own test suite must still pass — i.e. "did we just break ourselves?"
- The actual pass/fail *numbers* stay yours to set. I'm only asking you to approve the **shape** of the test, because it's the gate on the first time the factory modifies itself, and that's a judgment call, not a mechanical one.

The full write-up is the decision brief listed in the table below. Nothing is blocked in the meantime — the specs carry a sensible default with this question clearly flagged.

## What got built (in plain terms)

| Product | What it is | What I did |
|---|---|---|
| Gas City | The off-the-shelf engine the whole factory runs on; one install turns on eleven pieces | Deepened the eight pieces that needed it + wrote the install/config runbook + the verify-before-build checklist, all grounded in the working prototype |
| Claude Code under Max | The worker the engine drives to actually do the building | Deepened the worker loop + the cost/model routing policy + wrote the auth/session setup runbook |
| Spec intake | The written spec a build runs against, and how it becomes the prompt the worker sees | Deepened both; settled that the spec *is* the prompt file |
| Evaluation tier | The heart of the whole thing: run a held-out test, judge the result, turn judgments into a score | Deepened all four pieces; settled how the trajectory and score records flow between them |
| The fence | The safety boundary that must be up before the factory ever runs unsupervised | Deepened the blast-radius typing and the holdout-integrity checks |
| Bootstrap | The actual "factory builds a piece of itself, a human reviews it, it deploys" loop and its go/no-go gate | Deepened all three; this is where the go/no-go decision above lives |

A note on discipline: a reviewer whose only job was to check we hadn't over-built confirmed the depth stayed honest — the new work *configures and wraps* the tools we already adopted rather than re-inventing them, and two pieces that could have crept into scope were deliberately kept out.

## Suggested merge order

Merge bottom-to-top; each builds on the one before it.

1. **#237** — run setup (the scope I committed to + the format every spec follows)
2. **#238** — Gas City (the install + config + verify checklist) — *your first implementation target*
3. **#239** — Claude Code / Max (the worker + its setup) — *your second*
4. **#240** — Spec intake
5. **#241** — Evaluation tier
6. **#242** — The fence + Bootstrap (the safety + self-build apex)
7. **(this PR)** — this summary, the panel verdict, the decision brief, and the cross-product fixes

All seven are independent-to-read but should land in this order so the stack stays consistent.

## Pull requests opened (stack order)

| PR | Branch | What it delivers | Base |
|---|---|---|---|
| #237 | `…-OQ8g4` | Scope envelope + Sweep-2 dispatch contract | `main` |
| #238 | `…-gascity` | Gas City: 8 specs + config anchor + conformance check + runbook | #237 |
| #239 | `…-claudemax` | Claude Code/Max: C28 + C29 + Max runbook | #238 |
| #240 | `…-specintake` | Spec intake: C08 + C09 | #239 |
| #241 | `…-evaltier` | Evaluation tier: C30 + C31 + C32 + C33 | #240 |
| #242 | `…-fence-bootstrap` | Fence + Bootstrap: C34/C43/C51/C52/C53 + C20 refine | #241 |
| this | `…-summary` | Summary + panel verdict + decision brief + integration fixes | #242 |

## Decision briefs written

| Brief | Question | Rounds | Status |
|---|---|---|---|
| `auto-002` | The first-self-build go/no-go rule shape | 2 (opus panel = R1; 3 adversaries = R2, all accept-with-amendments) | **Needs your sign-off** — recommendation: the three-part test + post-deploy check above |

## Decisions I made and recorded (so they don't get re-litigated)

These were cross-piece consistency calls — naming, ownership, which-piece-owns-what — that I settled and propagated so the parallel work didn't drift. They're in the decision ledger (D-31 … D-41). Highlights in plain terms: a city runs *many* sandboxes not one (your input); the evaluation tier scores its own run log rather than pulling in the heavier trajectory database (kept two pieces out of scope); the judge runs in its own sandbox the worker can't see; and the records the self-build loop writes were reconciled so a "finished build" query actually finds finished builds.

## Morning-review items

1. **The go/no-go rule shape** (decision brief `auto-002`) — described above. Recommendation ready; needs your approval + the threshold numbers.
2. **The owed reality-check** — run Gas City end-to-end on a Docker-capable machine to confirm it *blocks* out-of-bounds access (not just logs it). Its outcome decides whether we additionally build a small blocking watcher. Until then, unsupervised operation stays off; supervised, per-step operation is fine.

## What I deliberately did NOT do

- **I did not design the blocking watcher.** We agreed its design waits until the reality-check above shows we actually need it. I kept every safety spec honest about this: they require blocking, mark it unverified, and hold a human-supervised posture in the meantime.
- **I did not run the reality-check** — no Docker here. It's owed, and flagged everywhere it matters.
- **I did not build the other thirty-two pieces** — only the spine, plus anything a spine piece strictly needed. Two tempting pull-ins (the trajectory database and the molecule runtime) were deliberately kept out, with the reasons recorded.
- **I did not relitigate anything already decided** (the prevent-gate, the earlier operator decisions).

## Rewind points

| Revert | Undoes |
|---|---|
| the `…-summary` PR | this summary + the panel + the brief + the 4 cross-product fixes |
| the `…-fence-bootstrap` PR | the fence + bootstrap + the bead-schema build-state refine |
| the `…-evaltier` PR | the evaluation tier |
| the `…-specintake` PR | spec intake |
| the `…-claudemax` PR | Claude Code/Max |
| the `…-gascity` PR | the entire Gas City layer |
| the `…-OQ8g4` PR | the whole run (back to before it began) |

Each spec was *deepened in place*, so reverting a PR drops the Sweep-2 depth and leaves the earlier foundation intact in `main`.

## Session metadata

- **Branch chain (bottom→top):** `main` → `…-OQ8g4` → `…-gascity` → `…-claudemax` → `…-specintake` → `…-evaltier` → `…-fence-bootstrap` → `…-summary`.
- **Subagents:** ~40+ across grounding, builders (one per component), integrators, per-product seam adversaries, a 5-persona opus panel, and a 2-round decision-brief review.
- **Method:** every spec written to disk by a subagent returning a short receipt; the lead held all git and committed every wave; real (never simulated) adversarial reviewers; cross-piece conflicts recorded as numbered ledger decisions and propagated.
