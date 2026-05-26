# ADR 0046: BF-M P-04 PR creator

- **Status**: Accepted
- **Date**: 2026-05-25
- **Deciders**: lead agent (Phase 5 Wave 5.3b BF-M-orphan subagent)

## Context

P-04 is BF-M's terminal substrate primitive: the authenticated egress that publishes a cycle's output as a branch push plus a pull request whose body bundles BF-M's stage-8 structured metadata (change-intent block + archaeological brief + trajectory pointer + acceptance verdict). Per the [P-04 buildability sketch in cluster-C1](../../architectures/v3/primitives/cluster-C1.md#p-04-pr-creator) the contract is: idempotent on `cycle_id`, structured-metadata block machine-readable for cognitive-escrow re-entry per BF-M D-2, F14 per-agent / per-model attribution required in commit messages, and authenticated egress that does not leak credentials into the cycle's P-01 closure.

P-04 is named by [BF-M's primitive list §1](../../architectures/v3/substrate-requirements/bf-m.md#1-primitive-list-buildability-confirmed) as a stage-8 capability ("authenticated branch-push + structured-metadata PR open"). It is a **BF-M orphan** in the Phase-4.2 overlap analysis — no other surviving candidate claims it as a load-bearing substrate primitive at this granularity (BF-S/BF-L absorb PR-opening into their CI tooling; greenfield tracks do not stage-8 against an external forge). Per [auto-005 Round 2 Wave 5.3b dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md), BF-M-orphan primitives that the sketch verdicts `commodity` still get a Phase-5 ADR to record the binding choice, the alternatives, and the cross-references to BF-M's metadata-bundling stack ([ADR 0035 P-24 attribution store](0035-p-24-attribution-store.md), [ADR 0012 P-05 trajectory capture](0012-p-05-trajectory-capture.md), [ADR 0034 P-27 archaeological-brief tooling](0034-p-27-archaeological-brief-tooling.md)).

The forcing failure modes are [F14 attribution collapse](../../architectures/v3/failure-modes-v3.md#f14--attribution-collapse) (widened in Phase 1 to forensic-reconstruction debt — every PR must carry the agent/model authorship that downstream diagnosis joins against P-24's envelope) and [F42 cognitive escrow](../../architectures/v3/failure-modes-v3.md) (the PR body IS BF-M's re-entry surface; if metadata is operator-formatted convention rather than substrate-emitted typed block, [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md) reasserts).

## Decision

**Build P-04 as a thin `gh` CLI wrapper invoked from the BF-M cycle harness, authenticated by a per-cycle GitHub App installation token issued at cycle boot, emitting a structured PR-body block from a typed template.** The harness function `forge.open_pr(worktree_path, cycle_manifest) -> pr_url` runs: (1) `git push origin refs/cycle/<cycle_id>:refs/heads/cycle-<cycle_id>` with the per-cycle token in `GIT_ASKPASS`; (2) `gh pr list --head cycle-<cycle_id> --json url` for idempotency check; (3) `gh pr create --base main --head cycle-<cycle_id> --title "<change-intent summary>" --body-file pr-body.md` (or `gh pr edit` on collision); (4) capture stdout PR URL into the cycle's trajectory record.

The PR body is rendered from a typed Pydantic template with required fields:

- `cycle_id` (opaque to P-04; provided by the cycle manifest)
- `agent_id` and `model_snapshot` (joined against [ADR 0035 P-24 attribution store](0035-p-24-attribution-store.md)'s envelope schema — the same `(agent_id, model_snapshot, cycle_id)` triple P-24 uses, so a reader of the PR can resolve back to the attribution envelope)
- `trajectory_pointer` (an `event_id` / cycle-ID URL into [ADR 0012 P-05 trajectory capture](0012-p-05-trajectory-capture.md)'s store)
- `change_intent_block`, `archaeological_brief_pointer` (rendered or linked from [ADR 0034 P-27 archaeological-brief tooling](0034-p-27-archaeological-brief-tooling.md)'s brief artifact), and `acceptance_verdict` (from stage-7 P-09 replay)

Commit messages on the pushed branch carry the F14 attribution trailers (`Co-Authored-By: factory-agent/<agent_id> <model_snapshot>`) the P-24 ingest worker parses.

Credentials never enter the cycle's P-01 closure. The installation token is held by the harness *outside* the closure; the `git push` and `gh` invocations are harness-side, not agent-side. The token is scoped to `contents:write` + `pull_requests:write` on the target repository only, and expires at cycle teardown. Non-GitHub forges (`glab` for GitLab, `tea` for Gitea) follow the same shape per the sketch's `forge.open_pr(...)` abstraction.

## Alternatives considered

**B. GitHub REST API via a custom HTTP client (no `gh` dependency).** Build the branch push (git smart-HTTP) and `POST /repos/{owner}/{repo}/pulls` directly in the harness. *Why rejected:* reinvents `gh`'s mature auth handling (installation-token refresh on the App token's 1-hour ceiling; rate-limit back-off; primary-vs-secondary rate-limit semantics; redaction in error output) and the marshalling of `--body-file`, idempotency lookup, and PR-edit-on-collision paths. The Phase-3.5 sketch's commodity verdict rests precisely on `gh` doing this work. A custom client is justified only if `gh` is unavailable on the harness host, which is not BF-M's deployment regime (containerised CI runner with `gh` preinstalled is the sketch's stated platform).

**C. Web automation (Playwright / Selenium-driven PR-open through the GitHub web UI).** *Why rejected:* non-deterministic (UI changes break the automation silently; selectors decay), authentication via stored browser session instead of an OIDC-scoped App token (cannot be audited per F14 / F32; cannot be revoked per-cycle), and the structured-metadata block cannot be reliably round-tripped through a textarea without escape-handling bugs. F53 voluntary-discipline fragility reasserts because every selector-break is an operator-patched failure rather than a typed substrate failure.

## Consequences

**Easier:** F14 attribution closure becomes substrate-emitted rather than operator-formatted — the PR body's typed block is the same envelope P-24 reads. F42 cognitive-escrow re-entry surface is a machine-readable artifact the methodology layer consumes without parsing free-form prose. The same `forge.open_pr` abstraction transparently swaps in `glab` / `tea` for non-GitHub deployments; BF-M is not locked to GitHub at the methodology layer.

**Harder:** Per-cycle installation-token issuance requires a GitHub App registered against the target organisation, plus a `actions/create-github-app-token`-equivalent step in the harness boot (one-time ops setup per deployment; documented at architecture-spec time, not here). The PR-body Pydantic schema becomes a versioned artifact whose changes are coordinated with P-24's envelope schema (additive-only, per ADR 0035's rolling-migration prohibition).

**Explicitly NOT promising:** the *semantics* of the change-intent block and the archaeological-brief pointer are BF-M methodology-layer content, not P-04 content — P-04 only guarantees the fields are present, well-typed, and machine-readable. The brief-quality calibration partial-RG ([substrate-requirements §2](../../architectures/v3/substrate-requirements/bf-m.md#2-rg-primitives)) lives on P-27, not P-04.

## References

- [P-04 buildability sketch in cluster-C1](../../architectures/v3/primitives/cluster-C1.md#p-04-pr-creator) — contract, construction path, commodity verdict
- [BF-M substrate requirements §1 (P-04 row) and §3 contracts](../../architectures/v3/substrate-requirements/bf-m.md#1-primitive-list-buildability-confirmed)
- [BF-M track stage 8 "Ship-or-escalate"](../../architectures/v3/tracks/brownfield-methodology-first.md) — the PR body's metadata bundle and F42 cognitive-escrow re-entry surface
- [F14 attribution collapse](../../architectures/v3/failure-modes-v3.md#f14--attribution-collapse), [F42 cognitive escrow](../../architectures/v3/failure-modes-v3.md), [F53 voluntary-discipline fragility](../../architectures/v3/failure-modes-v3.md)
- [ADR 0035: P-24 attribution store](0035-p-24-attribution-store.md) — `(agent_id, model_snapshot, cycle_id)` envelope schema the PR body mirrors
- [ADR 0012: P-05 trajectory capture](0012-p-05-trajectory-capture.md) — trajectory-pointer target
- [ADR 0034: P-27 archaeological-brief tooling](0034-p-27-archaeological-brief-tooling.md) — archaeological-brief artifact referenced from the PR body
- [auto-005 Round 2 Phase-5 dispatch shape](../../architectures/v3/decisions/auto-005-phase-5-dispatch-shape.md) — Wave 5.3b BF-M-orphan ADR scope
