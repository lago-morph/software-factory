# The progress-tracker TUI — an operator instrument built alongside the backbone

**What this is.** The plan for the **Gascity progress tracker**: a terminal UI over the
[software-factory-prototype](https://github.com/lago-morph/software-factory-prototype) that lets the
operator *see* the factory work — the flow of beads through agent sessions, the contents and status of
individual beads, the commit diffs a bead's execution produced, and the formulas the factory runs. It
tracks the request in [idea-pipeline issue #21](https://github.com/lago-morph/idea-pipeline/issues/21)
and is the durable home for how that request is being addressed.

**What this is NOT.** It is **not** a 26th backbone capability component. The
[backbone implementation plan](backbone-implementation-plan.md) builds a *closed, dependency-justified
set of 25* whose whole rationale is the safe self-build thesis. The tracker is an **operator
instrument** — the thing you watch the backbone *with*. The on-ramp already frames instruments this way:
*"until you trust the factory's instruments you can't trust the result of any card"*
([Board 1 on-ramp](../../BOARD.md#before-you-play-the-one-ordered-bit-the-on-ramp)). So it is built
*alongside* the backbone, not *inside* the 25.

---

## Why an instrument, not a component

The 25 backbone components form a strict dependency graph aimed at one apex (C53 behind the fence C43).
Inserting a viewer into that graph would distort the coverage map the
[build order](implementation-dependencies.md) is built around — the tracker depends on the substrate
but nothing depends on *it*. Recording it as an instrument keeps the backbone's accounting honest while
still giving the tracker a first-class place in the build: it is the **next thing built** once the
substrate is up, and it **grows as each backbone component lands** (each new watchable capability is a
reason to extend the tracker).

This also matches Board 1, which already carries the seed of this idea as
[Card 8 — Bead TUI viewer](../../BOARD.md#8-bead-tui-viewer--toy--dual-use-your-request), explicitly a
*toy (dual-use)* and *not one of the 57 components*. Card 8 is the smoke-test of the instrument this plan
institutionalizes.

---

## The three pieces (operator framing)

The operator described the work in three time-phases. All three are honored here:

1. **Right now — the toy (v0.1).** A deliberately minimal viewer the *current* prototype can build,
   delivered as small chunks (see [the chunk ladder](#the-chunk-ladder)). Each chunk doubles as a
   **shakedown of the prototype's own build loop**: the agent authors a `gc bd create` task prompt, the
   prototype's fleet builds it, and we learn whether the early factory can produce a non-trivial,
   useful artifact. Scope is kept small on purpose — confidence that the very early factory can build it
   matters more than features.
2. **While building the backbone — institutionalize it.** The tracker is recorded as an operator
   instrument (this plan), pointed to from the [backbone plan](backbone-implementation-plan.md), and
   extended as components land. Board cards don't begin until the backbone exists, so this phase is
   about keeping the instrument current with the substrate, not running enhancement cards yet.
3. **After the backbone — continual enhancement by cards.** Every new watchable capability becomes a
   **card on [the board](../../BOARD.md)**. The first step of any such card is a **back-and-forth scope
   and UI discussion with the operator**; anything ruled out of a given card's scope goes **back on the
   board** unless there is an explicit decision not to build it.

---

## The chunk ladder

Built incrementally; each rung is a single `gc bd create` task prompt the agent authors, kept tight so
the prototype can actually finish it. Later rungs start only if the prior rung lands cleanly.

| Rung | Capability | Read surface it leans on | Keyboard model |
|---|---|---|---|
| **1** | Browse **beads** across all scopes (city + each rig) | `gc bd list` / `gc bd list --rig <name>` / `gc bd show <id>` | ↑/↓ navigate · Enter detail · Esc back · q quit |
| **2** | Browse **sessions**; Enter shows a `tail -30` peek | `gc session list` / `gc session peek <id>` | ↑/↓ navigate · Enter peek · Esc back · q quit |
| **3+** | Bead **commit diffs**; configurable **polling** (default 60s) + force-refresh; interrupt-driven updates if feasible; **formula** browsing | rig git worktrees; the event bus (C23) if a watchable stream exists | grows; **keys always shown** |

Two invariants hold on every rung, straight from the request: **keyboard commands are prominently
displayed at all times**, and the viewer is **read-only**. Polling and interrupt-driven refresh are
deferred past rung 1 deliberately — rung 1 loads once, so the shakedown isolates "can the factory build
a TUI" from "can it build a live updater." Whether interrupt-driven (event-bus) updates are possible at
all is an open question to verify against the running prototype before that rung is scoped.

---

## Where everything lives (repo discipline)

Operator-set, and load-bearing for how this issue closes:

| Repo | Holds | Does NOT hold |
|---|---|---|
| [idea-pipeline](https://github.com/lago-morph/idea-pipeline) | **Only** issue #21 + progress comments | code, plans |
| [software-factory](https://github.com/lago-morph/software-factory) | durable plans / handoffs (this plan, the board card, the backbone note) | the runnable TUI |
| [software-factory-prototype](https://github.com/lago-morph/software-factory-prototype) | the **runnable TUI**, shipped inside the city container | the planning record |

**Close criterion for issue #21:** the issue closes once the effort is **institutionalized in durable
software-factory artifacts** (this plan + the backbone note + the board card) and the chunk-1 build loop
is proven — even though enhancement cards remain open on the board. The board, not the issue, is the
durable home of the ongoing work.

---

## Build & ship approach (the goal drives the config)

The prototype's configuration is ours to reshape to serve the goal, rather than a constraint to work
around. The target shape:

- **A repo-backed build rig.** A rig is pointed at the
  [software-factory-prototype](https://github.com/lago-morph/software-factory-prototype) repository (via
  its `RIG_*_URL`) with push credentials in the container, so the dogfood build produces a real branch
  we push — the factory builds its own viewer and the artifact is durable by construction.
- **Shipped in the city image.** The TUI source lives in the prototype's `tui/` directory; the
  Dockerfile bakes it into the image and a small run shim (`sftui`) makes it runnable as
  `docker compose exec city sftui`.
- **A human gate before self-modification.** A rig that *is* the prototype repo can edit the files that
  build its own container, so each chunk's bead is bounded to the `tui/` directory and the resulting PR
  is **operator-reviewed before merge and image rebuild**. This mirrors the backbone's own
  human-design-review gate (C52/C53) — the fence ethos applied to the instrument.

The concrete prototype changes (rig wiring, credentials, Dockerfile shim, `tui/` scaffold) are staged in
the [software-factory-prototype](https://github.com/lago-morph/software-factory-prototype) repository.
The live dogfood run (`docker compose up` + the chunk-1 `gc bd create` prompt) **can be exercised in the
Claude Code web sandbox itself** — Docker is available there (the daemon is started with `sudo dockerd`),
and a CA-injection + token build/test recipe is documented in
[the prototype's sandbox build/test notes](https://github.com/lago-morph/software-factory-prototype/blob/main/docs/HANDOFF.md).
It simply has not been run yet, so the prototype changes are unverified-by-execution until that pass.

---

## How the tracker grows with the backbone

As each backbone component lands, the tracker gains something to watch. The mapping (a guide, not a
contract):

| Backbone capability | What the tracker can then show |
|---|---|
| Bead store / schema (C19 / C20) | richer bead detail, typed views |
| Event bus (C23) | interrupt-driven / live updates instead of polling |
| Attribution (C41) | who/what did each unit of work |
| Formula engine + visualizer (C12–C14) | browse formulas and render them |
| Evaluation tier (C30–C33) | verdicts and satisfaction per build |
| Fence (C34 / C43) | blast-radius and holdout status of an action |

Each of those is a candidate enhancement **card** for the after-backbone phase, scoped through the
operator discussion the request requires.

---

*Companions: the [backbone implementation plan](backbone-implementation-plan.md) (the 25 this instrument
watches), [Board 1](../../BOARD.md) (the play surface and Card 8 seed), the
[build order](implementation-dependencies.md) (the dependency source of truth), and the
[charter](../../factory-discovery-charter.md) (the feel: fun-first, bookkeeping-as-byproduct). A living
plan — it grows as the chunk ladder climbs and the backbone components land.*
