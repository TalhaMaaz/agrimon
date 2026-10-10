---
type: process
status: proposal
tags: [rhythm, planning]
---

# Weekly rhythm (a proposal; adjust to your real hours)

Assumption (unconfirmed): about 15 to 20 hours per week, one third of it learning. Change the numbers, keep the shape.

```
 MON  Plan        /session-start, pick issues for the week, /phase-brief if a new phase starts
 TUE  Build       one issue: branch, code with the agent, tests
 WED  Build       one issue; read the walkthrough of what was built
 THU  Build       finish, /open-pr, read your own diff line by line
 FRI  Review      review and merge PRs yourself; write the walkthrough questions you cannot answer
 SAT  Learn       paper or course session; /teach-back on the week's concepts; update your own notes
 SUN  Rest, or 30 minutes: tick the MAP, skim STATUS
```

## Every week (30 to 45 minutes, usually Friday or Saturday)

Run `/weekly-review`. It checks the roadmap against reality, the risk register, open PRs and issues, and the ledger, and asks you three questions about the week.

## Every two weeks

Run `/viva-drill <phase or topic>` for five to eight questions. Record the weak spots in the ledger.

## Every month

- Documentation audit (see DOCUMENTATION_PROTOCOL section 8).
- Re-read the roadmap; change the order if evidence says so. There is no schedule to defend.
- Clean-clone reproducibility check.
- Update the viva questions list.

## Rules of thumb

- A merged PR you cannot explain is technical debt in your head. Slow down.
- Never finish a week without one written note in your own words in `my_understanding/`.
- If a week is lost, do not try to catch up by skipping learning; cut scope in the order given in the roadmap.
