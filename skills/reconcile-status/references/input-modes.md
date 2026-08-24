# Input modes

## Paste
User pastes any mix of status doc, ticket list, PR list, Slack thread, PRD.
- Ticket keys: `[A-Z][A-Z0-9]+-\d+`. PR refs: `#\d+` or GitHub URLs.
- Feature list = headings/bullets in the status doc; fall back to epics.
- Evidence you can't map to a feature goes under "Unmapped evidence". Never drop it silently.

## Export (directory of files — any subset)
- `status.md` — reported status. Headings = features. Look for Done / On track / At risk / Blocked.
- `jira.csv` — columns used: `Issue key, Issue Type, Summary, Status, Parent, Resolution, Priority`. Extras ignored.
- `prs.json` — `gh pr list --state all --json number,title,state,isDraft,mergedAt,baseRefName,body,url`.
- `slack.txt` — one message per line: `YYYY-MM-DD HH:MM #channel @user: text`.
- `prd.md` — requirement lines matching `R-\d+`; dependent teams as `Depends on: team-a, team-b`.
- `deploys.txt` — optional: `YYYY-MM-DD tag sha env` per line.

Run `python scripts/reconcile.py <dir>` for the first-pass table, then read the files yourself to verify every conflicting row. The script is deterministic but shallow.

## Connected (MCP / CLI)
Pull the same things live: Jira epics + children + linked bugs; GitHub PRs mentioning ticket keys; Slack release and downstream channels since last deploy. Save what you pulled to a scratch dir and continue as Export mode so the evidence stays reviewable.
