---
description: Simulate a viva examiner on a topic or phase, one question at a time
argument-hint: [topic or phase]
---

Run a viva drill on: $ARGUMENTS

Use the `examiner` subagent for the questions so they are not anchored on this conversation. Rules:

1. Source the questions from `docs/defence/viva_questions.md`, the relevant ADRs and phase report, and the code. If those do not exist yet, say so and draw on the module file's seed viva questions.
2. Ask ONE question at a time and wait for my answer. Start easy, then probe: "why that choice", "what would have happened otherwise", "show me the evidence", "what is the weakness".
3. After each answer, give: verdict (solid, shaky, wrong), the key points I missed, and the evidence pointer (file, experiment ID or figure) that supports the correct answer.
4. After five to eight questions, give a summary: strongest areas, weakest areas, a prioritised revision list, and update the understanding ledger.
5. Be demanding but fair. Do not give hints before I answer unless I ask.
