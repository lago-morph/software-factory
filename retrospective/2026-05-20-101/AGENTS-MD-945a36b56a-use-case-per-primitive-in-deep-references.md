# agent instruction

**Include at least one use-case scenario per major-primitive section in deep architecture references.** When writing a deep architecture reference intended for a future AI session (e.g., `research/followup/`), each major-primitive section should include at least one motivating use-case scenario — not just the syntactic mechanics of the primitive. A reader of the document in isolation must be able to answer "what would I actually compose / configure this for?" without chasing cross-links to a separate synthesis report.

*Grounded in: PR #101 follow-up Q1 — gas city deep-dive covered pack-composition mechanics in §4 + §14 but use-case scenarios lived only in the synthesis report §4 + §5.*

# justification

After PR #101 merged, the user asked: *"Did the detailed analysis of gas city talk about the fact that it is broken down into packs that are composable and give some examples of how that could be used?"* The honest answer was: yes, the deep-dive covered the mechanics of pack composability comprehensively (§4 has the `pack.toml` `[imports.gastown]` + `[imports.review]` example, the six-step composition pipeline, the override-cascade table; §14 enumerates the 5 bundled packs and the `gc import add/install/upgrade/why` model). But the *worked use-case scenarios* — "compose a darkfactory pack alongside gastown for scenario-driven build," "compose a compound pack on top of gastown with 14 reviewer agents" — lived only in the synthesis report.

That asymmetry is structurally inappropriate for a deep-dive whose audience is "a future AI session that needs to understand this tool well enough to use it, extend it, or treat it as a runtime substrate." A reader who loads only the deep-dive (the natural reading mode for a deep reference) sees the syntax of `[imports.X]` but cannot answer "what would I actually compose this for?" without loading a separate file. The fix is one to two paragraphs per major primitive section — e.g., §14 Pack Ecosystem should include a "compose a security-review pack into an existing town" or "swap the gastown.polecat provider per-rig" scenario alongside the bundled-packs table.

Marginal cost: ~5 minutes per primitive section. Cost of skipping: every reader of the deep-dive in isolation has to either chase the synthesis-report cross-link (slow) or reason from syntax to use-case themselves (error-prone). The pattern generalises to any architecture reference written for asynchronous-reader audiences (which is most of `research/followup/`).
