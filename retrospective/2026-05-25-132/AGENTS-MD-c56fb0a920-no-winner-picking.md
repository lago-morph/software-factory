# agent instruction

**Don't bake winner-picking framing into multi-candidate exploration.** When the user is in research/exploration mode (synthesis methodology, multi-option decision points), default to "carry all defensible candidates" framing rather than "pick one option." Verify the user wants elimination before structuring decisions as option-picks. If unsure, ask the user once before authoring decision briefs.

*Grounded in: Phase-3.4 integration brief was over-eliminative; user reframed twice before the framing matched their actual goal.*

# justification

The Phase-3.4 integration brief structured each Tier-1 decision as "pick one of options A/B/C/D" — a winner-picking framing. The user reframed twice in the same session: first to "carry all defensible candidates" as the scoping principle, then to a deeper reframe of DEC-1 itself ("the original DEC-1 question is wrong; ask a different question"). Both reframes wasted ~2000 words of brief authoring that had to be retroactively annotated with SUPERSEDED banners and re-written into handoff docs. Marginal cost of asking up front: one clarifying question at the start of brief authoring. Asymmetry: avoiding the trap costs 1 question; falling into it costs ~30-60 minutes of rewrite plus the cognitive load of explaining the reframe to a context-tired user.
