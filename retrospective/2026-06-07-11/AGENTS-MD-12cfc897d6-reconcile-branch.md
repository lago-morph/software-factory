# agent instruction

**Reconcile the working branch from git, not just the handoff doc.** When a handoff or pickup doc names a branch and the harness names a different one, do not trust either on faith: run `git branch --show-current`, `git branch -a`, and compare the candidate branch to `origin/main` before the first commit. The checked-out branch and the origin state are authoritative; a handoff doc's branch name is often stale from the session that wrote it.

*Grounded in: the HANDOFF named `claude/software-factory-v4-setup-vTSqG` while the actual branch was `claude/stoic-ptolemy-Hvsiv`, which already equalled `origin/main`.*

# justification

A pickup brief and the harness disagreed on the branch name in the first minute of this session. The handoff said `claude/software-factory-v4-setup-vTSqG`; the real checked-out branch was `claude/stoic-ptolemy-Hvsiv`, already equal to `origin/main`. Had the agent trusted the handoff, the first `git push -u origin claude/software-factory-v4-setup-vTSqG` would have created a stray branch divorced from the real work, and every PR would have targeted the wrong head. The check is three read-only git commands costing seconds; the failure it prevents is a confusing tangle of branches that the operator has to clean up. The asymmetry is overwhelming, and handoff docs go stale on exactly this field because the branch is often regenerated per session.
