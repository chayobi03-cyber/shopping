# Agentic Engineering Workflow

## 1. Purpose

This repository uses two complementary systems:

- **Spec Kit** owns the specification lifecycle: intent, requirements, technical plan, tasks, and convergence.
- **Superpowers** owns execution discipline: problem framing, TDD, debugging, review, isolated work, and verification.

They are not competing planners. Spec Kit is the authoritative feature record; Superpowers provides the practices used to execute it.

## 2. Feature workflow

Use the full Spec Kit path for production features:

1. Confirm repository baseline, active branch, active Spec Kit feature, and existing tests.
2. Use Superpowers brainstorming only when the requested outcome, tradeoffs, or boundaries are unclear. Feed the approved outcome into the feature spec; do not keep a second design document.
3. Run Spec Kit specify.
4. Run clarify for unresolved behavior and acceptance criteria.
5. Run plan against the existing architecture and documented standards.
6. Run checklist for requirement completeness and risk coverage.
7. Run tasks and keep dependencies explicit.
8. Run analyze to identify inconsistencies across spec, plan, tasks, Constitution, and existing architecture.
9. Human reviews the artifacts before implementation begins.
10. Implement with Superpowers TDD. Every code task should have a test or an explicit reason why a test is not applicable.
11. Use systematic-debugging for failures; do not patch symptoms or weaken validation gates to make tests green.
12. Request code review after meaningful implementation slices and before merge.
13. Run verification-before-completion: tests, static checks, data-quality checks, and any reproducibility checks.
14. Run Spec Kit converge. Repeat implementation and convergence until remaining work is either closed or explicitly accepted as deferred.
15. Human reviews the final diff and approves merge/release.

Codex CLI uses Spec Kit skill invocation such as $speckit-specify. Claude Code uses /speckit-specify. Use the exact invocation syntax generated for the active integration.

## 3. Bug-fix workflow

For a defect in existing behavior:

1. Reproduce the defect and capture the failing test or deterministic evidence.
2. Use Superpowers systematic-debugging to trace the root cause.
3. Use the Spec Kit bug-fixing workflow if the fix changes a contract, data model, or externally observable behavior materially.
4. Add a regression test before the fix.
5. Fix the root cause with the smallest change.
6. Run the affected test set and broader regression tests.
7. Verify that the fix did not weaken a hard gate or alter unrelated behavior.
8. Record any revised rule or schema in the relevant documentation.

A trivial typo or isolated documentation correction does not need a full feature specification.

## 4. Skill routing

### Superpowers skills

Use when applicable:

- brainstorming: scope discovery before approving a new design;
- using-git-worktrees: isolate concurrent feature work;
- writing-plans: use only when no Spec Kit plan exists; otherwise enrich the Spec Kit plan;
- subagent-driven-development: independent task execution with review between tasks;
- dispatching-parallel-agents: independent research or implementation slices only;
- test-driven-development: implementation of deterministic logic;
- systematic-debugging: failures and unexpected behavior;
- requesting-code-review and receiving-code-review: independent review and response;
- verification-before-completion: evidence-backed completion;
- finishing-a-development-branch: tests, final review, and merge/PR decision.

### Spec Kit commands

Use for production features:

- constitution: once per project, then update only through an explicit reviewed change;
- specify: feature intent and user-visible requirements;
- clarify: ambiguity and missing acceptance details;
- plan: architecture and implementation approach;
- checklist: requirements-quality and risk checklists;
- tasks: actionable dependency-aware tasks;
- analyze: cross-artifact consistency;
- implement: execute approved tasks;
- converge: identify remaining gaps and reconcile artifacts.

## 5. Avoid duplicated work

- Do not produce a Superpowers plan and a separate Spec Kit plan for the same feature.
- Brainstorming output is input to spec.md, not an alternative specification.
- TDD tests must map to acceptance criteria or explicit quality requirements.
- Code review findings should become task updates or tracked defects, not unlinked chat notes.
- Humanizer must not modify numeric facts, units, model identifiers, URLs, citations, statuses, test expectations, or legal wording.
- Do not run all skills on every trivial change. Match the skill to the task trigger.

## 6. Parallel-agent controls

Parallel work is permitted only when tasks have independent ownership and stable interfaces.

Good candidates:
- separate source adapters with a frozen adapter contract;
- separate parser fixtures for independent source formats;
- independent documentation review;
- independent security and data-quality reviews.

Single-writer work:
- shared schemas and enums;
- database migrations;
- identity-resolution rules;
- source reliability scoring;
- global Constitution and AGENTS.md;
- release gates.

Every subagent handoff must include changed files, tests run, evidence, unresolved risks, and commit SHA. A reviewer must inspect each result before integration.

## 7. Evidence and release gates

For each change, preserve:

- branch and base commit;
- active Spec Kit feature path;
- commands and tool versions;
- test names and pass/fail counts;
- data-quality results and sample scope;
- unresolved conflicts or limitations;
- final commit and PR references.

No green status may be inferred from missing evidence. Use NOT_RUN, BLOCKED, or DATA_NOT_READY rather than implying success.

## 8. Document and report quality

Humanizer is optional and applies only to prose intended for human readers. It may improve readability, but facts and technical contracts are immutable. Compare before/after output and reject changes that alter any factual content.
