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
    """The seven sequential phases of a chef-agent session."""

    INTAKE = "INTAKE"
    CLARIFY = "CLARIFY"
    GROUNDING = "GROUNDING"
    RESEARCH = "RESEARCH"
    CURATE = "CURATE"
    SYNTHESIZE = "SYNTHESIZE"
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


class Intent(BaseModel):
    """What the user said they want to cook, refined through INTAKE + CLARIFY."""

    model_config = ConfigDict(extra="forbid")

    star_ingredient: str | None = None
    cuisine: str | None = None
    cuisine_region: str | None = None
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
