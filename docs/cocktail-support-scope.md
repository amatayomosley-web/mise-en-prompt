# Scope — cocktail support

**Status:** proposal, not yet implemented.
**Baseline:** `c28fa73`, 53 tests passing.

---

## Recommendation

Add cocktails as a **second domain on the existing spine**, not as a second agent.

Concretely: a `domain: food | cocktail` discriminator on `State`, domain-swapped lookup
tables inside the existing conflict rules, one new knowledge pillar for the physics that
cooking doesn't cover, and a `/bar` command that enters the same 8-phase walk with a
different vocabulary. The phases, the hooks, the CURATE `AskUserQuestion` loop, and the
state contract stay exactly as they are.

The reason is load-bearing: the phase walk and the conflict engine are the product. A
`bartender` agent that duplicates them starts as a copy of 546 lines of phase prose and
diverges from it within two commits.

---

## What already transfers

These were verified against the code at `c28fa73`, not assumed.

**`functional_role` is a free string** (`state.py:121`), and `filter_candidates_for_role`
compares it case-insensitively (`conflicts.py:234`). Running the CURATE filter against a
cocktail role works today with zero code change:

```
filter --role base_spirit -> ['Jamaican pot still rum', 'rhum agricole'] | would_prune: []
```

That is the single most important finding in this document. The role-by-role prompt loop —
the interaction the whole project is built around — needs nothing.

**The rest of the spine transfers as-is:**

| Component | Why it holds for drinks |
|---|---|
| 8 phases | INTAKE → GUIDE maps cleanly; a spec sheet is a recipe with a shorter Method |
| `cuisine_stance` (`state.py:65`) | "Canonical Negroni" vs. "best Negroni-shaped thing" is exactly `tradition` vs. `explore` |
| `check_allergy` (HARD) | Dairy, egg, nut, gluten exclusions all apply — see the orgeat gap below |
| `phase_check` hook | Regex targets `sessions/<id>/recipe.md` (`phase_check.py:22`); unchanged if drinks keep that filename |
| ENHANCE classification | `objectively_better` / `taste_dependent` / `tradition_respected` / `cargo_cult` needs no new buckets |
| `culinary-balance` | Sweet–sour–bitter rescue logic is arguably *closer* to cocktail work than to cooking |

---

## What genuinely doesn't transfer

### 1. `culinary-technique` is entirely thermal

Maillard, collagen breakdown, reduction targets, heat-driven emulsions. Cocktails run on the
opposite physics — dilution, chilling curves, aeration, carbonation, clarification. This
cannot be an edit to the existing pillar; it needs a sibling.

### 2. `functional_redundancy` fights a canonical cocktail technique

`check_functional_redundancy` (`conflicts.py:171`) flags a same-role candidate within
intensity ±2 of an already-selected one. In food that's a real smell (two mid-intensity acids
is usually a mistake). In cocktails, **a split base is a technique, not a redundancy** — Fish
House Punch, split-base daiquiris, rum-and-cognac builds. The rule would fire on the correct
answer.

Fix: `base_spirit` and `modifier` need either `STACKABLE_ROLES` membership
(`conflicts.py:113`) or a domain-specific threshold. Recommend stackable, with the
strength rule below carrying the real constraint.

### 3. `orgeat` slips the nut filter — verified

```
orgeat vs "nuts" exclusion  -> NO FINDING (gap)
almond syrup vs "nuts"      -> allergy_hard_filter
```

`check_allergy` (`conflicts.py:130`) does substring matching against `EXCLUSION_ALIASES`
(`conflicts.py:49`), and `"orgeat"` contains no alias. Orgeat is *the* almond syrup of tiki —
the most-reached-for sweetener in the entire idiom — and it currently passes a declared nut
allergy silently. Same class of gap: amaretto, nocino, crème de noyaux, Frangelico.

This is a HARD-filter miss, so it is the highest-priority item in M1 regardless of how much
else ships.

### 4. `CUISINE_GROUPS` has no drink taxonomy

`_find_cuisine_group` (`conflicts.py:118`) resolves against seven regional food groups. Drinks
have their own two-axis taxonomy — spirit family (agave / cane / grain / grape / botanical)
and structural template (the Cocktail Codex six: Old-Fashioned, Martini, Daiquiri, Sidecar,
Highball, Flip). Drift should key on spirit family; template belongs with technique.

### 5. `heat_level` is a chile axis

`HeatLevel = Literal["mild", "medium", "spicy", "very_spicy"]` (`state.py:62`) is meaningless
for most drinks. It stays nullable and food-only — spicy margaritas are the exception that
keeps it from being wrong, not a reason to redesign it. What cocktails need instead is a
**strength** axis, which food has no analog for.

### 6. `PRECURSORS` assumes an aromatic base

The `state_validate` hook (`state_validate.py:28`) enforces `aromatic_base → functional_role
→ candidate`. Cocktails have a base *spirit*, not an aromatic base. Either add a `base_spirit`
research tag at the same graph position, or make the graph domain-aware. Recommend both:
new tag, domain-selected graph.

### 7. `extra="forbid"` blocks the field before it exists — verified

```
State.model_validate({... "domain": "cocktail"}) -> REJECTED: Extra inputs are not permitted
```

This forces an ordering constraint: **the schema change must merge before any agent prose
writes `domain`**, or the `state_validate` hook blocks the agent's own first write. Schema
first, prompt second, in that order, in separate commits.

---

## Architecture

### Chosen: `domain` discriminator + externalized domain profiles

```
State.domain: Literal["food","cocktail"] = "food"    # defaulted → every existing state.yaml still loads

.claude/agents/chef.md          # 8-phase spine, domain-agnostic (+ ~40-line routing section)
.claude/domains/food.md         # role list, role order, balance axes, recipe template  ← extracted verbatim
.claude/domains/cocktail.md     # same shape, drink content                             ← new
.claude/commands/chef.md        # domain=food
.claude/commands/bar.md         # domain=cocktail                                       ← new
```

At INTAKE the agent sets `state.domain` and reads `.claude/domains/<domain>.md`. Everything
domain-specific — the functional-role list, the CURATE role-order heuristic, the balance axes,
the artifact template — lives in the profile. The spine never branches.

One agent, two commands, two profiles. The persona difference (chef vs. bartender voice) is a
profile concern, not an agent-file concern.

### Rejected: a separate `bartender` agent

Clean isolation, but it forks 546 lines of phase prose plus the CURATE interaction spec — the
parts most likely to be edited and least likely to be kept in sync. The `/chef` command file
already documents why the interactive walk is the product; duplicating it doubles the
maintenance surface for the one thing that must not drift.

### Rejected: branching every phase inside `chef.md`

`chef.md` is already 546 lines. Inlining a domain branch at every phase roughly doubles it
and makes the food path harder to read than it is today.

---

## Change inventory

### `src/mise_en_prompt/state.py`

| Change | Note |
|---|---|
| `Domain = Literal["food","cocktail"]` | new |
| `State.domain: Domain = "food"` | **defaulted** — existing sessions and the sample fixture keep validating |
| `Intent.strength_target: Literal["low","medium","spirit_forward"] \| None` | new; the axis food lacks |
| `Intent.serve_style: Literal["up","rocks","long","hot"] \| None` | new; drives dilution target and glassware |
| `Intent.abv_ceiling: float \| None` | new; `0.0` = zero-proof, and it is a *hard* constraint |
| `ResearchTag` += `base_spirit`, `modifier`, `dilution` | additive; existing tags untouched |
| `PruneRule` += `strength_violation` | additive |

**Deliberately reused rather than added:** `star_ingredient` (= base spirit), `cuisine`
(= drink family: tiki, pre-Prohibition, Italian aperitivo), `cuisine_stance`, `servings`
(= number of drinks), `time_budget_min`, `exclusions`, `occasion`. Adding parallel
`base_spirit`/`drink_family` fields would double the intake surface for no gain and leave
two fields that mean the same thing to every downstream consumer.

**Deliberately not renamed:** `PruneRule.CUISINE_DRIFT` keeps its name and gains a
family-drift meaning under `domain: cocktail`. Renaming the enum breaks the `pruned[]` entries
in every existing `state.yaml` and every hook that validates them — a docs change buys the
same clarity for none of the cost.

### `src/mise_en_prompt/conflicts.py`

| Change | Note |
|---|---|
| `SPIRIT_FAMILIES` dict alongside `CUISINE_GROUPS` | `_find_cuisine_group` selects the table by `state.domain` |
| `EXCLUSION_ALIASES` += orgeat, amaretto, nocino, noyaux, frangelico under `nuts` | **the verified HARD-filter gap** |
| `EXCLUSION_ALIASES` += new `alcohol` key | covers the whole spirit list for the zero-proof path |
| `STACKABLE_ROLES` += `bitters`, `garnish`, `base_spirit`, `modifier` | unblocks split bases |
| `check_strength` — new rule | HARD when `abv_ceiling == 0` and the candidate is alcoholic; SOFT when the running build's estimated ABV exceeds the ceiling |
| `_ALL_RULES` += `check_strength` | |

`check_strength` is the one place cocktails get a *better* programmatic check than food does:
final ABV and dilution are arithmetic, so the rule can compute rather than pattern-match.
`check_technique_impossibility` (`conflicts.py:204`) is still a v1 stub and stays one.

### Skills

| Skill | Action |
|---|---|
| `cocktail-technique` | **new pillar** — dilution math by method, ice, shake/stir/throw/whip, dry and reverse-dry shake, clarification (milk, agar), infusion (fat-wash, oleo-saccharum, tincture), carbonation, temperature and service, batching pre-dilution |
| `culinary-balance` | **extend** — sour ratios, the strong/sweet/sour triangle, bitterness and amaro, dilution as a balance axis; one-line description edit so it triggers on drinks |
| `culinary-ingredients` | **extend** — spirit, modifier, and bitters taxonomy by functional role |
| `culinary-technique` | **untouched** |

Source doc: `docs/pillar-source/04_dilution_texture_and_service.md`, mirroring the existing
pillar-source convention.

Extending balance and ingredients beats adding `cocktail-balance` and `cocktail-ingredients`:
the rescue-table logic and the functional-role model are genuinely shared, and two skills that
disagree about what "acid" means is a worse failure than one skill with two sections.

### Hooks

| Hook | Change |
|---|---|
| `state_validate` | `PRECURSORS` becomes domain-aware. The hook already parses the full `State`, so it reads `domain` for free. |
| `phase_check` | **none** — keep the `recipe.md` filename for drinks. Renaming to `spec.md` costs a regex change, a hook change, and test churn, to buy a nicer noun. |

### Tests

New coverage: domain-aware family drift, the `check_strength` rule and its ABV arithmetic,
the orgeat/nut regression specifically, `PRECURSORS` branching, schema round-trip with
`domain` present and absent, and a cocktail sample session under `sessions/`.

The existing `sessions/2026-04-28-pinto-beans-sample/state.yaml` doubles as the food-path
regression fixture for the `chef.md` extraction.

---

## Milestones

**M1 — walking skeleton.** Schema, domain-aware conflicts, the orgeat fix, `check_strength`,
`.claude/domains/cocktail.md`, `/bar`, a thin `cocktail-technique` pillar covering dilution and
method only, one sample session. Ships a working Daiquiri / Negroni / Old-Fashioned path.

**M2 — depth.** Full pillar 4. Balance and ingredients cocktail sections. ENHANCE's physics
lens rewritten for dilution, temperature, and texture. Batching math.

**M3 — reach.** Zero-proof promoted from a constraint to a first-class path. Cross-domain
pairing (design a drink for the dish from the previous session — the schema already supports
it, since both sessions are just state files). Clarification and carbonation.

The `chef.md` → `domains/food.md` extraction lands in M1 because everything after it assumes
the spine is domain-agnostic; doing it later means doing it twice.

---

## Non-goals

- **Bar inventory / stock modeling.** Matches the existing "availability is the user's call"
  principle. The user doesn't pick what they don't have.
- **Wine, beer, coffee.** Coffee is a plausible third domain later; it is not this change.
- **Nutrition or standard-drink health guidance.**
- **Anything that makes the food path worse.** The extraction must be behavior-neutral.

---

## Risks

| Risk | Mitigation |
|---|---|
| `chef.md` extraction regresses the food path | Extract verbatim, no rewording in the same commit; sample session as the regression fixture |
| Confabulated dilution numbers in pillar 4 | Reuse the existing ENHANCE confidence discipline — `HIGH` requires named literature (Arnold's *Liquid Intelligence*, *Cocktail Codex*, Meehan). Cooking has McGee and Kenji as anchors; cocktails must cite equivalently or mark `MEDIUM`. |
| Scope creep into a bar-inventory app | Non-goals above are load-bearing |
| The agent now outputs alcohol quantities | `abv_ceiling` is a real hard constraint, a standard-drink line goes in the spec sheet, and the zero-proof path is a first-class option rather than a degraded one |

---

## Open questions

1. **`/bar`, `/pour`, or `/bartender`?** `/bar` reads best next to `/chef` and is the shortest
   to type.
2. **Is zero-proof a constraint or a domain?** This proposal makes it `abv_ceiling: 0.0` on the
   cocktail domain. The argument for a third domain is that zero-proof technique diverges
   sharply (acid adjustment, verjus, tea tannin standing in for ethanol's body). Deferred to M3
   on purpose — M1 will show whether the constraint model strains.
3. **Does `chef` stay the agent name?** The frontmatter description gains drinks either way.
   Renaming the agent is a bigger blast radius than the feature warrants.

---

## Verification notes

Every claim above marked *verified* was checked by executing against `c28fa73`:

- `filter --role base_spirit` returning both split-base candidates with no prune
- `orgeat` producing no finding under a declared `nuts` exclusion, while `almond syrup` produces
  `allergy_hard_filter`
- `State.model_validate` rejecting an unknown `domain` key under `extra="forbid"`
- `python -m pytest -q` → 53 passed
