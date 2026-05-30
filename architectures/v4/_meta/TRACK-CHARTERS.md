# Track Charters

Binding rules for every builder/adversary/reconciler subagent. A persona brief always names which
track it serves; these are the rules it must obey.

## Track A — Faithful ("fixed proof")

**Premise:** The four v4 docs are a *fixed proof*. Your job is to render what they say into a complete,
precise spec/plan — not to improve it.

Rules:
1. **No architectural changes.** You may not add, remove, rename, or re-scope components beyond what v4
   states or unambiguously implies.
2. Where v4 is silent, you **specify the minimal faithful elaboration** needed to be implementable, and
   you **flag it** with `> [FAITHFUL-FILL]` noting the inference and why it is the smallest consistent choice.
3. Where v4 is contradictory or ambiguous, you **do not pick a winner silently** — you record both
   readings under `> [AMBIGUITY: Gxx]` and pick the one most consistent with the rest of v4, stating why.
4. Adversarial review in Track A may attack *fidelity and completeness*, not the design itself.
5. Every claim traces to a v4 source (doc + section).

## Track B — Optimized ("ruthless improvement")

**Premise:** v4 is the starting point and fair game. Produce the best architecture you can defend.

Rules:
1. **Improve freely**, guided by sound engineering judgment, the Skeptic's gap findings, and the
   failure-mode coverage goals.
2. **Every deviation from v4 is an explicit delta.** Mark with `> [DELTA-NN]` and record: what v4 said,
   what you changed it to, the rationale, and the tradeoff accepted. Maintain a running delta index in
   each doc's header.
3. Deltas must be **justified against concrete forces** (scale, failure, cost, security, operability,
   simplicity, parallelizability) — not taste.
4. Preserve diffability with Track A: keep the **same component IDs** from the canonical inventory even
   when you re-scope, so the two tracks can be compared component-by-component. If you split/merge a
   component, note the ID mapping.
5. Adversarial review in Track B attacks the *design* hard: "what breaks, what's cheaper, what's simpler."

## Shared rules (both tracks)
- Obey the context-preservation protocol in `META-PLAN.md` §2.
- One subagent = one file (distinct path). Never touch another agent's file.
- Never run git. The primary commits between waves.
- Cite sources. Prefer precision over prose. Tables and diagrams over paragraphs where they carry more.
