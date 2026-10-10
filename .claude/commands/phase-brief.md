---
description: Produce the Technical Report (Phase Brief) for a phase and wait for approval
argument-hint: [phase, e.g. A-1]
---

Write the Phase Brief for phase $ARGUMENTS and do not write any code or create any files other than the brief itself until I explicitly approve.

First read `docs/agent/ROADMAP.md`, the current module file, and `docs/STATUS.md`. Then produce, in this order:

1. Assumptions (every one, first).
2. Clarifying questions for me (ask them rather than choosing the likeliest reading).
3. Design overview.
4. Tools and technologies, with pros and cons of each alternative.
5. Newer concepts or patterns used, each with a one-line plain-language explanation.
6. System design (ASCII diagram).
7. Code plan: modules, functions, tests, commands, expected outputs.
8. Risks and anti-patterns to avoid, including any weakness in my own request.
9. Learning plan for this phase: the one concept to teach first, then the order of the rest, with which library lessons and course chapters it needs.
10. GitHub plan: issues to open, branch names, PR slicing.
11. Standards and transfer: for each main technique in this phase, the established practice and its source, where we follow or deviate from it and why, and whether it carries over to Pakistan (Stage 2). This feeds the playbook entry at the end of the phase (`docs/playbook/`).

Save the brief to `docs/phase_briefs/$ARGUMENTS.md` only after I say go. End with: "Reply 'go' to approve, or tell me what to change."
