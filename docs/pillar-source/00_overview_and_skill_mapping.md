# Culinary Agent Knowledge Base — Overview & Skill Mapping

**Purpose.** This document set is the foundational research for a culinary AI agent. The three pillars below cover what the agent must know about ingredients, transformation, and balance. This overview file explains how the three pillars fit together, how to decompose them into discrete skills, and how the agent should route incoming user requests to the right pillar at runtime.

**Total content:** ~42,000 words across three pillars (≈140 pages of dense reference at standard formatting).

---

## The Three-Pillar Architecture

The knowledge base is organized around the three operations a culinary agent performs in sequence whenever it builds, modifies, or critiques a dish:

| # | Pillar | Question it answers | File |
|---|--------|---------------------|------|
| 1 | **Ingredient Taxonomy & Flavor Profiles** | *What does this ingredient bring to the dish, and what does it pair with?* | `01_ingredient_taxonomy_and_flavor_profiles.md` |
| 2 | **Technique & Transformation** | *How will heat, time, and pressure change my ingredients?* | `02_technique_and_transformation.md` |
| 3 | **Flavor Theory & Balancing Rules** | *Is the dish balanced, and if not, how do I fix it?* | `03_flavor_theory_and_balancing.md` |

The pillars are sequential in a normal cooking workflow (choose ingredients → cook them → taste and adjust), but the agent can enter at any pillar depending on the user's question.

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

## Cross-pillar workflows

The pillars are designed to compose. The agent rarely uses just one — typical multi-pillar workflows:

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

---

## File manifest

| File | Purpose | Words | Status |
|------|---------|-------|--------|
| `00_overview_and_skill_mapping.md` | This file — roadmap and skill conversion guide | ~1,800 | Complete |
| `01_ingredient_taxonomy_and_flavor_profiles.md` | Pillar 1 — ingredient ontology, pairings, functional roles | 11,821 | Complete |
| `02_technique_and_transformation.md` | Pillar 2 — Maillard, state changes, emulsions, reduction | 13,526 | Complete |
| `03_flavor_theory_and_balancing.md` | Pillar 3 — balance, layering, timing, tasting protocol | 16,698 | Complete |

**Total:** ≈43,800 words.

---

## Recommended next steps

1. **Read the three pillars in order** — they build on each other; later pillars assume the vocabulary established in earlier ones.
2. **Pick the skill seams** — for each pillar, look at the suggested decomposition table above and decide whether to split into multiple skills or keep as one large skill with sub-procedures.
3. **Write SKILL.md files** — for each skill, write a tightly scoped SKILL.md whose description triggers reliably and whose body is a procedure rather than knowledge. Push knowledge to `reference.md`.
4. **Build the example library** — extract the worked examples currently embedded in each pillar into standalone example files the skills can cite.
5. **Test triggering** — once skills exist, write evaluation prompts (typical user requests) and verify the right skill triggers without over-triggering on adjacent topics.

The skill-creator skill is well-suited to step 3; once you have this knowledge base loaded into a context, you can have the agent help write the SKILL.md files itself, using `01_ingredient_taxonomy_and_flavor_profiles.md` (etc.) as the source-of-truth reference.
