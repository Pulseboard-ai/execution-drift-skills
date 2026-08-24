# Escalation gate

Escalate only if at least one is true. Otherwise resolve at team level, log it, and don't send a memo.

1. **Authority.** The fix needs a decision the TPM and EMs can't make: budget, headcount, cross-org priority, customer commitment, a date already communicated externally.
2. **Cross-org tradeoff.** Two orgs would each give something up, and no common manager below the escalation rung exists.
3. **Cost of delay.** Estimated cost of one more week exceeds the org's threshold (set it in `stakeholders.md`; default: any slip to a date leadership has already repeated).

If the gate fails, output:

```
Team-level resolution — <blocker>
Type: <type> · Chosen: <option> · Owner: <name> · Done by: <date>
Why no escalation: <which tests failed>
Logged to resolutions/ · Follow-up: <date>
```

Leaders trust memos that arrive because the memos that don't need to arrive, don't.
