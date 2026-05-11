# ADR skill

This skill records binding architectural decisions as numbered,
immutable, markdown ADRs at `docs/adr/`. See `SKILL.md` for the
operational specification.

## Why bother

The first 5 minutes of any agent session in this repo are spent figuring
out what's already been decided and why. ADRs short-circuit that. A
future agent can scan `docs/adr/` and learn:

- which decisions are binding (Accepted) vs. open (Proposed)
- when each was made and what motivated it
- which alternatives were considered and rejected
- which earlier decisions have been superseded

Without an ADR log, this knowledge is scattered across commit messages,
chat history (which is lost to context truncation), and tribal memory
(which a fresh agent doesn't have).

## When this skill earns its keep — concrete examples

| Situation | ADR title that would have prevented rework |
|---|---|
| Two agents independently build similar fetcher mechanisms with incompatible conventions | `ADR-0001: Use fetch-blocked-urls action for sandbox-blocked sources` |
| A new agent swaps Poetry for pip because they didn't know why Poetry was chosen | `ADR-NNNN: Use pip + uv.lock for dependency management` |
| A test framework migration silently breaks a downstream contract | `ADR-NNNN: Use pytest with the asserts-only style (no unittest)` |
| Someone proposes pushing workflow output to main; nobody remembers why we use side branches | `ADR-NNNN: Workflows commit to side branches; humans merge` |

In each case the ADR is short (~1 page) but the cost of not having it is
large (rework, regression, mis-aligned future work).

## Relative-link rule (the load-bearing invariant)

Every internal reference in an ADR uses a relative path:

```markdown
- [Research synthesis §3](../../research/00-synthesis.md#3-where-the-sources-disagree)
- [ADR-0002: ...](./0002-some-other-decision.md)
- [The workflow](../../.github/workflows/fetch-blocked-urls.yml)
```

**Not** absolute `https://github.com/...` URLs. The reason: relative
paths survive fork, rename, branch move, tarball export, and offline
read. Absolute GitHub URLs break the moment the repo is forked,
renamed, or mirrored — and the breakage is invisible until someone
clicks.

External resources (papers, blog posts, vendor docs) use absolute URLs;
that's correct because the URL is the canonical identifier.

The bundled `scripts/check_adr_links.py` walks `docs/adr/`, parses every
relative link, and verifies (a) the target file exists and (b) any anchor
fragment resolves to a real heading. Run it before committing an ADR.

## Anti-patterns

- **Treating ADRs as design docs.** ADRs are 1-page decisions. The full
  rationale lives in `research/` or `architectures/`.
- **Editing accepted ADRs.** They are immutable. To change direction,
  write a superseding ADR.
- **Skipping the supersession update.** When ADR-NNNN supersedes
  ADR-MMMM, both files change in one commit: NNNN is created, MMMM's
  Status line is updated to point at NNNN. Without bidirectionality the
  chain is broken.
- **Absolute GitHub URLs for repo content.** They break.

## Files in this skill directory

- `SKILL.md` — operational specification (trigger, workflow, anti-patterns).
- `templates/0000-template.md` — the template, copied to `docs/adr/0000-template.md` on first use.
- `scripts/check_adr_links.py` — link / anchor validator.
- `README.md` — this file.

## Bootstrapping

The first time this skill activates in a repo, it creates:

```
docs/adr/
  README.md            # the index (initially almost empty)
  0000-template.md     # copied from this skill's templates/
```

Subsequent invocations only add new `NNNN-*.md` files.
