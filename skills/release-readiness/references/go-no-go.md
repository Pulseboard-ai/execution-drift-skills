# Go / No-Go rules

**GO** — every committed feature has links 2, 3, 5, 6 confirmed; no undisclosed scope cuts; no uncommitted PRs in the release, or all of them acknowledged in the release doc; stakeholders notified after the last change. Links 1 and 7 listed as manual checks still owed.

**GO-WITH-CUTS** — same as GO except one or more committed features are explicitly pulled from the release in this verdict, with the stakeholder message drafted.

**NO-GO** — any committed feature has a conflicting link and no cut decision has been made; or an undisclosed scope cut; or uncommitted work shipped that release stakeholders weren't told about.

## Output template

# Release <name> — target <date> — **<GO | GO-WITH-CUTS | NO-GO>**

| Committed feature | 2 | 3 | 4 | 5 | 6 | 8 | Ready? | Reason |
|---|---|---|---|---|---|---|---|---|

**Uncommitted in release** — PR, keys, merged date, disclosed in release doc? y/n
**Scope cuts** — requirement, resolution, disclosed? y/n
**Stakeholder comms** — team, last told, told after last change? y/n
**Manual checks owed** — link 1 and 7 per feature, owner
**To reach GO** — the shortest list of actions, one line each

Next: run resolve-blocker on <feature> to plan the fix.
