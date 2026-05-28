# agent instruction

**Per-candidate engagement over blanket-skip for prior-phase defaults.** When a dispatch brief proposes to "skip" or "auto-classify-as-absorbed" a set of prior-phase defaults (e.g., D-1..D-7 inherited consensus items) for parallel per-candidate subagents, the brief MUST instead instruct each subagent to verify per-candidate via `grep` against its candidate's spec content + a one-token-verdict-per-default rubric (`absorbed-verified-at-§X` / `absorbed-silently-flagged` / `challenged` / `not-applicable-to-candidate-mandate`). Word cost: ~40 words per default × N defaults per candidate. Required even when the defaults are documented as "already inherited" upstream.

*Grounded in: Phase-7 auto-007 Round 2 — Reviewer 5 / scoping-skeptic Defect 1 + Reviewer 6 / historian D-H5 amendments folded; BF-L spec explicitly challenges D-1, D-2 (and partially D-3) which Round-1 blanket-skip would have hidden.*

# justification

The auto-007 Round-1 brief instructed all 10 per-candidate back-fill subagents to skip D-1..D-7 defaults as "already-inherited material" — mark them `absorbed (v3 default D-N) without further analysis`. Two independent Round-2 reviewers caught this:

Reviewer 5 (scoping-principle-skeptic) cited [`archive/synthesis-v1-v2/ARCHIVE.md` line 18](archive/synthesis-v1-v2/ARCHIVE.md) verbatim: *"Defaults are not invariants — every Phase-2 track must mark each as `accepted with justification` or `challenged`."* Blanket-skip violates per-candidate engagement.

Reviewer 6 (historian/prior-art) empirically confirmed by `grep`-ing the BF-L spec: BF-L's §4 discipline binding **explicitly challenges D-1** (substrate-displaces-spec; Codebase Model is the durable artifact) AND **D-2** (scenarios-from-model; not out-of-tree) AND **partially D-3**. D7-U-1 generalizes D-4 to every artifact boundary. Round-1 blanket-skip would have silently mis-classified these as `absorbed (v3 default D-N)` when the specs actively reject them.

The Round-2 fix (new §1.5 verification subsection in every back-fill notes file; ~280 words per candidate; mechanical `grep`-based) surfaced 5 candidate-default explicit-challenges at fanout-close that would otherwise have been invisible.

Cost of not having the rule: future fanouts blanket-skip ostensibly-inherited defaults, hiding per-candidate departures that are exactly the kind of finding the audit exists to surface. Cost of adopting the rule: ~280 words per candidate notes file. The asymmetry: a hidden challenge is invisible at audit-close; a slightly longer notes file is mechanically obvious.
