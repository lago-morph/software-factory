# Spec: `cross-corpus-propagation`

## Intent

When a drain or audit produces a finding that *refutes or amends* a claim already propagated across the corpus, the work isn't done when the source-report is updated. Every other place the old claim appeared must be corrected too — otherwise the corpus contains two contradictory framings of the same fact, and the wrong one is silently more numerous.

Grounded in this session's Phase D reversal-of-reversal episode: the Lenny × Willison transcript drain established that "Simon runs 4 agents in parallel and is wiped out by 11 AM" is verbatim-correct. A prior round (round 2 or so) had "corrected" the claim, calling the "4 agents" number a fabrication. That "correction" had propagated to 7 places: `research/00-synthesis.md` (4 refs in revision note + body + parallelism bullet + round-1 HN-row table), `research/06-hn-and-lenny.md` (7 refs in source-status block, body, notable quotes, quantitative claims table, outstanding questions, Cherny-section delta), and `research/blocked-urls.md` (1 audit-trail entry). All 12 references had to be reversed in a single pass.

The drain subagent that surfaces the reversal cannot do this pass — its brief is to update its target report only. The orchestrator can, but it's easy to forget. `cross-corpus-propagation` formalizes the pass.

## Trigger

**Direct phrases:**
- "Propagate this refutation"
- "Sweep the corpus for the old framing"
- "Cross-corpus fix"
- `/cross-corpus-propagation`

**Proactive trigger:** offer immediately after any drain subagent's report-back includes the words "refutes," "reverses," "corrects," "was wrong," "fabrication," or "reversal." These signals indicate cross-corpus debt.

**Negative trigger:**
- Refutations that are clearly local (e.g., a typo correction in one place) — don't dispatch a corpus-wide sweep for cosmetic fixes.

## Inputs

- The *refuted* framing (a string or short phrase that appears in the corpus).
- The *replacement* framing (what to put instead).
- The drain commit hash that established the refutation (for audit trail).
- Scope hint (e.g., "research/ + architectures/" vs "research/ only").

## Outputs

- Inline summary of every file/line corrected.
- A single commit (or commit chain) applying the corrections.
- A pending-followups entry in `research/PLAN.md` if any place uses the old framing in a context where the fix isn't a 1-for-1 swap (e.g., a body paragraph that argues *against* the old framing — that argument may need to be inverted, which is editorial, not mechanical).

## Workflow

1. **Build the search pattern.** Construct a `grep -niE` pattern covering the refuted framing and likely paraphrases. Example for the "4 agents → 11 AM" reversal: `grep -niE "4 agents.{0,8}11.AM|four agents.{0,8}fabricat|specific.*number.*fabricat|fabricated.*4|fabricated.*four"`.

2. **Scope the search.** Default to `research/*.md research/followup/*.md research/blocked-urls*.md architectures/*.md`. Exclude `retrospective/`, `reference-only/`, `.claude/skills/` (those are not the corpus).

3. **For each match**, classify by edit type:
   - **Trivial swap:** the line says "X is fabricated" → flip to "X is correct (reversal-of-reversal)." 1-for-1 replacement.
   - **Narrative inversion:** the line argues from the refuted premise. The whole paragraph may need rewriting.
   - **Audit-trail entry:** the line is part of a "revision notes" block or `blocked-urls.md` entry. Mark with strikethrough + REVERSAL-OF-REVERSAL note rather than deleting (preserve audit trail).

4. **Apply trivial swaps in bulk** via `Edit` (or multi-line patches).

5. **For narrative inversions**, present the orchestrator with the original paragraph + proposed replacement. Do NOT auto-apply — these need editorial judgement.

6. **For audit-trail entries**, append a "REVERSAL-OF-REVERSAL on [date]" footnote rather than removing the original entry. This preserves the history of corrections.

7. **Update the INDEX.md / PLAN.md** with a brief note about the reversal in the affected reports.

8. **Commit** with a clear message: `"Cross-corpus propagation: <refutation in 1 line>"`. Body lists every file:line touched.

## Concrete examples

### Example 1 — "4 agents → 11 AM" reversal-of-reversal (this session)

Drain commit: `cce6659` (Lenny Willison transcript drain).

- Refuted framing: "the 4 agents number was a fabrication; only the exhaustion claim is real."
- Replacement framing: "the Lenny Willison transcript drained 2026-05-13 contains verbatim: 'I can fire up like four agents in parallel and have him work on four different problems, and by like, 11am I am wiped out for the day.' The 4-agent count is real."

Search pattern run:

```
grep -niE "4 agents|four agents|mentally exhausted|11 a\.m\.|specific.*number.*fabricat|fabricated.*4|fabricated.*four" research/*.md research/followup/*.md research/blocked-urls*.md
```

Matches: 12 across `research/00-synthesis.md` (4), `research/06-hn-and-lenny.md` (7), `research/blocked-urls.md` (1).

Classification:
- `research/00-synthesis.md:15`, `:82`, `:142`, `:303` — all trivial swaps; flipped to the reversal-of-reversal framing with primary-source citation.
- `research/06-hn-and-lenny.md` lines 34, 57, 258, 406, 465, 502, 524 — mix of trivial swaps (table rows, notable quotes) and narrative inversions (body paragraphs in §"Practitioner sentiment splits"). Applied trivial swaps inline; rewrote one body paragraph.
- `research/06-hn-and-lenny.md` header — added a prominent "Drain note (2026-05-13)" block at the top documenting the reversal.
- `research/blocked-urls.md:112` — audit-trail entry; marked with strikethrough + REVERSAL-OF-REVERSAL annotation.

Total: 12 file:line edits + 1 new header block. One commit (`f480c8b`). The corpus is now internally consistent on the "4 agents → 11 AM" claim.

### Example 2 — Anthropic Skills `allowed-tools` re-classification

Hypothetical: a future drain surfaces that `allowed-tools` is in fact part of the canonical Anthropic SKILL.md spec (refuting the cross-ref from this session's `research/04-every-skill-libraries.md` update that says it's a Claude-Code extension).

- Refuted framing: "`allowed-tools` is a Claude Code extension, not part of canonical SKILL.md."
- Replacement framing: TBD by drain.

Search pattern: `grep -niE "allowed-tools.{0,40}(claude code extension|not canonical|not part of canonical)"`. Matches in `research/04-every-skill-libraries.md` (1) and `research/23-anthropic-engineering-trilogy.md` §3 drain note (1).

Apply inversion. Document the reversal-of-reversal in the report headers + PLAN.md.

## Anti-patterns

- **Sweeping without a primary-source anchor.** The sweep is justified by a drain that surfaced primary-source evidence. If the trigger is "I think X might be wrong," verify with a drain first; don't apply corpus-wide changes on speculation.
- **Auto-applying narrative inversions.** Trivial swaps are mechanical; narrative inversions need editorial judgement. Always surface narrative paragraphs to the orchestrator for review.
- **Deleting audit-trail entries.** A line in `blocked-urls.md` saying "X was a fabrication" should NOT be removed when X turns out to be real — strike through it and add a REVERSAL-OF-REVERSAL annotation. This preserves the history of how the understanding evolved.
- **Forgetting `architectures/`.** Cross-corpus is not just `research/`. The four candidate architectures often cite research findings; check them too unless the scope explicitly excludes them.
- **One pass, then forget.** After applying the corrections, log the reversal in `PLAN.md` (or wherever the rolling decision-log lives) so a future agent can see that "this was wrong, then right" rather than just "the corpus says X."
- **Skipping the INDEX update.** If a report's status changes (e.g., a reversal turns a 🟡-partial into ✅-full because the previously-refuted claim is now primary-anchored), update `INDEX.md` in the same commit.

## Acceptance criteria

1. Every match of the refuted framing in the scoped corpus is either corrected, marked as audit trail with strikethrough, or flagged for narrative review.
2. The orchestrator commits one (or one chained set of) commits with a clear cross-corpus message.
3. `PLAN.md` records the reversal in its decision log section.
4. Running the original `grep` after the sweep returns zero matches of the old framing (except inside audit-trail strikethrough blocks).
5. `INDEX.md` reflects any status changes resulting from the reversal.

## Files this skill creates / modifies

- Inline edits to any file matching the search pattern (typically several files under `research/`, `architectures/`).
- Updates `research/PLAN.md` with a one-line decision-log entry.
- Updates `research/INDEX.md` if any report's status changed.
- Creates one commit (or short chain) with a clear cross-corpus message.
