"""Session state schema for the chef agent.

The agent persists state to ``sessions/<session-id>/state.yaml`` between turns. This module
defines the typed shape of that state, the round-trip serializer, and the constrained
enums that downstream tooling (conflicts, hooks, renderer) reads.

Schema is the primary architectural artifact for this project: hooks enforce phase
progression by reading State.phase, conflict rules read State.candidates and State.intent,
and the renderer composes recipe.md from State.selected and State.research_log.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Annotated, Any, Literal, get_args

import yaml
from pydantic import BaseModel, ConfigDict, Discriminator, Field, Tag, model_validator


class Phase(str, Enum):
    """The eight sequential phases of a chef-agent session.

    ENHANCE sits between SYNTHESIZE (recipe drafted internally) and GUIDE (recipe written
    to disk). It runs the deconstruction + elevation pass: walks the draft move-by-move,
    classifies each technique and ingredient under physics + flavor lenses, and writes
    the structured analysis to State.enhancements so GUIDE can render the operational
    recipe above the line and the deconstruction/variants below it.
    """

    INTAKE = "INTAKE"
    CLARIFY = "CLARIFY"
    GROUNDING = "GROUNDING"
    RESEARCH = "RESEARCH"
    CURATE = "CURATE"
    SYNTHESIZE = "SYNTHESIZE"
    ENHANCE = "ENHANCE"
    GUIDE = "GUIDE"


class PruneRule(str, Enum):
    """Why a candidate ingredient was removed during CURATE."""

    CUISINE_DRIFT = "cuisine_drift"
    FUNCTIONAL_REDUNDANCY = "functional_redundancy"
    ALLERGY_HARD_FILTER = "allergy_hard_filter"
    TECHNIQUE_IMPOSSIBILITY = "technique_impossibility"


class DrinkPruneRule(str, Enum):
    """Why a candidate drink component was removed during CURATE.

    Sibling of PruneRule. Drinks get their own rule vocabulary so the audit trail in
    State.pruned never labels a drink decision with a food-named rule.

    DRINK_ALLERGY_SOFT_FLAG has no food counterpart: food allergy filtering is HARD-only,
    but a distilled grain spirit is not a gluten exposure the way beer is, so the drink
    path surfaces those for the user to judge instead of silently deleting them.
    """

    FAMILY_DRIFT = "family_drift"
    DRINK_FUNCTIONAL_REDUNDANCY = "drink_functional_redundancy"
    DRINK_ALLERGY_HARD_FILTER = "drink_allergy_hard_filter"
    DRINK_ALLERGY_SOFT_FLAG = "drink_allergy_soft_flag"
    BUILD_IMPOSSIBILITY = "build_impossibility"


Medium = Literal["dish", "drink"]
"""Whether this session is designing a dish or a drink. Absent means ``dish``.

The single value the conflict dispatcher and the hook's ordering dispatcher read to
decide which family of rules applies. Legacy state.yaml files predate the field and
default to ``dish``, so they route exactly as they did before drinks existed."""


ResearchTag = Literal[
    "aromatic_base",
    "functional_role",
    "candidate",
    "pairing",
    "technique",
]
"""Ordered research tags. Hooks enforce that searches happen in this order:
aromatic_base -> functional_role -> candidate -> pairing/technique."""


DrinkResearchTag = Literal[
    "base_spirit",
    "drink_role",
    "drink_candidate",
    "drink_pairing",
    "build_method",
    "dilution_math",
]
"""Ordered drink research tags. Hooks enforce that searches happen in this order:
base_spirit -> drink_role -> drink_candidate -> drink_pairing, and
build_method -> dilution_math (you cannot compute dilution before you know whether the
drink is stirred, shaken, or built)."""


RESEARCH_TAGS: frozenset[str] = frozenset(get_args(ResearchTag))
DRINK_RESEARCH_TAGS: frozenset[str] = frozenset(get_args(DrinkResearchTag))
"""The two tag vocabularies as sets, derived from the Literals rather than restated.

State validates that a session's research_log only uses the vocabulary its medium owns, and
the hook's precursor tables are keyed by the same strings. Widening ResearchLogEntry.tag to
accept both vocabularies is what lets one model serve both media; it is these sets that keep
a dish session from labelling an entry with a drink tag the food precursor table has never
heard of (and would therefore wave through unordered)."""


HeatLevel = Literal["mild", "medium", "spicy", "very_spicy"]


StrengthLevel = Literal["low_abv", "sessionable", "standard", "spirit_forward", "overproof"]
"""How hard the finished drink hits. First half of the HeatLevel analog — the intensity
axis a drinker actually dials, and the one that constrains base-spirit proof and the
stirred/shaken decision downstream."""


SweetnessLevel = Literal["bone_dry", "dry", "off_dry", "balanced", "sweet", "dessert"]
"""How sweet the finished drink reads. Second half of the HeatLevel analog. Food gets one
intensity axis; drinks need two, because strength and sweetness move independently — a
spirit-forward drink can be bone dry (Martini) or sweet (Vieux Carré)."""


BuildMethod = Literal[
    "built",
    "stirred",
    "shaken",
    "dry_shaken",
    "thrown",
    "swizzled",
    "blended",
    "flash_blended",
    "carbonated",
    "clarified",
]
"""How the drink is assembled and chilled. Not a stylistic label: the method sets water
pickup, aeration, and final temperature, so it has to be known before dilution can be
computed at all."""


ServiceFormat = Literal["single", "batched", "bottled", "punch_bowl", "on_tap"]
"""Whether the spec is built one at a time or scaled ahead. Batched, bottled, and on-tap
formats carry pre-dilution — water that would otherwise arrive from ice at service must be
added by measure instead, so the format changes the arithmetic, not just the volume."""


CuisineStance = Literal["tradition", "explore"]
"""How the user wants the chef to relate to the named cuisine.

- ``tradition``: stay within the cuisine's canon. ``cuisine_drift`` soft conflicts in
  CURATE fire as warnings the user must override case-by-case. Cross-cuisine flavor
  identity moves (soy sauce in Provençal, gochujang in Veracruz) are filtered out.
- ``explore``: the cuisine is a starting point, not a definition. ``cuisine_drift``
  becomes informational rather than gating. Cross-cuisine moves are surfaced when
  food science says they enhance the dish — the agent's job is the best version of
  the dish, not the most canonical one.

Asked in CLARIFY before CURATE so role-by-role candidate surfacing and Step-5 vector
filtering both respect the stance from the first prompt onward."""


FamilyStance = Literal["tradition", "explore"]
"""How the user wants the chef to relate to the named drink family.

- ``tradition``: stay on the canonical spec. ``family_drift`` soft conflicts in CURATE
  fire as warnings the user must override case-by-case. Components that belong to a
  different family's grammar (falernum in a Manhattan, Campari in a tiki build) are
  filtered out.
- ``explore``: the family is a starting point, not a definition. ``family_drift`` becomes
  informational rather than gating. Cross-family moves are surfaced when the drink is
  better for them — the agent's job is the best version of the drink, not the most
  canonical one.

Sibling of CuisineStance. Structurally identical, named separately so a drink session's
audit trail never reads as a cuisine decision."""


FOOD_ONLY_INTENT_FIELDS: tuple[str, ...] = (
    "star_ingredient",
    "cuisine",
    "cuisine_region",
    "cuisine_stance",
    "heat_level",
)
"""The Intent fields that describe a dish and have a DrinkIntent counterpart.

Everything not listed here is genuinely shared (servings, time_budget_min, exclusions,
occasion) and stays on Intent for both media. These five are what ``medium`` is checked
against: a session that claims to be a drink but carries a star ingredient and a cuisine is
a food session wearing a drink label, and every downstream medium dispatch — the conflict
rule set, the precursor table, the research plan shape — would then be reading a flag that
does not describe the payload."""


class Intent(BaseModel):
    """What the user said they want to cook, refined through INTAKE + CLARIFY."""

    model_config = ConfigDict(extra="forbid")

    star_ingredient: str | None = None
    cuisine: str | None = None
    cuisine_region: str | None = None
    cuisine_stance: CuisineStance | None = None
    heat_level: HeatLevel | None = None
    servings: int | None = None
    time_budget_min: int | None = None
    exclusions: list[str] = Field(default_factory=list)
    occasion: str | None = None
    medium: Medium = "dish"
    drink: DrinkIntent | None = None

    @model_validator(mode="after")
    def _medium_matches_shape(self) -> Intent:
        """``medium`` must describe the fields actually present, in both directions.

        Without this, ``medium`` is a free-floating label: a fully food-shaped intent could
        carry ``medium: drink`` and validate clean, and every consumer that dispatches on it
        would then apply drink rules to food content — including the HARD allergy tier, which
        is the one the user never sees. The field is one token in a YAML file, so the schema
        is the only place this can be caught.

        Legacy states are unaffected: ``medium`` defaults to ``dish`` and ``drink`` defaults
        to None, so a state.yaml written before drinks existed satisfies both directions.
        """
        if self.medium == "drink":
            present = [f for f in FOOD_ONLY_INTENT_FIELDS if getattr(self, f) is not None]
            if present:
                raise ValueError(
                    f"intent.medium is 'drink' but food-shaped field(s) {', '.join(present)} "
                    f"are set. A drink session carries these under intent.drink instead "
                    f"(star_ingredient -> base_spirit, cuisine -> drink_family, "
                    f"cuisine_region -> family_variant, cuisine_stance -> family_stance, "
                    f"heat_level -> strength_level + sweetness_level). servings, "
                    f"time_budget_min, exclusions and occasion stay on intent for both media"
                )
        elif self.drink is not None:
            raise ValueError(
                "intent.drink is set but intent.medium is 'dish'; set medium: drink for a "
                "drink session, or drop the drink block"
            )
        return self


class DrinkIntent(BaseModel):
    """What the user said they want to drink, refined through INTAKE + CLARIFY.

    Sibling of Intent's food-specific fields rather than a replacement for Intent: it hangs
    off ``Intent.drink`` and only the food-shaped fields are mirrored here. servings,
    time_budget_min, exclusions and occasion stay on Intent because a drink has all four,
    and exclusions in particular must stay shared so both allergy rules read one list.

    The analogs are one-to-one: star_ingredient -> base_spirit, cuisine -> drink_family,
    cuisine_region -> family_variant, cuisine_stance -> family_stance, and heat_level ->
    strength_level + sweetness_level. The last five fields have no food counterpart at all;
    they carry the build, the dilution/ABV arithmetic, and the batching format.
    """

    model_config = ConfigDict(extra="forbid")

    base_spirit: str | None = None
    drink_family: str | None = None
    family_variant: str | None = None
    family_stance: FamilyStance | None = None
    strength_level: StrengthLevel | None = None
    sweetness_level: SweetnessLevel | None = None
    build_method: BuildMethod | None = None
    abv_target_pct: float | None = None
    dilution_target_pct: float | None = None
    service_format: ServiceFormat | None = None
    glassware: str | None = None


class ResearchPlan(BaseModel):
    """The agent's plan of what to research, written in GROUNDING."""

    model_config = ConfigDict(extra="forbid")

    aromatic_base: str
    functional_roles_to_fill: list[str]
    techniques_under_consideration: list[str] = Field(default_factory=list)


class DrinkResearchPlan(BaseModel):
    """The agent's plan of what to research for a drink, written in GROUNDING.

    Sibling of ResearchPlan. base_spirit is required for the same reason aromatic_base is:
    it is the backbone the rest of the plan hangs off, and a plan that has not named it has
    not been made. A drink has no aromatic base, so the two plans are separate models
    rather than one model with optional halves.
    """

    model_config = ConfigDict(extra="forbid")

    base_spirit: str
    drink_roles_to_fill: list[str]
    build_methods_under_consideration: list[str] = Field(default_factory=list)


def _research_plan_kind(value: Any) -> str:
    """Discriminate a research plan payload by the required field it carries.

    Returns ``"drink"`` for DrinkResearchPlan-shaped input and ``"dish"`` for everything
    else, including unrecognised payloads — an unrecognised payload falls through to
    ResearchPlan so the user still sees the existing food-side ValidationError rather than
    a new union-shaped one.
    """
    if isinstance(value, DrinkResearchPlan):
        return "drink"
    if isinstance(value, ResearchPlan):
        return "dish"
    if isinstance(value, dict):
        if "base_spirit" in value or "drink_roles_to_fill" in value:
            return "drink"
        if "aromatic_base" in value or "functional_roles_to_fill" in value:
            return "dish"
    return "dish"


AnyResearchPlan = Annotated[
    Annotated[ResearchPlan, Tag("dish")] | Annotated[DrinkResearchPlan, Tag("drink")],
    Discriminator(_research_plan_kind),
]
"""The research plan for either medium, resolved by an explicit callable discriminator.

Deliberately not a bare smart union: ``ResearchPlan | DrinkResearchPlan`` only resolves
correctly today because both models forbid extras and have disjoint required fields, which
is an implicit invariant a future field addition would silently break. Discriminating on
the payload shape is deterministic by construction, and it needs no discriminator field on
either model — so ResearchPlan is untouched and a food state.yaml gains no new key.

The discriminator answers *which model this payload is*, not *which model this session is
allowed to have*: pydantic hands a callable discriminator the field value alone, with no
view of intent.medium. The second question is cross-field and is answered in
State._medium_matches_vocabulary, which is what keeps aromatic_base effectively required
for a dish session."""


class ResearchLogEntry(BaseModel):
    """One web-research call the agent executed during RESEARCH.

    Hooks read research_log to enforce ordering: an aromatic_base entry must precede any
    functional_role entry; functional_role must precede candidate, etc. Drink sessions log
    under DrinkResearchTag and are ordered by the parallel precursor table.
    """

    model_config = ConfigDict(extra="forbid")

    timestamp: datetime
    tag: ResearchTag | DrinkResearchTag
    query: str
    result_summary: str


class Candidate(BaseModel):
    """An ingredient the agent surfaced for the user to pick from in CURATE."""

    model_config = ConfigDict(extra="forbid")

    name: str
    cuisine_origin: str
    functional_role: str
    intensity: int | None = None
    notes: str | None = None


class PrunedItem(BaseModel):
    """A candidate that was removed, with the rule that fired and the human-readable reason."""

    model_config = ConfigDict(extra="forbid")

    name: str
    rule: PruneRule | DrinkPruneRule
    reason: str


EnhancementLens = Literal["physics", "flavor"]
"""Which lens surfaced this candidate. Physics covers heat-transfer, equipment, and
mechanical technique upgrades. Flavor covers cross-cuisine vectors and chemistry-driven
ingredient or timing moves."""


EnhancementClassification = Literal[
    "objectively_better",
    "taste_dependent",
    "tradition_respected",
    "cargo_cult",
]
"""Where the candidate lands after the pass:
- objectively_better: same dish character, measurably improved on a named axis; auto-applied
  to the recipe with an inline fallback line for any equipment-coupling
- taste_dependent: shifts dish character; surfaced as a Variants menu, user picks
- tradition_respected: physics could push but eating shouldn't; documented and left alone
- cargo_cult: deconstruction couldn't find a reason; flagged for next-cook removal test"""


EnhancementConfidence = Literal["HIGH", "MEDIUM", "LOW"]
"""Honest confidence marking for the mechanism claim. The first-principles pass risks
confabulating plausible-sounding food science; HIGH requires named literature
(Modernist Cuisine, Kenji, McGee, Cook's Illustrated, peer-reviewed)."""


class DeconstructionNote(BaseModel):
    """One per-move analysis entry: what this technique or ingredient is doing in the dish.

    Populated during ENHANCE. Rendered below the line in the recipe under "Why this works".
    """

    model_config = ConfigDict(extra="forbid")

    move: str
    """Step number, ingredient name, or short identifier the cook can map to the recipe."""

    function: str
    """What this move is doing — the role it serves in flavor/texture/structure."""

    load_bearing: bool
    """True if removing or substituting this move would meaningfully degrade the dish."""

    tradition_note: str | None = None
    """If the move is culturally specific (epazote, comal-charring, piloncillo), the
    tradition reason that protects it from physics-driven substitution."""


class EnhancementCandidate(BaseModel):
    """One candidate surfaced by the ENHANCE pass, classified for GUIDE to render.

    The pass produces a list of these per recipe. The renderer routes by classification:
    objectively_better candidates are folded into the Method (with fallback), taste_dependent
    candidates appear in the Variants section, tradition_respected candidates appear as
    annotations in the Why-section, cargo_cult candidates appear in a flag list.
    """

    model_config = ConfigDict(extra="forbid")

    move: str
    """Which step or ingredient this candidate targets — must match a recipe move."""

    lens: EnhancementLens
    classification: EnhancementClassification

    proposal: str
    """The actual move proposed (technique change, ingredient addition, timing shift)."""

    mechanism: str
    """What this move optimizes. Cite named food science where possible. Vague claims
    ('this adds depth') do not earn their place — that's the cargo-cult bucket."""

    confidence: EnhancementConfidence

    tradeoff: str | None = None
    """Required for taste_dependent: what changes about the dish if this is adopted.
    Required for tradition_respected: what physics says vs what eating wants."""

    fallback: str | None = None
    """Required for objectively_better candidates with equipment-coupling
    (Dutch oven, microwave, probe thermometer): what to do if the cook lacks the tool."""


class Enhancements(BaseModel):
    """The full output of the ENHANCE pass. Lives at State.enhancements.

    Two parts: deconstruction (what each move is doing) and candidates (upgrades the pass
    surfaced under physics and flavor lenses). GUIDE renders both below the line.
    """

    model_config = ConfigDict(extra="forbid")

    deconstruction: list[DeconstructionNote] = Field(default_factory=list)
    candidates: list[EnhancementCandidate] = Field(default_factory=list)


class State(BaseModel):
    """The full session state. Persisted to sessions/<session_id>/state.yaml."""

    model_config = ConfigDict(extra="forbid")

    session_id: str
    phase: Phase
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    intent: Intent = Field(default_factory=Intent)
    research_plan: AnyResearchPlan | None = None
    research_log: list[ResearchLogEntry] = Field(default_factory=list)
    candidates: list[Candidate] = Field(default_factory=list)
    selected: list[str] = Field(default_factory=list)
    pruned: list[PrunedItem] = Field(default_factory=list)
    enhancements: Enhancements | None = None
    recipe_path: str | None = None

    @model_validator(mode="after")
    def _medium_matches_vocabulary(self) -> State:
        """Every medium-scoped vocabulary in the state must match ``intent.medium``.

        Three fields widened to serve both media — research_plan (a union), research_log.tag
        and pruned.rule (both widened Literals/enums). Widening them alone would move the
        enforcement each one used to do out of the schema and into a prompt instruction:
        a dish session could carry a drink research plan (and lose the aromatic_base
        requirement), log an entry under a drink tag the food precursor table has never heard
        of (and skip the ordering gate entirely), or label a food prune with a drink rule.

        The medium picks the vocabulary; this validator holds each field to it. Which is the
        same dispatch the conflict rules and the hook's precursor table already do — the
        schema is simply where it has to happen for the fields the schema owns.
        """
        medium = self.intent.medium
        expected_plan = DrinkResearchPlan if medium == "drink" else ResearchPlan
        required = (
            "base_spirit + drink_roles_to_fill" if medium == "drink"
            else "aromatic_base + functional_roles_to_fill"
        )
        if self.research_plan is not None and not isinstance(self.research_plan, expected_plan):
            raise ValueError(
                f"intent.medium is {medium!r} but research_plan is a "
                f"{type(self.research_plan).__name__}; a {medium} session requires a "
                f"{expected_plan.__name__} ({required})"
            )
        tags = DRINK_RESEARCH_TAGS if medium == "drink" else RESEARCH_TAGS
        for index, entry in enumerate(self.research_log):
            if entry.tag not in tags:
                raise ValueError(
                    f"research_log[{index}] tag {entry.tag!r} is not a {medium} research tag "
                    f"(valid for {medium}: {', '.join(sorted(tags))})"
                )
        rules = DrinkPruneRule if medium == "drink" else PruneRule
        for index, item in enumerate(self.pruned):
            if not isinstance(item.rule, rules):
                raise ValueError(
                    f"pruned[{index}] rule {item.rule.value!r} is not a {medium} prune rule "
                    f"(valid for {medium}: {', '.join(sorted(r.value for r in rules))})"
                )
        return self

    def dump_yaml(self, path: Path) -> None:
        """Write this state to ``path`` as YAML.

        Uses pydantic's JSON-mode dump so datetimes become ISO strings and enums become
        their string values, both of which YAML serializes cleanly without custom
        representers.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            yaml.safe_dump(
                self.model_dump(mode="json"),
                sort_keys=False,
                default_flow_style=False,
                allow_unicode=True,
            ),
            encoding="utf-8",
        )

    @classmethod
    def load_yaml(cls, path: Path) -> State:
        """Load and validate a state.yaml file produced by ``dump_yaml``."""
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        return cls.model_validate(data)
