# Session handoff — 2026-06-05 — discovery charter + next-steps; what comes next

> **Status:** the discovery framing and the plain-language plan are authored, reviewed, and (as of this
> handoff) merged to `main` via PR #247. **No factory code exists yet** — this session produced
> *orientation and plan*, not implementation. This doc tells the next session exactly where to pick up.
>
> **Read [the charter](../../factory-discovery-charter.md) first** for the feel; this handoff assumes
> its vocabulary (trust map, board of cards, drivers, toys, reduced models, self-builds, the two
> ledgers, fun-first).

---

## Where we are

This session reframed "what to do with the v4 factory" and recorded it durably. The key correction:
the factory is a **prototype for discovery**, built **co-implemented** with a *portfolio* of real
projects (agent-os is the first of several), and the work is selected from a **board of cards** shopped
by mood, with **fun as a first-class constraint**. An earlier draft's "march to a finished factory,
agent-os as the sole workload, batched production line" framing was wrong and has been superseded —
**the charter wins on framing where older artifacts disagree.**

**Important ordering reality:** the plain-language plan describes how to *exercise* the factory, written
*as if* the first 25 components ("safe self-build backbone") already exist. **They do not exist yet.**
The real near-term sequence is the three steps below.

---

## What this session authored (all on `main` after the PR #247 merge)

**Deliverables (plain-language, for the operator + future agents):**
- [`factory-discovery-charter.md`](../../factory-discovery-charter.md) — the essence: why/how/vocabulary/rules-of-the-game/fun-first. **The North Star.**
- [`next-steps-plain-english.md`](../../next-steps-plain-english.md) — the on-ramp + the board model + a starter board of example cards.
- [`methodology-and-formulas-plain-english.md`](../../methodology-and-formulas-plain-english.md) — concrete Gas City **formulas** (with an illustrative `build-component-v1`) + the co-implementation loop.

**The reasoning trail** (working corpus in [`_meta/next-steps/`](_meta/next-steps/)):
- [grounding brief + exemplar](_meta/next-steps/00-grounding-and-exemplar.md)
- three competing draft plans: [velocity](_meta/next-steps/plan-A-velocity.md), [de-risk](_meta/next-steps/plan-B-derisk.md), [yield](_meta/next-steps/plan-C-yield.md)
- [the unified plan](_meta/next-steps/10-unified-plan.md)
- the six-expert panel + fact-check + verdict in [`_meta/next-steps/panel/`](_meta/next-steps/panel/), summarized in [the verdict ledger](_meta/next-steps/panel/VERDICT.md)

**Navigation:** [`AGENT-ENTRY.md`](../../AGENT-ENTRY.md) §2 now points future agents at the charter
first, and at this handoff as the active one.

---

## The next three steps (in order) — for future sessions

### STEP 1 (next session) — Build the first set of cards (author the opening board)
Create the **board**: the play-menu of candidate exercises the operator will shop by mood. Concretely:
1. **Inventory the factory's capabilities** (the things that will exist once built) — start from
   [the implementer build order](implementation-dependencies.md) (the 7 products / 25 backbone
   components) and the [primitive/component specs](spec/). Set each one's starting **trust** (mostly
   🌑 Untouched, since nothing's built).
2. **Write ~8–12 opening cards** across the flavors defined in
   [the charter](../../factory-discovery-charter.md#the-vocabulary-use-these-terms-precisely): a couple
   of **smoke-toys**, several **reduced models** (e.g. "tiny event registry" → agent-os B12; "two-rule
   policy bundle" → B3), the first **real drivers** (agent-os B12 core; *and consider a non-Kubernetes
   project* to dodge the twin gap), a few **self-builds** (e.g. C07 glossary, C14 formula→DOT
   visualizer), and **≥1 invented-for-fun project**. Use the starter board in
   [the next-steps report](../../next-steps-plain-english.md#a-starter-board-examples--not-an-order-pick-by-mood)
   as the seed — flesh each into a full card (pressures / trust-of-target / size / **fun** /
   what-you'll-learn / dual-use payoff / prereqs).
3. **Output:** a `board.md` (suggested: `architectures/v4/board.md` or `BOARD.md` at root) — the living
   menu. Keep card bookkeeping a *byproduct*, never a chore (charter rule).
4. **Operator decisions to surface during Step 1:** which projects beyond agent-os are in the portfolio
   (the charter assumes agent-os is "first of several" but the others are unnamed); and whether to add a
   deliberately non-cluster project as an early real driver (it would dodge the twin gap).

### STEP 2 (a later session) — Create a plan to implement the first 25 components
Plan the build of the **safe self-build backbone** (the 25). Pointers:
- [The implementer build order](implementation-dependencies.md) — the 7 products, the dependency
  graph, the "Gas City conformance check is the literal first step" rule, the three rings
  (possible / runnable / safe).
- Honor the [rules of the game](../../factory-discovery-charter.md#the-rules-of-the-game-hard-won-respect-these-regardless-of-which-card-you-play):
  verify the substrate first (prevent vs detect), calibrate the judge before trusting it, lock the
  holdout vault, single-seat-serial reality, the spec-completion pass for real specs.
- The [panel verdict ledger](_meta/next-steps/panel/VERDICT.md) — the 8 amendments are constraints on
  any implementation plan (esp. AM-1 judge calibration, AM-2 holdout, AM-3 fence/D-30, AM-7 right-sizing).

### STEP 3 (later session[s]) — Execute that plan
Build the 25 components per the Step-2 plan. After they exist, the **board from Step 1 becomes live** —
you start actually *playing cards* (the discovery loop in the charter).

---

## Context to carry (mostly pointers — don't restate)
- **agent-os** is a read-only clone at `/tmp/agent-os` in this session's sandbox (ephemeral — re-clone
  `https://github.com/lago-morph/agent-os` next session if needed; out-of-scope for the GitHub MCP, so
  use `git clone` or jentic). It is a ~65-component K8s agent platform; each component ships a
  `spec-X.md` + `plan-X.md`. Infra-light B-components (B12, B3) are the natural first real drivers;
  Workstream-A components are twin-gated.
- **One operator, one AI seat, serial.** Plan for getting it right and enjoying it, not for speed.
- **The factory is unproven by construction** — say so in artifacts; the conformance check is move #1.

---

## In-flight / not done (so nothing is silently lost)
- The **first board has NOT been authored** — that's Step 1, the explicit next-session task.
- The **25-component implementation plan has NOT been written** — Step 2.
- **No factory code exists** — Step 3.
- PR #247 is **merged**; its branch (`claude/gas-city-roadmap-plan-HWuGh`) is deleted post-merge. Any
  new work needs a fresh branch + PR.

*This handoff is the binding pickup brief for the next session. Update AGENT-ENTRY §2's active-handoff
pointer when the next handoff is written.*
