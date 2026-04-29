"""Tests for the enforcement hooks."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from mise_en_prompt.hooks.phase_check import (
    check_phase_for_recipe,
    derive_state_path_from_recipe_path,
    is_recipe_md_path,
)
from mise_en_prompt.hooks.state_validate import (
    is_state_yaml_path,
    validate_research_log_order,
    validate_state_content,
)
from mise_en_prompt.state import (
    Candidate,
    Intent,
    Phase,
    ResearchLogEntry,
    ResearchPlan,
    State,
)


# Path matchers ----------------------------------------------------------------


def test_is_state_yaml_path_matches_session_state():
    assert is_state_yaml_path("sessions/2026-04-28-pinto-beans/state.yaml")
    assert is_state_yaml_path("/abs/repo/sessions/2026-04-28/state.yaml")
    assert is_state_yaml_path(r"C:\repo\sessions\2026-04-28\state.yaml")


def test_is_state_yaml_path_rejects_other_yaml():
    assert not is_state_yaml_path("sessions/state.yaml")  # no session dir
    assert not is_state_yaml_path("config.yaml")
    assert not is_state_yaml_path("sessions/abc/notes.yaml")


def test_is_recipe_md_path_matches_session_recipe():
    assert is_recipe_md_path("sessions/2026-04-28-pinto-beans/recipe.md")
    assert is_recipe_md_path(r"C:\repo\sessions\2026-04-28\recipe.md")


def test_is_recipe_md_path_rejects_other_md():
    assert not is_recipe_md_path("sessions/abc/notes.md")
    assert not is_recipe_md_path("README.md")


def test_derive_state_path_from_recipe_path():
    assert (
        derive_state_path_from_recipe_path("sessions/2026-04-28/recipe.md")
        == "sessions/2026-04-28/state.yaml"
    )


# validate_state_content -------------------------------------------------------


def _valid_state() -> State:
    return State(
        session_id="t-valid",
        phase=Phase.INTAKE,
        intent=Intent(star_ingredient="pinto beans"),
    )


def test_validate_state_content_valid_yaml_passes(tmp_path: Path):
    state = _valid_state()
    yaml_path = tmp_path / "state.yaml"
    state.dump_yaml(yaml_path)
    content = yaml_path.read_text(encoding="utf-8")
    valid, msg = validate_state_content(content)
    assert valid, f"expected valid, got: {msg}"


def test_validate_state_content_unparseable_yaml_blocks():
    bad = "this is :: not :: yaml :: at all\n: unclosed"
    valid, msg = validate_state_content(bad)
    assert not valid
    assert "yaml" in msg.lower() or "validate" in msg.lower() or "parse" in msg.lower()


def test_validate_state_content_missing_required_field_blocks():
    """State.session_id is required; YAML without it must be rejected."""
    bad = "phase: INTAKE\n"  # missing session_id
    valid, msg = validate_state_content(bad)
    assert not valid


def test_validate_state_content_invalid_phase_blocks():
    bad = "session_id: x\nphase: NOT_A_REAL_PHASE\n"
    valid, msg = validate_state_content(bad)
    assert not valid


# validate_research_log_order --------------------------------------------------


def _entry(tag: str) -> ResearchLogEntry:
    return ResearchLogEntry(
        timestamp=datetime(2026, 4, 28, 12, 0),
        tag=tag,
        query=f"query for {tag}",
        result_summary="summary",
    )


def test_research_log_empty_is_valid():
    assert validate_research_log_order([]) is None


def test_research_log_aromatic_base_first_is_valid():
    log = [_entry("aromatic_base"), _entry("functional_role"), _entry("candidate")]
    assert validate_research_log_order(log) is None


def test_research_log_technique_anywhere_is_valid():
    """technique has no precursors — can appear before aromatic_base."""
    log = [_entry("technique"), _entry("aromatic_base")]
    assert validate_research_log_order(log) is None


def test_research_log_functional_role_before_aromatic_base_blocks():
    log = [_entry("functional_role")]
    msg = validate_research_log_order(log)
    assert msg is not None
    assert "aromatic_base" in msg


def test_research_log_candidate_before_functional_role_blocks():
    log = [_entry("aromatic_base"), _entry("candidate")]
    msg = validate_research_log_order(log)
    assert msg is not None
    assert "functional_role" in msg


def test_research_log_pairing_before_functional_role_blocks():
    log = [_entry("aromatic_base"), _entry("pairing")]
    msg = validate_research_log_order(log)
    assert msg is not None


def test_validate_state_content_blocks_out_of_order_research_log(tmp_path: Path):
    """End-to-end: state with bad log order via validate_state_content."""
    bad_state = State(
        session_id="bad-order",
        phase=Phase.RESEARCH,
        research_log=[_entry("functional_role")],  # missing aromatic_base precursor
    )
    yaml_path = tmp_path / "state.yaml"
    bad_state.dump_yaml(yaml_path)
    content = yaml_path.read_text(encoding="utf-8")
    valid, msg = validate_state_content(content)
    assert not valid
    assert "research_log" in msg or "aromatic_base" in msg


# check_phase_for_recipe -------------------------------------------------------


def test_check_phase_for_recipe_blocks_when_not_guide(tmp_path: Path):
    state = State(session_id="phase-test", phase=Phase.CURATE)
    yaml_path = tmp_path / "state.yaml"
    state.dump_yaml(yaml_path)
    valid, msg = check_phase_for_recipe(str(yaml_path))
    assert not valid
    assert "GUIDE" in msg
    assert "CURATE" in msg


def test_check_phase_for_recipe_allows_when_guide(tmp_path: Path):
    state = State(session_id="phase-test", phase=Phase.GUIDE)
    yaml_path = tmp_path / "state.yaml"
    state.dump_yaml(yaml_path)
    valid, msg = check_phase_for_recipe(str(yaml_path))
    assert valid


def test_check_phase_for_recipe_blocks_when_state_missing(tmp_path: Path):
    missing = tmp_path / "does-not-exist" / "state.yaml"
    valid, msg = check_phase_for_recipe(str(missing))
    assert not valid
    assert "no state" in msg.lower() or "not found" in msg.lower()
