# Skill spec — `reconstitute-and-index-sources`

## Status

**Stub.** This file is an *accumulator*. Each step in `/reference-only/reorg-plan.md` appends a `### From Step N` block below before opening its PR. Blocks may be disorganized — that's intended. The final step (skill instantiation) reads everything here plus the PR descriptions and synthesizes the actual skill at `.claude/skills/reconstitute-and-index-sources/SKILL.md`.

## Working name

`reconstitute-and-index-sources`

## Intent (rough)

When a corpus of primary-source material has been spread across many directories, partially deleted across past commits, or has outgrown its original flat-file inventory, this skill:

1. Reconstitutes the full set of sources (including those deleted in past commits).
2. Categorizes them into balanced, navigable groups.
3. Produces a top-level navigation README plus per-category `INDEX.md` files.

Refine this section in the final step. The plan at `/reference-only/reorg-plan.md` is a concrete instance of executing this skill — generalize from it.

## Triggers (draft, refine in final step)

TBD. Candidate triggers:
- User asks to "reorganize the reference-only directory", "reshape the corpus", "split the sources into categories".
- A README inventory table has grown past ~20 rows.
- Sources have been restored from git history and need re-indexing.

## Anti-patterns (draft, refine in final step)

TBD. Candidates from the plan:
- Splitting the README into INDEX files before the physical move (links won't resolve; categorization isn't yet pressure-tested).
- Adding prose during the split step (it's supposed to be mechanical).
- Combining steps into one PR (loses per-phase review checkpoint).
- Putting new steps *after* the skill-instantiation step (skill instantiation must be terminal).

---

## Lessons learned (accumulator)

### From Step 1

*(to be appended at the end of Step 1, just before the PR is opened)*

### From Step 2

*(to be appended at the end of Step 2, just before the PR is opened)*

*(further `### From Step N` blocks appended by each additional step)*

---

## Enhancement suggestions (accumulator, may be disorganized)

*(append freely during execution — bullets, half-thoughts, links, all welcome)*

---

## Final-step instructions for the synthesizer

When you reach the final step of `/reference-only/reorg-plan.md`:

1. Read every `### From Step N` block above plus the **Enhancement suggestions** section.
2. Fetch each prior step's PR description via the GitHub MCP tools and harvest additional learnings.
3. Look at sibling skills in `.claude/skills/` (`adr`, `research-pipeline`, `preliminary-index-pass`, `self-retrospective`, `parallel-subagent-fanout`) to match the project's skill-authoring conventions — frontmatter style, section ordering, length, anti-pattern lists, etc.
4. Synthesize into `.claude/skills/reconstitute-and-index-sources/SKILL.md`. Preserve specific, surprising, hard-won learnings (process gotchas, not just the recipe). Discard verbose contradictions only after reconciling them.
5. Cross-link the new skill back to this spec file in its PR description for provenance.
