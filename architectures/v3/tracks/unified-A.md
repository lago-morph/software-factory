---
track: unified-no-axis-A
axis: risk-tier-as-primary (blast-radius × reversibility, mandate-derived)
mandate-scope: both
based-on-commit: 9a205b6
based-on-date: 2026-05-24
---

# Unified Track A — Risk-Tier-as-Primary

A single architecture for both greenfield and brownfield mandates, organized around **per-work-item risk tier** (blast radius × reversibility × Kahana-RSI exposure), not around mandate. Mandate is a *derived attribute* of a work item: it shifts which substrate primitives feed the item, but does not change the architecture's organizing principle.

This track is **strong on the unified case**, not strong on either mandate individually. The bet is that the corpus' empirical anchors converge on risk-tier as the variable that actually drives regime/gates/judge-architecture/escrow choices — and that mandate is a *covariate* of risk-tier rather than its peer.

---

## §0 — Axis declaration, glossary, defense, pre-response

### 0.1 Axis declaration (one sentence)

**Every work item the factory accepts is classified into a `risk-tier ∈ {T0-sandbox, T1-recoverable, T2-rollback, T3-production-scissors, T4-RSI-exposed}` before any other architectural decision is made; the tier — not the mandate — determines the regime, the judge architecture, the cost ceiling, the escrow shape, the V&V depth, and the watchdog cadence.**

### 0.2 Glossary (this track's vocabulary)

| Term | Definition (in this track) |
|---|---|
| **Risk-tier** | Discrete classification of a work item by blast radius × reversibility × Kahana-RSI exposure. Five tiers (T0–T4). Stable across mandates. |
| **Blast radius** | Maximum surface area a failed execution can affect: sandbox-only / local-repo / merged-PR / shipped-artifact / production-data. |
| **Reversibility** | Cost to undo a successful but wrong execution: trivial / git-revert / rollback-deploy / data-restore / unrecoverable. |
| **RSI-exposed** | Per Kahana ([report 31](../../../research/31-caremark-rsi-board-exposure.md)): work item meets RSI three-part test (durable + compounding + limited-gating). Forces T4 regardless of blast radius. |
| **Regime** | Per glossary §0: L3-Augmentation / L4-lights-out-with-policy / L5-dark-factory. In this track, regime is a *function of tier*, not a top-level architectural choice. |
| **Tier-classifier** | The substrate primitive that takes a work item (issue, spec-diff, refactor request, cold-start prompt, regression report) and emits its tier. Itself L3-Augmentation-only (humans review classifier output for tier ≥ T3). |
| **Tier-overlay** | The per-tier configuration of (cost ceiling, judge count, judge-model diversity, watchdog cadence, escrow design, V&V depth, post-merge sample-audit rate). |
| **Mandate-feed** | Per-tier substrate primitive that injects greenfield-specific or brownfield-specific inputs (cold-start priors vs. codebase archaeology) without changing the regime. |

### 0.3 Defense: why risk-tier is the right primary axis for a unified architecture

Four corpus-grounded reasons:

1. **The empirical anchors that contest UC1 lights-out are tier-shaped, not mandate-shaped.** [CodeRabbit 1.4× / Veracode 45% / METR 19%](../failure-modes-v3.md#f1--hallucination-loop) (per [report 09](../../../research/09-jaymin-book-harnesses-practices-mental-models.md) §7) and the Replit DB wipe ([followup 10](../../../research/followup/10-governance.md), [F56](../failure-modes-v3.md#f56--guardrail-bypass-under-stress-replit-class-incident)) all bite at the *production-scissors* boundary — not at "greenfield vs. brownfield." Jaymin's own Ch 9 §2c statement that L5-for-brownfield ceilings at ~L3 ([CTR-A5](../contradictions.md#ctr-a5--jaymins-brownfield-ceiling-vs-mandate-agnostic-v2-stance)) is a *risk* claim disguised as a mandate claim: brownfield ceilings lower because brownfield work has higher default tier (production proximity, [F12/F33/F44](../failure-modes-v3.md#f12--lethal-trifecta--prompt-injection) cascade).

2. **Shapiro's R3 ("do not give it production scissors", [report 32](../../../research/32-shapiro-completion-chat-agent-claw.md) §8.2; [F44](../failure-modes-v3.md#f44--lethal-trifecta-production-scissors-default)) is a tier rule, not a mandate rule.** A greenfield Claw that deploys to live infra has the same scissors as a brownfield one. The corpus' single most-cited hardening rule is tier-indexed.

3. **Kahana's RSI three-part test ([report 31](../../../research/31-caremark-rsi-board-exposure.md)) is mandate-agnostic.** A greenfield factory that self-improves over many cycles meets the test; a brownfield factory that only does single-cycle regression-fixes against frozen specs does not. The board-exposure question is about durability + compounding + gating — all tier-axis concepts. F43 (RSI Board-Visibility Gap), F54 (Goal subversion), F55 (Behavioural drift) are all RSI-class failures the *tier* classifier must surface.

4. **Brier's pace-layers ([followup 12](../../../research/followup/12-brier-pace-layers.md)) is dialectically close but wrong organising axis for this track.** Brier organizes by *artifact pace* (code-fast / standards-slow); we organize by *blast radius / reversibility of the cycle's effect*. The two axes are orthogonal-but-related: a slow-pace-layer change (architecture, standards) tends to be high-tier *because* it propagates. We borrow Brier's "patterns sift downward" as a tier-graduation mechanism (T0 successes graduate to T1 templates, T1 patterns sift into T2 standards) but reject pace-layer as the primary organising frame because it does not directly index the lights-out/L5 tension (CTR-A4) — risk-tier does.

### 0.4 Pre-response to the Phase-3 unified-mandate-attacker

The strongest attack on this architecture, I expect, will target **greenfield cold-start**: *"At day 0, every work item is novel, unmeasured, and irreversible (you can't 'roll back' the founding spec); the tier classifier has no information to classify on; risk-tier collapses to 'everything is T3+' and the architecture degenerates into a single-tier shape that is just 'cautious greenfield'."*

Pre-response: this is correct **for the first ~5 cycles**, and the architecture leans into it rather than denying it. The cold-start regime is **explicitly tier-pinned to T2 (rollback) for the bootstrap window** (§5 below) with reduced parallelism, mandatory dual-model judge ([F46](../failure-modes-v3.md#f46--single-model-review-blindspot)), and an enforced escrow interval ([F42](../failure-modes-v3.md#f42--cognitive-escrow-negligence)) for every cycle. Cold-start *graduates* into the multi-tier shape as the tier classifier's training data (per-cycle outcomes + judge verdicts + post-merge sample-audit results) accumulates. The graduation criterion is itself a substrate primitive (§3.4) with a corpus-grounded threshold from Jaymin's K=5 ≥70% Augmentation bar applied to the classifier itself, not to the agents. This is not handwaving: it's the same trajectory-capture mechanism the substrate already uses for D-7, repurposed as classifier-training signal.

The secondary attack I expect: *"brownfield never reaches T0 (the codebase is always production-adjacent), so half your tiers go unused on the brownfield side — that's not 'unified', that's 'brownfield always operates in tiers 2–4'."* Pre-response: this is descriptively true and a *feature*. The architecture **does not require every tier to be used on every mandate**; it requires that *the same classifier, with the same primitives, with the same tier-overlay protocol, operate on both mandates*. The tier *distribution* differs; the tier *mechanism* does not. The mandate-fit YAML (§7) captures the distribution-difference per-work-unit-class.

A third attack — *"this is just D2 in different clothing; it conflates 'risk-tier' with 'work-unit-class'"* — I address in §1.4 by showing the two axes cross-cut: a `refactor` work-unit-class can be T0 (test-only refactor, sandbox) or T3 (production schema migration), so tier ≠ class.

---

## §1 — Architectural shape

### 1.1 Substrate (mandate-agnostic, tier-aware)

The substrate is a **tier-classifier + tier-overlay matrix + mandate-feed adapters**. Concretely:

- **Tier-classifier** (substrate primitive). A deterministic + LLM-judge hybrid that scores each work item on blast-radius (5-point: sandbox/local/PR/shipped/prod-data) × reversibility (5-point: trivial/revert/rollback/restore/unrecoverable) × RSI-exposure (binary, Kahana three-part test). Emits T0..T4 and a confidence value. RSI-exposed always pins to T4. Confidence below threshold → escalate to human-in-classifier-loop (NOT human-in-cycle-loop). Anchored on: [report 31](../../../research/31-caremark-rsi-board-exposure.md) RSI test; [F44](../failure-modes-v3.md#f44--lethal-trifecta-production-scissors-default) hardening rules; [F57](../failure-modes-v3.md#f57--design-authority-erosion-convenience-reclassifies-stakes) (convenience reclassifies stakes — directly addressed because the classifier's tier-emit is an audited substrate event, not an implicit operator judgment).

- **Tier-overlay matrix** (substrate primitive). For each tier, a fixed bundle:
  - T0: 1 builder, 0 judges (substrate-deterministic gates only), $0.50 cost ceiling, watchdog-Daemon-only, no escrow.
  - T1: 1 builder + 1 same-model judge, $5 ceiling, Daemon+Triage watchdog, escrow = 30s.
  - T2: 1 builder + 2 cross-model judges (kevin/carl per [F46](../failure-modes-v3.md#f46--single-model-review-blindspot)), $50 ceiling, full Daemon/Triage/Patrol, escrow = 2min with re-engagement prompt.
  - T3: 1 builder + 3 cross-model judges + deterministic perimeter (CaMeL-class typed boundary per [followup 08](../../../research/followup/08-security-primitives.md)), $500 ceiling, Patrol+human-escalation, escrow = 10min, mandatory dry-run.
  - T4: All-of-T3 + Kahana three-control package (AILCCP Human Approval Gate / sandboxing / immutable logging per [report 31](../../../research/31-caremark-rsi-board-exposure.md)), cost uncapped (governance-supervised), Patrol→Board reporting per [F43](../failure-modes-v3.md#f43--rsi-board-visibility-gap), pre-action human authorization required.

  This is **not** "augmentation vs automation" as a binary (per Jaymin) but a **5-tier graded escalation** where the agent autonomy budget drops monotonically with tier. T0 is full Automation. T4 is Augmentation-with-Approval. T1–T3 are graded.

- **Mandate-feed adapters** (substrate primitives). Two adapters that inject mandate-specific inputs into a work item *before* tier-classification:
  - `greenfield-feed`: connects to cold-start substrate (§5) — adjacent-domain priors, exemplar projects, library docs, operator knowledge, [report 25](../../../research/25-requirements-engineering-foundations.md) GtWR scaffolds, [report 14](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) intent-block templates.
  - `brownfield-feed`: connects to codebase archaeology — git history, runtime traces, test suite, dependency graph, production telemetry, existing CLAUDE.md/AGENTS.md.

  Both feed into the same downstream pipeline; they are interchangeable at the work-item-input boundary. This is the heart of the unified claim: **the same tier-classifier + tier-overlay matrix operates on output from either feed**.

- **Shared substrate primitives** (mandate-agnostic, tier-agnostic, the "always on" layer): trajectory capture (D-7, [report 11](../../../research/11-openhands-substrate-audit.md) sub-ms persist anchor); cost-ceiling enforcement (D-5); tiered watchdog Daemon/Triage/Patrol (D-6); secret store; sandbox; OTEL five-event export ([report 18](../../../research/18-openai-codex-substrate.md)); `.rules` Starlark DSL for auditable V&V auto-rejection; deterministic perimeter (CaMeL, [followup 08](../../../research/followup/08-security-primitives.md)); coordination via git+GitHub-issues per CTR-C7 (NOT mail bus).

### 1.2 Methodology (thin overlay; per-tier, mandate-aware via feeds)

Per Round-2's substrate-heavy/thin-methodology framing ([CTR-C2](../contradictions.md#ctr-c2--substrate-heavy--thin-methodology-round-2-framing-vs-methodology-dominates-uc4-hypothesis)) — which UC4 contests — this track sides with substrate-heavy: methodology is a **per-tier playbook** rather than a per-mandate methodology. The playbook is:

1. Work item enters via a mandate-feed.
2. Tier-classifier emits tier + confidence.
3. Tier-overlay matrix configures the cycle (builder count, judge count, model diversity, cost ceiling, watchdog cadence, escrow shape, gates).
4. Cycle runs with the configured overlay.
5. Post-cycle: trajectory archived; outcome scored; sample-audit at tier-indexed rate (T0: 0%; T1: 1%; T2: 5%; T3: 25%; T4: 100%).
6. Audit results feed back into the tier-classifier as training signal (substrate-level "compounding" per F35-aware governance).

The corpus methodology shapes — Compound Engineering ([report 03](../../../research/03-every-compound-engineering.md)), Attractor pipelines ([report 02](../../../research/02-strongdm-attractor.md)), Refinery layered-spec, Tournament populations — are **available as tier-overlay choices** rather than competing top-level architectures:

- T0 work uses Attractor-style `.dot` pipelines for cheap parallelism.
- T1 work uses Compound-Engineering-style issue-queue-with-skills.
- T2 work uses Refinery-style layered spec with explicit gates.
- T3 work uses Tournament-style population-with-cross-model-diversity (F46 mitigation as architecture, per [CTR-D4](../contradictions.md#ctr-d4--f1-hallucination-loop--substrate-mitigable-vs-architecture-mitigable)).
- T4 work uses Council-style multi-agent panel with mandatory human-final-approval ([report 16](../../../research/16-el-kaim-book-council-and-delegation.md)).

This makes the v2 architecture set a **menu of tier-overlay choices**, not a competing set. The Phase-7 back-fill audit will find this favourable: most v2 architectures absorb as tier-overlays.

### 1.3 Engagement with CTR-A4 (lights-out↔L5 vocabulary mapping)

This track's resolution of CTR-A4 is **option (b)+(c) from brief §2.1**: lights-out is redefined *over a defined risk-tier surface* (T0–T2), with T3 being lights-out-with-immutable-logging-and-board-visibility and T4 being explicitly human-in-loop. The vocabulary mapping is:

- **Lights-out (UC1)** = the *operating mode for T0–T2*, where no human is in the per-cycle inner loop.
- **L4 (Shapiro "I'm here")** = the *operating mode for T3*, where the human is at the policy boundary with sample-audit and escalation.
- **L5 (Jaymin's empirical anti-pattern)** = the *forbidden regime for T4*, and the *contested regime for T3*. We do not claim L5 anywhere except T0/T1 (which Jaymin's anti-pattern critique does not actually attack — CodeRabbit/Veracode/METR all measure at T2+ analogues).

This dissolves CTR-A1 (L5-target vs. L5-anti-pattern) by **never running L5 at tier ≥ T2**. CTR-A5 (Jaymin's brownfield L3 ceiling) becomes a *tier-distribution claim*, not a mandate-ceiling claim: brownfield has more high-tier work, so the brownfield empirical ceiling looks like L3 in *aggregate* because most brownfield work runs at T2 (which is L4 + cross-model judge), not because brownfield is structurally L3-capped.

### 1.4 Engagement with D2 (work-unit-class) — risk-tier is orthogonal, not redundant

D2's work-unit-class taxonomy (`initial-spec / refactor / mvp / post-mvp-evolution / regression-fix`) describes *what kind of work the cycle does*. Risk-tier describes *what happens if the cycle gets it wrong*. They cross-cut:

| Work-unit-class \ Risk-tier | T0 sandbox | T1 recoverable | T2 rollback | T3 prod-scissors | T4 RSI |
|---|---|---|---|---|---|
| initial-spec | greenfield-cold-start | spec-refinement | spec-with-implications | spec-with-customer-promise | spec-with-RSI-exposure |
| refactor | test-only refactor | local module refactor | cross-module refactor | schema/API breaking refactor | RSI-class refactor |
| mvp | sandbox prototype | demo MVP | beta MVP | shipped MVP | RSI-class MVP |
| post-mvp-evolution | A/B experiment | feature add | breaking change | data-migration evolution | RSI-class evolution |
| regression-fix | test-only fix | local fix | merged fix | hotfix-to-prod | RSI-class regression |

Every cell is reachable; tier is not derivable from class alone. The mandate-fit YAML in §7 expresses per-(class × tier × mandate) coverage.

---

## §2 — Engagement with MISSED-3 (El Kaim 9-field intent vs. UC4 spec-malleable)

This is the contradiction at the heart of whether unified architecture is possible. My reconciliation:

The 9-field intent block ([report 14](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) §4.1) and UC4 spec-malleability are **operating at different tiers**. El Kaim's `invariants` ("non-negotiable conditions any valid realization must preserve") is a **T3/T4 substrate primitive**: it is exactly what you write when the work item is production-scissors-class or RSI-class, because the cost of getting it wrong forecloses your ability to revise. UC4's spec-malleability is a **T0/T1 methodology default**: the spec moves freely during cold-start because nothing irreversible has happened yet.

Concretely: greenfield cold-start at T2 (rollback) runs *spec-malleable on the spec body* but *intent-block-stable on the invariants*. As cycles graduate from T0→T2→T3, the invariant set grows monotonically (this is enforced by the substrate; invariants are append-only after T3 entry). The spec body remains malleable across the invariant set. This **reconciles UC4 and El Kaim by tiering the malleability**: not "spec is malleable" vs. "spec is fixed" — but "spec body is tier-graded for malleability; invariants ratchet with tier".

This is *not* a hand-wave because:

- It is testable: a T3 work item with a freshly-changed invariant is a substrate violation, auditable in trajectory.
- It uses an existing primitive (the El Kaim 9-field block) rather than inventing one.
- It honors UC4 by preserving malleability where the user's claim applies (low-tier early-cycle work) and El Kaim where his applies (high-tier downstream work).

CTR-B6 dissolves under this reading; CTR-B7 (Brier vs. Nystrom on spec velocity) also dissolves — spec velocity is tier-indexed: high at T0 (Nystrom's "spec git-history is the changelog" regime), low at T4 (Brier's pace-layer 3 stability regime).

---

## §3 — Substrate primitives (re-derived from scratch per D3-style discipline)

This track's substrate primitive list (re-derived, not inherited from Round-2):

1. **Trajectory capture** (D-7 retained; [report 11](../../../research/11-openhands-substrate-audit.md) measurement anchor). Mandate-agnostic, tier-agnostic.
2. **Tier-classifier** (new; this track's central primitive). Discussed §1.1.
3. **Tier-overlay matrix** (new). Discussed §1.1.
4. **Mandate-feed adapters** (new). Discussed §1.1.
5. **Tiered watchdog** (D-6 retained, [report 13 / Overstory](../../../archive/synthesis-v1-v2/13-round-2-synthesis.md) heritage; cadence is now tier-indexed not architecture-indexed).
6. **Cost ceiling** (D-5 retained; ceiling is tier-indexed).
7. **Deterministic perimeter** (CaMeL, [followup 08](../../../research/followup/08-security-primitives.md)); always on at T2+; closes [F12](../failure-modes-v3.md#f12--lethal-trifecta--prompt-injection) per CaMeL guarantees.
8. **Cross-model judge router** (new framing of RouterLLM but reframed; resolves [CTR-C4](../contradictions.md#ctr-c4--routerllm-as-substrate-primitive-vs-provider-aligned-profiles-do-not-unify) by *requiring* model-family diversity at T2+ and *permitting* provider-aligned profiles at T0/T1 — the contradiction was unforced because the corpus was reading it as one-size-fits-all).
9. **Scaffold-as-substrate** ([report 04](../../../research/04-every-skill-libraries.md), [report 23](../../../research/23-anthropic-engineering-trilogy.md)); SKILL.md / AGENTS.md / CLAUDE.md. Per [CTR-C6](../contradictions.md#ctr-c6--scaffold-as-load-bearing-jaymin-book-vs-scaffold-as-anti-pattern-jaymin-manifesto) and its Phase-1 bias-guard sharpening (bitter-lesson vs. scaffold-substrate cleavage), this track takes the **scaffold-substrate side** because the tier-overlay matrix is itself scaffold (a per-tier YAML the substrate reads). The bitter-lesson position (Jaymin Manifesto + Gas City) is rejected on the corpus-internal evidence that Anthropic Skills + OpenAI Codex + Every SKILL.md + El Kaim Codex all ship scaffold-substrate; the bitter-lesson camp has one practitioner (Jaymin himself, contradicting his own book) and one substrate vendor (Gas City) on its side.
10. **Cognitive-escrow primitive** ([report 30](../../../research/30-cognitive-escrow.md); [F42](../failure-modes-v3.md#f42--cognitive-escrow-negligence); [F53](../failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class)). The interval is tier-indexed: longer escrow at higher tier, with re-engagement prompts substrate-triggered (not operator-voluntary, addressing F53).
11. **Knowledge-store with `discovered-from` edges** ([report 38](../../../research/38-gas-systems-substrate.md) Beads primitive). Per-tier write/read policies: T0 writes go to a sandboxed ephemeral store; T2+ writes go to the durable store; T4 writes require human approval. Addresses [CTR-H2](../contradictions.md#ctr-h2--knowledge-eagerly-captured-compound-vs-lazily-logged-cxdb) by tiering the eagerness.
12. **Coordination medium = git+GitHub-issues** (per [CTR-C7](../contradictions.md#ctr-c7--coordination-medium-mail-bus-overstory-vs-github-issues-as-coordination-ci-friendly-translation) resolution). Mail bus rejected.
13. **OTEL five-event export + AI security-triage agent** ([report 18](../../../research/18-openai-codex-substrate.md)). Always on; events tier-tagged.
14. **`.rules` Starlark DSL for auditable V&V auto-rejection** ([report 18](../../../research/18-openai-codex-substrate.md)). Always on; rules are tier-indexed.
15. **AILCCP three controls** (Human Approval Gate / sandboxing / immutable logging; [report 31](../../../research/31-caremark-rsi-board-exposure.md); [followup 10](../../../research/followup/10-governance.md)). Conditional on T4.
16. **Sample-audit rate scheduler** (new). Tier-indexed: 0/1/5/25/100%.

**What dropped from Round-2's list**: mail-bus coordination (replaced); Overstory `AgentRuntime` weakest-link framing (replaced by tier-overlay; the substrate's safety floor is set per-tier, not by adapter); RouterLLM as monolithic primitive (refined to tier-conditional cross-model router).

---

## §4 — §4 defaults: accepted vs. challenged

Per D3 mandatory marking, every default:

- **D-1 (Specs are durable, version-controlled, human-curated):** **`accepted with justification`** — but with the tier-graded reconciliation in §2. The spec body is malleable at T0–T1; the invariant block ratchets with tier. The Nystrom spec-git-history-as-changelog framing ([report 35](../../../research/35-lenny-howiai-spec-driven-and-team-ops.md)) is the operating shape at T0–T2; the Brier pace-layer-3 stability framing ([followup 12](../../../research/followup/12-brier-pace-layers.md)) is the operating shape at T3–T4.

- **D-2 (Scenarios live outside the codebase as a holdout set):** **`challenged`** — per [CTR-B5](../contradictions.md#ctr-b5--scenarios-live-outside-the-codebase-round-1-d-2-vs-brownfield-scenarios-live-inside-fragile-default-flag) and its Phase-1 sharpening (StrongDM's own "Tokens are the fuel" page includes incident replays + agentic simulation — necessarily inside/generated-from-runtime). This track holds scenarios in a **tier-indexed location**: T0 scenarios are inline test-only; T1 scenarios live in the codebase (test suite, runtime traces, brownfield-feed); T2+ scenarios live outside the codebase as substrate-enforced holdouts (D-4 holdout discipline preserved at T2+). The "outside vs inside" is not a single answer — it's a tier rule. This is *not* mandate-derived; greenfield T2+ work also uses out-of-tree holdouts (because by T2 a greenfield system has output worth holding out).

- **D-3 (Agent = Model + Harness):** **`challenged` — partial**. Accepted at T0–T2 where single-agent cycles dominate. Challenged at T3–T4 where the cycle is shaped as a Tournament-style population (CTR-C1; D-3 fragile-default flag) or a Council-style graph. Per [CTR-C10](../contradictions.md#ctr-c10--report-37-portuguese-vs-english-language-effect-on-policy-vs-routerllm-provider-agnosticism-missed-8) and report 37's empirical anchor, "Agent = Model + Harness + Natural-Language-Register" is more accurate at T3+; the natural-language register of prompts is a substrate-modeled parameter for high-tier work (substrate logs prompt-language as a first-class OTEL event field). Vocabulary update accepted from CTR-C10.

- **D-4 (Holdout discipline is substrate-enforced):** **`accepted with justification`** at T2+; trivially satisfied at T0–T1 because the cost of leakage is bounded by the tier's blast radius.

- **D-5 (Hard cost ceilings non-optional in CI):** **`accepted with justification`** — ceilings are tier-indexed per §3 primitive 6. Per [CTR-E1](../contradictions.md#ctr-e1--token-spend-per-engineer--cherny-100kmonth-vs-independent-5005000day) (Cherny $100K/month vs. independent $500/day variance), the 10× variance is *explained* by tier-distribution: high-tier work dominates Cherny's number, low-tier work dominates independents'. Validates the tier-indexed ceiling.

- **D-6 (Tiered watchdog Daemon/Triage/Patrol is substrate primitive):** **`accepted with justification`** — and the watchdog's per-tier cadence is itself a substrate parameter. T0 = Daemon only; T1 adds Triage; T2 adds Patrol; T3 adds human-escalation; T4 adds board-reporting per [F43](../failure-modes-v3.md#f43--rsi-board-visibility-gap).

- **D-7 (Trajectory capture is cheap and production-tested):** **`accepted with justification`** — [report 11](../../../research/11-openhands-substrate-audit.md) sub-ms-per-event anchor stands; trajectory is the training-data source for the tier-classifier and the sample-audit feedback loop.

---

## §5 — Cold-start (mandatory per brief §5)

Cold-start is a *first-class greenfield concern* in this track, addressed structurally rather than punted.

### 5.1 Day-0 state

On day 0, the factory has:
- The `greenfield-feed` adapter pre-loaded with: adjacent-domain priors (operator-supplied); exemplar projects (operator-curated); library docs (Context7-class); operator knowledge (CLAUDE.md / AGENTS.md hand-authored); [report 25](../../../research/25-requirements-engineering-foundations.md) GtWR R1–R42 lint rules; [report 14](../../../research/14-el-kaim-book-intent-and-spec-authorship.md) 9-field intent-block templates; [report 26](../../../research/26-prompt-underspecification-academic.md) Yang/Larbi contradictory-prompt detector.
- The tier-classifier in **bootstrap mode**: every work item pinned to T2 regardless of classifier output, for the bootstrap window (default 5 cycles or until 3 successful T2 cycles, whichever first).
- The tier-overlay matrix configured for T2 as above (2 cross-model judges, $50 ceiling, full watchdog, 2min escrow with re-engagement prompt).

### 5.2 Bootstrap protection against silent failure

The bootstrap regime explicitly addresses the "no track record yet to evaluate against" problem (brief §5.2) by:

- **Mandatory dual-model judging** at every cycle ([F46](../failure-modes-v3.md#f46--single-model-review-blindspot)). At least one judge must be from a different model family than the builder (CTR-C4 resolution per §3 primitive 8). Husain/Shankar's "same-model-different-task judges are fine" finding ([CTR-D7](../contradictions.md#ctr-d7--anthropic-single-judge-finding-vs-ctr-d4-cross-model-critic-framing-missed-1)) is rejected for cold-start specifically — the bootstrap regime cannot rely on alignment-with-human metric because there are no per-prior-cycle human alignments to measure against. After bootstrap, T0/T1 work permits same-model judges per Husain/Shankar.
- **Contradictory-prompt detector mandatory** ([F37](../failure-modes-v3.md#f37--silent-contradictory-prompt-collapse); [report 26](../../../research/26-prompt-underspecification-academic.md)). Larbi's 73.8%→6.7% collapse is exactly the cold-start failure mode — the spec is being authored under conditions where contradictions are hardest to spot.
- **Vocabulary lint** ([F38](../failure-modes-v3.md#f38--vocabulary-lint-debt); [report 25](../../../research/25-requirements-engineering-foundations.md) GtWR R7/R8/R9). Substrate-deterministic; cheap.
- **Region-vs-point spec check** ([F39](../failure-modes-v3.md#f39--point-spec--region-mismatch); INCOSE Complexity Primer principle 12). LLM-judge applied to spec shape, not content.
- **AILCCP Human Approval Gate** ([followup 10](../../../research/followup/10-governance.md)) required for all bootstrap-window merges. Yes, this means cold-start is not lights-out for the first 5 cycles. **This is the point.** Per [F58](../failure-modes-v3.md#f58--runtimedesign-time-compliance-split) and Kahana's RSI failure modes, "lights-out from day 0" is not achievable structurally for novel work; the architecture admits this rather than papering over it.
- **Cognitive-escrow re-engagement prompts** ([report 30](../../../research/30-cognitive-escrow.md); [F42](../failure-modes-v3.md#f42--cognitive-escrow-negligence)) every cycle during bootstrap, with the substrate-triggered escrow design addressing [F53](../failure-modes-v3.md#f53--voluntary-discipline-fragility-kahana-fragile-dependency-class) (Kahana fragile-dependency class).

### 5.3 Trajectory from day 0 → day N (graduation)

- **Day 0–5 (bootstrap):** All work pinned T2. Human approval gate on all merges. Tier-classifier emits tiers but they are advisory (recorded for training, not used for routing).
- **Day 5–~30 (early-steady-state):** Tier-classifier outputs become operational at T0/T1 (low-stakes work routes around the gate). T2+ work still requires gate. Sample-audit at 100% for all merges to populate classifier training data.
- **Day ~30+ (steady-state):** Full tier-overlay matrix operational. Sample-audit rates drop to per-tier targets. Classifier confidence threshold relaxes as training data accumulates. Lights-out on T0/T1; L4-with-policy on T2; L4-with-audit on T3; Augmentation-with-Approval on T4.

The graduation criterion uses Jaymin's K=5 ≥70% Augmentation bar applied to **the classifier** (not the builder agents): the classifier must agree with itself across K=5 re-classifications on ≥70% of work items before its outputs become operational. This is the corpus-grounded threshold; it can be tightened to ≥90% (Automation Mode bar) per architecture choice and OQ-B6 (open).

### 5.4 What cold-start is NOT in this track

Cold-start is *not* a separate architecture or a separate mandate. It is **a temporally-bounded regime of the unified architecture** in which the tier-classifier is in bootstrap mode and all work is T2-pinned. The substrate primitives, the methodology overlays, the failure-mode mitigations, the escrow shape — all are the same primitives that operate at steady state, just configured for the bootstrap regime.

This addresses CTR-G3 (cold-start vs. legacy-ingestion symmetry): legacy-ingestion is the *brownfield-feed analog* of cold-start, and it gets the same bootstrap regime (T2 pin) for the first N cycles, with the bootstrap window calibrated against codebase-archaeology-confidence rather than against prior-cycle count. The symmetry CTR-G3 surfaces is *real* and structurally encoded.

---

## §6 — Failure-mode coverage (summary)

| F-mode | Tier where it bites | Mitigation primitive | Mandate divergence |
|---|---|---|---|
| F1 Hallucination Loop | T2+ critical | Cross-model judge router (§3-8) | Same primitive; brownfield's existing tests reduce severity at T1 |
| F2 Reward hacking | T2+ high | `.rules` DSL auto-rejection + holdout (D-4) | Same |
| F9 Spec overfitting | T0–T1 critical (greenfield) | Tier-graded invariant ratchet (§2) | Greenfield-acute at low tier; brownfield-rare |
| F12/F33/F44 Lethal-trifecta cascade | T3+ critical | Deterministic perimeter (CaMeL) + R3 production-scissors-off-by-default | Brownfield reaches T3 faster |
| F20 Maintenance vs. greenfield asymmetry | n/a as F-mode | Mandate-feed adapter design | Mandate-feed exists per-mandate; this *is* the architectural answer |
| F27 Circularity | T2+ high | Cross-model + Tournament-as-T3-overlay | Same |
| F40 Last-Mile Drift | T3+ critical (greenfield) | Tier T3 mandatory dry-run + sample-audit 25% | Greenfield-acute |
| F42/F53 Escrow + voluntary-discipline | All tiers, T2+ critical | Substrate-triggered escrow with re-engagement prompts | Same |
| F46 Single-model review blindspot | T2+ critical | Cross-model judge router | Same |
| F52 Tempting-Wrong-Hybrid | T0–T1 wrap-temptation | Tier-overlay forces minimum-viable wrapping; over-wrapping audited as substrate violation | Same |
| F54 Goal subversion | T2+ critical | OTEL goal-frame logging + Patrol cross-cycle goal-drift detection | Brownfield-acute (issue queue is the vector) |
| F55 Behavioural drift | T2+ critical | Mandate-feed external-anchor injection every N cycles | Greenfield-critical (no other anchor) |
| F56 Replit-class guardrail bypass | T3+ critical | AILCCP Human Approval Gate at T3+; substrate-default production-scissors-off | Brownfield-canonical |
| F58 Runtime/design-time compliance split | T3+ critical | Runtime OTEL events as continuous-conformance evidence | Brownfield-acute |
| F60 Parallel-cycle compounding | T1–T2 high | Tier-indexed parallelism cap (T0 unlimited; T1 = 8; T2 = 4; T3 = 1; T4 = 1) | Brownfield-acute (Stripe/Cherny scale) |

The pattern: most F-modes are addressed by *tier-graded* mitigation that costs more at higher tier and is free at lower tier. This is precisely the "substrate is cheap" thesis being honest about its cost ([CTR-E6](../contradictions.md#ctr-e6--camel-7-point-utility-tax-empirics-vs-lights-out-cost--output-framing-missed-9), CaMeL 7-point utility tax): substrate is cheap at low tiers because most primitives are inactive; substrate gets expensive at high tiers because more primitives engage. The tier-overlay matrix surfaces the cost-vs-safety tradeoff explicitly.

---

## §7 — Mandate-fit matrix (per D2)

```yaml
mandate-fit:
  initial-spec: both        # tier-classifier handles both; greenfield runs cold-start regime, brownfield runs spec-against-existing-system regime, same primitives
  refactor: both            # tier-derived from blast radius; same overlay matrix
  mvp: both                 # greenfield-dominant in distribution, brownfield-rare; same architecture
  post-mvp-evolution: both  # tier distribution skews higher for brownfield (more production-proximity)
  regression-fix: both      # brownfield-dominant in distribution; same architecture
```

All five work-unit-classes are `both`. This is the unified claim. The *distribution of tiers per class per mandate* differs (brownfield skews to T2+; greenfield skews to T0–T1 in early cycles, then evolves to T2+ as the system ships) but the **architecture is the same**.

---

## §8 — Open questions surfaced by this track

- **OQ-A1.** Is the tier-classifier itself a F1-class hallucination vector? (Tier-classifier is an LLM-judge; it could mis-classify systematically.) Mitigation: deterministic floors (RSI test always pins T4; production-scissors always pins T3+) + classifier confidence threshold + classifier sample-audit. *Action:* Phase 5 ADR on classifier architecture; lead-agent owns.
- **OQ-A2.** Does the tier-overlay matrix itself drift over time? ([F35](../failure-modes-v3.md#f35--federation-as-family-drift) federation-as-family-drift acutely applies to the matrix as a managed family.) Mitigation: matrix is version-controlled scaffold (CLAUDE.md / AGENTS.md class); changes are themselves T3 work items. *Action:* Phase 5 ADR on overlay versioning.
- **OQ-A3.** Cold-start bootstrap-window calibration (5 cycles? K=5 ≥70%? something else?). The cold-start threshold is one Jaymin-Augmentation-bar choice; OQ-B6 in the brief is the source. *Action:* Phase 6 architecture spec must declare; lead-agent decision pending corpus consensus on OQ-B6.
- **OQ-A4.** Mandate-feed adapter API — what is the minimal interface? (Both feeds must produce identically-typed work-item objects for the tier-classifier to consume uniformly.) *Action:* Phase 5 ADR on work-item schema.
- **OQ-A5.** Tier graduation criterion — fully automatic vs. operator-confirmed? (T0 success graduating to T1 template; T1 pattern sifting to T2 standard, per Brier "patterns sift downward".) Tension with [F57](../failure-modes-v3.md#f57--design-authority-erosion-convenience-reclassifies-stakes) (convenience reclassifies stakes). *Action:* Phase 4 substrate-boundary decision.

---

## §9 — Pre-response to Phase-3 adversarial (multi-persona)

Anticipated personas the unified-mandate-attacker may deploy:

- **Greenfield-purist attack** (Skeptic-class): "Risk-tier collapses greenfield to cautious-incremental shape; the spec-malleable nature is lost when every cycle is at T2." Response: §2 tier-graded malleability — the spec *body* remains malleable; only the *invariant block* ratchets. UC4's malleability is preserved where the user's claim applies (spec-body in low-stakes early cycles).

- **Brownfield-purist attack**: "Brownfield's code-archaeological nature means the tier-classifier can never see the work item without first reading the codebase; classification cost ~= cycle cost, defeating the architecture." Response: brownfield-feed adapter pre-loads codebase archaeology before tier-classification (§1.1); classification consumes already-loaded context, not a fresh codebase scan per cycle. The cost is amortized.

- **Regulator-class attack**: "T4 = AILCCP + board reporting is correct but T3 = lights-out-with-immutable-logging is exactly the Caremark-exposed surface Kahana names." Response: T3 is *not* lights-out per the glossary; it is L4-with-sample-audit (25%) + Patrol watchdog + immutable logging + human-escalation. Per [F43](../failure-modes-v3.md#f43--rsi-board-visibility-gap), T3 work that meets RSI three-part test gets re-classified up to T4 by the classifier's RSI gate. The "RSI-class T3" cell in §1.4 is structurally empty.

- **Newcomer/vocabulary attack**: "Five tiers is one more than Shapiro's five levels and conflates them." Response: §1.3 explicit mapping (lights-out = T0–T2; L4 = T3; L5-rejected = T4). The five tiers are *risk classes*, not *autonomy levels*; the mapping is many-to-one (each tier maps to one regime; regimes contain multiple tiers).

- **Historian attack**: "v2 had four architectures; this collapses them to overlays — that's just re-naming, not unifying." Response: the architectures *are* unified — they share substrate, tier-classifier, tier-overlay matrix, watchdog, judges, escrow, knowledge store, mandate-feeds. What was previously a top-level architectural choice (Atelier vs. Refinery vs. Tournament vs. Foundry) is now a tier-overlay slot. The unification is real; the v2 architectures survive as configuration.

- **CFO/cost attack**: "Tier-overlay = 5 cost ceilings + 5 judge configurations + 5 watchdog cadences + 5 escrow shapes = 5× the implementation cost." Response: low tiers reuse high-tier substrate at reduced configuration. T0 = T1 with judges and Patrol disabled. T1 = T2 with one judge instead of two. The matrix is compositional; substrate cost ~= T4 cost; per-tier marginal cost is configuration, not implementation.

---

## §10 — Verdict on the unified hypothesis (UC4 / D1)

**Conditional yes.** A unified architecture is possible **if** the organizing axis is shifted from mandate to risk-tier. The corpus' empirical anchors (CodeRabbit, Veracode, METR, Replit, Kahana RSI, Shapiro R3) align with risk-tier, not mandate. The substrate primitives (trajectory, watchdog, deterministic perimeter, cross-model judge, escrow) are mandate-agnostic. The methodology overlays (Compound, Attractor, Refinery, Tournament, Council) absorb cleanly as tier-overlay choices.

UC4's "no single architecture works best for both" claim is **partially preserved**: this architecture is not *optimized* for either mandate individually; a mandate-specific architecture would beat it on its native mandate's distribution. The unified claim is that the *cross-mandate substrate cost* of one architecture is lower than the *substrate-divergence cost* of two architectures, given UC2's "share substrate where it makes sense" constraint. This is empirically testable in Phase 8 lean evals.

The hypothesis is not *falsified*. It is also not *confirmed in the maximal form*. A defensible unified architecture exists; whether it dominates two mandate-specific architectures is a Phase-8 measurement question.

---

*End of unified-A.md.*
