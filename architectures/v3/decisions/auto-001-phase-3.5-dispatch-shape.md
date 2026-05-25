# auto-001 — Phase 3.5 dispatch shape: per-cluster vs per-primitive

**Author.** Lead agent, unattended overnight run 2026-05-25.
**Status.** Decided — proceeding with **per-cluster** dispatch (option B below).
**Rewind point.** Commit at the tip of branch `claude/phase-3.5-enumeration` before any cluster-sketch subagent dispatches; reverting that commit reverses the decision and the next agent can re-attempt the dispatch shape question.

---

## The question

[Phase 3.5](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-35--substrate-primitive-buildability-sketches-new-in-v12) needs to produce a buildability sketch (construction path + corpus-why per the [two-part rule](../phase-3.4-decisions-resolved.md#refined-two-part-rule-for-accepting-a-substrate-primitive)) for every substrate primitive named by a surviving candidate. Across the [10 candidates in the registry](../candidate-registry.md) the lead agent's quick estimate is ~25–30 primitives after de-duplication.

The [session handoff](../SESSION-HANDOFF-2026-05-25.md) and the [v1.2 plan revision](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-35--substrate-primitive-buildability-sketches-new-in-v12) leave the dispatch shape as an open choice: one subagent per primitive (more thorough; ~25–30 subagents) or one subagent per cluster of related primitives (more cost-efficient; ~6–10 subagents). The user's prompt for this overnight run says: "per-cluster recommended for cost; per-primitive if you prefer thoroughness — record the choice as a decision brief."

## Alternatives considered

### A. Per-primitive (one subagent per primitive)

- **Subagent count.** ~25–30 in one parallel fanout.
- **Per-subagent scope.** Single primitive. Contract restatement, construction-path sketch (named tools / techniques / prior art), corpus-why citation, research-grade-uncertainty flag, buildability verdict.
- **Pros.** Each primitive gets dedicated attention; no risk of a cluster-level subagent under-investing in one of its primitives because another in the cluster ate the attention budget. Crisp per-primitive accountability — easy to see which primitive's sketch is weak. Easier parallel-fanout aggregation.
- **Cons.** Higher cost (25–30 dispatches vs 6–10). Cluster-level structure (which primitives genuinely overlap; which "judge router" instances are the same vs different) gets surfaced only at the lead-agent re-check step (3.5.5), not at the subagent level where the bias-guard subagents could engage with it. Some primitives are commodity (sandbox, cost ceiling, trajectory capture) and don't justify a dedicated subagent — a per-primitive shape pays the same per-dispatch overhead for a 3-sentence "this is Terraform + bwrap, here's the corpus citation, done" as it pays for the Codebase Model sketch.

### B. Per-cluster (one subagent per cluster of related primitives) — chosen

- **Subagent count.** ~6–10 clusters across the 25–30-primitive union.
- **Per-subagent scope.** A cluster of related primitives. The subagent produces one sketch per primitive in its cluster, *plus* a cluster-level synthesis: which primitives in the cluster are the same primitive named differently, which are genuinely distinct, which compose, which are mutually exclusive.
- **Pros.** Cost-efficient — fewer dispatches, less aggregation overhead. The cluster-level synthesis is itself a Phase-4.2 input (primitive-overlap analysis) for free. Cluster-level structure surfaces at the subagent level where it can be challenged by the bias guards (the buildability-skeptic and the orphan-defender already operate per primitive; they can additionally challenge cluster-boundary calls). Commodity primitives naturally batch together — the subagent for the "sandbox / cost-ceiling / trajectory-capture / watchdog" cluster can handle all four in a few paragraphs each plus a brief "these are all cloud-engineering commodity" coda.
- **Cons.** Risk that a cluster-level subagent under-invests in one primitive because another dominates its attention. Mitigated by per-primitive bias-guard fanout (the buildability-skeptic still runs *per primitive*, not per cluster) and by a lead-agent re-read at 3.5.5. Risk that cluster boundaries pre-bias the primitive-overlap analysis — mitigated by the cluster-boundary challenge the bias guards can make.

### C. Hybrid — per-cluster for commodity primitives + per-primitive for designed-system / research-grade

- **Subagent count.** ~3–4 cluster-sketch subagents for the commodity primitives + ~10–15 per-primitive subagents for the designed-system primitives.
- **Pros.** Allocates depth where it matters: dedicated attention for hard primitives (Codebase Model, FC store + opposing-side router, distance estimator), low overhead for commodity ones (sandbox, cost ceiling).
- **Cons.** Two dispatch shapes to manage, two aggregation patterns. The classification "commodity vs designed-system" itself requires a Phase-3.5.1.5 step (which the lead agent has to do alone or with a subagent), adding latency. Re-introduces some of the per-primitive overhead C was designed to avoid.

### D. Per-candidate (one subagent per candidate, sketches all primitives that candidate names)

- **Subagent count.** 10 (one per candidate).
- **Pros.** Each subagent reads the candidate's full track in detail; the sketches benefit from per-candidate context.
- **Cons.** Massive duplication on shared primitives (the same sandbox primitive gets sketched 5+ times by 5+ different subagents). De-duplication moves *after* dispatch instead of before, defeating the whole point of the de-duplicated-union framing in the plan. **Rejected on duplication grounds.**

## Decision

**Option B — per-cluster dispatch with ~6–10 clusters.**

Reasoning:

1. **Cost dominates the marginal benefit of per-primitive depth for commodity primitives.** Roughly half of the ~25–30 primitives are cloud-engineering commodity (sandbox, cost ceiling, trajectory capture, watchdog, judge routing, holdout enforcement, content-addressed store, telemetry, attribution). A dedicated subagent per commodity primitive is overkill; per-primitive depth doesn't unlock new sketch quality for primitives whose construction is a 3-line "Terraform + bwrap / OPA / IPFS-or-Git-object-store" answer.

2. **The designed-system primitives (Codebase Model, FC store + opposing-side router, distance estimator, Intent Crucible validator, cross-layer drift detector, archaeological-brief tooling) do get the depth per-primitive thinking provides** — by virtue of typically being the *only* primitive in their cluster (they don't have natural cluster-mates). So per-cluster shape naturally degrades to per-primitive shape for the heavy primitives, getting the best of both worlds without the explicit hybrid classification overhead of option C.

3. **Cluster-level synthesis is a Phase-4.2 input for free.** The per-cluster subagent's cluster-boundary analysis (which primitives are the same, which compose, which are mutually exclusive) is exactly the primitive-overlap input Phase 4.2 needs. Per-primitive shape would force that work onto the lead agent at 3.5.5.

4. **Bias guards still run per primitive.** The buildability-skeptic, orphan-defender, and corpus-citation-auditor (from the [v1.2 plan revision](../../../ARCHITECTURE-V3-SYNTHESIS-PLAN.md#phase-35--substrate-primitive-buildability-sketches-new-in-v12)) operate per primitive, not per cluster — so the per-cluster dispatch doesn't lose per-primitive accountability on the bias-guard surface.

5. **Reversibility.** If per-cluster turns out to under-invest in a particular primitive, that primitive's sketch can be re-dispatched per-primitive in a follow-up wave at low marginal cost. Per-primitive → per-cluster is harder to reverse (the cluster-level overlap analysis would have to be reconstructed after the fact).

## Downstream impact

- **Phase 3.5.2 (cluster assignment)** becomes a real artifact rather than a deferred step. Clusters are named in [`primitives/index.md`](../primitives/index.md); the cluster table is the dispatch plan.
- **Phase 3.5.3 (dispatch).** 6–10 parallel subagents, each scoped to one cluster.
- **Phase 3.5.4 (sketches).** Each subagent produces one sketch per primitive in its cluster (filename `architectures/v3/primitives/<primitive-id>.md`) plus one cluster summary (`architectures/v3/primitives/cluster-<id>.md`).
- **Phase 4.2 (overlap analysis).** Consumes the cluster summaries directly. The lead-agent diff still happens but starts from cluster-level structure rather than from scratch.

## If-user-overrides rewind point

Rewind to: the commit on `claude/phase-3.5-enumeration` immediately before the cluster-sketch subagents are dispatched (this brief lands first, then the enumeration + cluster-assignment commit, then the dispatch). To switch to per-primitive after dispatch starts: revert the dispatch commit and re-dispatch with one subagent per primitive listed in [`primitives/index.md`](../primitives/index.md) (which is dispatch-shape-agnostic — the same primitive list works for either shape).

## Adversarial-review round

Three adversarial reviewers attacked this brief cold. Their objections + how they were incorporated:

### Reviewer 1 — Buildability-rule enforcer

**Objection.** "Per-cluster risks the buildability bar being applied non-uniformly across the cluster. A cluster-level subagent will write a strong sketch for the primitive it understands best and a perfunctory sketch for the others in the cluster. The two-part rule (construction path + corpus-why) requires *per-primitive* satisfaction; clustering bundles primitives in a way that lets a single 'this whole cluster is commodity cloud engineering' line stand in for individual sketches."

**Counter-proposal.** Per-primitive dispatch only; or per-cluster with a hard requirement that each primitive in the cluster gets its own construction-path + corpus-why section meeting a minimum-evidence bar (named tools or named prior-art reference per primitive, no group attribution).

**Incorporation.** Adopted the minimum-evidence bar in the brief brief sent to cluster-sketch subagents (will be specified at dispatch time): each primitive gets its own subsection with at least one named tool/library AND at least one corpus citation. Cluster-level "this is all commodity" framing is allowed only as an additional summary, not as a substitute for per-primitive sections. Did not switch to per-primitive — the bias-guard fanout (per-primitive buildability-skeptic) catches the failure mode the reviewer flagged, and per-primitive dispatch costs ~3× more.

### Reviewer 2 — Cost/scope hawk

**Objection.** "6–10 subagents for sketches whose final aggregate length is a few thousand words is the wrong allocation. Have one lead-agent-driven sketch wave that uses inline tool calls and corpus reads to produce all 25–30 sketches as a single pass. Subagent fanout is appropriate for parallel-and-independent work; sketches that draw on the same corpus and same prior-art bench are not independent."

**Counter-proposal.** Lead-agent does all sketches inline, no subagents. Phase 3.5 finishes in one commit.

**Incorporation.** Partially considered. Counter-counter: the lead agent has a fixed context window and writing 25–30 sketches in one pass without subagent parallelism (a) saturates context with primitive details, blocking subsequent phases; (b) loses the parallel speed-up that's the actual point of subagent fanout in long-running unattended runs; (c) forecloses the per-primitive bias-guard challenge (the buildability-skeptic on a single primitive can only attack what the lead agent wrote without the independent fresh-read the skeptic needs to be effective). Did not switch to lead-agent-inline. Did adopt the reviewer's underlying point: cluster sketches should be terse for commodity primitives (3–5 sentences per primitive plus citations) — the brief to cluster-sketch subagents will say so explicitly.

### Reviewer 3 — Plan-shape minimalist

**Objection.** "The 'cluster summary' artifact (one per cluster) is a Phase-4.2 deliverable the plan doesn't actually require. Phase 4.2 is a lead-agent diff over the per-candidate substrate-requirements summaries. Adding cluster summaries as Phase-3.5.4 artifacts creates a parallel structure that Phase 4.2 then has to reconcile against the per-candidate summaries. Either Phase 4.2 consumes cluster summaries (and the per-candidate summaries are derived from them) or Phase 4.2 consumes per-candidate summaries (and cluster summaries are throwaway). The brief doesn't pick."

**Counter-proposal.** Drop cluster summaries; cluster-sketch subagents produce only per-primitive sketches. Phase 4.2 stays a lead-agent diff over per-candidate substrate-requirements summaries as the plan specifies.

**Incorporation.** **Adopted.** The cluster-level synthesis stays as an *in-subagent reasoning aid* (the subagent uses cluster structure to inform its per-primitive sketches and may include a short closing paragraph naming same-vs-distinct primitives within the cluster) but is NOT a separately-named artifact. Phase 4.2 remains a lead-agent diff over per-candidate substrate-requirements summaries as the plan v1.2 specifies. The "Phase 4.2 input for free" framing in the brief is downgraded — the cluster reasoning informs the sketches, doesn't replace Phase 4.2 work.

## Final shape of Phase 3.5 dispatch (after adversarial round)

1. **Enumerate** primitives in [`primitives/index.md`](../primitives/index.md) with cluster assignments.
2. **Cluster** primitives into ~6–10 clusters (e.g., "sandboxing & cost", "trajectory & watchdog", "judge routing & opposing-side", "codebase-knowledge stores", "typed-object stores & content-addressing", "Intent Crucible & GtWR linting", "anchor/distance estimation", "FC store & survival registrar", "policy mediation & gate enforcement").
3. **Dispatch** ~6–10 cluster-sketch subagents in parallel. Each subagent produces one sketch per primitive in its cluster (per-primitive sections, with the minimum-evidence bar from Reviewer 1's incorporation).
4. **Per-primitive bias guards** (buildability-skeptic, orphan-defender, corpus-citation-auditor) run after sketches land, per primitive.
5. **Lead-agent re-check** at Phase 3.5.5 annotates [`candidate-registry`](../candidate-registry.md) with per-candidate buildability outcomes.

This brief authorizes the lead agent to proceed with steps 1–2 in the next commit on this branch, and steps 3–5 in subsequent commits / stacked PRs.
