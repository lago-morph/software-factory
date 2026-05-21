# ADR: Failure-mode coverage matrix lives in `architectures/failure-modes.md` and is owned by a self-installing skill

- **ID**: ADR-b201e941ba
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-05-21
- **Source retrospective**: ../2026-05-21-113.md
- **PRs covered**: #113

## Context

The architecture comparison document `architectures/00-comparison.md` carried §2.4 "Failure mode coverage" — a per-architecture matrix mapping F1–F20 to each of the four candidate architectures' coverage strategies. The §2.4 content was out of date (multiple synthesis rounds had introduced F21–F49 elsewhere without updating it). Two structural problems compounded: the matrix was buried inside an unrelated comparison narrative, and there was no enforcement that future edits to the architecture alternatives propagated into the matrix. Issue #111 asked to extract the matrix, designate it canonical, and add discipline so the matrix and the architecture alternatives stay coupled.

A second pressure shaped the location decision: failure modes are referenced from `research/synthesis/00-synthesis.md` (F1–F20 definitions), `research/synthesis/13-round-2-synthesis.md` (F21–F33), and at least twelve other research reports proposing F34–F49. The matrix-as-section-in-comparison-doc could not become "the canonical index" because the comparison doc has its own narrative purpose. The matrix needed a home that signaled "canonical project artifact across architecture, research, and retrospectives."

## Decision

Extract the failure-mode coverage matrix out of `architectures/00-comparison.md` into the canonical project file `architectures/failure-modes.md`, and assign exclusive ownership of its schema, edits, and CI gate to a single self-installing skill at `.claude/skills/architecture-failure-mode-gate/`.

The skill owns the schema (one column per `architectures/0N-*.md` alternative, header form `N: ShortName`, body rows `F<K>` with one cell per column), the linter, the workflow template, the install procedure, and the "Handling the gate review" override procedure. Any agent editing the matrix or any architecture alternative loads this skill first; the skill's no-prompt pre-flight ensures the CI workflow is installed and in sync before work proceeds.

## Alternatives considered

- **Keep the matrix in `00-comparison.md` §2.4 and document the discipline elsewhere.** Rejected: the matrix's location in a narrative document made it discoverable only via the comparison doc's table of contents, not via "the canonical project file on failure modes." Every research report citing F1–F20 had to point at `00-comparison.md` for coverage and `research/synthesis/00-synthesis.md` for definitions — a confusing split.
- **Put the matrix at repo root (`/failure-modes.md`).** Rejected after one round of review feedback: the file is conceptually about the *architecture alternatives*, and locating it next to its sibling architecture docs (under `architectures/`) makes the dependency direction visible. Top-level placement would have suggested the matrix is independent of the architecture set.
- **Make the matrix the source of truth and regenerate `00-comparison.md` §2.4 from it.** Rejected: this conflates two documents with different lifecycles. The matrix lives forever as the canonical coverage assessment; `00-comparison.md`'s §2.4 (now a 1-line pointer) lives only as long as readers expect to find coverage information in the comparison doc.
- **Document the discipline inline in `failure-modes.md` (no separate skill).** Rejected after one round of review feedback that asked for the schema, lint, and gate to all live inside a single skill directory. The skill-bounded layout means the discipline survives copying the skill into a fresh repo, and the no-prompt pre-flight removes the manual-install failure mode.
- **Add the discipline as an `AGENTS.md` rule.** Rejected as part of the same skill-bounded direction: rules in `AGENTS.md` document expected behavior but cannot enforce it; the lint + CI gate are the enforcement mechanism, and they need to be installed mechanically, not documented.

## Consequences

- **What becomes easier**: failure-mode coverage is now grep-able at a fixed canonical path; agents editing an architecture alternative are forced (by the gate) to update the matching column; the matrix can be cited from research reports and retrospectives without prefacing "see §2.4 of the comparison doc."
- **What becomes harder**: edits to an architecture alternative now require two file touches in the same PR (the alternative and column N of the matrix). The cost is real but small (~30 seconds of agent time per edit); the override-via-label escape hatch handles legitimately non-coverage-bearing edits.
- **Trade-off we accept**: one more skill to discover and load. The frontmatter description leads with the install command, and the `research-pipeline` skill cross-references the new skill in its decision tree, so the discoverability cost is bounded. The benefit of mechanical enforcement on a previously-rotting matrix outweighs the load cost.
- **Migration cost paid**: PR #113's six commits moved the content, relocated the file, hyperlinked references, built then refactored the gate, and reverted prior outside-skill content. Total: 9 files touched at the largest refactor. The migration is one-time.

## References

- [`../2026-05-21-113.md`](../2026-05-21-113.md) — the source retrospective.
- [`./SKILL-SPEC-7837ca0570-matrix-source-coupling-gate.md`](./SKILL-SPEC-7837ca0570-matrix-source-coupling-gate.md) — proposed generalization (factory skill for similar coupled-edit gates).
- [`./ADR-70fa46b61e-advisory-ci-gates-as-pr-reviews.md`](./ADR-70fa46b61e-advisory-ci-gates-as-pr-reviews.md) — the sibling ADR that captures the CI-as-PR-review pattern used by this skill's workflow.
- The shipped skill: `.claude/skills/architecture-failure-mode-gate/SKILL.md`.
- The canonical matrix: `architectures/failure-modes.md`.
- PR the decision was made in: #113.

<!--
PROMOTION NOTE:
When this draft is adopted into docs/adr/ via the `adr` skill, preserve
the `**ID**: ADR-b201e941ba` line verbatim. The NNNN number in the
docs/adr/ filename is a separate human-friendly sequence; the hash is
the durable identifier and must not drift.
-->
