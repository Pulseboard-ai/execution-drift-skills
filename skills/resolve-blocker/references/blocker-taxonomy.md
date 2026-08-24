# Blocker taxonomy

Pick one primary type. The type sets the option patterns and the usual escalation rung.

| Type | Tells | Option patterns | Usual rung |
|---|---|---|---|
| **decision** | Work paused waiting for a call nobody owns; two valid paths; "we need alignment" | Name a single decider; time-box; decide-then-review; pick the reversible path now | Director if cross-team, else EM |
| **dependency** | Blocked on another team/system; contract, API, data not ready; surfaced late by QA | Stub/mock and proceed; re-sequence to pull other work forward; negotiate a partial delivery; swap dependency | Both teams' managers; Director if priorities conflict |
| **resource** | Attrition, leave, lead ramping hires, fewer people than plan | Descope; extend date; borrow capacity with a defined return; pause a lower-priority item | EM, then Director for cross-team borrow |
| **information** | Owner left; nobody knows how the system works or who the partners are; PRD silent | Time-boxed spike to document; pair with the departed owner's peer; find the partner via ticket/commit history | EM (rarely escalates) |
| **alignment** | Two leaders disagree on scope/approach; teams optimizing different goals | Frame as a tradeoff with a shared metric; escalate to common manager; disagree-and-commit with a revisit date | Common manager of the two |
| **priority** | Team pulled onto something else; this item keeps slipping | Explicit re-rank with what it displaces; protect a fixed slice of capacity; stop the item openly | Director / VP owning the roadmap |
| **environment** | Test data missing, test env down, tooling blocks | Synthetic data; borrow another env; production-safe canary; fund the env fix as its own item | EM; Director if it's chronic |

## Secondary types
Common pairs: dependency + information (dep unknown because owner left); resource + priority (capacity exists but was reassigned). Name both; plan for the primary.

## Late-discovered dependencies
When a dependency appears from a tester or SME rather than the PRD, the memo must include a line on how it was missed. Not blame — the process gap is the real finding, and it feeds `reconcile-dependencies`.
