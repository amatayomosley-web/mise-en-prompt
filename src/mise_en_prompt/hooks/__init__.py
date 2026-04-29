"""Claude Code enforcement hooks for the chef agent.

Two hooks shipped:
  - state_validate: blocks Write to sessions/<id>/state.yaml when the schema or
    research_log ordering is violated.
  - phase_check: blocks Write/Edit to sessions/<id>/recipe.md when state.phase != GUIDE.

Registered in projects/public/mise-en-prompt/.claude/settings.json.
"""
