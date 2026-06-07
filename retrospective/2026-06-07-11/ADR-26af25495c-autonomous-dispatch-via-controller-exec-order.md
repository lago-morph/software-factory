# ADR: Autonomous dispatch via a controller exec order

- **ID**: ADR-26af25495c
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-06-07
- **Source retrospective**: ../2026-06-07-11.md
- **PRs covered**: #10

## Context

The v4 prototype needed a created task bead (`gc bd create --rig rigN …`) to be worked end-to-end with no manual nudge or sling, but out of the box it was not: gastown's **mayor** wakes on a cadence, *triages* the open beads, and idles, so a bead created after its last wake sits `open` until the next wake — and the mayor may judge it "spurious" and decline it (both observed live). The downstream pipeline (polecat claims → commits on a worktree branch → refinery merges → bead closes) was already verified to work *once a bead is routed*; the missing piece was strictly the routing decision. Three approaches were on the table (the HANDOFF named them a/b/c), and the choice is architectural because it determines where the autonomy seam lives — in a deterministic controller, in the daemon's scheduling knobs, or in an LLM agent's prompt — and every later autonomy layer builds on that seam.

## Decision

Implement autonomous dispatch of rig task beads as a city-level controller exec order on a short cooldown that slings ready, unrouted, top-level task beads directly to each rig's polecat, rather than changing the mayor's triage policy or loosening the daemon wake budget.

Concretely: `pack/orders/route-rig-tasks.toml`, `trigger = "cooldown"`, `interval = "30s"`, with an inline `exec` script that, for each rig (`RIG1_NAME`/`RIG2_NAME`), lists `gc bd list --rig <rig> --json` and `gc sling <rig>/gastown.polecat <id> --on sf-small-task` for every bead matching: `issue_type == "task"`, `status == "open"`, and **no** `gc.routed_to` / `gc.step_ref` / `gc.root_bead_id`, and `gc.kind != "workflow"`. `entrypoint.sh` symlinks the pack's `orders/` dir into the city scope so gc discovers it (gc scans an `orders/` dir beside each formula layer).

## Alternatives considered

- **(b) Loosen the daemon wake budget** (`[daemon].max_wakes_per_tick`, default 5) — rejected as a primary fix. It only changes how fast sessions *materialize* per tick; it does not make the mayor route a bead it triaged away, so it cannot by itself deliver hands-off dispatch. Left at the gastown default.
- **(c) Change the mayor's prompt/policy** to auto-sling every open task bead — rejected. It is heavier, diverges from gastown's mayor design (which is intentionally a triaging coordinator), and burns an LLM wake per cycle. Unnecessary once a mechanical order does the routing.
- **(a-nudge) An order that nudges the mayor** instead of slinging directly — rejected within the chosen approach. Nudging still routes the decision through the mayor's triage, which is exactly the failure mode (a declined bead never gets worked). Slinging directly side-steps triage, which is the point.

## Consequences

- **Easier:** a plain `gc bd create --rig rigN` is now worked unattended (verified live: auto-routed at t+69s → in_progress → polecat commit `7a691f9` → refinery merge → `closed`, ~10 min). The router costs nothing — no agent, no LLM, no token spend — and reuses the already-verified manual `gc sling` path, so the downstream pipeline is unchanged. It is idempotent (a slung bead's `gc.routed_to` is set, so the next tick skips it).
- **Harder / accepted trade-offs:** the mayor's triage judgment is deliberately bypassed for task beads — every top-level task bead is dispatched, even one the mayor would have declined. That is the intended behavior for the prototype's "create a bead and the city works it" goal, but a future variant that *wants* selective triage will need to re-introduce it (e.g. a label gate the order honors). The filter is coupled to gc's molecule metadata keys (`gc.step_ref`, `gc.root_bead_id`, `gc.kind`); if gastown changes those keys the filter must follow. Wake-budget latency still gates how fast the polecat *materializes*, so completion is "a few minutes," not seconds.

## References

- [`../2026-06-07-11.md`](../2026-06-07-11.md) — the source retrospective.
- [`./SKILL-SPEC-16761ebad2-probe-injected-exec-environment.md`](./SKILL-SPEC-16761ebad2-probe-injected-exec-environment.md) — the probe that established the order's exec environment.
- [`./SKILL-SPEC-33e57a82dc-tiered-token-verification.md`](./SKILL-SPEC-33e57a82dc-tiered-token-verification.md) — how the order was verified (free tier + one paid run).
- PR the decision was made in: #10 (`lago-morph/software-factory-prototype`). The order file: `pack/orders/route-rig-tasks.toml`; the design write-up: the prototype's `docs/PLAN.md` "Autonomous dispatch" section.
