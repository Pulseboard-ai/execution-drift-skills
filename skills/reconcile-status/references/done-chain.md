# Done Chain — evidence rules per link

Fill all eight links for every feature. Record the evidence you looked at, not just the result.

## 1. PRD requirements covered — MANUAL
Machine can list PRD requirement IDs with no ticket referencing them. It cannot judge coverage.
Output: `manual: PRD reqs R-3, R-7 have no linked ticket — confirm with <PM>`.
If no PRD supplied: `unverified: no PRD`.

## 2. Jira subtasks closed
Confirmed when every child of the feature epic is Done/Closed/Resolved.
Conflicting when the parent is Done but any child is open, or status doc says done and any child is open.
Watch for: subtasks moved to another epic mid-sprint (count them); resolutions of *Won't Do* (list separately — that's a scope cut and the status doc should say so).

## 3. PR merged
Confirmed when every PR referencing the feature's ticket keys is merged to the release branch.
Conflicting when any is open, draft, or closed-unmerged.
Watch for: PRs merged to a feature branch not yet in main; a merged revert PR.

## 4. Tested
Confirmed when a QA ticket, test run, or CI check tied to the feature passed after the last merge.
Conflicting when a later message says testing of any requirement is blocked or failed — a pass followed by "blocked on X" means that requirement is untested, whatever the QA ticket says.
Unverified when no test evidence exists. Never infer "tested" from "merged". Tests run against a feature branch don't count for a feature reported in prod.

## 5. Deployed to prod
Confirmed by a deploy log, release tag containing the merge SHA, or a deploy message in the release channel.
Conflicting when status says "in prod" and the latest prod tag predates the merge.

## 6. Defects closed
Confirmed when all bugs linked to the feature (or created against it after code-complete) are closed.
Conflicting when any Sev-1/Sev-2 is open. Open Sev-3+ is a note, not a conflict.
Unverified with a note when a defect is described in chat but has no ticket — say "bug reported 08-12 in #channel, no ticket filed".

## 7. Feature exercised end-to-end — MANUAL
Output the check: `manual: has anyone walked the <feature> flow in prod? owner: <QA lead or PM>`.
Confirmed only if the user states it was done.

## 8. Dependents notified
Confirmed when a message to each downstream team's channel, or a release note, exists after deploy.
Conflicting when the PRD or ticket names a dependent team and no notification is found.
Unverified when no comms data was supplied — say which channels to check.

## Beyond the script
The script only matches ticket keys. Read `slack.txt` yourself for: blocked/failed tests after a pass, bugs reported without tickets, dependencies on things with no key ("waiting on design tokens"), and notifications posted in the wrong channel. List each under the relevant link or under Undeclared dependencies.

## Edge cases
- Feature renamed between PRD and tracker: match on ticket keys, not titles; flag the alias.
- Multiple repos: one unmerged PR anywhere keeps link 3 open.
- Reported "on track" rather than "done": apply the chain to sprint commitments; drift = a link stalled longer than the sprint length.
