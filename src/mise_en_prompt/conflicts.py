"""Conflict detection rules for ingredient candidates.

Four rules:
  - check_allergy (HARD)            — candidate matches a state.intent.exclusions term
  - check_cuisine_drift (SOFT, or INFO under cuisine_stance=explore)
                                    — candidate's cuisine_origin is in a different group than the dish
  - check_functional_redundancy (SOFT) — same role + close intensity already in state.selected
  - check_technique_impossibility (SOFT) — candidate.prep_time_min exceeds intent.time_budget_min

Four mirrored rules for drinks, selected when state.intent.medium is "drink":
  - check_drink_allergy (HARD/SOFT)  — nut-bearing liqueurs hard-filter; distilled grain
    spirits surface as soft flags instead of vanishing
  - check_family_drift (SOFT, or INFO under drink.family_stance=explore)
                                    — candidate's cuisine_origin is in a different drink
    family group than the drink
  - check_drink_redundancy (SOFT)    — same role + same bar-product class already selected
  - check_build_impossibility (SOFT) — v1 stub, returns None

check_candidate runs whichever set _rules_for selects, with HARD taking precedence: an
allergy-blocked candidate reports only its hard findings. classify_candidate turns findings
into exactly one Verdict, and filter_candidates_for_role sorts a role's candidates into the
matching buckets (compatible, would_prune, excluded) used by the chef agent during CURATE.

Hooks call this module to verify the agent's pruning decisions; the agent calls the CLI
between AskUserQuestion prompts to compute the eligible pool for each functional role.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from enum import Enum
from functools import cache
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from mise_en_prompt.state import (
    Candidate,
    DrinkPruneRule,
    PruneRule,
    PrunedItem,
    State,
)


class Severity(str, Enum):
    HARD = "HARD"  # removed outright, never offered, not overridable
    SOFT = "SOFT"  # pulled from the offered pool; the user can override
    INFO = "INFO"  # offered as normal, with a note (cuisine_drift under explore)


class Verdict(str, Enum):
    """The one bucket a candidate lands in. Derived only from its findings."""

    COMPATIBLE = "compatible"
    WOULD_PRUNE = "would_prune"
    EXCLUDED = "excluded"


class ConflictFinding(BaseModel):
    """A single rule firing on a candidate. Findings compose into the agent's decision."""

    model_config = ConfigDict(extra="forbid")

    severity: Severity
    rule: PruneRule | DrinkPruneRule
    reason: str


# Allergy alias map. Common-case lookup only — comprehensive ingredient ontology is v2.
EXCLUSION_ALIASES: dict[str, list[str]] = {
    "shellfish": [
        "shrimp", "prawn", "lobster", "crab", "mussel", "oyster", "scallop",
        "clam", "crayfish", "langoustine",
    ],
    "dairy": [
        "milk", "cream", "butter", "cheese", "yogurt", "yoghurt", "whey",
        "lactose", "ghee", "curd",
    ],
    "gluten": [
        "wheat", "barley", "rye", "spelt", "couscous", "semolina", "bulgur",
        "farro", "seitan",
    ],
    "nuts": [
        "almond", "cashew", "walnut", "pecan", "pistachio", "hazelnut",
        "macadamia", "brazil nut",
    ],
    "eggs": ["egg", "yolk", "albumen"],
    "soy": ["soy", "soya", "tofu", "edamame", "miso", "tempeh", "tamari", "natto"],
    "fish": ["fish", "anchovy", "salmon", "tuna", "cod", "mackerel", "sardine", "trout"],
    "pork": [
        "pork", "bacon", "ham", "lard", "pancetta", "prosciutto", "chorizo",
        "guanciale",
    ],
    "beef": ["beef", "brisket", "chuck", "ribeye", "tenderloin"],
}


# Names that contain an allergen term without being that allergen. Each phrase is blanked
# out of the candidate name before that one term is matched, so "almond butter" still
# trips a nuts exclusion but not a dairy one, and "eggplant with egg wash" still trips eggs.
ALLERGEN_FALSE_FRIENDS: dict[str, list[str]] = {
    "egg": ["eggplant"],
    "lard": ["collard"],
    "ham": ["champagne", "graham"],
    "wheat": ["buckwheat"],
    "butter": [
        "butternut", "butter bean", "peanut butter", "almond butter", "cashew butter",
        "nut butter", "apple butter", "cocoa butter",
    ],
    "milk": ["coconut milk", "almond milk", "oat milk", "soy milk", "rice milk", "cashew milk"],
    "cream": ["coconut cream", "cream of tartar"],
}


def _contains_allergen(name_lower: str, term: str) -> bool:
    """True if ``term`` appears in ``name_lower`` outside any of its false-friend phrases."""
    for friend in ALLERGEN_FALSE_FRIENDS.get(term, []):
        name_lower = name_lower.replace(friend, " ")
    return term in name_lower


# Cuisine groupings — same-group cuisines compose comfortably. Hand-curated; expand as needed.
CUISINE_GROUPS: dict[str, list[str]] = {
    "Latin American": [
        "mexican", "honduran", "salvadoran", "guatemalan", "costa rican", "nicaraguan",
        "panamanian", "cuban", "puerto rican", "dominican", "haitian", "caribbean",
        "central american", "south american", "peruvian", "argentine", "brazilian",
        "colombian", "venezuelan", "chilean", "ecuadorian", "tex-mex", "latin",
    ],
    "European": [
        "italian", "french", "spanish", "portuguese", "greek", "british", "irish",
        "german", "polish", "russian", "scandinavian", "european",
    ],
    "East Asian": [
        "chinese", "japanese", "korean", "vietnamese", "thai", "malaysian",
        "indonesian", "filipino", "burmese", "cambodian", "laotian", "east asian",
        "taiwanese", "hong kong",
    ],
    "South Asian": [
        "indian", "pakistani", "bangladeshi", "sri lankan", "nepali", "south asian",
    ],
    "Middle Eastern": [
        "lebanese", "turkish", "iranian", "persian", "israeli", "syrian", "jordanian",
        "palestinian", "moroccan", "tunisian", "algerian", "egyptian", "middle eastern",
        "north african", "mediterranean",
    ],
    "Sub-Saharan African": [
        "ethiopian", "west african", "nigerian", "ghanaian", "senegalese", "south african",
        "kenyan", "tanzanian", "african",
    ],
    "North American": [
        "american", "cajun", "creole", "southern", "soul food", "new england",
    ],
}


# Roles where stacking multiple candidates is normal — skip redundancy check.
STACKABLE_ROLES: set[str] = {
    "aromatic_herb", "aromatic_herbs", "spice", "spices", "aromatic", "aromatics",
}


def _find_cuisine_group(cuisine: str) -> str | None:
    """Return the group for ``cuisine`` (case-insensitive).

    Tries, in order: an exact member match; the longest member contained in the cuisine
    ("Veracruz Mexican" -> mexican); the cuisine contained in a member ("Asian" ->
    east asian). The order matters: a plain substring scan put "American" in Latin
    American via "central american".
    """
    if not cuisine:
        return None
    cuisine_lower = cuisine.strip().lower()
    for group, members in CUISINE_GROUPS.items():
        if cuisine_lower in members:
            return group
    best: tuple[int, str] | None = None
    for group, members in CUISINE_GROUPS.items():
        for member in members:
            if member in cuisine_lower and (best is None or len(member) > best[0]):
                best = (len(member), group)
    if best:
        return best[1]
    for group, members in CUISINE_GROUPS.items():
        if any(cuisine_lower in member for member in members):
            return group
    return None


def check_allergy(candidate: Candidate, state: State) -> ConflictFinding | None:
    """HARD: candidate name (or alias for a category exclusion) matches an exclusion."""
    if not state.intent.exclusions:
        return None
    name_lower = candidate.name.lower()
    for exclusion in state.intent.exclusions:
        ex_lower = exclusion.strip().lower()
        if not ex_lower:
            continue
        if _contains_allergen(name_lower, ex_lower) or name_lower in ex_lower:
            return ConflictFinding(
                severity=Severity.HARD,
                rule=PruneRule.ALLERGY_HARD_FILTER,
                reason=f'matches exclusion "{exclusion}"',
            )
        for alias in EXCLUSION_ALIASES.get(ex_lower, []):
            if _contains_allergen(name_lower, alias):
                return ConflictFinding(
                    severity=Severity.HARD,
                    rule=PruneRule.ALLERGY_HARD_FILTER,
                    reason=f'"{candidate.name}" is a {exclusion} ingredient ({alias})',
                )
    return None


def check_cuisine_drift(candidate: Candidate, state: State) -> ConflictFinding | None:
    """candidate.cuisine_origin is in a different group than state.intent.cuisine.

    Severity follows intent.cuisine_stance: SOFT (gating, overridable) under tradition,
    INFO (offered with a note) under explore. An unset stance gates like tradition; the
    agent is meant to ask before CURATE, and the CLI says so when it hasn't.
    """
    if not state.intent.cuisine or not candidate.cuisine_origin:
        return None
    target_group = _find_cuisine_group(state.intent.cuisine)
    candidate_group = _find_cuisine_group(candidate.cuisine_origin)
    if target_group and candidate_group and target_group != candidate_group:
        explore = state.intent.cuisine_stance == "explore"
        return ConflictFinding(
            severity=Severity.INFO if explore else Severity.SOFT,
            rule=PruneRule.CUISINE_DRIFT,
            reason=(
                f'"{candidate.name}" is {candidate.cuisine_origin} ({candidate_group}); '
                f'target is {state.intent.cuisine} ({target_group})'
            ),
        )
    return None


def check_functional_redundancy(
    candidate: Candidate, state: State,
) -> ConflictFinding | None:
    """SOFT: state.selected already has a same-role candidate within intensity ±2.

    Skipped for STACKABLE_ROLES (herbs, spices) where layering multiple is normal.
    Skipped if either side has no intensity (can't compare). A selected candidate is
    never compared with itself, so re-filtering a role after a pick keeps the pick.
    """
    if candidate.functional_role.lower() in STACKABLE_ROLES:
        return None
    if candidate.intensity is None:
        return None
    same_role_selected = [
        c for c in state.candidates
        if c.name in state.selected
        and c.functional_role.lower() == candidate.functional_role.lower()
        and c.name.lower() != candidate.name.lower()
    ]
    for existing in same_role_selected:
        if existing.intensity is None:
            continue
        if abs(existing.intensity - candidate.intensity) <= 2:
            return ConflictFinding(
                severity=Severity.SOFT,
                rule=PruneRule.FUNCTIONAL_REDUNDANCY,
                reason=(
                    f'"{candidate.name}" (intensity {candidate.intensity}) overlaps '
                    f'"{existing.name}" (intensity {existing.intensity}) at the same '
                    f'{candidate.functional_role} role'
                ),
            )
    return None


def check_technique_impossibility(
    candidate: Candidate, state: State,
) -> ConflictFinding | None:
    """SOFT: the candidate's own lead time (soak, cure, ferment, long simmer) exceeds
    state.intent.time_budget_min.

    Needs both numbers; with either missing it returns None and the agent reasons about
    timing in conversation. It compares one candidate against the whole budget, so it
    catches the impossible (overnight soak in a 30-minute dish), not a tight schedule
    built from several candidates.
    """
    budget = state.intent.time_budget_min
    prep = candidate.prep_time_min
    if budget is None or prep is None or prep <= budget:
        return None
    return ConflictFinding(
        severity=Severity.SOFT,
        rule=PruneRule.TECHNIQUE_IMPOSSIBILITY,
        reason=(
            f'"{candidate.name}" needs about {prep} min of prep; '
            f"the time budget is {budget} min"
        ),
    )


_ALL_RULES = [
    check_allergy,
    check_cuisine_drift,
    check_functional_redundancy,
    check_technique_impossibility,
]


# Drink siblings ---------------------------------------------------------------
#
# Everything below mirrors a structure above rather than extending it. The food rules never
# learn what a drink is and the drink rules never learn what a dish is; the only thing that
# knows the difference is _rules_for.


# Drink allergy alias map, HARD tier. Sibling of EXCLUSION_ALIASES. It names the exposures a
# bar has and the food map cannot see — the ones hiding behind a product name (orgeat, Baileys,
# Clamato, Worcestershire) rather than behind an ingredient word. The nut list leans
# conservative: traditional and most commercial orgeat, falernum, amaretto, nocino and creme de
# noyaux are almond- or stone-fruit-kernel derived, and on an allergen the conservative side of
# the judgment is the safe one.
#
# This map ADDS to the food one rather than replacing it (see DRINK_EXCLUSION_FOOD_OVERRIDES):
# a bar ingredient that is literally a food ingredient — clam juice, anchovy, bacon fat, miso —
# is still that food ingredient, and a drink session that dropped the food aliases would lose
# the HARD tier for every category this map happens not to list.
DRINK_EXCLUSION_ALIASES: dict[str, list[str]] = {
    "nuts": [
        "orgeat", "falernum", "amaretto", "disaronno", "frangelico", "nocino",
        "nocello", "noyaux", "noyau", "praline", "walnut liqueur", "hazelnut",
        "almond", "pistachio", "macadamia", "pecan", "cashew", "nux alpina",
        "peanut", "peanuts",
    ],
    "dairy": [
        "irish cream", "cream liqueur", "baileys", "milk punch", "horchata",
        "advocaat", "alexander", "grasshopper", "eggnog", "heavy cream",
        "half-and-half", "whipped cream", "dulce de leche", "rumchata",
        "amarula", "buttered", "butter-washed", "ghee-washed",
    ],
    "eggs": [
        "egg white", "egg yolk", "whole egg", "eggnog", "advocaat", "flip",
        "silver fizz", "golden fizz", "royal fizz", "ramos gin fizz", "syllabub",
    ],
    "gluten": [
        "beer", "ale", "lager", "stout", "porter", "hefeweizen", "barley wine",
        "malt liquor", "shandy", "michelada", "boilermaker", "ipa", "pilsner",
        "kvass", "barley malt", "malt extract", "malted milk",
    ],
    "shellfish": [
        "clamato", "clam juice", "clam broth", "bloody caesar", "caesar mix",
        "oyster shooter", "shrimp paste",
    ],
    "fish": ["worcestershire", "colatura", "garum", "fish sauce"],
    "beef": ["bullshot", "bull shot", "beef consomme", "beef consommé"],
}


# Exclusion categories where the food alias list must not be unioned into the HARD tier behind a
# bar. One entry, and it is the whole reason this constant exists rather than an unconditional
# union: the food gluten list is built from grains (wheat, barley, rye), which is the wrong unit
# for a bar. A grain is a gluten exposure; a spirit distilled from that grain is not one in the
# same way, and unioning the food list in would HARD-delete the entire whiskey category before
# the soft tier below ever ran. Every other category unions cleanly, because a clam is a clam in
# either medium.
#
# Deferred, not discarded. check_drink_allergy still consults the food list for these categories
# after the SOFT tier has had its turn, at SOFT severity, so a grain the soft tier does not claim
# as a spirit ("wheat flour", "seitan") is surfaced rather than passing in silence. HARD would be
# wrong here for the same reason the override exists, but silence was wrong too: those two names
# match no drink alias and no soft alias, so a gluten exclusion previously missed them entirely.
DRINK_EXCLUSION_FOOD_OVERRIDES: frozenset[str] = frozenset({"gluten"})


# Drink allergy alias map, SOFT tier. No food counterpart — this is the safety asymmetry the
# drink path needs. Distillation leaves the gluten protein behind in the wash, so a grain
# spirit is not a gluten exposure the way a beer is; but plenty of drinkers avoid grain spirits
# regardless, and a HARD rule would silently delete the entire whiskey category from a session
# without the user ever seeing it. Same logic for sulfites in wine-based aromatized products and
# for the drink names that merely imply an egg. Surfaced for the user to decide, never removed.
DRINK_EXCLUSION_SOFT_ALIASES: dict[str, list[str]] = {
    "gluten": [
        "whiskey", "whisky", "bourbon", "rye", "scotch", "single malt",
        "grain whisky", "wheat vodka", "grain vodka", "barley shochu",
        "mugi shochu", "genever", "korn", "baijiu",
    ],
    "eggs": ["sour", "fizz", "aquafaba"],
    "fish": ["bloody mary", "bloody maria", "red snapper", "caesar", "michelada"],
    "dairy": ["irish coffee"],
    "sulfites": [
        "wine", "vermouth", "sherry", "port", "madeira", "amontillado", "fino",
        "oloroso", "manzanilla", "prosecco", "champagne", "cava", "lillet",
        "cocchi", "quinquina", "sake", "cider", "maraschino cherry",
        "cocktail cherry", "dried fruit",
    ],
}


# Name-collision guard. These are false friends, not ambiguity: cream sherry is a sweetened
# oloroso, creme de cacao/menthe/cassis are dairy-free, cream of coconut is a coconut product,
# coconut is a drupe and nutmeg a seed, ginger beer and root beer are sodas that share a word
# with a brewed product without sharing its grain, a Prairie Oyster is a raw egg and no
# shellfish at all, Fish House Punch is named for a Philadelphia fishing club, and Beefeater is
# a gin. Flagging any of them would be noise on a true negative, and ginger beer in particular
# is a highball staple a highball session cannot afford to lose silently. Peanut is deliberately
# NOT exempt under nuts: it is botanically a legume rather than a tree nut, but that is not a
# distinction to draw silently on an allergen, so peanut and peanut-fat-washed spirits are HARD
# nut hits and the drinker is told which nut it is.
#
# An entry suppresses only the term whose collision it explains: it must appear in the candidate
# name AND contain the term that fired (see _is_false_friend). "ginger beer" therefore cancels
# "beer" and nothing else, so a coconut-cream orgeat is still caught on orgeat under a nut
# exclusion rather than being waved through by the word "coconut". A blanket per-category skip
# would silently drop the rest of the category's checks for that candidate, which on an allergen
# is the wrong direction to fail in.
DRINK_EXCLUSION_EXEMPT: dict[str, list[str]] = {
    "dairy": [
        "cream sherry", "cream soda", "creme de ", "creme d'", "cream ale",
        "coconut cream", "cream of coconut", "peanut butter",
    ],
    "nuts": ["coconut", "nutmeg", "cocoa", "creme de cacao"],
    "eggs": ["eggplant"],
    "gluten": [
        "ginger beer", "ginger ale", "root beer", "porter's gin",
        "gluten-free beer", "gluten-free ale", "gluten-free lager",
    ],
    "shellfish": ["prairie oyster", "oyster bay"],
    "fish": ["fish house punch"],
    "beef": ["beefeater"],
}


# Drink family groupings — same-group families share a template and compose comfortably.
# Sibling of CUISINE_GROUPS. Members are multi-word wherever a single word would swallow
# another family under the bidirectional matcher: bare "fizz" is out of Highball because it is
# a substring of silver/golden fizz in Flip & punch, and bare "punch" is out of every group
# because it is a substring of rum punch, milk punch and planter's punch across three of them.
DRINK_FAMILIES: dict[str, list[str]] = {
    "Spirit-forward": [
        "spirit-forward", "spirit forward", "stirred cocktail", "old fashioned",
        "manhattan", "martini", "martinez", "negroni", "boulevardier", "sazerac",
        "vieux carre", "rob roy", "hanky panky", "bijou", "improved whiskey cocktail",
    ],
    "Sour": [
        "sour", "daiquiri", "margarita", "sidecar", "gimlet", "bee's knees",
        "pisco sour", "last word", "paper plane", "corpse reviver", "jack rose",
        "aviation", "white lady", "clover club", "southside",
    ],
    "Highball": [
        "highball", "collins", "mojito", "cuba libre", "dark and stormy", "paloma",
        "gin and tonic", "americano", "spritz", "rickey", "gin fizz", "moscow mule",
        "buck", "presbyterian", "tall drink",
    ],
    "Tiki": [
        "tiki", "mai tai", "zombie", "jungle bird", "painkiller", "navy grog",
        "three dots and a dash", "fog cutter", "planter's punch", "rum punch",
        "swizzle", "hurricane", "saturn", "polynesian", "exotic cocktail",
    ],
    "Aperitivo & amaro": [
        "aperitivo", "amaro", "amari", "italian bitter", "vermouth cocktail",
        "bicicletta", "garibaldi", "milano-torino", "sbagliato", "bitter aperitif",
        "french aperitif", "low-abv bitter",
    ],
    "Champagne & wine": [
        "champagne cocktail", "wine cocktail", "sparkling cocktail", "french 75",
        "kir royale", "bellini", "mimosa", "death in the afternoon", "seelbach",
        "sherry cobbler", "bamboo", "adonis", "vermouth aperitif",
    ],
    "Flip & punch": [
        "flip", "eggnog", "nog", "brandy alexander", "grasshopper", "golden fizz",
        "silver fizz", "milk punch", "clarified milk punch", "syllabub",
        "fish house punch", "bowl punch", "batched punch", "posset", "wassail",
    ],
}


# Roles where stacking multiple candidates is normal — skip the intensity check. Sibling of
# STACKABLE_ROLES. base and modifier are here because the split base (two rums) and the double
# modifier are canonical construction rather than accidents, and stacked bitters are the
# defining move of the form. sweet, acid, dilution and texture stay single-slot.
DRINK_STACKABLE_ROLES: set[str] = {
    "base", "bases", "modifier", "modifiers",
    "bitter", "bitters", "aromatic", "aromatics",
}


# Bar-product classes. No food sibling — this is what lets the drink redundancy rule allow a
# split base while still catching two of the same bottle. Intensity alone cannot tell Jamaican
# pot-still rum from Demerara rum (a deliberate contrast) apart from Smith & Cross against
# Jamaican pot-still rum (the same product twice). Keep the syrup classes split: a single
# lumped "cane syrup" class wrongly collapses demerara syrup into rich simple syrup.
DRINK_PRODUCT_CLASSES: dict[str, list[str]] = {
    "dry vermouth": ["dry vermouth", "french vermouth", "dolin dry", "noilly prat"],
    "sweet vermouth": [
        "sweet vermouth", "italian vermouth", "rosso vermouth", "carpano antica",
        "punt e mes", "cocchi di torino",
    ],
    "orange liqueur": [
        "orange liqueur", "triple sec", "cointreau", "grand marnier", "curacao",
        "dry curacao", "combier", "orange curacao",
    ],
    "maraschino liqueur": ["maraschino", "luxardo maraschino"],
    "london dry gin": ["london dry", "london dry gin", "beefeater", "tanqueray"],
    "aromatic bitters": ["angostura", "aromatic bitters", "bogart bitters"],
    "orange bitters": ["orange bitters", "regans", "seville bitters"],
    "jamaican rum": ["jamaican rum", "jamaican pot-still", "pot-still rum", "smith & cross"],
    "demerara rum": ["demerara rum", "guyanese rum", "el dorado"],
    "agricole rhum": ["rhum agricole", "agricole", "cane juice rum"],
    "demerara syrup": ["demerara syrup", "demerara gum syrup", "turbinado syrup"],
    "cane syrup": ["cane syrup", "cane sugar syrup", "petite canne"],
    "simple syrup": ["simple syrup", "sugar syrup", "rich syrup", "1:1 syrup", "2:1 syrup"],
    "honey syrup": ["honey syrup", "honey water", "hot honey syrup"],
    "red bitter aperitivo": ["campari", "red bitter", "bitter aperitivo", "contratto bitter"],
}


def _find_drink_family(family: str) -> str | None:
    """Return the group containing the given drink family via case-insensitive substring.

    The two match directions are not equally trustworthy, so they are ranked rather than
    taken first-wins.

    A *naming* match — a member appears inside the query, "milk punch" in "hot milk punch" —
    means the query names that family, and the first one wins as before.

    A *fragment* match — the query appears inside a member, "punch" in "rum punch" — means the
    query is a bare word that several families happen to share. DRINK_FAMILIES deliberately
    withholds those bare words from every group for this reason, but first-wins defeated that:
    "punch" is a fragment of Tiki's rum punch AND of Flip & punch's milk punch, and whichever
    group iterated first silently claimed it. A fragment is therefore only honored when it
    lands in exactly one group; when it straddles groups the honest answer is None, which is
    the same silent no-claim the matcher already gives an unclassifiable string.
    """
    if not family:
        return None
    family_lower = family.lower()
    named: list[str] = []
    fragments: set[str] = set()
    for group, members in DRINK_FAMILIES.items():
        for member in members:
            if member in family_lower:
                named.append(group)
            elif family_lower in member:
                fragments.add(group)
    if named:
        return named[0]
    if len(fragments) == 1:
        return next(iter(fragments))
    return None


def _find_product_class(name: str) -> str | None:
    """Return the bar-product class for an ingredient name, or None if unclassified.

    One-directional substring on purpose: classes are matched against long product names
    ("Smith & Cross Jamaican pot-still rum"), so the reverse direction _find_cuisine_group
    allows would only buy false positives here.
    """
    if not name:
        return None
    name_lower = name.lower()
    for product_class, members in DRINK_PRODUCT_CLASSES.items():
        for member in members:
            if member in name_lower:
                return product_class
    return None


@cache
def _alias_pattern(alias: str) -> re.Pattern[str]:
    """Compile a whole-word matcher for one alias. Cached; the alias maps are static."""
    return re.compile(rf"(?<!\w){re.escape(alias)}(?!\w)")


def _alias_matches(alias: str, name_lower: str) -> bool:
    """Whole-word containment, not bare substring.

    Bar products are named after places, people and brands, and short aliases collide with
    them constantly: "ale" appears inside Salers, Alessio and Aleppo, "cod" inside Código,
    "beef" inside Beefeater, "ham" inside Hamilton. A substring test HARD-deletes those, and a
    HARD finding never reaches the user (filter_candidates_for_role keeps it out of
    `compatible`), so the failure is silent. Requiring a word boundary on both sides keeps
    "pale ale" and "ginger beer" matching while none of the collisions above do.

    The cost is that inflected forms no longer match a stem, so any that matter are listed
    outright — "buttered" alongside the food map's "butter" — which suits maps that are
    hand-curated bar knowledge anyway.
    """
    return _alias_pattern(alias).search(name_lower) is not None


def _is_false_friend(term: str, name_lower: str, exclusion: str) -> bool:
    """True if a declared collision in DRINK_EXCLUSION_EXEMPT explains this exact hit.

    Scoped two ways: the exempt phrase must be present in the candidate name, and it must
    contain the term that fired. "ginger beer" cancels "beer" in "Fever-Tree ginger beer" and
    leaves every other check on that candidate running.

    The food map's ALLERGEN_FALSE_FRIENDS are honored too, keyed on the term that fired, since
    the HARD tier unions the food aliases in: "milk" must not block coconut or oat milk behind
    a bar any more than in a kitchen. Per term, so "almond milk" still trips a nut exclusion.
    """
    if any(friend in name_lower for friend in ALLERGEN_FALSE_FRIENDS.get(term, [])):
        return True
    return any(
        phrase in name_lower and term in phrase
        for phrase in DRINK_EXCLUSION_EXEMPT.get(exclusion, [])
    )


def _drink_hard_aliases(exclusion: str) -> list[str]:
    """The HARD alias list for one exclusion: the drink map, then the food map behind it.

    The food map is skipped only for the categories in DRINK_EXCLUSION_FOOD_OVERRIDES. For
    everything else the union is what makes the drink HARD tier a superset of the food one, so
    switching a session to `medium: drink` can never lose an allergen the food path caught.
    """
    aliases = list(DRINK_EXCLUSION_ALIASES.get(exclusion, []))
    if exclusion in DRINK_EXCLUSION_FOOD_OVERRIDES:
        # Withheld here so the SOFT tier can claim distilled spirits first. check_drink_allergy
        # falls back to EXCLUSION_ALIASES for these categories once it has, at SOFT severity, so
        # the food list is deferred rather than dropped.
        return aliases
    aliases.extend(a for a in EXCLUSION_ALIASES.get(exclusion, []) if a not in aliases)
    return aliases


def check_drink_allergy(candidate: Candidate, state: State) -> ConflictFinding | None:
    """HARD/SOFT: candidate name matches an exclusion, an alias, or an ambiguous path.

    Sibling of check_allergy, with three tiers evaluated in a load-bearing order per
    exclusion: HARD alias (drink map plus the food map behind it), direct substring on the
    exclusion term itself, then SOFT alias. Aliases are checked before the direct term (food
    checks them after) so specific beats generic and the SOFT tier stays reachable. Every tier
    is guarded by the false-friend check, and alias matching is whole-word.

    Across exclusions, severity decides which single finding is returned, not list order. The
    food sibling can return on its first hit because every food finding is HARD; here a SOFT
    hit on an earlier exclusion would otherwise mask a HARD hit on a later one, and a bacon-fat
    washed bourbon under ``["gluten", "pork"]`` would come back merely soft-flagged.
    """
    if not state.intent.exclusions:
        return None
    name_lower = candidate.name.lower()
    soft_finding: ConflictFinding | None = None
    for exclusion in state.intent.exclusions:
        ex_lower = exclusion.lower()
        for alias in _drink_hard_aliases(ex_lower):
            if _alias_matches(alias, name_lower) and not _is_false_friend(
                alias, name_lower, ex_lower,
            ):
                return ConflictFinding(
                    severity=Severity.HARD,
                    rule=DrinkPruneRule.DRINK_ALLERGY_HARD_FILTER,
                    reason=f'"{candidate.name}" is a {exclusion} ingredient ({alias})',
                )
        if (ex_lower in name_lower or name_lower in ex_lower) and not _is_false_friend(
            ex_lower, name_lower, ex_lower,
        ):
            return ConflictFinding(
                severity=Severity.HARD,
                rule=DrinkPruneRule.DRINK_ALLERGY_HARD_FILTER,
                reason=f'matches exclusion "{exclusion}"',
            )
        soft_alias = next(
            (
                alias
                for alias in DRINK_EXCLUSION_SOFT_ALIASES.get(ex_lower, [])
                if _alias_matches(alias, name_lower)
                and not _is_false_friend(alias, name_lower, ex_lower)
            ),
            None,
        )
        # An override category withheld its food aliases from the HARD tier above so a grain term
        # could not delete the whole distilled-spirit category before the SOFT tier ran. Consult
        # that list here, once the SOFT tier has had its turn, at SOFT severity: a grain word
        # behind a bar is genuinely ambiguous, so promoting it to HARD would delete rye whiskey
        # on the word "rye" — the exact failure the override exists to prevent. But leaving it
        # unexamined is the other failure: "wheat flour" and "seitan" match no drink alias and no
        # soft alias, so before this fallback they passed a gluten exclusion in complete silence.
        # Deferred, not discarded. Surfacing beats both deleting and ignoring.
        if soft_alias is None and ex_lower in DRINK_EXCLUSION_FOOD_OVERRIDES:
            soft_alias = next(
                (
                    alias
                    for alias in EXCLUSION_ALIASES.get(ex_lower, [])
                    if _alias_matches(alias, name_lower)
                    and not _is_false_friend(alias, name_lower, ex_lower)
                ),
                None,
            )
        if soft_alias is not None and soft_finding is None:
            soft_finding = ConflictFinding(
                severity=Severity.SOFT,
                rule=DrinkPruneRule.DRINK_ALLERGY_SOFT_FLAG,
                reason=(
                    f'"{candidate.name}" ({soft_alias}) is an ambiguous {exclusion} path — '
                    f'surfaced for the user to decide, never silently removed'
                ),
            )
    return soft_finding


def check_family_drift(candidate: Candidate, state: State) -> ConflictFinding | None:
    """candidate.cuisine_origin is in a different group than intent.drink.drink_family.

    Sibling of check_cuisine_drift. For a drink session cuisine_origin carries a DRINK_FAMILIES
    string; components that belong to no family (syrups, citrus, ice) leave it empty and the
    rule stays silent on them, exactly as the food rule does for an unclassified origin.

    Severity follows intent.drink.family_stance the way the food rule follows cuisine_stance:
    SOFT under tradition or an unset stance, INFO (offered with a note) under explore.
    """
    drink = state.intent.drink
    target = drink.drink_family if drink else None
    if not target or not candidate.cuisine_origin:
        return None
    target_group = _find_drink_family(target)
    candidate_group = _find_drink_family(candidate.cuisine_origin)
    if target_group and candidate_group and target_group != candidate_group:
        explore = drink.family_stance == "explore"
        return ConflictFinding(
            severity=Severity.INFO if explore else Severity.SOFT,
            rule=DrinkPruneRule.FAMILY_DRIFT,
            reason=(
                f'"{candidate.name}" is {candidate.cuisine_origin} ({candidate_group}); '
                f'target is {target} ({target_group})'
            ),
        )
    return None


def check_drink_redundancy(candidate: Candidate, state: State) -> ConflictFinding | None:
    """SOFT: state.selected already has a same-role candidate of the same bar-product class.

    Sibling of check_functional_redundancy, keyed on product class first and intensity second.
    The class check runs unconditionally, so two dry vermouths are caught even inside a
    stackable role; stackability only governs the intensity fallback, which is what lets a
    split base and stacked bitters through while single-slot roles (sweet, acid, dilution,
    texture) still fall back to the food-style intensity ±2 comparison.

    One deliberate divergence from the food sibling: candidates are compared against selected
    peers other than themselves. The food rule hides that case behind its intensity
    requirement; the unconditional class check would otherwise match a candidate to itself.
    """
    role_lower = candidate.functional_role.lower()
    same_role_selected = [
        c for c in state.candidates
        if c.name in state.selected
        and c.name != candidate.name
        and c.functional_role.lower() == role_lower
    ]
    candidate_class = _find_product_class(candidate.name)
    if candidate_class is not None:
        for existing in same_role_selected:
            if _find_product_class(existing.name) == candidate_class:
                return ConflictFinding(
                    severity=Severity.SOFT,
                    rule=DrinkPruneRule.DRINK_FUNCTIONAL_REDUNDANCY,
                    reason=(
                        f'"{candidate.name}" and "{existing.name}" are both {candidate_class} '
                        f'at the same {candidate.functional_role} role'
                    ),
                )
    if role_lower in DRINK_STACKABLE_ROLES:
        return None
    if candidate.intensity is None:
        return None
    for existing in same_role_selected:
        if existing.intensity is None:
            continue
        if abs(existing.intensity - candidate.intensity) <= 2:
            return ConflictFinding(
                severity=Severity.SOFT,
                rule=DrinkPruneRule.DRINK_FUNCTIONAL_REDUNDANCY,
                reason=(
                    f'"{candidate.name}" (intensity {candidate.intensity}) overlaps '
                    f'"{existing.name}" (intensity {existing.intensity}) at the same '
                    f'{candidate.functional_role} role'
                ),
            )
    return None


def check_build_impossibility(
    candidate: Candidate, state: State,  # noqa: ARG001
) -> ConflictFinding | None:
    """SOFT: v1 stub sibling of check_technique_impossibility. Returns None.

    v2 will check the candidate against state.intent.drink.build_method: an egg white cannot
    be stirred, and a carbonated build cannot take a fresh-citrus component without
    pre-clarification. For v1, the agent reasons about the build in conversation rather than
    via a programmatic check.
    """
    return None


_ALL_DRINK_RULES = [
    check_drink_allergy,
    check_family_drift,
    check_drink_redundancy,
    check_build_impossibility,
]


def _rules_for(state: State) -> list:
    """The single medium dispatch point. Food rule bodies are never branched."""
    if state.intent.medium == "drink":
        return _ALL_DRINK_RULES
    return _ALL_RULES


def check_candidate(candidate: Candidate, state: State) -> list[ConflictFinding]:
    """Run the medium's rules against the candidate; return its findings (may be empty).

    Hard rules win: if one fires, only hard findings come back. A blocked candidate is
    out, so a soft flag on it would only invite an override the user can't make. Severity
    is read off each finding rather than off the rule, because check_drink_allergy can
    return either.
    """
    findings = [f for rule_fn in _rules_for(state) if (f := rule_fn(candidate, state))]
    hard = [f for f in findings if f.severity == Severity.HARD]
    return hard or findings


def classify_candidate(
    candidate: Candidate, state: State,
) -> tuple[Verdict, list[ConflictFinding]]:
    """Return the one bucket the candidate belongs in, with the findings behind it."""
    findings = check_candidate(candidate, state)
    severities = {f.severity for f in findings}
    if Severity.HARD in severities:
        return Verdict.EXCLUDED, findings
    if Severity.SOFT in severities:
        return Verdict.WOULD_PRUNE, findings
    return Verdict.COMPATIBLE, findings


class RoleFilter(BaseModel):
    """A role's candidates, each in exactly one of compatible / would_prune / excluded.

    compatible:  offered to the user. May carry INFO notes (drift under explore).
    would_prune: SOFT prunes, kept out of the offered pool. The user can ask to see them
                 or override one; keep the entry in state.pruned with overridden: true.
    excluded:    HARD prunes (allergy). Never shown, never overridable, but logged with
                 the reason so state.pruned can record them.
    notes:       INFO findings (drift under explore) on compatible or would_prune
                 candidates, for the agent to mention. Never a reason to prune.
    """

    model_config = ConfigDict(extra="forbid")

    compatible: list[Candidate] = []
    would_prune: list[PrunedItem] = []
    excluded: list[PrunedItem] = []
    notes: list[PrunedItem] = []


def filter_candidates_for_role(role: str, state: State) -> RoleFilter:
    """Sort state.candidates matching ``role`` into a RoleFilter, preserving order."""
    role_lower = role.lower()
    result = RoleFilter()
    for candidate in state.candidates:
        if candidate.functional_role.lower() != role_lower:
            continue
        verdict, findings = classify_candidate(candidate, state)
        items = {
            severity: [
                PrunedItem(name=candidate.name, rule=f.rule, reason=f.reason)
                for f in findings if f.severity == severity
            ]
            for severity in Severity
        }
        if verdict == Verdict.EXCLUDED:
            result.excluded.extend(items[Severity.HARD])
        elif verdict == Verdict.WOULD_PRUNE:
            result.would_prune.extend(items[Severity.SOFT])
        else:
            result.compatible.append(candidate)
        result.notes.extend(items[Severity.INFO])
    return result


_STANCE_UNSET_WARNING = (
    "intent.cuisine_stance is unset, so cuisine_drift is gated as under tradition. "
    "Ask tradition or explore before CURATE."
)
_FAMILY_STANCE_UNSET_WARNING = (
    "intent.drink.family_stance is unset, so family_drift is gated as under tradition. "
    "Ask tradition or explore before CURATE."
)


def _stance_output(state: State) -> dict:
    """The stance key for the session's medium, plus a warning when it is unset."""
    if state.intent.medium == "drink":
        stance = state.intent.drink.family_stance if state.intent.drink else None
        output: dict = {"family_stance": stance}
        warning = _FAMILY_STANCE_UNSET_WARNING
    else:
        stance = state.intent.cuisine_stance
        output = {"cuisine_stance": stance}
        warning = _STANCE_UNSET_WARNING
    if stance is None:
        output["warning"] = warning
    return output


# CLI -------------------------------------------------------------------------


def _cli_filter(args: argparse.Namespace) -> int:
    state = State.load_yaml(Path(args.state))
    stance = _stance_output(state)
    warning = stance.pop("warning", None)
    output: dict = {
        **stance,
        **filter_candidates_for_role(args.role, state).model_dump(mode="json"),
    }
    if warning:
        output["warning"] = warning
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


def _cli_check(args: argparse.Namespace) -> int:
    state = State.load_yaml(Path(args.state))
    candidate = Candidate.model_validate(json.loads(args.candidate))
    verdict, findings = classify_candidate(candidate, state)
    output: dict = {
        "candidate": candidate.model_dump(mode="json"),
        "verdict": verdict.value,
        "findings": [f.model_dump(mode="json") for f in findings],
    }
    if warning := _stance_output(state).get("warning"):
        output["warning"] = warning
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mise_en_prompt.conflicts")
    sub = parser.add_subparsers(dest="cmd", required=True)

    filter_p = sub.add_parser("filter", help="Filter state.candidates for a role.")
    filter_p.add_argument("--role", required=True, help="Functional role (heat, acid, ...).")
    filter_p.add_argument("--state", required=True, help="Path to state.yaml.")
    filter_p.set_defaults(func=_cli_filter)

    check_p = sub.add_parser("check", help="Check a single candidate for conflicts.")
    check_p.add_argument(
        "--candidate", required=True,
        help='JSON object: {"name":..., "cuisine_origin":..., "functional_role":..., ...}',
    )
    check_p.add_argument("--state", required=True, help="Path to state.yaml.")
    check_p.set_defaults(func=_cli_check)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
