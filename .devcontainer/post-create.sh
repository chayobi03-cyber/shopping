#!/usr/bin/env bash
set -euo pipefail

# Provide a general-purpose Python package manager. Do not install a specific
# coding agent, agent plugin, or specification CLI in the development image.
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

export PATH="$HOME/.local/bin:$PATH"

echo
echo "General development environment ready."
echo "Python: $(python --version)"
echo "uv: $(uv --version)"
echo "No coding agent, Spec Kit CLI, or Superpowers plugin was installed."
