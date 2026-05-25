# agent instruction

**Iterate document clarity reviews until no MEDIUM-severity findings remain.** For load-bearing documents read by audiences outside the authoring context, dispatch fresh-context reviewers in successive rounds. Each round: reviewer with stable persona and constrained glossary; apply findings; dispatch another round. Terminate when a round reports 0 HIGH and 0 MEDIUM findings; LOW findings are optional.

*Grounded in: 6 rounds of primer reviews; each round found 2–7 MEDIUMs the prior round missed.*

# justification

The primer went through 6 rounds of clean-context review. Round 1 found 0 HIGH + 7 MEDIUM + 5 LOW. Each subsequent round found previously-invisible MEDIUMs even after prior MEDIUMs were fixed — because each fix opens new visibility into adjacent issues, and fresh-context reviewers don't carry the author's blind spots. The exit criterion ("0 HIGH, 0 MEDIUM") terminated naturally at round 6. A single-pass review would have shipped a document the user could not have used with confidence; the 6-round loop produced a document the user explicitly said "helped a lot." Marginal cost per round: one subagent dispatch (~3-5 minutes) plus ~5 minutes of fix application. Asymmetry: 30-50 minutes of review iteration vs. shipping a confusing document that downstream readers cannot use as a primer.
