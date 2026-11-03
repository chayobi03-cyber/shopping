# Mobile-only development: GitHub Codespaces

This guide describes an optional Android-only development path. It does not prescribe a coding agent. No local PC or Termux installation is required.

## What this setup provides

- A cloud Linux development container hosted by GitHub Codespaces.
- Browser-based VS Code controlled from Chrome on Android.
- Python 3.12 and a general-purpose Python package manager (\`uv\`).
- Repository source, Markdown rules, tests, and Git history in one workspace.

The environment does **not** install or authenticate Codex, Claude Code, Copilot, Spec Kit CLI, or Superpowers. The Rulebook is directly readable in the repository and can be followed from ChatGPT or another agent without plugins.

## Launch steps

1. Open the repository or pull request branch in Chrome:
   https://github.com/chayobi03-cyber/shopping
2. Select the branch you intend to work on. For the current Rulebook proposal, use \`adopt/agentic-workflow\`.
3. Open **Code → Codespaces → Create codespace on [branch]**.
4. If the mobile UI hides Codespaces, open:
   https://github.com/codespaces
   Then choose **New codespace**, repository \`chayobi03-cyber/shopping\`, and the intended branch.
5. Wait for the browser editor and container setup to complete.
6. Open a terminal and inspect the environment:

\`\`\`bash
git status --short
python --version
uv --version
\`\`\`

7. Read \`AGENTS.md\`, \`docs/agentic/RULEBOOK.md\`, and \`AGENT_WORKFLOW.md\` before changing files.

## Working without a coding-agent plugin

The user can edit Markdown files directly in the Codespaces editor, or provide relevant repository documents and the requested diff to an external assistant. The work should still follow the same gates:

1. State the intended outcome and affected files.
2. Read the canonical Rulebook and relevant domain standards.
3. Prepare or update the feature spec/plan/tasks for material changes.
4. Make the smallest change and inspect the complete diff.
5. Run relevant checks where available.
6. Report commands, results, untested areas, and open risks.
7. Keep merge/release under human control.

An external assistant's statement that it followed a method is not proof. Inspect the resulting files and verification evidence.

## Mobile usability

- Use Chrome's **Desktop site** option if the editor layout is compressed.
- Rotate to landscape for terminal/editor work.
- Stop the Codespace when finished to avoid idle compute use.
- Monitor the included usage quota and spending limit in GitHub Settings → Billing and plans.
- Never commit \`.env\`, access tokens, browser cookies, passwords, or credentials.

## Acceptance checklist

- [ ] Codespace starts from the intended branch.
- [ ] Python and \`uv\` are available.
- [ ] Git status and current branch are correct.
- [ ] Repository Rulebook and relevant standards are accessible.
- [ ] Existing local changes are understood before editing.
- [ ] No secrets are present in Git status or committed files.
- [ ] Tests and CI are reported only when actually executed.
