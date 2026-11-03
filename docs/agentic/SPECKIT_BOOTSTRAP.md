# Spec Kit and Superpowers Bootstrap

## 1. Scope and status

This guide prepares the existing shopping repository for Spec-Driven Development and Superpowers. Repository policies and domain skills are committed here. The Spec Kit CLI and Superpowers plugin must still be installed in the user's local coding-agent environment; a GitHub commit cannot install software on that machine.

Use the dedicated adoption branch first. Do not initialize directly on main.

## 2. Prepare a local checkout

Fetch and check out this branch:

    git fetch origin
    git switch --track origin/adopt/agentic-workflow

Confirm the working tree and base diff before running a scaffold generator:

    git status --short
    git log -1 --oneline

## 3. Install Spec Kit CLI

Prerequisites:
- Python 3.11 or later
- uv recommended, or pipx
- Git
- a supported coding agent

Recommended install:

    uv tool install specify-cli
    specify version

For reproducible team setup, record the exact output of specify version in the team's tool-version record and pin that version in setup documentation or bootstrap automation after it has been validated.

## 4. Initialize this existing repository

Choose one primary agent integration.

Codex CLI:

    specify init --here --force --non-interactive --integration codex

Claude Code:

    specify init --here --force --non-interactive --integration claude

The --force option acknowledges that this is a non-empty repository and may replace files at conflicting Spec Kit-managed paths. The branch is the reviewable baseline. Inspect the complete diff after initialization; do not accept unexplained changes to existing project documents.

Codex installs Spec Kit skills under .agents/skills/speckit-<command>/SKILL.md and uses $speckit-<command> invocation. Claude Code installs them under .claude/skills/speckit-<command>/SKILL.md and uses /speckit-<command>. Project-local Shopping skills are mirrored in both directories for these two harnesses. Keep the mirror copies identical. Follow the syntax generated for the selected integration.

Do not manually edit generated speckit-* skill files. Keep project policy in AGENTS.md and docs/agentic/SHOPPING_CONSTITUTION.md. The shopping-* skill files are project-owned and may be revised through normal review.

## 5. Create the project Constitution

After initialization, open the coding agent in this repository and run the generated constitution skill. Use the following instruction:

    Read docs/agentic/SHOPPING_CONSTITUTION.md and AGENTS.md.
    Establish the Spec Kit Constitution from those existing, approved project rules.
    Preserve the principles and hard gates without weakening or silently rewriting them.
    Place the result at the generated .specify/memory/constitution.md.
    Report any conflict with the generated template and show the diff for review.

Review the generated file against the source document. Commit the approved Constitution with the adoption branch.

## 6. Install Superpowers

Install Superpowers separately in each coding-agent harness that will use it.

Codex App:
- Open Plugins in the Codex app.
- Find Superpowers in the Coding category.
- Select Add and complete the installation flow.

Codex CLI:
- Open the plugin interface with /plugins.
- Search for superpowers.
- Select Install Plugin.

Claude Code:
- Install from the official Claude plugin marketplace:

    /plugin install superpowers@claude-plugins-official

Restart or open a fresh agent session if the harness requires it. Verify that using-superpowers is discoverable and that the agent can load the skills it claims to use.

Official project: https://github.com/obra/superpowers

## 7. First Spec Kit feature

The first bounded feature brief is:

    specs/001-product-identity-resolver/FEATURE_BRIEF.md

After Spec Kit initialization and Constitution approval, use the selected agent's generated specify skill with that brief as the source. Then complete the production workflow:

    specify → clarify → plan → checklist → tasks → analyze → implement → converge

For Codex, use the generated $speckit-* skill invocations. For Claude Code, use the generated /speckit-* skill invocations. Commands are executed in the agent chat, not as terminal commands.

## 8. Verify the setup

- [ ] specify version returns a version.
- [ ] The selected Spec Kit integration is listed by specify integration status.
- [ ] Expected Spec Kit skill files exist for the selected agent.
- [ ] Superpowers appears in the agent plugin/skill list.
- [ ] using-superpowers can be loaded.
- [ ] The project Constitution matches docs/agentic/SHOPPING_CONSTITUTION.md.
- [ ] Existing README and standards were not overwritten unexpectedly.
- [ ] The first feature's active directory is explicit in .specify/feature.json.
- [ ] A test invocation or dry run confirms the selected skills are callable.

## 9. Upgrade and maintenance

- Record the CLI version, Superpowers plugin version/revision, selected integration, and date in the project tool record.
- Review upstream changelogs before upgrading.
- Re-run integration status and inspect all generated file changes after an upgrade.
- Never update generated skill files by hand. Change project rules in AGENTS.md, the Constitution source, or project-local custom skills.
