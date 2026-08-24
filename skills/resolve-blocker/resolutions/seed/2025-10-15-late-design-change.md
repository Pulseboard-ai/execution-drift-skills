---
date: 2025-10-15
type: priority
secondary: resource
keywords: [design-change, late, scope, launch-date, tradeoff]
program: enterprise fintech platform (anonymized)
status: draft — from M3's scenario notes; verify durations and outcome
---
Blocker: Design revised a core flow two weeks before code freeze; engineering estimated 3 weeks to absorb.
Gap: No change-control threshold after design sign-off.
Options:
  - A: Accept the redesign, move the date 3 weeks
  - B: Ship the original design, redesign as fast-follow — one-way door on first-impression UX
  - C: Split: ship redesigned flow for the primary path only, original for edge paths, full redesign next release
Chosen: C
Why: Primary path was 80% of usage; date held; edge paths were low-visibility.
Escalated: yes — VP Product + VP Eng, because it was a scope vs date call
Time to resolve: 2 days to decision, on-time delivery
Outcome: Shipped on date. Design and eng agreed a post-sign-off change needs the TPM's cost estimate attached before it's raised.
