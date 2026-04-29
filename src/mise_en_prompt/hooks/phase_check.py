"""PreToolUse hook: block recipe.md writes before phase=GUIDE.

When the chef agent tries to Write or Edit ``sessions/<id>/recipe.md``, this hook
loads the corresponding ``sessions/<id>/state.yaml`` and confirms that
``state.phase == GUIDE``. If not, the write is blocked.

Invocation: ``python -m mise_en_prompt.hooks.phase_check`` reading hook payload
JSON from stdin. Exit codes: 0 = allow, 2 = block.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from pydantic import ValidationError

from mise_en_prompt.state import Phase, State


_RECIPE_MD_RE = re.compile(
    r"sessions[/\\][^/\\]+[/\\]recipe\.md$",
    re.IGNORECASE,
)


def is_recipe_md_path(path: str) -> bool:
    """Return True if ``path`` matches the sessions/<id>/recipe.md pattern."""
    if not path:
        return False
    return bool(_RECIPE_MD_RE.search(path.replace("\\", "/")))


def derive_state_path_from_recipe_path(recipe_path: str) -> str:
    """Replace the trailing 'recipe.md' with 'state.yaml' in the same session dir."""
    return re.sub(r"recipe\.md$", "state.yaml", recipe_path, flags=re.IGNORECASE)


def check_phase_for_recipe(state_path: str) -> tuple[bool, str]:
    """Load state.yaml and return (allow, message) based on whether phase == GUIDE."""
    path = Path(state_path)
    if not path.exists():
        return False, f"no state.yaml found at {state_path}; cannot verify phase"
    try:
        state = State.load_yaml(path)
    except (ValidationError, ValueError) as exc:
        return False, f"state.yaml at {state_path} is invalid: {exc}"
    except Exception as exc:  # pragma: no cover — defensive
        return False, f"state.yaml at {state_path} could not be loaded: {exc}"
    if state.phase != Phase.GUIDE:
        return False, (
            f"recipe.md write requires phase=GUIDE, current phase is {state.phase.value}. "
            f"Complete CURATE and SYNTHESIZE first."
        )
    return True, "ok"


def main(argv: list[str] | None = None) -> int:  # noqa: ARG001
    """Read hook payload from stdin; exit 0 to allow, 2 to block."""
    try:
        if sys.stdin.isatty():
            return 0
        raw = sys.stdin.read()
        if not raw.strip():
            return 0
        payload = json.loads(raw)
    except (json.JSONDecodeError, OSError):
        print("[phase_check] could not read hook payload; allowing", file=sys.stderr)
        return 0

    tool_name = payload.get("toolName") or payload.get("tool_name") or ""
    if tool_name not in ("Write", "Edit"):
        return 0

    tool_input = payload.get("toolInput") or payload.get("tool_input") or {}
    file_path = tool_input.get("file_path", "")
    if not is_recipe_md_path(file_path):
        return 0

    state_path = derive_state_path_from_recipe_path(file_path)
    valid, msg = check_phase_for_recipe(state_path)
    if not valid:
        print(f"BLOCKED by phase_check hook: {msg}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
