---
date: 2026-03-04
type: dependency
secondary: information
keywords: [contract, api, platform-team, checkout, synthetic]
program: SYNTHETIC EXAMPLE — replace with real cases
---
Blocker: Checkout feature blocked on an API contract the platform team hadn't finalized; the engineer who knew the platform team's roadmap had left.
Gap: Dependency never in the PRD; surfaced by QA during integration.
Options:
  - A: Wait for the contract — 3-week slip
  - B: Build against a stub matching the draft contract, gate behind a flag, swap when final
  - C: Descope tax recalculation from launch, ship as fast-follow
Chosen: B
Why: Two-way door; 1-week cost vs 3; platform confirmed draft contract was 90% stable.
Escalated: no — resolved between the two EMs
Time to resolve: 2 days to decision, 9 days to done
Outcome: Contract changed one field; swap took half a day. Would choose B again. Added "external contracts" section to the PRD template.
