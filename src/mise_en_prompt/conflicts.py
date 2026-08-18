"""Conflict detection rules for ingredient candidates.

Four rules:
  - check_allergy (HARD)            — candidate matches a state.intent.exclusions term
  - check_cuisine_drift (SOFT)      — candidate's cuisine_origin is in a different group than the dish
  - check_functional_redundancy (SOFT) — same role + close intensity already in state.selected
  - check_technique_impossibility (SOFT) — v1 stub, returns None

The aggregator check_candidate runs all four. filter_candidates_for_role returns the
(compatible, would_prune) split used by the chef agent during CURATE.

Hooks call this module to verify the agent's pruning decisions; the agent calls the CLI
between AskUserQuestion prompts to compute the eligible pool for each functional role.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from mise_en_prompt.state import (
    Candidate,
    PruneRule,
    PrunedItem,
    Severity,
    State,
)

__all__ = [
    "CUISINE_ADJACENCY",
    "ConflictFinding",
    "Severity",
    "check_allergy",
    "check_candidate",
    "check_cuisine_drift",
    "check_functional_redundancy",
    "check_technique_impossibility",
    "filter_candidates_for_role",
]


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


# Group pairs with enough historical culinary exchange that crossing them is a note,
# not a warning. CUISINE_GROUPS is a partition, but real cuisines are not partitioned:
# chili con carne is genuinely both Latin American and North American, and no single
# group value is correct for it. Rather than forcing a dish to pick one group (or
# widening Intent.cuisine to a set, which every consumer would then have to handle),
# adjacency makes drift a function of *distance* between groups instead of mere
# inequality. Adjacent crossings report INFO; distant ones report SOFT.
#
# Kept deliberately short. If everything is adjacent to everything, the signal is gone.
_ADJACENT_GROUP_PAIRS: tuple[tuple[str, str], ...] = (
    ("Latin American", "North American"),      # Tex-Mex, Cal-Mex, Southwestern, Creole
    ("Latin American", "European"),            # Columbian exchange; Iberian colonization
    ("Latin American", "Sub-Saharan African"), # transatlantic: okra, rice, black-eyed peas
    ("North American", "European"),            # settler cuisine; most US canon is European-derived
    ("European", "Middle Eastern"),            # the Mediterranean basin is one food world
    ("Middle Eastern", "South Asian"),         # Persian-Mughal exchange
    ("Middle Eastern", "Sub-Saharan African"), # trans-Saharan trade; the North African bridge
    ("South Asian", "East Asian"),             # Buddhist trade routes; curry dispersal
)

CUISINE_ADJACENCY: dict[str, frozenset[str]] = {
    group: frozenset(
        other
        for pair in _ADJACENT_GROUP_PAIRS
        for other in pair
        if group in pair and other != group
    )
    for group in CUISINE_GROUPS
}


def _groups_are_adjacent(one: str, other: str) -> bool:
    """True if crossing between these two groups is a note rather than a warning."""
    return other in CUISINE_ADJACENCY.get(one, frozenset())


# Roles where stacking multiple candidates is normal — skip redundancy check.
STACKABLE_ROLES: set[str] = {
    "aromatic_herb", "aromatic_herbs", "spice", "spices", "aromatic", "aromatics",
}


def _find_cuisine_group(cuisine: str) -> str | None:
    """Return the group containing the given cuisine.

    Resolution order, most specific first:

    1. Exact match against a group name or one of its members.
    2. Longest group name or member that appears *inside* the query, so
       "Central American Stew" resolves on "central american" rather than on the
       shorter "american" it also contains.

    A query shorter than a member no longer matches it. That direction
    (``cuisine_lower in member``) previously made "American" resolve to Latin
    American, because "american" is a substring of "central american" and dict
    iteration reaches Latin American first — a silent false negative that let a
    Mexican candidate pass clean in an American dish. Returning None is better
    than misrouting.
    """
    if not cuisine:
        return None
    cuisine_lower = cuisine.lower().strip()

    for group, members in CUISINE_GROUPS.items():
        if cuisine_lower == group.lower() or cuisine_lower in members:
            return group

    best_group: str | None = None
    best_len = 0
    for group, members in CUISINE_GROUPS.items():
        for token in (group.lower(), *members):
            if token in cuisine_lower and len(token) > best_len:
                best_group, best_len = group, len(token)
    return best_group


def check_allergy(candidate: Candidate, state: State) -> ConflictFinding | None:
    """HARD: candidate name (or alias for a category exclusion) matches an exclusion."""
    if not state.intent.exclusions:
        return None
    name_lower = candidate.name.lower()
    for exclusion in state.intent.exclusions:
        ex_lower = exclusion.lower()
        if ex_lower in name_lower or name_lower in ex_lower:
            return ConflictFinding(
                severity=Severity.HARD,
                rule=PruneRule.ALLERGY_HARD_FILTER,
                reason=f'matches exclusion "{exclusion}"',
            )
        for alias in EXCLUSION_ALIASES.get(ex_lower, []):
            if alias in name_lower:
                return ConflictFinding(
                    severity=Severity.HARD,
                    rule=PruneRule.ALLERGY_HARD_FILTER,
                    reason=f'"{candidate.name}" is a {exclusion} ingredient ({alias})',
                )
    return None


def check_cuisine_drift(candidate: Candidate, state: State) -> ConflictFinding | None:
    """SOFT: candidate.cuisine_origin is in a different group than state.intent.cuisine."""
    if not state.intent.cuisine or not candidate.cuisine_origin:
        return None
    target_group = _find_cuisine_group(state.intent.cuisine)
    candidate_group = _find_cuisine_group(candidate.cuisine_origin)
    if target_group and candidate_group and target_group != candidate_group:
        exploring = state.intent.cuisine_stance == "explore"
        adjacent = _groups_are_adjacent(target_group, candidate_group)
        reason = (
            f'"{candidate.name}" is {candidate.cuisine_origin} ({candidate_group}); '
            f'target is {state.intent.cuisine} ({target_group})'
        )
        if adjacent:
            reason += " — adjacent groups, long history of exchange"
        if exploring:
            reason += " — informational only, cuisine_stance is explore"
        return ConflictFinding(
            severity=Severity.INFO if (exploring or adjacent) else Severity.SOFT,
            rule=PruneRule.CUISINE_DRIFT,
            reason=reason,
        )
    return None


def check_functional_redundancy(
    candidate: Candidate, state: State,
) -> ConflictFinding | None:
    """SOFT: state.selected already has a same-role candidate within intensity ±2.

    Skipped for STACKABLE_ROLES (herbs, spices) where layering multiple is normal.
    Skipped if either side has no intensity (can't compare).
    """
    if candidate.functional_role.lower() in STACKABLE_ROLES:
        return None
    if candidate.intensity is None:
        return None
    same_role_selected = [
        c for c in state.candidates
        if c.name in state.selected
        and c.functional_role.lower() == candidate.functional_role.lower()
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
    candidate: Candidate, state: State,  # noqa: ARG001
) -> ConflictFinding | None:
    """SOFT: v1 stub. Returns None.

    v2 will check candidate.prep_time_min (when added to schema) against
    state.intent.time_budget_min. For v1, the agent reasons about timing in
    conversation rather than via a programmatic check.
    """
    return None


_ALL_RULES = [
    check_allergy,
    check_cuisine_drift,
    check_functional_redundancy,
    check_technique_impossibility,
]


def check_candidate(candidate: Candidate, state: State) -> list[ConflictFinding]:
    """Run every rule against the candidate; return all findings (may be empty)."""
    findings: list[ConflictFinding] = []
    for rule_fn in _ALL_RULES:
        finding = rule_fn(candidate, state)
        if finding is not None:
            findings.append(finding)
    return findings


def filter_candidates_for_role(
    role: str, state: State,
) -> tuple[list[Candidate], list[PrunedItem]]:
    """Split state.candidates matching `role` into (compatible, would_prune).

    compatible: ordered candidates with no HARD findings. SOFT findings still allow
                inclusion — the chef agent surfaces those in the conflict-resolution
                AskUserQuestion prompt so the user can override or accept.
    would_prune: PrunedItems for every finding, carrying the severity that fired.
                 HARD ones are silently excluded from compatible (the agent never
                 displays them). SOFT and INFO ones appear in compatible AND here,
                 so the agent can tell the user "this one would drift cuisine"
                 before they pick it. Read ``severity`` to tell a warning the user
                 must resolve (SOFT) from an awareness note (INFO).
    """
    role_lower = role.lower()
    compatible: list[Candidate] = []
    would_prune: list[PrunedItem] = []
    for candidate in state.candidates:
        if candidate.functional_role.lower() != role_lower:
            continue
        findings = check_candidate(candidate, state)
        hard_findings = [f for f in findings if f.severity == Severity.HARD]
        advisory_findings = [f for f in findings if f.severity != Severity.HARD]
        if hard_findings:
            for finding in hard_findings:
                would_prune.append(
                    PrunedItem(
                        name=candidate.name,
                        rule=finding.rule,
                        reason=finding.reason,
                        severity=finding.severity,
                    )
                )
            continue
        compatible.append(candidate)
        for finding in advisory_findings:
            would_prune.append(
                PrunedItem(
                    name=candidate.name,
                    rule=finding.rule,
                    reason=finding.reason,
                    severity=finding.severity,
                )
            )
    return compatible, would_prune


# CLI -------------------------------------------------------------------------


def _cli_filter(args: argparse.Namespace) -> int:
    state = State.load_yaml(Path(args.state))
    compatible, would_prune = filter_candidates_for_role(args.role, state)
    output = {
        "compatible": [c.model_dump(mode="json") for c in compatible],
        "would_prune": [p.model_dump(mode="json") for p in would_prune],
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


def _cli_check(args: argparse.Namespace) -> int:
    state = State.load_yaml(Path(args.state))
    candidate = Candidate.model_validate(json.loads(args.candidate))
    findings = check_candidate(candidate, state)
    output = {
        "candidate": candidate.model_dump(mode="json"),
        "findings": [f.model_dump(mode="json") for f in findings],
    }
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
