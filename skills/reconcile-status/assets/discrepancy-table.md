# Output template

## Discrepancy table

| Feature | Reported | 1 PRD | 2 Subtasks | 3 PR | 4 Tested | 5 Prod | 6 Defects | 7 Exercised | 8 Notified |
|---|---|---|---|---|---|---|---|---|---|
| <name> | Done / On track / At risk | manual | ✔ ✖ ? ○ | ✔ ✖ ? ○ | ✔ ? | ✔ ✖ ? | ✔ ✖ ? | manual | ✔ ✖ ? – |

Legend: ✔ confirmed · ✖ conflicting · ? unverified · ○ in progress (expected for non-Done) · – n/a until deployed · manual = human check required

## Findings (conflicting rows only)

**<Feature> — reported <status>, chain open at link <n>**
- Evidence: <ticket keys / PR numbers / message timestamps>
- What the reporter probably saw: <one charitable line>
- What would close it: <one line>

## Manual checks
- <Feature> link 1: <exact check> — owner <role>
- <Feature> link 7: <exact check> — owner <role>

## Unmapped evidence
- <anything not tied to a feature>

Next: run resolve-blocker on <feature> to plan the fix.

---

# Example (samples/)

| Feature | Reported | 1 PRD | 2 Subtasks | 3 PR | 4 Tested | 5 Prod | 6 Defects | 7 Exercised | 8 Notified |
|---|---|---|---|---|---|---|---|---|---|
| Checkout v2 | Done | manual | ✖ | ✖ | ? | ✖ | ✖ | manual | – |
| Search filters | On track | manual | ✔ | ✔ | ✔ | ✔ | ✔ | manual | ✔ |

**Checkout v2 — reported Done, chain open at link 2**
- Evidence: PAY-144 QA task In Progress; PR #88 draft since 2026-08-11; no deploy evidence; PAY-151 Sev-2 open
- What the reporter probably saw: epic flipped to Done when subtasks closed; PR and defect not reflected
- What would close it: finish PAY-144, merge #88, deploy, close PAY-151, then notify billing-team and notifications-team
