---
date: 2024-08-01
type: alignment
secondary: dependency
keywords: [scope-change, communication, dependent-teams, coordination-debt, notify]
program: consumer hardware platform (anonymized)
status: draft — from M3's scenario notes; verify durations and outcome
---
Blocker: Multiple mid-cycle changes to the feature; no single clear communication, so two dependent teams were building against the old spec.
Gap: Change decisions made in a team channel; no notify-dependents step existed.
Options:
  - A: Let dependents catch up on their own — they'd find out at integration
  - B: Freeze the spec, issue one consolidated change note with a diff, hold a 30-min sync with each dependent team
  - C: Roll back to the original spec
Chosen: B
Why: Rollback wasn't real (changes were customer-driven); a consolidated note plus 1:1s cost a day and stopped the bleed.
Escalated: no
Time to resolve: 1 day to notify, 5 days for dependents to re-plan
Outcome: One dependent team had 3 days of rework. Added a "dependents notified" gate to every change over a threshold; it's now Done Chain link 8.
