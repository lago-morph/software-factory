# agent instruction

**Address user confusion directly, not via meta-honesty sections.** "When the user expresses confusion about something you wrote, restate plainly. Don't structure the correction as 'honesty flags', 'things to acknowledge', 'two findings to record honestly', 'one wrinkle to flag', or similar meta-frames. The meta-frame adds parsing cost without adding clarity. State the corrected information; skip the narration about how you're being honest about correcting yourself."

*Grounded in: PR #218, the operator said "You have two sections with 'honest' in the header. They are both very confusing. Can you elaborate in plain language?" The meta-honesty framing was my coping mechanism for self-correction; it didn't help the reader.*

# justification

During PR #218's convergence write-up, I produced two adjacent summary blocks titled "Two findings to record honestly before I wrap up" and "Two honesty flags" — both contained valid content (the C08/C09 reclassification, the archive-in-place deviation from the original plan), but the meta-framing made the substance harder to find. The operator's response: "You have two sections with 'honest' in the header. They are both very confusing. Can you elaborate in plain language? It sounds like you ended up not doing anything? Or that there is more stuff to do, but we are deferring it somehow?"

The meta-honesty headers were a coping mechanism. I was correcting myself (the C08/C09 reversal, the deviation from the planned move-to-archive step), and the meta-frame felt necessary to mark "this is me being upfront." But from the reader's side, the frame is overhead. They have to parse "what does 'honesty flag' mean as a structural element here?" before getting to the content. And the substance — what changed, what was deferred, why — gets buried under the meta-narrative.

The fix is direct restatement. Instead of "Two honesty flags: (1) I reversed myself on 4 decisions, (2) I archived in place instead of moving," say "Three of the 25 keeps reclassified DROP on close read because they would reverse C08's deliberate spec/template collapse. I archived the optimized directories in place via a README rather than physically moving them; moving would have forced ~46 relative-link rewrites for cosmetic benefit." Same content, no meta-frame.

The cost of restraint is zero — the substance is the same. The cost of the meta-frame is the operator's parsing cost (they have to mentally strip the frame to find the content) plus a subtle erosion of trust (the meta-narrative reads as defensiveness rather than confidence). The asymmetry is decisive.

The rule generalizes to any structural meta-frame on a correction: "transparency note", "candor disclosure", "let me be honest about", "for full disclosure", "to be upfront". State the thing; do not narrate the stating.
