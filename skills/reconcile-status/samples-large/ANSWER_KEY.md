# Answer key — planted discrepancies

Cells: ✔ confirmed · ✖ conflicting · ? unverified · ○ in progress (expected for non-Done) · – n/a until deployed. Links 1 and 7 are always `manual`.

| # | Feature | Reported | Planted drift | Expected cells |
|---|---|---|---|---|
| 1 | Guest checkout | Done | none — control | 2✔ 3✔ 4✔ 5✔ 6✔ 8✔ |
| 2 | Address validation | Done | PR #131 merged to feature branch, not main | 3✖ 5✖ 8– |
| 3 | Promo codes | Done | ORD-223 resolved Won't Do — scope cut not in status | all ✔; Won't Do in Notes; link 1 manual check names R-7 |
| 4 | Split shipments | On track | PR #145 reverted by #149; bug reported in chat, no ticket | 2○ 3✖ 5✖ 6? (bug in Slack, no ticket) 8– |
| 5 | Carrier rate API | Done | QA open, no deploy, Sev-2 open | 2✖ 5✖ 6✖ 8– |
| 6 | Warehouse picking UI | At risk | sandbagged — chain fully complete | all ✔; flagged "reported At risk, chain complete" |
| 7 | Order SMS | Done | tester-found dependency on FUL-310 (not in PRD); delivery path untestable; support-team not notified; Sev-3 open | 4✖ (blocked test after pass) 8✖; NTF-400→FUL-310 under Undeclared dependencies; NTF-405 in Notes |
| 8 | Email templates v2 | On track | draft PR open longer than a sprint | 2○ 3✖ stalled flag; design-token wait is a second undeclared dependency (no ticket key — agent judgment, not script) |

Script-vs-agent: the script produces rows 2–6 and 8 exactly. Row 7 link 4 and the design-token dependency need the agent to read slack.txt — the script has no key to match on. Expected Next: line → Carrier rate API (highest severity: three ✖ plus a Sev-2).

Manual checks expected: link 1 on every row (with R-7 and R-14 called out), link 7 on every Done row. Unmapped evidence: none.
