# agent instruction

**Promote user conceptual confusion into the artifact, not just the chat reply.** "When the user expresses confusion about how a deliverable models something, treat it as a defect in the deliverable: add or rewrite a section that answers it durably, then mirror the answer in chat. A confusion voiced once is usually shared by every future reader of the artifact."

*Grounded in: the user's 'why are beads separate from Gas City' question, which became the permanent doc section 'Why several components are really one install' and exposed a real framing weakness.*

# justification

The user asked why beads (C19/C20) are listed as components separate from Gas City when Gas City needs them to run. Answering only in chat would have left the same confusion latent for every future reader of the build-order doc — and, worse, would have missed that the question exposed a real framing weakness: the doc presented capabilities that ship *inside* one adopted binary as if they were independently built boxes. Converting the answer into a standing section ("Why several components are really one install") fixed the artifact, not just the conversation, and seeded the product→components table that the user then asked for explicitly. The marginal cost is writing one section instead of one chat paragraph; the benefit is that the artifact now pre-empts the confusion for everyone, and the act of writing it durably forces the framing weakness into the open where it gets fixed. User confusion is free QA signal about the deliverable — spend it on the deliverable.
