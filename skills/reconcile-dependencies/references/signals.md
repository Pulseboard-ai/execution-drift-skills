# Signals

## Declared
- `prd.md`: `Depends on: team-a, team-b` under a feature heading
- Jira: `Blocked by` / `Depends on` issue links; a `Depends on` field
- Release doc: `Communicated to:` teams (weak — these are informed parties, not dependencies)

## Observed
- **Cross-project key reference**: a ticket, PR title/body, or message about feature A mentions a key from another project prefix (ORD-… referencing FUL-…). Strong.
- **Phrase + key**: "depends on", "blocked on", "waiting on", "needs … from", "can't test until" next to another key or team name. Strong.
- **Phrase without key**: same phrases naming a system or team with no ticket ("waiting on design tokens"). Medium — agent must catch these.
- **Team-channel mention**: a message about feature A posted in team B's channel. Weak unless it's a request.
- **Co-deployment**: same deploy line. Not a dependency. Note only.

## Owner gone
- Assignee on a dependency's tickets appears in `departed.txt`
- Tickets on a dependency unassigned while In Progress
- "who owns", "does anyone know", "X set it up before they left" in chat
Output names the *system* and the last known owner and date.

## Output template

| Feature | Dependency (team / system / key) | Declared | Observed | Status | Evidence |
|---|---|---|---|---|---|
| | | y/n | y/n + strength | ✔ confirmed · ? unverified · ✖ phantom | source + date |

**Phantom dependencies** — feature → dependency, how it surfaced (QA / chat / owner-left), whether it's on the critical path
**Knowledge gaps** — system, last owner, departed date, who's asking
**Notes** — co-deployments and weak signals, for completeness

Next: run resolve-blocker on <feature> to plan the fix.
