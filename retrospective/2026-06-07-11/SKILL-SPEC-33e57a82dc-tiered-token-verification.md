# Spec: `tiered-token-verification`

- **ID**: SKILL-SPEC-33e57a82dc
- **Source retrospective**: ../2026-06-07-11.md

## Intent

Live end-to-end verification of an agentic system often has two halves with very different costs: a deterministic, controller-side half (config discovery, scheduling, routing, idempotency, filtering) that costs nothing to run, and an irreducible agent-execution half (LLM agents doing real work) that spends money per run. This skill splits verification into those two tiers: exhaustively iterate the free deterministic tier to convergence first, proving every mechanism you can without spending, then do a single subagent-driven paid run to confirm only the agent-execution half. It earns its place because in this session it let the autonomous-dispatch order's routing, filtering, idempotency, and cooldown firing all be proven for $0, leaving exactly one ~10-minute token run for the polecat-commit/refinery-merge half.

## Trigger

- Direct: "verify this live", "test it end-to-end with the token", "does the autonomous flow actually work", any task that pairs *paid agent execution* with a *mechanical control plane*.
- Proactive: whenever a feature's behavior decomposes into (a) a scheduler/router/controller that can be exercised with no model calls, and (b) an LLM-agent step that costs money or wall-clock minutes per run. Especially when the paid run is slow (minutes) and you'll want several iterations.
- Negative: skip when the whole system is one inseparable paid path (no free control-plane to isolate), or when a single cheap run already covers everything.

## Inputs

- The system under test and a way to run it locally (e.g. a `docker compose` stack).
- A means to run the control plane **without** triggering paid agents — typically an empty/blank credential so agents fail auth harmlessly while the controller still schedules, routes, and reports.
- A real credential held in a file, loaded into the environment **without printing it**, for the single paid run.
- Knowledge of which observable signals belong to the free tier (e.g. a routing-metadata field being set) vs the paid tier (e.g. a commit landing, a merge completing).

## Outputs

- A converged free-tier result: the control-plane mechanism proven (routing fires, filter is correct, idempotent, on cadence) at zero cost, iterated until green.
- Exactly one (or very few) paid-tier run(s), ideally driven by a subagent so the orchestrator context stays lean, that confirm only the agent-execution half and then tear the stack down to stop spend.
- A concise timeline tying free-tier and paid-tier evidence together.

## Workflow

1. Decompose the acceptance criterion into a **free tier** (everything observable without paid agents) and a **paid tier** (the irreducible agent work). Write down which signal proves each.
2. Boot the system with the paid credential **blanked** so agents fail auth harmlessly. Confirm the control plane still runs.
3. Iterate the free tier to convergence: trigger the behavior, observe the free-tier signal, fix, repeat. Cover correctness, idempotency, and negative cases (things that must NOT happen). Do this entirely at $0.
4. Only once the free tier is green, load the real credential into the environment from a file **without ever echoing it** (verify presence by length/`grep -c`, not by printing).
5. Run the paid tier **once**, preferably from a background subagent with a bounded brief: create the input, poll for the state transitions, capture the load-bearing evidence (commit hash, final status), then tear the stack down to end spend. Never `sleep`-poll in the orchestrator.
6. Scrub the credential back to a placeholder afterward and confirm no secret/sandbox files are staged for commit.

## Concrete examples

### Example 1: autonomous-dispatch order (this session)

The acceptance criterion was "a plain `gc bd create --rig rig1` reaches `closed`, unattended." Decomposition: free tier = the controller `exec` order routes the bead (`gc.routed_to` gets set), excludes molecule scaffolding, and is idempotent; paid tier = the polecat actually edits+commits and the refinery merges. With a blank token, the order's cooldown auto-routed a created bead to `rig1/gastown.polecat` in ~55s, molecule step-beads were excluded, and a re-run slung nothing — all for $0, iterated until correct. Then one background subagent did the single paid run: auto-route at t+69s → `in_progress` → commit `7a691f9` → refinery merge → `closed`, then `docker compose down -v`. Total paid spend: one ~10-minute run.

### Example 2: a webhook-driven build pipeline (generalization)

A pipeline where a webhook handler routes events to an LLM worker that opens PRs. Free tier: fire synthetic webhooks with auth disabled and assert the router selects the right worker, dedupes repeated deliveries, and respects the cooldown — all without the worker running. Paid tier: enable the worker credential and run one real event end-to-end to confirm the PR is opened. The router bugs (wrong worker, double-fire, missed cooldown) are caught for free; the credential is spent once.

## Anti-patterns

- **Spending tokens to discover a control-plane bug.** In this session the routing filter, the cooldown timing, and idempotency were all controller-side — paying an agent to surface those would have been pure waste. Prove them blank-credential first.
- **Reasoning about the free tier instead of running it.** "The filter should exclude step-beads" is a hypothesis; run a blank-token boot and confirm `gc.routed_to`/`gc.step_ref` actually behave as assumed.
- **Driving the long paid run inline in the orchestrator.** It bloats context and tempts `sleep`-polling. Use a bounded subagent that returns a short timeline and tears down.
- **Leaving the stack (and spend) running after the paid run.** Tear down in the same subagent that started it.
- **Printing the credential to "verify" it.** Verify by length or `grep -c`; never echo the token.

## Acceptance criteria

- [ ] The acceptance criterion is split into an explicitly named free tier and paid tier before any paid run.
- [ ] The free tier is iterated to green at $0 (blanked credential) before the credential is loaded.
- [ ] The paid tier runs the minimum number of times (ideally once), from a bounded subagent that tears the stack down.
- [ ] The credential is loaded without being printed and scrubbed afterward; no secret/sandbox files are committed.
- [ ] The final report ties free-tier and paid-tier evidence into one timeline.

## Files this skill creates / modifies

- (Typically none committed.) It governs *how* verification is run; any scratch env/compose/credential files live outside the repo working tree and are scrubbed/removed when done.
