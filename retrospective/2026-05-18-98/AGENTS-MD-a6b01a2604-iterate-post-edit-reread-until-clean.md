# agent instruction

**Iterate post-edit-reread-pass until clean.** When the user asks to "iterate", "double-check", or "review yourself" on a multi-section doc edit, do not stop after iteration 1 just because iteration 1 found things — fixes from iteration N introduce drift that iteration N+1 catches. Stop only when the most recent full pass surfaces zero major or factually-wrong-minor findings.

*Grounded in: PR #98 audit iterations 1–6, where iteration 3 found Round-10's openai.com/index/* URL closures that iterations 1–2 had missed, and iteration 3's own fixes introduced "~4 URLs" residues that iteration 4 cleaned up.*

# justification

The session ran 6 iterations on PLAN.md. Iteration 1 caught the big drift (count drift in §1 + §2 layout staleness + §17 missing version-history rows). Iteration 2 was small (§1 open-items pointer; §6.2 row). Iteration 3 caught a cross-section contradiction Round-10 had introduced two weeks earlier (`openai.com/index/*` URLs closed but still listed outstanding in five places). Iteration 4 caught five "~7 URLs" residues from iteration 3's own incomplete sweep. Iteration 5 added one tiny fix (#82 missing from a list). Iteration 6 was the clean confirmation pass. If we'd stopped at iteration 3 — the natural "ok this looks done" stopping point — §4.1, §4.3, §5 task 7, §9, and §14 would still carry stale "~7 URLs" claims contradicting the §1 update. Cost of adopting the rule: 5 minutes per additional pass on a 500-line doc. Cost of not adopting: the drift that survives ships, and the iteration-N+1 work that *would* have caught it never happens.
