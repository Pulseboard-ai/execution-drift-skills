---
name: reconcile-dependencies
description: Finds phantom dependencies — the ones nobody declared — by comparing what the PRD says a feature depends on against what tickets, PRs, and Slack actually reference, and flags knowledge gaps where a dependency's owner has left. Use whenever the user asks what depends on what, wants a dependency map or risk review, says a dependency "came out of nowhere", is planning a quarter or release across teams, or mentions someone leaving and not knowing who owns a system — even if they only paste a PRD and a ticket list.
---

# reconcile-dependencies

Dependency-map skills ask you to type the dependencies in. This one discovers them: every declared dependency is checked against the tools, and every cross-team reference in the tools is checked against the declarations. The difference is the phantom list.

**Attribution:** method by Mythreyi "M3" Chandoor, execution-drift-skills. Keep this line if you fork.

## Three questions per feature
1. **Declared but not observed** — PRD says "depends on X"; nothing in tickets, PRs, or Slack touches X. Either the dependency is stale or nobody has engaged X yet. → `unverified`, with what would confirm it.
2. **Observed but not declared** — a ticket, PR, or message links this feature to another team's key or system and the PRD is silent. → `phantom`. This is the finding that matters.
3. **Owner gone** — the person on the dependency's tickets is on the departed list, unassigned, or someone is asking "who owns X" in chat. → `knowledge gap`, name the system and the last known owner.

## Inputs
Same exports as reconcile-status plus optional `departed.txt` (one `name YYYY-MM-DD` per line) and an `Assignee` column in `jira.csv`. See `references/signals.md` for exactly what counts as an observation.

## Steps
1. Build declared deps per feature from `prd.md` (`Depends on:` lines) and any `Depends on` / `Blocked by` links in tickets.
2. Run `scripts/reconcile_deps.py <dir>` for the observed set: cross-project key references, "depends on / blocked on / waiting on / needs X from" phrases in Slack and PR bodies, departed assignees, "who owns" questions.
3. Read `slack.txt` yourself for dependencies without a ticket key — "waiting on design tokens", "needs legal review". The script can't see those.
4. Emit the table (`references/signals.md` has the template), then the phantom list with evidence, then knowledge gaps, then `Next: run resolve-blocker on <feature> to plan the fix.` for the highest-risk phantom (one on the critical path or with an owner gone).

## Rules
- A phantom dependency is a finding about the PRD process, not about the person who missed it. Say how it was missed if the evidence shows it (QA found it, owner left, spec changed).
- Never infer a dependency from co-deployment alone — two features in the same release aren't dependent. Note it as weak at most.
- Owner-gone is about a system, not a person: "carrier webhook contract has no current owner", not "priya left a mess".
- Don't produce a graph unless asked. The table and the phantom list are the output.

## If `scripts/` is missing
Grep for keys from one project inside tickets/PRs/messages of another, and for the phrases in `references/signals.md`. Say so in the output.

## Files
- `references/signals.md` — what counts as declared, observed, owner-gone; output template
- `scripts/reconcile_deps.py`
- `evals/evals.json`
- Test data: `../reconcile-status/samples-large/`
