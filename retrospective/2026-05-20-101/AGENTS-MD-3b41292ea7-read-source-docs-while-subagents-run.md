# agent instruction

**Read load-bearing source docs while subagents run.** When dispatching deep-analysis subagents against a large repo or corpus, use the foreground wait to read 3–5 load-bearing docs from the target (typically the overview / architecture / coming-from-X files) so subagent output can be spot-checked before it commits to the corpus. The marginal cost is ~10 minutes of foreground reads; the benefit is catching paraphrased or confabulated claims before they propagate into a permanent reference.

*Grounded in: PR #101 — parallel ground-truth reads of nine-concepts.md and gastown/docs/design/architecture.md while subagents ran.*

# justification

PR #101's two subagents ran for ~12 minutes each in the background. During the wait, the foreground session read `gascity/docs/getting-started/coming-from-gastown.md`, `gascity/engdocs/architecture/nine-concepts.md`, and `gastown/docs/design/architecture.md` end-to-end. This produced a high-confidence ground-truth grasp of the "Nine Concepts" primitive set, the substrate-vs-application split, and the two-level Beads/Dolt routing — which is exactly what the subagent outputs were going to claim. When both analyses returned, the load-bearing claims (Nine Concepts mapping, ZFC + Bitter Lesson invariants, gastown role taxonomy as a pack) were verifiable against an already-loaded mental model, not against scrollback or re-reads.

The previous corpus has at least one known instance of subagent claim drift — `research/followup/04-gastown-beads.md` characterised `gt-proxy-server` as "for routing LLM API calls (model routing / quota management)" based on a partial read; the new followup/14 walk against the actual `internal/proxy/` code reveals it is **containerized polecat isolation via mTLS**, not LLM routing. That refutation is now in followup/14 and the synthesis report. The foreground reads on this session caught nothing that bad (subagent output was clean), but the discipline scales the audit trail — every load-bearing claim in the deep-dives could be cross-checked in real time, not in a separate post-commit pass.

Cost: ~10 minutes of foreground reads during a wait that would otherwise be idle. Benefit: subagent output ships with verified load-bearing claims, not "probably correct, will audit later" claims. The corpus has accumulated enough "verbatim quotes that turned out to be confabulated" entries (every revision-notes section of report 01, 02, 07 catalogues several) that the marginal cost of foreground verification pays for itself within one session.
