"""PreToolUse hook: validate state.yaml writes.

Blocks Write operations on ``sessions/<id>/state.yaml`` whose content fails to:
- Parse as YAML
- Validate against the State pydantic schema
- Satisfy research_log ordering (each entry's tag must have its precursor in the log,
  read from PRECURSORS for a dish session or DRINK_PRECURSORS for a drink one)

Edit operations on state.yaml are allowed (only old_string/new_string is visible
in the hook payload, not the resulting full content). The next Write to the same
file will catch any drift.

Invocation: ``python -m mise_en_prompt.hooks.state_validate`` reading hook
payload JSON from stdin. Exit codes: 0 = allow, 2 = block.
"""
from __future__ import annotations

import json
import re
import sys

import yaml
from pydantic import ValidationError

from mise_en_prompt.state import ResearchLogEntry, State


# Research-tag dependency graph. None means no precursor required.
PRECURSORS: dict[str, str | None] = {
    "aromatic_base": None,
    "functional_role": "aromatic_base",
    "candidate": "functional_role",
    "pairing": "functional_role",
    "technique": None,
}


# Drink research-tag dependency graph. Sibling of PRECURSORS; None means no precursor
# required. base_spirit is the drink analog of aromatic_base — roles cannot be assigned
# before the backbone is known. build_method is the analog of technique in that nothing
# precedes it, but unlike technique it gains a dependent: water pickup is a property of the
# build, so dilution cannot be computed until stirred/shaken/built has been decided.
DRINK_PRECURSORS: dict[str, str | None] = {
    "base_spirit": None,
    "drink_role": "base_spirit",
    "drink_candidate": "drink_role",
    "drink_pairing": "drink_role",
    "build_method": None,
    "dilution_math": "build_method",
}


_STATE_YAML_RE = re.compile(
    r"sessions[/\\][^/\\]+[/\\]state\.yaml$",
    re.IGNORECASE,
)


def is_state_yaml_path(path: str) -> bool:
    """Return True if ``path`` matches the sessions/<id>/state.yaml pattern."""
    if not path:
        return False
    return bool(_STATE_YAML_RE.search(path.replace("\\", "/")))


def validate_research_log_order(
    log: list[ResearchLogEntry], medium: str = "dish",
) -> str | None:
    """Return None if log ordering is valid, else a human-readable error message.

    The ordering dispatch point: ``medium`` selects which precursor table applies, the way
    _rules_for selects a conflict rule set. It defaults to ``dish`` so a legacy state.yaml
    with no medium key is ordered exactly as it was before drinks existed.

    A tag from the other medium's vocabulary is rejected rather than skipped. ``.get`` on the
    wrong table returns None, which reads as "no precursor required" — so without this check
    a dish session could walk past the ordering gate entirely by labelling its entries with
    drink tags. State enforces the same invariant at the schema level; this is the layer that
    states it in the hook's own voice, for callers that reach the ordering check directly.
    """
    precursors = DRINK_PRECURSORS if medium == "drink" else PRECURSORS
    seen: set[str] = set()
    for entry in log:
        if entry.tag not in precursors:
            return (
                f"entry tag '{entry.tag}' is not a {medium} research tag "
                f"(valid for {medium}: {', '.join(sorted(precursors))})"
            )
        precursor = precursors.get(entry.tag)
        if precursor and precursor not in seen:
            return (
                f"entry tag '{entry.tag}' requires '{precursor}' to appear earlier in "
                f"research_log (currently seen: {sorted(seen) or '[]'})"
            )
        seen.add(entry.tag)
    return None


def validate_state_content(content: str) -> tuple[bool, str]:
    """Validate a YAML string as a State.

    Returns (True, "ok") on success or (False, message) on any failure: parse
    error, schema violation, or research_log ordering violation.
    """
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        return False, f"state.yaml does not parse as YAML: {exc}"
    if not isinstance(data, dict):
        return False, "state.yaml must be a YAML mapping at the top level"
    try:
        state = State.model_validate(data)
    except ValidationError as exc:
        return False, f"state.yaml does not validate against State schema: {exc}"
    log_msg = validate_research_log_order(state.research_log, state.intent.medium)
    if log_msg:
        return False, f"research_log order violation: {log_msg}"
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
        # If we can't read the payload, don't block — fail-open with stderr note.
        print("[state_validate] could not read hook payload; allowing", file=sys.stderr)
        return 0

    tool_name = payload.get("toolName") or payload.get("tool_name") or ""
    if tool_name not in ("Write",):
        # Edit operations don't carry full content; skip.
        return 0

    tool_input = payload.get("toolInput") or payload.get("tool_input") or {}
    file_path = tool_input.get("file_path", "")
    if not is_state_yaml_path(file_path):
        return 0

    content = tool_input.get("content", "")
    if not content:
        return 0

    valid, msg = validate_state_content(content)
    if not valid:
        print(f"BLOCKED by state_validate hook: {msg}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
