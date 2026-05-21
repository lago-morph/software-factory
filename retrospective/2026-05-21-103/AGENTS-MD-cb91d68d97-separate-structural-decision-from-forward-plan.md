# agent instruction

**Separate structural decision from forward-plan recommendations when extracting an ADR.** When a recommendation or proposal document mixes a structural decision (a layered convention, a contract, a fixed flow) with forward-plan recommendations (collapse to v3, build X next), the extracted ADR codifies the structural decision under `## Decision` but defers the forward plan under "what this is explicitly not promising" in `## Consequences`. Do not let a structural ADR quietly commit to in-flight sequencing.

*Grounded in: ADR-0002 extracted from `research-plan.md` — three-layer pipeline (structural, codified) vs. "cut a unified v3 synthesis" (forward plan, deferred).*

# justification

`research-plan.md` opens with "This is a recommendation, not a settled plan." It then mixes two distinct kinds of content: a description of an existing structural funnel (reports → synthesis → architectures → ADRs), and a forward plan for what to do once "enough research" is reached (cut a unified v3 synthesis, collapse to one architecture, run a §6 lean evaluation). Both are real, both matter, but they have different decision status. The structural funnel already exists in the repo and works — the directory layout, the file conventions, the one-way citation flow. The forward plan is a recommendation about sequencing that the user has not signed off on.

If the extracted ADR conflates the two, it accidentally promotes the forward plan from "recommendation" to "Accepted decision". That is the kind of silent over-commit that gets discovered six months later when someone asks "wait, when did we decide to collapse to one architecture?" — and the answer is "we didn't; an agent extracted both halves of research-plan.md into a single ADR." The cost is reputational (the ADR log loses credibility as a record of real decisions) and operational (a future agent treats the forward plan as a settled constraint).

The marginal cost of adopting this rule is a sentence or two in the ADR's Consequences section explicitly disclaiming the forward plan. That is cheap. The benefit is a clean separation between "we have committed to this" and "we are recommending this next" — which is the entire point of having an ADR log distinct from a plan document.
