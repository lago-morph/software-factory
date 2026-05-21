# agent instruction

**Verify a script supports a flag before relying on a plan's invocation.** When a plan document, skill, or ADR specifies running `script.py --flag`, grep the script for the flag name (or run `--help`) before assuming the flag exists. Plan-document authors sometimes propose flags the script doesn't actually support; catching the gap early either uncovers a real implementation gap (file it) or a documentation slip (work around it inline and note it in the PR description).

*Grounded in: cleanup plan §L.2 specified `check-source-refs.py --fix` to repopulate `references_from`; the script has no --fix mode, so the equivalent jq edit was applied manually.*

# justification

The cleanup plan twice instructed running `python .claude/skills/research-pipeline/scripts/check-source-refs.py --fix` to repopulate `references_from`. The script has no `--fix` mode — `grep argparse check-source-refs.py` returned nothing, and the file has no flag handling at all. The plan author assumed the flag existed; the discipline of verifying before invoking caught the gap in seconds.

The recovery was cheap (one jq command in place of the missing script flag), and the PR description acknowledged the gap so a follow-up could either add the flag or update the plan. Without the verify-before-invoke check, the failure mode is: invoke the script, hit an argparse error or silent no-op, debug it, file an issue, possibly stall the PR. Five seconds of due diligence avoid all of that.

Marginal cost: one `grep` per non-trivial script invocation in a plan. Cost of skipping: every false invocation costs at least a few minutes of debug or a stalled commit.
