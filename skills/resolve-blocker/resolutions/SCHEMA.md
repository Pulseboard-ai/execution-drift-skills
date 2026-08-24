# Precedent log schema

One file per case: `resolutions/YYYY-MM-DD-<slug>.md`. Gitignored by default. Anonymize before sharing.

```
---
date: 2026-08-20
type: dependency            # decision | dependency | resource | information | alignment | priority | environment
secondary: information      # optional
keywords: [tax-service, contract, checkout]
program: <name or redacted>
---
Blocker: <one sentence>
Gap: <what was missing>
Options: 
  - A: <name> — <one line>
  - B: <name> — <one line>
Chosen: B
Why: <one line>
Escalated: yes/no — <rung>
Time to resolve: <n> days from memo to decision, <n> days to done
Outcome: <what actually happened; would you choose the same again?>
```

`scripts/precedent_search.py` matches on `type`, then ranks by keyword overlap, then recency.
