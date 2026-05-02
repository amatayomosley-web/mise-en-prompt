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
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field


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


ResearchTag = Literal[
    "aromatic_base",
    "functional_role",
    "candidate",
    "pairing",
    "technique",
]
"""Ordered research tags. Hooks enforce that searches happen in this order:
aromatic_base -> functional_role -> candidate -> pairing/technique."""


HeatLevel = Literal["mild", "medium", "spicy", "very_spicy"]


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


class ResearchPlan(BaseModel):
    """The agent's plan of what to research, written in GROUNDING."""

    model_config = ConfigDict(extra="forbid")

    aromatic_base: str
    functional_roles_to_fill: list[str]
    techniques_under_consideration: list[str] = Field(default_factory=list)


class ResearchLogEntry(BaseModel):
    """One web-research call the agent executed during RESEARCH.

    Hooks read research_log to enforce ordering: an aromatic_base entry must precede any
    functional_role entry; functional_role must precede candidate, etc.
    """

    model_config = ConfigDict(extra="forbid")

    timestamp: datetime
    tag: ResearchTag
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
    rule: PruneRule
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
    research_plan: ResearchPlan | None = None
    research_log: list[ResearchLogEntry] = Field(default_factory=list)
    candidates: list[Candidate] = Field(default_factory=list)
    selected: list[str] = Field(default_factory=list)
    pruned: list[PrunedItem] = Field(default_factory=list)
    enhancements: Enhancements | None = None
    recipe_path: str | None = None

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
