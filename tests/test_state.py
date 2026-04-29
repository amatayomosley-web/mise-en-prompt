"""Tests for the session state schema."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from mise_en_prompt.state import (
    Candidate,
    Intent,
    Phase,
    PruneRule,
    PrunedItem,
    ResearchLogEntry,
    ResearchPlan,
    State,
)


def test_phase_enum_has_seven_values():
    assert {p.value for p in Phase} == {
        "INTAKE",
        "CLARIFY",
        "GROUNDING",
        "RESEARCH",
        "CURATE",
        "SYNTHESIZE",
        "GUIDE",
    }


def test_prune_rule_enum_has_four_values():
    assert {r.value for r in PruneRule} == {
        "cuisine_drift",
        "functional_redundancy",
        "allergy_hard_filter",
        "technique_impossibility",
    }


def test_state_minimal_construction():
    state = State(
        session_id="2026-04-28-pinto-beans",
        phase=Phase.INTAKE,
    )
    assert state.session_id == "2026-04-28-pinto-beans"
    assert state.phase == Phase.INTAKE
    assert state.intent.exclusions == []
    assert state.candidates == []
    assert state.selected == []
    assert state.pruned == []


def test_state_round_trip(tmp_path: Path):
    """Dumping then loading preserves all fields including nested models."""
    fixed_time = datetime(2026, 4, 28, 17, 0, 0)
    original = State(
        session_id="rt-test",
        phase=Phase.CURATE,
        created_at=fixed_time,
        updated_at=fixed_time,
        intent=Intent(
            star_ingredient="pinto beans",
            cuisine="Central American",
            cuisine_region="Honduran",
            heat_level="spicy",
            servings=4,
            time_budget_min=180,
            exclusions=["shellfish"],
            occasion="weeknight dinner",
        ),
        research_plan=ResearchPlan(
            aromatic_base="Latin sofrito (Honduran variant)",
            functional_roles_to_fill=["heat", "acid", "fat", "umami", "salt", "aromatic_herb"],
            techniques_under_consideration=["slow_simmer", "pressure_cook"],
        ),
        research_log=[
            ResearchLogEntry(
                timestamp=fixed_time,
                tag="aromatic_base",
                query="Honduran sofrito ingredients",
                result_summary="onion, garlic, sweet pepper, recao",
            ),
        ],
        candidates=[
            Candidate(
                name="chile cobanero",
                cuisine_origin="Honduran",
                functional_role="heat",
                intensity=7,
                notes="smoked, fruity, regionally specific",
            ),
        ],
        selected=["chile cobanero"],
        pruned=[
            PrunedItem(
                name="shrimp",
                rule=PruneRule.ALLERGY_HARD_FILTER,
                reason="user excluded shellfish",
            ),
        ],
    )

    target = tmp_path / "state.yaml"
    original.dump_yaml(target)
    loaded = State.load_yaml(target)

    assert loaded == original


def test_research_log_entry_rejects_unknown_tag():
    with pytest.raises(ValueError):
        ResearchLogEntry(
            timestamp=datetime(2026, 4, 28, 12, 0),
            tag="not_a_valid_tag",
            query="x",
            result_summary="y",
        )


def test_pruned_item_round_trip(tmp_path: Path):
    item = PrunedItem(
        name="miso",
        rule=PruneRule.CUISINE_DRIFT,
        reason="Japanese aromatic, target is Central American",
    )
    state = State(session_id="prune-test", phase=Phase.CURATE, pruned=[item])
    target = tmp_path / "state.yaml"
    state.dump_yaml(target)
    loaded = State.load_yaml(target)
    assert loaded.pruned[0].rule == PruneRule.CUISINE_DRIFT
    assert loaded.pruned[0].name == "miso"
