# agent instruction

**Confirm tail-of-file structure before composing Edit `old_string`.** "When using the Edit tool on a section near end-of-file, verify the literal trailing characters in your proposed `old_string` (closing fence markers, trailing blank lines, final newline placement) match the actual file content. Run a quick `tail` or targeted `Read` on the relevant range before submitting — stale trailing characters fail the exact-match check and require an extra round trip."

*Grounded in: PR #95 spec/SPEC.md §13.7 edit that failed because old_string included a trailing ``` not present in the file.*

# justification

In PR #95 I composed an Edit `old_string` for the §13.7-§13.9 region of SPEC.md based on the structure of the surrounding similar sections in SKILL.md — which happened to end with a closing ``` code fence. The actual SPEC.md region did not. The Edit tool rejected the call with "String to replace not found in file", and the error helpfully noted the literal mismatch was likely "elsewhere in old_string". One `tail` invocation fixed it; the failure cost one extra tool round-trip plus the time to re-read and re-compose.

The cost of the rule is one `tail` or one ranged `Read` per Edit on long-file tails — sub-second, and you usually already have a Read for that range. The cost of skipping the rule is one full tool round-trip per failure, plus the recompose effort, plus the risk of the second attempt also failing if the agent invents a "fix" rather than checking the literal content. This is the cheap-rule / expensive-failure asymmetry that makes a sub-second pre-check obviously worth it.
