# Agent Operating Contract

This repository combines Superpowers-style engineering discipline with GitHub Spec Kit-style specification-driven delivery.

## Required workflow
1. Read `spec-kit/constitution/CONSTITUTION.md`, `spec-kit/constitution/QUALITY_GATES.md`, and the active feature's `spec.md`.
2. For new behavior, refine the user story and acceptance criteria before implementation. Use brainstorming to identify assumptions and alternatives.
3. Keep the active `.specify/feature.json` aligned with the feature being changed.
4. Write or update the plan and dependency-ordered tasks before coding.
5. Use test-driven development: add a failing regression test, confirm the expected failure when a runnable environment exists, implement the smallest fix, then run the test.
6. Delegate independent domains (e.g. price, size, source adapters) to separate specialists when available. Keep shared-file writes sequential.
7. After implementation, perform two independent reviews: (a) specification compliance, (b) code quality/security.
8. Run tests and CI. Do not claim success without captured output.
9. Run convergence analysis against spec, plan, tasks, and code. Add tasks for every gap.
10. Auto-approve versioned artifacts only after all release gates pass.

## Superpowers skill mapping
Use the corresponding installed skill when available:
- brainstorming: refine intent and design before behavior changes.
- writing-plans: task-level implementation plan.
- dispatching-parallel-agents / subagent-driven-development: parallel independent work with review.
- test-driven-development: RED-GREEN-REFACTOR.
- systematic-debugging: establish root cause before repair.
- requesting-code-review / receiving-code-review: independent review and evidence-based response.
- verification-before-completion: verify before declaring done.
- finishing-a-development-branch: integration and branch completion.

## Spec Kit SDD mapping
Production feature path:
Constitution → Specify → Clarify → Plan → Checklist → Tasks → Analyze → Implement → Converge.

Spec Kit process commands run inside a supported coding agent, not in the shell. The repository currently keeps agent-neutral artifacts; install the Specify CLI and choose the intended integration to generate its native command/skill files.

## Safety and decision boundaries
- Agents research and propose; deterministic code validates.
- No LLM may change hard user constraints or override gate results.
- Unknown, stale, conflict, or missing provenance never passes a hard gate.
- BUY is a recommendation, not permission to transact.
- No checkout, payment, account mutation, or personal-data disclosure without explicit, transaction-specific user approval.
