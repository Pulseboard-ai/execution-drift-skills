---
date: 2024-02-12
type: decision
secondary: dependency
keywords: [status, done, pr, unmerged, defects, prod, done-chain]
program: enterprise fintech platform (anonymized)
status: draft — from M3's scenario notes; verify durations and outcome
---
Blocker: Feature reported "Done" in the weekly status; walking the Done Chain showed subtasks closed but the PR unmerged, two open defects, and nothing in prod.
Gap: "Done" meant "dev complete" to the team and "shipped" to leadership. No shared definition; nobody had exercised the feature end to end.
Options:
  - A: Keep status green, fix quietly before launch — risk of surprise if it slips
  - B: Re-status to "code complete, not shipped", publish the Done Chain per feature going forward
  - C: Re-status and pull launch a week to absorb merge + defect fix
Chosen: B
Why: The status inaccuracy was the real risk, not the week. Leadership tolerates a slip they can see; not one they discover.
Escalated: no — corrected at the program review with the EM present
Time to resolve: 1 day to re-status, 6 days to actually shipped
Outcome: Done Chain became the status template for the program. Reported-vs-actual gaps dropped to near zero within two cycles.
