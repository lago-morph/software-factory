# agent instruction

**Glob real filenames before dispatching file-targeted subagents.** Before briefing a subagent to edit files by path, resolve the actual on-disk names with a glob or `ls`; never hand a subagent assumed paths like `spec/C43.md` when the real file is `spec/C43-isolation-boundary.md`.

*Grounded in: the first spec-annotation subagent in this session, which was briefed with `C<NN>.md` paths, found nothing to edit, and forced a second dispatch once the real `C<NN>-<slug>.md` filenames were discovered.*

# justification

The v4 spec corpus names files `C43-isolation-boundary.md`, not `C43.md`. The first integrator subagent was briefed with the short form, silently found no matching files for its edits, and returned having changed nothing — so a second subagent had to be dispatched with globbed paths, doubling the cost of that wave and creating a window where two agents could (and did) race on the same files. A subagent cannot recover from a wrong path the way the lead agent can, because it does not know the corpus's naming convention unless told. The marginal cost of the rule is one `ls spec/C43-*.md` per target before writing the brief; the cost of skipping it was a wasted ~9-minute subagent run plus the reconciliation work to clean up the resulting duplicate edits.
