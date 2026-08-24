---
date: 2024-06-20
type: dependency
secondary: information
keywords: [prd-gap, qa, sme, late-dependency, integration]
program: enterprise fintech platform (anonymized)
status: draft — from M3's scenario notes; verify durations and outcome
---
Blocker: The QA lead, who was the subject-matter expert for the domain, flagged during test that the feature depended on a downstream service the PRD never mentioned.
Gap: PRD authored without the SME in the room; dependency section empty.
Options:
  - A: Slip to align with the downstream service's schedule — 4 weeks
  - B: Ship behind a flag with the dependency stubbed; enable when downstream is ready
  - C: Negotiate a partial delivery from downstream covering only the path this feature needs
Chosen: C
Why: Downstream could deliver the narrow interface in 1 week; full delivery was the 4-week item.
Escalated: yes — Director, because it changed the downstream team's sprint
Time to resolve: 3 days to decision, 8 days to done
Outcome: Delivered 1 week late. PRD template gained a required "dependencies reviewed with QA/SME" sign-off before dev starts.
