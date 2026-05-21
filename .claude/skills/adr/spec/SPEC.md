# `adr` — Implementation Spec

This is the reference specification. `../SKILL.md` is the executable
operational form (loaded by the harness on skill activation); this file
adds rationale, worked examples, and design decisions.

---

## 1. Intent

Architecture Decision Records (ADRs) are short, immutable, numbered
markdown files that record binding decisions and the context that
produced them. They are how a future agent (or human) answers "why did
we do it this way?" without re-reading the entire commit history.

The first 5 minutes of any agent session in a repo are spent figuring
out what's already been decided and why. ADRs short-circuit that. A
future agent can scan `docs/adr/` and learn:

- which decisions are binding (Accepted) vs. open (Proposed)
- when each was made and what motivated it
- which alternatives were considered and rejected
- which earlier decisions have been superseded

Without an ADR log, this knowledge is scattered across commit messages,
chat history (lost to context truncation), and tribal memory
(a fresh agent doesn't have it).

### 1.1 Concrete examples where an ADR earns its keep

| Situation | ADR title that would have prevented rework |
|---|---|
| Two agents independently build similar fetcher mechanisms with incompatible conventions | `ADR 0001: Use fetch-blocked-urls action for sandbox-blocked sources` |
| A new agent swaps Poetry for pip because they didn't know why Poetry was chosen | `ADR-NNNN: Use pip + uv.lock for dependency management` |
| A test framework migration silently breaks a downstream contract | `ADR-NNNN: Use pytest with the asserts-only style (no unittest)` |
| Someone proposes pushing workflow output to main; nobody remembers why we use side branches | `ADR-NNNN: Workflows commit to side branches; humans merge` |

In each case the ADR is short (~1 page) but the cost of not having it
is large (rework, regression, mis-aligned future work).

---

## 2. Compatibility with `lago-morph/agent-os/adr`

This skill follows the agent-os ADR convention as the canonical format,
with a small superset of features. ADRs produced by this skill can live
in agent-os-style repos without modification; ADRs from agent-os parse
cleanly through this skill's link checker.

| Property | agent-os | this skill |
|---|---|---|
| H1 form | `# ADR NNNN: Title` | same |
| Status states | Accepted | Proposed / Accepted / Deprecated / Superseded-by (superset) |
| Date | required | required |
| Deciders | not used | **optional** (superset) |
| Section order | Context → Decision → Alternatives considered → Consequences → References | same |
| "Alternatives considered" casing | lowercase `c` | same |
| Supersedes / Superseded by | not shown in samples | optional (superset) |
| Direct subsection linking in References | yes | yes (incorporated from agent-os) |

The superset additions (Deciders, lifecycle states, Supersedes /
Superseded-by) are all optional. An ADR using only the agent-os subset
is fully valid under this skill.

---

## 3. Section structure

Every ADR uses this exact section structure, in this order:

```markdown
# ADR NNNN: <Title in Sentence Case>

- **Status**: Proposed | Accepted | Deprecated | Superseded by ADR-NNNN
- **Date**: YYYY-MM-DD
- **Deciders** (optional): <names or roles>

## Context

(Evidence-driven. What is the issue we are seeing? What forces are at
play? Cite the research that informed it via relative links.)

## Decision

(What is the change we are making? State the chosen option in one
sentence at the top; expand below if needed.)

## Alternatives considered

(For each meaningfully-considered alternative, one paragraph: what it
is, why we did not pick it. Skip only if there were no real alternatives.)

## Consequences

(What becomes easier? What becomes harder? What trade-offs are we
accepting? Include "what we are explicitly not promising" if relevant.)

## References

(Relative links only for repo-internal content. Direct subsection
linking is encouraged for dense cross-references — see §5 below.)
```

Heading case is **load-bearing for anchor compatibility**: use
"Alternatives considered" (lowercase `c`).

---

## 4. The relative-link rule

All internal links use relative paths. No absolute GitHub URLs for
repo-internal content.

| Use | Don't use |
|---|---|
| `[sibling ADR](./0002-foo.md)` | `https://github.com/.../docs/adr/0002-foo.md` |
| `[synthesis §3](../../research/00-synthesis.md#3-...)` | `https://github.com/.../research/00-synthesis.md#3-...` |
| External: `[arXiv 2503.18813](https://arxiv.org/abs/2503.18813)` | (correct — absolute for external) |

Why: relative paths survive fork, rename, branch move, and tarball
export. Absolute GitHub URLs break the moment the repo is forked,
renamed, or mirrored — and the breakage is invisible until someone
clicks.

---

## 5. Direct subsection linking

When citing multiple sections of the same target file, prefer the
multi-link bullet form over multiple bullets:

```markdown
- [overview.md](../overview.md) [§5](../overview.md#5-foo), [§6.2](../overview.md#62-bar), [§9](../overview.md#9-baz)
```

instead of:

```markdown
- [overview.md §5](../overview.md#5-foo)
- [overview.md §6.2](../overview.md#62-bar)
- [overview.md §9](../overview.md#9-baz)
```

The multi-link form is dense and scans well. The link checker treats
each `[text](path)` independently regardless of bullet structure, so
it validates every anchor.

Both forms are legal. Use single-link bullets when the section
identity is the load-bearing part (sibling ADRs, single workflow
files); use multi-link bullets when you're citing several sections of
the same source.

---

## 6. Lifecycle

| State | Transition |
|---|---|
| **Proposed** | Initial state when a draft ADR is committed for review. |
| **Accepted** | Decision is binding. Move from Proposed once review is complete. |
| **Deprecated** | Decision no longer applies but is not directly replaced (rare). |
| **`Superseded by ADR-NNNN`** | A later ADR reverses or replaces this one. |

**The only legal in-place edits** to an Accepted ADR:

1. Changing **Status** to `Superseded by ADR-NNNN` when a later ADR
   replaces it.
2. Changing **Status** to `Deprecated` (with a short justification appended).
3. Fixing typos / broken links — never substantive content.

Substantive change always means writing a new ADR. **Bidirectional
supersession links** are required: when writing a superseding ADR,
update the old one's Status line in the same commit.

---

## 7. Anchor-link conventions

GitHub-flavored markdown derives anchors from heading text:

1. Lowercase the heading.
2. Replace spaces with hyphens.
3. Strip most punctuation (keep alphanumerics, hyphens, underscores).
4. **Do NOT collapse consecutive hyphens.** GFM preserves them: "A — B"
   produces `a--b` (two hyphens around where the em-dash was, because
   the surrounding spaces became hyphens).

Examples:

| Heading | Anchor |
|---|---|
| `## Context` | `#context` |
| `## Alternatives considered` | `#alternatives-considered` |
| `## 3.2 Where the sources agree` | `#32-where-the-sources-agree` |
| `## 6. GitHub Action — security stance` | `#6-github-action--security-stance` |

The check script applies these rules to verify anchor targets.

---

## 8. Worked example: ADR-0001

The first real ADR in this repo demonstrates every feature:

`docs/adr/0001-fetch-blocked-urls-mechanism.md`

- H1: `# ADR 0001: Use the fetch-blocked-urls action for sandbox-blocked sources`
- Status / Date metadata, no Deciders (using the agent-os subset).
- Sections in canonical order: Context, Decision, Alternatives
  considered, Consequences, References.
- References use both forms:
  - Single-link bullets for sibling skill, workflow file.
  - **Direct subsection linking** for `research/PLAN.md` (three section
    links) and `research/synthesis/00-synthesis.md` (one anchor).

Read it as a reference when writing the next ADR.

---

## 9. Bundled files

```
.claude/skills/adr/
├── SKILL.md                          # operational spec (harness loads this)
├── templates/0000-template.md        # canonical template
├── scripts/check_adr_links.py        # link + anchor validator
└── spec/SPEC.md                      # this file
```

On first use, the skill copies `templates/0000-template.md` into
`docs/adr/0000-template.md` and creates `docs/adr/README.md` as an index.

---

## 10. Link checker — design notes

`scripts/check_adr_links.py`:

- Walks one or more directories or files.
- Parses `[text](path)` and `[text](path#anchor)` patterns.
- **Skips** content inside fenced code blocks, inline code spans, and
  HTML comments — those are illustrative examples, not real links.
- For each non-skipped link:
  - Skips absolute URLs (http, https, mailto, ftp, data).
  - Resolves the relative path against the source file's directory.
  - Refuses to escape the repo root via `../..` tricks.
  - Verifies the target file exists.
  - If the link has an anchor fragment, derives all heading slugs in
    the target file (using GFM rules without hyphen collapsing) and
    verifies the anchor matches one of them.
- Reports broken links to stderr and exits non-zero on any failure.

### 10.1 GFM slug derivation

Implemented as: lowercase → replace spaces with hyphens → strip
non-alphanumerics-except-hyphen-and-underscore → **no collapse**. The
no-collapse rule is essential — GFM preserves consecutive hyphens
introduced by stripped punctuation. Empirically verified against
rendered TOCs on github.com.

### 10.2 Verified fixtures

7/7 slug derivation fixtures pass, including the em-dash case
needed by ADR-0001's reference to `research/PLAN.md` §6:

- `Context` → `context`
- `Alternatives considered` → `alternatives-considered`
- `3.2 Where the sources agree` → `32-where-the-sources-agree`
- `Use \`pip\`, not Poetry` → `use-pip-not-poetry`
- `What's next?` → `whats-next`
- `6. GitHub Action — security stance` → `6-github-action--security-stance`

---

## 11. Anti-patterns

- **ADR-as-design-doc.** ADRs are decisions, not designs. Keep each to
  ~1 page. Long rationale lives in `research/` or `architectures/`.
- **Editing accepted ADRs.** The whole point is immutability. Write a
  superseding ADR.
- **Absolute GitHub URLs to repo content.** They break under fork /
  rename / mirror. Use relative paths.
- **Implicit decisions.** "We just kind of started using X" → write an
  ADR retroactively. Otherwise the next agent will swap X for Y without
  knowing what they're undoing.
- **Renumbering or reusing numbers.** Numbers are permanent — even for
  abandoned proposals.
- **One-way supersession.** Always update the old ADR's Status when
  writing a superseding ADR.
- **ADRs for tactical choices.** "We use 4-space indentation" is not
  an ADR. ADR-worthy means architectural.
- **Title-case "Considered".** The convention is "Alternatives
  considered" (lowercase `c`). Title-casing the second word breaks
  anchor-slug compatibility with the agent-os repos.

---

## 12. See also

- [Michael Nygard, "Documenting Architecture Decisions"](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — the original ADR essay.
- [`lago-morph/agent-os/adr/`](https://github.com/lago-morph/agent-os/tree/main/adr) — the convention this skill aligns with; 41 real ADRs.
- [MADR (Markdown ADR) project](https://adr.github.io/madr/) — a fuller variant; we use a deliberately minimal subset.
