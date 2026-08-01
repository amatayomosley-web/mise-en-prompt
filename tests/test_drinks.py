"""Tests for the drink structures that sit alongside the food ones.

Every test here targets a mirror invariant: a drink structure behaves like its food
sibling where the shape is shared, and diverges only where the bar demands it. The
food-path assertions in this file are regression guards — they assert that adding the
drink siblings changed nothing about how a dish session behaves.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest

from mise_en_prompt.conflicts import (
    _ALL_DRINK_RULES,
    _ALL_RULES,
    Severity,
    _find_cuisine_group,
    _find_drink_family,
    _find_product_class,
    _rules_for,
    check_build_impossibility,
    check_candidate,
    check_drink_allergy,
    check_drink_redundancy,
    check_family_drift,
    check_functional_redundancy,
    filter_candidates_for_role,
)
from mise_en_prompt.hooks.state_validate import (
    DRINK_PRECURSORS,
    PRECURSORS,
    validate_research_log_order,
    validate_state_content,
)
from mise_en_prompt.state import (
    Candidate,
    DrinkIntent,
    DrinkPruneRule,
    DrinkResearchPlan,
    Intent,
    Phase,
    PrunedItem,
    PruneRule,
    ResearchLogEntry,
    ResearchPlan,
    State,
)


def _drink_state(
    intent: DrinkIntent | None = None,
    candidates: list[Candidate] | None = None,
    selected: list[str] | None = None,
    exclusions: list[str] | None = None,
) -> State:
    """A CURATE-phase drink session. Mirror of test_conflicts._state_with."""
    return State(
        session_id="d",
        phase=Phase.CURATE,
        intent=Intent(
            medium="drink",
            exclusions=exclusions or [],
            drink=intent if intent is not None else DrinkIntent(),
        ),
        candidates=candidates or [],
        selected=selected or [],
    )


def _dish_state(
    intent: Intent | None = None,
    candidates: list[Candidate] | None = None,
    selected: list[str] | None = None,
) -> State:
    return State(
        session_id="t",
        phase=Phase.CURATE,
        intent=intent or Intent(),
        candidates=candidates or [],
        selected=selected or [],
    )


def _component(name: str, role: str, intensity: int | None = None, origin: str = "") -> Candidate:
    return Candidate(
        name=name, cuisine_origin=origin, functional_role=role, intensity=intensity,
    )


# _find_drink_family -----------------------------------------------------------


@pytest.mark.parametrize(
    ("family", "group"),
    [
        ("Tiki", "Tiki"),
        ("Sour", "Sour"),
        ("Spirit-forward", "Spirit-forward"),
        ("Mai Tai", "Tiki"),
        ("Negroni", "Spirit-forward"),
        ("Daiquiri", "Sour"),
        ("Milk Punch", "Flip & punch"),
        ("Gin and Tonic", "Highball"),
    ],
)
def test_find_drink_family_resolves_real_families(family: str, group: str):
    """Drink families the food matcher could not see at all now resolve to a drink group."""
    assert _find_drink_family(family) == group


@pytest.mark.parametrize(
    ("family", "drink_group", "food_group"),
    [
        ("Italian aperitivo", "Aperitivo & amaro", "European"),
        ("Japanese highball", "Highball", "East Asian"),
        ("French 75", "Champagne & wine", "European"),
    ],
)
def test_drink_family_no_longer_picks_up_food_region_semantics(
    family: str, drink_group: str, food_group: str,
):
    """A family whose name embeds a country used to fall through to a FOOD region.

    _find_cuisine_group still resolves these strings to a cuisine group — it is untouched —
    but a drink session never calls it, and the drink matcher lands them on the drink group
    their template actually belongs to.
    """
    assert _find_cuisine_group(family) == food_group
    assert _find_drink_family(family) == drink_group
    assert _find_drink_family(family) != _find_cuisine_group(family)


@pytest.mark.parametrize("provenance", ["Caribbean rum", "Classic American", "Nordic akvavit"])
def test_spirit_provenance_is_not_a_drink_family(provenance: str):
    """Provenance strings resolve to no drink family — the same silent no-claim food gives.

    These are the strings that used to land in a food region by accident. In a drink session
    they belong in Candidate.notes, not cuisine_origin, and None is the correct answer.
    """
    assert _find_drink_family(provenance) is None


def test_find_drink_family_empty_returns_none():
    assert _find_drink_family("") is None


def test_every_declared_family_member_resolves_to_its_own_group():
    """No intra-set collisions: the bidirectional matcher never crosses group boundaries."""
    from mise_en_prompt.conflicts import DRINK_FAMILIES

    for group, members in DRINK_FAMILIES.items():
        for member in members:
            assert _find_drink_family(member) == group, f"{member!r} leaked out of {group!r}"


# check_family_drift -----------------------------------------------------------


def test_family_drift_same_group_no_conflict():
    state = _drink_state(DrinkIntent(drink_family="Mai Tai"))
    candidate = _component("velvet falernum", "sweet", origin="Zombie")
    assert check_family_drift(candidate, state) is None


def test_family_drift_different_group_fires():
    state = _drink_state(DrinkIntent(drink_family="Mai Tai"))
    candidate = _component("Campari", "bitter", origin="Negroni")
    finding = check_family_drift(candidate, state)
    assert finding is not None
    assert finding.severity == Severity.SOFT
    assert finding.rule == DrinkPruneRule.FAMILY_DRIFT


def test_family_drift_no_target_family_no_conflict():
    state = _drink_state(DrinkIntent())
    candidate = _component("Campari", "bitter", origin="Negroni")
    assert check_family_drift(candidate, state) is None


def test_family_drift_no_drink_intent_no_conflict():
    """A state with medium=drink but no DrinkIntent yet must not raise."""
    state = State(
        session_id="d", phase=Phase.CURATE, intent=Intent(medium="drink"),
    )
    candidate = _component("Campari", "bitter", origin="Negroni")
    assert check_family_drift(candidate, state) is None


def test_family_drift_silent_on_family_neutral_component():
    """Syrups, citrus and ice carry no family — the rule must not fire on a simple syrup."""
    state = _drink_state(DrinkIntent(drink_family="Mai Tai"))
    candidate = _component("rich simple syrup", "sweet", origin="")
    assert check_family_drift(candidate, state) is None


# check_drink_allergy — nut-bearing liqueurs -----------------------------------


@pytest.mark.parametrize(
    "name",
    ["orgeat", "velvet falernum", "amaretto", "Frangelico", "Nocino", "creme de noyaux"],
)
def test_nut_bearing_liqueurs_hard_filter_on_nut_exclusion(name: str):
    """The real nut paths behind a bar carry no nut word — they must still hard-filter."""
    state = _drink_state(exclusions=["nuts"])
    finding = check_drink_allergy(_component(name, "sweet"), state)
    assert finding is not None, f"{name!r} slipped through a nut exclusion"
    assert finding.severity == Severity.HARD
    assert finding.rule == DrinkPruneRule.DRINK_ALLERGY_HARD_FILTER
    assert "nuts" in finding.reason


@pytest.mark.parametrize("name", ["coconut cream", "nutmeg", "creme de cacao", "lime juice"])
def test_nut_false_friends_are_exempt(name: str):
    """Coconut is a drupe, nutmeg a seed, creme de cacao dairy-free and nut-free.

    Flagging these would be noise on a true negative, so the exempt tier wins outright.
    """
    state = _drink_state(exclusions=["nuts"])
    assert check_drink_allergy(_component(name, "sweet"), state) is None


# check_drink_allergy — gluten / distillation asymmetry ------------------------


@pytest.mark.parametrize("name", ["rye whiskey", "wheat vodka", "barley shochu", "Irish whiskey"])
def test_distilled_grain_spirits_are_soft_flagged_not_hard_deleted(name: str):
    """Distillation leaves the gluten protein in the wash, so this is not a beer-grade exposure.

    The finding is SOFT: the candidate is surfaced for the user to decide rather than
    silently removed, which is what a HARD rule would do to the entire whiskey category.
    """
    state = _drink_state(exclusions=["gluten"])
    finding = check_drink_allergy(_component(name, "base"), state)
    assert finding is not None
    assert finding.severity == Severity.SOFT
    assert finding.rule == DrinkPruneRule.DRINK_ALLERGY_SOFT_FLAG
    assert "never silently removed" in finding.reason


@pytest.mark.parametrize("name", ["stout", "pale ale", "hefeweizen", "lager"])
def test_undistilled_grain_products_still_hard_filter_on_gluten(name: str):
    """The asymmetry cuts one way only: a beer is a real gluten exposure."""
    state = _drink_state(exclusions=["gluten"])
    finding = check_drink_allergy(_component(name, "modifier"), state)
    assert finding is not None
    assert finding.severity == Severity.HARD
    assert finding.rule == DrinkPruneRule.DRINK_ALLERGY_HARD_FILTER


@pytest.mark.parametrize("name", ["tequila", "rhum agricole", "Cognac"])
def test_non_grain_spirits_are_clean_under_a_gluten_exclusion(name: str):
    state = _drink_state(exclusions=["gluten"])
    assert check_drink_allergy(_component(name, "base"), state) is None


@pytest.mark.parametrize("name", ["ginger beer", "Fever-Tree ginger beer", "ginger ale",
                                  "root beer"])
def test_gluten_false_friends_are_exempt(name: str):
    """Sodas that share a word with a brewed product carry none of its grain.

    Ginger beer is the load-bearing case: it is a highball staple (mule, Dark 'n' Stormy,
    Jungle Bird) and a HARD hit would delete it from the session without the user seeing it.
    """
    state = _drink_state(exclusions=["gluten"])
    assert check_drink_allergy(_component(name, "dilution"), state) is None


def test_ginger_beer_survives_the_curate_filter_under_a_gluten_exclusion():
    """The exemption has to hold end-to-end, not just in the rule."""
    pool = [_component("ginger beer", "dilution", 4), _component("stout", "dilution", 7)]
    state = _drink_state(exclusions=["gluten"], candidates=pool)
    compatible, would_prune = filter_candidates_for_role("dilution", state)
    assert [c.name for c in compatible] == ["ginger beer"]
    assert [p.name for p in would_prune] == ["stout"]


def test_soft_flagged_spirit_stays_visible_to_the_user():
    """End-to-end proof of the not-a-silent-delete claim, through the CURATE filter.

    A SOFT gluten flag lands in BOTH compatible (so the user can still pick it) and
    would_prune (so the agent surfaces the reason). A HARD nut hit lands only in would_prune.
    """
    pool = [
        _component("rye whiskey", "base", 8),
        _component("orgeat", "sweet", 3),
    ]
    state = _drink_state(exclusions=["gluten", "nuts"], candidates=pool)

    compatible, would_prune = filter_candidates_for_role("base", state)
    assert [c.name for c in compatible] == ["rye whiskey"]
    assert ("rye whiskey", DrinkPruneRule.DRINK_ALLERGY_SOFT_FLAG) in [
        (p.name, p.rule) for p in would_prune
    ]

    compatible, would_prune = filter_candidates_for_role("sweet", state)
    assert [c.name for c in compatible] == []
    assert ("orgeat", DrinkPruneRule.DRINK_ALLERGY_HARD_FILTER) in [
        (p.name, p.rule) for p in would_prune
    ]


# check_drink_allergy — other tiers --------------------------------------------


@pytest.mark.parametrize("name", ["Baileys Irish Cream", "heavy cream", "RumChata"])
def test_dairy_liqueurs_hard_filter(name: str):
    state = _drink_state(exclusions=["dairy"])
    finding = check_drink_allergy(_component(name, "texture"), state)
    assert finding is not None
    assert finding.severity == Severity.HARD


@pytest.mark.parametrize(
    ("name", "exclusion"),
    [
        ("Amarula", "dairy"),
        ("clarified milk punch", "dairy"),
        ("advocaat", "eggs"),
        ("Ramos Gin Fizz", "eggs"),
        ("Golden Fizz", "eggs"),
        ("malted milk syrup", "gluten"),
    ],
)
def test_the_paths_the_pillar_names_are_the_paths_the_rule_catches(name: str, exclusion: str):
    """Doc/code agreement: every hidden path §3.5 names must actually hard-filter.

    Clarified milk punch is the non-obvious one — the casein curd is strained out, but the whey
    proteins stay dissolved in what reaches the glass.
    """
    state = _drink_state(exclusions=[exclusion])
    finding = check_drink_allergy(_component(name, "texture"), state)
    assert finding is not None
    assert finding.severity == Severity.HARD


@pytest.mark.parametrize("name", ["cream sherry", "creme de menthe", "cream soda"])
def test_dairy_false_friends_are_exempt(name: str):
    """Cream sherry is a sweetened oloroso; creme de menthe is dairy-free."""
    state = _drink_state(exclusions=["dairy"])
    assert check_drink_allergy(_component(name, "modifier"), state) is None


def test_drink_allergy_falls_back_to_direct_substring_for_uncovered_categories():
    """The food rule's generic fallback is preserved for exclusions in neither alias map."""
    state = _drink_state(exclusions=["celery"])
    finding = check_drink_allergy(_component("celery bitters", "aromatic"), state)
    assert finding is not None
    assert finding.severity == Severity.HARD
    assert 'matches exclusion "celery"' in finding.reason


def test_drink_allergy_no_exclusions_returns_none():
    state = _drink_state()
    assert check_drink_allergy(_component("orgeat", "sweet"), state) is None


# check_drink_allergy — whole-word matching --------------------------------------


@pytest.mark.parametrize("name", ["Salers", "Alessio Vermouth", "Aleppo tincture"])
def test_short_aliases_do_not_match_inside_a_longer_word(name: str):
    """"ale" is a word, not a substring.

    Salers is a gentian aperitif and Alessio a vermouth — both gluten-free, both containing
    the letters a-l-e. A HARD finding never reaches the user (it is excluded from
    `compatible`), so a substring match here deletes a safe bottle silently.
    """
    state = _drink_state(exclusions=["gluten"])
    finding = check_drink_allergy(_component(name, "modifier"), state)
    assert finding is None or finding.severity == Severity.SOFT


@pytest.mark.parametrize(
    ("name", "exclusion"),
    [
        ("Beefeater gin", "beef"),
        ("Codigo 1530 tequila", "fish"),
        ("Hamilton 86 rum", "pork"),
        ("Fish House Punch", "fish"),
        ("Prairie Oyster", "shellfish"),
        ("gluten-free beer", "gluten"),
        ("Porter's Gin", "gluten"),
    ],
)
def test_bar_name_collisions_are_not_allergen_hits(name: str, exclusion: str):
    """Products named after people, places and clubs collide with allergen words.

    A Prairie Oyster is a raw egg; Fish House Punch is named for a Philadelphia fishing club.
    Word boundaries handle most of these; the rest are declared collisions.
    """
    state = _drink_state(exclusions=[exclusion])
    assert check_drink_allergy(_component(name, "modifier"), state) is None


@pytest.mark.parametrize("name", ["pale ale", "cream ale", "Baltic porter", "malted milk"])
def test_whole_word_matching_still_catches_the_real_products(name: str):
    state = _drink_state(exclusions=["gluten"])
    finding = check_drink_allergy(_component(name, "modifier"), state)
    assert finding is not None
    assert finding.severity == Severity.HARD


# check_drink_allergy — food-allergen coverage behind a bar ---------------------


@pytest.mark.parametrize(
    ("name", "exclusion"),
    [
        ("clam juice", "shellfish"),
        ("Clamato", "shellfish"),
        ("shrimp paste", "shellfish"),
        ("Worcestershire sauce", "fish"),
        ("anchovy-stuffed olive", "fish"),
        ("bacon fat-washed bourbon", "pork"),
        ("beef consomme", "beef"),
        ("soy sauce", "soy"),
        ("miso-washed rye", "soy"),
        ("hot buttered rum", "dairy"),
    ],
)
def test_food_allergens_behind_the_bar_still_hard_filter(name: str, exclusion: str):
    """A drink session must not lose an allergen category the food session catches.

    Clamato is clam broth, Worcestershire carries anchovy, and a fat wash carries whatever fat
    it was made with. These are food exposures that happen to arrive in a glass.
    """
    state = _drink_state(exclusions=[exclusion])
    finding = check_drink_allergy(_component(name, "modifier"), state)
    assert finding is not None, f"{name!r} slipped a {exclusion} exclusion"
    assert finding.severity == Severity.HARD


def test_drink_hard_tier_covers_every_food_alias_except_the_overridden_category():
    """The structural invariant behind the fix: drink HARD ⊇ food HARD, gluten excepted.

    Switching a session to `medium: drink` must never lose an allergen path. Rather than
    trusting that the drink map was hand-copied completely, the rule reads the food map for
    every category not in DRINK_EXCLUSION_FOOD_OVERRIDES, and this walks all of them.
    """
    from mise_en_prompt.conflicts import DRINK_EXCLUSION_FOOD_OVERRIDES, EXCLUSION_ALIASES

    for exclusion, aliases in EXCLUSION_ALIASES.items():
        if exclusion in DRINK_EXCLUSION_FOOD_OVERRIDES:
            continue
        state = _drink_state(exclusions=[exclusion])
        for alias in aliases:
            finding = check_drink_allergy(_component(alias, "modifier"), state)
            assert finding is not None, f"{alias!r} slipped a drink-side {exclusion} exclusion"
            assert finding.severity == Severity.HARD


@pytest.mark.parametrize("name", ["wheat", "barley", "rye", "spelt", "farro"])
def test_the_food_gluten_list_is_the_one_category_that_does_not_carry_over(name: str):
    """Grains are the wrong unit behind a bar — that asymmetry is the whole soft tier.

    A bare grain word must not HARD-fire in a drink session, or `rye` deletes rye whiskey.
    """
    state = _drink_state(exclusions=["gluten"])
    finding = check_drink_allergy(_component(name, "base"), state)
    assert finding is None or finding.severity == Severity.SOFT


@pytest.mark.parametrize("name", ["wheat flour", "seitan", "semolina", "couscous", "bulgur"])
def test_grain_foods_are_surfaced_rather_than_passing_a_gluten_exclusion_in_silence(name: str):
    """The override defers the food gluten list; it must not discard it.

    These names match no drink alias and no soft alias, so withholding EXCLUSION_ALIASES from
    the HARD tier left them with no tier at all and they cleared a gluten exclusion silently.
    SOFT rather than HARD because promoting a grain word to HARD behind a bar is what the
    override exists to prevent — "rye" would delete rye whiskey. Surfacing beats both.
    """
    state = _drink_state(exclusions=["gluten"])
    finding = check_drink_allergy(_component(name, "modifier"), state)
    assert finding is not None, f"{name!r} cleared a gluten exclusion with no finding at all"
    assert finding.severity == Severity.SOFT


def test_the_deferred_gluten_fallback_does_not_mask_a_hard_hit_on_another_exclusion():
    """Severity still decides across exclusions once the fallback can produce a SOFT hit."""
    state = _drink_state(exclusions=["gluten", "nuts"])
    finding = check_drink_allergy(_component("seitan orgeat", "sweet"), state)
    assert finding is not None
    assert finding.severity == Severity.HARD


def test_a_false_friend_cancels_only_the_word_it_explains():
    """"coconut" must not wave a candidate past the rest of the nut checks."""
    state = _drink_state(exclusions=["nuts"])
    finding = check_drink_allergy(_component("coconut orgeat", "sweet"), state)
    assert finding is not None
    assert finding.severity == Severity.HARD
    assert "orgeat" in finding.reason
    assert check_drink_allergy(_component("coconut cream", "sweet"), state) is None


@pytest.mark.parametrize("name", ["peanut orgeat", "peanut-washed bourbon"])
def test_peanut_is_a_hard_nut_hit_not_a_false_friend(name: str):
    """Legume-not-tree-nut is a real distinction and the wrong one to draw silently."""
    state = _drink_state(exclusions=["nuts"])
    finding = check_drink_allergy(_component(name, "sweet"), state)
    assert finding is not None
    assert finding.severity == Severity.HARD


def test_a_hard_hit_outranks_a_soft_hit_on_an_earlier_exclusion():
    """Severity decides which finding is returned, not the order of intent.exclusions.

    A bacon-fat-washed bourbon is an ambiguous gluten path and a definite pork one. Returning
    on first match would report only the soft flag and leave it in `compatible`.
    """
    state = _drink_state(exclusions=["gluten", "pork"])
    finding = check_drink_allergy(_component("bacon fat-washed bourbon", "base"), state)
    assert finding is not None
    assert finding.severity == Severity.HARD
    assert "pork" in finding.reason

    pool = [_component("bacon fat-washed bourbon", "base", 8)]
    compatible, would_prune = filter_candidates_for_role("base", _drink_state(
        exclusions=["gluten", "pork"], candidates=pool,
    ))
    assert compatible == []
    assert [p.rule for p in would_prune] == [DrinkPruneRule.DRINK_ALLERGY_HARD_FILTER]


# check_drink_redundancy -------------------------------------------------------


def test_split_base_survives_redundancy():
    """Two rums at intensity 8 and 7 in the base slot is the canonical split base.

    The food rule prunes this on intensity ±2; the drink rule allows it because the two
    are different bar-product classes and `base` is a stackable role.
    """
    pot = _component("Jamaican pot-still rum", "base", 8)
    demerara = _component("Demerara rum", "base", 7)
    state = _drink_state(
        candidates=[pot, demerara], selected=["Jamaican pot-still rum"],
    )
    assert check_drink_redundancy(demerara, state) is None


def test_stacked_bitters_survive_redundancy():
    """Angostura at 6 plus orange bitters at 5 is the defining move, not an accident."""
    angostura = _component("Angostura bitters", "bitter", 6)
    orange = _component("orange bitters", "bitter", 5)
    state = _drink_state(candidates=[angostura, orange], selected=["Angostura bitters"])
    assert check_drink_redundancy(orange, state) is None


def test_same_product_class_in_a_stackable_role_is_still_caught():
    """Stackability governs only the intensity fallback — the class check runs first."""
    pot = _component("Jamaican pot-still rum", "base", 8)
    smith = _component("Smith & Cross", "base", 9)
    state = _drink_state(candidates=[pot, smith], selected=["Jamaican pot-still rum"])
    finding = check_drink_redundancy(smith, state)
    assert finding is not None
    assert finding.severity == Severity.SOFT
    assert finding.rule == DrinkPruneRule.DRINK_FUNCTIONAL_REDUNDANCY
    assert "jamaican rum" in finding.reason


def test_two_dry_vermouths_collapse_to_one_slot():
    dolin = _component("Dolin Dry vermouth", "modifier", 4)
    noilly = _component("Noilly Prat", "modifier", 4)
    state = _drink_state(candidates=[dolin, noilly], selected=["Dolin Dry vermouth"])
    finding = check_drink_redundancy(noilly, state)
    assert finding is not None
    assert "dry vermouth" in finding.reason


def test_two_orange_liqueurs_collapse_to_one_slot():
    cointreau = _component("Cointreau", "modifier", 6)
    marnier = _component("Grand Marnier", "modifier", 6)
    state = _drink_state(candidates=[cointreau, marnier], selected=["Cointreau"])
    assert check_drink_redundancy(marnier, state) is not None


def test_single_slot_role_still_falls_back_to_intensity():
    """sweet/acid/dilution/texture are single-slot — they keep the food-style ±2 comparison."""
    lime = _component("lime juice", "acid", 7)
    lemon = _component("lemon juice", "acid", 6)
    state = _drink_state(candidates=[lime, lemon], selected=["lime juice"])
    finding = check_drink_redundancy(lemon, state)
    assert finding is not None
    assert finding.rule == DrinkPruneRule.DRINK_FUNCTIONAL_REDUNDANCY


def test_single_slot_role_far_intensity_no_conflict():
    lime = _component("lime juice", "acid", 7)
    verjus = _component("verjus", "acid", 2)
    state = _drink_state(candidates=[lime, verjus], selected=["lime juice"])
    assert check_drink_redundancy(verjus, state) is None


def test_drink_redundancy_never_matches_a_candidate_to_itself():
    """The unconditional class check would otherwise flag an already-selected candidate."""
    dolin = _component("Dolin Dry vermouth", "modifier", 4)
    state = _drink_state(candidates=[dolin], selected=["Dolin Dry vermouth"])
    assert check_drink_redundancy(dolin, state) is None


def test_drink_redundancy_different_role_no_conflict():
    dolin = _component("Dolin Dry vermouth", "modifier", 4)
    noilly = _component("Noilly Prat", "aromatic", 4)
    state = _drink_state(candidates=[dolin, noilly], selected=["Dolin Dry vermouth"])
    assert check_drink_redundancy(noilly, state) is None


def test_unclassified_components_fall_through_to_intensity_only():
    """A component with no bar-product class is judged exactly as food judges an ingredient."""
    assert _find_product_class("egg white") is None
    egg = _component("egg white", "texture", 5)
    aquafaba = _component("aquafaba", "texture", 4)
    state = _drink_state(candidates=[egg, aquafaba], selected=["egg white"])
    assert check_drink_redundancy(aquafaba, state) is not None


# check_build_impossibility (v1 stub) ------------------------------------------


def test_build_impossibility_v1_stub_returns_none():
    state = _drink_state(DrinkIntent(build_method="stirred"))
    assert check_build_impossibility(_component("egg white", "texture"), state) is None


# Medium dispatch --------------------------------------------------------------


def test_rules_for_dispatches_on_medium():
    assert _rules_for(_dish_state()) is _ALL_RULES
    assert _rules_for(_drink_state()) is _ALL_DRINK_RULES


def test_drink_session_never_emits_a_food_rule():
    """A drifting drink candidate is labelled family_drift, never cuisine_drift."""
    state = _drink_state(DrinkIntent(drink_family="Mai Tai"), exclusions=["nuts"])
    candidate = _component("amaretto", "sweet", 5, origin="Negroni")
    findings = check_candidate(candidate, state)
    rules = {f.rule for f in findings}
    assert DrinkPruneRule.DRINK_ALLERGY_HARD_FILTER in rules
    assert DrinkPruneRule.FAMILY_DRIFT in rules
    assert not any(isinstance(r, PruneRule) for r in rules)


def test_dish_session_never_emits_a_drink_rule():
    state = _dish_state(Intent(cuisine="Honduran", exclusions=["shellfish"]))
    candidate = Candidate(
        name="dried shrimp", cuisine_origin="Japanese", functional_role="umami",
    )
    findings = check_candidate(candidate, state)
    rules = {f.rule for f in findings}
    assert PruneRule.ALLERGY_HARD_FILTER in rules
    assert PruneRule.CUISINE_DRIFT in rules
    assert not any(isinstance(r, DrinkPruneRule) for r in rules)


def test_food_redundancy_still_prunes_the_pair_the_drink_rule_allows():
    """Regression guard: the food rule was not loosened to make split base work."""
    pot = _component("Jamaican pot-still rum", "base", 8)
    demerara = _component("Demerara rum", "base", 7)
    state = _dish_state(candidates=[pot, demerara], selected=["Jamaican pot-still rum"])
    finding = check_functional_redundancy(demerara, state)
    assert finding is not None
    assert finding.rule == PruneRule.FUNCTIONAL_REDUNDANCY


def test_food_allergy_behavior_on_grain_spirits_is_unchanged():
    """The food gluten list is still grain-based; the drink asymmetry did not leak into it."""
    from mise_en_prompt.conflicts import check_allergy

    state = _dish_state(Intent(exclusions=["gluten"]))
    finding = check_allergy(
        Candidate(name="rye whiskey", cuisine_origin="", functional_role="base"), state,
    )
    assert finding is not None
    assert finding.severity == Severity.HARD
    assert finding.rule == PruneRule.ALLERGY_HARD_FILTER


# Schema -----------------------------------------------------------------------


def test_drink_prune_rule_enum_has_five_values():
    assert {r.value for r in DrinkPruneRule} == {
        "family_drift",
        "drink_functional_redundancy",
        "drink_allergy_hard_filter",
        "drink_allergy_soft_flag",
        "build_impossibility",
    }


def test_prune_rule_enums_are_disjoint():
    """Disjoint values are what let PrunedItem.rule widen without ambiguity."""
    assert not {r.value for r in PruneRule} & {r.value for r in DrinkPruneRule}


def test_drink_research_plan_constructs_without_an_aromatic_base():
    """A drink has no aromatic base — the plan must be constructable without one."""
    plan = DrinkResearchPlan(
        base_spirit="Jamaican pot-still rum",
        drink_roles_to_fill=["base", "sweet", "acid", "modifier"],
        build_methods_under_consideration=["shaken", "swizzled"],
    )
    assert plan.base_spirit == "Jamaican pot-still rum"
    assert "aromatic_base" not in plan.model_dump()


def test_drink_research_plan_requires_a_base_spirit():
    """base_spirit is required for the same reason aromatic_base is: it is the backbone."""
    with pytest.raises(ValueError, match="base_spirit"):
        DrinkResearchPlan(drink_roles_to_fill=["base"])


def test_drink_research_plan_forbids_food_fields():
    with pytest.raises(ValueError):
        DrinkResearchPlan(
            base_spirit="rye", drink_roles_to_fill=[], aromatic_base="sofrito",
        )


def test_food_research_plan_still_requires_an_aromatic_base():
    """Regression guard: ResearchPlan was not relaxed to accommodate drinks."""
    with pytest.raises(ValueError, match="aromatic_base"):
        ResearchPlan(functional_roles_to_fill=["heat"])


def test_research_plan_discriminator_routes_by_payload_shape():
    dish = State(
        session_id="x", phase=Phase.GROUNDING,
        research_plan={"aromatic_base": "sofrito", "functional_roles_to_fill": ["heat"]},
    )
    drink = State(
        session_id="y", phase=Phase.GROUNDING,
        intent=Intent(medium="drink"),
        research_plan={"base_spirit": "rye", "drink_roles_to_fill": ["base"]},
    )
    assert isinstance(dish.research_plan, ResearchPlan)
    assert isinstance(drink.research_plan, DrinkResearchPlan)


def test_a_dish_session_cannot_carry_a_drink_research_plan():
    """The discriminator answers which model the payload is; the medium says which is allowed.

    Without the second check, aromatic_base stops being effectively required for a dish
    session — a drink-shaped payload routes to DrinkResearchPlan and validates, and every
    downstream read of `research_plan.functional_roles_to_fill` raises AttributeError.
    """
    with pytest.raises(ValueError, match="research_plan"):
        State(
            session_id="x", phase=Phase.GROUNDING,
            intent=Intent(star_ingredient="duck leg", cuisine="French"),
            research_plan={"base_spirit": "rye", "drink_roles_to_fill": ["base"]},
        )


def test_a_drink_session_cannot_carry_a_food_research_plan():
    with pytest.raises(ValueError, match="research_plan"):
        State(
            session_id="y", phase=Phase.GROUNDING,
            intent=Intent(medium="drink"),
            research_plan={"aromatic_base": "sofrito", "functional_roles_to_fill": ["heat"]},
        )


# Medium / vocabulary coupling -------------------------------------------------


def test_medium_drink_rejects_food_shaped_intent_fields():
    """`medium` must describe the payload, or it is a label the dispatchers misread.

    A food-shaped intent carrying `medium: drink` used to validate clean, and every medium
    dispatch downstream would then apply drink rules to food content.
    """
    with pytest.raises(ValueError, match="star_ingredient"):
        Intent(medium="drink", star_ingredient="paella", cuisine="Spanish")


def test_medium_dish_rejects_a_drink_block():
    with pytest.raises(ValueError, match="medium"):
        Intent(drink=DrinkIntent(base_spirit="rye"))


def test_shared_intent_fields_are_legal_in_both_media():
    """servings, time_budget_min, exclusions and occasion belong to both."""
    drink = Intent(
        medium="drink", servings=2, time_budget_min=10,
        exclusions=["nuts"], occasion="aperitivo hour",
    )
    assert drink.servings == 2
    dish = Intent(star_ingredient="pinto beans", servings=2, exclusions=["nuts"])
    assert dish.medium == "dish"


def test_a_food_shaped_state_cannot_relabel_itself_as_a_drink_and_lose_the_hard_tier():
    """The end-to-end version: the hook blocks the state the mislabel would have produced."""
    yaml_text = (
        "session_id: mislabelled\n"
        "phase: CURATE\n"
        "intent:\n"
        "  star_ingredient: paella\n"
        "  cuisine: Spanish\n"
        "  exclusions: [shellfish]\n"
        "  medium: drink\n"
    )
    valid, msg = validate_state_content(yaml_text)
    assert not valid
    assert "star_ingredient" in msg


def test_a_dish_session_cannot_log_research_under_a_drink_tag():
    """Relabelling an entry with a drink tag used to skip the ordering gate entirely.

    PRECURSORS.get('drink_role') is None, which reads as "no precursor required" — so a dish
    log of [dilution_math, drink_candidate] passed with an empty prior log.
    """
    with pytest.raises(ValueError, match="research_log"):
        State(
            session_id="x", phase=Phase.RESEARCH,
            intent=Intent(star_ingredient="duck leg"),
            research_log=[_entry("drink_role")],
        )


def test_a_drink_session_cannot_log_research_under_a_food_tag():
    with pytest.raises(ValueError, match="research_log"):
        State(
            session_id="y", phase=Phase.RESEARCH,
            intent=Intent(medium="drink"),
            research_log=[_entry("aromatic_base")],
        )


def test_a_dish_session_cannot_record_a_drink_prune_rule():
    """The audit-trail claim in the DrinkPruneRule docstring, enforced by the schema."""
    with pytest.raises(ValueError, match="pruned"):
        State(
            session_id="x", phase=Phase.CURATE,
            intent=Intent(star_ingredient="duck leg"),
            pruned=[PrunedItem(
                name="x", rule=DrinkPruneRule.DRINK_ALLERGY_SOFT_FLAG, reason="r",
            )],
        )


def test_a_drink_session_cannot_record_a_food_prune_rule():
    with pytest.raises(ValueError, match="pruned"):
        State(
            session_id="y", phase=Phase.CURATE,
            intent=Intent(medium="drink"),
            pruned=[PrunedItem(name="x", rule=PruneRule.CUISINE_DRIFT, reason="r")],
        )


def test_unrecognised_research_plan_still_reports_the_food_side_error():
    """An unrecognised payload falls through to ResearchPlan, not a new union-shaped error."""
    with pytest.raises(ValueError, match="aromatic_base"):
        State(session_id="x", phase=Phase.GROUNDING, research_plan={"nonsense": 1})


def test_intent_accepts_drink_fields_under_the_drink_key():
    """The fields Intent rejects at the top level live on DrinkIntent instead."""
    with pytest.raises(ValueError):
        Intent(base_spirit="rye whiskey")
    intent = Intent(
        medium="drink",
        drink=DrinkIntent(base_spirit="rye whiskey", build_method="stirred", abv_target_pct=24.0),
    )
    assert intent.drink is not None
    assert intent.drink.base_spirit == "rye whiskey"


def test_drink_intent_forbids_unknown_fields():
    with pytest.raises(ValueError):
        DrinkIntent(garnish="lemon twist")


@pytest.mark.parametrize("bad", [{"build_method": "microwaved"}, {"strength_level": "boozy"},
                                 {"sweetness_level": "sugary"}, {"service_format": "keg"},
                                 {"family_stance": "freestyle"}])
def test_drink_intent_rejects_invalid_literals(bad: dict):
    with pytest.raises(ValueError):
        DrinkIntent(**bad)


def test_pruned_item_carries_a_drink_rule():
    item = PrunedItem(
        name="orgeat",
        rule=DrinkPruneRule.DRINK_ALLERGY_HARD_FILTER,
        reason="user excluded nuts",
    )
    assert item.rule == DrinkPruneRule.DRINK_ALLERGY_HARD_FILTER


def test_research_log_entry_accepts_drink_tags():
    entry = ResearchLogEntry(
        timestamp=datetime(2026, 8, 1, 12, 0),
        tag="dilution_math",
        query="shaken dilution for a daiquiri",
        result_summary="water pickup measured per build",
    )
    assert entry.tag == "dilution_math"


def test_research_log_entry_still_rejects_unknown_tags():
    with pytest.raises(ValueError):
        ResearchLogEntry(
            timestamp=datetime(2026, 8, 1, 12, 0),
            tag="not_a_valid_tag",
            query="x",
            result_summary="y",
        )


# Round trip -------------------------------------------------------------------


def _full_drink_state() -> State:
    fixed_time = datetime(2026, 8, 1, 17, 0, 0)
    return State(
        session_id="drink-rt",
        phase=Phase.CURATE,
        created_at=fixed_time,
        updated_at=fixed_time,
        intent=Intent(
            medium="drink",
            servings=2,
            time_budget_min=10,
            exclusions=["nuts"],
            occasion="aperitivo hour",
            drink=DrinkIntent(
                base_spirit="Jamaican pot-still rum",
                drink_family="Tiki",
                family_variant="Mai Tai",
                family_stance="tradition",
                strength_level="spirit_forward",
                sweetness_level="off_dry",
                build_method="shaken",
                abv_target_pct=22.5,
                dilution_target_pct=25.0,
                service_format="single",
                glassware="double old fashioned",
            ),
        ),
        research_plan=DrinkResearchPlan(
            base_spirit="Jamaican pot-still rum",
            drink_roles_to_fill=["base", "modifier", "sweet", "acid"],
            build_methods_under_consideration=["shaken", "swizzled"],
        ),
        research_log=[
            ResearchLogEntry(
                timestamp=fixed_time,
                tag="base_spirit",
                query="Jamaican pot-still rum ester profile",
                result_summary="high-ester funk; pairs with Demerara for a split base",
            ),
            ResearchLogEntry(
                timestamp=fixed_time,
                tag="drink_role",
                query="Mai Tai role slots",
                result_summary="split base, orange liqueur, orgeat, lime",
            ),
            ResearchLogEntry(
                timestamp=fixed_time,
                tag="build_method",
                query="shake vs swizzle for a Mai Tai",
                result_summary="shake with crushed ice, then swizzle in glass",
            ),
            ResearchLogEntry(
                timestamp=fixed_time,
                tag="dilution_math",
                query="water pickup on a hard shake",
                result_summary="measured per build; batch requires added water by measure",
            ),
        ],
        candidates=[
            Candidate(
                name="Jamaican pot-still rum",
                cuisine_origin="Tiki",
                functional_role="base",
                intensity=8,
                notes="Jamaican provenance; high ester",
            ),
            Candidate(
                name="Demerara rum",
                cuisine_origin="Tiki",
                functional_role="base",
                intensity=7,
                notes="Guyanese provenance; molasses depth",
            ),
        ],
        selected=["Jamaican pot-still rum", "Demerara rum"],
        pruned=[
            PrunedItem(
                name="orgeat",
                rule=DrinkPruneRule.DRINK_ALLERGY_HARD_FILTER,
                reason="user excluded nuts",
            ),
            PrunedItem(
                name="Campari",
                rule=DrinkPruneRule.FAMILY_DRIFT,
                reason="Negroni (Spirit-forward); target is Tiki (Tiki)",
            ),
        ],
    )


def test_drink_state_round_trip(tmp_path: Path):
    """Dumping then loading a drink state preserves every field, discriminator included."""
    original = _full_drink_state()
    target = tmp_path / "state.yaml"
    original.dump_yaml(target)
    loaded = State.load_yaml(target)

    assert loaded == original
    assert isinstance(loaded.research_plan, DrinkResearchPlan)
    assert loaded.intent.medium == "drink"
    assert loaded.intent.drink is not None
    assert loaded.intent.drink.abv_target_pct == 22.5
    assert loaded.pruned[0].rule == DrinkPruneRule.DRINK_ALLERGY_HARD_FILTER


def test_dish_state_round_trip_still_loads_as_a_food_research_plan(tmp_path: Path):
    """Regression guard: a food plan must not be reinterpreted as a drink one."""
    original = State(
        session_id="dish-rt",
        phase=Phase.GROUNDING,
        intent=Intent(star_ingredient="pinto beans", cuisine="Honduran"),
        research_plan=ResearchPlan(
            aromatic_base="Latin sofrito",
            functional_roles_to_fill=["heat", "acid"],
        ),
    )
    target = tmp_path / "state.yaml"
    original.dump_yaml(target)
    loaded = State.load_yaml(target)

    assert loaded == original
    assert isinstance(loaded.research_plan, ResearchPlan)
    assert not isinstance(loaded.research_plan, DrinkResearchPlan)
    assert loaded.intent.medium == "dish"


# Backward compatibility -------------------------------------------------------


LEGACY_STATE_YAML = """\
session_id: legacy-no-medium
phase: CURATE
created_at: '2026-04-28T17:00:00'
updated_at: '2026-04-28T17:00:00'
intent:
  star_ingredient: pinto beans
  cuisine: Honduran
  cuisine_region: Honduran
  heat_level: spicy
  servings: 4
  time_budget_min: 180
  exclusions:
  - shellfish
  occasion: weeknight dinner
research_plan:
  aromatic_base: Latin sofrito (Honduran variant)
  functional_roles_to_fill:
  - heat
  - acid
"""
"""Byte-for-byte the shape the schema emitted before drinks existed: no ``medium`` key on
intent, no ``drink`` key, and a bare food research plan."""


def test_legacy_state_yaml_without_medium_loads(tmp_path: Path):
    """A state.yaml written before drinks existed has no medium key and must still load."""
    target = tmp_path / "state.yaml"
    target.write_text(LEGACY_STATE_YAML, encoding="utf-8")
    loaded = State.load_yaml(target)
    assert loaded.intent.medium == "dish"
    assert loaded.intent.drink is None
    assert isinstance(loaded.research_plan, ResearchPlan)


def test_legacy_state_yaml_dispatches_to_the_food_rules(tmp_path: Path):
    """Backward compat is behavioral, not just structural: same rule list object as before."""
    target = tmp_path / "state.yaml"
    target.write_text(LEGACY_STATE_YAML, encoding="utf-8")
    loaded = State.load_yaml(target)
    assert _rules_for(loaded) is _ALL_RULES


def test_legacy_state_yaml_passes_the_validation_hook():
    valid, msg = validate_state_content(LEGACY_STATE_YAML)
    assert valid, msg


def test_repo_sample_session_still_loads_and_behaves_as_a_dish():
    """The checked-in pre-drink sample session is the real-world backward-compat case."""
    sample = (
        Path(__file__).resolve().parents[1]
        / "sessions" / "2026-04-28-pinto-beans-sample" / "state.yaml"
    )
    if not sample.exists():
        pytest.skip("sample session not present in this checkout")
    loaded = State.load_yaml(sample)
    assert loaded.intent.medium == "dish"
    assert _rules_for(loaded) is _ALL_RULES


# Hook ordering ----------------------------------------------------------------


def _entry(tag: str) -> ResearchLogEntry:
    return ResearchLogEntry(
        timestamp=datetime(2026, 8, 1, 12, 0),
        tag=tag,
        query=f"query for {tag}",
        result_summary="summary",
    )


def test_drink_precursors_mirror_the_food_table_without_touching_it():
    assert PRECURSORS == {
        "aromatic_base": None,
        "functional_role": "aromatic_base",
        "candidate": "functional_role",
        "pairing": "functional_role",
        "technique": None,
    }
    assert DRINK_PRECURSORS == {
        "base_spirit": None,
        "drink_role": "base_spirit",
        "drink_candidate": "drink_role",
        "drink_pairing": "drink_role",
        "build_method": None,
        "dilution_math": "build_method",
    }


def test_drink_research_log_passes_without_a_fabricated_aromatic_base():
    """The whole point: a drink log satisfies the hook using only drink tags."""
    log = [_entry("base_spirit"), _entry("drink_role"), _entry("drink_candidate")]
    assert validate_research_log_order(log, "drink") is None


def test_drink_role_before_base_spirit_blocks():
    msg = validate_research_log_order([_entry("drink_role")], "drink")
    assert msg is not None
    assert "base_spirit" in msg


def test_drink_candidate_before_drink_role_blocks():
    msg = validate_research_log_order([_entry("base_spirit"), _entry("drink_candidate")], "drink")
    assert msg is not None
    assert "drink_role" in msg


def test_dilution_math_before_build_method_blocks():
    """Water pickup is a property of the build — it cannot be computed before the build is known."""
    msg = validate_research_log_order([_entry("dilution_math")], "drink")
    assert msg is not None
    assert "build_method" in msg


def test_build_method_has_no_precursor():
    log = [_entry("build_method"), _entry("dilution_math"), _entry("base_spirit")]
    assert validate_research_log_order(log, "drink") is None


def test_the_ordering_gate_rejects_a_tag_from_the_other_medium():
    """`.get` on the wrong table returns None, which reads as "no precursor required".

    Rejecting rather than skipping is what stops the ordering invariant from being escapable
    by relabelling an entry.
    """
    msg = validate_research_log_order([_entry("drink_role")], "dish")
    assert msg is not None
    assert "not a dish research tag" in msg

    msg = validate_research_log_order([_entry("functional_role")], "drink")
    assert msg is not None
    assert "not a drink research tag" in msg


def test_validate_research_log_order_defaults_to_the_food_table():
    """The defaulted parameter is what keeps every existing single-argument call site valid."""
    assert validate_research_log_order([_entry("functional_role")]) is not None
    assert validate_research_log_order([_entry("aromatic_base"), _entry("functional_role")]) is None


def test_validate_state_content_accepts_a_well_formed_drink_state(tmp_path: Path):
    state = _full_drink_state()
    yaml_path = tmp_path / "state.yaml"
    state.dump_yaml(yaml_path)
    valid, msg = validate_state_content(yaml_path.read_text(encoding="utf-8"))
    assert valid, msg


def test_validate_state_content_blocks_out_of_order_drink_research_log(tmp_path: Path):
    """End-to-end: the medium on the state selects the drink precursor table."""
    bad_state = State(
        session_id="bad-drink-order",
        phase=Phase.RESEARCH,
        intent=Intent(medium="drink", drink=DrinkIntent(drink_family="Tiki")),
        research_log=[_entry("drink_role")],  # missing base_spirit precursor
    )
    yaml_path = tmp_path / "state.yaml"
    bad_state.dump_yaml(yaml_path)
    valid, msg = validate_state_content(yaml_path.read_text(encoding="utf-8"))
    assert not valid
    assert "research_log" in msg
    assert "base_spirit" in msg


# CLI smoke tests --------------------------------------------------------------


def test_cli_filter_command_on_a_drink_state(tmp_path: Path):
    state = _drink_state(
        DrinkIntent(drink_family="Mai Tai"),
        exclusions=["nuts"],
        candidates=[
            _component("Jamaican pot-still rum", "base", 8, origin="Tiki"),
            _component("Demerara rum", "base", 7, origin="Tiki"),
            _component("orgeat", "sweet", 3),
        ],
    )
    state_path = tmp_path / "state.yaml"
    state.dump_yaml(state_path)

    result = subprocess.run(
        [
            sys.executable, "-m", "mise_en_prompt.conflicts",
            "filter", "--role", "base", "--state", str(state_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    output = json.loads(result.stdout)
    names = [c["name"] for c in output["compatible"]]
    assert "Jamaican pot-still rum" in names
    assert "Demerara rum" in names
    assert output["would_prune"] == []


def test_cli_check_command_on_a_drink_state(tmp_path: Path):
    state = _drink_state(DrinkIntent(drink_family="Mai Tai"), exclusions=["nuts"])
    state_path = tmp_path / "state.yaml"
    state.dump_yaml(state_path)

    candidate_json = json.dumps({
        "name": "amaretto",
        "cuisine_origin": "Negroni",
        "functional_role": "sweet",
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
    assert DrinkPruneRule.DRINK_ALLERGY_HARD_FILTER.value in rules
    assert DrinkPruneRule.FAMILY_DRIFT.value in rules
    assert PruneRule.CUISINE_DRIFT.value not in rules
