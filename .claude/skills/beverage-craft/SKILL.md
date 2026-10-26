---
name: beverage-craft
description: Use when designing or fixing a cocktail or any other mixed drink — picking a drink family or template (sour, spirit-forward / stirred, highball, tiki, flip or fizz, sparkling, punch, aperitivo / spritz), choosing a base spirit or a modifier, calculating dilution, ABV, or standard drinks, choosing a build method (shake vs. stir vs. build vs. throw vs. swizzle vs. blend), diagnosing a drink that tastes too boozy / too sweet / too sour / watery / flat, screening a drink for hidden allergens (nut, dairy, egg, gluten, sulfite, or a savory shellfish / fish / soy / pork path), or planning bar prep (syrup ratios, oleo-saccharum, orgeat, falernum, cordials, shrubs, infusions, fat-washing, milk clarification, batching, carbonation, glassware and garnish).
---

# Beverage Craft

Reasoning about drinks: what template a drink is, what fills each slot, what cold water does to it, and what has to be made days before service.

## When the chef agent calls this skill

Invoked in the GROUNDING, RESEARCH, SYNTHESIZE, and GUIDE phases whenever the medium is a drink — and any time the user reports a taste problem in a glass. Match the question to one of the procedures below.

### "What kind of drink is this / what template should I build on?"
1. Open `reference.md` → **Drink Families & Structural Templates** (`#drink-families`)
2. Run the seven-question template selector at the end of the section (citrus? aromatized wine? carbonation? egg or dairy? split base? base under 25% ABV? batched for a group?)
3. Return: the family, its skeleton, the typical ratio, the method, the ice, the glass, the expected dilution, and the finished ABV band — the Master Template Comparison table has all seven in one row
   - Sour · spirit + sugar + citrus · 2 : 0.75 : 0.75 · shake
   - Spirit-forward · Old Fashioned root (spirit + sugar + bitters) or Martini root (spirit + aromatized wine) · stir
   - Highball · 1 part spirit : 2–4 parts carbonation · build
   - Tiki · split base + multiple acids + compound sweetener · whip shake over crushed
   - Flip / fizz · spirit + sugar + egg or dairy · dry shake then wet
   - Sparkling · concentrated base topped with wine · shake the base, top, never shake the bubbles
   - Punch · 1 sour : 2 sweet : 3 strong : 4 weak, dilution designed in
   - Aperitivo / spritz · bitter liqueur or aromatized wine in the base slot, 6–12% finished

### "Which base spirit, and what does it change?"
1. Open `reference.md` → **Base Spirits — Structural and Aromatic Taxonomy** (`#base-spirits`)
2. Read the spirit on three axes: **proof**, **congener load**, **wood contribution**
3. Check the Base Spirit → Template Fit grid at the end of the section before committing
4. Return: the style, its ABV, its dominant compounds, and the design consequence — higher proof and higher congener load carry *more* sugar, not less; a high-phenol spirit (mezcal, peated Scotch) belongs in a split base at 0.25–0.75 oz before it gets a full pour

### "What goes in the non-base slots?"
1. Open `reference.md` → **Modifiers, Sweeteners & the Bitter Axis** (`#modifiers-sweeteners-bitter-axis`)
2. Fill the roles the drink still needs: `base`, `modifier`, `sweetener`, `acid`, `bitters`, `lengthener`, `texture`, `aromatic garnish`
3. **`base`, `modifier`, `bitters`, and `acid` are stackable roles** — two rums in the base slot and two bitters in a build are canonical construction, not redundancy. Say so explicitly when returning candidates, so nothing downstream prunes them
4. Before setting the syrup volume, subtract the sugar already in the glass — liqueurs run ~250 g/L, crème de cassis ≥400, sweet vermouth ~150, PX sherry 350–500
5. Return: candidates per role with ABV, sugar load, and aromatic register, plus what each substitution would cost

### "Screen this drink for an allergy or an exclusion"
1. Open `reference.md` → **Allergen and Exclusion Screening** (`#allergen-screening`) and read the list for the category asked about: nuts, dairy, egg, gluten, sulfites, or the savory paths (shellfish, fish, soy, pork, beef)
2. **Never screen by string-matching the ingredient name.** It fails in both directions, and both failures are silent:
   - *Hidden exposure* — orgeat (almond), falernum (almond), Amaretto (apricot kernel), Frangelico (hazelnut), Nocino (walnut), crème de noyaux (stone-fruit kernel), Baileys and RumChata (dairy cream), clarified milk punch (whey), Clamato (clam broth), Worcestershire (anchovy), any fat-washed spirit (whatever fat it was washed with) — none carry the allergen word
   - *False alarm* — cream sherry, cream of coconut, crème de anything, ginger beer, root beer, Fish House Punch, the Prairie Oyster, Beefeater. Do not remove these
3. **Gluten is asymmetric and the asymmetry is the answer.** Beer, ale, stout and any beer cocktail are real exposures. A spirit distilled from a gluten grain is not one in the same way — the protein stays in the wash, which is why FDA and TTB both allow a "gluten-free" claim on it since 2020, while a merely *fermented* product may only say "processed to remove gluten". Flag whiskey, bourbon, rye and grain vodka as an ambiguous path with the mechanism stated; never delete them silently
4. Return the conflict to the drinker with a named substitute and its cost (toasted seed or toasted-rice orgeat; rich syrup + lime zest + clove + ginger for falernum). Do not silently delete a load-bearing ingredient — an orgeat-less Mai Tai is a different drink and the drinker should choose it

### "How much water, how cold, and how strong is it?"
1. Open `reference.md` → **Dilution, Temperature & ABV Math** (`#dilution-temperature-abv`)
2. Chilling and dilution are **one variable, not two** — the cooling is paid for by melting ice, and the melt goes in the glass
3. Compute: ethanol_oz = Σ(volume × ABV); ABV_final = ABV_pre ÷ (1 + dilution); standard drinks = ethanol_oz ÷ 0.6 (US)
4. Return: pre-dilution ABV, the dilution the method implies (stirred 20–25%, shaken 25–30%, whip 10–15%, built 5–10%, swizzle 25–35%, blended 50%+), the finished ABV, the finished **volume** so the glass can be sized to it, and the standard-drink count

### "Shake or stir?"
1. Open `reference.md` → **Build Methods** (`#build-methods`) and apply the ten-row decision rule in order — the first rule that matches wins
2. The short form: carbonation overrides everything (build, add bubbles last, one vertical spoon lift); frozen → blend; egg or dairy with a wanted foam → dry or reverse dry shake; citrus, juice, purée, cream → shake hard 8–15 s and double-strain; savory and pulpy → throw or roll; crushed-ice service with heavy syrups → whip shake; everything-is-spirit → stir 25–35 s
3. Return: the method, the duration, the strainer, and the mechanical reason (needs emulsifying / needs aerating / must not be agitated)

### "This drink tastes wrong"
**This is the flagship use.** Always start here when the user describes a problem in the glass.

1. Open `reference.md` → **Balance & the Drink Rescue Table** (`#drink-rescue-table`)
2. Work the diagnostic order — **temperature, then dilution, then sweet/sour, then bitterness and aroma, then rebuild.** Half of reported imbalance is a temperature failure wearing a costume
3. Find the symptom row: too boozy / too sweet / too sour / too bitter / watery / flat / too dilute / not cold enough / muddy / cloying / thin
4. Return: primary, secondary, and tertiary fixes **with the cost of each**, and instruct the user to taste between adjustments — adjust in units of 0.125 oz syrup or citrus, 1 dash of bitters, 2 drops of saline, 5 seconds of agitation

### "What do I need to make in advance?"
1. Open `reference.md` → **Bar Prep Projects** (`#bar-prep-projects`)
2. Return the prep with its ratio, active time, elapsed time, shelf life, and failure mode — syrups, infused syrups, oleo-saccharum, orgeat, falernum, cordials and acid-adjusted citrus, shrubs, spirit infusions, fat-washing, milk clarification, batching, carbonation
3. If the design needs more prep than the user has time for, cut from the bottom of the Prep Board — rich demerara syrup and oleo-saccharum buy the most character per hour; carbonated bottling and orgeat buy the least
4. For a **batch**: never omit the dilution water. Pre-measure it, then check the finished ABV against the freezing-point table before promising freezer service

### "How is it served?"
1. Open `reference.md` → **Glassware, Garnish, and Service** (`#glassware-garnish-service`)
2. Return: glass (sized to the *post-dilution* volume), ice format, garnish, and rim treatment
3. Apply the garnish test — **remove it and see whether a blind taster notices.** An expressed peel is an ingredient; the same peel dropped in unexpressed is decoration

## Worked example
Guest wants "something with mezcal, not too strong, a little bitter."
- **Template**: no citrus → the selector goes to step 2, and 0.75 oz of sweet vermouth is an aromatized wine in a structural quantity (≥0.5 oz), so it stops there: **Martini root**, stirred (`#drink-families`). Structurally this is a mezcal Negroni with a split base. It is *not* the aperitivo family — that requires the bitter liqueur or aromatized wine to **replace** the base spirit and finish at 6–12%
- **Base**: mezcal is high-phenol → split base, 0.75 oz mezcal against 0.75 oz blanco tequila, not a full 2 oz (`#base-spirits`)
- **Modifiers**: Campari 0.75 oz (bitterness 7, ~24%) + sweet vermouth 0.75 oz (~150 g/L sugar) → **no added syrup**; the vermouth is the sweetener (`#modifiers-sweeteners-bitter-axis`)
- **Math**: ethanol = 0.75×0.45 + 0.75×0.40 + 0.75×0.24 + 0.75×0.16 = 0.94 oz in 3.0 oz = 31% pre-dilution; stirred at 22% → **25.6% finished**, 3.7 oz in the glass, 1.6 US standard drinks (`#dilution-temperature-abv`)
- **Check that against the brief**: 25.6% is spirit-forward, not "not too strong" — the classification did not fix the strength, the arithmetic did. Lengthen instead: build the same 3 oz over ice with 2 oz soda in a wine glass → ~5.3 oz at **~17–18%** (`#build-methods`)
- **If the guest wants the actual aperitivo band** (6–12%): the bitter has to take the base slot, not sit beside it. 0.5 oz mezcal as an accent, 1 oz Campari, 1 oz sweet vermouth, 3 oz soda → 0.63 oz ethanol in ~5.9 oz = **~10–11%** (`#drink-families`)
- **Service**: wine glass, large cubes, expressed grapefruit peel — load-bearing, since grapefruit oil bridges the mezcal and the Campari (`#glassware-garnish-service`)

## Reference

The full template tables, spirit taxonomies, dilution and ABV arithmetic, rescue table, prep formulas, and worked examples live in `reference.md`. **When you read a section, cite the H2 heading and the anchor** so the user can verify the recommendation against source. Every dilution figure in this skill is stated as water added *as a percentage of the pre-dilution volume*; keep that convention when reporting.
