# Board 1 — the opening play menu (a shakedown cruise)

**What this is.** The [charter](factory-discovery-charter.md) says we shop a **board of cards** by mood
and play one. This is the **first board**. Read the [charter](factory-discovery-charter.md) for the
*feel* (trust map, drivers, toys, reduced models, the two ledgers, fun-first), the
[next-steps report](next-steps-plain-english.md) for the on-ramp, and the
[methodology companion](methodology-and-formulas-plain-english.md) for what a *formula* is. This file is
the menu itself — the living thing you actually shop.

> **Bookkeeping is a byproduct, never a chore** (charter rule). If keeping this board ever feels like
> filling a spreadsheet, simplify it away. Trust levels and the two ledgers fall out of *playing*; they
> are not homework.

---

## The theme of Board 1: does the backbone even hang together?

This board has **one governing purpose**: find out whether the **first 25 components** (the
[safe self-build backbone](architectures/v4/implementation-dependencies.md#the-backbone-the-most-aggressive-path-to-safe-self-building))
actually *work together* once they exist. It is a **shakedown cruise**, not a production run. Three
deliberate constraints make it safe and simple — *it is unwise to do complicated things the first time
you use something this experimental*:

1. **The only real drivers are factory self-builds.** The "real thing we want to keep" that each driver
   card produces is one of the **factory's own next components** (a dogfood self-build). We are building
   *the factory*, by the factory, in the gentlest possible way.
2. **agent-os appears only as reduced-fidelity models.** agent-os is the eventual product, but on Board 1
   it shows up *only* as **reduced models** — shrunk-down stand-ins used to stress a capability in
   isolation. No real, twin-gated agent-os component gets built yet. (Why: agent-os is a Kubernetes
   platform; safely building its real components needs digital twins, C44, which the backbone defers.)
3. **No other portfolio projects.** The portfolio stays frozen at agent-os-as-test-target for now.

The backbone's twenty-five are: **C01–C05, C08, C09, C17, C18, C19, C20, C23, C28, C29, C30–C34, C41,
C42, C43, C51, C52, C53** (the three rings — *possible / runnable / safe* — are in
[the build order](architectures/v4/implementation-dependencies.md#three-rings-possible-runnable-safe)).
Every card below names which of those it leans on, so the board *collectively* is a coverage map of the
shakedown.

---

## Before you play: the one ordered bit (the on-ramp)

Everything on the board is free choice **except** three moves that genuinely come first, because until
you trust the factory's *instruments* you can't trust the result of any card. Full version in
[next-steps Part 1](next-steps-plain-english.md#part-1--the-one-ordered-bit-a-short-on-ramp-to-trust-your-instruments):

1. **Is the engine real?** Run the Gas City **conformance check** — does `gc` *physically refuse* a
   forbidden action, or only *log it after the fact*? If detect-only, everything stays fully
   human-supervised. *(This is move #1 of the entire build.)*
2. **Can you trust the judge?** Measure the judge's false-"all-good" rate on known-answer builds (two
   human labellers) before its verdicts drive anything. Until it clears a bar, **every build gets full
   human review.**
3. **Lock the test vault.** Held-out scenarios must be unreadable *and* un-weakenable by the worker, and
   authored by someone other than the worker.

The smoke-toys below are the natural way to *do* the on-ramp while having a bit of fun.

---

## The trust map right now

Nothing is built, so **everything is 🌑 Untouched**. The whole point of Board 1 is to start nudging the
backbone-25 off 🌑. The ladder: 🌑 untouched → 🌒 smoke-OK → 🌓 poked → 🌔 worked → 🌕 trusted.

| Product (capability cluster) | Backbone components | Trust today |
|---|---|---|
| **Gas City** (the substrate — one install) | C01 C02 C03 C04 C05 C17 C18 C19 C23 C41 C42 | 🌑 |
| **Claude Code** (worker) + **model-floor** | C28 C29 | 🌑 |
| **Spec intake** | C08 C09 | 🌑 |
| **Bead-type schema** | C20 | 🌑 |
| **Evaluation tier** (the hinge) | C30 C31 C32 C33 | 🌑 |
| **The fence** (safety) | C34 C43 | 🌑 |
| **Bootstrap** (self-build loop) | C51 C52 C53 | 🌑 |

*Set trust by feel; let the playing nudge it. A card that survives a trivial run earns its target 🌒; a
card aimed deliberately at a target that survives earns 🌓; a self-build that ships a real factory part
earns 🌔.*

---

## The board — shop by mood

| # | Card | Flavor · what it pressures | Size · vibe | What you'd learn | Leaves behind | Needs first |
|---|---|---|---|---|---|---|
| 1 | **Hello, formula** | *Smoke-toy* · the run loop (C01 C04 C05 C18 C19 C23) | tiny · a quick win | does a 3-step recipe run end-to-end at all? | a warm engine (throwaway) | on-ramp #1 |
| 2 | **Does the judge speak?** | *Smoke-toy* · the eval tier (C30 C31 C32 C33 C42) | tiny · reassuring | does a build get *run* and *get a verdict* at all? | the judge harness, warmed | on-ramp #1 |
| 3 | **Tiny event registry** | *Reduced model of agent-os B12* · spec-intake + judge (C08 C09 C32 C33) | small · clean | can the judge tell a *spec* bug from a *code* bug on a simple schema? | a reduced model on the path to B12 | on-ramp |
| 4 | **Two-rule policy bundle** | *Reduced model of agent-os B3* · deterministic tool path + judge (C17 C05 C32) | small · tidy | does "deterministic-first" actually pay off? | a reduced model toward B3 | on-ramp |
| 5 | **C07 glossary** ⭐ | *Self-build (real driver)* · the gentlest dogfood (C08 C09 C51 C52 C53) | tiny · satisfying | can the factory build a tiny piece of *itself* and pass the gate? | **a real factory part: the canonical glossary** | on-ramp; an exemplar to copy |
| 6 | **Make formulas visible (C14)** | *Self-build (real driver)* · the self-build loop on a small tool (C51 C52 C53) | a session · genuinely useful | can the factory build a small *tool* for itself? | a real factory part: the DOT/workflow viewer | on-ramp; card 5 as exemplar |
| 7 | **EARS spec linter (C10)** | *Self-build (real driver)* · deterministic gate on the load-bearing input (C08 C51 C52 C53) | a session · solid | does a built-by-factory *tool* hold up on real specs? | a real factory part: the spec linter | on-ramp; card 5 as exemplar |
| 8 | **Bead TUI viewer** | *Toy (dual-use)* · the bead store + event bus + attribution (C19 C23 C41) | a session · fun & handy | what do runs actually *look like* as beads? | **a keeper: your window into every run** | on-ramp #1 |
| 9 | **Emoji-saga** | *Invented-for-fun* · formula composition + discipline nudge (C12/C13 + C16) | tiny · silly | does the formula engine compose, and does the discipline linter nag correctly? | a giggle (throwaway) | on-ramp #1 |
| 10 | **_(your idea here)_** | *Invented project* · whatever feels lonely + fun | your call | depends — that's the point | maybe a gem | tag it so it still counts |

⭐ = the required first card. The point of the table isn't the exact cards — it's the **shape**: a
low-energy night → a 🌒 smoke-toy (1, 2); a "let's build something real" night → a self-build (5, 6, 7);
a "let me just *see* what's happening" night → the bead viewer (8); a "let me enjoy myself" night → make
something up (9, 10).

---

## The cards, fleshed out

### 1. Hello, formula  *(smoke-toy)*
- **Pressures:** the bare run loop — substrate (C01), session (C04), dispatch/sling (C05), reconciler
  (C18), bead store (C19), event bus (C23). The native formula/molecule engine (C12/C13) rides along.
- **Trust of target:** 🌑 everything.
- **Size · vibe:** tiny · a quick win to prove the lights turn on.
- **What you'll learn:** does a trivial 3-step recipe (a `tool` → `agent` → `tool`) actually instantiate
  into a molecule and walk to completion? Where does it break first?
- **Dual-use:** throwaway — but it leaves the engine *warm* and you with a working mental model.
- **Prereqs:** on-ramp #1 (conformance check) — you want to know the engine is real before you trust the
  run.

### 2. Does the judge speak?  *(smoke-toy)*
- **Pressures:** the evaluation tier — scenario store (C30), runner (C31), judge (C32), satisfaction
  (C33), run in an isolated rig (C42).
- **Trust of target:** 🌑.
- **Size · vibe:** tiny · reassuring.
- **What you'll learn:** can a built thing be *run* against a held-out scenario and *get a verdict* at
  all — on an obvious known-good and an obvious known-bad? This is the smoke before the real
  judge-calibration of on-ramp #2.
- **Dual-use:** scaffolds straight into on-ramp #2 (calibration); the harness stays warm.
- **Prereqs:** on-ramp #1. (Do **not** trust the verdict yet — that's what calibration is for.)

### 3. Tiny event registry  *(reduced model of agent-os B12)*
- **Pressures:** spec-intake (C08 spec artifact, C09 prompt binding) and the judge's *diagnostic* power
  (C32 → C33) on simple, cluster-free schema data.
- **Trust of target:** 🌑.
- **Size · vibe:** small · clean and satisfying.
- **What you'll learn:** can the [triangle](docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md)
  actually distinguish a **spec** bug from a **code** bug on simple schemas — i.e. is the judge a
  *diagnostician*, not just a scorer?
- **Dual-use:** a reduced model *on the path to* real agent-os B12 — the learning transfers when B12
  becomes a real driver on a later board.
- **Prereqs:** on-ramp (you're leaning on the judge).

### 4. Two-rule policy bundle  *(reduced model of agent-os B3)*
- **Pressures:** the **deterministic (no-AI) tool path** (C17 tool nodes, C05 dispatch) and the judge
  (C32) on a tiny policy.
- **Trust of target:** 🌑.
- **Size · vibe:** small · tidy.
- **What you'll learn:** does **"deterministic-first"** actually pay off — is a `tool` step cheaper *and*
  more reproducible than an `agent` step where a script suffices? (The discipline linter is already
  nudging you here; this measures the payoff.)
- **Dual-use:** a reduced model toward agent-os B3/B16 policy tooling.
- **Prereqs:** on-ramp.

### 5. C07 glossary  *(self-build — real driver)* ⭐ **the required first card**
- **Pressures:** the **gentlest possible self-build**. It exercises spec-intake (C08/C09) and the
  bootstrap self-build loop (C51 gene-transfusion predicate → C52 recursion + human design-review gate →
  C53 go/no-go milestone) **at the lowest risk in the whole graph** — because C07 owns *no runtime, no
  process, no live state*: it is a document plus a machine-readable term registry
  ([C07 spec §1](architectures/v4/spec/C07-vocabulary-glossary.md#1-purpose--responsibility)).
- **Trust of target:** 🌑 (the self-build loop has never run).
- **Size · vibe:** tiny · satisfying — the gentlest first dogfood.
- **What you'll learn:** can the factory **author a spec for one of its own components, build it in
  isolation, have it scored, and pass a human-reviewed gate** — the
  [bootstrap thesis](architectures/v4/implementation-dependencies.md#the-backbone-the-most-aggressive-path-to-safe-self-building)
  — when the component is as simple as a glossary? If the loop can't do *this*, it can't do anything.
- **Dual-use:** maximally dual-use — it leaves behind **a real, kept factory part: the single canonical
  glossary** of every load-bearing Gas City / v4 term (`city`, `rig`, `formula`, `molecule`, `bead`,
  `sling`, `Order`, `Health Patrol`, `gene transfusion`, …), each paired with its generic equivalent and
  corpus provenance. That directly kills the **undefined-term debt** (defect G06) and the
  **vocabulary-lock-in** risk the design names
  ([C07 spec §1](architectures/v4/spec/C07-vocabulary-glossary.md#1-purpose--responsibility)) — and it's
  the *best cost/benefit ratio in the entire component graph*
  ([build order, top-ten #1](architectures/v4/implementation-dependencies.md#after-the-backbone-the-top-ten-to-build-next-by-costbenefit)).
- **Prereqs:** on-ramp; and an **exemplar to copy** — a self-build "rides on the same guardrails as any
  build: it needs a real external example to copy (no invention from scratch)"
  ([methodology Part 6](methodology-and-formulas-plain-english.md#part-6--the-co-implementation-loop-worked-end-to-end)).
  The [C07 spec](architectures/v4/spec/C07-vocabulary-glossary.md) (and its seed term table in
  [§4.1](architectures/v4/spec/C07-vocabulary-glossary.md#4-data-model--state)) is the natural exemplar.
- **Why it's first:** it is the *least-contested, lowest-risk* self-build — exactly the right thing to
  try the bootstrap loop on the very first time (and the right
  [exemplar](AGENTS.md) for self-build cards 6 and 7).

### 6. Make formulas visible — C14 DOT visualizer  *(self-build — real driver)*
- **Pressures:** the self-build loop (C51/C52/C53) on a small **tool** rather than a document — one step
  up in complexity from the glossary.
- **Trust of target:** 🌑 (nudged to 🌒 if card 5 ran first).
- **Size · vibe:** a session · genuinely useful to you.
- **What you'll learn:** can the factory build a small *tool for itself* — the
  [formula↔DOT translator/visualizer (C14)](architectures/v4/spec/C14-formula-dot-translator.md) — so you
  can finally **see** a formula as a graph (`gc formula export <name> --format dot`)? "I couldn't *see*
  what the formula did until I hand-drew it" is a predicted early factory-gap; this closes it.
- **Dual-use:** a real, kept factory part — the workflow viewer you'll use on every later card.
- **Prereqs:** on-ramp; card 5 (C07) as the exemplar for "how a self-build goes."

### 7. EARS spec linter — C10  *(self-build — real driver)*
- **Pressures:** the self-build loop (C51/C52/C53) plus the **deterministic tool path** — a built-by-
  factory `tool` that runs on the load-bearing input, the spec artifact (C08).
- **Trust of target:** 🌑.
- **Size · vibe:** a session · solid.
- **What you'll learn:** does a factory-built *deterministic* tool hold up on real specs — i.e. can the
  factory produce a cheap, reproducible quality gate
  ([C10 spec](architectures/v4/spec/C10-spec-linter-ears.md))? It's off-the-shelf INCOSE/EARS rules, so
  the *building* is the test, not the rules.
- **Dual-use:** a real, kept factory part — a deterministic gate on every future spec.
- **Prereqs:** on-ramp; card 5 as exemplar.

### 8. Bead TUI viewer  *(toy — dual-use; your request)*
- **Pressures:** the **bead store** read path (C19 — the typed work-graph and its `state`), the **event
  bus** (C23 — the append-only timeline), and **attribution** (C41 — who/what did each unit of work).
- **Trust of target:** 🌑.
- **Size · vibe:** a session · fun and immediately handy.
- **What you'll learn:** what does a run actually *look like* as beads? A terminal UI to **browse what's
  in the store and what completed** turns the abstract "watch it as beads"
  ([methodology Part 4](methodology-and-formulas-plain-english.md#part-4--how-you-actually-run-one-the-operators-loop))
  into something you can actually scroll. It also quietly pressure-tests whether the bead schema (C20)
  carries enough state to be *browsable*.
- **Dual-use:** **a keeper** — your window into every other card you play. Not one of the 57 components,
  so tag it as an *invented tool* (it still counts toward coverage of C19/C23/C41).
- **Prereqs:** on-ramp #1 (you need a real store with real beads in it — run card 1 first and you'll have
  something to look at).

### 9. Emoji-saga  *(invented-for-fun)*
- **Pressures:** formula **composition** (C12/C13 — chaining `agent` + `tool` steps and a `sub_formula`)
  and the **discipline linter** (C16 — does it correctly nag you for using an `agent` step where a `tool`
  would do?).
- **Trust of target:** 🌑.
- **Size · vibe:** tiny · deliberately silly.
- **What you'll learn:** does the formula engine actually *compose* small recipes, and does the discipline
  nudge fire when it should — discovered while making something that makes you smile.
- **Dual-use:** throwaway (but pressure-testing and amusement are the same move — charter rule).
- **Prereqs:** on-ramp #1.

### 10. _(your idea here)_  *(invented project — the open slot)*
- **Pressures:** whatever's **lonely** (low-trust, not visited) and sounds fun. The charter says you can
  **insert your own project any time** — we just tag it so it still counts toward coverage.
- **Everything else:** your call. That's the point.

---

## What the opening board touches (a gentle coverage nudge)

Played together, cards 1–9 lean on most of the backbone-25:
**C01 C04 C05 C08 C09 C17 C18 C19 C23 C30 C31 C32 C33 C41 C42 C51 C52 C53** (and C28/C29/C03 ride along
under every agent step and config load).

**Honestly lonely after Board 1** (a *suggestion*, never a mandate):
- **The fence — C34 (holdout integrity) and C43 (blast-radius boundary).** Deliberately so: the fence is
  what you need to run *unattended*, and Board 1 is a fully-supervised shakedown. The fence becomes
  interesting on a later board, once you trust the instruments and want to take your hands off.
- **C02 (pack ABI) and C20 (bead schema contract).** C20 gets *partially* poked by the bead viewer
  (card 8); a dedicated card can come later if it stays lonely.

That lonely list is the seed of the **factory-gap ledger** below — the board is *showing* you what it
isn't exercising yet.

---

## The two ledgers (byproducts — start empty)

Per the [charter](factory-discovery-charter.md#the-two-ledgers-the-only-records-we-keep-both-byproducts),
these are the only records we keep, and both fall out of *playing* — never separate admin.

### Defect ledger
*Every failed build, tagged by which corner of the
[triangle](docs/adr/0069-spec-scenarios-system-triangle-evaluation-invariant.md) was at fault — spec /
scenarios / system / judge.*

| Date | Card | Triangle corner | Note |
|---|---|---|---|
| _(empty — nothing built yet)_ | | | |

### Factory-gap ledger
*Every time real work hits a factory limitation (missing part, awkward formula, judge weakness,
substrate surprise, work-it-can't-build-yet). **This ledger — not a roadmap — decides what we build
next.***

| Date | Card | Gap hit | Candidate fix-card |
|---|---|---|---|
| _(pre-seeded from coverage)_ | Board 1 | The fence (C34/C43) is unexercised; can't run unattended until it exists | a "stand up the fence" card on a later board |

---

## Decisions settled for this board

These were the [operator decisions the handoff flagged for Step 1](architectures/v4/SESSION-HANDOFF-2026-06-05-discovery-charter-and-next-steps.md#step-1-next-session--build-the-first-set-of-cards-author-the-opening-board),
now resolved by the operator (2026-06-06):

1. **Real drivers on Board 1 = factory self-builds only.** No real agent-os component is built yet;
   agent-os appears *only* as reduced-fidelity models (cards 3, 4). Rationale: Board 1 is a shakedown to
   see whether the 25 work together — don't do complicated (twin-gated, cluster) work the first time on
   an experimental system.
2. **Portfolio frozen.** No second portfolio project is named now; agent-os stays the sole (test-target)
   product.
3. **Added toy:** the **bead TUI viewer** (card 8), for browsing what's in the store and what completed.

---

*Companions: [the charter](factory-discovery-charter.md) (why & how),
[the next-steps report](next-steps-plain-english.md) (the on-ramp & board model),
[the methodology & formulas report](methodology-and-formulas-plain-english.md) (the Gas City formulas).
This is a living board — cards get played, trust gets nudged, and the gap ledger grows. The next step
after the board is [Step 2: a plan to implement the first 25 components](architectures/v4/SESSION-HANDOFF-2026-06-05-discovery-charter-and-next-steps.md#step-2-a-later-session--create-a-plan-to-implement-the-first-25-components).*
