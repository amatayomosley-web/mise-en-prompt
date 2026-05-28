# mise-en-prompt

> *mise en place* (n.): everything in its place. The prep work a chef does before cooking begins.

A culinary agent that helps you cook intentionally. You describe what you want for dinner; it asks
clarifying questions, researches authentic ingredients grounded in regional cooking knowledge,
walks you through curating an ingredient list (pruning conflicts as you go), and assembles the
final recipe and cooking guide.

Runs as a Claude Code agent.

## Usage

Invoke with the `/chef` slash command. This activates the chef in the active conversation
so `AskUserQuestion` can reach your keyboard during CURATE. The role-by-role ingredient
walk is the load-bearing interaction and only works in an active session.

> **Don't** invoke chef via `subagent_type: chef` (Task tool). Subagents are one-shot and
> can't fire `AskUserQuestion`, so the CURATE walk collapses into a single recipe-generation
> turn and you lose the whole point of the agent. See `.claude/commands/chef.md` for the
> full diagnosis.

## Status

Pre-alpha. Last development pass: May 2026. The 8-phase agent flow works end-to-end; further iteration depends on user feedback. Issues and discussion welcome.

## How it works

The agent moves through 8 phases, persisting state to `sessions/<session-id>/state.yaml` between
turns:

1. **Intake.** Capture the initial request.
2. **Clarify.** Fill in gaps (cuisine specificity, heat tolerance, exclusions, time budget).
3. **Grounding.** Consult the three culinary pillars to plan research.
4. **Research.** Web search for region-specific ingredients and traditional pairings.
5. **Curate.** Present candidates; user picks; the agent prunes conflicts (cuisine drift,
   functional redundancy, allergy, technique impossibility). Availability is a user concern:
   the user simply doesn't pick what they don't have or can't get.
6. **Synthesize.** Draft the recipe from selected ingredients.
7. **Enhance.** Walk the draft move-by-move under physics and flavor lenses; classify each
   candidate (objectively_better, taste_dependent, tradition_respected, cargo_cult);
   write the deconstruction and elevation candidates to `state.enhancements`.
8. **Guide.** Render the cooking guide with operational content above the line and
   deconstruction plus variants below; auto-apply objectively-better upgrades inline with
   fallbacks; surface taste-dependent options as a Variants menu.

## The three pillars

The agent doesn't ship a closed recipe database. It ships a methodology: three knowledge pillars
that ground how it researches and reasons.

- **Ingredients.** What each ingredient *contributes* (aromatic role, flavor affinity, functional role).
- **Technique.** What heat, time, and pressure do to ingredients (Maillard, state changes, emulsions).
- **Balance.** How to diagnose and fix off-balance dishes (rescue tables, layering, timing).

## Layout

```
.claude/
  agents/chef.md                            # the chef agent system prompt
  settings.json                             # registers the enforcement hooks
  skills/
    culinary-ingredients/{SKILL.md, reference.md}
    culinary-technique/{SKILL.md, reference.md}
    culinary-balance/{SKILL.md, reference.md}
src/mise_en_prompt/
  state.py                                  # session state schema (pydantic)
  conflicts.py                              # conflict detection rules + CLI
  hooks/
    state_validate.py                       # PreToolUse: validates state.yaml writes
    phase_check.py                          # PreToolUse: blocks recipe.md before phase=GUIDE
sessions/                                   # per-session state (gitignored except sample)
  2026-04-28-pinto-beans-sample/
    state.yaml                              # example session at the CURATE phase
tests/
docs/
  pillar-source/                            # original research documents preserved
```

## Enforcement

Two project-local hooks (registered in `.claude/settings.json`) guard the agent's state contract:

- **`state_validate`.** Every Write to `sessions/<id>/state.yaml` must parse, validate against the
  pydantic schema, and respect research_log ordering (e.g. you can't research candidates before
  you've researched the aromatic base). Invalid writes are blocked with a clear error.
- **`phase_check`.** Writes to `sessions/<id>/recipe.md` are blocked unless the corresponding
  `state.yaml` shows `phase: GUIDE`. The agent can't ship a recipe before completing CURATE and
  SYNTHESIZE.

## Conflict rules

Four prune rules apply during CURATE (see [`conflicts.py`](src/mise_en_prompt/conflicts.py)):

| Rule | Severity | Behavior |
|---|---|---|
| `allergy_hard_filter` | HARD | Candidates matching `intent.exclusions` are silently removed (with alias expansion: "shellfish" → shrimp/lobster/crab/etc.). |
| `cuisine_drift` | SOFT | Candidates in a different cuisine group from the target dish are flagged; the user decides. |
| `functional_redundancy` | SOFT | Adding a same-role candidate within intensity ±2 of an already-selected one is flagged. Stackable roles (herbs, spices) skip this check. |
| `technique_impossibility` | SOFT | v1 stub. v2 will check candidate prep time against `intent.time_budget_min`. |

Run them on a session yourself:

```bash
python -m mise_en_prompt.conflicts filter --role heat --state sessions/<id>/state.yaml
```

## Install

```bash
pip install -e ".[dev]"
```

## License

MIT
