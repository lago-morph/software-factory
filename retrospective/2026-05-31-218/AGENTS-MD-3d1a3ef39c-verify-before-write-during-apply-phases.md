# agent instruction

**Verify-before-write during apply phases.** "When applying a planned edit set to artifacts (post-decision, post-design, post-survey), read each target artifact in full before writing. If the intended minimal form is already present, mark it no-op and move on. If the edit would overturn a deliberate decision in the artifact (esp. one flagged by the original author as load-bearing), flag it for the operator rather than silently overwriting. Report no-ops explicitly — they are the proof the canonical was already correct, not wasted work."

*Grounded in: PR #218 survivor-pass apply phase, where reading the canonical specs first revealed 21 of 25 intended edits were already present, and 4 would have reversed faithful's deliberate spec/template collapse.*

# justification

This session's survivor-pass produced a ledger of 25 KEEP-MINIMAL deltas to fold into the canonical track. The apply phase was the moment of truth. Two outcomes the discipline of reading-each-target-first surfaced that pattern-matching would have missed:

First, 21 of the 25 keeps were already present in the canonical track in minimal form. The original author had been working to a "minimal fills" charter that produced the same minimal capabilities the survivor-pass had identified as worth adding. Without reading, I would have either duplicated existing content (noise) or — worse — overwritten the minimal form with the divergent track's full hardening, which is exactly what the operator's capability-for-principle bar said to drop. The "no-op" finding is not absent work; it is the verification that the canonical was complete, which is the load-bearing claim of the convergence.

Second, 4 of the 25 (the C08/C09 cluster) reclassified when read in their full text. The C08 spec had explicitly flagged an `[AMBIGUITY: OQ-1]` — "should the spec be the prompt-template file (Reading A, collapse) or a standalone bundle the template references (Reading B, split)?" — and resolved it to Reading A, flagged as the load-bearing integrator decision. Pulling in the divergent track's standalone-bundle deltas would have silently reversed that decision. The read caught it; pattern-matching from the survivor-pass scoring did not (I told the operator earlier in the session "no decisions change under the refined bar" — that statement was wrong, and I had to publicly walk it back during the apply).

The cost of reading-first is one file read per intended edit — a few seconds each in subagent time, none in operator time. The cost of skipping the read is unrecoverable: silent overturning of a flagged decision rots downstream; duplicating content makes the canonical noisier; and the operator's trust in the planning step is eroded each time pattern-matching from a survey fails to survive contact with the artifact.

The discipline is: list intended edits → open each target file in full → verdict per intended edit (already-in / apply / reclassify-drop / reclassify-defer) → apply only the genuine gaps → report no-ops in the summary.
