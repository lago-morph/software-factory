# `research/manual/` — transient drop zone for manual fetches

This directory is the landing pad for raw content the user retrieves from a browser session (Path A: `fetch-from-browser.sh` with cookies; Path B: Save Page As → drag-and-drop). It is **transient** — every file here gets drained into a numbered report by the next `research-pipeline` activation, then deleted per Phase 6.

**If you are looking for primary sources that we deliberately keep on disk for re-quoting, see `/reference-only/` at the repo root.** That is where processed-but-still-useful sources live (El Kaim book chapters, the ChatGPT deep-research artifact, the Dark Factory / Brier / Every.to "My AI had already fixed" articles that anchor reports 03, 07, and followup/12).

## Lifecycle of a file in this directory

1. User drops file here (via `fetch-from-browser.sh` or Save Page As)
2. User commits + pushes
3. Next Claude session activates the `research-pipeline` skill, which scans this directory in Phase 0
4. Subagents fold the content into the relevant numbered report(s)
5. Phase 6 deletes the raw file (unless the orchestrator decides to keep it as a primary-source quote, in which case it moves to `/reference-only/`)

A non-empty `research/manual/` is a signal that there is unfinished drain work.
