---
based-on-commit: d430aeb
based-on-date: 2026-05-23
track: unified-no-axis-B
axis: pace-layers (Brier-style; Code / Plans / Specs / Architecture / Standards) as primary; mandate as derived view
mandate-scope: both
---

# Track unified-B — Pace-Layered Factory

## §0. Axis declaration, glossary, and pre-response to adversarial

### 0.1 Chosen axis: pace-layers

**Primary organizing axis:** Brier's five pace-layers — **Code / Plans / Specs / Architecture / Standards** (followup [`12`](../../research/followup/12-brier-pace-layers.md)) — with each layer carrying its own (i) artifact format, (ii) churn cadence, (iii) regime declaration (L3/L4/L5), (iv) judge architecture, and (v) human-re-entry trigger set.

**Mandate becomes a derived view, not a top-level branch.** The same five-layer stack applies to both mandates; the differences between greenfield and brownfield are **per-layer churn-rate distributions** (greenfield = Specs+Plans are fastest, Architecture is fluid; brownfield = Architecture+Standards are fastest-given because pre-existing, Plans+Code are where new churn lives) — not a difference in the stack itself.

### 0.2 Why this axis (not the obvious ones)

Candidate axes the brief enumerates: substrate-vs-methodology split (Round-2 default, likely Track A); regime per Jaymin (Augmentation vs. Automation); stakes/risk-tier; work-unit-class (D2); knowledge-accumulation strategy; judge-architecture; scaffold-vs-substrate; language-as-harness; governance-tier; **pace-layers (Brier)**.

**Pace-layers is the strongest unified axis** because:

1. **It dissolves CTR-A4 (lights-out vs. L5) constructively, not by punting.** Lights-out is per-layer, not uniform. Code-layer cycles can run L5/lights-out (fast, cheap, reversible via Git, test-gated); Architecture and Standards layers stay at L4 with explicit human approval — Shapiro's "I'm here" position is preserved exactly where he ships it (L4) and the L5 anti-pattern citations (CodeRabbit 1.4×, Veracode 45%) get scoped to the *layer they were measured at* (code review, code generation), not blanket-applied to the whole factory. See §3 for the regime-per-layer matrix.

2. **It engages MISSED-3 (El Kaim invariants vs. UC4 spec-malleable) head-on.** El Kaim's 9-field intent-block with **non-negotiable invariants** lives at the **Standards layer** (slow, human-curated, governs everything below). UC4's spec-malleability is a property of the **Spec and Plan layers** (faster cadence). The contradiction was real only under a flat-spec model; under pace-layering, both are true at different layers. This is the corpus's own resolution mechanism — Brier explicitly proposes the stack as the cure for "everything-is-spec" confusion (followup [`12`](../../research/followup/12-brier-pace-layers.md) §6, where Brier names Arch 1 spec-primary as falsified).

3. **It directly attacks F34 (cross-layer drift)**, which the failure-mode catalog calls **critical for brownfield, high for greenfield** ([`failure-modes-v3`](../failure-modes-v3.md) §3 F34). F34 is *defined* in pace-layer vocabulary; an architecture organized around pace-layers can give F34 a first-class judge (the "Sentinel" — see §3.3) rather than relying on per-cycle reviewers to catch slow-layer violations.

4. **It works identically for both mandates because the layers are properties of any non-trivial software system, not properties of a development phase.** Brownfield starts with Architecture/Standards populated from the existing codebase; greenfield starts with them empty (cold-start, §5). The substrate primitives are mandate-agnostic; what changes per mandate is the *initial state* of each layer and the *direction of churn-rate gradient*.

5. **The "software factory vs. software company" CTR-F1 disagreement is at the metaphor layer; pace-layers is Brier's positive proposal**, not just his negative critique. Adopting Brier's frame *as architecture* honors the corpus's single explicit counter-voice on its own constructive terms while keeping UC1's factory framing as the operating mode at the fast layers.

**Why not substrate-vs-methodology (likely Track A's pick).** That axis answers "where does the boundary fall" but doesn't tell you what shape the factory takes. Pace-layers is shape-giving. Substrate-vs-methodology arises naturally as a **per-layer question** under pace-layering (each layer has its own substrate primitives and methodology overlay; see §3).

**Why not regime/Augmentation-vs-Automation (likely Track C's pick).** Regime is an *attribute* of a layer in this design, not the organizing principle. Pace-layering subsumes regime: fast layer = Automation eligible; slow layer = Augmentation required. Track C will likely cut the same architecture differently; we expect convergence on substrate primitives but divergence on which questions are first-class.

**Why not work-unit-class (D2 taxonomy).** Work-unit-class is what *flows through* the factory; pace-layer is the *structure* the flow moves through. A `regression-fix` is a Code-layer work unit; a `refactor` typically touches Plans+Code; an `initial-spec` lives at Specs layer; a `post-mvp-evolution` may cross Architecture. The mandate-fit matrix (D2) is *more easily filled in* under pace-layering because the layer-of-impact predicts the regime-of-cycle.

### 0.3 Verdict on unified-possibility

**Unified case is genuinely possible** under this axis. The architecture below works for both mandates with the **same substrate primitives** and **same layer set**; differences are confined to per-layer initial state, per-layer churn-rate priors, and per-layer cold-start procedure (§5). The hypothesis UC4 ("no single architecture works best for both") is **falsified for the layered-pace shape** (though we acknowledge in §7 that "works best" for a specific mandate × work-unit-class cell may still favor a specialized architecture; this is what D2's matrix exists to show).

### 0.4 Pre-response to Phase-3 unified-mandate-attacker

The attacker will argue this CANNOT work for one of the two mandates. The two most likely lines:

**Attack line A (against greenfield):** *"At cold-start, the Architecture and Standards layers are empty. The pace-layer architecture is a stack of layers that are mostly null. You don't have a pace-layered system; you have a Specs layer doing all the work, dressed up. UC4 wins: greenfield is spec-malleable, and your layers are vanity until day N."*

**Pre-response:** §5 cold-start treats Architecture and Standards layers as **populated from operator-curated priors** (adjacent-domain reference architectures, regulatory standards from followup [`10`](../../research/followup/10-governance.md), El Kaim intent-block invariants from report [`14`](../../research/14-el-kaim-book-intent-and-spec-authorship.md), prior-factory `docs/solutions/` from another run if available). These priors are not null; they are deliberately seeded. The Specs layer's malleability operates *under* these invariants; UC4 is honored at Spec/Plan, El Kaim is honored at Standards/Architecture. Day-0 is not flat-spec; it is constrained-spec under inherited invariants. The bootstrap-against-silent-failure question (brief §5.2) is answered by the Sentinel judge at the Architecture↔Spec boundary, which has signal even at day 0 (the inherited invariants are themselves checkable).

**Attack line B (against brownfield):** *"Brownfield's Architecture and Standards layers are not just 'pre-populated' — they are an undocumented, contradictory, archaeologically-buried mess. Your layered substrate assumes the layers are legible. Brownfield's reality is that the Architecture layer is implicit in 100k LOC of mutual entanglement. Your Sentinel has nothing to read."*

**Pre-response:** This is partly conceded — see §5.2 brownfield ingestion. The Architecture layer is *constructed* during a brownfield ingestion phase using F20-aware techniques (codebase-as-spec extraction, per report [`22`](../../research/22-academic-foundations.md) nutshell-bench framing; AFIS strategy-3 reverse-mode per report [`25`](../../research/25-requirements-engineering-foundations.md)). The ingestion phase is **time-boxed**, **trajectory-captured**, and **its output is itself a Standards-layer artifact** that humans approve before lights-out begins on the brownfield codebase. The architecture does not assume legibility; it makes legibility a precondition the ingestion phase produces. Where ingestion fails, the factory stays at L3 for that subsystem (regime declaration per §3).

### 0.5 Glossary (track-local vocabulary)

| Term | Meaning in this track |
|---|---|
| **Layer** | One of Brier's five: Code / Plans / Specs / Architecture / Standards. Each is an artifact-class with a churn cadence and regime declaration. |
| **Sentinel** | Judge agent dedicated to cross-layer-drift detection (F34). Reads slow-layer invariants; checks fast-layer artifacts against them. Distinct from per-cycle judges. |
| **Pace gradient** | Per-mandate distribution of *where churn lives*. Greenfield: gradient steep at Specs+Plans. Brownfield: gradient steep at Plans+Code under near-stable Architecture+Standards. |
| **Layer-regime** | The L3/L4/L5 declaration for a given layer. Code may be L5; Standards is L4 minimum. |
| **Invariant pack** | The Standards-layer artifact — El Kaim 9-field intent blocks + INCOSE GtWR rules + governance controls (AILCCP). Non-negotiable; changes require human ratification. |
| **Intake** | The brownfield-only Phase-0 process that constructs Architecture+Standards layers from an existing codebase. |
| **Cold seed** | The greenfield-only Phase-0 process that populates Architecture+Standards layers from operator-curated priors. |
| **Layer-handoff** | The substrate-mediated event when an artifact moves up or down a layer (e.g., a recurring fix-pattern at Code layer promoted to a Plan template, or a Plan pattern promoted to a Spec convention). Each handoff is a regime escalation/de-escalation event. |

---

## §1. The architecture in one paragraph

The factory is a **stack of five concurrent loops**, one per pace layer (Code / Plans / Specs / Architecture / Standards). Each loop has its own (i) artifact store on disk under version control, (ii) regime declaration (L5 at Code, L4 at Plans/Specs, L4-with-human-ratification at Architecture, L4-with-formal-sign-off at Standards), (iii) judge architecture appropriate to the layer's risk profile, (iv) churn cadence (Code: minutes; Plans: hours; Specs: days; Architecture: weeks; Standards: months/years), and (v) human-re-entry trigger set. A **Sentinel** judge watches the boundaries and surfaces cross-layer drift (F34) as a first-class signal. The **mandate** determines only the *initial state* of each layer (greenfield: empty plus Cold-Seed priors; brownfield: extracted via Intake) and the *churn-rate prior* (where work-units are expected to land). The same substrate primitives — trajectory capture (D-7), holdout discipline (D-4), watchdog (D-6), cost ceilings (D-5) — serve all five loops. Work-unit-classes (D2) map to layer-of-impact, which determines which loop owns the cycle and which regime governs it.

## §2. The five layers in detail

### 2.1 Code layer (fastest; L5-eligible)

- **Artifacts:** source files, test files, generated docs, lockfiles. Stored in the working repo.
- **Churn cadence:** minutes to hours. Many cycles per day.
- **Regime:** L5/lights-out eligible — *but only* for cycles that satisfy: (a) work-unit-class is `refactor` / `regression-fix` / well-specified `mvp` chunk, (b) Sentinel reports no upstream drift since last cycle, (c) all changes are confined to Code layer (no Plan/Spec/Architecture/Standards diffs in the same cycle), (d) holdout scenarios remain green.
- **Judge architecture:** per-cycle pass/fail gate against scenarios (D-2 + Round-1 D-2 default carried), plus same-model-different-role specialist critics (Anthropic Auto-Review pattern, report [`23`](../../research/23-anthropic-engineering-trilogy.md) §3.5) — this engages CTR-D4 / WEAK-5's third position (same-model-different-role) at the right layer.
- **Substrate primitives consumed:** sandbox; trajectory capture; cost ceiling; watchdog Daemon+Triage tiers.
- **Cold-start state — greenfield:** empty repo; populated cycle-by-cycle starting from the first Plan.
- **Initial state — brownfield:** existing repo; treated as ground truth.
- **F-modes most acute here:** F1, F2, F4, F27, F46.

### 2.2 Plans layer (hours; L4-default, L5-conditional)

- **Artifacts:** issue queue (Atelier-style per OQ-B4) and/or `.dot` pipelines (Attractor-style per report [`27`](../../research/27-dotfile-pipelines-as-product.md)) and/or change requests. The architecture is **plan-shape-agnostic** at this layer — operators can pick.
- **Churn cadence:** hours to a day. Plans are short-lived.
- **Regime:** L4 default. L5 only when the Plan is a *template instance* derived from a Standards-layer pattern (e.g., "this is the 47th occurrence of the `dependency-bump` plan-template; the template is approved").
- **Judge:** plan-quality judge that checks against Spec-layer requirements + Standards-layer invariant pack. F36 (instruction-following ceiling) is managed here by **per-plan requirement chunking** — no plan carries >10 requirement bullets (the empirical ceiling from report [`26`](../../research/26-prompt-underspecification-academic.md)). F37 (silent contradictory-prompt collapse) mitigation: plan-validation judge runs *before* dispatch and uses cross-model topology (report [`34`](../../research/34-lenny-howiai-personal-harnesses.md) `kevin/carl`), not same-model — because at the Plans layer the cost-per-cycle is high enough to justify cross-model.
- **Cold-start — greenfield:** first plan is hand-authored or human-ratified; subsequent plans agent-authored under Sentinel.
- **F-modes most acute here:** F25 (design starvation), F36, F37, F41 (under-defined-intent debt).

### 2.3 Specs layer (days; L4)

- **Artifacts:** Markdown specs in `agent specs/` (per Nystrom/Notion industrial anchor, report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md)) — *the spec git-history IS the changelog* (engages CTR-B7 by adopting Nystrom over Brier at this specific layer; Brier's pace-layer 3 framing is honored by the existence of the Architecture layer above, which provides the slow anchor Brier rightly demands).
- **Churn cadence:** days to weeks.
- **Regime:** L4 always. Spec changes are human-ratified at merge; agent-drafted in between.
- **Judge:** spec-quality judge against Standards-layer invariants. INCOSE GtWR R7/R8/R9 vocabulary-lint (F38) runs as deterministic CI here, not as LLM judge — because F51 (Ashby-deficient probabilistic guard) bites hard at the spec layer where the disturbance variety is largest.
- **Spec format:** prose Markdown + structured ID stable refs (resolves CTR-B1 by picking the StrongDM-NLSpec + Every-stable-IDs combination; rejects DOT-graph here and EARS-only because both are too narrow for the layer's role).
- **Spec-velocity stance:** Specs *do* move (Nystrom is right that history-as-changelog matters), but they move *under invariants* (Brier+El Kaim are right that something must be slower). This is the pace-layer architecture's positive answer to CTR-B7.
- **F-modes most acute here:** F3, F9 (spec overfitting), F18, F38, F39.

### 2.4 Architecture layer (weeks; L4-with-ratification)

- **Artifacts:** `ARCHITECTURE.md` per repo (Brier's recommendation, followup [`12`](../../research/followup/12-brier-pace-layers.md)) + El Kaim typed `ArchitectureSpecification` objects (report [`14`](../../research/14-el-kaim-book-intent-and-spec-authorship.md)) with `derivedFrom: DecisionRecord` and `evidenceSources` rules. ADR set lives here.
- **Churn cadence:** weeks to a couple of months.
- **Regime:** L4. Changes require: (i) Sentinel-approved derivation chain showing why downstream change requires the architecture change, (ii) explicit human approval gate (AILCCP Human Approval Gate, followup [`10`](../../research/followup/10-governance.md)), (iii) update of Standards-layer linkage where invariants are affected.
- **Judge:** structural-consistency judge (do all downstream Specs/Plans/Code still satisfy invariants?) + Sentinel cross-layer drift report.
- **Cold-start — greenfield:** Cold-Seed phase populates from operator-curated reference architectures + El Kaim's 9-field intent block (which acts as the **non-negotiable upstream anchor MISSED-3 demands**). UC4 spec-malleability is preserved at the Spec layer *below* this anchor.
- **Initial state — brownfield:** Intake phase extracts via codebase archaeology — file structure, dependency graph, observed runtime invariants, existing ADRs if any. Output is human-ratified before lights-out begins.
- **F-modes most acute here:** F34, F50, F41 deep variant.

### 2.5 Standards layer (months/years; L4-with-formal-sign-off)

- **Artifacts:** invariant pack (non-negotiable invariants per El Kaim Ch 3 §4.1), governance controls (AILCCP 48-controls subset declared in-scope), regulatory bindings (RSI declaration per report [`31`](../../research/31-caremark-rsi-board-exposure.md) if applicable, SB 53 binding if applicable), language/runtime/security floor (`.rules` Starlark DSL per report [`18`](../../research/18-openai-codex-substrate.md) — substrate primitive at this layer because it is auditable-V&V-by-rejection).
- **Churn cadence:** months to years. Changes are rare events, not cycles.
- **Regime:** L4 minimum. For governance-exposed deployments (per F30, F43), changes require board-visibility per Caremark-line discipline.
- **Judge:** the Standards layer judges *itself* via formal-methods-style checks where possible (deterministic `.rules` enforcement); LLM judges are explicitly NOT trusted at this layer (F51, F33).
- **Cold-start — greenfield:** Cold-Seed populates from regulatory baseline (followup [`10`](../../research/followup/10-governance.md)) + INCOSE GtWR + adjacent-domain norms.
- **Initial state — brownfield:** Intake extracts implicit invariants from production telemetry, existing tests, and operator interview. Gaps surface as DECISIONS-PENDING.
- **F-modes most acute here:** F12, F30, F33, F43, F44, F51 (every security-class and governance-class F-mode lives here).

## §3. The Sentinel and the cross-layer regime matrix

### 3.1 Sentinel role

The Sentinel is the **cross-layer drift judge** — a dedicated agent that:

1. Watches every artifact-mutation event from any layer (events sourced via D-7 trajectory capture).
2. For each downstream artifact, verifies the derivation chain to the nearest upstream invariant (`derivedFrom` per El Kaim) still holds.
3. Emits a **drift-score** per layer-pair (Code↔Plans, Plans↔Specs, Specs↔Architecture, Architecture↔Standards).
4. Triggers human re-entry (Patrol-tier watchdog escalation, per D-6 / Round-2 C14) when drift exceeds threshold on the Architecture↔Standards boundary; triggers L5→L4 regime de-escalation for the affected work-unit-class when drift exceeds threshold at any lower boundary.

This makes F34 (cross-layer drift) — currently rated **critical for brownfield, high for greenfield** ([`failure-modes-v3`](../failure-modes-v3.md) §3 F34) — a first-class architectural concern with a dedicated mitigator.

### 3.2 Regime-per-layer matrix (resolves CTR-A4 / OQ-B1)

| Layer | Regime default | L5 eligibility | Per Jaymin bar (OQ-B6) |
|---|---|---|---|
| Code | L5 (lights-out per UC1) | Yes, conditional on §2.1 (a)–(d) | Must clear Automation Mode (≥90% K=5, 5-of-5 paraphrase, zero medium+ safety incidents) |
| Plans | L4 | Yes, only for Standards-derived templates | Augmentation Mode at minimum (≥70%, ≥3-of-5); template-instance plans may run at Automation |
| Specs | L4 | No | Augmentation Mode |
| Architecture | L4 with human ratification | No | Augmentation + Caremark-line discipline |
| Standards | L4 with formal sign-off | No | Augmentation + governance ratification |

**This is how lights-out (UC1) survives Jaymin's L5-anti-pattern citations:** lights-out applies to *cycles*, and cycles live at layers; only Code-layer cycles run lights-out, and only when the upstream layers are stable and the cycle is within the eligibility conditions. Shapiro's L4 self-position is preserved at every layer he actually operates at (Plans and above). Jaymin's CodeRabbit/Veracode/METR numbers are scoped to the layer they were measured at (code-level review/generation) and become acceptance-thresholds the Code layer's judges must clear, not blanket refutations.

This also resolves **CTR-A4** by making the vocabulary mapping explicit: "lights-out" in UC1 maps to "L5-eligible at the Code layer under conditions"; it does NOT map to "L5 uniformly across the factory."

### 3.3 Engagement with MISSED-3 (El Kaim vs. UC4)

El Kaim's 9-field intent block with non-negotiable invariants **lives at the Standards layer.** UC4's spec-malleability is a property of the **Spec layer** (and to some extent Plans). The architecture treats both as true at their respective layers — Brier's pace-layer framing is precisely the corpus's mechanism for holding both. This **falsifies the framing of MISSED-3 as a flat contradiction** while preserving the empirical truth on both sides. If UC4 insists spec-malleability extends all the way up to the Standards layer, then this architecture cannot serve that interpretation — but that interpretation would also rule out any governance-aware factory, so the conflict is at the constraint level, not the architecture level.

## §4. §4 defaults: accepted vs challenged (all 7 marked per D3)

| # | Default | Stance | Justification / Citation |
|---|---|---|---|
| **D-1** | Specs are durable version-controlled human-curated artifact | **accepted with justification** | At the Specs layer specifically, this is exactly Nystrom's industrial practice (report [`35`](../../research/35-lenny-howiai-spec-driven-and-team-ops.md)) and the architecture builds the Specs loop around it. The default is preserved; what this architecture adds is that *additional* slower layers exist above the Spec (Architecture, Standards) per Brier (followup [`12`](../../research/followup/12-brier-pace-layers.md)) — so spec is durable but not the most-slow artifact. |
| **D-2** | Scenarios live outside the codebase as a holdout set | **challenged** | Per fragile-default flag in brief §4. Under this architecture, scenarios live at **Specs+Plans layers** under version control alongside other artifacts; for brownfield, production traces and existing test suites are *additional* scenario sources that live *inside* the running codebase (resolving CTR-B5 — and consistent with the sharper reading in CTR-B5's WEAK-3 sharpening, which shows StrongDM's own practice already permits scenario-equivalents inside the runtime, per report [`01`](../../research/01-strongdm-factory.md) §1). Substrate-enforced holdout discipline (D-4) is what matters, not location. |
| **D-3** | Agent = Model + Harness | **challenged** | Per fragile-default flag in brief §4 and MISSED-8 (CTR-C10): report [`37`](../../research/37-academic-llm-agent-collusion.md) provides empirical evidence that natural-language-of-prompt is a behaviour-influencing harness parameter the formula doesn't model. This architecture uses an expanded vocabulary: **Agent = Model + Harness + Scaffold + Natural-Language-Register** at all layers; the Sentinel watches the latter two as drift sources too. |
| **D-4** | Holdout discipline substrate-enforced | **accepted with justification** | Acceptance criteria withheld from builder agents at *every* layer's cycle is even more important under pace-layering, because the Sentinel itself must not see the holdout. Substrate provides the boundary uniformly. |
| **D-5** | Hard cost ceilings non-optional in CI | **accepted with justification** | Per-layer ceilings (Code cycles cheapest, Standards changes most expensive but rare) — substrate enforces; methodology declares. Engages CTR-E6 (CaMeL ~7-point utility tax) by allowing per-layer ceilings to include security-tax budgets explicitly. |
| **D-6** | Tiered watchdog (Daemon/Triage/Patrol) | **accepted with justification** | Patrol tier is exactly the layer-drift-escalation surface the Sentinel emits to. Daemon at Code-cycle level; Triage at Plan-execution level; Patrol at Architecture↔Standards drift. |
| **D-7** | Trajectory capture cheap, production-tested | **accepted with justification** | Per OpenHands V1 measurements (report [`11`](../../research/11-openhands-substrate-audit.md)); used uniformly across all five layer-loops. The Sentinel's input is the trajectory stream. |

## §5. Cold-start (MANDATORY per brief §5; both mandates' bootstraps)

### 5.1 Greenfield Cold-Seed (day 0 → day N)

**Day 0 inputs (operator-curated priors, per the revised greenfield definition in glossary):**

1. **Standards layer seed:**
   - Regulatory baseline from followup [`10`](../../research/followup/10-governance.md) (AILCCP 48 controls; pick the subset applicable to target deployment regime — consumer/SaaS/regulated).
   - INCOSE GtWR R1–R42 + EARS canonical guide (report [`25`](../../research/25-requirements-engineering-foundations.md)) — vocabulary-lint and structural-quality rules as deterministic CI checks (mitigates F38).
   - Caremark-line declaration: RSI status per the three-part test (report [`31`](../../research/31-caremark-rsi-board-exposure.md)) — *the factory must declare what it is before it ships* (engages F43 board-visibility gap at day 0).
   - Language/runtime/security floor as `.rules` Starlark DSL (report [`18`](../../research/18-openai-codex-substrate.md)).

2. **Architecture layer seed:**
   - El Kaim 9-field intent block with non-negotiable invariants (report [`14`](../../research/14-el-kaim-book-intent-and-spec-authorship.md)) — this is the **upstream stability anchor** MISSED-3 says the corpus's deepest spec-authorship anchor requires.
   - Adjacent-domain reference architectures (operator picks 1–3 exemplars from public corpora).
   - Initial `ARCHITECTURE.md` (Brier's primitive, followup [`12`](../../research/followup/12-brier-pace-layers.md)) — human-authored at day 0; subsequent edits agent-drafted under Sentinel.

3. **Specs / Plans / Code layers:** empty.

**Day 0 → Day N trajectory:**

- **Day 0–2:** human-authored initial Spec (under invariants), human-authored first Plan (under Spec), agent-drafted Code cycles at L4 (NOT L5 yet — Sentinel has no baseline). Trajectory capture begins.
- **Day 2–14:** Sentinel accumulates baseline; if K=5 consistency at Code layer reaches Jaymin's Automation thresholds (≥90% K=5; 5-of-5 paraphrase; zero medium+ safety incidents per report [`09`](../../research/09-jaymin-book-harnesses-practices-mental-models.md) §5.5), Code-layer regime promotes to L5-conditional. Plan-template extraction begins (recurring plan-shapes promoted to Standards-derived templates).
- **Day 14+:** steady-state pace-layered operation. Periodic operator audit at the Architecture↔Standards boundary (governance cadence).

**Bootstrap-against-silent-failure (brief §5.2 question):** The Sentinel has signal at day 0 because the seeded invariants are deterministically checkable; even with no historical trajectory, the *vertical* derivation-chain check works. Plus: the K=5 consistency bar prevents L5 promotion before the Sentinel has accumulated enough trajectory data — silent failure is gated at the regime-promotion boundary.

**Engagement with F25 (design starvation):** cold-start is *exactly* design-starvation territory ([`failure-modes-v3`](../failure-modes-v3.md) §2 F25 critical for greenfield). The mitigation is that Day 0–2 is *human-authored*; the factory does not pretend to be lights-out until baseline is established. UC1 is preserved at steady-state, not at day 0.

### 5.2 Brownfield Intake (day 0 → day N)

Brownfield's "cold-start" is **codebase ingestion**, not knowledge-priming:

**Intake phase (time-boxed, e.g., 1–4 weeks):**

1. **Code layer:** declared as-is; ground truth.
2. **Architecture layer extraction:** dependency-graph extraction (deterministic tooling); module-boundary inference (LLM-assisted but human-ratified); ADR catalog audit (if any). Output: draft `ARCHITECTURE.md` + draft typed `ArchitectureSpecification` objects.
3. **Standards layer extraction:** existing `CONTRIBUTING.md`, lint configs, security policies, runtime invariants from production telemetry (per CTR-B5 sharpening — these are *legitimate scenario sources from inside the codebase*). Operator interview surfaces implicit invariants.
4. **Specs layer:** initially empty; populated as work units arrive (no retroactive spec-back-fill — F9 spec-overfitting risk too high).
5. **Plans layer:** existing issue queue (Atelier-style per OQ-B4) ingested; F40 (last-mile drift) addressed by per-Plan completion-criteria attached at intake.

**Sentinel boot:** trained on the extracted Architecture+Standards layers; ready to flag drift from intake-day-1.

**Regime at intake-day-1:** L3 for all layers. Promotion to L4 (steady-state brownfield default) happens per-subsystem as Sentinel accumulates signal. L5 at Code-layer only for subsystems where ingestion produced clean invariants AND scenario coverage exists.

**Engagement with F20 (maintenance vs. greenfield asymmetry, critical for brownfield):** Intake is the *answer* to F20 — the factory does not pretend brownfield is greenfield by hand-waving the pre-existing layers. Layered ingestion is the structural mechanism.

## §6. Substrate vs. methodology placement (engages OQ-B2)

Phase 4 will draw this boundary formally; this track's working claim:

- **Substrate (mandate-agnostic, layer-agnostic):** trajectory capture (D-7); sandbox; holdout enforcement (D-4); cost ceilings (D-5); tiered watchdog (D-6); `.rules` DSL enforcement (deterministic V&V); OTEL five-event export (report [`18`](../../research/18-openai-codex-substrate.md)); cross-model judge routing (engages CTR-D4 / CTR-D7 / CTR-D8 — by making model-family-diversity *available* without mandating it; CaMeL-class typed-perimeter security primitive (followup [`08`](../../research/followup/08-security-primitives.md)).

- **Methodology (per-layer; pace-layer-shape):** the five-loop control structure itself; the Sentinel role; the regime-promotion logic; the layer-handoff protocol; cold-start procedures (Cold-Seed / Intake); judge-architecture choices per layer.

The substrate-vs-methodology boundary therefore *runs orthogonally* to the pace-layer boundary — substrate is the *vertical* spine; methodology is the *horizontal* per-layer logic.

## §7. Mandate-fit projection (per D2 schema)

```yaml
mandate-fit:
  initial-spec: both       # Specs layer; both mandates use same loop, different cold-start
  refactor: both           # Plans+Code layers; same loop both mandates; brownfield more frequent
  mvp: greenfield          # Architecture+Specs+Plans+Code all active at once; greenfield-shaped
  post-mvp-evolution: both # Plans+Code primary, occasional Specs touch; same loop both mandates
  regression-fix: both     # Code-layer-only; L5-eligible; same loop both mandates
```

**Where this architecture is genuinely strongest:** `regression-fix` and `refactor` for both mandates (Code+Plans loops, mature L5/L4-template eligibility, Sentinel reliable). `post-mvp-evolution` for brownfield (Intake-populated upper layers make Sentinel signal strong). **Where it is acceptable but not differentiating:** `initial-spec` and `mvp` for greenfield (Cold-Seed gets you there but a Refinery-style spec-primary architecture might run faster at this cell; pace-layering's cost is upfront seeding). **Where it punts:** governance-tier cells where Standards-layer changes are frequent (the architecture is built for slow Standards; rapid-evolution-of-Standards is a different shape entirely).

## §8. Open items and DECISIONS-PENDING

1. **DECISIONS-PENDING — work-unit-class taxonomy adequacy.** Per D2, the 5-class taxonomy is illustrative. Under pace-layering, the natural taxonomy is *layer-of-impact*: `code-only / plan-shape / spec-touching / architecture-touching / standards-touching`. This is a different cut. → Phase 4 ADR.
2. **DECISIONS-PENDING — Sentinel implementation as substrate vs. methodology.** §6 places Sentinel role on methodology side; the *judge-routing* it consumes is substrate. The boundary is fuzzy. → Phase-5 ADR on Sentinel role.
3. **DECISIONS-PENDING — pace-layer count.** Brier names 5. The architecture may need more (e.g., a Test layer between Code and Plans) or fewer. → Lean-eval brief.
4. **TBD — engagement with F35 (Federation-as-Family Drift).** If the factory itself becomes a family of pack-instances (e.g., per Gas City pack model, report [`38`](../../research/38-gas-systems-substrate.md)), F35 bites at the meta-layer. Phase 4 should address whether this architecture is a "pack" or "the engine."
5. **Falsifiability check:** if any Phase-2 track (greenfield-only or brownfield-only) produces a clearly stronger architecture for a specific mandate × work-unit-class cell than this architecture's projection in §7, that cell is a candidate for specialization (consistent with D1's mandate that unified is one *option*, not the required answer).

---

## Report-back (6 sentences)

**Chosen axis:** Brier's five pace-layers (Code / Plans / Specs / Architecture / Standards) with each carrying its own regime declaration, judge, and cadence; mandate becomes per-layer initial-state and churn-gradient, not a top-level branch. **Verdict on unified-possibility:** unified is possible and the pace-layered shape is genuinely strong for both mandates; UC4's "no single architecture works best" is falsified for the shape (though specialized architectures may still win specific D2 cells). **Architectural choices:** (i) regime is per-layer not per-factory (L5 at Code only, L4 above, dissolving CTR-A4); (ii) a dedicated Sentinel judge mitigates F34 at every layer-boundary; (iii) cold-start has two mandate-specific entry procedures (Cold-Seed for greenfield seeds Standards+Architecture from operator priors and El Kaim invariants; Intake for brownfield extracts them from the codebase) on the same substrate. **§4 markings:** D-2 and D-3 challenged (per fragile-default flags); D-1, D-4, D-5, D-6, D-7 accepted with justification. **Most-cited CTR/F-mode:** CTR-A4 (lights-out vs. L5 vocabulary mapping) plus MISSED-3 (El Kaim invariants vs. UC4) on the contradictions side; F34 (cross-layer drift) on the failure-mode side. **Expected differences from A and C:** A will likely organize around substrate-vs-methodology split (the Round-2-default frame), making different choices about substrate primitives but converging on similar mandate-agnostic judge/sandbox/watchdog primitives; C will likely organize around regime (Augmentation/Automation) or work-unit-class, producing a flatter architecture that handles MISSED-3 as a per-unit-class declaration rather than as a layer-of-anchor — convergence expected on substrate primitives, divergence expected on whether F34 is first-class architectural (this track) or absorbed into per-cycle judging (likely A/C).
