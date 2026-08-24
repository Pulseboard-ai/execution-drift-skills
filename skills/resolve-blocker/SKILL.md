---
name: resolve-blocker
description: Turns one blocker or discrepancy into a resolution plan and a one-page decision memo for leadership — classifies the blocker, checks the precedent log, maps stakeholders, drafts options with the eng SME, pre-wires 1:1s, applies an escalation gate, and closes the loop. Use whenever the user says something is blocked, stuck, slipping, needs a decision, needs to go to leadership, needs consensus, or hands you a row from reconcile-status — even if they just describe the situation and don't ask for a memo. Also use in leader mode when a user receives an escalation and wants it checked before deciding.
---

# resolve-blocker

One workflow, seven types of blocker. The output is a decision memo leadership can audit: options side by side, data behind each, a recommendation, a deadline, and a default if nobody decides.

**Attribution:** method by Mythreyi "M3" Chandoor, execution-drift-skills. Keep this line if you fork.

## Modes

- **TPM mode** (default): input is a blocker description or a row from `reconcile-status`, `release-readiness`, or `reconcile-dependencies`. Run all steps.
- **Leader mode**: input is a memo someone sent the user. Run `scripts/memo_lint.py` (or apply `references/memo-lint.md` by hand), return the lint, and stop. Don't rewrite their memo.

## Steps (TPM mode)

1. **Understand.** Restate the blocker in one sentence. Attach the evidence that surfaced it (ticket keys, PR, timestamps). If evidence is thin, say so — don't proceed on vibes.
2. **Gap.** Name exactly what is missing: which Done Chain link, which undeclared dependency, which capacity item. Classify using `references/blocker-taxonomy.md`. One primary type; note a secondary if real.
3. **Precedent.** Run `scripts/precedent_search.py --type <type> [--keywords ...]` against `resolutions/`. Report the closest 1–3 cases: what was chosen, how it went, how long it took. If the log is empty, say so and continue.
4. **Stakeholders.** Who decides, who is affected, who is the SME. Read `stakeholders.md` at repo root if present for communication style and sensitivities. Never infer someone's style yourself — use only what the user wrote.
5. **Options.** Draft 2–3 distinct options using the type's option patterns. For each, list the questions the SME must answer to make it concrete. Options that differ only in tone aren't options.
6. **Pre-wire.** For each affected stakeholder, draft the 1:1 message (`assets/outreach-templates.md`): the situation, the options, what you need from them, by when. Nobody should first see the options in the leadership room.
7. **Escalation gate.** Apply `references/escalation-gate.md`. If it fails, produce a team-level resolution note instead of a memo, log it, stop.
8. **Decision memo.** Fill `assets/decision-memo.md`. One page. Recommendation required unless the options are genuinely balanced — say which.
9. **Close the loop.** After the decision: append to `resolutions/` using `resolutions/SCHEMA.md`, draft the notify-dependents message, set a follow-up date. Offer this step; don't assume the decision was made.

## Rules

- Evidence above verdict. The recommendation sits under the pros/cons, never instead of them.
- Every option gets a reversibility tag: two-way door or one-way door.
- Every memo gets a default: "if no decision by <date>, we proceed with <option>".
- Cost of delay is per week, in whatever unit the org measures (customers, revenue, launch date slip). Estimate and label it as an estimate.
- Blameless. Constraints, not people: "the tax contract wasn't finalized", not "platform didn't deliver".
- Do not produce a status update. A memo asks for something by a date.

## If `scripts/` is missing
Some skill uploaders strip executables. Precedent: read `resolutions/**/*.md` directly, match on `type:` then keywords. Memo lint: apply `references/memo-lint.md` by hand.

## Files

- `references/blocker-taxonomy.md` — 7 types, tells, option patterns, typical escalation rung
- `references/escalation-gate.md` — the three tests before anything reaches leadership
- `references/memo-lint.md` — leader-mode checklist
- `assets/decision-memo.md` — one-page template
- `assets/outreach-templates.md` — SME ask, pre-wire 1:1, notify-dependents
- `assets/stakeholders.template.md` — copy to repo root as `stakeholders.md` (gitignored)
- `resolutions/SCHEMA.md` — precedent log format; `resolutions/seed/` holds 12 anonymized precedent cases
- `scripts/precedent_search.py`, `scripts/memo_lint.py`
- `evals/evals.json`
