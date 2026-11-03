# Mobile-only setup: GitHub Codespaces + Codex + Spec Kit + Superpowers

This repository is being prepared for a user who currently has only an Android phone. Use GitHub Codespaces as the cloud Linux development machine and the mobile browser as the control surface. No local PC or Termux installation is required.

## What this setup does

- Runs the development container in GitHub's cloud.
- Uses browser-based VS Code in Codespaces.
- Installs Python 3.12, Node.js 22, uv, Specify CLI, and Codex CLI.
- Keeps source, specifications, tests, and Git history in the existing repository.
- Installs Superpowers inside Codex after the user authenticates.

The repository's `.devcontainer/devcontainer.json` and `.devcontainer/post-create.sh` define the environment. Codespaces creation and authentication are user actions.

## Mobile launch steps

1. Open this PR in Chrome on Android:
   https://github.com/chayobi03-cyber/shopping/pull/1
2. Open the PR head branch `adopt/agentic-workflow` in GitHub.
3. Open the branch's Code menu, choose Codespaces, then create a codespace on `adopt/agentic-workflow`.
4. Wait for the browser editor and post-create setup to finish. If the mobile UI hides the Codespaces action, open:
   https://github.com/codespaces
   then choose **New codespace** and select repository `chayobi03-cyber/shopping`, branch `adopt/agentic-workflow`.
5. In the Codespaces terminal, run:

```bash
specify version
specify check
codex --version
```

6. Start Codex:

```bash
codex
```

Complete the browser-based sign-in flow. Do not paste API keys, passwords, or tokens into chat or commit them to the repository.

7. Inside Codex, open the plugin interface:

```text
/plugins
```

Search for **Superpowers**, select **Install Plugin**, and restart Codex if requested.

8. Start a fresh Codex session in the repository and verify skill discovery:

```text
$using-superpowers
$speckit-constitution
```

If the first skill name is not directly invokable, ask Codex to list discovered Superpowers skills and confirm the Superpowers bootstrap instructions are active. Do not treat a printed claim as proof; inspect the installed plugin list and generated skill files.

## Initialize Spec Kit safely

The branch already contains project-owned policy, skill files, and a feature brief. Do not run initialization with `--force` until checking for path collisions.

First inspect:

```bash
git status --short
find .agents/skills -maxdepth 2 -name SKILL.md -print
ls -la .specify 2>/dev/null || true
```

If `.specify/` is not initialized yet, run:

```bash
specify init --here --integration codex --integration-options="--skills"
```

If the CLI reports that the directory is non-empty, stop and inspect the exact conflict. Do not blindly add `--force`. Back up/commit the current state first, then use the existing-project adoption guide and review the complete diff.

Verify:

```bash
specify check
specify integration list
git status --short
```

## First feature workflow

Use Superpowers for the discovery/design discussion, but keep Spec Kit as the canonical artifact owner.

1. In Codex, invoke Superpowers brainstorming for Product Identity Resolver.
2. Resolve open questions and record explicit decisions in the feature spec.
3. Run `$speckit-specify` using the accepted feature brief.
4. Run `$speckit-clarify` and resolve blocking ambiguities.
5. Run `$speckit-plan`.
6. Run `$speckit-tasks`.
7. Run `$speckit-analyze`.
8. Use Superpowers TDD and systematic debugging during implementation.
9. Run tests and `$speckit-converge`; review the diff and evidence before creating/updating the PR.

The initial scope is deterministic product identity resolution, not crawling, price ranking, or stock discovery. Identity must be established before downstream product facts are joined.

## Mobile usability tips

- Use Chrome's **Desktop site** option if the VS Code layout is too compressed.
- Rotate to landscape for terminal/editor work.
- Keep one Codespace; stop it when finished to avoid consuming compute hours while idle.
- Codespaces has a monthly included quota for personal GitHub accounts; monitor usage and spending limits in GitHub Settings → Billing → Plans and usage.
- Never commit `.env`, access tokens, browser cookies, or credentials.

## Acceptance checklist

- [ ] Codespace starts from the intended PR branch.
- [ ] Post-create script succeeds.
- [ ] `specify version`, `specify check`, and `codex --version` succeed.
- [ ] Codex authentication completes.
- [ ] Superpowers plugin appears in the installed plugin list.
- [ ] A fresh Codex session discovers Superpowers skills.
- [ ] Spec Kit Codex skills exist under `.agents/skills/speckit-*/`.
- [ ] Existing Shopping skills remain intact.
- [ ] No secrets are present in Git status or committed files.
