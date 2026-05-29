# agent instruction

**Pivot on substantive pushback.** "When the user pushes back substantively on a recommendation, treat the pushback as a signal that the framing itself may be wrong, not just a request for clarification. Re-examine the load-bearing assumption before defending or restating the original recommendation. If the assumption was wrong, acknowledge it explicitly ('Yes, you're right') before pivoting."

*Grounded in: the v4 pack-vs-fork correction (PR #211) and the BLAKE3-CAS scope-creep correction in the same session.*

# justification

The cost of NOT pivoting on substantive pushback compounds — the user gets frustrated, the wrong recommendation propagates to downstream artifacts (the fork recommendation propagated to both v4 README and AI-CONTEXT before correction), and the eventual correction costs more than catching it the first time. In the pack-vs-fork case, the user had to type "Why did you suggest forking gascity? I thought its whole thing was you could extend with packs" — clean substantive pushback that landed because I'd conflated two distinct earlier-discussed goals. The marginal cost of pivoting is roughly two minutes of "let me re-examine the assumption" thinking. Asymmetry is large.
