# Tool Independence Policy

## 1. Objective

The Shopping development process must remain portable across AI assistants, coding agents, IDEs, CLIs, hosted workspaces, and human-only workflows. Project policy and feature history must not depend on one vendor's runtime or command syntax.

## 2. Canonical source of truth

The following repository documents are authoritative:

1. \`docs/agentic/SHOPPING_CONSTITUTION.md\`
2. \`docs/agentic/RULEBOOK.md\`
3. \`AGENT_WORKFLOW.md\`
4. \`docs/agentic/QUALITY_GATES.md\`
5. Domain standards and schemas
6. Approved feature artifacts under \`specs/\`

Tool-specific files such as \`AGENTS.md\`, \`CLAUDE.md\`, IDE rules, prompt files, or generated skill definitions may point to these sources and provide execution hints. They must not establish a separate or contradictory policy.

## 3. No mandatory agent product

No specific coding agent or model is mandated. Codex, Claude Code, GitHub Copilot, other coding agents, and manual editing are possible interfaces, subject to access, privacy, and security requirements.

The repository does not require:
- Codex CLI or Codex App;
- Claude Code;
- GitHub Copilot;
- Spec Kit CLI;
- Superpowers plugin installation;
- any paid model or agent subscription.

Superpowers and Spec Kit are used as references for methods and lifecycle design, not as runtime dependencies.

## 4. Tool-selection criteria

Before adopting a tool, assess:

- Does it read and edit the repository files reliably?
- Can it preserve Git diffs and work on an isolated branch?
- Can it run tests and report actual command outputs?
- Can it read and follow repository instructions?
- Does it expose secrets, private product/source data, or customer information?
- What permissions, account scopes, data retention, and costs apply?
- Can the project continue if the tool is removed?

Record the decision and use the least privilege needed. Avoid overlapping tools that do the same job without measurable benefit.

## 5. Skill and prompt adapters

- The Markdown Rulebook is canonical; skill files are optional adapters.
- Keep adapters short and link to the relevant source policy rather than copying whole policies.
- If mirrored adapters exist, designate a canonical copy and verify equality after updates.
- Never treat a skill invocation, plugin presence, or model statement as proof that work was completed.
- Do not require a skill for a task that can be safely and correctly completed using the written workflow.

## 6. Portable execution contract

Any tool or human performing material work must return:

1. task classification and intended outcome;
2. repository baseline and affected paths;
3. relevant requirements and acceptance criteria;
4. plan and task ownership;
5. changes made and rationale;
6. tests/checks actually run and exact results;
7. unresolved issues, risks, and NOT_RUN/NOT_VERIFIED items;
8. commit/PR reference and requested human decision.

The interface may change; this evidence contract does not.

## 7. Tool migration

When changing tools:

1. preserve Git history, source documents, and feature artifacts;
2. verify that the new tool can read the canonical instructions;
3. map old commands to workflow stages without changing acceptance criteria;
4. compare any generated instructions or skill files against the Rulebook;
5. run a small positive/negative acceptance test;
6. retain the previous workflow until the new one is verified.

No tool migration may weaken source-policy, identity, evidence, test, review, or human-approval gates.
