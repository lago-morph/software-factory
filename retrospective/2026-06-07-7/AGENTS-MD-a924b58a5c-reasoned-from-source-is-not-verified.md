# agent instruction

**Reasoned-from-source is not verified.** A change derived from reading source code is a hypothesis, not a verified fix; label it as unverified and run it against the real system before shipping it or claiming it works.

*Grounded in: `GC_BEADS_FORCE_FALLBACK` shipped from code-reading and introduced the gc-status 3s-timeout regression.*

# justification

In PR #2 the `GC_BEADS_FORCE_FALLBACK=1` setting was shipped on the strength of reading gc's source: the code-reading concluded that forcing the fallback store would sidestep a native-store retry. It was plausible and wrong — forcing every snapshot read through a `bd` subprocess blew gc's 3s budget on the WSL2 VM, producing a "loading session snapshot timed out after 3s" regression that PR #3 had to undo. Reading source tells you what the code intends to do, not what it does under the target's real timing, filesystem, and process costs. The cost of treating reasoned-from-source as verified is shipping regressions that look like fixes and then spending a whole follow-up PR diagnosing and reversing them. The marginal cost of the rule is a single live run of the change before claiming it works — and explicitly labeling any unrun change as a hypothesis so a reviewer knows what they're trusting.
