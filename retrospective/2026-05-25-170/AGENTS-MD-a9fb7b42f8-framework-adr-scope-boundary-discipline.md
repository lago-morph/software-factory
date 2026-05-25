# agent instruction

**Framework-ADR scope-boundary discipline.** Common ADRs for substrate primitives that have deferred per-variant ADRs MUST carry an explicit scope-boundary statement in their `## Consequences` section naming (a) the variant landscape, (b) the deferral target (next run / wave / phase), (c) the cross-reference requirement for downstream consumers (e.g., "Phase-N specs MUST reference BOTH this framework ADR AND the candidate's per-variant ADR").

*Grounded in: ADR 0036 (P-30 event registrar substrate) carried the verbatim DISTINCT-primitives scope warning because Round-2 adversarial review caught the risk.*

# justification

In the 2026-05-25 Wave 5.1b dispatch, four framework ADRs (P-19, P-28, P-29, P-30) had per-variant ADRs deferred to Wave 5.3 next run. The pre-mortemer Round-2 reviewer surfaced a specific failure mode: a Phase-6 architecture-spec author would cite "the P-30 ADR" for state-machine semantics not realizing the common ADR covers Temporal substrate only — the U-A re-entry-interval state machine and the D7-U-1 survival-window state machine are separate per-variant ADRs in Wave 5.3. The auto-005 Round-2 amendment mandated each Wave-5.1b subagent's brief carry an explicit scope-boundary requirement; all four ADRs complied.

Without the rule, similar silent under-reference happens every time a framework ADR ships ahead of its variants. The marginal cost: 3-5 extra sentences in `## Consequences` (one paragraph). The asymmetric cost without: Phase-N consumers (here Phase 6 architecture specs) cite the framework ADR and miss the variant — the framework alone does not carry the variant semantics, but the cross-reference omission is invisible until the spec is reviewed. Catching it at Phase-N review is high-cost (re-author the spec section); catching it at framework-ADR authoring time via this rule is near-zero-cost.
