# mise-en-prompt

> *mise en place* (n.): everything in its place. The prep work a chef does before cooking begins.

A culinary agent that helps you cook intentionally. You describe what you want for dinner; it asks
clarifying questions, researches authentic ingredients grounded in regional cooking knowledge,
walks you through curating an ingredient list (pruning conflicts as you go), and assembles the
final recipe and cooking guide.

It does the same for drinks. Ask for a cocktail and the session runs on drink structures rather
than food ones: drink family and build method in place of cuisine and technique, base spirit in
place of aromatic base, strength and sweetness as two separate axes, and a conflict pass that
knows a split base is construction rather than redundancy. Coverage is cocktails and bar prep
(build methods, dilution and ABV math, syrups, sweetener ratios, cordials, infusions,
fat-washing, clarification, batching). Fermentation and homebrewing are out of scope.

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

Pre-alpha. Last development pass: August 2026. The 8-phase agent flow works end-to-end; further iteration depends on user feedback. Issues and discussion welcome.

The drink path is newer than the food path and has had less real use. It was added alongside the
food structures rather than on top of them, so the food path behaves exactly as it did before:
same schema, same rules, same hooks, same tests passing unmodified. A `state.yaml` written before
drinks existed still loads and still runs the same four rules it always did.

## How it works

The agent moves through 8 phases, persisting state to `sessions/<session-id>/state.yaml` between
turns. The phases are identical for a dish and a drink. What changes per phase is which pillar
gets consulted, which roles get curated, and which conflict rules run.

1. **Intake.** Capture the initial request, and settle the medium (`intent.medium`, either `dish`
   or `drink`). Absent means dish.
2. **Clarify.** Fill in gaps. For a dish: cuisine specificity, heat tolerance, exclusions, time
   budget. For a drink: drink family, base spirit, strength and sweetness (two axes, because they
   move independently), one drink or a batch, and what glassware and ice you actually have.
3. **Grounding.** Consult the pillars to plan research. A dish reads the three culinary pillars;
   a drink reads `beverage-craft` plus `culinary-balance`, which transfers to a glass unchanged.
4. **Research.** Web search for region-specific ingredients and traditional pairings, or for a
   drink, the family's template, what fills each role, the build method, and the dilution that
   build implies.
5. **Curate.** Present candidates; user picks; the agent prunes conflicts (see Conflict rules
   below). Availability is a user concern: the user simply doesn't pick what they don't have or
   can't get.
6. **Synthesize.** Draft the recipe from selected ingredients, or for a drink, the spec:
   volumes, build, dilution, and finished ABV.
7. **Enhance.** Walk the draft move-by-move under physics and flavor lenses; classify each
   candidate (objectively_better, taste_dependent, tradition_respected, cargo_cult);
   write the deconstruction and elevation candidates to `state.enhancements`.
8. **Guide.** Render the cooking guide (for a drink, the build and service guide) with operational
   content above the line and deconstruction plus variants below; auto-apply objectively-better
   upgrades inline with fallbacks; surface taste-dependent options as a Variants menu.

## The four pillars

The agent doesn't ship a closed recipe database. It ships a methodology: four knowledge pillars
that ground how it researches and reasons.

- **Ingredients.** What each ingredient *contributes* (aromatic role, flavor affinity, functional role).
- **Technique.** What heat, time, and pressure do to ingredients (Maillard, state changes, emulsions).
- **Balance.** How to diagnose and fix off-balance dishes (rescue tables, layering, timing).
- **Beverage craft.** What structural template a drink is, what fills each slot, what cold water
  does to it, and what has to be made days in advance (templates and ratios, build methods,
  dilution and ABV math, syrups and cordials, infusions and fat-washing, clarification, batching).

The fourth pillar sits alongside the first three rather than extending them. A drink session
reads it instead of Ingredients and Technique, and keeps Balance, whose taste axes and rescue
logic are medium-agnostic. Technique is food-only: a cold drink has no Maillard, no collagen,
and no reduction.

## Layout

```
.claude/
  agents/chef.md                            # the chef agent system prompt
  settings.json                             # registers the enforcement hooks
  skills/
    culinary-ingredients/{SKILL.md, reference.md}
    culinary-technique/{SKILL.md, reference.md}
    culinary-balance/{SKILL.md, reference.md}
    beverage-craft/{SKILL.md, reference.md}   # the drink pillar
src/mise_en_prompt/
  state.py                                  # session state schema (pydantic), dish and drink
  conflicts.py                              # conflict detection rules + CLI, dish and drink
  hooks/
    state_validate.py                       # PreToolUse: validates state.yaml writes
    phase_check.py                          # PreToolUse: blocks recipe.md before phase=GUIDE
sessions/                                   # per-session state (gitignored except sample)
  2026-04-28-pinto-beans-sample/
    state.yaml                              # example session at the CURATE phase
tests/
docs/
  pillar-source/                            # original research documents preserved
    00_overview_and_skill_mapping.md        # which document became which skill
    01..03                                  # the three food pillars
    04_beverage_craft_and_dilution.md       # the drink pillar
```

## Enforcement

Two project-local hooks (registered in `.claude/settings.json`) guard the agent's state contract:

- **`state_validate`.** Every Write to `sessions/<id>/state.yaml` must parse, validate against the
  pydantic schema, and respect research_log ordering (e.g. you can't research candidates before
  you've researched the aromatic base). Invalid writes are blocked with a clear error. Ordering is
  medium-aware: a drink session is checked against its own dependency graph, where the base spirit
  precedes the roles and the build method precedes the dilution math, because water pickup is a
  property of the build rather than of the ingredients. `intent.medium` is checked against the
  state's actual shape rather than trusted: a drink session cannot carry food-shaped intent fields,
  a food research plan, food research tags or food prune rules, and a dish session cannot carry
  their drink counterparts. Otherwise one token in a YAML file silently swaps which rules apply.
- **`phase_check`.** Writes to `sessions/<id>/recipe.md` are blocked unless the corresponding
  `state.yaml` shows `phase: GUIDE`. The agent can't ship a recipe before completing CURATE and
  SYNTHESIZE. This hook is medium-agnostic and unchanged: a drink session walks the same 8 phases
  and its spec is gated the same way.

## Conflict rules

Four prune rules apply during CURATE in a dish session (see
[`conflicts.py`](src/mise_en_prompt/conflicts.py)):

| Rule | Severity | Behavior |
|---|---|---|
| `allergy_hard_filter` | HARD | Candidates matching `intent.exclusions` are silently removed (with alias expansion: "shellfish" → shrimp/lobster/crab/etc.). |
| `cuisine_drift` | SOFT | Candidates in a different cuisine group from the target dish are flagged; the user decides. |
| `functional_redundancy` | SOFT | Adding a same-role candidate within intensity ±2 of an already-selected one is flagged. Stackable roles (herbs, spices) skip this check. |
| `technique_impossibility` | SOFT | v1 stub. v2 will check candidate prep time against `intent.time_budget_min`. |

A drink session runs four mirrored rules instead, selected on `intent.medium`, and those four
carry the five labels below (the allergy rule can resolve either way). They are siblings, not
overrides: the food rules are never branched, never consulted for a drink, and unchanged by any of
this. The two rule vocabularies are separate enums, so the audit trail in `state.pruned` never
labels a drink decision with a food-named rule.

| Rule | Severity | Behavior |
|---|---|---|
| `drink_allergy_hard_filter` | HARD | Candidates matching `intent.exclusions` are silently removed, including the nut paths that carry no nut word: orgeat, falernum, Amaretto, Frangelico, Nocino, crème de noyaux. Gluten aside, this tier reads the food alias list as well as the drink one, so a drink session cannot lose a category the food session catches — Clamato and clam juice under shellfish, Worcestershire under fish, a bacon fat-wash under pork. Matching is whole-word and a false-friend guard cancels known collisions, so cream sherry and crème de cacao are not read as dairy, coconut and nutmeg are not read as tree nuts, ginger beer is not read as beer, and Salers, Fish House Punch and Beefeater are not read as anything. Each false friend cancels only the word it explains, so a coconut orgeat is still caught on the orgeat. |
| `drink_allergy_soft_flag` | SOFT | No food counterpart. Distillation leaves gluten protein behind in the wash, so a rye whiskey is not a gluten exposure the way a beer is, but plenty of drinkers avoid grain spirits anyway. Those candidates are surfaced for the user to decide rather than silently deleted. Same tier for sulfites in wine-based products. |
| `family_drift` | SOFT | Candidates in a different drink family group from the target drink are flagged; the user decides. Family-neutral components (syrups, citrus, ice) carry no family and the rule stays silent on them. |
| `drink_functional_redundancy` | SOFT | Keyed on bar-product class first, intensity second. Two dry vermouths or two orange liqueurs in the same slot are flagged even in a stackable role, while a split base (two different rums) and stacked bitters pass, because those are the defining moves of the form rather than accidents. Single-slot roles (sweet, acid, dilution, texture) fall back to the same intensity ±2 comparison the food rule uses. |
| `build_impossibility` | SOFT | v1 stub, same as its food sibling. v2 will check the candidate against `intent.drink.build_method`: an egg white cannot be stirred, and a carbonated build cannot take fresh citrus without pre-clarification. |

Run either set on a session yourself. The CLI reads the medium off the state file and dispatches:

```bash
python -m mise_en_prompt.conflicts filter --role heat --state sessions/<id>/state.yaml
python -m mise_en_prompt.conflicts filter --role modifier --state sessions/<id>/state.yaml
```

## Install

```bash
pip install -e ".[dev]"
```

## License

MIT
