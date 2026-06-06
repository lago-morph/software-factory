# Session handoff — 2026-06-06 — Board 1 + backbone build plan closed; next is execution (environment-gated)

This is the pickup brief for the next session. The **planning arc of the discovery phase is closed**:
the opening board and the backbone build plan are authored, reviewed, and merged. The next work is
**Step 3 — execution (standing up Gas City and running the Gate B0 conformance check)** — but it is
**gated on a real environment**, which is the single most important thing this handoff carries forward.

Supersedes the [prior handoff](SESSION-HANDOFF-2026-06-05-discovery-charter-and-next-steps.md) (which
named the three steps; Steps 1–2 are now done).

## Where we are

| Concern | State | Detail |
|---|---|---|
| Step 1 — the opening board | **Closed** (PR #249 merged) | [`BOARD.md`](../../BOARD.md) |
| Step 2 — the backbone build plan | **Closed** (PR #250 merged) | [`backbone-implementation-plan.md`](backbone-implementation-plan.md) |
| Step 3 — execute (build the 25) | **Not started; environment-gated** | see [the sandbox reality](#the-load-bearing-reality-the-sandbox-cannot-host-the-running-factory) |
| Factory code / running `gc` | **None exists** | nothing has been installed or run; Gas City's native claims are still *unverified* |
| Navigation | **Updated** | [`AGENT-ENTRY.md`](../../AGENT-ENTRY.md) §2 (board + this handoff) and §3 (both plans) |

## The load-bearing reality: the sandbox cannot host the running factory

Everything shipped so far is **authoring** — documents committed to git, which is exactly what the
ephemeral web sandbox is for. But **Step 3 is different in kind**, and the next session must not assume
it can "just build it here." Three honest reasons, settled with the operator this session:

1. **The sandbox is ephemeral.** The container is reclaimed after the session ends; only what is
   committed and pushed survives. An installed `gc` binary, a running worker rig, a populated bead
   store, process state — all vanish. A factory that must be reinstalled from scratch every session is
   not a factory you *operate*.
2. **Network is policy-gated.** Outbound access depends on the environment's network policy. Whether the
   sandbox can clone the gascity-prototype, install `gc`, and pull dependencies is **unknown until
   probed** (see [work that doesn't need user input](#work-that-doesnt-need-user-input)).
3. **Gate B0 needs a *real, pinned* `gc`.** The whole point of the conformance check is to turn "Gas City
   natively *prevents* bad access" from an assumption into a fact by running the actual binary end-to-end
   (the design states plainly that nobody has done this). A throwaway run in an ephemeral box yields a
   throwaway answer; the result the build *stands on* must come from an environment the operator keeps.

**The split, therefore:** *author* the implementation here (config, scripts, schema, glue) and commit
it; *run and operate* the factory on a **persistent, networked host the operator controls** (their
machine, or a server/VM). The two are different venues for different work.

## The next work — Step 3 (execute), entry at Gate B0

The canonical phase description is [the backbone build plan, Gate B0](backbone-implementation-plan.md#gate-b0--substrate-truth-the-literal-first-move):
adopt + pin `gc`, author `city.toml`/`pack.toml`, run the conformance check, **record prevent-vs-detect**.

### Entry blocker (genuine user-input territory)

- **Question:** *Which environment will host the actual build and run of the factory?* (operator's
  machine, a dedicated server/VM, a cloud host, …) The sandbox cannot be it (above).
- **Lead-agent recommendation:** a **persistent host the operator controls**, with network access to the
  gascity-prototype. Treat this web sandbox as a *development + authoring* venue only. *(This is a
  practical judgment, not an evidence-based finding.)*
- **Rewind path:** if the operator wants a quick **throwaway spike** in-sandbox just to see `gc` move,
  that's fine — but its results are explicitly *not trusted* as the Gate B0 verdict; the real conformance
  check re-runs on the chosen host.

### Work that doesn't need user input (can be done in-sandbox now, and committed)

All of this is *authoring* that makes the first real move ready-to-run the moment an environment exists:

1. **Probe sandbox reachability** — attempt to clone `lago-morph/gascity-prototype` and note whether the
   network policy allows it. One command; tells us whether an in-sandbox spike is even possible. *(Pure
   diagnostics; no commitment.)*
2. **Author the Gate B0 artifacts** — the conformance-check **probe script(s)** (attempt a
   cross-partition read of the scenario partition + a production-typed action; record prevent-or-detect
   per probe, per [C01 §AC-2](spec/C01-gas-city-substrate.md)) and the `city.toml`/`pack.toml`
   **skeleton** (per [C03](spec/C03-config-feature-flags.md)). So Gate B0 becomes "run these," not
   "design these."
3. **Author early custom-build pieces that are pure authoring** — the **bead-type schema interface
   freeze** ([C20](spec/C20-bead-schema.md)) and a first **spec-intake format** sketch
   ([C08/C09](spec/C08-spec-artifact.md)), both of which the build plan schedules in Gate B1 and neither
   of which needs a running `gc` to *draft*.

## Carried-forward material (binding reading list, in order)

1. [`AGENTS.md`](../../AGENTS.md) — binding conventions (PR-ready-not-draft, internal-reference rule, process-skill triggers).
2. [`AGENT-ENTRY.md`](../../AGENT-ENTRY.md) — navigation; §2 current state, §3 the two plans.
3. [factory discovery charter](../../factory-discovery-charter.md) — the feel + vocabulary + rules-of-the-game; **read for the feel before the plans.**
4. [backbone implementation plan](backbone-implementation-plan.md) — **the binding spec for Step 3**; start at Gate B0. Adopt-vs-build classification, the five gates, the amendment map.
5. [implementation build order](implementation-dependencies.md) — the dependency source of truth (7 products, three rings, critical path).
6. [panel verdict — the 8 amendments](_meta/next-steps/panel/VERDICT.md) — binding constraints on the build (esp. AM-1 calibration, AM-2 holdout-write-path, AM-3 fence/D-30, AM-7 single-seat).
7. [Board 1](../../BOARD.md) — the play menu at the seam between building and exercising.
8. [decisions-to-make](../../decisions-to-make.md) — the operator decisions; **#4 prevent-vs-detect** and **#1 fence-before-unattended** govern Gate B0.
9. For Gate B0 specifically: [C01 substrate/conformance](spec/C01-gas-city-substrate.md), [C43 fence](spec/C43-isolation-boundary.md), [C34 holdout](spec/C34-holdout-integrity.md).

## Open questions / suggestions for the next session to surface

1. **Which environment hosts the real build** (the entry blocker above). *Value judgment + practical
   constraint; no corpus evidence decides it — the operator does.*
2. **Author the Gate B0 prep artifacts in-sandbox now?** Recommended yes — it's free, durable, and
   de-risks the first real move. *Lead-agent view; low stakes.*
3. **The `[PROPOSED]` judge-calibration bar + sample size** (false-green threshold, per-corner min-N).
   Deferred to Gate B4 but it is operator policy — surface it with a recommended coarse/time-boxed
   default when the eval tier is stood up. Evidence: [AM-1/AM-8](_meta/next-steps/panel/VERDICT.md).
4. **Secrets storage + one library's license** ([decision #6](../../decisions-to-make.md)) — defer until
   the first component needs a real credential.

## Task-aware reading lists

### Step 3 entry — stand up Gas City + run the Gate B0 conformance check (on a real host)
- Read: [`AGENTS.md`](../../AGENTS.md), [`AGENT-ENTRY.md`](../../AGENT-ENTRY.md), [backbone plan § Gate B0](backbone-implementation-plan.md#gate-b0--substrate-truth-the-literal-first-move), [C01 substrate/conformance](spec/C01-gas-city-substrate.md), [decision #4 prevent-vs-detect](../../decisions-to-make.md#4-does-gas-city-prevent-bad-access-or-only-notice-it-after-the-fact), [C43 fence](spec/C43-isolation-boundary.md), [C34 holdout](spec/C34-holdout-integrity.md).
- Skip: the [unified/exercising plan](_meta/next-steps/10-unified-plan.md) (that phase begins *after* the 25 exist); all v3 synthesis docs.

### Author Gate B0/B1 prep artifacts in-sandbox (no running `gc` needed)
- Read: [backbone plan § Gate B0–B1](backbone-implementation-plan.md#gate-b0--substrate-truth-the-literal-first-move), [C01](spec/C01-gas-city-substrate.md) + [C03 config](spec/C03-config-feature-flags.md) (for `city.toml`/`pack.toml`), [C20 bead schema](spec/C20-bead-schema.md), [C08 spec artifact](spec/C08-spec-artifact.md), [methodology companion](../../methodology-and-formulas-plain-english.md) (the formula shape).
- Skip: eval-tier (C30–C33), fence-holdout (C34), and bootstrap (C51–C53) specs until their gates.

## Concrete pickup steps for the next session

1. Read items 1–4 of the [binding reading list](#carried-forward-material-binding-reading-list-in-order) (AGENTS, AGENT-ENTRY, charter, backbone plan).
2. Internalize [the sandbox reality](#the-load-bearing-reality-the-sandbox-cannot-host-the-running-factory) — do **not** assume Step 3 runs here.
3. Surface the [entry blocker](#entry-blocker-genuine-user-input-territory) to the operator: which environment hosts the real build. Use `AskUserQuestion`.
4. In parallel (needs no answer): offer to **probe sandbox reachability** and **author the Gate B0 prep artifacts** — both are in-sandbox, committable, and de-risk the first real move.
5. Once the environment is chosen, execute Gate B0 there: install/pin `gc`, run the conformance probes, record the prevent-vs-detect verdict, and write the one-page substrate-truth note (the build plan's Gate B0 exit).

## Current git state

Branch chain at handoff (top to bottom):
- `claude/software-factory-c07-cards-ahWyY` — **this handoff** (PR pending).
- Board 1 ([PR #249](https://github.com/lago-morph/software-factory/pull/249)) — **merged** to `main`.
- Backbone build plan ([PR #250](https://github.com/lago-morph/software-factory/pull/250)) — **merged** to `main`.
- `main` (at `bef5ec5`, the #250 merge).

No subagents were used this session; no open PRs other than this handoff's. When this merges, the state
above is the canonical pickup point.
