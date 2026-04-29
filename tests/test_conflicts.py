"""Tests for the conflict detection rules."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mise_en_prompt.conflicts import (
    Severity,
    check_allergy,
    check_candidate,
    check_cuisine_drift,
    check_functional_redundancy,
    check_technique_impossibility,
    filter_candidates_for_role,
)
from mise_en_prompt.state import (
    Candidate,
    Intent,
    Phase,
    PruneRule,
    State,
)


def _state_with(
    intent: Intent,
    candidates: list[Candidate] | None = None,
    selected: list[str] | None = None,
) -> State:
    return State(
        session_id="t",
        phase=Phase.CURATE,
        intent=intent,
        candidates=candidates or [],
        selected=selected or [],
    )


# check_allergy ----------------------------------------------------------------


def test_allergy_direct_match():
    state = _state_with(Intent(exclusions=["shrimp"]))
    candidate = Candidate(name="dried shrimp", cuisine_origin="Asian", functional_role="umami")
    finding = check_allergy(candidate, state)
    assert finding is not None
    assert finding.severity == Severity.HARD
    assert finding.rule == PruneRule.ALLERGY_HARD_FILTER


def test_allergy_alias_shellfish_to_shrimp():
    state = _state_with(Intent(exclusions=["shellfish"]))
    candidate = Candidate(name="shrimp", cuisine_origin="Asian", functional_role="protein")
    finding = check_allergy(candidate, state)
    assert finding is not None
    assert finding.rule == PruneRule.ALLERGY_HARD_FILTER
    assert "shellfish" in finding.reason


def test_allergy_alias_dairy_to_butter():
    state = _state_with(Intent(exclusions=["dairy"]))
    candidate = Candidate(name="brown butter", cuisine_origin="French", functional_role="fat")
    finding = check_allergy(candidate, state)
    assert finding is not None
    assert finding.severity == Severity.HARD


def test_allergy_no_exclusions_returns_none():
    state = _state_with(Intent())
    candidate = Candidate(name="shrimp", cuisine_origin="Asian", functional_role="protein")
    assert check_allergy(candidate, state) is None


def test_allergy_no_match_returns_none():
    state = _state_with(Intent(exclusions=["shellfish"]))
    candidate = Candidate(name="chicken", cuisine_origin="American", functional_role="protein")
    assert check_allergy(candidate, state) is None


# check_cuisine_drift ----------------------------------------------------------


def test_cuisine_drift_same_group_no_conflict():
    state = _state_with(Intent(cuisine="Honduran"))
    candidate = Candidate(name="chipotle", cuisine_origin="Mexican", functional_role="heat")
    assert check_cuisine_drift(candidate, state) is None


def test_cuisine_drift_different_group_fires():
    state = _state_with(Intent(cuisine="Honduran"))
    candidate = Candidate(name="miso", cuisine_origin="Japanese", functional_role="umami")
    finding = check_cuisine_drift(candidate, state)
    assert finding is not None
    assert finding.severity == Severity.SOFT
    assert finding.rule == PruneRule.CUISINE_DRIFT


def test_cuisine_drift_no_target_cuisine_no_conflict():
    state = _state_with(Intent())
    candidate = Candidate(name="miso", cuisine_origin="Japanese", functional_role="umami")
    assert check_cuisine_drift(candidate, state) is None


def test_cuisine_drift_no_candidate_origin_no_conflict():
    state = _state_with(Intent(cuisine="Honduran"))
    candidate = Candidate(name="generic salt", cuisine_origin="", functional_role="salt")
    assert check_cuisine_drift(candidate, state) is None


# check_functional_redundancy --------------------------------------------------


def _seeded_chile_at_7() -> tuple[list[Candidate], list[str]]:
    cobanero = Candidate(
        name="chile cobanero", cuisine_origin="Honduran",
        functional_role="heat", intensity=7,
    )
    return [cobanero], ["chile cobanero"]


def test_functional_redundancy_same_role_close_intensity_fires():
    candidates, selected = _seeded_chile_at_7()
    state = _state_with(
        Intent(cuisine="Honduran"), candidates=candidates, selected=selected,
    )
    new = Candidate(
        name="chile chiltepe", cuisine_origin="Salvadoran",
        functional_role="heat", intensity=8,
    )
    finding = check_functional_redundancy(new, state)
    assert finding is not None
    assert finding.rule == PruneRule.FUNCTIONAL_REDUNDANCY


def test_functional_redundancy_far_intensity_no_conflict():
    candidates, selected = _seeded_chile_at_7()
    state = _state_with(
        Intent(cuisine="Honduran"), candidates=candidates, selected=selected,
    )
    new = Candidate(
        name="paprika dulce", cuisine_origin="Spanish",
        functional_role="heat", intensity=2,
    )
    assert check_functional_redundancy(new, state) is None


def test_functional_redundancy_stackable_role_no_conflict():
    """Aromatic herbs stack — multiple at same intensity is fine."""
    epazote = Candidate(
        name="epazote", cuisine_origin="Mexican",
        functional_role="aromatic_herb", intensity=5,
    )
    state = _state_with(Intent(), candidates=[epazote], selected=["epazote"])
    new = Candidate(
        name="cilantro", cuisine_origin="Mexican",
        functional_role="aromatic_herb", intensity=4,
    )
    assert check_functional_redundancy(new, state) is None


def test_functional_redundancy_different_role_no_conflict():
    candidates, selected = _seeded_chile_at_7()
    state = _state_with(Intent(), candidates=candidates, selected=selected)
    new = Candidate(
        name="lime", cuisine_origin="generic",
        functional_role="acid", intensity=5,
    )
    assert check_functional_redundancy(new, state) is None


def test_functional_redundancy_missing_intensity_no_conflict():
    """If either candidate has no intensity, can't compare — return None."""
    cobanero_no_intensity = Candidate(
        name="chile cobanero", cuisine_origin="Honduran", functional_role="heat",
    )
    state = _state_with(
        Intent(),
        candidates=[cobanero_no_intensity],
        selected=["chile cobanero"],
    )
    new = Candidate(
        name="chile chiltepe", cuisine_origin="Salvadoran",
        functional_role="heat", intensity=8,
    )
    assert check_functional_redundancy(new, state) is None


# check_technique_impossibility (v1 stub) --------------------------------------


def test_technique_impossibility_v1_stub_returns_none():
    state = _state_with(Intent(time_budget_min=30))
    candidate = Candidate(
        name="dried beans", cuisine_origin="generic", functional_role="protein",
    )
    assert check_technique_impossibility(candidate, state) is None


# check_candidate aggregator ---------------------------------------------------


def test_check_candidate_aggregates_multiple_findings():
    """A candidate triggering both allergy and drift returns both findings."""
    state = _state_with(Intent(cuisine="Honduran", exclusions=["shellfish"]))
    candidate = Candidate(
        name="dried shrimp", cuisine_origin="Japanese", functional_role="umami",
    )
    findings = check_candidate(candidate, state)
    rules = {f.rule for f in findings}
    assert PruneRule.ALLERGY_HARD_FILTER in rules
    assert PruneRule.CUISINE_DRIFT in rules


def test_check_candidate_no_findings_returns_empty_list():
    state = _state_with(Intent(cuisine="Honduran"))
    candidate = Candidate(
        name="lime", cuisine_origin="Mexican",
        functional_role="acid", intensity=5,
    )
    assert check_candidate(candidate, state) == []


# filter_candidates_for_role ---------------------------------------------------


def test_filter_role_hard_prune_excluded_from_compatible():
    pool = [
        Candidate(
            name="chile cobanero", cuisine_origin="Honduran",
            functional_role="heat", intensity=7,
        ),
        Candidate(
            name="dried shrimp paste", cuisine_origin="Asian",
            functional_role="heat", intensity=5,
        ),
    ]
    state = _state_with(
        Intent(cuisine="Honduran", exclusions=["shellfish", "shrimp"]),
        candidates=pool,
    )
    compatible, would_prune = filter_candidates_for_role("heat", state)
    names = [c.name for c in compatible]
    assert "chile cobanero" in names
    assert "dried shrimp paste" not in names
    pruned_names = [p.name for p in would_prune]
    assert "dried shrimp paste" in pruned_names


def test_filter_role_soft_drift_appears_in_both():
    """Soft conflicts: candidate stays in compatible (so user can pick) AND in would_prune (so agent flags)."""
    pool = [
        Candidate(
            name="chile cobanero", cuisine_origin="Honduran",
            functional_role="heat", intensity=7,
        ),
        Candidate(
            name="szechuan peppercorn", cuisine_origin="Chinese",
            functional_role="heat", intensity=6,
        ),
    ]
    state = _state_with(Intent(cuisine="Honduran"), candidates=pool)
    compatible, would_prune = filter_candidates_for_role("heat", state)
    compat_names = [c.name for c in compatible]
    assert "chile cobanero" in compat_names
    assert "szechuan peppercorn" in compat_names
    prune_names = [p.name for p in would_prune]
    assert "szechuan peppercorn" in prune_names


def test_filter_role_skips_other_roles():
    pool = [
        Candidate(
            name="chile cobanero", cuisine_origin="Honduran",
            functional_role="heat",
        ),
        Candidate(
            name="lime", cuisine_origin="generic",
            functional_role="acid",
        ),
    ]
    state = _state_with(Intent(), candidates=pool)
    compatible, _ = filter_candidates_for_role("heat", state)
    names = [c.name for c in compatible]
    assert "chile cobanero" in names
    assert "lime" not in names


# CLI smoke tests --------------------------------------------------------------


def test_cli_filter_command(tmp_path: Path):
    state = State(
        session_id="cli-test",
        phase=Phase.CURATE,
        intent=Intent(cuisine="Honduran", exclusions=["shellfish"]),
        candidates=[
            Candidate(
                name="chile cobanero", cuisine_origin="Honduran",
                functional_role="heat", intensity=7,
            ),
            Candidate(
                name="dried shrimp", cuisine_origin="Asian",
                functional_role="heat", intensity=5,
            ),
        ],
    )
    state_path = tmp_path / "state.yaml"
    state.dump_yaml(state_path)

    result = subprocess.run(
        [
            sys.executable, "-m", "mise_en_prompt.conflicts",
            "filter", "--role", "heat", "--state", str(state_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    output = json.loads(result.stdout)
    assert any(c["name"] == "chile cobanero" for c in output["compatible"])
    assert not any(c["name"] == "dried shrimp" for c in output["compatible"])


def test_cli_check_command(tmp_path: Path):
    state = State(
        session_id="cli-test",
        phase=Phase.CURATE,
        intent=Intent(cuisine="Honduran"),
    )
    state_path = tmp_path / "state.yaml"
    state.dump_yaml(state_path)

    candidate_json = json.dumps({
        "name": "miso",
        "cuisine_origin": "Japanese",
        "functional_role": "umami",
    })
    result = subprocess.run(
        [
            sys.executable, "-m", "mise_en_prompt.conflicts",
            "check", "--candidate", candidate_json, "--state", str(state_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    output = json.loads(result.stdout)
    rules = [f["rule"] for f in output["findings"]]
    assert PruneRule.CUISINE_DRIFT.value in rules
