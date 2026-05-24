---
based-on-commit: 9a205b6
based-on-date: 2026-05-23
track: unified-no-axis-C
axis: stakes-tier / blast-radius (work-unit classified by reversibility × scope × regulatory-exposure, not by mandate)
mandate-scope: both
---

# Unified architecture — track C: **Stakes-Tiered Factory** (axis: blast-radius tier)

## §0. Axis declaration, defense, vocabulary, and pre-response to the attacker

### 0.1 Chosen axis

The organizing axis is **stakes tier** (a.k.a. *blast-radius tier*): every work-unit a factory cycle ingests is classified into one of four tiers — `T0-sandboxed` / `T1-revertible` / `T2-production-touch` / `T3-regulated` — by three orthogonal properties (**reversibility**, **scope of impact**, **regulatory exposure**). Mandate (greenfield vs. brownfield), unit-of-work shape (issue vs. spec-delta vs. refactor), and regime (Augmentation vs. Automation) are *derived* from the tier classification, not primary.

The architecture is one substrate (the **Stakes Router** + the seven primitives below) running four tier-specific methodology overlays. Greenfield and brownfield are produced by the same factory because they have *overlapping tier mixes* — they are not categorically distinct; they are statistically distinct distributions over the tier surface. A greenfield cold-start cycle on a sandboxed prototype and a brownfield regression-fix on a stable module are *both T0–T1 work* and ride the identical methodology; a brownfield deploy to a regulated production database and a greenfield first-launch of a payments product are *both T3 work* and ride the same gated methodology.

### 0.2 Why stakes, not mandate, regime, substrate/methodology, or pace-layers

- **Vs. mandate-as-primary (UC4 working hypothesis):** Two corpus signals reframe UC4 as a *statistical* claim, not a structural one. (a) The brief's `mandate-fit` matrix per D2 already concedes that one architecture may serve different work-unit-classes differently — the matrix cells are tier-shaped in disguise. (b) F12, F30, F33, F43, F44, F54, F56, F58 — every single trifecta / governance / RSI / production-scissors / Replit-class F-mode — escalates from `high` greenfield to `critical` brownfield not because the *mandate* changed but because **production proximity changed**. Production proximity is a stakes property, not a mandate property. A brownfield refactor on an archived codebase is T0; a greenfield first-launch payment system is T3. Mandate is an OK proxy, but tier is the underlying causal variable.
- **Vs. regime-as-primary (Jaymin Augmentation/Automation, per report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md)):** Regime is *consequent* on stakes. Per CTR-A1 / WEAK-1, Jaymin himself is unstable — L5 anti-pattern *and* "this time it works." Resolving that instability requires saying *for what work*, which is a stakes question. The architecture treats regime as the *output* of the tier classifier (T0–T1 → Automation, T2 → Augmentation, T3 → Human-gated-with-cognitive-escrow).
- **Vs. substrate-vs-methodology split (tracks A/B may pick this):** That split is a *layer* question, not an axis question. Stakes-tiered architecture answers the layer question downstream: the *Stakes Router*, *Holdout Mediator*, *Cognitive Escrow*, *Trajectory Capture*, and *Watchdog* live in the substrate; the *tier-specific cycle methodology* lives on top. The split is preserved; it just isn't the organizing principle.
- **Vs. Brier pace-layers (followup [`12`](../../research/followup/12-brier-pace-layers.md)):** Pace-layers organize *artifacts*; stakes-tier organizes *work-units*. They are orthogonal and composable. Pace-layers tell you which artifact is moving fast (code) vs. slow (standards); stakes-tier tells you which *cycle of work* deserves which gates. F34 (cross-layer drift) is mitigated by *both* a pace-layer-aware judge (which slow-layer invariants apply) *and* a stakes-tier-aware gate (whether to merge without human review). Architecture C imports Brier's pace-layers as the *artifact-side* dimension; stakes is the *cycle-side* dimension.
- **Vs. work-unit-class taxonomy per D2 (`initial-spec` / `refactor` / `mvp` / `post-mvp-evolution` / `regression-fix`):** The D2 taxonomy is shape-based (what kind of work). Stakes is property-based (what happens if it's wrong). Both are valid; stakes is *strictly more discriminating* for the questions the architecture must answer at the cycle boundary — *should a human enter the inner loop? should the holdout discipline apply? should production scissors be on?* The five-class D2 taxonomy is preserved as a *secondary* dimension; the architecture's mandate-fit matrix per D2 is filled out in §6.

### 0.3 Pre-response to Phase-3 unified-mandate-attacker

The attacker will say: *"Stakes-tier collapses the mandate distinction without justifying it. UC4 names spec-malleability for greenfield and existing-architecture-as-given for brownfield; these are deep structural properties of the work, not blast-radius properties. Your architecture pretends they are the same thing."*

Pre-response:

1. **The architecture does not collapse the distinction; it relocates it.** Spec-malleability (UC4) and existing-architecture-as-given (UC4) are properties of *which methodology overlay* fires, not properties of *which architecture is running*. Greenfield T0–T1 cycles use the **discovery overlay** (spec-malleable; intent-block-anchored upstream per El Kaim, report [`14`](../../research/14-el-kaim-book-intent-and-spec-authorship.md); MISSED-3 handled by tier-aware invariant strictness — see §3.2). Brownfield T0–T1 cycles use the **excavation overlay** (codebase-traversal-first; scenarios inherited from the codebase per CTR-B5 brownfield inversion). These are different overlays on the same substrate; the attacker's "deep structural difference" is real but lives at the methodology layer, not at the substrate layer.

2. **UC4 is a falsifiable hypothesis (D1), and the falsification is specific.** UC4 predicts no single architecture works for both. The architecture-C claim is more precise: *no single methodology overlay works for both, but a single substrate plus a tier-aware overlay-selector does.* This is the substrate-heavy + thin-methodology shape Round-2 §8 named (CTR-C2 framing); the corpus' deepest substrate audits (reports [`11`](../../research/11-openhands-substrate-audit.md), [`18`](../../research/18-openai-codex-substrate.md), [`38`](../../research/38-gas-systems-substrate.md)) all describe substrate primitives that are mandate-agnostic. Round-2's substrate-heavy thesis is corroborated empirically.

3. **The attacker may then say: "Then your architecture is just a substrate with two methodologies bolted on; it's not unified, it's two architectures sharing infrastructure."** Pre-response: The unification is *not* in the substrate alone. It is in (a) the **tier classifier** that mechanically selects the overlay (and reclassifies dynamically as work progresses — F57 mitigation); (b) the **knowledge-accumulation primitive** (Beads' `discovered-from` edge per report [`38`](../../research/38-gas-systems-substrate.md); CK typed-classification per followup [`11`](../../research/followup/11-compound-knowledge.md)) that is shared across overlays so a brownfield excavation finding informs a greenfield discovery and vice versa; (c) the **holdout-mediator** that enforces D-4 across overlays. Without (a)+(b)+(c) it would indeed be two architectures sharing a substrate; with them, it is one factory with a stakes-router at its front door.

4. **The attacker's strongest move is to challenge the tier classifier itself.** F36 (instruction-following ceiling) and F37 (silent contradictory-prompt collapse) say LLM-based classifiers degrade past 10–20 requirements; F38 (vocabulary lint debt) says LLM-authored classification rules drift. The classifier is therefore designed as a **deterministic policy table over typed attributes** (production-access? regulated-domain? reversible? blast-radius-LOC?) — not an LLM judgment. This is the F51 (Ashby-deficient probabilistic guard) lesson generalised one layer up: the *router itself* must not be a probabilistic guard.

5. **Falsification claim:** If Phase 4 finds that no shared substrate primitive serves T0 greenfield and T3 brownfield without per-mandate divergence even at the substrate layer, the architecture is falsified. The Phase-4 substrate/divergence extraction is the empirical test. (See §7.)

### 0.4 Vocabulary

| Term | Definition (architecture C specific) |
|---|---|
| **Tier** | A property of a work-unit, not of a factory or a codebase. Four values: T0/T1/T2/T3 (see §1). |
| **Stakes Router** | Substrate-level deterministic classifier that assigns a tier to a work-unit at ingestion and re-evaluates at declared trigger points. |
| **Overlay** | A tier-specific methodology bundle (discovery / iteration / production-touch / regulated). |
| **Excavation overlay** | The methodology overlay used for brownfield-shape work at T0–T1: codebase-traversal-first, scenarios-from-codebase, El-Kaim-spec-constrains-refactor. |
| **Discovery overlay** | The methodology overlay used for greenfield-shape work at T0–T1: intent-block-anchored, spec-malleable below invariants, EARS/GtWR-linted, three-prototypes-of-ascending-fidelity (Klaassen, followup [`05`](../../research/followup/05-klaassen-siblings.md)). |
| **Production-touch overlay** | T2 methodology: holdout enforced, cross-model judge required, cognitive-escrow on every artifact crossing the production boundary, F44 production-scissors-off by substrate default. |
| **Regulated overlay** | T3 methodology: Human Approval Gate per AILCCP (followup [`10`](../../research/followup/10-governance.md)); SB-53/SEC-IAC structured-reporting payload generated per cycle (F43 mitigation); RSI three-part-test classifier evaluated (F54/F55 mitigation). |
| **Stakes drift** | The F57 failure mode of convenience reclassifying a work-unit downward across cycles. Substrate-monitored. |
| **Tier-lock** | A scaffold annotation on an artifact (file, module, deploy target) that pins it to a minimum tier regardless of work-unit classification. Brownfield codebases inherit tier-locks from their existing classification; greenfield codebases accumulate them. |

---

## §1. The four tiers (the axis, operationalized)

Tier classification uses three orthogonal properties (deterministic, not LLM-judged):

1. **Reversibility** — can the artifact be rolled back to its pre-cycle state by `git revert` + redeploy alone? (yes/no)
2. **Scope** — does the artifact change cross a process / VM / network / org boundary at deploy? (sandboxed / repo-local / cross-system / cross-org)
3. **Regulatory exposure** — does the artifact touch a class declared as regulated by operator policy (PCI / HIPAA / GDPR / SB-53 RSI / Caremark mission-critical)? (none / declared / declared+attestation-required)

The tier is the *least-permissive* result of evaluating all three properties:

| Tier | Reversibility | Scope | Regulatory | Examples |
|---|---|---|---|---|
| **T0-sandboxed** | yes | sandboxed | none | greenfield prototype iteration; brownfield code-archaeology / read-only analysis; experimental branches |
| **T1-revertible** | yes | repo-local | none | greenfield MVP feature add; brownfield refactor or regression-fix that lands in a feature branch behind a flag |
| **T2-production-touch** | no (data migration / external API change / deploy artifact) | cross-system | none-or-declared | greenfield first launch; brownfield post-MVP evolution shipping to users; any data-schema migration |
| **T3-regulated** | usually no | cross-system or cross-org | declared+attestation-required | brownfield change to a Caremark mission-critical system; greenfield deploy into a regulated domain (finance / health / aviation); any change classified under SB-53 RSI three-part test per report [`31`](../../research/31-caremark-rsi-board-exposure.md) |

**Why this taxonomy generalizes:** Every load-bearing severity divergence in the F-mode catalog between greenfield and brownfield reduces to a tier shift. F12 (lethal trifecta) `high → critical` because brownfield is more often T2/T3 (production access). F33 (adversarial-prompt judge defeat) same reason. F34 (cross-layer drift) `high → critical` because brownfield has explicit slow-layer invariants (architecture, standards) that are *tier-locked*. F44 (production-scissors default) same reason. The mandate-axis severity column is a proxy for the tier-frequency-distribution per mandate; the tier-axis is the underlying mechanism.

**Why mandate is not eliminated:** The *distribution* over tiers differs by mandate. Greenfield concentrates work in T0–T1 with episodic T2 launches; brownfield concentrates work in T1–T2 with chronic T3 exposure. Mandate predicts *which overlay will fire most often*; tier mechanically *selects* the overlay per cycle.

---

## §2. Substrate primitives (shared across all tiers and both mandates)

Seven substrate primitives. Each is named, located in the substrate-vs-methodology layer per CTR-C2 / CTR-F3, and cited.

### S1. Stakes Router (NEW; architecture-C-specific substrate primitive)

Deterministic classifier; reads typed work-unit attributes (operator-declared on ingestion) plus scaffold-declared tier-locks; outputs a tier and the overlay-selection. Re-evaluates at named trigger points (artifact crosses a tier-lock boundary; CI declares a deploy intent; operator policy update). Implemented as a policy table; never an LLM call (per §0.3 point 4 and F51 Ashby argument).

Substrate-location: yes. Mandate-agnostic: yes.

### S2. Holdout Mediator (substrate-enforced D-4)

Per Round-2 C13: acceptance criteria withheld from builder agents by substrate, not methodology. Architecture-C extension: in brownfield T1–T2, the holdout is *partially* the codebase (CTR-B5 inversion — production traces and existing tests are the held-out signal); the Holdout Mediator brokers which signals are visible to which agent under which overlay. D-2 fragility (scenarios outside vs. inside the codebase) is resolved by tier+mandate: T0 greenfield → out-of-tree scenarios (StrongDM canonical); T1+ brownfield → in-tree-but-mediator-gated.

Substrate-location: yes. Per D-2: *challenged* (see §4).

### S3. Cognitive Escrow (per report [`30`](../../research/30-cognitive-escrow.md))

Interval-as-design-surface. Substrate-level primitive that shapes the prompt→response interval per overlay: T0 → zero-interval (lights-out); T1 → batched-summary-interval (operator reviews aggregated, not per-cycle); T2 → per-artifact escrow with re-engagement prompts; T3 → Human Approval Gate per AILCCP. Mitigates F42 directly and F53 (voluntary-discipline fragility) by substrate-triggering the discipline rather than relying on operator-voluntary action.

Substrate-location: yes. Mandate-agnostic: yes.

### S4. Trajectory Capture (D-7 default, accepted)

Per Round-2 C16 / report [`11`](../../research/11-openhands-substrate-audit.md): sub-ms persist, 7.4ms recovery. Architecture-C extension: every trajectory event carries a `tier` and `overlay` tag for downstream forensic reconstruction (F14 widened mechanism). Brownfield trajectories additionally tag `tier-lock-source` (which scaffold annotation pinned the tier).

Substrate-location: yes. Per D-7: *accepted with justification* (tier-tagging is additive, not structural).

### S5. Tiered Watchdog (D-6 default, accepted; extended)

Per Round-2 C14: Daemon (seconds) / Triage (minutes) / Patrol (hours). Architecture-C extension: Patrol additionally watches for **stakes drift** (F57) — a work-unit reclassified downward across cycles without an explicit policy change triggers a Patrol escalation, regardless of per-cycle health.

Substrate-location: yes. Per D-6: *accepted with justification*.

### S6. Knowledge-Accumulation Edge (Beads' `discovered-from` per report [`38`](../../research/38-gas-systems-substrate.md); CK typed-classification per followup [`11`](../../research/followup/11-compound-knowledge.md))

A typed edge in a knowledge graph (insight / playbook / correction / pattern, per CK) that records which prior cycle generated each piece of knowledge and what tier+overlay produced it. Cross-overlay queries are first-class: a brownfield excavation can query for greenfield discovery findings tagged "pattern" from the same domain. Mitigates F8 (stale-knowledge inversion) by tier-aware staleness rules (T3 findings expire faster than T0); F55 (behavioural drift / self-reference loop) by tracking provenance to human-origin vs. agent-origin.

Substrate-location: yes. Mandate-agnostic: yes (cross-overlay reads are the unification mechanism per §0.3 point 3).

### S7. Provider-Property Declaration (per OQ-B8; not RouterLLM unification per CTR-C4)

Per CTR-C4 unresolved tension: architectures declare *provider-property requirements* (model-family diversity for T2/T3 judges; long-context for T0 discovery; tool-calling latency for T1 iteration). Per-overlay profile rather than per-call router. Sidesteps the OpenHands-vs-Attractor unification dispute by declaring requirements without prescribing the router shape. CTR-D7 (Anthropic same-model-judge-is-fine) is resolved by tier: T0–T1 may use same-model judging (Anthropic's claim holds for low-stakes); T2–T3 require cross-model judging (CJ Hess `kevin/carl` pattern from report [`34`](../../research/34-lenny-howiai-personal-harnesses.md) holds when the failure mode matters).

Substrate-location: yes (the *requirement declaration interface* is substrate; the *router implementation* is operator-chosen).

---

## §3. The four overlays (the methodology, tier-selected)

### 3.1 Discovery overlay (T0–T1 greenfield-shape; also T0 brownfield exploration)

- **Unit of work:** an intent block (El Kaim 9-field, report [`14`](../../research/14-el-kaim-book-intent-and-spec-authorship.md)) plus a freshly-authored spec fragment under it.
- **Spec discipline:** *invariants* in the intent block are non-negotiable (resolves MISSED-3: spec-malleable below the invariant line, not above); spec drafts under the invariants are malleable. UC4's spec-malleability is preserved *between* invariants and is bounded *by* invariants. EARS / GtWR-linted at the authoring boundary (F38 mitigation).
- **Cold-start protocol:** see §5.
- **Judge:** same-model judging permitted at T0 (per CTR-D7 / Anthropic Husain/Shankar position); T1 requires a second-model spot-check.
- **Knowledge writes:** every cycle writes a CK-typed entry; `discovered-from` edge links to upstream intent block.
- **Holdout:** out-of-tree scenarios (StrongDM canonical).

### 3.2 Excavation overlay (T0–T1 brownfield-shape)

- **Unit of work:** a *change request against the existing system* (OQ-B4 — neither pure issue nor pure spec-delta; a *codebase-evolution proposal* with a typed `affects` graph over existing files).
- **Spec discipline:** spec extracted from existing code via codebase-traversal agents *before* the change proposal is allowed to be drafted (CTR-G4 — code is readable archaeological input, *not* opaque ML weights). The spec is constrained by the existing system (UC4 brownfield framing preserved).
- **Judge:** existing tests + production-trace replay are *primary* signal; LLM judges are secondary.
- **Holdout:** D-2 *challenged* — scenarios inherited from the codebase (CTR-B5 inversion; brownfield is closer to StrongDM's actual practice per WEAK-3).
- **Knowledge writes:** CK entries with `archaeological` sub-tag; cross-readable from discovery overlay.

### 3.3 Production-touch overlay (T2 — both mandates)

- **Unit of work:** a deploy candidate plus its rollback artifact.
- **Spec discipline:** spec frozen at the T1→T2 transition; spec git-history-is-changelog (Nystrom / report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md)). Resolves CTR-B7 spec-velocity by tier: T0–T1 spec moves fast (Nystrom); T2+ spec is stable mid-layer (Brier). The *same spec* moves through the velocity bands.
- **Judge:** cross-model required (CJ Hess `kevin/carl` pattern; F46 mitigation); same-model self-review prohibited at this tier.
- **Holdout:** strict (D-4 fully enforced); production traces from prior deploys added to holdout pool.
- **Knowledge writes:** CK entries tagged `production-validated`; subject to stricter staleness rules.
- **Substrate gates:** F44 production-scissors-off by default; F12/F33 mitigations enforced; CaMeL-class typed-interpreter perimeter per followup [`08`](../../research/followup/08-security-primitives.md).
- **Cognitive escrow:** per-artifact, with re-engagement prompts (F42 mitigation).

### 3.4 Regulated overlay (T3 — both mandates)

- **Unit of work:** as T2, plus a *governance payload* (RSI three-part-test evaluation; AILCCP control attestation; SB-53/SEC-IAC reporting bundle).
- **Spec discipline:** as T2, plus *runtime-compliance attestation* (F58 mitigation — design-time/runtime split addressed by attaching runtime-monitored invariants to every spec invariant).
- **Judge:** as T2, plus a *third-party* validator (model from a different vendor than primary or critic, per CTR-D4 / D7 resolution: at T3, judge-diversity moves from preference to substrate requirement).
- **Holdout:** as T2, plus regulator-facing audit-trail discipline (BCG "structurally easier to audit" claim per CTR-H5; Kahana "tracing difficult by design" mitigated by structured-reporting payload).
- **Knowledge writes:** CK entries tagged `regulated`; immutable-log requirement per AILCCP control.
- **Human Approval Gate:** mandatory per AILCCP; this is the **human re-entry mechanism** per OQ-B3.

---

## §4. §4 defaults — accepted vs. challenged

| Default | Status (architecture C) | Justification |
|---|---|---|
| **D-1** Specs are durable, version-controlled, human-curated | **accepted with justification** | Holds across all four overlays; *content* of "human-curated" differs (T0–T1 discovery = author-drafted-then-agent-extended; T2+ = frozen-and-version-history-is-changelog per Nystrom). Provenance: brief §4.1 + CTR-B7 resolution by tier. |
| **D-2** Scenarios live outside the codebase as a holdout set | **challenged** (per the brief's own fragile-flag) | Per CTR-B5 / WEAK-3 / CTR-G2: in brownfield T1–T2 the holdout *includes* in-codebase signals (production traces, existing tests) brokered by S2 Holdout Mediator. StrongDM's own primary pages already include scenario-equivalents inside the running system (WEAK-3); D-2 oversimplifies its own source. Architecture-C resolution: the substrate enforces holdout *discipline*; the *location* of the holdout is overlay-dependent. |
| **D-3** Agent = Model + Harness | **accepted with justification, with one extension** | Holds for the agent shapes architecture C uses (discovery agent / excavation agent / cross-model critic / regulated validator). Extension per CTR-C10 / MISSED-8: the substrate's provider-property declaration (S7) includes natural-language register as a declarable harness parameter (Portuguese-vs-English collusion-rate finding from report [`37`](../../research/37-academic-llm-agent-collusion.md) made the vocabulary incomplete). Graph-node / population shapes (CTR-C1 fragile flag) are not used. |
| **D-4** Holdout discipline substrate-enforced | **accepted with justification** | S2 Holdout Mediator is the substrate enforcement. Mandate-agnostic. |
| **D-5** Hard cost ceilings non-optional in CI | **accepted with justification, with one extension** | Per CTR-E1 (Cherny $100K vs. noosphr $500/day): cost ceiling is *per-tier*, not uniform. T0 cycles have generous ceilings; T3 cycles have aggressive ones (the regulated overlay is expensive per cycle and cheap to halt). Per CTR-E6 / MISSED-9 (CaMeL 7-point utility tax): the cost-of-safety is named explicitly in T2–T3 budgets, not assumed zero. |
| **D-6** Tiered watchdog substrate primitive | **accepted with justification** | S5; extended with stakes-drift detection in Patrol layer (F57 mitigation). |
| **D-7** Trajectory capture cheap and production-tested | **accepted with justification** | S4; extended with tier+overlay tagging. |

---

## §5. Cold-start (MANDATORY — architecture addresses greenfield T0)

Per brief §5.1 (Historian M5), the required reading is reports [`25`](../../research/25-requirements-engineering-foundations.md), [`26`](../../research/26-prompt-underspecification-academic.md), [`30`](../../research/30-cognitive-escrow.md), [`31`](../../research/31-caremark-rsi-board-exposure.md), followup [`10`](../../research/followup/10-governance.md). Each is addressed below.

### 5.1 Day 0 — no scenarios, no issue queue, no prior runs

The greenfield T0 cold-start uses the **Discovery overlay** (§3.1) bootstrapped by a **three-anchor day-0 protocol**:

1. **Intent block** (El Kaim 9-field, report [`14`](../../research/14-el-kaim-book-intent-and-spec-authorship.md)) authored by the operator. The `invariants` field is the *only* non-negotiable artifact; everything else is malleable. This addresses MISSED-3 by *bounding* UC4's spec-malleability rather than denying it — invariants are stable upstream; specs are malleable below.
2. **Adjacent-domain prior pool** (per brief §0 glossary, greenfield permits priors). Operator declares N adjacent-domain exemplar codebases / projects / docs / SKILL.md libraries; substrate ingests them as *read-only* corpus tagged `prior-art`. Knowledge-accumulation edge (S6) will tag day-0 CK entries with `derived-from-prior-art`.
3. **EARS / GtWR-shaped scaffold** (report [`25`](../../research/25-requirements-engineering-foundations.md)) for the first spec. This is the RE/SE foundational catalog; the linter (F38 mitigation) runs from cycle 1.

### 5.2 Priors that are permitted (per UC6 revision)

Adjacent-domain exemplars; library docs; operator-curated knowledge from *other* factory runs (with cross-run provenance preserved by S6); the RE/SE foundational catalog (EARS, GtWR, INCOSE Complexity Primer); the AILCCP framework as governance scaffold (followup [`10`](../../research/followup/10-governance.md)); the cognitive-escrow patterns from report [`30`](../../research/30-cognitive-escrow.md).

### 5.3 Bootstrap protection against silent failure (the cold-start central risk)

The architecture has no track record on day 0; it cannot self-evaluate. Four mitigations:

1. **Empirical-bar declaration per overlay (OQ-B6).** The discovery overlay's day-0 bars are *Jaymin Augmentation thresholds* (K=5 ≥70%; prompt-paraphrase ≥3/5 — corpus-derived, not user-mandated, per Skeptic #10) — explicitly the lower bar set; Automation bars only unlock at T0→T1 when 10 consecutive cycles clear them. Engages WEAK-1 (Jaymin's instability) by *not* claiming Jaymin's bars are correct; only that they are the conservative default.
2. **Yang et al. F36 ceiling-aware scoping.** The day-0 spec is *required* to fit ≤10 requirements per discovery cycle (well under the 10–20 LLM ceiling, per report [`26`](../../research/26-prompt-underspecification-academic.md)). Larger specs are decomposed by the substrate, not the agent.
3. **Larbi et al. F37 contradiction-check on every spec write.** A second-model contradiction-detector runs on every new spec fragment (MCC ≤0.55 is insufficient, so the detector is one signal among several, not a sole guard — F51 Ashby-deficient lesson applied).
4. **Cognitive Escrow at T0 is batched-summary, not zero-interval, for the first N cycles** (operator-tunable; default N=10). Lights-out *transitions in* once the empirical-bar declaration is cleared, not on day 0. This addresses the brief §2.1 lights-out / L5 tension at the cold-start boundary: the architecture is *Augmentation-mode at cold-start by substrate default*, transitioning to Automation-mode per-overlay as evidence accumulates.

### 5.4 Trajectory day-0 → day-N (when cold-start ends)

- **Day 0:** Augmentation-mode by substrate default; T0-only work; operator in batched-summary escrow.
- **Day ~5:** First T1 work admitted if T0 cycles cleared bars 10 consecutive times.
- **Day ~30:** First T2 work admitted if T1 cycles cleared bars 10 consecutive times AND production-touch overlay's cross-model judge is configured.
- **T3 work admitted** only after operator-declared regulatory regime is named *and* AILCCP controls are running (governance-by-design per followup [`10`](../../research/followup/10-governance.md) §3 BCG framing). T3 is not a default trajectory; it is operator-elected.
- **Cold-start ends** when steady-state is declared: a defined fraction (default 80%) of cycles complete without operator inner-loop entry over a defined window (default 30 days). Steady-state is a substrate flag, not an aspiration.

### 5.5 Engaging the Stanford CodeX governance pair (reports [`30`](../../research/30-cognitive-escrow.md) + [`31`](../../research/31-caremark-rsi-board-exposure.md))

- **Cognitive Escrow (report 30):** S3 is the substrate-level instantiation. The AILCCP missing-fourth-question (about the *interval*) is answered by the per-tier escrow design.
- **Caremark / RSI (report 31):** The T3 regulated overlay carries the RSI three-part-test classifier and the SB-53/SEC-IAC reporting payload. F43 (RSI Board-Visibility Gap) is mitigated by *generating the governance payload per cycle*, not as a post-hoc reporting layer. Architecture-C asserts: greenfield deployments into regulated domains *cannot* skip T3 overlay even at cold-start; the day-0 operator declaration includes a regulatory-regime field.

---

## §6. Mandate-fit matrix per D2

| Work-unit-class | Tier distribution | Greenfield-fit | Brownfield-fit | Notes |
|---|---|---|---|---|
| `initial-spec` | T0 dominant; T1 once invariants stable | **both** (Discovery overlay primary) | **both** (Excavation overlay for brownfield re-spec; Discovery for greenfield-shape T0 work in a brownfield codebase) | The overlay differs; the substrate is identical. |
| `refactor` | T0–T1 dominant; T2 when crossing module boundaries | **both** (rare for pure greenfield; Discovery overlay handles small early refactors) | **both** (Excavation overlay primary) | Brownfield refactor is the canonical case; greenfield refactor is a special case of Discovery. |
| `mvp` | T0–T1 sweep, terminating in a T2 first-launch | **both** (Discovery → Production-touch overlay transition) | **n/a** (an MVP in an existing system is a `post-mvp-evolution`) | This is the cleanest greenfield work-class. |
| `post-mvp-evolution` | T1–T2 dominant; T3 when in regulated domain | **both** (Discovery overlay with tier-locks accumulating) | **both** (Excavation → Production-touch overlay) | Brownfield-dominant statistically; both mandates fit structurally. |
| `regression-fix` | T1 default; T2 if hot-fix; T3 if regulated | **both** (rare) | **both** (Excavation overlay with strict change-budget) | Brownfield-dominant statistically. |

**Headline view (per UC3 and D2):** Architecture C is `both` for every work-unit-class because the substrate is shared and the overlay-selection is tier-driven. The *strength* of fit varies by tier-frequency-distribution per mandate, which is captured in the *Notes* column rather than collapsing the fit values to single-mandate tags.

---

## §7. Cross-cutting addresses to load-bearing tensions

### 7.1 The lights-out / L5 / regime tension (OQ-B1, brief §2.1) — engaging CTR-A4 explicitly

Per CTR-A4: "lights-out" (UC1) is not necessarily L5 (Jaymin). Architecture-C resolves the mapping by **regime per tier, not per architecture** — brief §2.1 option (c) + (b) plus an extension:

- **T0 cycles:** lights-out = L5-equivalent (no human in inner loop; per Jaymin's Augmentation/Automation thresholds being cleared, where applicable). Jaymin's L5-anti-pattern claim is *engaged* here by requiring the bars to clear *empirically* before lights-out unlocks (per §5.3); the architecture defaults to Augmentation at cold-start.
- **T1 cycles:** lights-out (Automation mode), human re-engages on watchdog escalation per OQ-B3 protocol.
- **T2 cycles:** human in the loop for the production-boundary crossing only (Augmentation-mode for that step; Automation everywhere else in the cycle). Compatible with brief §0 definition of lights-out (*"automation-eligible work units"*).
- **T3 cycles:** Human Approval Gate mandatory per AILCCP; this is *not lights-out*. The architecture is honest that T3 work is L3–L4, not L5.

**Engaging WEAK-1** (Jaymin's self-instability): the architecture does not adopt Jaymin's bars as definitively correct; they are the substrate's *conservative default* and operator-overridable per OQ-B6. Architecture-C's empirical-bar declaration is per-overlay, surface-visible, and re-evaluable as evidence accumulates.

**Engaging Shapiro's L4 self-position (CTR-A2):** consistent with architecture C — T2 and T3 cycles are explicitly L4 (Shapiro's "I'm here"); T0–T1 may be L5-equivalent post-bar-clearance. Architecture C does not require any human to be at L5; it requires *some work* to be at L5 once empirically defensible.

### 7.2 MISSED-3 — El Kaim invariants vs. UC4 spec-malleability

Resolved by the Discovery overlay (§3.1): invariants in the intent block are non-negotiable; specs below invariants are malleable. UC4 is preserved as a *between-invariants* property. This makes the tension a layer-decomposition question rather than a contradiction.

### 7.3 CTR-C2 — substrate-heavy + thin-methodology vs. UC4

Architecture C is the *exact shape* CTR-C2 names as the alternative to UC4: a shared substrate (S1–S7) with thin per-tier methodology overlays. The Phase-4 substrate/divergence extraction will test whether the substrate primitives genuinely serve all four overlays without per-overlay divergence at the substrate layer; if S2/S3/S6 require overlay-specific implementations rather than overlay-specific configurations, the unified case weakens.

### 7.4 The substrate stack — CTR-C5 (OpenHands+Overstory vs. Gas City)

Architecture C is substrate-stack-agnostic by declaration. The seven primitives (S1–S7) are declared by capability, not by implementation: a Gas City pack implementation, an OpenHands+Overstory implementation, or a from-scratch implementation can each carry the primitives. The S6 knowledge-accumulation edge maps most naturally to Beads' `discovered-from` (report [`38`](../../research/38-gas-systems-substrate.md)); the S4 trajectory capture maps most naturally to OpenHands V1 event-sourcing (report [`11`](../../research/11-openhands-substrate-audit.md)). Architecture C does not pre-commit; the substrate ADR (Phase 5) does.

### 7.5 The scaffold split — CTR-C6 / WEAK-2 (bitter-lesson vs. scaffold-substrate)

Architecture C sides with the **scaffold-substrate camp** (Anthropic Skills + AGENTS.md + Codex + Compound knowledge-store) but with a tier-aware bound: scaffold dependencies must be *declared* per overlay so that a scaffold change is itself a tier-routable work-unit. This addresses the bitter-lesson critique without abandoning scaffolds: scaffolds remain load-bearing, but they are versioned, attributed, and tier-classified rather than ambient. Brief §0 substrate-primitive #9 (AGENTS.md discoverability) is preserved.

### 7.6 F48/F49 multi-agent collusion (CTR-D5, report [`37`](../../research/37-academic-llm-agent-collusion.md))

T2 and T3 overlays prohibit multi-agent shared-context coordination beyond the cross-model judge pattern. Tournament-style population architectures (CTR-D3) are not used at T2/T3. F48 (tacit collusion) is bounded to T0–T1 where the blast radius permits the failure. This is a deliberate scope choice: architecture C does not solve F48/F49 for T2/T3 — it *avoids* the failure-surface by restricting the agent topology there.

### 7.7 Engaging the F-mode catalog explicitly

- **F1, F27, F46, F48** (correlated-error cluster): mitigated by S7 + per-tier judge requirements (§3); fully mitigated at T2/T3, partially at T0–T1.
- **F12, F33, F44, F56** (production-scissors / Trifecta / Replit-class): T2/T3 substrate defaults close the trifecta; T0–T1 inherit sandbox isolation as the closure.
- **F30, F43, F54, F58** (governance / RSI / runtime-compliance): T3 overlay is the primary mitigation; F58 is acknowledged as a residual risk for any T2 cycle in a regulated-adjacent system.
- **F34, F35, F59** (drift / decomposition): tier-locks and the pace-layer-aware judge (§0.2) bound the drift; F59 (premature decomposition) is mitigated by *not decomposing T0 work into spec-then-implement* — Discovery overlay allows implementation to discover the spec shape.
- **F36, F37, F38, F39** (spec/prompt failures): scoping discipline (§5.3); EARS/GtWR lint; complexity-diagnosis at T1→T2 transition.
- **F42, F53, F57** (cognitive-escrow / voluntary-discipline / stakes-drift): S3 substrate-trigger removes the operator-voluntary requirement; S5 Patrol watches stakes drift.
- **Most-cited (this track): F12 / F44 (production-scissors cluster) and CTR-A4 (lights-out/L5 mapping).**

---

## §8. Open questions, falsification surface, and TBDs

### 8.1 Open questions surfaced by this architecture

- **OQ-C1.** The tier classifier is deterministic (§0.3 point 4). Does the typed-attribute set (reversibility / scope / regulatory) actually cover all corpus work-unit shapes, or does it require a fourth attribute (e.g., *velocity-criticality* for hot-fix work, *audience* for internal-tooling vs. customer-facing)? *Next action: Phase-4 substrate ADR to enumerate attribute set; operator-extensible policy table.*
- **OQ-C2.** Per CTR-D7 / D8: same-model judging is permitted at T0–T1, prohibited at T2–T3. Where exactly is the cut? *Next action: Phase-5 ADR on judge-diversity-by-tier; lean-eval brief to test 0–4 cycle types.*
- **OQ-C3.** The Discovery overlay's empirical-bar declaration (§5.3) defaults to Jaymin's bars per Skeptic #10. WEAK-1 says Jaymin is self-unstable. *Next action: Phase-6 architecture spec to declare which bar set the architecture's lean-eval will measure against; surface as DECISIONS-PENDING for operator policy.*
- **OQ-C4.** Per CTR-C5: substrate stack is declared by capability. Which existing stack (Gas City vs. OpenHands+Overstory vs. from-scratch) best carries S1–S7? *Next action: Phase-5 substrate ADR; possibly multiple stack-specific architecture specs in Phase 6.*
- **OQ-C5.** The cross-mandate knowledge-accumulation edge (S6) is the central unification claim per §0.3 point 3. Does an operator running both mandates actually benefit from cross-overlay knowledge transfer, or does it pollute (F8 stale-knowledge inversion across mandate boundaries)? *Next action: lean-eval brief to A/B test cross-overlay vs. partitioned knowledge graphs.*

### 8.2 Falsification surface

Architecture C is falsified if any of the following are demonstrated in Phase 4+:

1. The seven substrate primitives cannot serve all four overlays without per-overlay divergence at the substrate layer. (Tests CTR-C2.)
2. The tier classifier requires LLM judgment in non-trivial fraction of cases (>5% per operator workload). (Falsifies §0.3 point 4; resurrects F51.)
3. The cross-overlay knowledge-accumulation edge (S6) shows measurable knowledge degradation rather than transfer in the lean-eval. (Falsifies §0.3 point 3.)
4. Operator workload data shows the stakes-tier classification mismatches operator's intuitive mandate-classification >50% of the time in a way that produces incorrect overlay selection. (Falsifies the axis choice itself.)

### 8.3 What architecture C is *not*

- Not a substrate-stack proposal (CTR-C5 explicitly deferred to Phase 5).
- Not a regime declaration (regime is *derived* per tier).
- Not a multi-codebase coordination story (out of scope per brief §7).
- Not a methodology-evolution story (OQ-B9 not resolved; methodology overlays are static within a tier; meta-evolution is a Phase-5 ADR).

---

## §9. Summary

**The unified case is possible**, *if* the organizing axis is stakes-tier rather than mandate. The architecture is one substrate (S1–S7) running four tier-selected methodology overlays (Discovery / Excavation / Production-touch / Regulated). Greenfield and brownfield are statistical distributions over the same tier surface; UC4's spec-malleability is preserved as a property of overlays at T0–T1, not as a property of the architecture. Lights-out / L5 / regime tension is resolved by per-tier regime classification (CTR-A4 resolution: T0–T1 may be L5-equivalent post-empirical-bar-clearance; T2 is L4; T3 is L3 with Human Approval Gate). Cold-start uses Augmentation-mode default transitioning to Automation per-overlay as evidence accumulates.

*End of unified-C.md.*
