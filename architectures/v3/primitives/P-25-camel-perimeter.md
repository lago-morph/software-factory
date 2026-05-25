# P-25 — CaMeL-class typed perimeter

Per-primitive Phase-3.5 buildability sketch. Dispatched per the [hybrid (option C) shape](../decisions/auto-001-phase-3.5-dispatch-shape.md#revised-decision) under the [two-part rule](../phase-3.4-decisions-resolved.md#refined-two-part-rule-for-accepting-a-substrate-primitive). Claimed by [BF-S §1 S-5](../tracks/brownfield-substrate-first.md) and [BF-M cycle stage 5](../tracks/brownfield-methodology-first.md).

---

## Contract restatement

P-25 is the **capability-typed boundary** through which every production-adjacent read or write performed by a builder agent must pass. Its surface mediates tool-call edges — not prompt-text edges — so the defence operates on dataflow, not on adversarial-string filtering. Contract elements:

- **Typed-interpreter pattern.** A custom interpreter (per CaMeL: a restricted Python AST executor) runs the *plan* the Privileged LLM emits; the LLM itself never directly invokes production tools. Plan steps are interpreted; tool calls are dispatched by the interpreter after capability check.
- **Capability tokens per value.** Every value flowing through the interpreter carries tags: `provenance` (User / CaMeL-derived / `tool:<id>`), `readers` (Public | set-of-users), and optional inner-source. Tools are typed by required-capability sets.
- **Allowed-call-set per token.** For each call, the interpreter compares the token's capability profile to the tool's required policy; mismatch → `CapabilityError`, no call dispatched.
- **Production-adjacent isolation.** When the surrounding work-unit class is flagged `production-adjacent`, the perimeter is mandatory (per [F44](../failure-modes-v3.md#f44--lethal-trifecta-production-scissors-default) production-scissors-default-off); otherwise the cycle may run in a sandbox without the perimeter. The substrate enforces the regime tag — not the agent ([F53](../failure-modes-v3.md) voluntary-discipline fragility).
- **NORMAL vs STRICT modes** (per CaMeL paper §4.4) for side-channel mitigation under high-stakes calls.

## Construction path

**Primary tool: the CaMeL reference implementation** ([`google-research/camel-prompt-injection`](https://github.com/google-research/camel-prompt-injection), released alongside the [Debenedetti et al. 2025 paper](../../../research/followup/08-security-primitives.md#3-camel--capability-typed-program-model-debenedetti-et-al-march-2025); paper-body archived under `reference-only/camel-paper/`). The reference impl ships the Privileged-LLM / Quarantined-LLM split, the custom Python AST interpreter, and a capability-propagation lattice already exercised on the AgentDojo benchmark (77% provable-security task success vs 84% undefended baseline).

**Integration sentence.** P-25 wraps the CaMeL interpreter as a substrate service: BF-M stage-5 calls `CaMeL.execute(plan_ast, capability_profile, policy)` where `plan_ast` is the Privileged LLM's emitted Python AST, `capability_profile` is the cycle's `{readers, provenance}` token set derived from BF-S's S-3 telemetry partition + S-4 attribution store, and `policy` is the per-work-unit-class allowed-call-set; the interpreter dispatches concrete tool calls through P-29 (policy mediator) only after token-vs-policy reconciliation, returning `{result, capability-trace, mode-used}` to P-05 for trajectory capture. Plan steps whose required readers are not subset-of the carrier's readers raise `CapabilityError` and never reach the tool surface.

**Prior-art alternatives considered.** (a) **Cap'n Proto capability tokens** — well-engineered capability transport but lacks the interpreter-as-orchestrator pattern that's load-bearing for CaMeL's data-flow guarantee; usable for the token-transport layer inside the interpreter, not as the perimeter itself. (b) **OPA / Cedar** for the policy DSL — adopted as P-29's substrate; P-25 *invokes* OPA at the capability-vs-policy reconciliation step rather than reimplementing it. (c) **eBPF for kernel-level capability enforcement** — defence-in-depth below the interpreter (e.g., to enforce egress allow-lists on the tool dispatcher's process) but does not give the dataflow-tracking the typed interpreter provides. The chosen integration is therefore: CaMeL interpreter (primary), OPA inside it (policy), eBPF/sandbox below it (defence-in-depth).

## CaMeL utility-tax engagement (BF-M OQ-T3)

[BF-M §6 OQ-T3](../tracks/brownfield-methodology-first.md) flags that the utility-tax acceptance criterion is not set — the corpus reports a headline ~7-point tax (77/84 on AgentDojo) but the paper-body fetch [REFUTES](../../../research/followup/08-security-primitives.md) any read of this as uniform: per-model and per-suite variance is large, Travel suite dominates the loss, and some configurations *improve* utility. Engagement for buildability:

- **A-priori measurability — NO.** The tax depends on (i) the model family driving the Privileged LLM, (ii) the tool-call density of the work-unit class, (iii) how often the Quarantined LLM raises `NotEnoughInformationError`, and (iv) the strictness of the policy DSL. None of these can be characterised before the perimeter is wired into a specific deployment.
- **Use-time measurable — YES**, by holding out a fraction of work-units to run perimeter-off vs perimeter-on and comparing task-success-rate. This is what BF-M's "Phase-5 ADR" deferral acknowledges: the *acceptance criterion* is a calibration step, not a buildability question. The perimeter is buildable; *whether the tax is tolerable for a given work-unit class* is a per-deployment policy decision.

**Implication for P-25's buildability:** the tax is real and structurally non-zero, but it does not block construction. It does flag a **calibration obligation** the substrate must support — the perimeter must be *configurably bypassable* per work-unit-class with the bypass itself substrate-logged (F53-resistant: bypass cannot be set by the agent under review). This is a designed-system feature, not research-grade uncertainty.

## Per-candidate notes (no same-vs-distinct verdict)

- **BF-S §S-5** claims P-25 as the **substrate perimeter / trifecta-closure layer** — production-scissors-default-off, read/write asymmetric, sandboxed, with the CaMeL ~7-point tax accepted at substrate level. Cross-model judge availability and guard-bypass detection ([F56](../failure-modes-v3.md#f56--guardrail-bypass-under-stress-replit-class-incident)) are co-located here.
- **BF-M cycle stage 5** invokes P-25 as a **production-adjacent boundary** wrapped around the build stage when the work-unit-class regime is `production-adjacent`. BF-M does not own the perimeter; it queries it.

Both claims point at the same contract surface (capability-typed boundary, CaMeL-class). Whether this is one primitive or two is a Phase 4.2 same-vs-distinct call deferred per the [scoping principle](../phase-3.4-decisions-resolved.md#scoping-principle-immutable-overrides-any-conflicting-framing-in-the-integration-brief).

## Corpus-why citation

[F12 — Lethal trifecta / prompt injection](../failure-modes-v3.md#f12--lethal-trifecta--prompt-injection) (the originating Willison framing); [F33 — Adversarial-prompt defeat of LLM-based security analysis](../failure-modes-v3.md#f33--adversarial-prompt-defeat-of-llm-based-security-analysis); [F44 — Lethal-Trifecta Production-Scissors Default](../failure-modes-v3.md#f44--lethal-trifecta-production-scissors-default) (Shapiro / OpenClaw incident — substrate-default rather than per-agent discipline). The F12 → F33 → F44 cascade is the canonical motivation: prompt-level filtering cannot be hardened ([Schulhoff §5, "impossible to solve entirely"](../../../research/followup/08-security-primitives.md)); the defence must shift to capability-typed program models. Primary anchor: [followup-08 §3 CaMeL paper-body](../../../research/followup/08-security-primitives.md#3-camel--capability-typed-program-model-debenedetti-et-al-march-2025) + AgentDojo benchmark. Practitioner-side anchor: [report-32 Shapiro §5 R1–R5 rules](../../../research/32-shapiro-completion-chat-agent-claw.md) (read-anything-but-only-draft; thumbprint every artifact; "do not give it production scissors").

## Research-grade-uncertainty flag

**`partial — utility-tax calibration only`.** The perimeter itself is **not** research-grade: the CaMeL reference implementation exists, is benchmarked, and ships with the interpreter + capability lattice intact. The standing research-grade uncertainty is the **per-deployment utility-tax calibration** — whether the ~7-point headline tax holds for *this* factory's mix of work-unit-classes is empirically open and depends on the work mix, model choices, and policy strictness. BF-M's OQ-T3 explicitly defers the acceptance criterion to Phase-5 ADR; this sketch concurs that the acceptance criterion is a calibration question, not a buildability question. Two secondary uncertainties acknowledged: (i) text-to-text attacks (phishing, summary-tampering with no dataflow) are *explicitly out-of-scope* for CaMeL per `main.tex:167`; the factory must combine P-25 with content review for that class; (ii) ROP-analogy gadget attacks on the capability lattice are flagged by the paper authors as suspected-feasible — defence-in-depth (eBPF, sandbox) is the mitigation, not stronger typing.

## Buildability verdict

**`designed-system`** (with the partial research-grade flag on utility-tax calibration noted above). The core perimeter is buildable today against a released reference implementation with named prior art (Cap'n Proto, OPA, eBPF) for the integration layers around it. The construction path is concrete: wrap the CaMeL interpreter as a substrate service, integrate OPA for the policy DSL, log capability traces to P-05, expose a configurable per-work-unit-class bypass. The structural cost (utility tax) is real but calibratable at use time, not a-priori — which is a designed-system feature (configurable bypass + substrate-logged), not a research-grade obstacle.
