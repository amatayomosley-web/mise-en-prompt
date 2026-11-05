"""Tests for the conflict detection rules."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from mise_en_prompt.conflicts import (
    CUISINE_ADJACENCY,
    CUISINE_GROUPS,
    Severity,
    Verdict,
    _find_cuisine_group,
    check_allergy,
    check_candidate,
    check_cuisine_drift,
    check_functional_redundancy,
    check_technique_impossibility,
    classify_candidate,
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


def test_functional_redundancy_ignores_the_selected_candidate_itself():
    """Re-filtering a role after a pick must not flag the pick as redundant with itself."""
    candidates, selected = _seeded_chile_at_7()
    state = _state_with(Intent(), candidates=candidates, selected=selected)
    assert check_functional_redundancy(candidates[0], state) is None


# check_allergy false friends ---------------------------------------------------


def test_allergy_false_friends_are_not_blocked():
    cases = [
        ("eggs", "eggplant"),
        ("pork", "collard greens"),
        ("pork", "champagne vinegar"),
        ("dairy", "butternut squash"),
        ("dairy", "coconut milk"),
        ("dairy", "peanut butter"),
        ("dairy", "cream of tartar"),
        ("gluten", "buckwheat"),
    ]
    for exclusion, name in cases:
        state = _state_with(Intent(exclusions=[exclusion]))
        candidate = Candidate(name=name, cuisine_origin="generic", functional_role="x")
        assert check_allergy(candidate, state) is None, (exclusion, name)


def test_allergy_false_friend_does_not_hide_a_real_allergen():
    cases = [
        ("dairy", "buttermilk"),
        ("nuts", "almond butter"),
        ("dairy", "eggplant parmesan with butter"),
        ("eggs", "eggplant with egg wash"),
    ]
    for exclusion, name in cases:
        state = _state_with(Intent(exclusions=[exclusion]))
        candidate = Candidate(name=name, cuisine_origin="generic", functional_role="x")
        assert check_allergy(candidate, state) is not None, (exclusion, name)


# cuisine group lookup --------------------------------------------------------


def test_cuisine_group_american_is_north_american():
    assert _find_cuisine_group("American") == "North American"
    assert _find_cuisine_group("Central American") == "Latin American"
    assert _find_cuisine_group("Asian") == "East Asian"


def test_cuisine_drift_american_target_flags_mexican_not_cajun():
    state = _state_with(Intent(cuisine="American"))
    mexican = Candidate(name="chipotle", cuisine_origin="Mexican", functional_role="heat")
    cajun = Candidate(name="andouille", cuisine_origin="Cajun", functional_role="umami")
    assert check_cuisine_drift(mexican, state) is not None
    assert check_cuisine_drift(cajun, state) is None


# check_technique_impossibility ------------------------------------------------


def test_technique_impossibility_prep_over_budget_fires():
    state = _state_with(Intent(time_budget_min=30))
    candidate = Candidate(
        name="dried beans", cuisine_origin="generic", functional_role="protein",
        prep_time_min=480,
    )
    finding = check_technique_impossibility(candidate, state)
    assert finding is not None
    assert finding.severity == Severity.SOFT
    assert finding.rule == PruneRule.TECHNIQUE_IMPOSSIBILITY
    assert "480" in finding.reason and "30" in finding.reason


def test_technique_impossibility_prep_within_budget_no_conflict():
    state = _state_with(Intent(time_budget_min=180))
    candidate = Candidate(
        name="dried beans", cuisine_origin="generic", functional_role="protein",
        prep_time_min=120,
    )
    assert check_technique_impossibility(candidate, state) is None


def test_technique_impossibility_unknown_prep_or_budget_no_conflict():
    """Without both numbers there is nothing to compare; the agent reasons in chat."""
    no_prep = Candidate(
        name="dried beans", cuisine_origin="generic", functional_role="protein",
    )
    assert check_technique_impossibility(
        no_prep, _state_with(Intent(time_budget_min=30)),
    ) is None
    with_prep = Candidate(
        name="dried beans", cuisine_origin="generic", functional_role="protein",
        prep_time_min=480,
    )
    assert check_technique_impossibility(with_prep, _state_with(Intent())) is None


# check_candidate aggregator ---------------------------------------------------


def test_check_candidate_aggregates_multiple_soft_findings():
    """A candidate tripping two soft rules returns both findings."""
    state = _state_with(Intent(cuisine="Honduran", time_budget_min=30))
    candidate = Candidate(
        name="miso", cuisine_origin="Japanese", functional_role="umami",
        prep_time_min=60,
    )
    rules = {f.rule for f in check_candidate(candidate, state)}
    assert rules == {PruneRule.CUISINE_DRIFT, PruneRule.TECHNIQUE_IMPOSSIBILITY}


def test_check_candidate_hard_finding_suppresses_soft():
    """An allergy-blocked candidate reports only the hard rule, never a soft flag."""
    state = _state_with(Intent(cuisine="Honduran", exclusions=["shellfish"]))
    candidate = Candidate(
        name="dried shrimp", cuisine_origin="Japanese", functional_role="umami",
    )
    findings = check_candidate(candidate, state)
    assert [f.rule for f in findings] == [PruneRule.ALLERGY_HARD_FILTER]


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
    result = filter_candidates_for_role("heat", state)
    names = [c.name for c in result.compatible]
    assert "chile cobanero" in names
    assert "dried shrimp paste" not in names
    assert "dried shrimp paste" not in [p.name for p in result.would_prune]
    assert [p.name for p in result.excluded] == ["dried shrimp paste"]
    assert result.excluded[0].rule == PruneRule.ALLERGY_HARD_FILTER


def _heat_pool() -> list[Candidate]:
    return [
        Candidate(
            name="chile cobanero", cuisine_origin="Honduran",
            functional_role="heat", intensity=7,
        ),
        Candidate(
            name="szechuan peppercorn", cuisine_origin="Chinese",
            functional_role="heat", intensity=4,
        ),
    ]


def test_filter_role_tradition_soft_drift_only_in_would_prune():
    """Tradition: a drifting candidate leaves the offered pool; the user can override."""
    state = _state_with(
        Intent(cuisine="Honduran", cuisine_stance="tradition"), candidates=_heat_pool(),
    )
    result = filter_candidates_for_role("heat", state)
    assert [c.name for c in result.compatible] == ["chile cobanero"]
    assert [p.name for p in result.would_prune] == ["szechuan peppercorn"]
    assert result.would_prune[0].rule == PruneRule.CUISINE_DRIFT
    assert result.excluded == []


def test_filter_role_unset_stance_gates_like_tradition():
    state = _state_with(Intent(cuisine="Honduran"), candidates=_heat_pool())
    result = filter_candidates_for_role("heat", state)
    assert [c.name for c in result.compatible] == ["chile cobanero"]
    assert [p.name for p in result.would_prune] == ["szechuan peppercorn"]


def test_filter_role_explore_drift_is_informational():
    """Explore: drift doesn't gate; the candidate is offered with a note."""
    state = _state_with(
        Intent(cuisine="Honduran", cuisine_stance="explore"), candidates=_heat_pool(),
    )
    result = filter_candidates_for_role("heat", state)
    assert [c.name for c in result.compatible] == ["chile cobanero", "szechuan peppercorn"]
    assert result.would_prune == []
    assert [(n.name, n.rule) for n in result.notes] == [
        ("szechuan peppercorn", PruneRule.CUISINE_DRIFT),
    ]


def test_explore_still_prunes_allergy_redundancy_and_technique():
    pool = [
        Candidate(name="chile cobanero", cuisine_origin="Honduran",
                  functional_role="heat", intensity=7),
        Candidate(name="chile chiltepe", cuisine_origin="Salvadoran",
                  functional_role="heat", intensity=8),
        Candidate(name="shrimp chili crisp", cuisine_origin="Chinese",
                  functional_role="heat", intensity=2),
        Candidate(name="fermented chile mash", cuisine_origin="Korean",
                  functional_role="heat", intensity=1, prep_time_min=4320),
    ]
    state = _state_with(
        Intent(cuisine="Honduran", cuisine_stance="explore",
               exclusions=["shellfish"], time_budget_min=180),
        candidates=pool, selected=["chile cobanero"],
    )
    result = filter_candidates_for_role("heat", state)
    assert [c.name for c in result.compatible] == ["chile cobanero"]
    assert {(p.name, p.rule) for p in result.would_prune} == {
        ("chile chiltepe", PruneRule.FUNCTIONAL_REDUNDANCY),
        ("fermented chile mash", PruneRule.TECHNIQUE_IMPOSSIBILITY),
    }
    assert [(p.name, p.rule) for p in result.excluded] == [
        ("shrimp chili crisp", PruneRule.ALLERGY_HARD_FILTER),
    ]


def test_sample_session_every_candidate_lands_in_exactly_one_bucket():
    sample = Path(__file__).parent.parent / "sessions" / "2026-04-28-pinto-beans-sample"
    base = State.load_yaml(sample / "state.yaml")
    for stance in (None, "tradition", "explore"):
        state = base.model_copy(
            update={"intent": base.intent.model_copy(update={"cuisine_stance": stance})},
        )
        for role in {c.functional_role for c in state.candidates}:
            result = filter_candidates_for_role(role, state)
            compatible = [c.name for c in result.compatible]
            would_prune = [p.name for p in result.would_prune]
            excluded = [p.name for p in result.excluded]
            buckets = compatible + sorted(set(would_prune)) + sorted(set(excluded))
            expected = [c.name for c in state.candidates if c.functional_role == role]
            assert sorted(buckets) == sorted(expected), (stance, role, buckets)
        umami = filter_candidates_for_role("umami", state)
        assert [p.name for p in umami.excluded] == ["dried shrimp"]
        assert "dried shrimp" not in [p.name for p in umami.would_prune]
        miso_offered = "miso" in [c.name for c in umami.compatible]
        assert miso_offered == (stance == "explore")


def test_classify_candidate_verdicts():
    state = _state_with(Intent(cuisine="Honduran", exclusions=["shellfish"]))
    shrimp = Candidate(name="dried shrimp", cuisine_origin="Asian", functional_role="umami")
    miso = Candidate(name="miso", cuisine_origin="Japanese", functional_role="umami")
    lime = Candidate(name="lime", cuisine_origin="Mexican", functional_role="acid")
    assert classify_candidate(shrimp, state)[0] == Verdict.EXCLUDED
    assert classify_candidate(miso, state)[0] == Verdict.WOULD_PRUNE
    assert classify_candidate(lime, state) == (Verdict.COMPATIBLE, [])


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
    names = [c.name for c in filter_candidates_for_role("heat", state).compatible]
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
    assert not any(p["name"] == "dried shrimp" for p in output["would_prune"])
    assert [p["name"] for p in output["excluded"]] == ["dried shrimp"]
    assert output["cuisine_stance"] is None


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
    assert output["verdict"] == Verdict.WOULD_PRUNE.value


# _find_cuisine_group ----------------------------------------------------------


def test_american_resolves_to_north_american():
    """Regression: "American" used to resolve to Latin American.

    ``_find_cuisine_group`` matched bidirectionally, so "american" hit the longer
    member "central american" and dict iteration reached Latin American first. The
    failure was silent — for a dish with cuisine "American", a Mexican candidate
    produced no cuisine_drift finding because both sides resolved to the same group.
    """
    assert _find_cuisine_group("American") == "North American"


def test_american_dish_flags_mexican_candidate_as_drift():
    """The user-visible consequence of the bug above: drift must actually fire.

    Before the fix this returned None, because "American" resolved to Latin American
    and so did "Mexican". It now fires at INFO — North American and Latin American are
    adjacent, so the crossing is real but unremarkable.
    """
    state = _state_with(Intent(cuisine="American"))
    candidate = Candidate(name="guajillo", cuisine_origin="Mexican", functional_role="heat")
    finding = check_cuisine_drift(candidate, state)
    assert finding is not None
    assert finding.rule == PruneRule.CUISINE_DRIFT
    assert finding.severity == Severity.INFO


def test_every_group_member_resolves_to_its_own_group():
    """No member may be captured by a different group's substring."""
    for group, members in CUISINE_GROUPS.items():
        for member in members:
            assert _find_cuisine_group(member) == group, (
                f"{member!r} resolved to {_find_cuisine_group(member)!r}, expected {group!r}"
            )


def test_group_names_resolve_to_themselves():
    for group in CUISINE_GROUPS:
        assert _find_cuisine_group(group) == group


def test_longest_member_wins_inside_a_longer_query():
    """"Central American Stew" contains both "central american" and "american"."""
    assert _find_cuisine_group("Central American Stew") == "Latin American"
    assert _find_cuisine_group("Honduran sofrito") == "Latin American"


def test_query_shorter_than_a_member_still_resolves():
    """Fix-prune's third step survives the merge: "Asian" must reach East Asian via "east asian"."""
    assert _find_cuisine_group("Asian") is not None
    assert _find_cuisine_group("Mex") == "Latin American"


def test_unknown_cuisine_resolves_to_none():
    assert _find_cuisine_group("Klingon") is None
    assert _find_cuisine_group("") is None


# cuisine_stance == explore ----------------------------------------------------


def test_cuisine_drift_downgrades_to_info_when_exploring():
    """chef.md Principle 8: under `explore`, drift is informational, not gating."""
    state = _state_with(Intent(cuisine="Tex-Mex", cuisine_stance="explore"))
    candidate = Candidate(
        name="fish sauce", cuisine_origin="Vietnamese",
        functional_role="umami_glutamate",
    )
    finding = check_cuisine_drift(candidate, state)
    assert finding is not None
    assert finding.severity == Severity.INFO
    assert "explore" in finding.reason


def test_cuisine_drift_stays_soft_under_tradition():
    state = _state_with(Intent(cuisine="Tex-Mex", cuisine_stance="tradition"))
    candidate = Candidate(
        name="fish sauce", cuisine_origin="Vietnamese",
        functional_role="umami_glutamate",
    )
    finding = check_cuisine_drift(candidate, state)
    assert finding is not None
    assert finding.severity == Severity.SOFT


def test_cuisine_drift_stays_soft_when_stance_unset():
    state = _state_with(Intent(cuisine="Tex-Mex"))
    candidate = Candidate(
        name="fish sauce", cuisine_origin="Vietnamese",
        functional_role="umami_glutamate",
    )
    finding = check_cuisine_drift(candidate, state)
    assert finding is not None
    assert finding.severity == Severity.SOFT


def test_filter_reports_info_findings_as_notes():
    """INFO findings land in notes and keep the candidate compatible."""
    candidate = Candidate(
        name="dried porcini", cuisine_origin="Italian",
        functional_role="umami_guanylate", intensity=6,
    )
    state = _state_with(
        Intent(cuisine="Tex-Mex", cuisine_stance="explore"), candidates=[candidate],
    )
    result = filter_candidates_for_role("umami_guanylate", state)
    assert [c.name for c in result.compatible] == ["dried porcini"]
    assert result.would_prune == []
    assert len(result.notes) == 1
    assert result.notes[0].rule == PruneRule.CUISINE_DRIFT


# umami compound-class convention ----------------------------------------------


def test_umami_classes_do_not_collide_across_compound_classes():
    """The synergy the ingredients pillar calls for must survive the redundancy rule.

    Glutamate x guanylate is the several-fold multiplicative pairing. Modeled as a single
    `umami` role these would collide on intensity and the rule would prune exactly
    the stack the science recommends.
    """
    glutamate = Candidate(
        name="fish sauce", cuisine_origin="Vietnamese",
        functional_role="umami_glutamate", intensity=8,
    )
    guanylate = Candidate(
        name="dried shiitake", cuisine_origin="Japanese",
        functional_role="umami_guanylate", intensity=9,
    )
    state = _state_with(
        Intent(cuisine="Tex-Mex"),
        candidates=[glutamate, guanylate],
        selected=["fish sauce"],
    )
    assert check_functional_redundancy(guanylate, state) is None


def test_umami_same_compound_class_still_flags_redundancy():
    """Two glutamate sources at close intensity are genuinely redundant.

    Glutamate x glutamate is additive, not synergistic — unlike the cross-class case.
    """
    fish_sauce = Candidate(
        name="fish sauce", cuisine_origin="Vietnamese",
        functional_role="umami_glutamate", intensity=8,
    )
    msg = Candidate(
        name="MSG", cuisine_origin="Japanese",
        functional_role="umami_glutamate", intensity=7,
    )
    state = _state_with(
        Intent(cuisine="Tex-Mex"),
        candidates=[fish_sauce, msg],
        selected=["fish sauce"],
    )
    finding = check_functional_redundancy(msg, state)
    assert finding is not None
    assert finding.rule == PruneRule.FUNCTIONAL_REDUNDANCY


# cuisine adjacency ------------------------------------------------------------


def test_adjacency_is_symmetric():
    for group, neighbours in CUISINE_ADJACENCY.items():
        for neighbour in neighbours:
            assert group in CUISINE_ADJACENCY[neighbour], (
                f"{group!r} lists {neighbour!r} but not the reverse"
            )


def test_adjacency_covers_every_group_key():
    assert set(CUISINE_ADJACENCY) == set(CUISINE_GROUPS)


def test_no_group_is_adjacent_to_itself():
    for group, neighbours in CUISINE_ADJACENCY.items():
        assert group not in neighbours


def test_adjacency_stays_sparse():
    """If everything is adjacent to everything, the finding carries no signal."""
    total = sum(len(n) for n in CUISINE_ADJACENCY.values())
    complete = len(CUISINE_GROUPS) * (len(CUISINE_GROUPS) - 1)
    assert total < complete / 2, "adjacency map has grown too dense to be meaningful"


def test_adjacent_crossing_reports_info_even_under_tradition():
    """Bacon in a Tex-Mex pot is a note, not a decision to adjudicate."""
    state = _state_with(Intent(cuisine="Tex-Mex", cuisine_stance="tradition"))
    candidate = Candidate(name="bacon", cuisine_origin="American", functional_role="fat")
    finding = check_cuisine_drift(candidate, state)
    assert finding is not None
    assert finding.severity == Severity.INFO
    assert "adjacent" in finding.reason


def test_distant_crossing_still_reports_soft_under_tradition():
    """Fish sauce in a Tex-Mex pot is a real crossing; the user should decide."""
    state = _state_with(Intent(cuisine="Tex-Mex", cuisine_stance="tradition"))
    candidate = Candidate(
        name="fish sauce", cuisine_origin="Vietnamese", functional_role="umami_glutamate",
    )
    finding = check_cuisine_drift(candidate, state)
    assert finding is not None
    assert finding.severity == Severity.SOFT


def test_same_group_reports_nothing_regardless_of_adjacency():
    state = _state_with(Intent(cuisine="Tex-Mex", cuisine_stance="tradition"))
    candidate = Candidate(name="chipotle", cuisine_origin="Mexican", functional_role="heat")
    assert check_cuisine_drift(candidate, state) is None
