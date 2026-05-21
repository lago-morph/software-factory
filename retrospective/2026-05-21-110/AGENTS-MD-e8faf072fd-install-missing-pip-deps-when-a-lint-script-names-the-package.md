# agent instruction

**Install missing pip deps when a lint script names the exact package.** When a project lint / validate / build script fails with a message containing `pip install <package>` literally (e.g., `jsonschema not installed: pip install jsonschema`), run that install command and re-run the script before treating the non-zero exit code as a real failure.

*Grounded in: first lint pass during PR #110 cleanup reported `FAIL: schema + structural` whose actual cause was a missing `jsonschema` package; `pip install jsonschema` resolved it in one command.*

# justification

The cleanup-PR's first `lint-sources.sh` run printed `FAIL: schema + structural` near the top of the output. Reading the body revealed `jsonschema not installed: pip install jsonschema` — the script was telling me exactly how to fix the problem, but the FAIL tag near the top is easy to read as a substantive validation failure that needs investigation.

`pip install jsonschema` took five seconds. Mistaking the missing-dependency case for a real validation failure would have wasted minutes hunting for non-existent schema issues. The rule generalizes: any time a script's own error text says `pip install X`, treat the missing dep as a precondition to satisfy before treating exit code as signal.

Marginal cost: one install command on first sandbox session. Cost of not adopting: minutes lost mis-classifying the failure mode on every fresh sandbox.
