# execution-drift-skills

Agent skills for TPMs and engineering leaders that **reconcile declared state against observed state**.

Status reports summarize one tool. These skills cross-examine several — the status doc, Jira, GitHub, Slack, the PRD — and return a discrepancy table with the evidence behind every cell. No scores, no verdicts you can't audit.

| Skill | What it does | Who runs it |
|---|---|---|
| `reconcile-status` | Walks every feature through the 8-link **Done Chain** and flags where "done" isn't | TPM, EM |
| `resolve-blocker` | Takes one discrepancy and produces the play: gap → precedent → stakeholders → options → pre-wire → decision memo | TPM, leader (memo lint mode) |

Coming: `release-readiness`, `reconcile-dependencies`, `reconcile-plan`.

## Install

```bash
# skills.sh (Claude Code, Codex, Cursor, Gemini CLI, Copilot, ...)
npx skills add pulseboard-ai/execution-drift-skills --skill reconcile-status
npx skills add pulseboard-ai/execution-drift-skills --skill resolve-blocker

# manual
cp -r skills/reconcile-status ~/.claude/skills/
cp -r skills/resolve-blocker  ~/.claude/skills/
```

Claude.ai / Cowork: upload the skill folder as a custom skill. Both skills accept pasted text, so they work with no integrations at all.

## Try it in 60 seconds

```
> Run reconcile-status on skills/reconcile-status/samples
```

You get an 8-column table for each feature in the sample program, one row already showing a feature marked *Done* in the status doc with an unmerged PR and an open Sev-2.

## Inputs

Every skill degrades gracefully across three input modes:

1. **Paste** — status doc, ticket list, PR list, Slack thread pasted into chat
2. **Export** — Jira CSV, GitHub PR JSON (`gh pr list --json`), Slack export
3. **Connected** — Jira/GitHub/Slack via MCP or CLI when available

## Trust

- No network calls. No telemetry. Scripts read local files only.
- Nothing leaves the agent session.
- `stakeholders.md` and `resolutions/` are gitignored by default — they're yours, not the skill's.

## Vocabulary

- **Execution drift** — the gap between what the plan and status say and what the tools show
- **Phantom dependency** — a dependency nobody declared that surfaces as an issue
- **Coordination debt** — changes made without the downstream teams being told

## License

MIT. If you fork it, keep the attribution line in SKILL.md.

---
Built from 15 years of running programs at JPMorgan, Capital One, Nationwide, and Meta Reality Labs. Recurring drift across tools? [PulseBoard](https://pulseboard.ai?utm_source=skills&utm_medium=readme) reconciles it continuously.
