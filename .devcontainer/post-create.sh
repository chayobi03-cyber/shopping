#!/usr/bin/env bash
set -euo pipefail

# Install uv and Spec Kit in the Codespaces container.
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

uv tool install --upgrade specify-cli

# Install Codex CLI. Authentication is deliberately left to the user.
if ! command -v codex >/dev/null 2>&1; then
  npm install --global @openai/codex
fi

echo
echo "Tool bootstrap completed."
echo "Next: run 'specify version', 'specify check', and 'codex --version'."
echo "Authenticate Codex interactively with 'codex' and follow the browser login flow."
echo "Install Superpowers from inside Codex using /plugins."
