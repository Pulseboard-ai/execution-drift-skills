---
date: 2025-12-01
type: environment
keywords: [test-env, staging, instability, chronic, regression]
program: consumer hardware platform (anonymized)
status: draft — from M3's scenario notes; verify durations and outcome
---
Blocker: Shared test environment down or unstable roughly a third of the time; regression runs kept restarting.
Gap: Environment owned by nobody; treated as everyone's problem and therefore no one's.
Options:
  - A: Keep retrying — hidden cost, ~2 engineer-days per week
  - B: Borrow a second environment from an adjacent team for the release period
  - C: Fund the environment fix as its own roadmap item with an owner; borrow in the meantime
Chosen: C
Why: Borrowing alone would recur next release. The cost-of-delay number (engineer-days lost per week) made the funding case.
Escalated: yes — Director, because it needed a roadmap slot
Time to resolve: 2 days to borrow, 6 weeks to fix
Outcome: Release unaffected; environment stable after the fix. Chronic environment issues are now escalated on the second occurrence, not the fifth.
