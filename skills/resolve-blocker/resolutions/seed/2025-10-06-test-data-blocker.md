---
date: 2025-10-06
type: environment
secondary: dependency
keywords: [test-data, qa, synthetic-data, masking, compliance]
program: enterprise fintech platform (anonymized)
status: draft — from M3's scenario notes; verify durations and outcome
---
Blocker: QA could not run end-to-end tests; production-like test data was blocked pending a data-masking approval.
Gap: Test-data provisioning treated as a QA detail, not a program dependency with a date.
Options:
  - A: Wait for the masking approval — unknown duration
  - B: Generate synthetic data covering the required scenarios, accept lower coverage on edge cases
  - C: Escalate the approval as a program blocker with cost of delay attached
Chosen: B and C in parallel
Why: Synthetic data unblocked 80% of testing in 3 days; the escalation got the approval in a week instead of "eventually".
Escalated: yes — Director, to the data governance owner
Time to resolve: 3 days to partial unblock, 7 days to full
Outcome: No slip. Test-data readiness is now a named milestone in every plan.
