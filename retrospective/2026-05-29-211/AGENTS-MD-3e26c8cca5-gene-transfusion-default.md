# agent instruction

**Gene transfusion as default for factory self-build.** "When asking a factory (or any AI agent) to build a complex component, always identify the strongest available exemplar from public OSS or established research and brief the agent to transfuse from that exemplar rather than invent from scratch. Current-generation models port and adapt reliably; they invent unreliably. Record the exemplar's URL in the component's transfused_from metadata."

*Grounded in: v4 plan relies on gene transfusion at every Phase 3+ component (LocalStack for Layer 5 twins, Tracker Diagnose APIs for Layer 4 Healer, DSPy for Layer 6 prompt optimization, etc.), which makes the bootstrap plan credible.*

# justification

Gene transfusion is the technique that makes "factory builds factory" actually plausible. Without it, you'd be asking the factory to invent a diagnosis agent, a Healer, a twin scaffolder — all from scratch. Current models struggle at invention; they excel at porting. The v4 plan named specific transfusion sources for every Phase 3+ component, which is what shrinks the engineering risk from "research-frontier work" to "transfusion-and-orchestrate work." The marginal cost is one identification step per component (find the strongest exemplar, note its license, draft the transfusion brief); the asymmetry of value is enormous. Without transfusion, the bootstrap plan is wishful; with it, the plan is credible.
