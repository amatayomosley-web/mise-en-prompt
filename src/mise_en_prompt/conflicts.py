"""Conflict detection rules for ingredient candidates.

Four rules:
  - check_allergy (HARD)            — candidate matches a state.intent.exclusions term
  - check_cuisine_drift (SOFT, or INFO under cuisine_stance=explore)
                                    — candidate's cuisine_origin is in a different group than the dish
  - check_functional_redundancy (SOFT) — same role + close intensity already in state.selected
  - check_technique_impossibility (SOFT) — candidate.prep_time_min exceeds intent.time_budget_min

check_candidate runs them, with HARD taking precedence: an allergy-blocked candidate
reports only its hard finding. classify_candidate turns findings into exactly one
Verdict, and filter_candidates_for_role sorts a role's candidates into the matching
buckets (compatible, would_prune, excluded) used by the chef agent during CURATE.

Hooks call this module to verify the agent's pruning decisions; the agent calls the CLI
between AskUserQuestion prompts to compute the eligible pool for each functional role.
"""
from __future__ import annotations

import argparse
import json
import sys
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from mise_en_prompt.state import (
    Candidate,
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
    rule: PruneRule
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


_HARD_RULES = [check_allergy]
_SOFT_RULES = [
    check_cuisine_drift,
    check_functional_redundancy,
    check_technique_impossibility,
]


def check_candidate(candidate: Candidate, state: State) -> list[ConflictFinding]:
    """Run the rules against the candidate; return its findings (may be empty).

    Hard rules win: if one fires, only hard findings come back. A blocked candidate is
    out, so a soft flag on it would only invite an override the user can't make.
    """
    hard = [f for rule_fn in _HARD_RULES if (f := rule_fn(candidate, state))]
    if hard:
        return hard
    return [f for rule_fn in _SOFT_RULES if (f := rule_fn(candidate, state))]


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
                 or override one; record an override in state.pruned for the audit trail.
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


# CLI -------------------------------------------------------------------------


def _cli_filter(args: argparse.Namespace) -> int:
    state = State.load_yaml(Path(args.state))
    output: dict = {
        "cuisine_stance": state.intent.cuisine_stance,
        **filter_candidates_for_role(args.role, state).model_dump(mode="json"),
    }
    if state.intent.cuisine_stance is None:
        output["warning"] = _STANCE_UNSET_WARNING
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
    if state.intent.cuisine_stance is None:
        output["warning"] = _STANCE_UNSET_WARNING
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
