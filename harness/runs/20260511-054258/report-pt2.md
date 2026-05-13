# Fanout run pt-2 report — 20260511 (post-main-merge drain)

Run on 2026-05-11 after PR #25 merged the night-1 fanout to `main`. Goal: drain three branches that remained ahead of main after the user's cleanup pass.

## Summary

| Subtask | Source branch | Target report | Words | Refuted | New claims | Status |
|---------|---------------|---------------|------:|--------:|-----------:|--------|
| sub-30 Brier pace-layers drain | `claude/add-article-source-axo4b` | **NEW** `research/followup/12-brier-pace-layers.md` | 2,571 | 0 | (new report) | SUCCESS |
| sub-31 Klaassen Every trilogy drain | `fetched/issue-23` | `research/followup/05-klaassen-siblings.md` (2,330 → 5,731) | +3,401 | 4 | 15+ | SUCCESS |
| sub-32 Evals primary-source drain | `fetched/issue-24` | `research/followup/07-evals-deepdive.md` (2,150 → 4,511) | +2,361 | 2 | 10 | SUCCESS |

**Totals:** 3 subtasks dispatched in one parallel wave, 3 merged. 0 conflicts. ~8,300 words of new/upgraded content. 6 reconstructed claims **refuted by primary text** and corrected.

## Notable findings

- **Brier (sub-30):** the only voice in the corpus that explicitly pushes back on the software-factory metaphor. Five-layer pace-layers framework (standards → architecture → specs → plans → code) drawn from Stewart Brand. Candidate **F34 — cross-layer drift** added to the failure-mode catalog (locally consistent at fast layers; violates a slow layer). Brier is a user of StrongDM's substrate while a critic of its metaphor.
- **Klaassen (sub-31):** the most surprising win — `every.to/chain-of-thought/*` was action-fetchable despite `unfetched-sources.md`'s "Defer to user — Path B only" labeling. Four claim-level corrections landed: (1) article 3 author was actually Katie Parrott, not Klaassen; (2) fidelity tiers F1/F2/F3 came from article 1, not article 2; (3) the Puppeteer-Figma loop predicate was "until they match" (diff-equality), not "pixel-perfect"; (4) four claims previously sourced to article 3 (44 agents, 11 projects in 6 hours, `/lfg`, "folder is the agent") aren't there at all — they belong to other Klaassen pieces. Snippet-anchored research carries attribution-confusion risk.
- **Evals (sub-32):** Anthropic and Husain/Shankar primary sources locked down five load-bearing verbatim quotes. Two reconstructed claims **refuted**: (a) the ">90% expert agreement in 3 iterations" claim was never in the FAQ — replaced with the FAQ's actual TPR/TNR alignment guidance; (b) multi-agent token tax is **~15×** chat, not ~4× — corrected.

## Corpus-level lesson

Three hosts that `unfetched-sources.md` labelled "Defer to user / Path B" are in fact **action-fetchable** for publicly-visible bodies: `every.to/chain-of-thought/*`, `anthropic.com/engineering/`, `hamel.dev`. The sandbox 403s do NOT propagate to GitHub-runner IPs. Going forward: **always file a `[fetch-urls]` issue before invoking a browser-cookie pass**; escalate to Path B only when the action also returns ❌. This rule has been added to `research/unfetched-sources.md` and `research/PLAN.md` §14.3.1.

## Merge log

All 3 merges clean (`--no-ff`, no conflicts):
- a67877f → merge add-article-source-axo4b → merge fetched/issue-23 → merge fetched/issue-24 → sub-30 → sub-31 → sub-32.

## Final state

- Feature branch: `claude/parallelize-with-subagents-SO0nR` (re-created post-cleanup)
- `research/manual/` contains only `multi/` (Round-4 chapters per PLAN §12); the Brier .txt source is gone.
- `research/fetched/` is empty (removed during merge).
- `.fetch-work/` is gone.
- The two video-only Lenny URLs in `unfetched-sources.md` §"Currently unfetched" remain user-only (need YouTube transcript extraction).
- 8 deferred fetch-action candidate URL families remain unfiled in `unfetched-sources.md` §"Deferred fetch-action candidates"; one is now confidently action-fetchable (`anthropic.com/engineering/`) following pt-2 evidence.
