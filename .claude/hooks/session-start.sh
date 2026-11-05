#!/bin/bash
# SessionStart hook: prepare the environment the chef agent needs.
#
# The two PreToolUse enforcement hooks in .claude/settings.json shell out to
# `python -m mise_en_prompt.hooks.*`, so the package has to be importable before
# the agent writes its first state.yaml. A fresh remote container starts with
# neither the package nor its dependencies, so install them here.
#
# Idempotent and non-interactive: safe to re-run on every session start.
set -euo pipefail

# Only run in Claude Code on the web. Local checkouts manage their own env
# (virtualenv, pyenv, etc.) and should not have packages installed under them.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  echo "[session-start] not a remote session; skipping dependency install"
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

echo "[session-start] installing mise-en-prompt (editable) with dev extras"
python3 -m pip install --disable-pip-version-check --quiet -e ".[dev]"

# Smoke-check what the enforcement hooks actually import. `python -m <module>`
# on a missing package exits 1, which Claude Code treats as a non-blocking
# error, so a broken install would otherwise stay silent until it mattered.
echo "[session-start] verifying enforcement hooks are importable"
python -c "
import mise_en_prompt.conflicts
import mise_en_prompt.hooks.phase_check
import mise_en_prompt.hooks.state_validate
"

echo "[session-start] ready — chef enforcement hooks, pytest, and ruff are available"
