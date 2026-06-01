# Spec: `paradigm-shift-reconciliation`

- **ID**: SKILL-SPEC-c207874125
- **Source retrospective**: ../2026-06-01-227.md

## Intent

Finish a half-applied paradigm shift in a long-lived document: locate the commit where the organizing principle changed via git archaeology, name the old and new organizing principles explicitly, then re-derive the whole document around the new principle while preserving the old structure's factual content and stripping all narration about how the document changed. It earns its place because this session was handed a doc whose organize-by-product edits sat on top of a still-intact organize-by-phase skeleton, and the fix required first pinpointing the shift via git log and git show on the two prior commits.

## Trigger

- Direct: "this doc mixes two styles", "the last edits started reorganizing by X but the old Y structure is still there", "make X first-class, not Y", "finish the restructure", "reconcile the two organizing principles".
- Proactive: when editing a document and you notice two competing organizing structures coexisting (e.g. a new top section in one paradigm and a large unchanged body in the old one), or pervasive change-narration referencing an "old version."
- Negative: a greenfield document (no prior paradigm to reconcile), or a doc where both structures are intentionally present and serve different audiences.

## Inputs

- The target document path.
- The desired organizing principle (from the user) — what should be first-class.
- Read access to git history for the file.
- The source-of-truth the document's factual content derives from (so the re-derivation preserves facts while changing structure).

## Outputs

- The document re-derived around the new organizing principle, with the old skeleton dissolved and its factual content re-homed (no information loss).
- Zero change-narration / conversation-anchoring in the result.
- Optionally, an ADR recording the chosen organizing principle as a convention for sibling docs.

## Workflow

1. **Locate the shift.** Run `git log --oneline -- <file>` and `git show <commit>` on the most recent commits. Identify the commit(s) where the new paradigm entered and read the diff to see exactly what was added on top of what.
2. **Name both principles explicitly** in your own working notes: the old organizing axis (e.g. "dependency phase/wave") and the new one (e.g. "the adopted product"). State which is the keeper.
3. **Confirm scope with the user** if the disposition of the old structure is a real fork (delete entirely vs fold its content into the new structure vs keep as an appendix). This is the one decision worth a question — it changes a lot of downstream work.
4. **Ground the new structure against the source of truth.** Dispatch cooperative research subagents to verify the new organizing units and re-extract any factual content (mappings, dependency edges) the re-derivation needs, writing findings to disk. Do not trust the half-applied edits' facts uncritically — they often carry errors.
5. **Re-derive the document** around the new principle: every section is now a unit of the new axis; the old axis's factual content (dependencies, counts, ordering) is preserved but re-expressed within/across the new units.
6. **Strip all change-narration** — every "this replaces", "unchanged below", "now leads with", "corrected", "you asked". State what the document is.
7. **Validate** (diagrams, link/ref checkers) and run the result through adversarial review (see `iterative-multi-persona-review-loop`), because half-applied paradigm shifts hide subtle cross-section contradictions.

## Concrete examples

### Example 1: phases → products (this session)

`architectures/v4/implementation-dependencies.md` had been edited to add a product-clustering view (Gas City delivers ~11 components) but kept its original 10-phase wave structure intact below — scattering one product's components across Phases 1/2/3. `git log --oneline -- <file>` showed three commits: the original (phase-organized) and two that bolted products on top. `git show` on the two later commits pinpointed exactly the added sections. The reconciliation: make the product the first-class unit (external adoptions + internal custom build-test-integrate units, some single-component), dissolve the 10 phases, and re-express all dependency/parallelism/critical-path content in a "Build order across products" section — preserving every inventory edge. Then strip "this replaces the old long pole", "the original view, unchanged below", "you asked a sharp question", etc.

### Example 2: chronological → thematic changelog

A `CHANGELOG`-style design doc that began as date-ordered entries but later grew theme-based sections ("Auth", "Storage") on top, leaving entries duplicated in both. `git log` locates where the thematic sections appeared; name the axes (date vs theme); confirm theme is the keeper; fold each dated entry under its theme; remove "(moved from the dated section above)" narration.

## Anti-patterns

- **Editing from a guess about where the inconsistency lives** instead of reading the diff first — you find the deeper structural layer only after reworking the shallow one.
- **Trusting the half-applied edits' facts.** The new sections often carry errors (this session: a mis-licensed dependency, a double-counted component, a dropped tool still implied present). Re-ground against the source of truth.
- **Leaving change-narration in** because it "explains the transition" — it bewilders the first-time reader who has no prior version in mind.
- **Deleting the old structure's information along with its skeleton.** Dissolve the organizing axis, not the facts it carried.
- **Skipping the scope question** when "delete vs fold vs appendix" genuinely changes the deliverable.

## Acceptance criteria

- [ ] The shift commit(s) are identified from git history and the old vs new organizing principle is named explicitly.
- [ ] The result is organized entirely around the new principle; no residue of the old skeleton remains as a competing structure.
- [ ] All factual content from the old structure is preserved (verified against the source of truth), with zero information loss.
- [ ] Zero change-narration or conversation-anchoring remains (grep for the telltale phrases).
- [ ] The result passes diagram/link validation and an adversarial review round with no factual/contradiction findings.

## Files this skill creates / modifies

- The target document — re-derived around the new organizing principle.
- `<scratch>/_meta/*VERIFY*.md`, `*EXTRACT*.md` — cooperative-subagent grounding findings (mapping verification, dependency-graph extraction).
- (Optionally) an ADR draft recording the organizing-principle convention.
