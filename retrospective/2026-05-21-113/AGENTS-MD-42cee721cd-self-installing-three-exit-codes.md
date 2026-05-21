# agent instruction

**Self-installing skills use three exit codes from `install.py --check`.** A self-bootstrapping skill's check script must distinguish three outcomes with distinct exit codes so the agent's auto-recovery branches correctly: `0` means installed and in sync (proceed); `1` means workflow / artifact missing or drifted (auto-fix with `--force`, no user prompt); `2` means a skill-internal file is missing (skill installation defect — re-copy the skill, do NOT auto-fix). Two exit codes (pass/fail) conflate recoverable drift with unrecoverable skill damage and make the auto-fix policy unsafe.

*Grounded in: `architecture-failure-mode-gate` `install.py` refinement in PR #113 commit `891eef3`.*

# justification

The existing `self-bootstrapping-skill` pattern documented two exit codes (success / failure) plus a passing mention of "exit 2 if template missing from the skill itself." PR #113 made the exit-2 case concrete and tested all three (delete lint script → exit 2; delete installed workflow → exit 1; everything intact → exit 0). The reason this needs to be enforced as a project-wide rule: if the agent's pre-flight maps "exit 1" to "auto-fix with `--force`" and the install script also returns 1 for skill-internal damage, the agent will repeatedly try to `--force`-install in a broken state, producing confusing error logs without ever surfacing the actual skill-defect cause. Three exit codes carry distinct recovery semantics; conflating two of them is the source of the failure mode. Marginal cost: ~6 lines of Python per install script. Marginal benefit: agents auto-recover correctly without operator intervention.
