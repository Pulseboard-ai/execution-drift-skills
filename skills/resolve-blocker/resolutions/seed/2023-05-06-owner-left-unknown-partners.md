---
date: 2023-05-06
type: information
secondary: dependency
keywords: [attrition, knowledge-gap, partner-teams, undocumented, dependency-discovery]
program: consumer hardware platform (anonymized)
status: draft — from M3's scenario notes; verify durations and outcome
---
Blocker: The engineer who owned an integration left; nobody knew how the working system connected to partner teams. Dependencies started appearing as issues weeks later.
Gap: System knowledge and partner map lived in one person. No handoff doc, no ownership in the PRD.
Options:
  - A: Wait for the replacement hire to ramp and rediscover it — 6+ weeks
  - B: Two-day spike: mine tickets, commits, and Slack history for partner references, produce a dependency map, review with the departed owner's closest peer
  - C: Ask each candidate partner team to self-report dependencies — slow, incomplete
Chosen: B
Why: Cheapest path to a defensible map; the history was already in the tools.
Escalated: no — EM approved the spike
Time to resolve: 2 days to map, 3 weeks for all surfaced dependencies to close
Outcome: Map found four partner teams, two unknown to anyone still on the team. Added "system owner + backup" and a partner list to every PRD.
