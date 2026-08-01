# Culinary Agent Knowledge Base — Overview & Skill Mapping

**Purpose.** This document set is the foundational research for a culinary AI agent. Pillars 1–3 cover what the agent must know about ingredients, transformation, and balance in a dish. Pillar 4 is the drink-side parallel: the same reasoning applied to a glass. This overview file explains how the pillars fit together, how to decompose them into discrete skills, and how the agent should route incoming user requests to the right pillar at runtime.

**Total content:** ~68,000 words across four pillars (≈225 pages of dense reference at standard formatting).

---

## The Four-Pillar Architecture

The knowledge base is organized around the operations a culinary agent performs whenever it builds, modifies, or critiques something a person will consume. Pillars 1–3 are the three operations performed in sequence on a dish. Pillar 4 runs the same three operations on a drink, and is a parallel structure rather than an extension of the first three:

| # | Pillar | Question it answers | Medium | File |
|---|--------|---------------------|--------|------|
| 1 | **Ingredient Taxonomy & Flavor Profiles** | *What does this ingredient bring to the dish, and what does it pair with?* | dish | `01_ingredient_taxonomy_and_flavor_profiles.md` |
| 2 | **Technique & Transformation** | *How will heat, time, and pressure change my ingredients?* | dish | `02_technique_and_transformation.md` |
| 3 | **Flavor Theory & Balancing Rules** | *Is the dish balanced, and if not, how do I fix it?* | dish | `03_flavor_theory_and_balancing.md` |
| 4 | **Beverage Craft: Cocktails & Bar Prep** | *What template is this drink, what fills each slot, what does cold water do to it, and what has to be made in advance?* | drink | `04_beverage_craft_and_dilution.md` |

Pillars 1–3 are sequential in a normal cooking workflow (choose ingredients → cook them → taste and adjust), but the agent can enter at any pillar depending on the user's question.

Pillar 4 is not a fourth step in that sequence. It is the whole sequence again in a different medium, which is why it is a single document covering selection, transformation, and balance for drinks rather than three parallel documents. The agent selects between the food pillars and the drink pillar on the session's medium, and the two sets do not mix: a drink is not a dish with liquor in it, and the food pillars have nothing correct to say about dilution, ABV, or a split base.

---

## Pillar 1 — Ingredient Taxonomy & Flavor Profiles (≈11,800 words)

**Scope.** A global ingredient ontology that describes ingredients by *what they contribute*, not just what category they belong to. Built around three lenses: aromatic foundations, flavor affinities, and functional roles.

### Section map

1. **Aromatic Foundations** — 11 global bases with chemistry: French mirepoix, Italian soffritto, Spanish/Latin sofrito (with regional variants), Cajun/Creole holy trinity, Chinese ginger-scallion-garlic, Indian onion-ginger-garlic + tadka, Thai curry pastes (red/green/yellow), Japanese dashi/aromatic logic, Mexican onion-garlic-tomato-chile + recados, West African tomato-pepper-onion + Maggi, Middle Eastern/North African onion-garlic-spice with ras el hanout/baharat/advieh. Each base includes ingredient ratios, build technique, and the underlying chemistry (sulfur compounds in alliums, terpenes in carrots/celery, pyrazine development from gentle browning).
2. **Flavor Affinities** — extensive pairing tables for 20+ base ingredients (proteins, starches, vegetables, fruits, chocolate). Both classical traditions (lamb + rosemary; black beans + cumin + epazote; tomato + basil) and the molecular logic (shared volatile aromatic compounds, foodpairing theory, Niki Segnit's structure).
3. **Functional Categories** — ingredients grouped by what they *do* in a dish:
   - **Acid** (vinegars, citrus, fermented dairy, tamarind, sumac, verjuice) with pH and dominant acid type
   - **Fat** (oils by smoke point and flavor, animal fats, dairy fats) with fatty acid profile
   - **Salt** (sea salts, fermented salts: soy, fish sauce, miso, anchovy) with sodium + glutamate content
   - **Umami** (parmesan, tomato, mushroom, kombu, dashi, cured meats) with explicit glutamate/IMP/GMP synergy math
   - **Heat / Pungent** (capsaicin, piperine, isothiocyanates, gingerol, sansho) with mechanism
   - **Sweet** (sugars, honey, maple, mirin, caramelized vegetable sugars) with relative sweetness data

### Suggested skill decompositions

This pillar's content cleanly splits into 3–5 separate skills, depending on how granular you want to go:

| Skill | What it does | Source sections |
|-------|--------------|-----------------|
| `aromatic-base-builder` | Given a target cuisine, prescribe the right aromatic foundation, ratios, and build technique. | Section 1 (Aromatic Foundations) |
| `flavor-pairing-lookup` | Given an ingredient, return traditional partners + molecular pairing rationale. | Section 2 (Flavor Affinities) |
| `functional-substitution` | Given a dish that needs more *acid / fat / salt / umami / heat*, return ranked substitutions across cuisines. | Section 3 (Functional Categories) |
| `umami-amplifier` | Detect umami-poor dishes; prescribe glutamate + nucleotide combinations exploiting the 8× synergy effect. | Section 3.4 (Umami) |
| `cuisine-translator` | Convert a dish from one cuisine to another by swapping aromatic base + functional category sources while preserving role. | Cross-section |

---

## Pillar 2 — Technique & Transformation (≈13,500 words)

**Scope.** How heat, time, and pressure change the chemistry of ingredients. The agent must reason about *what ingredients become*, not just what they are.

### Section map

1. **Maillard Reaction & Caramelization** — the two browning pathways. Maillard chemistry (140–165°C / 285–330°F): amino acid + reducing sugar → pyrazines, thiazoles, melanoidins. Caramelization chemistry (160–190°C / 320–375°F): pure sugar pyrolysis. The contrast: low-heat sweating (releasing sugars without browning) vs. high-heat char-sautéing (Maillard + Strecker degradation for bitter/complex notes). 10+ worked global examples — French onion soup, dry-roasting Indian/Mexican spices, deglazing fond, dulce de leche, soy sauce production, Cantonese wok hei, Indian bhuna, Mexican blackened chiles.
2. **State Changes & Structural Breakdown** — slow braising (collagen → gelatin at 70–80°C / 160–180°F over hours); pressure cooking (same chemistry at 115–120°C / 240–250°F, ~3× faster); confit; sous-vide (precise enzymatic + collagen control); pickling and fermentation (lactobacillus pH drop); curing (osmotic dehydration); smoking (phenols + drying); nixtamalization (alkaline corn). Worked dishes: French boeuf bourguignon, Italian osso buco, Mexican barbacoa, Indian dum, Korean galbi-jjim, Chinese hong shao rou, North African tagine.
3. **Emulsification & Reduction** — emulsion chemistry (oil-in-water vs water-in-oil; surfactants: lecithin, mustard mucilage, sodium caseinate, hydrocolloids). Classical emulsions: mayonnaise, hollandaise, vinaigrette, beurre blanc, aioli, romesco, mole, Indian masala, Thai coconut curry. Broken emulsion failure modes and recovery. Reduction: Maillard happening *in* the liquid, glutamate concentration, gelatin viscosity, demi-glace, jus, Italian ragù evaporation, Indian bhuna's "oil-splitting" doneness signal.
4. **Troubleshooting & Decision Trees** — 4 troubleshooting tables (too-thin sauces, too-thick or broken sauces, emulsions that won't form, dishes lacking depth) + a braising decision tree.
5. **Cross-Cultural Applications** — Maillard, slow-cooking, and emulsification techniques mapped across 8+ regional cuisines.

### Suggested skill decompositions

| Skill | What it does | Source sections |
|-------|--------------|-----------------|
| `browning-strategist` | Given an ingredient and a desired flavor outcome, prescribe target temp, time, and visual cues. | Section 1 |
| `protein-tenderizer` | Given a protein cut (collagen content, fat content), recommend braise / pressure-cook / sous-vide / dry-heat with target temps and times. | Section 2 |
| `emulsion-doctor` | Diagnose broken emulsions and prescribe rescue (yolk re-emulsion, lecithin add, water drizzle). | Section 3 + Section 4 troubleshooting |
| `reduction-coach` | Calculate target reduction levels by viscosity / volume / glutamate concentration. Prevent over-reduction. | Section 3 |
| `state-change-explainer` | Educational mode — explain what's happening chemically when a user describes a technique. | All sections |

---

## Pillar 3 — Flavor Theory & Balancing Rules (≈16,700 words)

**Scope.** How to diagnose and fix off-balance dishes, how to layer flavors for depth, and the timing rules that keep aromatics alive.

### Section map

1. **The Five Basic Tastes and Beyond** — sweet, salty, sour, bitter, umami + pungent/heat, astringency, numbing (sansho/Sichuan), aroma, mouthfeel — receptor mechanisms for each.
2. **The Four Cardinal Elements** — Salt, Fat, Acid, Heat (per Samin Nosrat).
3. **The Counterbalancing Framework** — relative balance, interactions between tastes (salt suppresses bitter; fat carries fat-soluble aromatics; acid brightens).
4. **The Master Rescue Table** — 8-row × 6-column lookup for "if dish is too X, add Y" with primary, secondary, and tertiary remedies. *This is the agent's most-used table.*
5. **Global Flavor Balance Philosophies** — Thai *rot* chart (sweet/salty/sour/spicy), Sichuan *má-là* (numbing-spicy), Indian masala layering, Mexican picante-fresco, Japanese kuchidoke, Vietnamese fish-sauce-lime-sugar-chili balance.
6. **Flavor Layering** — base → body → brightness → finishing framework.
7. **Layering the Same Ingredient in Different Forms** — garlic (raw, sautéed, confit, roasted, fried, black, powder); same logic for onion, tomato, citrus, chile.
8. **Staggered Timing** — when to add aromatics, whole vs ground spices, salt (early/late/finishing), acid (mostly late).
9. **Aromatic Volatility Hierarchy** — what evaporates first and what that means for timing.
10. **Salt Mechanics in Depth** — diffusion timing, wet vs dry brining, salt as flavor amplifier.
11. **Acid Mechanics in Depth** — acid as brightener and tenderizer; timing.
12. **Fat Mechanics in Depth** — fat as flavor carrier (fat-soluble aromatics); fat to mute heat.
13. **The Umami Amplification Layer** — glutamate + nucleotide synergy worked in detail (8× amplification).
14. **Bitter and Astringent Perception** — distinguishing bitterness from astringency; PROP-taster genetics.
15. **Professional Tasting Protocol** — the spoon-and-adjust loop, palate cleansers, five-question diagnostic.
16. **Decision Trees and Diagnostic Flowcharts** — quick-reference 9-row table of common flavor problems.

### Suggested skill decompositions

This is the most skill-rich pillar. Suggested splits:

| Skill | What it does | Source sections |
|-------|--------------|-----------------|
| `dish-doctor` | The flagship. User says "my dish tastes flat / too salty / too sweet" → agent runs the rescue table and prescribes a fix sequence. | Section 4 (Master Rescue Table) + Section 16 |
| `flavor-layering-coach` | Given a recipe, suggest where to add same-ingredient variants for depth. | Sections 6 & 7 |
| `timing-sequencer` | Given a recipe, reorder ingredient additions so volatiles survive and salt has time to penetrate. | Sections 8 & 9 |
| `cuisine-balance-checker` | Given a target cuisine (Thai, Sichuan, Mexican, Japanese), score the dish against that cuisine's balance philosophy. | Section 5 |
| `tasting-protocol-trainer` | Walk a user through the spoon-and-adjust loop step by step. | Section 15 |
| `umami-stack-builder` | Construct multi-source umami stacks exploiting glutamate + nucleotide synergy. | Section 13 |

---

## Pillar 4 — Beverage Craft: Cocktails & Bar Prep (≈25,900 words)

**Scope.** Alcoholic mixed drinks, from structural template through service, plus the days-scale preparations the drinks depend on. Coverage is cocktails and bar prep: build methods, dilution and ABV arithmetic, drink templates, sweetener ratios, infusions, syrups, cordials, fat-washing, batching, and clarification. **Fermentation, brewing, winemaking and distillation are deliberately out of scope** — this pillar reasons about what a bartender does with finished bottles, not about how the bottles were made.

**Units and conventions.** US fluid ounces with metric alongside (1 fl oz = 29.6 mL). ABV is percent by volume; US proof is exactly 2 × ABV. Dilution is stated throughout as **water added as a percentage of the pre-dilution liquid volume**, not as a percentage of the finished drink. Every figure in the pillar is an arithmetic identity, a definitional ratio, a published physical constant, or a range from bar practice explicitly labelled as a range.

### Section map

1. **Drink Families & Structural Templates** — the six roots (Old Fashioned, Martini, Daiquiri, Sidecar, Whisky Highball, Flip) and the nine working families built on them: sour, spirit-forward/stirred, highball, tiki, flip/fizz, sparkling, punch, aperitivo/spritz. Each family gets its skeleton, typical ratio, method, ice, glass, expected dilution and finished ABV band, consolidated into a Master Template Comparison table plus a seven-question template selector.
2. **Base Spirits — Structural and Aromatic Taxonomy** — gin, whiskey, rum, agave, brandy, and the neutral/regional group (vodka, aquavit, cachaça, shochu, soju), each read on three axes: **proof, congener load, wood contribution**. Closes with a Base Spirit → Template Fit grid. The load-bearing design rule: higher proof and higher congener load carry *more* sugar, not less, and a high-phenol spirit belongs in a split base before it gets a full pour.
3. **Modifiers, Sweeteners & the Bitter Axis** — the eight functional roles in a glass and which of them stack; fortified and aromatized wines; amari and bitter liqueurs; liqueurs by aromatic register; **explicit allergen screening lists** covering nuts, dairy, egg, gluten, sulfites and the savory paths, with the false friends named in both directions; sweeteners by ratio, sugar-per-mL, viscosity and shelf life; acids by titratable acidity and pKa; bitters and why stacking them is correct; hidden sugar accounting; substitution within a role.
4. **Balance & the Drink Rescue Table** — the drink-side analog of Pillar 3's Master Rescue Table. Symptom rows (too boozy, too sweet, too sour, too bitter, watery, flat, cloying, thin, not cold enough, muddy) against primary, secondary and tertiary fixes with the cost of each. Includes the diagnostic order — temperature, then dilution, then sweet/sour, then bitterness and aroma, then rebuild — and worked rescues.
5. **Dilution, Temperature & ABV Math** — the core quantitative section. Chilling and dilution are one variable, not two: the cooling is paid for by melting ice and the melt goes in the glass. Energy accounting from the latent heat of fusion; freezing-point depression by mixture ABV; typical dilution by method; ice format and surface-area-to-volume; the ABV calculation with worked examples; glassware chilling; standard drinks by jurisdiction.
6. **Build Methods** — stirred, shaken, dry shake, reverse dry shake, whip shake, throwing, rolling, building in glass, carbonated builds, blending, swizzling, each with its mechanical justification, and a ten-row decision rule applied in order where the first match wins.
7. **Bar Prep Projects** — thirteen preparations with ratio, active time, elapsed time, shelf life and failure mode: the syrup family and water activity, infused syrups, oleo-saccharum, orgeat, falernum, cordials and acid-adjusted citrus, shrubs, spirit infusions, fat-washing, milk clarification, batching, carbonation, and a Prep Board that ranks them by character bought per hour spent.
8. **Glassware, Garnish, and Service** — glass shape as work rather than decoration, garnish as an aromatic ingredient (with the removal test that separates ingredient from theatre), rim treatments, station service order, and a glass-and-garnish quick reference by family.

### Suggested skill decompositions

This pillar ships as a **single skill** (`beverage-craft`) rather than a split, because the sections are more tightly coupled than the food pillars are: you cannot choose a build method without knowing the template, and you cannot compute the finished ABV without knowing the build method. The table below records the seams if a future split is wanted.

| Skill | What it does | Source sections |
|-------|--------------|-----------------|
| `drink-template-selector` | Given a rough brief, name the family, its skeleton, its ratio, its method and its expected finished ABV. | Section 1 |
| `dilution-and-abv-calculator` | Compute pre-dilution ABV, the dilution the method implies, finished ABV, finished volume, and standard-drink count. | Section 5 |
| `build-method-chooser` | Given the ingredient list, return shake / stir / build / throw / roll / whip / swizzle / blend with the mechanical reason. | Section 6 |
| `drink-doctor` | The flagship, and the direct analog of `dish-doctor`. User says "too boozy / too sweet / watery / flat" → run the rescue table in diagnostic order. | Section 4 |
| `bar-prep-planner` | Given a drink and a time budget, return the preps it needs with ratios, elapsed times, shelf lives and what to cut first. | Section 7 |
| `batching-calculator` | Scale a single-serve spec to N servings with the dilution water measured in rather than shaken in, and check the finished ABV against the freezing-point table. | Sections 5 and 7.11 |
| `bar-allergen-screen` | Screen a spec for nut, dairy, egg, gluten, sulfite and savory (shellfish / fish / soy / pork) exposure by ingredient identity rather than by string-matching the name, including the gluten distillation asymmetry and the false-friend list. | Section 3.5 |

### Why this pillar needs its own structures, not the food ones

Recorded here because it is the reason the fourth pillar exists as a parallel rather than as additional sections bolted onto Pillars 1–3:

- **There is no aromatic base.** Pillar 1's organizing question is which aromatic foundation a cuisine uses. A drink has a *base spirit* instead, and the analogy holds structurally (it is the thing every other decision is measured against) while the content shares nothing.
- **Two intensity axes, not one.** Food carries a single heat axis. A drink carries **strength** and **sweetness** independently, and a drink that is wrong on one is fixed by a different move than a drink that is wrong on the other.
- **Water is an ingredient.** Dilution is a designed quantity in a glass in a way it is not in a braise, which is why it is a functional role of its own and why Section 5 is arithmetic rather than prose.
- **Some roles stack and some do not.** Two rums in the base slot and two bitters in a build are canonical construction, not redundancy — but two dry vermouths in the same slot are a mistake. The distinguishing variable is bar-product class, not intensity, and no food structure encodes it.
- **Allergen exposure hides behind product names.** Orgeat is almond, falernum is almond in most formulations, Amaretto is apricot kernel, Frangelico is hazelnut, Nocino is walnut, crème de noyaux is stone-fruit kernel. None of them contain a nut word. Conversely, distillation leaves gluten protein behind in the wash, so a rye whiskey is not a gluten exposure the way a beer is. A screen built on ingredient names alone is wrong in both directions.

---

## Cross-pillar workflows

Pillars 1–3 are designed to compose. The agent rarely uses just one — typical multi-pillar workflows:

**Workflow: Build a new dish from scratch**
1. Pillar 1: pick the aromatic base appropriate for the target cuisine and protein.
2. Pillar 1: pick complementary ingredients via flavor affinities.
3. Pillar 2: choose technique (braise vs sear vs poach) given the protein's collagen/fat profile.
4. Pillar 3: plan timing — when does each aromatic / spice / acid go in?
5. Pillar 3: at the end, run the tasting protocol and the rescue table if needed.

**Workflow: Fix a broken dish**
1. Pillar 3 first: run the Master Rescue Table to identify the imbalance.
2. Pillar 1: pick the *specific* ingredient to add (e.g., "needs umami" → which umami source pairs with this cuisine?).
3. Pillar 2 if structural: emulsion broken? sauce too thin? — go to Pillar 2 troubleshooting.

**Workflow: Translate a dish across cuisines**
1. Pillar 1: identify functional roles in the source dish (which ingredient is the acid? the fat? the umami?).
2. Pillar 1: substitute each role with the target cuisine's equivalent (rice vinegar → lime; olive oil → coconut milk; parmesan → fish sauce).
3. Pillar 1: swap aromatic base.
4. Pillar 3: re-balance using the target cuisine's balance philosophy.

**Workflow: Explain *why* a recipe works**
1. Pillar 1: chemistry of the ingredients and base.
2. Pillar 2: chemistry of what cooking does to them.
3. Pillar 3: the balance and layering logic.

---

## Drink workflows (Pillar 4)

Pillar 4 does not compose with Pillars 1–3; it replaces them. The agent picks a medium first and then stays on one side of the line. What follows are the drink-side equivalents of the workflows above, all of them running inside Pillar 4's own sections.

**Workflow: Build a new drink from scratch**
1. Section 1: run the template selector on the brief — citrus? aromatized wine? carbonation? egg or dairy? split base? batched?
2. Section 2: pick the base spirit on proof, congener load and wood, and check it against the template fit grid.
3. Section 3: fill the remaining roles, subtracting the sugar and ethanol already contributed by the modifiers before setting the syrup volume.
4. Section 6: the build method falls out of the ingredient list, not out of preference.
5. Section 5: compute pre-dilution ABV, the dilution the method implies, the finished ABV, the finished volume and the standard-drink count.
6. Section 7: identify what has to be made in advance, and cut from the bottom of the Prep Board if the time budget will not carry it.
7. Section 8: size the glass to the *post-dilution* volume, choose the ice format, and apply the removal test to the garnish.

**Workflow: Fix a drink that tastes wrong**
1. Section 4 first, and work the diagnostic order: temperature, then dilution, then sweet/sour, then bitterness and aroma, then rebuild. A large share of reported imbalance is a temperature failure wearing a costume.
2. Section 5 if the symptom is watery, hot, or thin — that is dilution and ice, and it is arithmetic.
3. Section 3 if the symptom is sweetness or sourness — convert everything to grams of sugar and percent acid before adjusting anything.
4. Adjust in units the palate can resolve: 0.125 oz of syrup or citrus, one dash of bitters, two drops of saline, five seconds of agitation. Taste between adjustments.

**Workflow: Substitute an ingredient without breaking the drink**
1. Section 3: identify the slot the ingredient occupies and its three numbers — **ABV, sugar, aromatic register**.
2. Substitute something that preserves those three, or correct the deviation elsewhere in the build.
3. Section 5: re-run the ABV math if the substitution moved proof or volume.
4. If the substitution is being made for an allergy, surface it to the drinker rather than making it silently. An orgeat-less Mai Tai is a different drink and the drinker should be the one to choose it.

**Workflow: Scale a drink to a crowd**
1. Section 5: compute the single-serve finished ABV and volume first, including dilution.
2. Section 7.11: multiply, and **measure the dilution water in** rather than shaking it in. This is the only method where dilution is exact.
3. Check the batch's finished ABV against the freezing-point table before promising freezer service: fully liquid above roughly 35%, syrupy to slushy between about 25% and 35%, frozen below 25%.
4. Section 8: pre-chill glassware and sequence the round from most durable to most perishable.

---

## How to convert each pillar into a SKILL.md

When you take a pillar (or a skill-sized section of one) and turn it into an Anthropic-style skill, the structure should be:

```
skills/<skill-name>/
  SKILL.md          # short, action-oriented; references the reference doc
  reference.md      # the dense knowledge (subsection of the pillar)
  examples/         # 3-10 worked example dish files
```

**SKILL.md should contain:**
- A description aggressive enough to trigger correctly (e.g., for `dish-doctor`: "Use this whenever the user describes a dish that tastes wrong — flat, too salty, too sweet, etc.")
- A 5–10 step decision procedure that points the agent to the right table or worked example in `reference.md`
- One or two minimal worked examples inline
- Explicit instruction to consult `reference.md` for the master tables

**reference.md should contain:**
- The lookup tables verbatim from the pillar
- The chemistry / mechanism explanations
- Decision trees in markdown table form

**examples/ should contain:**
- Worked rescues / pairings / techniques as standalone files the skill can cite

The pillars in this knowledge base are already structured for this — every section has tables (lookup), worked examples (illustrations), and decision rules (the "if X then Y" sentences). When you split a pillar, the natural seams are the H2 headers.

**What actually shipped.** Each of the four pillars became exactly one skill rather than the 3–5 suggested above: `culinary-ingredients`, `culinary-technique`, `culinary-balance`, `beverage-craft`. The decomposition tables are kept as a record of the seams, not as a plan. Each skill is a `SKILL.md` of procedures pointing at anchors in a `reference.md` that is the pillar document itself, and no skill ships an `examples/` directory — the worked examples stayed inline in the reference where the procedures could cite them by anchor.

---

## File manifest

| File | Purpose | Words | Skill | Status |
|------|---------|-------|-------|--------|
| `00_overview_and_skill_mapping.md` | This file — roadmap and skill conversion guide | ~4,200 | — | Complete |
| `01_ingredient_taxonomy_and_flavor_profiles.md` | Pillar 1 — ingredient ontology, pairings, functional roles | 11,821 | `culinary-ingredients` | Complete |
| `02_technique_and_transformation.md` | Pillar 2 — Maillard, state changes, emulsions, reduction | 13,526 | `culinary-technique` | Complete |
| `03_flavor_theory_and_balancing.md` | Pillar 3 — balance, layering, timing, tasting protocol | 16,698 | `culinary-balance` | Complete |
| `04_beverage_craft_and_dilution.md` | Pillar 4 — drink templates, dilution and ABV math, build methods, bar prep | 25,902 | `beverage-craft` | Complete |

**Total:** ≈72,200 words.

Each numbered pillar file is preserved here as the source of record for its skill's `reference.md`. The skill directory holds the working copy the agent loads; this directory holds the research document it came from. For Pillars 1–3 the two copies are byte-identical. Pillar 4's copy here closes with a References & Sources and Document Metadata section, matching the other three pillar documents; the skill's working copy does not carry that tail.

---

## Recommended next steps

1. **Read Pillars 1–3 in order** — they build on each other; later pillars assume the vocabulary established in earlier ones. Pillar 4 is free-standing and can be read on its own, though it borrows the rescue-table and layering vocabulary from Pillar 3 and the functional-role vocabulary from Pillar 1.
2. **Pick the skill seams** — for each pillar, look at the suggested decomposition table above and decide whether to split into multiple skills or keep as one large skill with sub-procedures.
3. **Write SKILL.md files** — for each skill, write a tightly scoped SKILL.md whose description triggers reliably and whose body is a procedure rather than knowledge. Push knowledge to `reference.md`.
4. **Build the example library** — extract the worked examples currently embedded in each pillar into standalone example files the skills can cite.
5. **Test triggering** — once skills exist, write evaluation prompts (typical user requests) and verify the right skill triggers without over-triggering on adjacent topics.

The skill-creator skill is well-suited to step 3; once you have this knowledge base loaded into a context, you can have the agent help write the SKILL.md files itself, using `01_ingredient_taxonomy_and_flavor_profiles.md` (etc.) as the source-of-truth reference.
