# agent instruction

**Sweep `references_from` when deleting any path the catalog tracks.** When `git rm`-ing a file path that appears in any record's `references_from` array in `reference-only/sources.json`, walk every record and remove the dead entry in the same commit. Use:

```bash
F=reference-only/sources.json
jq 'with_entries(if .value.references_from then .value.references_from |= map(select(. != "PATH/TO/DELETED")) else . end)' "$F" > /tmp/new.json && mv /tmp/new.json "$F" && bash .claude/skills/research-pipeline/scripts/normalize-sources-json.sh "$F"
```

Otherwise `check-source-refs.py` reports stale-reference warnings on the next lint run.

*Grounded in: deleting `research/plan-sync.md` and rewriting `research/PLAN.md` left a dozen records with stale `references_from` entries pointing at dead paths.*

# justification

Deleting `research/plan-sync.md` (a file that the cleanup plan explicitly retired) left ten records with `references_from: ["research/plan-sync.md"]` after the file was gone. The first lint run after the file deletion produced ten warnings — they weren't blocking errors (warnings only), but they would have stayed forever and accreted with every future delete.

The one-line jq sweep was inexpensive (sub-second), idempotent (running it again produces no change), and is the same shape regardless of which file path is being purged. Codifying it as a discipline rule means future "delete a path that lives in the catalog umbrella" operations don't accrete stale references — the catalog stays canonical.

Marginal cost: one jq command per file delete. Cost of not adopting: stale-reference warnings drift in the catalog and erode the URL-vs-reports check's signal-to-noise ratio.
