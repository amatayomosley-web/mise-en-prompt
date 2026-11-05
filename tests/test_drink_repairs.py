"""Behavioral tests for the Step 0 drink repairs (design 00-step0-repairs.md section 0.5).

Each new rule has a test that fails when the rule is removed. Where the rule is a table or a
set, the test removes the row with monkeypatch and asserts the finding disappears, so the
test proves the row is load-bearing rather than merely present. The prose-side pins (the
Negroni figures, headings, bands) are in test_drink_docs.py.
"""
from __future__ import annotations

from typing import get_args

import pytest

from mise_en_prompt import conflicts
from mise_en_prompt.conflicts import (
    BUILD_IMPOSSIBILITY_RULES,
    DRINK_FAMILIES,
    DRINK_PRODUCT_CLASSES,
    DRINK_STACKABLE_ROLES,
    Severity,
    Verdict,
    _find_drink_family,
    _find_product_class,
    check_build_impossibility,
    check_candidate,
    check_drink_redundancy,
    check_family_drift,
    classify_candidate,
    drink_role_warning,
    filter_candidates_for_role,
    normalize_drink_role,
)
from mise_en_prompt.state import (
    DRINK_FAMILY_ALIASES,
    DRINK_ROLE_ALIASES,
    BuildMethod,
    Candidate,
    DrinkFamily,
    DrinkIntent,
    DrinkPruneRule,
    DrinkRole,
    Intent,
    Phase,
    State,
)


def _drink_state(
    intent: DrinkIntent | None = None,
    candidates: list[Candidate] | None = None,
    selected: list[str] | None = None,
) -> State:
    return State(
        session_id="d",
        phase=Phase.CURATE,
        intent=Intent(medium="drink", drink=intent if intent is not None else DrinkIntent()),
        candidates=candidates or [],
        selected=selected or [],
    )


def _dish_state(candidates: list[Candidate] | None = None) -> State:
    return State(session_id="t", phase=Phase.CURATE, intent=Intent(), candidates=candidates or [])


def _comp(
    name: str, role: str, intensity: int | None = None, origin: str = "", contains: tuple = (),
) -> Candidate:
    return Candidate(
        name=name, cuisine_origin=origin, functional_role=role, intensity=intensity,
        contains=list(contains),
    )


# Row b: the eight role names ---------------------------------------------------


@pytest.mark.parametrize(
    ("legacy", "canonical"),
    [
        ("sweet", "sweetener"),
        ("bitter", "bitters"),
        ("aromatic", "aromatic_garnish"),
        ("aromatics", "aromatic_garnish"),
        ("aromatic garnish", "aromatic_garnish"),
        ("dilution", "lengthener"),
        ("bases", "base"),
        ("modifiers", "modifier"),
        ("Sweet", "sweetener"),
    ],
)
def test_legacy_role_names_are_accepted_as_aliases(legacy: str, canonical: str):
    assert normalize_drink_role(legacy) == canonical


@pytest.mark.parametrize("role", get_args(DrinkRole))
def test_the_eight_canonical_roles_map_to_themselves(role: str):
    assert normalize_drink_role(role) == role


def test_there_are_eight_roles_and_every_alias_lands_on_one():
    assert len(get_args(DrinkRole)) == 8
    assert set(DRINK_ROLE_ALIASES.values()) <= set(get_args(DrinkRole))
    assert DRINK_STACKABLE_ROLES <= set(get_args(DrinkRole))
    assert "dilution" not in get_args(DrinkRole)


def test_an_unknown_role_passes_through_lowercased():
    assert normalize_drink_role("Garnish Foam") == "garnish foam"


def test_legacy_and_canonical_spellings_share_one_slot():
    """A session that wrote `bitter` and one that wrote `bitters` are the same role."""
    angostura = _comp("Angostura bitters", "bitter", 6)
    aromatic = _comp("aromatic bitters", "bitters", 5)
    state = _drink_state(candidates=[angostura, aromatic], selected=["Angostura bitters"])
    finding = check_drink_redundancy(aromatic, state)
    assert finding is not None and "aromatic bitters" in finding.reason


def test_legacy_sweet_and_canonical_sweetener_collide_on_intensity():
    simple = _comp("simple syrup", "sweet", 4)
    agave = _comp("agave nectar", "sweetener", 5)
    state = _drink_state(candidates=[simple, agave], selected=["simple syrup"])
    assert check_drink_redundancy(agave, state) is not None


@pytest.mark.parametrize("role", ["aromatic_garnish", "aromatic"])
def test_aromatic_garnish_stacks_under_either_spelling(role: str):
    peel = _comp("orange peel", role, 5)
    sprig = _comp("mint sprig", role, 5)
    state = _drink_state(candidates=[peel, sprig], selected=["orange peel"])
    assert check_drink_redundancy(sprig, state) is None


def test_filter_finds_a_legacy_role_under_its_canonical_name_and_back():
    bitters = _comp("Angostura bitters", "bitter", 6)
    state = _drink_state(candidates=[bitters])
    assert filter_candidates_for_role("bitters", state).compatible == [bitters]
    assert filter_candidates_for_role("bitter", state).compatible == [bitters]


def test_dilution_role_is_read_as_lengthener_with_a_warning():
    soda = _comp("soda water", "dilution", 2)
    state = _drink_state(candidates=[soda])
    result = filter_candidates_for_role("lengthener", state)
    assert result.compatible == [soda]
    assert len(result.warnings) == 1 and "computed quantity" in result.warnings[0]
    assert drink_role_warning("dilution") is not None
    assert drink_role_warning("lengthener") is None
    assert filter_candidates_for_role("sweetener", _drink_state(candidates=[soda])).warnings == []


def test_dish_sessions_keep_exact_role_matching():
    """The alias map is a drink map: a dish `sweet` is not a `sweetener`."""
    sugar = _comp("palm sugar", "sweet", 4)
    state = _dish_state([sugar])
    assert filter_candidates_for_role("sweetener", state).compatible == []
    assert filter_candidates_for_role("sweet", state).compatible == [sugar]
    assert filter_candidates_for_role("dilution", state).warnings == []


# Row c: acid stacks by product class -------------------------------------------


def test_lemon_and_lime_split_citrus_passes_at_equal_intensity():
    lemon = _comp("lemon juice", "acid", 6)
    lime = _comp("lime juice", "acid", 6)
    state = _drink_state(candidates=[lemon, lime], selected=["lemon juice"])
    assert check_drink_redundancy(lime, state) is None


def test_two_lemon_juices_are_one_product_twice_even_far_apart_in_intensity():
    fresh = _comp("fresh lemon juice", "acid", 9)
    bottled = _comp("lemon juice", "acid", 2)
    state = _drink_state(candidates=[fresh, bottled], selected=["fresh lemon juice"])
    finding = check_drink_redundancy(bottled, state)
    assert finding is not None
    assert finding.rule == DrinkPruneRule.DRINK_FUNCTIONAL_REDUNDANCY
    assert "lemon juice" in finding.reason


def test_lime_and_grapefruit_are_different_classes():
    lime = _comp("lime juice", "acid", 6)
    grapefruit = _comp("grapefruit juice", "acid", 6)
    state = _drink_state(candidates=[lime, grapefruit], selected=["lime juice"])
    assert check_drink_redundancy(grapefruit, state) is None


def test_two_acid_blends_share_a_class():
    one = _comp("acid blend", "acid", 5)
    two = _comp("super juice", "acid", 5)
    state = _drink_state(candidates=[one, two], selected=["acid blend"])
    assert check_drink_redundancy(two, state) is not None


def test_isolated_acids_are_unclassed_so_a_citric_malic_pair_passes():
    citric = _comp("citric acid solution", "acid", 5)
    malic = _comp("malic acid", "acid", 5)
    assert _find_product_class("malic acid") is None
    state = _drink_state(candidates=[citric, malic], selected=["citric acid solution"])
    assert check_drink_redundancy(malic, state) is None


@pytest.mark.parametrize(
    ("name", "product_class"),
    [
        ("fresh lime juice", "lime juice"),
        ("Meyer lemon juice", "lemon juice"),
        ("pink grapefruit juice", "grapefruit juice"),
        ("acid-adjusted orange juice", "acid solution"),
    ],
)
def test_citrus_product_classes_are_declared(name: str, product_class: str):
    assert _find_product_class(name) == product_class


def test_removing_acid_from_the_stackable_set_brings_the_old_prune_back(monkeypatch):
    """Load-bearing: without `acid` stackable, lemon plus lime at equal intensity is pruned."""
    lemon = _comp("lemon juice", "acid", 6)
    lime = _comp("lime juice", "acid", 6)
    state = _drink_state(candidates=[lemon, lime], selected=["lemon juice"])
    assert check_drink_redundancy(lime, state) is None
    monkeypatch.setattr(conflicts, "DRINK_STACKABLE_ROLES", DRINK_STACKABLE_ROLES - {"acid"})
    assert check_drink_redundancy(lime, state) is not None


def test_removing_the_lemon_class_lets_two_lemon_juices_through(monkeypatch):
    """Load-bearing: the class entry is what catches the duplicate in a stackable role."""
    fresh = _comp("fresh lemon juice", "acid", 9)
    bottled = _comp("lemon juice", "acid", 2)
    state = _drink_state(candidates=[fresh, bottled], selected=["fresh lemon juice"])
    assert check_drink_redundancy(bottled, state) is not None
    classes = {k: v for k, v in DRINK_PRODUCT_CLASSES.items() if k != "lemon juice"}
    monkeypatch.setattr(conflicts, "DRINK_PRODUCT_CLASSES", classes)
    assert check_drink_redundancy(bottled, state) is None


def test_split_citrus_survives_the_whole_filter():
    lemon = _comp("lemon juice", "acid", 6)
    lime = _comp("lime juice", "acid", 6)
    state = _drink_state(candidates=[lemon, lime], selected=["lemon juice"])
    result = filter_candidates_for_role("acid", state)
    assert result.would_prune == []
    assert result.compatible == [lemon, lime]


# Rows e and f: eight families --------------------------------------------------


def test_drink_families_are_exactly_the_eight_in_the_schema():
    assert len(DRINK_FAMILIES) == 8
    assert set(DRINK_FAMILIES) == set(get_args(DrinkFamily))


def test_family_aliases_land_on_real_families():
    for targets in DRINK_FAMILY_ALIASES.values():
        assert set(targets) <= set(get_args(DrinkFamily))


@pytest.mark.parametrize("family", get_args(DrinkFamily))
def test_every_family_name_resolves_to_itself(family: str):
    assert _find_drink_family(family) == family
    assert _find_drink_family(family.upper()) == family


@pytest.mark.parametrize(
    ("drink", "family"),
    [
        ("Americano", "Aperitivo & amaro"),
        ("Aperol Spritz", "Aperitivo & amaro"),
        ("Sherry Cobbler", "Sparkling & wine"),
        ("Adonis", "Sparkling & wine"),
        ("Fish House Punch", "Punch"),
        ("Golden Fizz", "Flip & fizz"),
        ("Gin and Tonic", "Highball"),
    ],
)
def test_pillar_placement_of_the_contested_drinks(drink: str, family: str):
    assert _find_drink_family(drink) == family


def test_bare_punch_is_not_a_member_but_the_family_name_resolves():
    members = {m for ms in DRINK_FAMILIES.values() for m in ms}
    assert "punch" not in members
    assert _find_drink_family("punch") == "Punch"
    assert _find_drink_family("rum punch") == "Tiki"


def test_legacy_family_names_still_resolve():
    assert _find_drink_family("Champagne & wine") == "Sparkling & wine"
    assert _find_drink_family("Flip & punch") == "Flip & fizz"


def _drift(target: str, origin: str) -> object:
    state = _drink_state(DrinkIntent(drink_family=target))
    return check_family_drift(_comp("x", "modifier", 5, origin=origin), state)


def test_a_legacy_flip_and_punch_session_does_not_start_drifting_across_the_split():
    """`Flip & punch` became two groups; either half is still on-family for a legacy session."""
    assert _drift("Flip & punch", "milk punch") is None
    assert _drift("Flip & punch", "golden fizz") is None
    assert _drift("Flip & punch", "Sour") is not None
    assert _drift("milk punch", "Flip & punch") is None


def test_the_renamed_sparkling_family_is_one_family_under_both_names():
    assert _drift("Sparkling & wine", "Champagne & wine") is None
    assert _drift("Champagne & wine", "french 75") is None
    assert _drift("Champagne & wine", "Sour") is not None


def test_new_flip_and_punch_halves_are_separate_families():
    finding = _drift("Flip & fizz", "milk punch")
    assert finding is not None and finding.rule == DrinkPruneRule.FAMILY_DRIFT


def test_americano_is_aperitivo_not_highball():
    assert _drift("Aperitivo & amaro", "americano") is None
    assert _drift("Highball", "americano") is not None


# Row p: build_impossibility ----------------------------------------------------


def _build_state(method: BuildMethod | None, *peers: Candidate) -> State:
    return _drink_state(
        DrinkIntent(build_method=method),
        candidates=list(peers),
        selected=[p.name for p in peers],
    )


# (rule key, role, contains, build method, peers' contains, phrase the finding must carry)
BUILD_CASES = [
    ("foam_needs_shake", "texture", ("egg_raw",), "stirred", (), "dry_shaken or shaken"),
    ("foam_needs_shake", "texture", ("aquafaba",), "built", (), "dry_shaken or shaken"),
    ("foam_needs_shake", "texture", ("dairy", "foam"), "thrown", (), "dry_shaken or shaken"),
    ("citrus_stirred", "acid", ("citrus_juice",), "stirred", (), "shaking or throwing"),
    ("citrus_stirred", "modifier", ("puree",), "stirred", (), "shaking or throwing"),
    ("citrus_carbonated", "acid", ("citrus_juice",), "carbonated", (), "clarify first"),
    ("citrus_carbonated", "modifier", ("pulp",), "carbonated", (), "clarify first"),
    ("carbonation_agitated", "lengthener", ("carbonation",), "shaken", (), "never agitated"),
    ("carbonation_agitated", "lengthener", ("carbonation",), "blended", (), "never agitated"),
    ("carbonation_heated", "lengthener", ("carbonation",), "heated", (), "goes flat"),
    ("egg_heated", "texture", ("egg_raw",), "heated", (), "tempered"),
    ("dairy_with_citrus", "texture", ("dairy",), "shaken", ("citrus_juice",), "choose one"),
    ("dairy_with_citrus", "acid", ("citrus_juice",), "shaken", ("dairy",), "choose one"),
    ("dairy_with_citrus", "texture", ("dairy", "citrus_juice"), "shaken", (), "choose one"),
    ("cream_liqueur_carbonated", "modifier", ("cream_liqueur",), "carbonated", (), "foams"),
    ("low_proof_base_shaken", "base", ("beer",), "shaken", (), "5-10%"),
    ("low_proof_base_shaken", "base", ("cider",), "shaken", (), "5-10%"),
]


def test_the_rule_table_has_one_row_per_design_rule():
    keys = [rule.key for rule in BUILD_IMPOSSIBILITY_RULES]
    assert len(keys) == len(set(keys)) == 9
    assert {case[0] for case in BUILD_CASES} == set(keys)


@pytest.mark.parametrize(("key", "role", "contains", "method", "peer_tags", "phrase"), BUILD_CASES)
def test_each_build_rule_fires_a_soft_finding(key, role, contains, method, peer_tags, phrase):
    peers = [_comp("peer", "modifier", contains=peer_tags)] if peer_tags else []
    candidate = _comp("subject", role, contains=contains)
    state = _build_state(method, *peers)
    finding = check_build_impossibility(candidate, state)
    assert finding is not None
    assert finding.severity == Severity.SOFT
    assert finding.rule == DrinkPruneRule.BUILD_IMPOSSIBILITY
    assert phrase in finding.reason
    assert method in finding.reason


@pytest.mark.parametrize(("key", "role", "contains", "method", "peer_tags", "phrase"), BUILD_CASES)
def test_each_build_rule_is_load_bearing(
    monkeypatch, key, role, contains, method, peer_tags, phrase,
):
    """Remove the one table row and exactly its finding disappears."""
    peers = [_comp("peer", "modifier", contains=peer_tags)] if peer_tags else []
    candidate = _comp("subject", role, contains=contains)
    state = _build_state(method, *peers)
    assert check_build_impossibility(candidate, state) is not None
    without = tuple(r for r in BUILD_IMPOSSIBILITY_RULES if r.key != key)
    monkeypatch.setattr(conflicts, "BUILD_IMPOSSIBILITY_RULES", without)
    assert check_build_impossibility(candidate, state) is None


@pytest.mark.parametrize(
    ("role", "contains", "method", "peer_tags"),
    [
        ("texture", ("egg_raw",), "dry_shaken", ()),
        ("texture", ("egg_raw",), "shaken", ()),
        ("texture", ("dairy",), "stirred", ()),  # cream stirred in for body, no foam wanted
        ("acid", ("citrus_juice",), "shaken", ()),
        ("acid", ("citrus_juice",), "thrown", ()),
        ("lengthener", ("carbonation",), "built", ()),
        ("lengthener", ("carbonation",), "carbonated", ()),
        ("texture", ("egg_raw",), None, ()),  # no build method chosen yet
        ("texture", ("dairy",), "clarified", ("citrus_juice",)),  # milk punch: clarified away
        ("modifier", ("beer",), "shaken", ()),  # low-proof but not in the base slot
        ("base", ("beer",), "built", ()),
        ("modifier", ("cream_liqueur",), "shaken", ()),
    ],
)
def test_build_rules_stay_quiet_on_workable_builds(role, contains, method, peer_tags):
    peers = [_comp("peer", "modifier", contains=peer_tags)] if peer_tags else []
    candidate = _comp("subject", role, contains=contains)
    finding = check_build_impossibility(candidate, _build_state(method, *peers))
    assert finding is None


def test_first_matching_row_wins():
    both = _comp("odd", "texture", contains=("egg_raw", "citrus_juice"))
    finding = check_build_impossibility(both, _build_state("stirred"))
    assert finding is not None and "dry_shaken or shaken" in finding.reason
    assert "shaking or throwing" not in finding.reason


def test_a_candidate_without_tags_is_never_flagged():
    assert check_build_impossibility(_comp("rye", "base"), _build_state("stirred")) is None


def test_a_session_with_no_drink_block_is_not_flagged():
    state = _drink_state(None)
    assert check_build_impossibility(_comp("egg", "texture", contains=("egg_raw",)), state) is None


def test_a_raw_egg_in_a_stirred_build_lands_in_would_prune_and_overridable():
    egg = _comp("egg white", "texture", contains=("egg_raw",))
    state = _build_state("stirred", egg)
    state.selected = []
    verdict, findings = classify_candidate(egg, state)
    assert verdict == Verdict.WOULD_PRUNE
    assert [f.rule for f in findings] == [DrinkPruneRule.BUILD_IMPOSSIBILITY]
    result = filter_candidates_for_role("texture", state)
    assert result.compatible == []
    assert [p.rule for p in result.would_prune] == [DrinkPruneRule.BUILD_IMPOSSIBILITY]
    assert check_candidate(egg, _build_state("dry_shaken", egg)) == []


def test_a_dish_session_never_runs_the_build_rules():
    egg = _comp("egg white", "texture", contains=("egg_raw",))
    assert check_candidate(egg, _dish_state([egg])) == []


def test_heated_is_a_build_method_and_legacy_candidates_load_without_contains():
    assert "heated" in get_args(BuildMethod)
    assert DrinkIntent(build_method="heated").build_method == "heated"
    legacy = Candidate(name="rye", cuisine_origin="", functional_role="base")
    assert legacy.contains == []


def test_a_misspelled_component_tag_is_rejected_rather_than_silently_ignored():
    with pytest.raises(ValueError, match="contains"):
        Candidate(name="x", cuisine_origin="", functional_role="base", contains=["egg-raw"])
