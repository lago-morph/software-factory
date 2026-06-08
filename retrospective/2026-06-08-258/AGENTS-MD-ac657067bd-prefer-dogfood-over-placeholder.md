# agent instruction

**Prefer verified dogfood output over hand-written placeholders.** When the system under test can generate the artifact itself (a dogfood / factory build) and that output passes verification, ship the generated artifact with its provenance recorded, rather than a hand-written stub — even if you already wrote the stub.

*Grounded in: the prototype's own build loop producing a cleaner, working `beadview.py` than the placeholder the agent had written, which then replaced it.*

# justification

The agent shipped a hand-written placeholder `beadview.py` so the Docker image had something to bake, fully expecting to keep it. But the whole point of the exercise was to have the *prototype* build the viewer — and when the dogfood ran, it produced a 230-line, stdlib-only viewer that discovered `gc bd list --json` on its own, handled scroll math and `curses.error` gracefully, and met every spec point: objectively better than the placeholder. Shipping the placeholder anyway would have thrown away both the better artifact and its "the factory built this" provenance, which is the entire thesis being demonstrated. The rule costs nothing — it just says "when the real producer succeeds, use its output" — and it keeps the demonstration honest. The only guardrail is that the generated output must pass verification first (which the new always-test-fixes rule already enforces).
