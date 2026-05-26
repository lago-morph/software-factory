# agent instruction

**ADR-number-to-filename mapping in subagent dispatch briefs.** When dispatching a parallel ADR-authoring fanout, the lead agent MUST publish the full ADR-number-to-filename mapping for ALL ADRs in the wave (including those authored by sibling subagents) in each subagent's brief, so cross-references between same-wave ADRs resolve correctly the first time without forward-ref-by-wrong-number bugs.

*Grounded in: Wave 5.1b ADR 0034 (P-27) authored a forward-reference to a future P-26 ADR at the wrong number (assumed 0033, which was actually P-25); caught at lead-agent aggregation and fixed inline.*

# justification

In the 2026-05-25 Wave 5.1b dispatch, the P-27 archaeological-brief subagent assumed P-26 (Codebase Model) would be assigned ADR-0033 — a reasonable speculation since 0033 was the next number after P-27's likely 0032. But the lead agent had assigned 0033 to P-25 CaMeL perimeter; P-26 was in fact deferred to Wave 5.3. The cross-reference `[./0033-p-26-codebase-model.md]` broke and was caught only when `check-internal-refs.py` ran at aggregation. The fix was trivial (rewrite the link to point at Wave 5.3 deferral) but the bug class is dangerous: if a subagent's speculative reference happens to match an unrelated ADR's filename slug, the link-checker accepts it, producing a silent cross-reference to the wrong target.

The marginal cost of the rule: one paragraph in each subagent's brief carrying the wave's full ADR-number → filename table (~10 lines, mechanically templatable from the wave manifest). The asymmetric cost without: one cross-reference bug per fanout-with-cross-refs, only sometimes catchable by the link checker, sometimes producing silent-misroute (the worst kind of cross-reference drift). The rule scales — a wave dispatching 10+ subagents in parallel saves 10 potential cross-reference debugging sessions over its lifetime.
