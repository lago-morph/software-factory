# Spec: `adr`

## Intent

Architecture Decision Records (ADRs) are short, immutable, numbered markdown files that record binding architectural decisions and the context that produced them. They answer "why did we do it this way?" without forcing the next agent to read the entire commit history.

In this session, two agents independently built duplicate fetcher mechanisms (`fetch-blocked-sources.yml` vs `fetch-blocked-urls.yml`) with incompatible conventions because no ADR captured the existing mechanism. Reconciliation took ~20 minutes; shipping both would have cost hours plus data fragmentation. **The presence of an ADR-0001 recording the fetch-blocked-urls mechanism would have made the duplicate unnecessary.** Every infrastructure decision earns an ADR for this reason.

This skill produces ADRs at `docs/adr/NNNN-kebab-title.md` using a structure compatible with `lago-morph/agent-os/adr` (a 41-ADR reference repo) as a small superset.

## Trigger

**Direct user requests:**
- "ADR this"
- "Record this decision"
- "Let's write it down"
- "Log the decision"
- "Why did we choose X?" (look-up of an existing ADR)
- `/adr`

**Proactive triggers (offer the skill):**
- A decision is being made that affects multiple files or lasts beyond the session.
- A default tool, library, framework, or pattern is being chosen.
- A non-obvious choice ("we will use X because Y") is being made.
- A prior decision is being reversed — write a superseding ADR.
- Substantive design conversation has concluded.

**Negative triggers (do NOT activate):**
- Tactical implementation choices internal to one file.
- Style preferences without architectural impact.
- Decisions you have not actually made yet (write the ADR *after* the call; design rationale lives in `research/` or `architectures/`).

## Inputs

- Title (sentence-case, kebab-case in filename).
- Status (default: `Accepted`).
- Date (today; verify via tool call if necessary).
- Context, Decision, Alternatives considered, Consequences — content the agent writes.
- References — relative paths to research, sibling ADRs, code.
- (Optional) Supersedes — number of the ADR this replaces.

## Outputs

- A new file at `docs/adr/NNNN-kebab-title.md`.
- If superseding: also an in-place edit to the prior ADR's Status line (`Superseded by ADR-NNNN`).
- An update to `docs/adr/README.md` (the index).
- A commit message in the form `ADR-NNNN: <Title> (<status>)`.

## Workflow

1. **Verify there's a real decision to record.** Affects multiple files / outlives this session, and is already made (or about to be made with user approval).
2. **Survey existing ADRs.** `ls docs/adr/` to find the highest number. If the directory does not exist, bootstrap it: `mkdir -p docs/adr; cp .claude/skills/adr/templates/0000-template.md docs/adr/0000-template.md`.
3. **Assign the next number** (zero-padded to 4 digits). Numbers are permanent; never reuse.
4. **Draft the ADR** from the template. Keep each section to ~1 paragraph or a small list.
5. **Wire up References** with relative links. Use direct subsection linking (multi-link bullet) for multiple sections of one file.
6. **If superseding:** update the old ADR's Status to `Superseded by ADR-NNNN` (in the same commit).
7. **Run the link checker:** `python3 .claude/skills/adr/scripts/check_adr_links.py docs/adr/`. Fix any reported broken links before committing.
8. **Update `docs/adr/README.md`** index (add a row for the new ADR).
9. **Commit** with message `ADR-NNNN: <Title> (<status>)`. Both files (new + supersession update, if any) in one commit.

## Section structure (mandatory order)

```markdown
# ADR NNNN: Title in Sentence Case

- **Status**: Proposed | Accepted | Deprecated | Superseded by ADR-NNNN
- **Date**: YYYY-MM-DD
- **Deciders** (optional): names or roles

## Context
## Decision
## Alternatives considered
## Consequences
## References
```

Heading case matters: lowercase `c` in "Alternatives considered". This matches the `lago-morph/agent-os/adr` convention and preserves anchor-slug compatibility.

## Concrete examples

### Example 1 — recording the fetch-blocked-urls decision

`docs/adr/0001-fetch-blocked-urls-mechanism.md` in this repo records the binding choice to use main's `fetch-blocked-urls` GitHub Action as the single mechanism for sandbox-blocked source retrieval. It exercises every feature:

- H1 form: `# ADR 0001: Use the fetch-blocked-urls action for sandbox-blocked sources`
- Status / Date only (no Deciders — using the agent-os subset).
- Sections in canonical order: Context, Decision, Alternatives considered, Consequences, References.
- **Direct subsection linking** in References for `research/PLAN.md` (three section anchors in one bullet) and `research/00-synthesis.md` (one anchor).

Read [`docs/adr/0001-fetch-blocked-urls-mechanism.md`](../../../docs/adr/0001-fetch-blocked-urls-mechanism.md) as a worked example.

### Example 2 — direct subsection linking in References

When citing multiple sections of one target file, prefer:

```markdown
- [overview.md](../overview.md) [§5](../overview.md#5-foo), [§6.2](../overview.md#62-bar), [§9](../overview.md#9-baz)
```

over:

```markdown
- [overview.md §5](../overview.md#5-foo)
- [overview.md §6.2](../overview.md#62-bar)
- [overview.md §9](../overview.md#9-baz)
```

The multi-link form is dense and scans well. The link checker treats each `[text](path)` independently regardless of bullet structure.

### Example 3 — superseding an existing ADR

When ADR-0007 supersedes ADR-0003, two files change in one commit:

```diff
# In docs/adr/0003-old-decision.md:
- - **Status**: Accepted
+ - **Status**: Superseded by ADR-0007
```

The body of ADR-0003 is **not** edited — only its status line. ADR-0007 is created fresh, with a "Supersedes" metadata line pointing back: `- **Supersedes**: ADR-0003`.

## Anti-patterns

- **ADR-as-design-doc.** ADRs are decisions. Long rationale lives in `research/` or `architectures/`; the ADR *references* it.
- **Editing accepted ADRs.** The whole point is immutability. Write a superseding ADR.
- **Absolute GitHub URLs to repo content.** They break under fork / rename / mirror. Use relative paths.
- **Implicit decisions.** "We just kind of started using X" → write an ADR retroactively. Otherwise the next agent will swap it.
- **Renumbering or reusing numbers.** Numbers are permanent — even for abandoned proposals.
- **One-way supersession.** Always update the old ADR's Status when writing a superseding ADR.
- **ADRs for tactical choices.** "We use 4-space indentation" is not an ADR. ADR-worthy means architectural.
- **Title-case "Considered".** The convention is "Alternatives considered" (lowercase `c`). Title-casing breaks anchor-slug compatibility with agent-os.

## Acceptance criteria

1. `docs/adr/NNNN-kebab-title.md` exists with the canonical section structure.
2. All internal references use relative paths (no absolute GitHub URLs).
3. `python3 .claude/skills/adr/scripts/check_adr_links.py docs/adr/` reports zero broken links.
4. If superseding: the old ADR's Status was updated in the same commit.
5. `docs/adr/README.md` index row was added.

## Files this skill creates / modifies

- `docs/adr/NNNN-kebab-title.md` — new ADR (creates).
- `docs/adr/0000-template.md` — bootstrap on first use (creates if absent).
- `docs/adr/README.md` — index (modifies, or creates on first use).
- `docs/adr/MMMM-prior.md` — Status line only, if superseding (modifies).
