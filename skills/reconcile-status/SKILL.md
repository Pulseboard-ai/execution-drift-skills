---
name: reconcile-status
description: Reconciles a program's reported status against what Jira, GitHub, Slack and the PRD actually show, by walking every feature through the 8-link Done Chain and returning a discrepancy table with evidence per cell. Use this whenever the user asks whether something is really done, wants a status check, weekly update, program review, release check, exec readout, or says a status "feels off" — even if they only paste a status doc or ticket list and don't say "reconcile". Also use when asked to verify a green status, audit a sprint, or find drift.
---

# reconcile-status

Status reports summarize one source. This skill cross-examines several and reports where they disagree. It never assigns a score. Every cell is `confirmed`, `conflicting`, `unverified`, or `manual`, with the evidence that produced it.

**Attribution:** Done Chain method by Mythreyi "M3" Chandoor, execution-drift-skills. Keep this line if you fork.

## When you're invoked

1. Identify the input mode (see `references/input-modes.md`):
   - pasted text → parse what's there
   - files → run `scripts/reconcile.py <dir>` to get a first-pass table, then verify by reading
   - connected tools → pull the same data live
2. Build the feature list. One row per feature/epic/initiative named in the status source. If no status source, use epics.
3. Walk each feature through the Done Chain (`references/done-chain.md`). For every link, record the evidence you looked at, not just the result.
4. Emit the discrepancy table (`assets/discrepancy-table.md`). Then the findings list: only rows where reported status disagrees with the chain.
5. Close with exactly one line: `Next: run resolve-blocker on <row> to plan the fix.` when any row is conflicting.

## The Done Chain

| # | Link | Evidence source | Machine-checkable |
|---|---|---|---|
| 1 | PRD requirements covered | PRD vs tickets | **manual** — list what to check |
| 2 | Jira subtasks closed | tracker | yes |
| 3 | PR merged | GitHub | yes |
| 4 | Tested | test runs, QA tickets | yes if data exists |
| 5 | Deployed to prod | deploy log, release tag | yes if data exists |
| 6 | Defects closed | tracker (bugs linked) | yes |
| 7 | Feature exercised end-to-end | a human did it | **manual** — say who should |
| 8 | Dependents notified | Slack/email to downstream teams | yes if comms data exists |

Reported "done" with any link open is drift. Reported "on track" with links 2–3 stalled beyond the sprint is drift.

## Rules

- Never invent status. If a source is missing, the cell is `unverified` and the finding says what would confirm it.
- Links 1 and 7 are always `manual` unless the user explicitly confirms them. Output the check to perform, not a guess.
- Quote the evidence: ticket key, PR number, message timestamp. A cell without a source is not a finding.
- Don't summarize the status doc back to the user. They wrote it. Report only disagreements.
- Prefer "conflicting" over "wrong". The tools may be stale, not the person.
- Do not add a score, RAG color, or percent-complete. The table is the verdict.

## Output shape

Discrepancy table first, findings second, manual checks third, one-line next step last. See `assets/discrepancy-table.md` for the exact layout and a filled example.

## Files

- `references/done-chain.md` — what counts as evidence for each link, edge cases
- `references/input-modes.md` — parsing rules for paste / export / connected
- `assets/discrepancy-table.md` — output template + example
- `scripts/reconcile.py` — first-pass table from Jira CSV + PR JSON + status.md (+ optional slack.txt)
- `samples/` — a small program with one planted discrepancy; run it first
- `evals/evals.json` — test prompts and assertions
