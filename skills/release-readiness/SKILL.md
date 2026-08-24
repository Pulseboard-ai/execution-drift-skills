---
name: release-readiness
description: Checks a release against what was committed in planning — for every committed feature walks the Done Chain, flags uncommitted work that slipped into the release branch, checks release stakeholders were told, and returns a GO / NO-GO with a reason per feature instead of a score. Use whenever the user asks if a release is ready, wants a go/no-go, a release checklist, a cut decision, a launch readiness review, or asks "can we ship Friday" — even if they only paste a release plan or a PR list. Not a build-hygiene checklist (tests, lint, changelog); this is commitment-vs-delivery.
---

# release-readiness

Release-hygiene skills check that the build is clean. This one checks that the release is *what was promised*: every committed feature is actually done, nothing uncommitted rode along, and the people who were told a date have been told what changed.

**Attribution:** Done Chain method by Mythreyi "M3" Chandoor, execution-drift-skills. Keep this line if you fork.

## Inputs
- `release.md` — the committed scope: target date, committed feature keys, who was told. If none exists, ask for the planning doc or reconstruct from the last release-planning message.
- Same exports as `reconcile-status` (`jira.csv`, `prs.json`, `slack.txt`, `deploys.txt`, `prd.md`). See `../reconcile-status/references/input-modes.md`.

## Steps
1. Parse committed scope from `release.md`. Each committed key is a row.
2. For each committed feature, run the Done Chain (`../reconcile-status/references/done-chain.md`). Reuse `reconcile-status` output if it was already produced this session.
3. **Scope creep:** every PR merged to main since the planning date whose keys are not in the committed scope. List with evidence. Hotfixes are still scope creep for this purpose — they change what ships.
4. **Scope cuts:** committed requirements resolved Won't Do or descoped — flag whether the release doc discloses them.
5. **Stakeholder comms:** for each team in `Communicated to:`, is there a message after the last scope change telling them what changed? Silence after a change is a conflict.
6. Verdict per `references/go-no-go.md`. Then exactly one line: `Next: run resolve-blocker on <feature> to plan the fix.` for the highest-severity NO-GO reason.

Run `scripts/release_readiness.py <dir>` for the first pass; verify conflicting rows by reading the files.

## Rules
- Same cell vocabulary as reconcile-status: ✔ ✖ ? ○ – manual.
- GO / NO-GO / GO-WITH-CUTS is stated once, with the reason per feature under it. No percentage-ready, no RAG.
- NO-GO is not a judgment on the team. Write the reasons as constraints.
- Uncommitted work is reported, not condemned — the finding is "leadership doesn't know this shipped", not "someone broke process".
- If `release.md` is missing, do not guess the scope. Ask.

## If `scripts/` is missing
Apply steps 1–6 by hand using the Done Chain reference. Say so in the output.

## Files
- `references/go-no-go.md` — verdict rules and output template
- `scripts/release_readiness.py` — first-pass table + scope diff
- `evals/evals.json`
- Test data: `../reconcile-status/samples-large/` (has `release.md`)
