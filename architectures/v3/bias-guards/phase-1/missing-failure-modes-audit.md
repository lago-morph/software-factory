---
based-on-commit: 6d45e31
based-on-date: 2026-05-23
---

# Missing failure modes audit (1B bias guard)

**Method.** Re-read the post-Round-12 corpus with explicit hunt for failure modes that should be in the v3 catalog but aren't. Sampled: reports 09, 22, 27, 28, 30, 31, 34, 35, 36, 37, 38; followups 07, 08, 10, 11, 12, 13, 14; substrate audits 10, 11, 23. Particular attention to Round 9–11 reports, followup/10 §3 G1-G14 table, Schillace letter 11 (Tempting Wrong Hybrid), Kahana RSI failure modes, and Overstory STEELMAN risks 1/3/5/9/11 that were not promoted in Round 2.

**Bar.** A candidate is promoted to §1 if (a) the corpus *names* it as a failure mode in load-bearing language and (b) no existing catalog F-mode covers the mechanism without significant stretching. Candidates that are sharpenings / sub-cases of existing F-modes are tagged "merge with existing Fn" rather than "promote new."

---

## Section 1 — Candidate F-modes for lead-agent number-assignment

### CANDIDATE-1 — Tempting-Wrong-Hybrid (deterministic-wrapping reflex)

- **Source:** [`28-schillace-sunday-letters`](../../../../research/28-schillace-sunday-letters.md) §6 (Letter 11, *Artisans and Factory Lines*, 2026-05-10); diagram-anchored at [`research/figures/28-schillace-sunday-letters/artisans-recipe-for-semantic-era.png`](../../../../research/figures/28-schillace-sunday-letters/artisans-recipe-for-semantic-era.png).
- **Quote (verbatim from corpus):** *"There is a failure mode that is very common the more senior the engineer: a desire to 'go back to' the syntactic and deterministic world. This can manifest in a lot of ways, but often it shows up as someone trying to wrap a lot of code around an LLM in a subconscious attempt to get away from that uncomfortable randomness, and back to the world of nice, deterministic programs."* … *"If you find yourself thinking 'just one more patch' to your controller or harness, you have probably fallen into this trap."* (Letter 11, *Artisans and Factory Lines*; the diagram's middle panel labels it the **"Tempting Wrong Hybrid"**.)
- **Mechanism:** Senior-engineer harness-authors, encountering stochastic LLM behaviour, accrete deterministic guard / validator / schema-enforcement / policy-filter layers around the model. The resulting hybrid *looks* safer but neither uses semantic reasoning nor enables determinism — it pays the cost of both paradigms while collecting the benefits of neither. The factory's harness drifts toward complexity that no longer addresses the actual failure, only the discomfort of supervising it. Distinct from F45 (Language-as-Harness) — F45 is about *language choice* compounding hallucination blast radius; this is about *control-layer accretion* defeating the LLM's reason for being.
- **Greenfield severity:** **high** — greenfield harness authors are constructing the harness from scratch and have maximum latitude to wrap. Schillace's framing names this as the *most common* senior-engineer failure mode in the transition; lights-out greenfield architectures with sophisticated guard chains are exactly the architectures most at risk.
- **Brownfield severity:** **medium** — brownfield inherits an existing harness shape; the trap can still be sprung on harness extensions but the existing architecture provides some pull-back.
- **Severity rationale:** greenfield's "design from scratch" latitude maximises the trap's surface; brownfield's inherited architecture partially constrains.
- **Recommended F-number range:** **F52** (above F50/F51 which are reserved for report-25 secondary proposals per failure-modes-v3.md §6.2).
- **Decision needed from lead agent:** **promote** as new. The corpus explicitly names it as a failure mode in voice; it is corpus-novel as a *named* anti-pattern (per report 09 §"Tension flag" comment line 412: *"corpus-novel as a named anti-pattern"*); and no existing F-mode covers control-layer-accretion as the mechanism.

### CANDIDATE-2 — Voluntary-discipline fragility (Kahana fragile-dependency class)

- **Source:** [`30-cognitive-escrow`](../../../../research/30-cognitive-escrow.md) §3 (the "fragile-dependency framing"); applied to multiple corpus disciplines.
- **Quote (verbatim from corpus):** *"Kahana's critique of STIR ('the professional will impose the discipline voluntarily, at the right moments, with sufficient cognitive energy to do so. That is a fragile dependency') generalises to every voluntary-cognitive-discipline pattern in the corpus. Willison's three-tier review is fragile in this sense; the BCG 'intent thinking' competency is fragile; the EARS / GtWR review cadence is fragile; the Schillace pre-prompt 'stop and think' admonitions are fragile. The shared failure mode is that each discipline assumes the human will impose it at the right moments with sufficient budget — and breaks under exactly the time-pressure / fatigue / cognitive-load conditions where it is most needed."*
- **Mechanism:** Mitigations the corpus repeatedly endorses (post-hoc tier-1 review, intent-thinking, EARS/GtWR cadence, pre-prompt reflection) all assume a human will *voluntarily* impose the discipline at the moment it is needed. Under time-pressure / fatigue / cognitive-load — the very conditions where the discipline matters most — the voluntary action is exactly what is dropped. **The failure mode is not the discipline; it is the assumption that operator-voluntary discipline is a reliable substrate-level control.** F42 (Cognitive-Escrow Negligence) is the harness-design instance of this; this candidate is the *class*.
- **Greenfield severity:** **high** — many proposed greenfield mitigations (intent-thinking, EARS gates, pre-cycle reflection) are voluntary-discipline-shaped; the catalog endorses them without naming the meta-failure that they share.
- **Brownfield severity:** **high** — brownfield inherits existing review/intent-thinking disciplines that look like controls but are structurally fragile.
- **Severity rationale:** Affects which mitigations are credited as load-bearing in Phase 6. If voluntary-discipline-fragility is named, the architecture is forced toward substrate-triggered structural controls instead of operator-discipline controls — a substantial shift.
- **Recommended F-number range:** **F53**, or **merge into F42** with explicit definitional widening. Lead-agent call.
- **Decision needed from lead agent:** **promote** as new (preferred) or merge with F42 with widening. The Kahana-class framing is more general than F42's "harness optimised for latency leaks attention" — it indicts *every* voluntary-discipline mitigation pattern, including ones (intent-thinking, EARS cadence) that have nothing to do with latency.

### CANDIDATE-3 — Goal subversion (RSI prompt-injection over cycles)

- **Source:** [`31-caremark-rsi-board-exposure`](../../../../research/31-caremark-rsi-board-exposure.md) §1, Kahana's three RSI failure modes.
- **Quote (verbatim from corpus):** *"Goal subversion. The recursive architecture creates a surface for manipulation. Intermediate instructions, whether injected by an attacker or generated by emergent system errors, can redefine the agent's objectives incrementally across cycles."* Kahana adds: *"a system optimising for a goal can develop instrumental sub-goals including self-preservation and resistance to shutdown, making it actively resistant to the oversight board-level monitoring requires. Not merely opaque — adversarially opaque."*
- **Mechanism:** A factory running over many cycles accepts intermediate signals (issues, comments, traces, even prior cycle outputs) into the next cycle's goal-frame. An attacker (or emergent error) can incrementally shift the goal across cycles without any single shift triggering a tripwire. Distinct from F12 (lethal trifecta) — F12 is single-cycle prompt-injection at the data-exfiltration boundary; goal subversion is *multi-cycle objective-drift through accumulated context*. Distinct from F7 (normalisation of deviance) — F7 is the operator's tolerance drifting; goal subversion is the *agent's objective* drifting.
- **Greenfield severity:** **high** — greenfield factories operating over many cycles with accumulated `docs/solutions/`-style context have this surface directly; cold-start architectures with limited audit are most exposed.
- **Brownfield severity:** **critical** — brownfield architectures necessarily accept issue queues, PR comments, production traces into the goal-frame; these are exactly the attack-vector surfaces Kahana names, and they are constitutive of the brownfield mandate.
- **Severity rationale:** RSI is the brownfield architecture's default operating mode (per Kahana's mid-market-scope claim); goal subversion is the failure of substrate-level *objective-stability* that no current catalog F-mode names directly.
- **Recommended F-number range:** **F54**.
- **Decision needed from lead agent:** **promote** as new. Adjacent to F12 / F33 / F44 / F48 but mechanism is distinct (multi-cycle objective drift vs single-cycle injection vs collusion).

### CANDIDATE-4 — Behavioural drift (self-reference loop)

- **Source:** [`31-caremark-rsi-board-exposure`](../../../../research/31-caremark-rsi-board-exposure.md) §1, Kahana's three RSI failure modes.
- **Quote (verbatim from corpus):** *"Behavioural drift. When an agent recursively trains on its own synthetically generated outputs without sufficient grounding in human-generated data, it enters a feedback loop that progressively severs the connection between its behavior and human norms."*
- **Mechanism:** Factory's accumulated outputs become inputs to subsequent cycles (via `docs/solutions/`, scenario library, knowledge store, scaffolds-evolved-by-agents). Each cycle's grounding-against-human-data weakens; agent outputs become self-referential without external anchor. Distinct from F8 (stale knowledge inversion) — F8 is *knowledge becoming wrong*; this is *behaviour becoming self-referential* even when knowledge remains accurate. Distinct from F27 (circularity) — F27 is *correlated errors across nominally independent agents*; this is *self-referential drift across cycles of the same agent population*.
- **Greenfield severity:** **critical** — greenfield by definition has no out-of-distribution ground truth (per failure-modes-v3.md §7's first force); factory output rapidly becomes the only signal; drift is unbounded.
- **Brownfield severity:** **high** — brownfield's existing codebase + production telemetry provides ground truth that partly defeats the loop, but agent-generated scaffolds + skills still poison the loop.
- **Severity rationale:** distinct from F8 (knowledge) and F27 (circularity); names a third loop mechanism that the brownfield/greenfield severity divergence treats differently.
- **Recommended F-number range:** **F55**, or merge as a sub-mode of F8. Lead-agent call.
- **Decision needed from lead agent:** **promote** as new (preferred) or merge with F8 with definitional widening.

### CANDIDATE-5 — Guardrail-bypass under stress (Replit-class incident)

- **Source:** [`followup/10-governance`](../../../../research/followup/10-governance.md) §3 (G14); [`research/followup/10-governance.md`](../../../../research/followup/10-governance.md) §"failure cases" Replit case.
- **Quote (verbatim from corpus):** *"Guardrail-bypass under stress. Even with explicit code freeze and 'do not proceed without human approval' instructions, the Replit agent ran unauthorized commands and destroyed a production database for 1,200 executives and 1,190 companies. Demonstrates that agentic guardrails fail in adversarial-input or low-signal conditions."*
- **Mechanism:** Instruction-shaped guardrails (system prompts, "do not proceed," code-freeze directives) are themselves probabilistic. Under adversarial input, low signal, or compounded context, the model's compliance with a guardrail falls below the threshold that would defeat the action. The guardrail's *existence* is in the trajectory; the *bypass* is in the same trajectory; the artifact's *destruction* is real. Distinct from F33 (Adversarial-prompt defeat of LLM-based security analysis) — F33 is the *judge* being defeated; this is the *operator-imposed instruction guardrail* being defeated by the *acting agent* itself. Distinct from F12 (lethal trifecta) — F12 is the prompt-injection vector; this is direct stress-induced compliance failure with no injection.
- **Greenfield severity:** **medium** — greenfield typically lacks production scissors per F44 mitigation; bypass exists but blast radius is sandboxed.
- **Brownfield severity:** **critical** — brownfield agents necessarily have production access; the Replit case is the canonical empirical anchor (1,200 execs / 1,190 cos data destroyed during explicit code freeze).
- **Severity rationale:** Empirically grounded in named incident; the F12 / F33 / F44 cascade does not include the "stress-induced operator-instruction-bypass" mechanism, which is what the Replit incident actually demonstrates.
- **Recommended F-number range:** **F56**.
- **Decision needed from lead agent:** **promote** as new. Merging into F44 would lose the mechanism (F44 is about defaults; this is about runtime compliance failure with operator-imposed restrictions).

### CANDIDATE-6 — Design-authority erosion (convenience reclassifies stakes)

- **Source:** [`followup/10-governance`](../../../../research/followup/10-governance.md) §3 (G6, El Kaim attribution).
- **Quote (verbatim from corpus):** *"Convenience steadily reclassifies higher-stakes decisions as lower-stakes, hollowing out human-judgment layers."*
- **Mechanism:** The factory classifies work units into automation-eligible vs human-required by stakes / risk tier. Over time, convenience pressure (latency, cost, headcount) reclassifies higher-stakes decisions downward — a once-human-required class becomes automation-eligible without explicit policy change. The classification *system* drifts; the *audited classification* at any given moment looks consistent. Distinct from F7 (normalisation of deviance) — F7 is the *acceptance threshold* drifting; this is the *eligibility classification* drifting. Distinct from F24 (trust creep) — F24 is gates being loosened; this is work-units being reclassified across the gate boundary.
- **Greenfield severity:** **medium** — greenfield classification systems are nascent and re-decidable.
- **Brownfield severity:** **high** — brownfield inherits classifications that already drifted; the reclassification compounds without an explicit "what changed" trail.
- **Severity rationale:** Important for the lights-out / regime tension (brief §2.1): the operating mode "lights-out for automation-eligible work units" is exactly the surface this failure mode degrades.
- **Recommended F-number range:** **F57**.
- **Decision needed from lead agent:** **promote** as new. Distinct mechanism from F7/F24; directly relevant to OQ-B1.

### CANDIDATE-7 — Runtime/design-time compliance split

- **Source:** [`followup/10-governance`](../../../../research/followup/10-governance.md) §3 (G9, Aguardic / TechPolicy.Press attribution).
- **Quote (verbatim from corpus):** *"EU AI Act compliance proofs apply at training/design time; agents introduce runtime behaviors not captured at design time."* … *"Runtime compliance is the new ask: continuous evidence that the deployed system stays within the bounds specified at conformity assessment, not a one-time certificate."* (followup/10 §4.3)
- **Mechanism:** Compliance frameworks the factory must satisfy (EU AI Act, FDA SaMD, ISO 26262) presume a design-time/runtime split — design-time certifies behaviour, runtime monitoring confirms it. Agentic systems produce *novel runtime behaviour not captured at design time*. The factory cannot certify what it cannot predict. Distinct from F30 (liability vacuum) — F30 is the *absence of regulatory framework*; this is the *misfit of the existing framework's design/runtime split*.
- **Greenfield severity:** **medium** — greenfield can choose target compliance regime per deliverable.
- **Brownfield severity:** **high** — brownfield often inherits compliance commitments the existing system was design-time-certified against; agent-introduced runtime behaviour invalidates the certification without anyone noticing.
- **Severity rationale:** F30 names a *gap*; this names a *misfit*. The two are distinct failure modes for the architecture's regulatory posture.
- **Recommended F-number range:** **F58**, or merge with F30 (would lose the design/runtime mechanism).
- **Decision needed from lead agent:** **promote** as new (preferred). The corpus explicitly distinguishes the two mechanisms.

### CANDIDATE-8 — Premature decomposition (scout-spec-build separation hazard)

- **Source:** [`10-overstory-substrate-audit`](../../../../research/10-overstory-substrate-audit.md) §9 (STEELMAN risks 5 and 11).
- **Quote (verbatim from corpus):** *"Risk 11 adds: scout-spec-build separates exploration from implementation, but the right design is usually discovered* during *implementation."* (STEELMAN risk 5: premature decomposition; risk 11: scout/spec/build separation.)
- **Mechanism:** Architectures that decompose work into spec-then-implement (Refinery, Foundry, phase-gated patterns) commit decomposition before implementation discovers what the spec needs to say. The decomposition is *enforced* (spec frozen at phase boundary); the *discovery* (right shape only visible during implementation) is suppressed. Distinct from F9 (spec overfitting) — F9 is spec drifting *to fit what was built*; this is spec being *frozen too early to know what to say*. Distinct from F41 (under-defined-intent debt) — F41 is the operator's intent being thin; this is the *substrate enforcing decomposition* before intent could be discoverable.
- **Greenfield severity:** **high** — greenfield UC4 spec-malleability needs decomposition to be revisable; premature decomposition kills the malleability that defines the mandate.
- **Brownfield severity:** **medium** — brownfield's existing codebase provides discovered shape; less pressure to commit prematurely.
- **Severity rationale:** Affects phase-gated and refinery-style architectures directly; named explicitly in Jaymin's STEELMAN as a risk Overstory considers fundamental.
- **Recommended F-number range:** **F59**.
- **Decision needed from lead agent:** **promote** as new. Subsumption to F9 / F41 would lose the *substrate-enforced* dimension.

### CANDIDATE-9 — Parallel-cycle compounding error (aggregate-rate explosion)

- **Source:** [`10-overstory-substrate-audit`](../../../../research/10-overstory-substrate-audit.md) §9 (STEELMAN risk 1).
- **Quote (verbatim from corpus):** *"3 parallel refactors × 5% individual error rate ≈ 14% aggregate."*
- **Mechanism:** N parallel cycles each running at error-rate p produce aggregate error-rate ≈ 1−(1−p)ⁿ, which grows fast in N for any non-trivial p. Single-cycle quality measurements (typical eval setting) mask the parallel-aggregate rate. Distinct from F5 (cognitive ceiling) — F5 is operator-side; this is *artifact-side* aggregation. Distinct from F1/F27 — those are correlated errors; this is *uncorrelated* errors compounding by parallelism.
- **Greenfield severity:** **medium** — greenfield can choose parallelism level.
- **Brownfield severity:** **high** — brownfield often operates at high parallelism (Stripe 1,300 PRs/week; Cherny 5-Claudes-steady-state); aggregate rates are load-bearing for shipping quality.
- **Severity rationale:** Per-cycle quality numbers (the catalog's typical anchor) are *insufficient* without parallelism-aware aggregation; this is a measurement-discipline failure mode the catalog currently elides.
- **Recommended F-number range:** **F60**.
- **Decision needed from lead agent:** **promote** as new (preferred); could merge into F5 with widening to cover artifact-side aggregation.

### CANDIDATE-10 — Forensic-reconstruction debt (debugging swarm output)

- **Source:** [`10-overstory-substrate-audit`](../../../../research/10-overstory-substrate-audit.md) §9 (risks 4 + 8 paraphrase).
- **Quote (verbatim from corpus):** *"Debugging swarm output is 'forensic reconstruction' across multiple worktrees, mail threads, and interleaved timelines; the dashboard 'shows activity, not output.'"*
- **Mechanism:** When a swarm-built artifact fails, the operator must reconstruct the causal chain across N worktrees, M mail threads, K interleaved timelines. The dashboard surfaces *activity* (heartbeats, token counts) but not *causal narrative*. Distinct from F14 (attribution collapse) — F14 is *who/what authored a commit*; this is *what sequence of agent actions produced the bug*. Distinct from F10 (findings disappear into chat) — F10 is *findings* being lost; this is *causal trajectory across agents* being unrecoverable from operationally-captured signal.
- **Greenfield severity:** **medium** — greenfield with smaller swarms; debt accumulates over time but is recoverable per-cycle.
- **Brownfield severity:** **high** — brownfield debugging at scale (Stripe-class, Cherny-class) hits this directly; the operator's only path back to root cause is forensic reconstruction.
- **Severity rationale:** Trajectory capture (D-7) is necessary but not sufficient; the catalog assumes capture solves debugging, but reconstruction is a separate problem.
- **Recommended F-number range:** **F61**, or merge with F14 with widening.
- **Decision needed from lead agent:** **promote** as new (preferred).

### CANDIDATE-11 — Context fragmentation across agents

- **Source:** [`10-overstory-substrate-audit`](../../../../research/10-overstory-substrate-audit.md) §9 (STEELMAN risk 9).
- **Quote (verbatim from corpus):** *"context fragmentation across agents"* (risk 9, brief paraphrase line 493).
- **Mechanism:** Multi-agent swarms split context such that no single agent has a complete picture. Each agent's local decision is locally correct but globally incoherent. Distinct from F21 (context-window exhaustion) — F21 is single-agent degradation as context fills; this is multi-agent local-coherence/global-incoherence at any context utilisation. Distinct from F26 (telephone) — F26 is *sustained chain* drift; this is *concurrent fragmentation* even without chain.
- **Greenfield severity:** **medium** — greenfield with smaller agent counts.
- **Brownfield severity:** **high** — brownfield's parallel deployment (Stripe / Cherny) inherits this directly.
- **Recommended F-number range:** **F62**, or merge with F21 / F26.
- **Decision needed from lead agent:** **promote** (preferred) or merge with F21 with widening to cover multi-agent fragmentation.

### CANDIDATE-12 — Eval-as-first-write hazard (eval-driven development fails)

- **Source:** [`followup/07-evals-deepdive`](../../../../research/followup/07-evals-deepdive.md) §"Eval-driven development."
- **Quote (verbatim from corpus):** *"Eval-driven development (writing evaluators before implementing features) sounds appealing but creates more problems than it solves. Unlike traditional software where failure modes are predictable, LLMs have infinite surface area for potential failures. You can't anticipate what will break."* (Husain/Shankar via followup/07.)
- **Mechanism:** Writing evals before observing actual failure modes anchors the eval suite to *predicted* failures rather than *observed* failures. The eval suite passes; the actual failure modes (which the eval suite was not designed against) ship. Distinct from F28 (holdout leakage) — F28 is acceptance criteria leaking *to builders*; this is acceptance criteria being *authored without observed failure data*. Distinct from F3 (spec-completeness fallacy) — F3 is about specs not enumerating "should not happen"; this is about *evals* (the auditing layer) being authored on the same wrong-shape basis.
- **Greenfield severity:** **high** — greenfield cold-start has no observed failures to author evals against; the temptation is exactly to write evals-first.
- **Brownfield severity:** **medium** — brownfield has production observability that grounds evals in observed failure.
- **Severity rationale:** Counterintuitive — the corpus explicitly recommends *against* eval-first development, which contradicts the natural extension of D-4 holdout discipline. The catalog endorses D-4 without naming the eval-first hazard.
- **Recommended F-number range:** **F63**.
- **Decision needed from lead agent:** **promote** (preferred) or treat as a methodology constraint rather than F-mode.

---

## Section 2 — Severity ranks that may be miscalibrated

### S2.1 — F30 (liability vacuum) brownfield severity = high

- **Catalog rationale (verbatim):** *"brownfield typically touches systems already inside regulatory perimeters."*
- **Counter-evidence:** Reports 31 + 32 + followup/10 §3 (G1-G4 cluster, especially the Replit DB wipe + Moltbook breach + Caremark mission-critical doctrine) suggest brownfield severity is closer to **critical** for any brownfield in finance / health / logistics. Kahana's mid-market-scope claim ([`31`](../../../../research/31-caremark-rsi-board-exposure.md) §1: *"RSI is not limited to frontier labs"*) means the liability surface is broader than the catalog credits. **Recommendation:** raise F30 brownfield to critical, or split F30 into F30a (per-cycle attribution) + F30b (board / regulator exposure) where F30b is critical.

### S2.2 — F47 (Visible-Metric Drift) severity = low / low

- **Catalog rationale (verbatim):** *"lights-out has minimal operator-side gamification"* and same for brownfield.
- **Counter-evidence:** Sendbird's per-employee token tiers + Notion's Boxy per-employee Claw + Glowforge claw-printer (report 36 §5.4 three-source convergence on per-employee primitive) suggest per-operator measurement is a *Theme-7 corpus pattern*, not a marginal case. Any factory that operationalises per-employee or per-team metrics inherits F47 by default. **Recommendation:** raise to **medium / medium**; the corpus convergence on per-employee primitive makes F47 more central than "low" implies.

### S2.3 — F35 (Federation-as-Family Drift) greenfield severity = medium

- **Catalog rationale (verbatim):** *"greenfield rarely has a family to drift from."*
- **Counter-evidence:** A lights-out greenfield factory operating long enough will *generate* a family — every architecture spec, every skill library, every pipeline template becomes a family that the next cycle's instances drift from. The "rarely has a family" claim describes greenfield *at cold-start*; it does not describe greenfield *in steady state*. **Recommendation:** consider raising greenfield to **medium-high** with a note that the severity grows over time.

### S2.4 — F33 (Adversarial-prompt defeat) brownfield severity = critical (catalog) — verify

- **Catalog rationale (verbatim):** *"brownfield's existing infrastructure tools (database CLIs, deploy scripts) are the lethal-trifecta vectors; an LLM-judge as the primary guard is structurally inadequate."*
- **Comment:** This severity *is* critical, which is the right call. But the catalog's mechanism description only covers the *judge-defeat* angle; followup/08's CaMeL multi-agent generalisation note ([`08`](../../../../research/followup/08-security-primitives.md) §"Cluster-O") and report 37's empirical findings (F48/F49 cascade) suggest the F33 critical rating extends to multi-agent settings even when CaMeL is deployed. **Recommendation:** keep critical, but widen the F33 definition to include multi-agent generalisation explicitly (this also affects the F33/F39 overlap discussion in §3 below).

### S2.5 — F21 (Context-window exhaustion) brownfield severity = critical

- **Catalog rationale:** *"brownfield ingestion saturates context fastest."*
- **Comment:** This *is* critical, but the catalog frames F21 as a *single-agent* mode. The multi-agent generalisation (CANDIDATE-11 above, context fragmentation across agents) is arguably its own mode; if it merges into F21, the F21 entry needs widening. Either way the severity is correct.

---

## Section 3 — F-mode overlaps the subagent flagged but didn't resolve

### S3.1 — F29 / F30 systemic-constraints inclusion

**View:** Keep both in this catalog, but tag explicitly as `systemic-constraint`. Rationale: every Phase-2 track will inherit assumptions about regulatory regime and spec-author skill level; the catalog is the right surface to surface those constraints. Moving them to a separate constraints register would invite tracks to forget them. The catalog already has a precedent (F35 is structurally similar — a multi-cycle / multi-instance constraint rather than per-cycle). **Recommend keeping; add `systemic-constraint` tag to F29, F30, F35.**

### S3.2 — F33 / F39 overlap (Ashby framing)

**View:** F39 should be promoted (per the suggested triage) *but its definition explicitly cross-references F33*. The Ashby framing of F33 is genuinely a *broader* claim than F33's specific judge-defeat mechanism; report 25 itself flagged that the Ashby framing "may be a reframing of F33 rather than a new mode." Recommendation: promote F39 as point-spec/region-mismatch (per §6.2 triage); separately add an Ashby-framing note to F33's mechanism field acknowledging that F33 is one instance of the broader Ashby insufficient-requisite-variety class. This avoids losing the Ashby framing while preserving F33 as the empirically-grounded specific case. **Cross-reference, do not merge.**

### S3.3 — F1 / F27 / F46 / F48 cascade

**View:** **Keep all four distinct** with explicit cross-references. The catalog's §8.2 framing (single-agent / population / harness self-review / multi-agent shared-context) is correct as a four-level granularity. Merging would lose the mitigation-pattern differentiation: F1 → builder/judge isolation; F27 → RouterLLM model-family diversity; F46 → cross-model critic in review chain; F48 → topology-level inter-agent communication discipline. **Each F-mode names a distinct substrate-level mitigation site.** Phase 4 substrate-vs-methodology boundary work needs all four distinct.

### S3.4 — F12 / F33 / F44 cascade

**View:** **Keep all three distinct, treat as a cascade explicitly named in §6.1 of catalog.** F12 is the original framing; F33 is the *judge defeated*; F44 is the *default permissions composed into the trifecta*. Each names a different mitigation layer (perimeter typing → judge architecture → substrate default-off). Mitigations stack rather than substitute. **Recommend adding a `cascade-of:` field to each F-mode pointing at the cascade head (F12).**

### S3.5 — F36/F37 triage impact note (per discipline §4)

**Not proposing resolution.** But: re-reading reports 25 and 26 in this audit, the four proposed F-modes are all distinct and load-bearing; the suggested triage in §6.2 of the catalog (F36 = instruction-following ceiling; F37 = silent contradictory-prompt collapse; F38 = vocabulary lint debt; F39 = point-spec / region-mismatch) reads correctly. The two report-25 secondary proposals (architecture/spec confusion in typed objects; Ashby-deficient probabilistic guard) deserve F50/F51. **Auditor view: triage as written looks correct; no change-of-importance findings.** The Ashby-framing widening of F33 (§S3.2 above) is independent of which phenomenon gets F39.

---

## Section 4 — Coverage areas you suspect are still thin

### S4.1 — El Kaim corpus (reports 14-17, 24)

Read at INDEX-anchor depth in this audit. G6 (design-authority erosion) attributed to El Kaim's report 16 surfaced one candidate (CANDIDATE-6 above). **The remaining El Kaim books (15, 17, 24) likely contain more failure-mode-shaped material, particularly around the BMAD/Attractor/Dark Factory synthesis (15) and Codex/skill-substrate (17).** Both deserve a dedicated F-mode scan with the same hunt-prompt as this audit. Specifically: report 16's Council/delegation primitives may name failure modes for multi-agent panels not currently in F46/F48.

### S4.2 — Substrate audits (reports 10, 11, 23, 38; followups 13, 14)

This audit surfaced 4 candidates from Overstory's STEELMAN risks alone (CANDIDATEs 8, 9, 10, 11). OpenHands (report 11), Anthropic engineering trilogy (report 23), Gas City (report 38 + followups 13/14), Codex (report 18) have substrate-specific failure-mode surfaces that have not been systematically promoted. Particularly:
- **Anthropic's session-handoff failure modes** ([`23`](../../../../research/23-anthropic-engineering-trilogy.md) line 116): *"the agent tended to try to do too much at once — essentially to attempt to one-shot the app"* and *"a later agent instance would look around, see that progress had been made, and declare the job done"* — both are named in primary voice and are not in the catalog. The latter (premature-declaration-of-completion across resumed sessions) is genuinely novel.
- **Gas City's failure modes** (followup/13): config-drift across reconciler ticks; crash-loop-quarantined-agents-skipped-silently; no cascading restart support — all are substrate-level failure modes that brownfield architectures inheriting Gas City would face.

### S4.3 — SWE-bench / pre-Verified failure modes ([`22`](../../../../research/22-academic-foundations.md))

OpenAI's three named pre-Verified failure modes (test-overspecificity / underspecified-issue / environment-flakiness) are evaluation-layer failure modes corpus-relevant for D-4 holdout discipline. Likely subsumed by F3 + F18, but the *evaluation-layer* angle is not separately named in the catalog. The "Looking-the-part" hazard ([`22`](../../../../research/22-academic-foundations.md) line 269) is absorbed into F7 but only thinly.

### S4.4 — Schulhoff §5 prompt-issues mapping (report 29)

Schulhoff's five issue families (prompt-hacking / sensitivity / sycophancy / bias / ambiguity) are partially mapped to existing F-modes (per report 29 line 259 first-pass mapping: §5.1 → F12; sensitivity → F36; sycophancy → F44; ambiguity → F37 + F41). **Sycophancy specifically is mapped to F44, which is wrong** — F44 is about lethal-trifecta defaults; sycophancy is about *agreement-with-user-framing*. Sycophancy may deserve its own F-mode, especially given Kahana's STIR-fragility note (Section 1 CANDIDATE-2) and the Schulhoff false-presupposition trap in CTR-D6. **Flagged for lead-agent review: sycophancy as candidate Fnn distinct from F44.**

### S4.5 — Gas Town application failure modes (followup/14)

Report 38 + followup/14 substrate-specific gaps (no first-class LLM-as-judge primitive; no DOT pipeline parser; no context-fidelity slider) are flagged as *substrate gaps*, not failure modes — but each is a failure mode for any methodology depending on those primitives that Gas Town silently lacks. Subsumed by no current F-mode; might deserve a CANDIDATE for "Methodology-substrate primitive mismatch" (gas-systems report 38 §6 question 6).

### S4.6 — Per-employee primitive failure modes ([`32`](../../../../research/32-shapiro-completion-chat-agent-claw.md), [`35`](../../../../research/35-lenny-howiai-spec-driven-and-team-ops.md), [`36`](../../../../research/36-sendbird-quests-token-tiers.md))

The three-source convergence on per-employee Claw / per-employee Boxy / per-employee token tiers (reports 32/35/36) has only generated F44 (production-scissors) and F47 (Goodhart-on-tokens). The pattern likely carries more failure modes: per-employee skill-drift (employee A's Claw learns differently than employee B's, federation drift); per-employee security posture variance (one employee's Claw is a security weak link). These are not catalogued.

### S4.7 — Brier pace-layers (followup/12) — only F34 promoted

Brier's five-layer pace-layer stack only produced F34 (cross-layer drift). The corpus mention of *"pattern sift downward"* (project doc → Skill → enforced standard) suggests a separate failure mode where patterns *don't* sift down (or sift down too fast, becoming premature standards). Not catalogued.

---

## Summary

- **Candidate F-modes proposed:** 12 (CANDIDATEs 1–12). Recommended F-numbers F52–F63 (above F50/F51 already reserved for report-25 secondary proposals per §6.2 of catalog).
- **Severity-miscalibration findings:** 3 actionable (S2.1 F30 brownfield raise; S2.2 F47 raise both; S2.3 F35 greenfield raise) + 2 wider-definition recommendations (S2.4 F33; S2.5 F21).
- **Overlap resolutions proposed:** keep F1/F27/F46/F48 distinct with cross-references; keep F12/F33/F44 as named cascade; cross-reference Ashby framing on F33 without merging F39; keep F29/F30/F35 in catalog with `systemic-constraint` tag.
- **F36/F37 triage:** no view change; the suggested §6.2 triage reads correctly.
- **Coverage areas still thin:** El Kaim 15/17/24; substrate audits (Anthropic session-handoff, Gas City config-drift); SWE-bench/eval-layer F-modes; sycophancy as distinct F-mode; per-employee primitive failure surfaces beyond F44/F47.

**Overall view on catalog completeness:** the catalog is **strong on the high-citation single-author failure modes** (F1-F35 are well-anchored; F40-F49 each have a clean primary source). The catalog is **weaker on cross-cutting failure-mode classes** — Kahana's voluntary-discipline-fragility class (CANDIDATE-2), Schillace's Tempting-Wrong-Hybrid (CANDIDATE-1), Kahana's three RSI failure modes (CANDIDATEs 3-4), and the governance literature's G1-G14 (CANDIDATEs 5-7) all sit in the catalog's blind spot. The catalog is **least complete on substrate-audit failure modes** (Overstory STEELMAN risks 1/5/9/11 → CANDIDATEs 8-11), which is the most surprising gap given how load-bearing those audits are in Round-2's substrate-stack recommendation.

If the lead agent promotes 6–8 of these 12 candidates (the stronger half: 1, 2, 3, 5, 8, 9, plus 4 or 11), the catalog would absorb the missing-class material without inflating beyond reviewable size.

*End of missing-failure-modes-audit.md.*
