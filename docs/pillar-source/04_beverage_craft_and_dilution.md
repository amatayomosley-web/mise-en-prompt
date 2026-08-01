# Pillar 4: Drink Craft — Cocktails and Bar Prep

How a mixed drink is structured, chilled, diluted, balanced, and prepped for in advance.

This pillar is the drink-side parallel to the three food pillars. Where those reason about
ingredients, transformations, and balance in a dish, this one reasons about the same four
questions in a glass: what structural template is this drink, what fills each slot, what does
cold water do to it, and what has to be built days in advance. Coverage is cocktails and bar
prep. Fermentation and brewing are deliberately out of scope.

**Scope**: drink families and templates, base spirits, modifiers and sweeteners, balance and
rescue, dilution/temperature/ABV arithmetic, build methods, bar prep projects, service.
**Units**: US fluid ounces with metric alongside; 1 fl oz = 29.6 mL. ABV is percent by volume.
**Dilution convention**: throughout this document, dilution is stated as **water added as a
percentage of the pre-dilution liquid volume**, not as a percentage of the finished drink.

---

## Table of Contents {#table-of-contents}

1. [Drink Families & Structural Templates](#drink-families)
2. [Base Spirits — Structural and Aromatic Taxonomy](#base-spirits)
3. [Modifiers, Sweeteners & the Bitter Axis](#modifiers-sweeteners-bitter-axis)
4. [Balance & the Drink Rescue Table](#drink-rescue-table)
5. [Dilution, Temperature & ABV Math](#dilution-temperature-abv)
6. [Build Methods](#build-methods)
7. [Bar Prep Projects — Syrups, Cordials, Infusions, Clarification, Batching](#bar-prep-projects)
8. [Glassware, Garnish, and Service](#glassware-garnish-service)

---

## Section 1: Drink Families & Structural Templates {#drink-families}

A cocktail is not a recipe; it is a *template* with substitutions. Every durable drink in the canon resolves to a small number of structural skeletons — a base spirit, a sweetening agent, an acid or an aromatized wine, a bittering agent, and a controlled quantity of water. Once the skeleton is identified, the ingredients become interchangeable within their structural slot, and the drink can be reasoned about rather than memorized. This is the central claim of *Cocktail Codex: Fundamentals, Formulas, Evolutions* (Alex Day, Nick Fauchald, David Kaplan, 2018), which reduces the entire modern repertoire to **six root templates**: the Old Fashioned, the Martini, the Daiquiri, the Sidecar, the Whisky Highball, and the Flip. Everything below is an elaboration of those roots plus two structures the six-root frame deliberately folds inward (tiki and punch), which are worth treating separately because their *split-base* and *batch* logic behaves differently under substitution.

### 1.1 The Six Roots and What Each One Actually Controls

| Root | Structural formula | The variable it isolates | Canonical exemplar |
|---|---|---|---|
| Old Fashioned | spirit + sugar + bitters + water | Spirit expression; sweetness as a *lengthening* agent, not a flavor | Old Fashioned, Sazerac, Improved Whiskey Cocktail |
| Martini | spirit + fortified/aromatized wine (+ bitters) | Aromatic wine as the diluent *and* the flavoring | Martini, Manhattan, Negroni, Martinez |
| Daiquiri | spirit + citrus + sugar | The sour axis; acid-to-sugar ratio | Daiquiri, Margarita, Whiskey Sour, Gimlet |
| Sidecar | spirit + citrus + liqueur (sugar carried *by* the liqueur) | Sweetener that also contributes flavor and alcohol | Sidecar, White Lady, Corpse Reviver No. 2, Last Word |
| Whisky Highball | spirit + carbonated lengthener | Carbonation, temperature, and dilution as texture | Whisky Highball, Gin & Tonic, Americano, Spritz |
| Flip | spirit + sugar + egg (and/or dairy) | Protein and fat as texture; emulsification | Flip, Whiskey Sour w/ egg white, Ramos Gin Fizz, Alexander |

The practical consequence for design: **a substitution is safe when it stays in its slot and preserves the slot's numbers.** Swapping Cointreau (40% ABV, ~250 g/L sugar) for simple syrup in a sour is not a one-for-one move — it changes both the sugar load and the alcohol load, which is why the Sidecar is a separate root from the Daiquiri rather than a variation on it.

### 1.2 The Sour Family {#template-sour}

**Formula:** base spirit : sweetener : fresh citrus, at roughly **2 : 0.75 : 0.75 to 2 : 1 : 0.75 (fl oz)**.

The historical form is usually quoted as **8 : 4 : 3** (strong : sweet : sour) — 2 oz spirit, 1 oz sweet, 0.75 oz sour — a reading of the sours in Jerry Thomas's 1862 *Bar-Tender's Guide*. Modern house specs run drier. *Death & Co: Modern Classic Cocktails* (Kaplan, Fauchald, Day, 2014) standardizes on a 2 oz base with 0.75 oz each of citrus and 1:1 simple syrup. Difford's Guide, which publishes several competing specs per drink rather than one, shows the same family spread across a band from bone dry to the period ratio; that spread is the point, not any single number in it.

**Why it holds together:** citrus juice is not just acid — lime runs **5–7% titratable acidity** (typically ~6%, mostly citric with a malic fraction), lemon **5–6%** citric, grapefruit **1.5–2.5%**, orange under **1%**. Sugar and acid suppress each other's perception nearly symmetrically, so the drink is stable across a band of ratios rather than balanced at a point. What actually fixes the ratio is the *base spirit's* congener load and proof: a 40% white rum needs less sugar to read as balanced than a 50% overproof or a phenolic mezcal, because sweetness is also doing the work of masking ethanol burn.

- **Daiquiri** — base + lime + 1:1 simple. Shake, fine strain, coupe. The template with nothing hidden in it, which is why it is the reference sour; if a bar's Daiquiri is wrong, its ice, its citrus, or its syrup is wrong.
- **Margarita** — base + lime + orange liqueur, with a small agave-syrup patch if the liqueur runs dry. Technically a Sidecar-root drink, since the liqueur carries the sugar.
- **Whiskey Sour** — base + lemon + simple, optional egg white. The high congener load of a whiskey base is what lets the drink carry the full template sweetener dose — 0.75 oz against a 2 oz base — without reading sweet; a lighter, lower-congener base in the same slot has to run drier to stay in balance.
- **Gimlet** — base + lime + simple. Substituting a bottled lime cordial changes the drink into a different (older) structure entirely.

**Failure modes:** bottled citrus (cooked, no volatiles, wrong acid balance); citrus juiced more than ~4 hours ahead (lime degrades fastest — its aroma flattens within hours even refrigerated); under-shaking, which leaves the drink warm *and* under-diluted at the same time.

### 1.3 The Spirit-Forward / Stirred Family {#template-stirred}

Two distinct roots, both stirred, both served without citrus, and both frequently confused.

**Old Fashioned root — spirit + sugar + bitters + water.**
A base pour, a small dose of rich (2:1) syrup or its equivalent in undissolved sugar, and bitters at dash scale, stirred; the family ratio, method, ice and glass are in §1.10. Sugar here is a *textural* agent rather than a flavor: it raises viscosity and rounds the ethanol edge without announcing itself, which is why this root's sweetener slot runs at roughly a third of what the sour template carries and why a correct build still reads dry. Bitters supply the aromatic top note and a trace of bitterness that keeps the sweetness from cloying; they are themselves spirits — the aromatic style runs **44.7% ABV** and the anise-cherry style **35%** (§3.8) — so even at dash scale they belong in the ABV arithmetic (§5.3). The **Sazerac** is the same root rebuilt on a higher-proof base, with an anise-spirit rinse and anise-cherry bitters in place of the aromatic ones.

**Martini root — spirit + aromatized/fortified wine.**
The wine is simultaneously the diluent (it is 15–18% ABV, so it lowers final strength) and the flavoring (it brings botanicals, oxidative notes, and residual sugar). Vermouth ratios have dried steadily over a century: Harry Craddock's *The Savoy Cocktail Book* (1930) specifies the Dry Martini as **equal parts** dry gin and French vermouth; the modern default sits near **5:1 to 3:1**. Audrey Saunders' Pegu Club-era wet Martini specs deliberately walked that back toward the historical range.

| Drink | Structure, by role | Root | Approx. finished ABV |
|---|---|---|---|
| Old Fashioned | base + rich sugar + aromatic bitters | Old Fashioned | ~32–35% |
| Sazerac | high-proof base + rich sugar + anise-cherry bitters + absinthe rinse | Old Fashioned | ~35–38% |
| Martini | base + dry aromatized wine at a dry ratio + orange bitters | Martini | ~34–35% |
| Manhattan | base + sweet aromatized wine at roughly 2:1 + aromatic bitters | Martini | ~27–30% |
| Negroni | base + red bitter aperitivo + sweet aromatized wine, equal parts | Martini | ~22–24% |
| Boulevardier | the Negroni structure on a whiskey base, base slot slightly long | Martini | ~23–25% |
| Martinez | lightly sweetened base + sweet aromatized wine at roughly 1:1 + maraschino accent + bitters | Martini | ~24–27% |

Every figure in the last column is the pre-dilution ABV divided by the stirred dilution band (20–25%), not an estimate: a Martini-root build carrying 1.265 oz of ethanol in 3 oz is 42% in the mixing glass and 33.7–35.1% in the glass. The full arithmetic is worked in §4, and the identity itself in §5.3. That makes the last column a **check on your own arithmetic**: a spec that "should" be a Martini but computes to 30% has more vermouth or more water in it than the row says, and a spec that should be a Negroni and computes to 30% is not an equal-parts build.

**Why stirring, not shaking:** the goal is a clear, dense, cold drink with no aeration. Shaking a spirit-forward drink introduces air bubbles that scatter light, raises the surface area for volatile loss, and produces ice shards. Stirred drinks land near **−7 to −3 °C** at roughly **20–25% dilution** (of the pre-dilution volume — the convention used throughout this document); shaken drinks land colder, **−8 to −4 °C**, and wetter, **25–30%**. Dave Arnold's argument in *Liquid Intelligence* (2014) is that these two numbers are *coupled and not independently adjustable* with ice alone: nearly all the cooling energy comes from the latent heat of fusion of melting ice (334 J/g) rather than from warming the ice itself (~2 J/g·K), so you cannot get a drink much colder without also getting it more dilute. Decoupling them requires pre-chilling, pre-dilution, or batching and freezing.

### 1.4 The Highball Family {#template-highball}

**Formula:** 1 part spirit : **2 to 4 parts** carbonated lengthener, built in the glass over ice, no agitation beyond a single lift.

| Drink | Lengthener | What the lengthener contributes besides volume | Finished ABV |
|---|---|---|---|
| Japanese Whisky Highball | Soda water | Nothing but carbonation and cold — the driest reading of the template, and the one that leaves the base fully exposed | ~9–11% |
| Gin & Tonic | Tonic | Quinine bitterness *and* **~7–9 g/100 mL sugar**; the lengthener is also the sweetener, so nothing else in the build should be | ~11–14% |
| Cuba Libre | Cola + lime | Sugar, caramel color, phosphoric acid and its own spice load; the base recedes to a supporting voice | ~10–12% |
| Americano | Soda water | Only volume and carbonation — the bitterness and the sugar already sit in the base slot (§1.9) | ~9–11% |
| Paloma | Grapefruit soda + lime + salt | Sugar, a second acid against the citric, and salt acting as a bitterness suppressor (§4.1) | ~11–13% |

**Why carbonation is structural, not decorative.** Dissolved CO₂ is converted to carbonic acid at the tongue by **carbonic anhydrase IV** expressed on sour-sensing taste cells, and it independently stimulates trigeminal receptors. Carbonation is therefore simultaneously an *acid*, a *tactile irritant*, and a *volatile carrier* — bursting bubbles eject aroma into the nasal cavity. Sparkling water typically sits at **pH 3.9–5.0**. This is why a highball needs less added acid than an equivalent-strength still drink, and why a flat highball tastes not just dull but noticeably *sweeter*.

**Carbonation care.** The physics (Henry's law, the solubility-versus-temperature table, and the full build procedure) is in §6.9; the template-level consequences are:
- Chill everything — spirit, mixer, glass, ice — to near freezing before assembly. A warm glass is the single largest cause of a flat highball.
- Soda water carries roughly **3.5–4.5 volumes** of CO₂; Champagne roughly **4.5–6 volumes** (≈5–6 atm at 20 °C).
- Minimize nucleation sites: pour down the side, use large clear ice with low surface area, stir once at most. Every stir costs carbonation.
- Because the mixer supplies most of the water, highballs need **little or no ice-melt dilution** — 5–10% at service. Build over the fewest, largest, coldest cubes available.

### 1.5 Tiki / Tropical {#template-tiki}

Tiki is a sour that has been deliberately over-complicated in three specific ways, each of which is a real structural move rather than ornament.

1. **Split base.** Two or more rums occupy the *same* structural slot to produce an aroma profile no single rum has: a high-ester Jamaican pot-still rum for fruit and funk, plus an aged Demerara for caramel, molasses, and body. This is the defining move of the form — pruning it as redundancy destroys the drink.
2. **Multiple acids.** Lime plus grapefruit, or lime plus passion fruit, layering citric against the malic/tartaric profile of tropical fruit for a longer, less spiky acid curve.
3. **Compound sweeteners.** Orgeat (almond syrup with orange flower water) contributes sugar, fat/emulsion body, and benzaldehyde-driven almond aroma at once. Falernum (lime, clove, ginger, almond, rum; John D. Taylor's Velvet Falernum is ~11% ABV) contributes sugar, spice, and a small alcohol load.

| Drink | Structure, by role | Structural note |
|---|---|---|
| Mai Tai (Trader Vic, 1944) | base + lime + orange liqueur + nut orgeat + rich sugar | Originally one 17-year J. Wray & Nephew; split base is the standard modern reconstruction |
| Jungle Bird | dark base + red bitter aperitivo + pineapple + lime + simple | Bitter aperitivo in a tropical frame; the outlier that proves the template |
| Zombie | triple-split base (gold + dark + overproof) + lime + a grapefruit-cinnamon syrup + falernum + grenadine, with absinthe and bitters at drop scale | Triple-split base and two acid sources; the ceiling of the form |
| Painkiller | dark base + pineapple + orange + cream of coconut, grated nutmeg | Fat-and-sugar route to body instead of an acid-forward route |

Jeff "Beachbum" Berry's archival work (*Sippin' Safari*, *Beachbum Berry Remixed*) is the source for the reconstructed Don the Beachcomber specs, including the Zombie; treat any tiki spec without that provenance as a modern interpretation. Tiki drinks are **flash-blended or whip-shaken with crushed ice**, which pushes dilution above the shaken norm — often **30–35% at service, and still climbing in the glass** — which is precisely what makes a 4 oz pour of spirit drinkable.

### 1.6 Flip, Fizz, and Dairy/Egg {#template-flip}

Three doses of the same ingredient, each a different structural job. **Whole egg (flip):** one whole egg per drink, against a base slot and a small rich-syrup dose (ratio in §1.10) — maximum body, moderate foam, and the only form that needs no other texture agent. **Egg white (sour foam):** 0.75–1 white per drink added to a standard sour — foam and a protein mouth-coating, no added richness. **Yolk only:** maximum richness and emulsification, minimum foam.

**Mechanism.** A large egg white is ~33 g, of which ~3.5 g is protein — principally ovalbumin (~54%), ovotransferrin (~12%), ovomucoid (~11%), plus globulins and lysozyme. Agitation denatures these at the air–water interface, where they unfold and cross-link into a viscoelastic film around each air cell. Ethanol is a *surfactant* and destabilizes that film, which is why cocktail foams are far less stable than a meringue and why very high-proof drinks foam poorly. Yolk contributes lecithin (phosphatidylcholine) and lipoproteins, which emulsify fat rather than trapping air; cream contributes fat globules that add viscosity and mouth-coating and blunt both acid and ethanol perception.

**Technique.** Egg and foam builds are the one place where the *order* of agitation is the recipe. Dry shake, reverse dry shake, and how to choose between them are treated in §6.3 and §6.4.

**Raw egg safety — state this plainly and never hedge it into invisibility.**
- Commonly cited US figures put *Salmonella* Enteritidis contamination near **1 in 20,000 shell eggs**. Acid and alcohol in a cocktail do **not** reliably sterilize; a Whiskey Sour's pH (~3.2–3.5) and ~15–18% ABV are insufficient for a meaningful log reduction in the seconds-to-minutes of service.
- **In-shell pasteurized eggs** (held below coagulation temperature long enough for a ~5-log reduction) foam nearly as well and remove the hazard. They are the correct default for anyone immunocompromised, pregnant, elderly, or very young.
- Aquafaba (chickpea liquid, ~1 oz per drink) and commercial foamers (methylcellulose or modified starch blends) are structurally valid substitutes; they foam via different mechanisms and give a slightly drier, less rich head.

**Canonical exemplars, by what each one adds to the sour or flip root:** the **Whiskey Sour with egg white** and the **Pisco Sour**, both the sour template plus a white, the latter finishing with aromatic bitters dashed on the foam as an orthonasal top note the drinker meets before the first sip; the **Ramos Gin Fizz**, a split-citrus sour carrying cream *and* egg white plus orange flower water and soda — the long shake is doing emulsification work, not theater; the **Brandy Alexander**, the dairy route to the same texture, where cream replaces the egg entirely and the equal-parts structure of §1.10 makes the liqueur carry both the sweetening and the flavor; and the **Brandy Flip**, the whole-egg root with nothing else in it.

### 1.7 Champagne and Sparkling-Wine Cocktails {#template-sparkling}

**Formula:** a small, concentrated, *already-balanced* base of 1.5–2.5 oz, lengthened with 2–3 oz sparkling wine.

The sparkling wine occupies the highball's lengthener slot but is not neutral: it brings **11–12.5% ABV**, its own acidity (tartaric and malic, typically pH 2.9–3.2 — notably more acidic than soda water), autolytic bready aroma from lees contact, and a dosage-determined sugar load. EU labeling terms are exact and worth using as a design dial:

| Term | Residual sugar (g/L) |
|---|---|
| Brut Nature / zero dosage | 0–3 |
| Extra Brut | 0–6 |
| Brut | 0–12 |
| Extra Dry / Extra Sec | 12–17 |
| Sec | 17–32 |
| Demi-Sec | 32–50 |
| Doux | 50+ |

Because Brut already contributes up to 12 g/L sugar and real acidity, a sparkling cocktail needs **less added sugar and less added acid** than the equivalent still drink. Build the base in a shaker or mixing glass, strain into a chilled flute or coupe, then top — never shake anything carbonated.

- **French 75** — a compact gin base + lemon + simple, lengthened with sparkling wine. (Cognac in the older reading.)
- **Old Cuban** (Audrey Saunders) — aged-rum base + lime + simple + aromatic bitters + mint, shaken, strained, and lengthened with sparkling wine. A mojito and a sparkling cocktail resolved into one structure.
- **Death in the Afternoon** (Hemingway) — a high-proof anise base lengthened with sparkling wine. Structurally a two-ingredient highball, and a deceptively strong one; see the worked check below.
- **Champagne Cocktail** — a bitters-saturated sugar cube in the flute, lengthened with sparkling wine. The Old Fashioned root run on wine.

**Worked check — the base-slot proof trap.** This template is the one place where the format lies about the strength, so run the arithmetic on the base-slot band above before trusting it. Take a 1.5 oz pour of a 60% base plus 4.5 oz of sparkling wine at ~12%, which together fill a 6 oz flute (§8.1): that is 0.9 + 0.54 = 1.44 oz of ethanol in 6 oz — **24% finished**, and **20–28%** across the full 45–74% band of the anise-spirit category in §3.4. That is a Martini-strength drink wearing a sparkling-cocktail costume, not a 15% aperitif. The lengthener cannot rescue it either: even at the bottom of that range, landing the drink at 18% would take 6.75 oz of sparkling wine on top of the 1.5 oz pour (10.5 oz at 60%), which is more than a flute holds. Any base-slot spirit above about 45% behaves the same way here, and the glass runs out of room before the arithmetic does — which is the general lesson, and the reason the 1.5–2.5 oz base-slot band above is a ceiling rather than a suggestion.

### 1.8 Punch {#template-punch}

The oldest mixed-drink structure in English, and the ancestor of the sour. The mnemonic is **"one of sour, two of sweet, three of strong, four of weak"** — 1 part citrus : 2 parts sugar : 3 parts spirit : 4 parts water/tea — with a **fifth element, spice** (nutmeg, clove, cinnamon, or tea tannin), which is why the word is often traced to the Sanskrit/Hindi *pañc*, "five." David Wondrich's *Punch: The Delights (and Dangers) of the Flowing Bowl* (2010) is the standard history and the source for most reconstructed period specs.

**Structural properties that make punch different from a scaled-up cocktail:**
- **Dilution is designed in, not melted in.** The "four of weak" is pre-measured water or tea, so the punch can be built ahead and chilled with a single large block of ice that melts slowly. This is the historical ancestor of modern batching.
- **Oleo-saccharum is the sugar slot.** Citrus peels macerated with sugar for 1–12 hours; the sugar osmotically draws the peel's essential oils (limonene, citral, linalool) into a thick, intensely aromatic syrup. This gives punch an aromatic top note that a citrus-juice-only drink cannot reach, and it uses the peels of the fruit you are already juicing.
- **Tea as the weak.** Tannin supplies astringency and structure that plain water cannot, and keeps a large-format sweet drink from reading flabby.
- **Finished strength lands low** — a 1:2:3:4 punch with a 40% spirit computes to roughly **12% ABV before ice melt**, appropriate for a drink served by the cup over an evening.

Modern practice runs drier than the mnemonic (the "two of sweet" reflects period sugar-in-syrup conventions and 18th-century palates); **1 : 1 : 3 : 4** is a reasonable contemporary starting point.

### 1.9 Low-ABV Aperitivo and Spritz {#template-aperitivo}

A family defined by *what replaces the base spirit*: a bitter liqueur or aromatized wine at 11–25% ABV occupies the base slot, and the drink finishes in the **6–12% ABV** band — wine strength, not cocktail strength.

The consequence for volume is the thing most builds get wrong. Because the base is running at a third to a half of a spirit's strength, **the base slot takes a long 2–3 oz pour here, not the 1.5–2.5 oz of a spirit base (§3.1)** — and it still finishes at wine strength rather than at cocktail strength, because a longer pour of a weaker base is exactly what lands the drink in the 6–12% band. Pour a low-ABV base at spirit volumes and the drink comes out thin and short; the family ratio and glass are in §1.10.

| Drink | Structure, by role | Bittering agent (ABV) | Finished ABV |
|---|---|---|---|
| Aperol Spritz (IBA) | low-bitter, heavily sugared aperitivo in the base slot, lengthened with sparkling wine and a splash of soda, over ice | Aperol (11%) | ~7–9% |
| Americano | bitter aperitivo + sweet vermouth sharing the base slot, lengthened with soda | Campari (20.5% IT / 24% US) | ~9–11% |
| Bicicletta | bitter aperitivo + dry white wine, lengthened with soda; the wine does the work sparkling wine does in a spritz, without the carbonation | Campari | ~9–11% |
| Sherry Cobbler | oxidative sherry at a long base pour + a small sugar dose + fruit, crushed ice | — (amontillado 17–19%) | ~10–13% |
| Cynar Spritz | vegetal artichoke amaro in the base slot, lengthened with sparkling wine and soda | Cynar (16.5%) | ~8–10% |
| Adonis | biological sherry + sweet vermouth sharing the base slot + orange bitters, no lengthener at all — which is why it finishes highest in the family | — | ~15–16% |

**Why it works.** Bitterness is doing the structural job that ethanol does in a spirit-forward drink: it provides the astringent, palate-clearing counterweight that keeps sugar from dominating. The bittering compounds are real and named — **quinine** in tonic, **gentiopicroside** in gentian (Suze, Aperol's bitter backbone), **cynarin** in artichoke (Cynar), **absinthin** in wormwood-based vermouths, and citrus-peel **naringin/limonin** in the Campari family. Because these liqueurs are already sweetened (Aperol and Campari both carry substantial residual sugar), the aperitivo family usually needs **no added sweetener at all** — adding syrup on top is the most common way to wreck one.

### 1.10 Master Template Comparison {#template-comparison}

| Family | Skeleton | Typical ratio | Method | Ice | Glass | Dilution (% of pre-dilution vol.) | Finished ABV |
|---|---|---|---|---|---|---|---|
| Sour | spirit + sugar + citrus | 2 : 0.75 : 0.75 | Shake | Fine-strain, up or rocks | Coupe / rocks | 25–30% | 16–20% |
| Sidecar (liqueur sour) | spirit + liqueur + citrus | 1.5 : 0.75 : 0.75 | Shake | Fine-strain, up | Coupe | 25–30% | 20–25% |
| Old Fashioned | spirit + sugar + bitters + water | 2 : 0.25 : 2 ds | Stir, or build in glass | Large rock | Rocks | 20–25% stirred; 5–10% at service if built | 32–38% |
| Martini root | spirit + aromatized wine | 5:1 to 1:1 | Stir | Up | Coupe / Nick & Nora | 20–25% | 22–35% |
| Highball | spirit + carbonation | 1 : 2–4 | Build | Large cubes, tall | Collins / highball | 5–10% | 9–14% |
| Tiki | split base + multi-acid + compound sweet | 2–4 oz total spirit | Whip / flash blend | Crushed | Tiki mug / Collins | 30–35% at service | 14–20% |
| Flip / dairy | spirit + sugar + egg/cream | 2 : 0.5 : 1 egg | Dry + wet shake | Fine-strain | Coupe / fizz | 25–30% | 12–18% |
| Sparkling | concentrated base + sparkling wine | 2 : 2–3 | Shake base, top | Up or cubes | Flute / coupe | 10–20% | 12–16% |
| Punch | 1 sour : 2 sweet : 3 strong : 4 weak | scaled batch | Pre-batch | One large block | Punch cup | designed in | 10–14% |
| Aperitivo / spritz | bitter liqueur + wine + soda | 3 : 2 : 1 | Build | Cubes | Wine glass | 5–15% | 6–12% |

### 1.11 Template Selection

1. **Is there citrus?** Yes → sour axis (§1.2) or Sidecar root if a liqueur carries the sugar. No → go to 2.
2. **Is there an aromatized or fortified wine in a structural quantity (≥0.5 oz)?** Yes → Martini root (§1.3). No → go to 3.
3. **Is there carbonation?** Yes → highball (§1.4) if the lengthener is soda/tonic/cola; sparkling (§1.7) if it is wine. No → go to 4.
4. **Is there egg or dairy?** Yes → flip/fizz (§1.6), and resolve the pasteurization question before proceeding. No → go to 5.
5. **More than one spirit in the base slot, plus a compound sweetener?** Yes → tiki (§1.5); expect higher dilution and crushed ice. No → go to 6.
6. **Is the alcoholic base under 25% ABV?** Yes → aperitivo/spritz (§1.9). No → Old Fashioned root (§1.3).
7. **Is it built for more than four people ahead of service?** Overlay punch logic (§1.8) on whichever template answered above: pre-measure the dilution, batch, and chill with one block.

---

## Section 2: Base Spirits — Structural and Aromatic Taxonomy {#base-spirits}

The base spirit occupies the same structural position in a drink that the protein or the aromatic base occupies in a dish: it sets the ceiling on intensity and dictates what everything else must accommodate. Three axes describe a base spirit for design purposes.

- **Proof / ABV.** Sets the finished strength and, critically, the *sweetener requirement*. Ethanol is perceived as both sweet and burning; a higher-proof base needs more sugar to read as balanced, not less.
- **Congener load.** Congeners are everything other than ethanol and water — higher alcohols (fusel oils), esters, aldehydes, acids, phenols. A low-congener spirit (vodka, korui shochu, column-still rum) is transparent and needs the drink to supply aroma. A high-congener spirit (Jamaican pot rum, mezcal, peated Scotch, cachaça) supplies the aroma itself and will overwrite delicate modifiers.
- **Wood contribution.** Oak contributes **vanillin** (vanilla), *cis*- and *trans*-**oak lactones** (coconut, "whiskey lactone"), **furfural** and other furans (caramel, toasted), **eugenol** (clove), and hydrolyzable **tannins** (astringency, structure). Charring caramelizes hemicellulose into color and sweetness; toasting without charring favors spice. Aged spirits therefore carry a *built-in sweetness signal* and usually need less added sugar than their unaged counterparts.

### 2.1 Gin {#spirit-gin}

Neutral spirit redistilled with botanicals, juniper predominant. US minimum **40% ABV (80 proof)**; EU minimum **37.5%**. Navy strength is **57% ABV (114 US proof)**.

| Botanical | Key compounds | Contribution |
|---|---|---|
| Juniper berry | α-pinene, myrcene, sabinene, limonene | Resinous, piney, the legally required backbone |
| Coriander seed | Linalool (often 60–70% of the seed oil) | Citrus-floral lift; the second botanical in nearly every gin |
| Angelica root | Macrocyclic musk lactones | Earthy, dry; acts as an aromatic *fixative*, binding volatiles together |
| Orris root | Irones | Violet, powdery; the other classical fixative |
| Citrus peel | Limonene, citral | Bright top note; volatile and fades fastest in the bottle |
| Licorice / cassia / cardamom | Glycyrrhizin, cinnamaldehyde, 1,8-cineole | Sweetness without sugar, warm spice, cooling |

**Styles.**
- **London Dry** — all flavoring introduced by distillation, no post-distillation sweetening beyond a trace, no added color. Juniper-forward and dry. *Suits:* Martini, Negroni, Gimlet, Gin & Tonic, French 75. The default.
- **Plymouth** — a geographic designation; earthier, softer, more root-driven, less juniper-dominant. 41.2% ABV. *Suits:* wetter Martinis, Gimlets.
- **Old Tom** — lightly sweetened (or barrel-rested); the historical bridge between genever and London Dry. *Suits:* Martinez, Tom Collins, Ramos Gin Fizz — anywhere a bit of body helps.
- **Contemporary / "New Western"** — juniper subordinated to citrus, floral, or cucumber vectors (Hendrick's 41.4%, Aviation 42%). *Suits:* highballs and light sours. *Fails:* Negroni and Martini, where juniper is doing structural work against the vermouth or Campari.
- **Genever** — malt-wine base, closer to an unaged whiskey with botanicals; oude vs jonge by malt-wine content. *Suits:* Improved Holland Gin Cocktail, Old Fashioned root.

### 2.2 Whiskey {#spirit-whiskey}

Mashbill and cask are the two dials. Grain sets the *sweetness-versus-spice* axis; cask sets vanilla, tannin, and body.

| Type | Legal spine | Typical ABV | Dominant character | Suits |
|---|---|---|---|---|
| Bourbon | ≥51% corn; distilled ≤160 proof; barreled ≤125 proof; **new charred oak**; bottled ≥80 proof | 40–50%+ | Corn sweetness + heavy new-oak vanillin/lactone/caramel | Old Fashioned, Whiskey Sour, Boulevardier, Mint Julep |
| Wheated bourbon | Bourbon with wheat as the flavoring grain | 45–50% | Softer, rounder, less spice | Old Fashioned where the spirit should recede |
| Rye (US) | ≥51% rye; otherwise as bourbon | 40–50%+ | Pepper, mint, and a distinct **dill** note at high rye content | Manhattan, Sazerac, Vieux Carré |
| Scotch (single malt) | Malted barley, ≥3 years in oak in Scotland, ≥40% | 40–46%+ | Malt, orchard fruit; ex-bourbon → vanilla, ex-sherry → dried fruit | Rob Roy, Penicillin, Blood & Sand |
| Peated Scotch | As above, malt dried over peat | 40–48% | **Guaiacol, cresols, phenol** — measured as ppm phenol in the malt (Laphroaig ~40, Ardbeg ~55, Octomore >100) | Split base, rinses, Penicillin float |
| Irish | Usually triple-distilled, ≥3 years | 40–46% | Light, smooth; **single pot still** (malted + unmalted barley) adds a creamy, spicy grip | Irish Coffee, highballs, light sours |
| Japanese | Scotch-modeled; JSLMA 2021 standards require mashing, fermentation, distillation and ≥3 years' aging in Japan | 43–48% | Precise, floral; **Mizunara** oak adds sandalwood and incense | The Highball, above all else |

**Design rule:** the higher the rye content and the higher the proof, the more sugar the drink can carry without reading sweet. A 100-proof rye tolerates a full 1 oz of sweet vermouth in a stirred build; an 80-proof blended whiskey in the same slot goes flabby.

### 2.3 Rum {#spirit-rum}

The most structurally varied category in the bar, and the one where "rum" as a single ingredient label is least useful. Two independent variables: **feedstock** (molasses vs. fresh cane juice) and **still** (pot vs. column).

| Style | Feedstock / still | ABV | Character | Suits |
|---|---|---|---|---|
| Spanish-style light | Molasses / column, filtered | 40% | Clean, faintly sweet, low congener | Daiquiri, Mojito, highballs |
| Jamaican pot still | Molasses / pot, long fermentation, often dunder | 40–63% | **Esters** — ethyl acetate, ethyl butyrate, ethyl hexanoate: banana, pineapple, overripe fruit. This is *hogo* (from *haut goût*) | Tiki split base, Mai Tai, Jungle Bird |
| Demerara (Guyana) | Molasses / wooden Coffey and double wooden pot stills | 40–75.5% | Caramel, molasses, smoke, heavy body | Tiki split base, Zombie, punch |
| Rhum agricole (AOC Martinique) | **Fresh cane juice** / column, bottled ≥40% | 40–55% | Grassy, vegetal, olive-brine, mineral | Ti' Punch, Daiquiri variations, agricole highball |
| Aged / añejo | Either, oak-aged, often solera | 40–45% | Vanilla, dried fruit, oak tannin | Old Cuban, rum Old Fashioned, Manhattan variations |
| Blackstrap / overproof | Molasses / column, dosed or high-strength | 40–75.5% | Burnt sugar, bitter molasses; overproof used as a float | Jungle Bird, Zombie float, punch |

Jamaican ester intensity is measured in **grams per hectoliter of pure alcohol (g/hLPA)** and formalized in trade classes: *Common Clean* ~80–150, *Plummer* ~150–200, *Wedderburn* ~200–300, *Continental Flavoured* up to the Jamaican legal ceiling of **1600 g/hLPA**. This is why a "split base" of Jamaican and Demerara is a real structural decision and not a duplication: one supplies volatile esters, the other supplies body and caramel, and neither is a substitute for the other.

### 2.4 Agave {#spirit-agave}

| Style | Definition | ABV | Character | Suits |
|---|---|---|---|---|
| Blanco / plata tequila | Blue Weber agave, unaged or ≤2 months | 38–46% (40% typical export) | Cooked agave, black pepper, citrus, wet earth | Margarita, Paloma, Tommy's, Batanga |
| Reposado | 2–12 months oak | 38–46% | Agave + light vanilla; the bridge | Tequila Old Fashioned, Rosita |
| Añejo / extra añejo | 1–3 years / 3+ years, ≤600 L barrels | 38–46% | Oak-dominant; agave recedes | Sipping; Manhattan-root substitutions |
| Mezcal | NOM 070; any permitted agave, agave roasted in earthen pits over wood | 40–55% (traditional often 45–48%) | **Smoke phenols (guaiacol, syringol)** over the agave base; enormous varietal range | Split base, rinses, Naked & Famous, mezcal Negroni |

Cooking method matters as much as aging: traditional stone ovens (*hornos*) hydrolyze agave fructans slowly and permit Maillard development, producing the cooked-sweet-potato note; autoclaves are faster and cleaner; **diffusers** extract with hot water and acid and strip most of it. Agave varietal in mezcal is a real flavor dial — **espadín** (workhorse, balanced), **tobalá** (floral, fruity, wild), **tepeztate** (herbaceous, green, sharp), **madrecuixe** (mineral, vegetal). Because mezcal's phenols behave like peated Scotch's, the same design rule applies: use it in a **split base** at 0.25–0.75 oz against a neutral partner before committing a full 2 oz.

### 2.5 Brandy {#spirit-brandy}

| Style | Base / method | ABV | Character | Suits |
|---|---|---|---|---|
| Cognac | Ugni Blanc grapes, **double** pot distillation, Limousin/Tronçais oak. VS ≥2 yr, VSOP ≥4 yr, XO ≥10 yr (raised from 6 in 2018) | ≥40% | Round, floral, dried apricot, rancio with age | Sidecar, Vieux Carré, Sazerac (historical), Brandy Crusta, French 75 |
| Armagnac | Folle Blanche / Baco / Ugni Blanc, usually **single continuous** column (*alambic armagnacais*) | 40–48% | Rustic, prune, leather, more congener than Cognac | Old Fashioned root, punch |
| Calvados | Apples (Domfrontais ≥30% pear); Pays d'Auge double pot distilled, ≥2 yr | ≥40% | Fresh and baked apple, orchard funk, oak | Corpse Reviver No. 1, Widow's Kiss, apple sours |
| Pisco (Peruvian) | Grape must; **no wood aging, no water added post-distillation** — bottled at distillation strength after a minimum **three months'** rest in inert vessels (glass, stainless, or ceramic), per the Peruvian standard NTP 211.001 | 38–48% | Bright, floral, grapey; Quebranta (neutral), Italia/Torontel/Moscatel (aromatic) | Pisco Sour, Chilcano, Pisco Punch |
| Grappa / marc | Pomace | 35–60% | Sharp, vinous, high fusel character | Rinses, small modifiers |

### 2.6 Vodka, Aquavit, Cachaça, Shochu & Soju {#spirit-neutral-regional}

| Spirit | Definition | ABV | Character | Suits |
|---|---|---|---|---|
| Vodka | Any fermentable base, distilled to high purity. US minimum 40%; EU minimum 37.5%. (The US TTB's "without distinctive character, aroma, taste or color" requirement was **removed in the 2020 labeling modernization**, so texture and grain character are now legitimate variables.) | 40–50% | Minimal congener; contributes **texture, viscosity, and ethanol structure**, not aroma | Vodka Martini, Moscow Mule, Espresso Martini, any drink where a modifier must lead |
| Aquavit | Grain or potato neutral spirit redistilled with **caraway and/or dill predominant**; also fennel, anise, coriander, citrus peel | 37.5–45% | Carvone (caraway/dill), anethole (fennel/anise). Norwegian *linie* styles rest in ex-sherry casks | Aquavit Gimlet, Nordic highball, Bloody Mary variations, Trident |
| Cachaça | Brazil; **fresh sugarcane juice**, distilled and bottled at **38–48% ABV**; up to 6 g/L sugar (above that, to 30 g/L, it must be labeled *adoçada*) | 38–48% | Grassy, funky, sulfurous-vegetal; aged in native woods — **amburana** brings cinnamon-vanilla coumarin notes, jequitibá and umburana others | Caipirinha, Batida, agricole-style sours |
| Shochu (*honkaku*) | Japan; single-distilled, koji-fermented, **≤45% ABV**; base is *imo* (sweet potato), *mugi* (barley), *kome* (rice), or *kokutō* (Amami brown sugar). Multiply-distilled *korui* is ≤36% and near-neutral | typically 25% (bottled), up to 45% | Low proof, distinct base character; *imo* earthy-sweet, *mugi* nutty, *kome* floral | Chu-hi and soda highballs, oyuwari (hot water), low-ABV builds |
| Soju | Korea; historically distilled rice/grain, now most commonly diluted neutral spirit, often sweetened | 16–25% (traditional *andong* higher) | Light, faintly sweet; very low proof | Highballs, low-ABV punches, spritz-family substitutions |

### 2.7 Base Spirit → Template Fit {#spirit-template-fit}

| Spirit | Sour | Old Fashioned | Martini root | Highball | Tiki | Flip / dairy | Sparkling | Aperitivo |
|---|---|---|---|---|---|---|---|---|
| London Dry gin | ✓✓ | ○ | ✓✓ | ✓✓ | ○ | ✓ | ✓✓ | ✓ |
| Old Tom gin | ✓ | ✓ | ✓✓ | ✓ | ○ | ✓✓ | ✓ | ✓ |
| Bourbon | ✓✓ | ✓✓ | ✓ | ✓ | ○ | ✓✓ | ○ | ✓ |
| Rye | ✓ | ✓✓ | ✓✓ | ✓ | ○ | ✓ | ○ | ✓ |
| Scotch (unpeated) | ✓ | ✓ | ✓✓ | ✓✓ | ○ | ✓ | ○ | ○ |
| Peated Scotch | split base only | ✓ | ○ | ✓ | split base only | ○ | ○ | ○ |
| Japanese whisky | ✓ | ✓ | ✓ | ✓✓✓ | ○ | ○ | ○ | ○ |
| Light rum | ✓✓✓ | ○ | ○ | ✓✓ | ✓ | ✓ | ✓✓ | ✓ |
| Jamaican pot rum | ✓✓ | ✓ | ✓ | ✓ | ✓✓✓ | ✓ | ✓ | ✓ |
| Demerara rum | ✓ | ✓✓ | ✓ | ○ | ✓✓✓ | ✓✓ | ○ | ○ |
| Rhum agricole | ✓✓ | ✓✓ (Ti' Punch) | ○ | ✓ | ✓✓ | ○ | ✓ | ○ |
| Blanco tequila | ✓✓✓ | ○ | ✓ | ✓✓ | ✓ | ○ | ✓ | ✓ |
| Reposado / añejo | ✓ | ✓✓ | ✓ | ✓ | ✓ | ✓ | ○ | ✓ |
| Mezcal | ✓✓ | ✓ | ✓ | ✓ | split base | ○ | ✓ | ✓✓ |
| Cognac | ✓✓ | ✓✓ | ✓ | ✓ | ✓ | ✓✓✓ | ✓✓ | ✓ |
| Calvados | ✓✓ | ✓✓ | ✓ | ✓ | ○ | ✓ | ✓ | ✓ |
| Pisco | ✓✓✓ | ○ | ○ | ✓✓ | ✓ | ✓✓ | ✓ | ○ |
| Vodka | ✓ | ○ | ✓✓ | ✓✓ | ○ | ✓✓ | ✓ | ✓ |
| Aquavit | ✓✓ | ✓ | ✓✓ | ✓✓ | ○ | ○ | ✓ | ✓ |
| Cachaça | ✓✓✓ | ✓ | ○ | ✓ | ✓✓ | ○ | ✓ | ○ |
| Shochu / soju | ✓ | ○ | ○ | ✓✓✓ | ○ | ○ | ✓ | ✓✓ |

✓✓✓ = definitional home · ✓✓ = strong · ✓ = workable · ○ = fights the template


---

## Section 3: Modifiers, Sweeteners & the Bitter Axis {#modifiers-sweeteners-bitter-axis}

Everything that is not the base spirit and not the water is a **modifier**. The word covers four structurally distinct jobs — supplying aroma, supplying sugar, supplying acid, supplying bitterness — and a drink fails most often because one ingredient was asked to do two of them at once. This section is organized by that functional split, mirroring the food pillar's treatment of ACID / FAT / SALT / UMAMI as contributions rather than as shopping categories.

### 3.1 The Modifier Roles and Which Ones Stack {#drink-functional-roles}

| Role | What it contributes | Typical volume in a 3–4 oz drink | Stackable? |
|---|---|---|---|
| `base` | Ethanol structure, congener aroma, the drink's identity | 1.5–2.5 oz | **Yes** — split bases are canonical (see §2.3 on rum ester classes and §1.5) |
| `modifier` | Aroma, secondary alcohol, some sugar; the "second voice" | 0.25–1.5 oz | **Yes** — two amari, or a vermouth plus a liqueur, is standard construction |
| `sweetener` | Sugar, viscosity, ethanol-masking | 0.25–1 oz | Rarely; a second sweetener is usually a modifier in disguise |
| `acid` | Titratable acidity, salivation, sugar suppression | 0.5–1 oz | Occasionally — split citrus (lemon + lime) is a real move |
| `bitters` | Aromatic top note, trace bitterness, "seasoning" | 1–6 dashes (0.6–6 mL) | **Yes** — stacking is correct practice, not redundancy (§3.8) |
| `lengthener` | Volume, carbonation, temperature | 2–6 oz | No |
| `texture` | Viscosity, foam, mouth-coating (egg, dairy, gum, saline) | trace–1 oz | No |
| `aromatic garnish` | Orthonasal aroma only; contributes almost no volume | expressed peel, sprig, dash-on-foam | Yes |

The stackable roles are exactly the ones where **two ingredients in the same slot are additive rather than competitive**, because each brings a distinct congener profile. A pruning rule that treats "two things with role = modifier" as redundancy will delete the Negroni's structure, the Vieux Carré's double bitters, and every split-base tiki drink in the canon.

### 3.2 Fortified & Aromatized Wines {#aromatized-wines}

Aromatized wines are the only bar ingredient that is simultaneously **diluent, flavoring, and sweetener**. They are wine-based, so they are perishable in a way that spirits are not — this is the single most common cause of a "flat, dusty, oxidized" Martini or Manhattan.

Under EU Regulation 251/2014, an aromatized wine must be **14.5–22% ABV** and at least 75% wine. Sugar class is a labeled term with numbers behind it: *extra dry* <30 g/L, *dry* <50 g/L, *semi-dry* 50–90 g/L, *semi-sweet* 90–130 g/L, *sweet* ≥130 g/L.

| Style | Representative | ABV | Sugar (g/L) | Aromatic register | Structural job |
|---|---|---|---|---|---|
| Dry (French) vermouth | Dolin Dry 17.5%, Noilly Prat Original Dry 18% | 16–18% | 20–40 | Alpine herb, chamomile, saline; Noilly is oxidative and nuttier | Martini modifier; lengthens without sweetening |
| Sweet (Italian/rosso) vermouth | Carpano Antica Formula 16.5%, Cocchi di Torino 16% | 15–18% | 130–160 | Vanilla, bitter orange, cocoa, wormwood | Manhattan/Negroni modifier; carries sugar *and* bitterness |
| Bianco / blanc | Dolin Blanc 16%, Martini Bianco 15% | 15–16% | 130–150 | Vanilla, elderflower, citrus blossom; pale but sweet | Sweetness without the caramel of rosso |
| Quinquina / americano | Cocchi Americano 16.5%, Byrrh 17%, Dubonnet | 16–18% | 60–140 | Cinchona bark (quinine) bitterness over wine fruit | Bitter modifier at low ABV |
| Lillet Blanc | Lillet Blanc | 17% | ~100 | Honeyed, candied citrus | Reformulated in 1986 with reduced quinine; **not** a like-for-like Kina Lillet substitute — Cocchi Americano is the usual stand-in for pre-1986 specs |

**Sherry by style.** Sherry's split is governed by *flor*, the yeast veil that survives only between roughly 15% and 17% ABV. Below that band, the wine ages biologically under flor and stays pale and saline; fortified above it, the flor dies and the wine ages oxidatively.

| Style | ABV | Aging | Character | Bar use |
|---|---|---|---|---|
| Fino | 15–15.5% | Biological, under flor | Bone dry, almond, saline, bready from autolysis | Bamboo, Sherry Cobbler, fino highball |
| Manzanilla | ~15% | Biological, Sanlúcar de Barrameda | Fino with more salinity and a lighter body | Same as fino; sharper, more coastal |
| Amontillado | 16.5–18% | Biological then oxidative | Hazelnut, dried orange, dry finish | Adonis, split-modifier stirred drinks |
| Oloroso | 18–20% | Fully oxidative | Walnut, leather, dried fig; dry despite the weight | Sherry-modified whiskey and brandy drinks |
| Pedro Ximénez (PX) | 15–17% | Sun-dried grapes, oxidative | ~350–500 g/L sugar; raisin, molasses, near-syrup | Sweetener *and* modifier; ¼ oz replaces syrup entirely |

**Oxidative shelf life once opened** — the number that actually matters, all figures assuming refrigeration and an intact seal:

| Product | Usable window after opening | Why |
|---|---|---|
| Fino / manzanilla | **3–5 days** | No residual sugar, low ABV, nothing to buffer oxidation; the flor character dies first |
| Dry vermouth | **2–4 weeks** | Low sugar; oxidation reads as cardboard and stewed apple |
| Sweet vermouth / bianco | **4–8 weeks** | Sugar and caramel mask oxidation longer, which is why it goes off unnoticed |
| Amontillado | **2–3 weeks** | Already partly oxidative, so decline is slower but the finish dries out |
| Oloroso | **4–8 weeks** | Fully oxidative already; ABV and extract buffer it |
| PX | **Months** | Sugar concentration drops water activity far enough to stabilize it |

Practical consequence: an aromatized-wine drink is a **freshness question before it is a ratio question**. If a Martini reads flat, check the vermouth's open date before touching the spec.

### 3.3 Amari & Bitter Liqueurs {#amari-bitter-axis}

Amari are bitter *and* sweet by construction — under EU rules a liqueur carries a minimum of 100 g/L sugar — so adding one always moves two axes at once. Rank by perceived bitterness, not by ABV; the two do not track.

| Amaro | ABV | Bitterness (1–10) | Bittering principal / register | What it brings |
|---|---|---|---|---|
| Aperol | 11% | 2 | Gentian and rhubarb, heavily sugared | Orange-rhubarb sweetness with a bitter suggestion; the low-ABV spritz workhorse |
| Amaro Montenegro | 23% | 3 | Floral-forward botanical blend | Orange blossom, rose, vanilla; a *rounding* amaro, not a bittering one |
| Cynar | 16.5% | 4 | Cardoon/artichoke | Vegetal, earthy, faintly saline; bridges savory ingredients (Cynar 70 is the 35% expression) |
| Averna | 29% | 4 | Caramel-sweetened Sicilian blend | Cola, burnt sugar, citrus peel; softens whiskey without brightening it |
| Amaro Nonino Quintessentia | 35% | 3–4 | Grappa base, low bitter load | Candied orange, apricot, silk texture — the reason it works in the Paper Plane |
| Braulio | 21% | 5 | Alpine (gentian, juniper, wormwood) | Pine, mint, camphor; reads cold and mountain-herbal |
| Campari | 20.5–25% by market (20.5% IT, 24% US) | 7 | Gentian, cascarilla, bitter orange | The reference red bitter; assertive enough to hold equal parts against gin |
| Suze | 15–20% by market | 8 | *Gentiana lutea* root, concentrated | Raw earthy gentian, grapefruit pith, almost no caramel cover |
| Fernet-Branca | 39% | 10 | Myrrh, saffron, gentian, aggressive menthol | Maximum bitterness plus a cooling trigeminal hit; a dash-scale ingredient in most builds |

**Design rule:** substituting within this table preserves *role* but not *balance*. Swapping Aperol for Campari in a spritz holds the slot but roughly triples the bitterness and doubles the ABV, so the sugar and the lengthener both need re-specifying. Two amari in one drink is normal construction — Campari for the front-palate bitterness plus Nonino or Braulio for the aromatic mid-palate — because they occupy different points on the temporal curve.

### 3.4 Liqueurs by Aromatic Register {#liqueurs}

| Liqueur | ABV | Approx. sugar | Character | Notes on substitution |
|---|---|---|---|---|
| Cointreau (triple sec) | 40% | ~250 g/L | Clean bitter-sweet orange, dry finish, high proof | The default when a spec says "triple sec" without qualifying; generic 15–30% triple secs are sweeter *and* weaker and are not one-for-one |
| Dry curaçao (e.g. Pierre Ferrand) | 40% | ~150–200 g/L | Brandy base, orange peel, faint oak, drier | Best in Sidecar-root drinks where the liqueur is the only sweetener |
| Grand Marnier Cordon Rouge | 40% | ~250 g/L | Cognac base; oak, vanilla, sweeter and heavier | Adds oak the other two do not; changes a Margarita's texture, not just its sweetness |
| Maraschino (Luxardo) | 32% | ~250 g/L | Marasca cherry distilled **with the pits**; funky, floral, benzaldehyde nuttiness | Not "cherry flavored" — it is dry, pungent, and dominates above 0.25 oz |
| Crème de cassis | 15–20% | **≥400 g/L** (EU minimum for this specific *crème de*) | Deep blackcurrant, tannic, low alcohol | Effectively a fruit sweetener; must be counted as sugar in the ratio |
| Crème de violette | 16–20% | ≥250 g/L | Parma violet, powdery, perfume-forward | Aviation-scale doses only (0.25 oz); overshoots into soap fast |
| Green / yellow Chartreuse | 55% / 40% | moderate | 130 botanicals; herbal, honeyed, high-proof | Raises finished ABV materially — treat as part base, part modifier |
| Absinthe | 45–74% | none | Anise, wormwood, fennel | Rinse-scale (a few mL, poured out); a full pour rebuilds the drink |

**Under EU spirit-drink rules, a "liqueur" needs ≥100 g/L sugar and a "crème de" ≥250 g/L, with crème de cassis alone required to hit 400 g/L.** These are labeling minimums, not typical values, but they establish the floor: any liqueur in a spec is carrying meaningful sugar and must be subtracted from the syrup, not added on top of it.

### 3.5 Allergen and Exclusion Screening {#allergen-screening}

A bar is an allergen environment with almost no ingredient labels in the guest's line of sight, and the names are actively misleading in both directions. **Screen by ingredient identity, never by string-matching the ingredient name.** A name-matching screen fails two ways, and both failures are silent:

- **False negative** — the exposure is real and the name conceals it. Orgeat is almond. Worcestershire is anchovy. Clamato is clam broth. A fat wash carries whatever fat it was made with. None of these contain the allergen word.
- **False positive** — the name contains the word and the exposure does not exist. Cream sherry is a sweetened oloroso. Cream of coconut is a coconut product. Ginger beer and root beer are sodas. A Prairie Oyster is a raw egg. Fish House Punch is named for a Philadelphia fishing club. Salers is a gentian aperitif whose name merely contains the letters of "ale". Deleting these costs the drinker a safe ingredient and tells them nothing.

The lists below are the screen, by category. This section and §7.4–7.5 are the authority for nuts; §1.6 is the authority for raw egg **safety**, which is a separate question from egg **allergy**.

**Tree nuts and kernels.** The single most concealed category behind a bar, because nut exposure arrives almost entirely through sweeteners and liqueurs rather than through anything visibly nutty.

| Ingredient | Nut / kernel source | Notes |
|---|---|---|
| **Orgeat** | **Almond** (plus orange flower water) | The most common hidden almond in the bar. Central to the Mai Tai, Japanese Cocktail, Fog Cutter, Army & Navy |
| **Falernum** | **Almond** in most commercial and traditional formulations (with lime, clove, ginger) | John D. Taylor's Velvet Falernum and most house recipes include almond; a few modern brands omit it — verify per bottle, do not assume |
| **Amaretto** (e.g. Disaronno) | **Apricot kernel** in the classic formulation; other brands use almond | Disaronno states it is made from apricot kernel oil rather than almonds, but stone-fruit kernels are chemically and clinically adjacent to almond and **must be flagged for a tree-nut exclusion**, not cleared |
| **Frangelico** | **Hazelnut** | Unambiguous |
| **Nocino** | **Green walnut** | Unambiguous |
| **Crème de noyaux** | **Stone-fruit kernels** (apricot/peach pits), sometimes with almond | The pink almond-flavored liqueur in the Pink Squirrel and Old Etonian |
| Maraschino liqueur | Marasca cherry **pits**, distilled | Distillate, not a nut, and the pit-derived character is aroma rather than protein — but disclose it when the exclusion is stone-fruit-kernel rather than tree-nut |
| Nut-washed or nut-infused spirits | Whatever was infused | Fat-washing with nut oils (§7.9) carries nut protein forward; treat as the source nut |
| Peanut, peanut-butter washes | **Peanut** | Botanically a legume rather than a tree nut, and a genuinely different allergen — but not a distinction to draw silently. Flag it and name the nut, so the drinker applies their own rule |

The correct behavior on a nut exclusion is to **surface the conflict to the drinker**, not to silently drop the ingredient — orgeat is load-bearing in the drinks that use it, and the substitution (a seed orgeat made from sunflower or pumpkin seed, or a toasted-rice orgeat) changes the drink enough that the drinker should choose it.

Not nuts, despite the name: **coconut** (a drupe; cream of coconut, coconut cream, coconut water), **nutmeg** (the seed of *Myristica fragrans*), **cocoa and crème de cacao**, **tiger nut / chufa** (a tuber, and the base of Valencian horchata de chufa). One caveat worth stating rather than assuming: US allergen labeling counts coconut on the tree-nut list even though most tree-nut-allergic people tolerate it, so if the drinker's exclusion came from a label rather than from their own experience, ask about coconut explicitly instead of clearing it by default.

**Dairy.** Cream in a bar is usually a liqueur rather than a carton, which is why it survives a visual check of the build.

| Path | Where it hides |
|---|---|
| Cream liqueurs | Baileys and other Irish creams, RumChata, Amarula — dairy cream is a formulation ingredient, not a garnish |
| Advocaat | Egg **and**, in most formulations, dairy |
| Dessert-family classics | Brandy Alexander, Grasshopper, Golden Cadillac, White Russian, eggnog, syllabub, posset |
| Milk punch, clarified | **Still a dairy exposure.** Milk clarification (§7.10) curdles the milk and strains out the casein curd along with the tannins and solids it traps; whey proteins remain dissolved in the liquid that goes in the glass |
| Butter or ghee fat-washes | Hot buttered rum, butter-washed spirits (§7.9) — the wash carries milk protein forward |
| Horchata | Mexican-style rice horchata is often finished with condensed or evaporated milk; the Valencian chufa version is not. Verify the specific product |

Not dairy: **cream sherry** (a sweetened oloroso — the word describes the texture), **cream soda**, **cream ale** (a beer style, and therefore a *gluten* flag), **cream of coconut**, and every **crème de** liqueur, where the term denotes a sugar minimum under EU rules (§3.4) and not a dairy content.

**Egg.** Egg arrives through the texture slot and through drink names that encode it as a convention rather than as an ingredient list.

- Direct: egg white (sour foam), yolk (richness and emulsification), whole egg (flip). See §1.6 for the structural mechanism and §6.3–6.4 for the shake order.
- By naming convention: a **Silver** Fizz is white, a **Golden** Fizz is yolk, a **Royal** Fizz is whole egg. A Ramos Gin Fizz is egg white by definition. Advocaat, eggnog, syllabub and any Flip carry egg by definition.
- Ambiguous by name alone: "sour" and "fizz" are families that *may* carry egg white. Ask; do not assume in either direction.
- Substitutes that are not egg: **aquafaba** (chickpea liquid, ~1 oz per drink) and commercial methylcellulose or modified-starch foamers. Both foam by different mechanisms and read slightly drier (§1.6).
- Not egg: **eggplant** anything, and the **Prairie Oyster**, which is the reverse trap — it is raw egg and contains no shellfish at all.

Raw-egg *safety* is a different question from egg *allergy*, and pasteurized egg answers only the first. See §1.6.

**Gluten, and the distillation asymmetry.** This is the one category where the food-side rule of thumb — screen the grain — gives the wrong answer behind a bar, and where the correct answer is asymmetric.

Gluten proteins and the peptides that provoke coeliac disease are large and non-volatile. They stay in the wash and do not carry into the distillate, which is why the regulatory position on both sides of the label changed in 2020: FDA (July 2020) and then TTB (October 2020) permit a **"gluten-free"** claim on spirits distilled from gluten-containing grains, while a product merely *fermented* from those grains may only claim **"processed to remove gluten"** and must hold documentation supporting it. The two claims are not synonyms, and the difference between them is exactly the still.

| Tier | Products | Why |
|---|---|---|
| **Real exposure** | Beer, ale, lager, stout, porter, hefeweizen, IPA, pilsner, barley wine, malt liquor; shandy, michelada, boilermaker and any beer cocktail; kvass; malted milk, barley malt and malt extract as syrup ingredients | Undistilled, or a malt ingredient added after distillation |
| **Ambiguous — flag, do not delete** | Whiskey, bourbon, rye, Scotch, single malt, grain and wheat vodka, barley (*mugi*) shochu, genever, korn, baijiu | The distillate itself carries no gluten protein, but post-distillation additions (flavorings, colorings, a malt-based blend) and shared-facility handling are real, and some drinkers avoid grain spirits regardless of the mechanism |
| **Not a gluten path** | Ginger beer, ginger ale, root beer (sodas that share a word with a brewed product), rum, tequila, mezcal, brandy, agricole, potato and grape vodka | No grain anywhere in the process |

A HARD screen on the middle tier deletes the entire whiskey category from a session without the drinker ever seeing it, which is why it is surfaced as an ambiguous path instead. State the mechanism, name the caveats, and let the drinker decide.

**Sulfites.** Every wine-based product on the back bar is a sulfite path: vermouth, sherry, port, madeira, quinquina and americano-style aperitifs, sparkling wine, cider and sake. US labeling requires a **"Contains sulfites"** declaration at or above **10 ppm total sulfur dioxide** (27 CFR 4.32(e) for wine; the same threshold applies to malt beverages), so the label answers the question for anything bottled. Beyond the bottles: bottled citrus juice, some grenadines and syrups, dried-fruit garnishes, and cocktail cherries, which are commonly brined with sulfur dioxide. Sulfite sensitivity is usually not an IgE allergy and its most serious presentation is in asthmatics, so treat it as an ambiguous path — flag, quantify where the label lets you, and let the drinker judge.

**Savory bar ingredients — shellfish, fish, soy, pork, beef.** The savory drink families import food allergens wholesale, and a screen built for sweeteners and liqueurs will miss all of them.

| Exclusion | Bar paths |
|---|---|
| Shellfish | Clamato and the Bloody Caesar (tomato **and clam broth** — this is the Canadian Caesar's defining ingredient, not a variation), clam juice, oyster shooters, shrimp garnishes and shrimp paste in savory mixes |
| Fish | **Worcestershire sauce**, which is anchovy-based in the standard formulation and is the default seasoning in a Bloody Mary, a Michelada and a Caesar; fish sauce, colatura and garum in modern savory drinks; anchovy-stuffed olives in a dirty Martini |
| Soy | Soy sauce and tamari as savory seasoning; miso-washed spirits |
| Pork / beef | Fat-washing (§7.9) with bacon fat, lard or duck fat; the Bullshot, which is vodka and beef consommé |

Not what the name suggests: **Fish House Punch** (named for a Philadelphia fishing club, and containing no fish), the **Prairie Oyster** (raw egg), and **Beefeater** (a gin).

**How to report a hit.** Name the ingredient, name the allergen path, say whether it is definite or ambiguous, and offer the substitution with its cost (§3.10). Do not silently delete a load-bearing ingredient — an orgeat-less Mai Tai is a different drink, and the drinker is the one who gets to choose it.

### 3.6 Sweeteners: Ratio, Viscosity, and Shelf Life {#sweeteners}

Sugar in a drink does three things simultaneously: it tastes sweet, it **suppresses perceived acidity and ethanol burn**, and it raises viscosity. The last one is why the syrup ratio is a texture decision, not just a sweetness decision.

| Syrup | Ratio | Sugar % w/w (≈Brix) | Sugar per mL | Viscosity @20 °C | Refrigerated life |
|---|---|---|---|---|---|
| Simple, by volume | 1 cup sugar : 1 cup water | ~46% | ~0.55 g | ~10–12 cP | 2–4 weeks |
| Simple, by weight | 1:1 | 50% | ~0.61 g | ~15 cP | 2–4 weeks |
| Medium rich, by weight | 1.5:1 | ~60% | ~0.76 g | ~50 cP | 1–3 months |
| **Rich, by weight** | **2:1** | **~67%** | **~0.89 g** | **~150+ cP** | **1–6 months** |
| Demerara rich | 2:1 demerara | ~67% | ~0.89 g | ~150+ cP | 1–6 months |
| Honey syrup | 3:1 honey:water (by weight) | ~62% | ~0.80 g | high | 1–2 months |
| Agave syrup | neat | ~75% | ~1.05 g | high | months |
| Agave syrup | 1:1 agave:water | ~55–60% | ~0.70 g | moderate | 1–2 months |
| Maple (grade A dark) | used neat | ≥66% by grading standard | ~0.88 g | ~150 cP | months |
| Gomme | 2:1 + gum arabic | ~67% | ~0.89 g | high, and *elastic* | 3–6 months |

**Why rich syrup changes texture and not merely sweetness.** The folk rule "use half as much rich syrup" is wrong in a specific and useful way. Rich (2:1 w/w) syrup carries roughly **1.44× the sugar per unit volume** of 1:1 syrup — not 2×, because the denser syrup is also heavier per mL. So halving the volume removes about a quarter of the sugar along with the water. What the drinker perceives is not "less sweet"; it is *drier and rounder at once*, because viscosity climbed by roughly an order of magnitude (about 15 cP at 50 Brix to 150+ cP near 67 Brix) while sugar fell slightly. Jeffrey Morgenthaler's *The Bar Book* argues for 2:1 as the house default largely on these grounds plus shelf life: the higher sugar concentration lowers water activity enough to resist mold and fermentation for months rather than weeks.

**The substitution arithmetic, stated once.** If a spec calls for 2:1 rich and you have 1:1 simple, use about **1.4× the volume** and count the extra water against your dilution budget. Going the other way, 1:1 simple replaced by rich at the same volume adds roughly 45% more sugar — not 100%, and not "half as much" either. Every other syrup in the table converts through the same column: grams of sugar per mL.

**The rest of the sweetener bench:**
- **Demerara / turbinado** — retains some molasses; adds a caramel-toffee mid-palate. The default sweetener for aged rum, rye, and tiki, where it reinforces the base's own congeners.
- **Honey** — roughly 38% fructose, 31% glucose, 17–18% water. Must be cut with water to pour cold; 3:1 by weight is the standard bar dilution, 1:1 for a lighter hand. Honey's floral volatiles are heat-labile: warm the water, do not boil the honey.
- **Agave** — dominated by fructose (typically 75–85%). Fructose's sweetness relative to sucrose *rises as temperature falls*, so agave and honey read sweeter in a cold drink than a room-temperature taste predicts. Correct for this at the tasting stage, not by guessing.
- **Maple** — US Grade A requires ≥66% soluble solids, so maple is already at rich-syrup concentration and substitutes 1:1 for 2:1 simple by volume, adding its own sotolone-driven aroma.
- **Gomme / gum syrup** — rich syrup with gum arabic (acacia gum) hydrated in water *before* the sugar goes in. Published doses vary widely, from a couple of percent of the syrup's weight up to ten; start at the low end and climb, because the texture change is obvious and the overshoot is gluey. Gum arabic is a hydrocolloid emulsifier: it raises viscosity and adds a silky, slightly slippery mouthfeel **without adding sugar**, which is the only way to increase body and dryness at the same time. This is the nineteenth-century default that modern bars rediscovered, and it remains the cleanest texture lever available for a spirit-forward drink.

### 3.7 Acids: Juice, Isolated Acid, and Acid-Adjusting {#acids}

| Acid source | Titratable acidity | pH | Dominant acid | Perceptual character |
|---|---|---|---|---|
| Lime juice | 5–7% (typ. ~6%) | 2.0–2.4 | Citric (+ a malic fraction) | Sharp, fast attack, aromatic terpene lift; the most *time-sensitive* bar citrus |
| Lemon juice | 5–6% | 2.2–2.6 | Citric (trace malic) | Cleaner and rounder than lime, less aromatic top note, holds longer after juicing |
| Grapefruit juice | 1.5–2.5% | 3.0–3.3 | Citric + malic | Half the acid of lemon plus real sugar plus naringin bitterness — it is an acid, a sweetener, and a bittering agent at once |
| Orange juice | 0.8–1.2% | 3.3–4.2 | Citric + malic | Functionally a sweet lengthener, not an acid; cannot balance a sour on its own |
| Pineapple juice | 0.8–1.2% | 3.2–4.0 | Citric + malic | Same acid load as orange, plus sugar, plus enough body to read as a texture ingredient |
| Apple juice | 0.4–0.8% | 3.3–4.0 | Malic | The lowest-acid common juice; a lengthener, never the acid slot |
| Citric acid (isolated) | — | pKa₁ 3.13 | — | The "citrus" reference sourness; bright, immediate, short |
| Malic acid | — | pKa₁ 3.40 | — | Green-apple, rounder and *longer* on the palate; softens a citric-only blend |
| Tartaric acid | — | pKa₁ 2.98 | — | Grape/wine acidity; sharper front, faintly astringent, mineral finish |
| Phosphoric acid | — | pKa₁ 2.15 | — | Non-fruity, "flat" mineral sourness with a dry finish; the soda-fountain acid, sold as acid phosphate |
| Lactic acid | — | pKa 3.86 | — | Soft, dairy-adjacent, no fruit; useful in milk punches and clarified drinks |
| Acetic (vinegar/shrub) | 4–6% in vinegar | 2.4–3.0 | Acetic | Volatile and aromatic — it is smelled as much as tasted |

**Acid-adjusting.** Because the sour template is really balancing *acid load* rather than "lime," any juice can be brought to lime-equivalent acidity by adding isolated acid. This is Dave Arnold's territory in *Liquid Intelligence*: work in weight-percent, target roughly **6% total acidity** to make a low-acid juice behave like lemon or lime, and keep separate stock solutions so the adjustment is measurable rather than guessed. A common working practice is pure citric to imitate lemon and a citric/malic blend to imitate lime's rounder tail; the mechanism to reason from is the pKa spread above, not any single published ratio. The payoff is drinks that are otherwise impossible — an acid-adjusted orange juice Daiquiri, a grapefruit sour that does not need supplemental lime, a clarified drink whose acidity survives filtration. The related "super juice" method (peel oleo extraction plus citric and malic to reconstitute juice at multiplied yield), popularized by bartender Nickle Morris, is the same arithmetic applied to yield rather than flavor.

**Splitting acids** is legitimate and common: lemon plus lime in a Tiki drink, or lime plus a few drops of phosphoric acid to add a dry mineral finish without more sourness. Two acids in the acid slot is a deliberate move, not duplication.

### 3.8 Bitters: The Dash as a Real Unit, and Why Stacking Is Correct {#bitters}

Bitters are high-proof botanical tinctures used at **fractions of a milliliter**. They are the drink's seasoning layer: their function is aromatic top note plus a trace of bitterness that keeps sugar from reading as cloying.

| Bitters | ABV | Register | Canonical use |
|---|---|---|---|
| Angostura aromatic | 44.7% | Gentian, clove, cinnamon, allspice; drying finish | Old Fashioned, Manhattan, Champagne Cocktail; 1.5 oz as the *base* of Giuseppe González's Trinidad Sour |
| Peychaud's | 35% | Anise, cherry, light florals; sweeter and softer than Angostura | Sazerac, Vieux Carré, Seelbach |
| Orange bitters | 28–45% by brand | Regans' No. 6 is cardamom- and coriander-forward and dry; Fee Brothers West Indian is sweeter and candied | Martinez, Dry Martini, Old Fashioned variations. A **1:1 blend of Regans' and Fee's** is the widely used house blend associated with Audrey Saunders' Pegu Club |
| Mole / cacao (e.g. Bittermens Xocolatl Mole) | ~45% | Cacao, cinnamon, dried chile | Agave and aged-rum drinks; bridges to dessert registers |
| Celery, grapefruit, cardamom, absinthe bitters | 30–45% | Single-register accents | Targeted aromatic patches on an otherwise finished drink |

**The dash, quantified.** From a standard dasher top, one dash is roughly **0.6–1.0 mL** — about ⅛ teaspoon (0.62 mL) at the low end — so **5–6 dashes ≈ 1 teaspoon** and 1 oz ≈ 30–50 dashes. The variance across bottle necks, viscosity, and wrist is real: for batching or for any spec that needs to reproduce, convert to milliliters and measure. For a single drink, dashes are precise enough because the ingredient's contribution is aromatic and the perceptual threshold is broad.

**Why stacking bitters is correct practice.** Two bitters in one drink are not two attempts at the same job:

1. **Different botanical extracts occupy different aromatic registers.** Angostura's gentian-clove-cinnamon axis and Peychaud's anise-cherry axis do not overlap. The **Vieux Carré** uses both by design — 2 dashes each — and dropping either collapses a specific part of the drink.
2. **They land at different points on the temporal curve.** Volatile citrus-oil-driven orange bitters read on the nose and the front palate; heavier, resinous aromatic bitters read mid-palate and on the finish. Stacking builds a longer arc, exactly as layering an ingredient in multiple forms does in the food pillar.
3. **The doses are seasoning-scale, so they add rather than compete.** Six total dashes is ~4 mL in a 100+ mL drink. There is no volumetric crowding to arbitrate.
4. **The canon is explicit about it.** The Old Fashioned root in *Cocktail Codex* and the house specs in *Death & Co* routinely list two and sometimes three bitters in a single build.

Treat "two bitters entries" the way a cook treats "salt at three stages": the same class of ingredient, deliberately repeated, because the repetition is the technique.

### 3.9 Accounting for Hidden Sugar {#hidden-sugar}

The most common ratio error in cocktail design is adding syrup on top of an ingredient that is already the sweetener. Convert everything to **grams of sugar in the glass** before deciding the syrup volume. One fluid ounce is 29.6 mL, so an ingredient at *n* g/L contributes about *n* × 0.0296 grams per ounce.

| Ingredient | Approx. sugar | Sugar in 0.75 oz | Equivalent volume of 1:1 simple |
|---|---|---|---|
| 1:1 simple syrup (by weight) | ~610 g/L | ~13.5 g | 0.75 oz (reference) |
| 2:1 rich syrup | ~890 g/L | ~19.7 g | ~1.1 oz |
| Cointreau / Grand Marnier | ~250 g/L | ~5.5 g | ~0.3 oz |
| Maraschino | ~250 g/L | ~5.5 g | ~0.3 oz |
| Crème de cassis | ≥400 g/L | ≥8.9 g | ≥0.5 oz |
| Sweet vermouth | ~150 g/L | ~3.3 g | ~0.2 oz |
| Aperol | ~250 g/L (est. from category) | ~5.5 g | ~0.3 oz |
| Pedro Ximénez sherry | 350–500 g/L | 8–11 g | 0.45–0.6 oz |
| Orange juice | ~90 g/L | ~2.0 g | ~0.1 oz |

This is why the Sidecar is a distinct root from the Daiquiri: 0.75 oz of Cointreau supplies roughly 40% of the sugar that 0.75 oz of simple syrup does, plus 0.3 oz of ethanol. Substituting one for the other holds the slot but moves both axes.

### 3.10 Substituting Within a Role {#modifier-substitution}

A substitution is safe when it preserves the slot's three numbers — **ABV, sugar, and aromatic register** — or when the deviation is corrected elsewhere in the build. Reason in that order.

| Original | Substitution | What is preserved | What must be corrected |
|---|---|---|---|
| Sweet vermouth | Cocchi Vermouth di Torino, Punt e Mes | ABV and sugar within a few points | Punt e Mes adds real bitterness; pull back any amaro |
| Sweet vermouth | Oloroso sherry + 0.1 oz rich syrup | Oxidative aroma and body | Sherry is drier and slightly higher ABV; the syrup restores the sugar |
| Dry vermouth | Fino sherry | Low sugar, saline register, similar ABV | Fino is drier and far more perishable (§3.2); it will not carry a wet Martini spec |
| Campari | Suze + 0.1 oz rich syrup | Bitterness at a similar intensity | Suze is earthier and paler; the color and orange note are lost |
| Aperol | Campari cut 1:1 with rich syrup and water | Sugar and roughly the bitterness | ABV still lands high; lengthen accordingly |
| Cointreau | Dry curaçao + 0.1 oz simple | ABV and orange register | Curaçao brings brandy and oak the triple sec does not |
| Orgeat (**nut allergy**) | Toasted seed orgeat (sunflower, pumpkin) or a toasted-rice orgeat | Sugar, viscosity, toasted-nutty register | Aroma differs materially — surface the swap to the drinker rather than making it silently (§3.5) |
| Falernum (**nut allergy**) | Rich syrup + lime zest + clove + ginger tincture | Sugar, spice register | Loses the almond note entirely; rebuild the spice level by taste |
| Simple syrup | Honey syrup 3:1 | Approximate sugar per oz | Honey's floral volatiles change the drink's identity; it also reads sweeter cold (§3.6) |
| Angostura | Peychaud's | Dash-scale seasoning role | Different register entirely — anise/cherry for clove/gentian; this is a redesign, not a swap |

---

## Section 4: Balance & the Drink Rescue Table {#drink-rescue-table}

A cocktail is balanced across **three axes at once**, and a diagnosis that names the wrong axis will make the drink worse:

1. **Strength** — finished ABV after dilution. Spirit-forward stirred drinks land at **25–35%**; sours at **12–18%**; highballs and spritzes at **5–12%**.
2. **Sweet ↔ sour** — sugar and acid suppress each other's perception nearly symmetrically, which is why a sour is stable across a *band* of ratios rather than balanced at a point.
3. **Texture and temperature** — viscosity, dilution, aeration, and cold. This axis is invisible on paper and accounts for most drinks that are "correct by the recipe" and still wrong in the glass.

Two arithmetic anchors to reason from. A stirred Martini-root build — 2.5 oz of a 47% base plus 0.5 oz of an 18% aromatized wine — carries 1.265 oz of ethanol in 3 oz, so **42% ABV pre-dilution**, falling to about **34%** after 25% dilution. A shaken sour — 2 oz of a 40% base, 1 oz citrus, 0.75 oz simple — carries 0.8 oz of ethanol in 3.75 oz, so **21% pre-dilution**, about **17%** finished. When a drink reads hot, check which of those two structures it actually is before adding anything.

### 4.1 The Drink Rescue Table {#the-drink-rescue-table}

| Symptom | Likely cause | Primary fix (and its cost) | Secondary fix (and its cost) | Tertiary fix (and its cost) |
|---|---|---|---|---|
| **Too boozy / hot** | Under-diluted, or the spec's ethanol load is genuinely too high for the sugar present | **More dilution** — stir or shake 5–10 s longer, or add 0.25 oz water directly. Cost: everything else gets proportionally weaker, including the aroma you wanted | **Swap part of the base for a lower-proof modifier** — replace 0.25–0.5 oz of the base with vermouth, sherry, or a 20% amaro. Cost: changes the flavor, not just the strength | **Add a texture agent** — 0.25 oz rich syrup, a few drops of 20% saline, or 0.5 oz egg white. Cost: sugar or protein you may not want; it masks the burn rather than removing it |
| **Too sweet** | Syrup overshoot, or an unaccounted-for liqueur (§3.4) carrying 250+ g/L | **Add acid** — 0.125–0.25 oz lemon or lime, or 2–3 drops of a 20% citric solution if you cannot spare the volume. Cost: volume and a citrus aroma the drink may not want | **Add bitterness** — 1–2 dashes of aromatic bitters, or 0.125 oz of a 7+ bitterness amaro. Cost: adds aroma and a little more alcohol | **Rebuild the sweetener** — remake with rich syrup at the same volume (drier per mL of water) or subtract the syrup entirely if a liqueur is already carrying it. Cost: a remake |
| **Too sour / puckering** | Acid overshoot, or an unusually acidic lime lot (juice runs 5–7%) | **Add sugar** — 0.125–0.25 oz simple; sugar suppresses sour perception directly | **Add a texture/fat agent** — egg white, cream, or 0.25 oz of a viscous liqueur. Cost: changes the drink's category | **Split the acid** — remake with part lemon or part malic acid for a rounder, longer sourness at the same titratable level. Cost: a remake |
| **Too bitter** | Amaro overshoot, over-expressed pith, or grapefruit's naringin stacking with an amaro | **Add sugar or a sweet modifier** — sugar is the most direct bitter suppressant on the palate | **Add salt** — 2–4 drops of 20% saline. Salt suppresses bitterness at concentrations well below its own detection threshold; this is the highest-leverage, lowest-cost fix in the table | **Dilute and re-cool** — bitterness scales with concentration; 0.25 oz more water plus fresh chill. Cost: strength and aroma |
| **Watery / flabby** | Over-dilution, warm ice, wet ice, or too little sugar and acid to carry the water | **Add back base and modifier at the original ratio** — a small "reinforcing" pour (e.g. 0.25 oz spirit + 0.1 oz syrup for a 2:0.75 drink). Cost: volume, so it only works if the glass has room | **Raise viscosity** — 0.125 oz rich or gomme syrup adds body without much sweetness. Cost: slight sweetening | **Remake on drier ice** — cold, dry, large-format ice; discard the wet ice. Cost: the current drink |
| **Flat / one-note** | No aromatic top layer; every ingredient sitting in the same register | **Add bitters** — 2 dashes of a complementary register (§3.8). This is the fastest fix in the table and costs almost no volume | **Add an expressed citrus peel** — orthonasal aroma with essentially zero volume and zero flavor change | **Split a role** — add a second modifier or a second base in the same slot (both are stackable) to build a longer temporal arc. Cost: a rebalance |
| **Too dilute** (distinct from watery — the flavors are right but faint) | Over-agitation, or melt from standing | **Reinforce proportionally**, as above; the ratios are correct, the concentration is not | **Serve on a single large rock** so further melt is slow, or serve up and drink faster | **Batch and pre-dilute deliberately** next time: hold the batch at −18 °C with dilution water already calculated in, so agitation adds chill and nothing else |
| **Not cold enough** | Too little ice, warm glassware, warm ingredients, or a shake stopped early | **Use more ice, not less** — a full tin chills faster and dilutes *less* than a half tin, because the larger thermal mass reaches equilibrium before much melting occurs | **Pre-chill the glass and the ingredients** — a frozen coupe is worth several degrees at no dilution cost | **Agitate longer.** Cost: dilution rises with time, so this is the last resort, not the first |
| **Muddy / smeared** | Too many ingredients in overlapping registers, over-muddled herbs (chlorophyll and bitter leaf compounds), or ice shards in a fine-textured drink | **Fine-strain** through a conical/tea strainer to remove shards and plant debris | **Cut an ingredient** — identify two ingredients holding the same slot in the same register and drop one; this is the case where redundancy is real | **Rebuild with roles separated** — one ingredient per job, then add back deliberately |
| **Cloying** (sweet *and* heavy, lingering) | Sugar plus low acid plus high viscosity, often a liqueur-sweetened drink with no citrus | **Add acid and bitterness together** — the two suppress sweetness by different mechanisms and stack cleanly | **Add carbonation or a lengthener** — 1–2 oz soda cuts the concentration and adds trigeminal bite from carbonic acid | **Lower the viscosity** — remake with 1:1 syrup instead of rich, or replace part of the liqueur with the equivalent spirit |
| **Thin texture** (tastes right, feels like water) | Nothing in the texture slot; a spirit-plus-juice build with no viscosity source | **Rich or gomme syrup** — gomme adds body without additional sugar (§3.6) | **Egg white (0.5–0.75 oz) or whole egg** — dry shake first, then shake with ice; adds foam and a protein mouth-coating | **Xanthan gum at 0.1–0.2% of total volume**, blended, for body without dairy or egg. Cost: overshoot reads slimy fast, so weigh it |

### 4.2 Diagnostic Order {#drink-diagnostic-order}

1. **Temperature first.** Touch the glass. A drink that is not cold reads simultaneously sweeter, hotter with ethanol, and less aromatic. Fix cold before you touch the spec — half of reported imbalance is a temperature failure wearing a costume.
2. **Then dilution.** Was this drink under- or over-diluted? Under-dilution reads hot and tight; over-dilution reads flabby. Both mimic ratio problems.
3. **Then the sweet/sour axis.** Only now compare the actual sugar and acid loads against the template, remembering that liqueurs and vermouths are carrying sugar the recipe may not name.
4. **Then bitterness and aroma.** These are the cheapest fixes — dashes and peels move perception a long way for almost no volume.
5. **Only then rebuild.** A remake is the correct call when the diagnosis is structural (wrong sweetener, wrong acid, two ingredients fighting for one slot), not when it is a matter of a quarter ounce.

**Golden rule:** adjust in units of **0.125 oz (≈4 mL) for syrup and citrus, 1 dash for bitters, 2 drops for saline, and 5 seconds for agitation** — and taste between each. As in the kitchen, you can add and you cannot subtract, and in a glass every addition also changes the ABV and the volume.

### 4.3 Taste-as-You-Build: Pre-Dilution vs Post-Dilution {#tasting-a-drink}

Professional practice is to taste the drink **twice** — once before chilling and once in the glass — because the two samples answer different questions.

**The pre-dilution taste (room temperature, undiluted, drawn with a straw from the mixing glass before ice).** This is where you check *ratios*. Because the sample will not be cold and will not be diluted, it should deliberately taste **wrong in three predictable directions**:

- **Noticeably sweeter than the finished drink should be.** Sweet perception is temperature-dependent — the TRPM5 channel in the sweet-taste pathway is substantially less responsive at low temperatures — so sweetness reads down when the drink is cold. Dilution then removes another 20–25% of the sugar concentration on top of that. A pre-dilution sample that tastes "correctly sweet" warm will land under-sweet cold. This effect is stronger for fructose-dominant sweeteners (honey, agave) than for sucrose.
- **Hotter and harsher with ethanol than the finished drink.** Ethanol potentiates the TRPV1 heat receptor, and TRPV1 is itself heat-activated, so a warm sample overstates burn. Do not "fix" alcohol heat from a warm taste.
- **More concentrated overall**, by exactly the dilution you are about to add.

What the pre-dilution taste *is* reliable for: whether the acid is present at all, whether an ingredient is spoiled (oxidized vermouth is unmistakable warm and easy to miss cold), whether two modifiers are fighting, and whether the aromatic layer exists.

**The post-dilution taste (the finished drink, or a sip from the strainer).** This is where you check *balance and texture*. Aroma release, sweetness, viscosity, and carbonation bite are all temperature-dependent, so this is the only sample that tells the truth about the drink the person will actually receive.

**Building the habit into the flow:**
- Taste every **citrus lot** before it goes in. Lime is the most variable and most time-sensitive of the bar citrus — its aroma shifts measurably within hours of juicing even refrigerated, while lemon holds noticeably longer. Adjust the syrup to that day's fruit rather than to the printed spec.
- Taste every **syrup** for concentration — a 1:1 that was boiled down is now a 1.4:1 and will overshoot.
- Smell every **aromatized wine and sherry** on opening and against the open date (§3.2). Oxidation is the most common silent failure in a stirred drink.
- For a **batch**, taste the batch at its *serving* dilution and *serving* temperature, not as concentrate. Batches taste correct as syrup and wrong in the glass more often than the reverse.
- Keep a **reference build** on hand when calibrating — the Daiquiri is the standard diagnostic drink precisely because it has nowhere to hide: three ingredients, all of them exposed, and any fault in the ice, the citrus, or the syrup shows up immediately.

### 4.4 Worked Rescues {#worked-rescues}

**An equal-parts bitter stirred drink that reads harsh and medicinal rather than bittersweet.**
Diagnosis order: the glass is cold, so temperature is not the fault. Dilution is short — it was stirred 15 seconds, not 25–30. Equal parts of a 44% base, a 24% bitter aperitivo and a 16% sweet vermouth is 0.84 oz ethanol in 3 oz, **28% pre-dilution**, and a spirit-forward drink under-diluted at 28% will lead with alcohol and gentian. Fix: stir 10 seconds longer to reach roughly 22–25% dilution, dropping the finished drink to about 23%. If it is still harsh, the vermouth is the next suspect — check the open date, because oxidized rosso loses its vanilla-and-cocoa cover and leaves the bitter liqueur naked. Only after both of those does the ratio come into question, at which point the correct move is walking the base slot back by 0.25 oz rather than adding syrup.

**A sour that tastes correct but feels like juice.**
Sugar and acid are both present at the template dose, so the sweet/sour axis is fine — the complaint is on the texture axis, which the ratio cannot address. Primary: rebuild the syrup as 2:1 at the same volume, which raises viscosity roughly ten-fold while slightly *reducing* sugar (§3.6). Secondary: 0.75 oz egg white, dry-shaken then shaken with ice, for foam and protein mouth-coating. Tertiary, if the drink must stay vegan and un-thickened: 2 drops of 20% saline, which raises perceived body and sweetness without adding either.

**A nut-orgeat tiki drink for a guest with a tree-nut allergy.**
Orgeat is the allergen and it is load-bearing — it supplies the almond aroma, roughly half an ounce of sugar-equivalent, and the viscosity that makes the drink read as tiki rather than as a rum sour. Do not silently drop it: the resulting drink is thin, dry, and unrecognizable. Surface the conflict, offer toasted seed orgeat or toasted-rice orgeat as the substitution, and note that the orange liqueur slot (§3.4) is unaffected. Then check the rest of the build for the same failure — falernum, amaretto, and crème de noyaux all appear in tiki specs and none of them contain a nut word (§3.5).

**A batched stirred drink that tastes flat at service after tasting perfect at prep.**
The batch was tasted as concentrate at room temperature, where sweetness and ethanol both read high and oxidation is obvious. In the glass, cold and at 22% dilution, the sugar drops out first. Fix at the source: pre-dilute the batch with the calculated water, hold it at −18 °C, and taste it at serving temperature and serving dilution before the first guest — not as syrup at the prep bench.


---

## Section 5: Dilution, Temperature & ABV Math {#dilution-temperature-abv}

### Overview: Chilling and Dilution Are One Variable, Not Two

The single most common error in drink design is treating "how cold" and "how watered" as independent knobs. They are not. In a mixed drink chilled by ice, essentially all of the cooling energy is paid for by melting that ice, and the melt water goes into the drink. You cannot buy cold without buying water. Dave Arnold makes this the organizing principle of the mixing chapters in *Liquid Intelligence* (2014), and it is the correct frame: a recipe is not "2 oz spirit, ½ oz syrup," it is "2 oz spirit, ½ oz syrup, and roughly ¾ oz of water you will not measure."

The energy accounting is simple and checkable:

| Quantity | Value | Consequence |
|---|---|---|
| Latent heat of fusion of water (ice → liquid at 0 °C) | 334 J/g (79.7 cal/g) | Every gram of melt buys 334 J of cooling |
| Specific heat of liquid water | 4.18 J/(g·K) | 100 g of drink cooled 20 K needs ~8,360 J |
| Specific heat of ethanol | 2.44 J/(g·K) | A higher-proof mix takes *less* energy to chill per gram |
| Specific heat of ice | 2.09 J/(g·K) | Ice below 0 °C absorbs heat *without* melting |
| Density of ethanol at 20 °C | 0.789 g/mL | Converts volume-ABV to mass and to grams of ethanol |

**The naive floor.** Take a spirit-forward mix at ~35% ABV pre-dilution, about 90 g in the glass, cooling from 20 °C to −5 °C. Its specific heat is roughly 0.30 × 2.44 + 0.70 × 4.18 ≈ 3.67 J/(g·K). Energy required: 90 × 3.67 × 25 ≈ 8,260 J. Divided by 334 J/g, that is ~25 g of ice melted — about 27% dilution by volume. That is the number you get if melting is the *only* cooling mechanism.

**Why real stirred drinks come in under it.** Freezer ice is not at 0 °C; it is typically at −15 to −20 °C. Warming a gram of ice from −18 °C to 0 °C absorbs 2.09 × 18 ≈ 38 J with *no* melting and *no* dilution. A mixing glass holds 150–250 g of ice; if even the outer shell of that mass warms to 0 °C during the stir, it contributes several thousand joules of free, dry cooling. This is why hard, cold, dry ice from a deep freezer produces a colder drink at lower dilution, and why wet ice sitting at 0 °C in a slushy bin produces a warmer, more watery one. The core of a large cube does *not* warm in 30 seconds, so the free contribution is bounded — treat it as a real effect of partial magnitude, not a loophole.

**Why alcohol makes the drink colder.** Ethanol depresses the freezing point of the mixture, so a spirit-forward drink has room to go below 0 °C where a juice-and-soda drink does not.

| Mixture ABV (v/v) | Approx. ethanol w/w | Approximate freezing point | Practical meaning |
|---|---|---|---|
| 0% | 0% | 0 °C / 32 °F | A zero-proof build cannot go meaningfully below freezing; it bottoms out near 0 °C |
| 10% | ~8% | ~−4 °C / 25 °F | Low-ABV spritz territory |
| 20% | ~17% | ~−9 °C / 16 °F | A shaken sour at service |
| 25% | ~21% | ~−12 °C / 10 °F | A diluted Negroni; will slush in a −18 °C freezer |
| 30% | ~25% | ~−15 °C / 5 °F | A finished Martini or Manhattan; thick and barely pourable at −18 °C |
| 35% | ~29% | ~−19 °C / −2 °F | The practical floor for a batch that must stay fully liquid at −18 °C |
| 40% | ~34% | ~−23 °C / −9 °F | Neat spirit; will not freeze in any household freezer |

Two design consequences follow. First, a batched, pre-diluted drink held in a domestic freezer (nominally −18 °C, though many run nearer −15 °C) stays **fully liquid above roughly 35% ABV**, goes **syrupy-to-slushy between about 25% and 35%**, and **freezes below 25%**. Most pre-diluted stirred cocktails land in the middle band, which is why freezer service is either accepted as deliberately viscous or handled by freezing the *undiluted* concentrate and adding measured chilled water at the pour (§7.11). Second, a zero-proof drink physically cannot be served as cold as its alcoholic parent — if the target texture depends on −6 °C, the zero-proof version needs a different lever (glycerol, viscosity, salt, higher acid) rather than more shaking.

### 5.1 Typical Dilution by Method

These are ranges from bar practice and from Arnold's published measurements, expressed as water added as a percentage of the pre-dilution liquid volume. **They are ranges, not constants.** They shift with ice temperature, ice wetness, ice size, agitation vigour, vessel material and ambient temperature. Any recipe that depends on a dilution figure to two significant digits is a recipe that will not reproduce.

| Method | Typical added water | Typical service temp | Notes on variance |
|---|---|---|---|
| Stirred, 1-inch cubes, 25–35 s | **~20–25%** | −7 to −3 °C | Wet ice or a warm mixing glass pushes toward 30%; hard dry ice and a chilled glass toward 18% |
| Stirred, single large rock in mixing glass | ~12–18% | −2 to +2 °C | Less surface area: slower chill *and* slower dilution. Rarely correct — you usually run out of patience before you run out of dilution budget |
| Shaken hard, 8–15 s | **~25–30%** | −8 to −4 °C | Ice fractures during the shake, spiking surface area; sloppy small or wet ice reaches 35%+ |
| Dry shake (no ice) | 0% | Rises 3–8 °C | Adds no water and *warms* the mix — this is the point |
| Whip shake (2–3 pellets, shaken to nothing) | ~10–15% | −2 to +2 °C | Deliberately under-diluted because crushed-ice service finishes the job |
| Thrown, 5–8 passes | ~15–20% | −4 to 0 °C | Aerates without fracturing ice; less dilution than shaking for similar integration |
| Rolled (ice in, gentle passes) | ~10–18% | −2 to +2 °C | Gentlest wet method |
| Built over ice, stirred briefly in glass | ~5–10% at service | 0 to +4 °C | Continues climbing throughout the drink — see §6.8 |
| Swizzled over crushed ice | ~25–35% at service | −4 to 0 °C | And still rising; swizzles are designed to be drunk fast |
| Blended | **50%+** | −4 to −1 °C | The ice *is* the drink; must be over-strengthened and over-seasoned to compensate |
| Batched and pre-diluted for freezer service | 20–25%, added by you | −12 to −18 °C | You measure the water in, so this is the only method where dilution is exact |

### 5.2 Ice Format: Surface Area Sets the Rate

Total dilution at equilibrium is set by the energy balance above. **Rate** is set by surface area, because convective heat transfer scales with contact area and with the temperature difference across it. For a cube, surface-area-to-volume ratio is 6/L — it varies inversely with edge length. Double the edge, halve the SA/V.

| Format | Edge / size | Mass per piece | SA/V (approx.) | Behaviour |
|---|---|---|---|---|
| Standard cube | 1 in / 2.5 cm | ~15 g | ~2.4 cm⁻¹ | The default for stirring and shaking; enough mass to survive agitation, enough surface to chill in 30 s |
| Large rock (single) | 2 in / 5.1 cm | ~120 g | ~1.2 cm⁻¹ | Half the SA/V of a 1-inch cube — the standard in-glass rock |
| King cube / sphere | 2.5 in / 6.4 cm | ~230 g | ~0.9 cm⁻¹ (sphere lower still) | A sphere has the minimum possible surface area for its volume; slowest melt of any format |
| Cracked / cheater cubes | 1–2 cm fragments | 1–5 g | ~5–10 cm⁻¹ | Fast chill, fast dilution; fine for shaking, ruinous for a slow-sipped rocks drink |
| Pellet / nugget | 6–10 mm | ~1 g | ~8–12 cm⁻¹ | Chills almost instantly; the Sonic-style pellet holds air and dilutes fast |
| Crushed | 2–5 mm shards | <1 g | ~15–25 cm⁻¹ | Roughly an order of magnitude more surface than a 1-inch cube. Reserved for drinks designed around fast dilution (juleps, swizzles, tiki) |

**Why the large rock in the glass matters.** A 2-inch rock has half the surface area per gram of a 1-inch cube, and one rock has far less total surface than the four or five small cubes it replaces. Over the 15–25 minutes a spirit-forward drink is actually sipped, that difference is the whole ballgame: the small-cube glass is watery at minute twelve, the rock glass is still recognisably the drink. The rock also enters colder in absolute terms if hard-frozen, and its low SA/V means its cold core survives longer.

**Clear ice and directional freezing.** Cloudiness in ice comes from dissolved gases and dissolved solids that the advancing crystal front rejects rather than incorporates, plus trapped micro-bubbles and internal stress fractures. Directional freezing exploits this: if water is insulated so it can freeze from one face only (the standard home method is an open, insulated cooler in a freezer, which freezes top-down), impurities and gas are pushed ahead of the front and concentrate in the last portion to freeze, which is cut away and discarded. Arnold treats this at length in *Liquid Intelligence*. The honest caveat: the strongest defensible claims for clear ice are aesthetic, plus the mechanical one — inclusions and internal stresses are crack initiation sites, and a cube that cracks gains surface area and melts faster. Claims that clear ice melts dramatically slower *purely by virtue of clarity*, at equal size and temperature, are not well supported; size and starting temperature dominate.

**Tempering.** Ice straight from a −18 °C freezer will craze and shatter on contact with room-temperature liquid, which is precisely the surface-area spike you were trying to avoid in a rocks drink. Letting a large rock sit 1–3 minutes before use reduces thermal shock. For stirring and shaking, do the opposite: use the coldest, driest ice you have, because that is where the dilution-free cooling comes from.

### 5.3 The ABV Calculation

The arithmetic is a volume-weighted average, then a dilution correction.

**Step 1 — Ethanol volume.** For each component, multiply its volume by its ABV expressed as a decimal. US proof is exactly 2 × ABV, so 90 proof = 45% ABV.

  ethanol_oz = Σ (volume_i × ABV_i)

**Step 2 — Pre-dilution ABV.**

  ABV_pre = ethanol_oz ÷ Σ volume_i

**Step 3 — Apply dilution.** Dilution d is expressed as a fraction of the pre-dilution volume.

  ABV_final = ethanol_oz ÷ (Σ volume_i × (1 + d))

Equivalently, ABV_final = ABV_pre ÷ (1 + d). Note what this means: dilution never changes the ethanol in the glass, only its concentration. The drinker consumes the same alcohol either way.

**Step 4 — Standard drinks.** Divide the ethanol volume by the local standard-drink definition (see §5.5).

#### Worked Example A — a stirred spirit-forward build

| Component | Volume | ABV | Ethanol contributed |
|---|---|---|---|
| Base spirit, 90 proof | 2.00 fl oz | 45% | 0.900 fl oz |
| Aromatized wine (sweet vermouth style) | 1.00 fl oz | 16% | 0.160 fl oz |
| Aromatic bitters, 2 dashes (~1.2 mL) | 0.04 fl oz | 44.7% | 0.018 fl oz |
| **Pre-dilution total** | **3.04 fl oz** | **35.5%** | **1.078 fl oz** |

Stirred to 22% dilution: water added = 0.22 × 3.04 = 0.67 fl oz. Final volume 3.71 fl oz (110 mL). Final ABV = 1.078 ÷ 3.71 = **29.1%**.

Sensitivity check across the plausible stirred band: at 20% dilution the drink lands at 29.6%; at 25%, at 28.4%. **The served ABV barely moves.** What moves across that band is temperature, viscosity and the perceived heat of the alcohol — which is exactly why "stir until cold" is a texture instruction, not a strength instruction. Ethanol served: 1.078 fl oz = **1.80 US standard drinks**.

#### Worked Example B — a shaken sour

| Component | Volume | ABV | Ethanol contributed |
|---|---|---|---|
| Base spirit, 80 proof | 2.00 fl oz | 40% | 0.800 fl oz |
| Fresh citrus juice | 0.75 fl oz | 0% | 0 |
| Simple syrup, 1:1 by weight | 0.75 fl oz | 0% | 0 |
| **Pre-dilution total** | **3.50 fl oz** | **22.9%** | **0.800 fl oz** |

Shaken to 27% dilution: water added = 0.945 fl oz. Final volume 4.45 fl oz (132 mL). Final ABV = 0.800 ÷ 4.45 = **18.0%**. Ethanol served: **1.33 US standard drinks**.

Read the two examples together. The sour starts 12 points lower in ABV, takes *more* water, and finishes at 18% — but it also finishes at 4.45 fl oz versus 3.71, which is why a sour needs a larger coupe. **Glassware must be sized to the post-dilution volume, not the recipe as written.** A 4.5 oz coupe cannot hold Example B.

### 5.4 Chilling Glassware and Serving Temperature

An unchilled glass is a heat reservoir sitting inside the drink. Soda-lime glass has a specific heat of ~0.84 J/(g·K); a 180 g coupe warming from 22 °C to 0 °C would absorb ~3,300 J — comparable in magnitude to the ~8,300 J spent chilling the drink itself. In practice only the inner surface equilibrates in the first seconds, so the real penalty is smaller, but it is routinely worth 2–5 °C on a drink served up. That is the whole margin between a Martini and a disappointment.

| Chilling method | Time to effective chill | Mechanism |
|---|---|---|
| Freezer, dry | 20–30 min | Still air is a poor conductor (~0.026 W/(m·K)); slow but requires no attention and chills the whole mass |
| Packed ice + water, filled | 2–3 min | Water conducts heat ~23× better than air (~0.6 W/(m·K)) and convects; far faster than dry freezer air |
| Packed ice, no water | 5–8 min | Point contact only; much slower than ice slurry |
| Rinse with crushed ice, swirl, discard | 30–60 s | Fastest expedient; partial only |

**Serving temperature targets by family.** Treat as targets, not measurements; published figures vary with vessel, room and technique.

| Family | Target at service | Rationale |
|---|---|---|
| Stirred, spirit-forward, up (Martini, Manhattan, Negroni up) | −7 to −3 °C / 19–27 °F | Cold suppresses ethanol burn and thickens the liquid perceptibly; freezing-point depression makes this reachable |
| Freezer-batched, pre-diluted, straight pour | −12 to −18 °C / 10 to 0 °F | Pourable above ~30% final ABV; fully liquid only above ~35% |
| Shaken sour, up | −8 to −4 °C / 18–25 °F | Shaking overshoots stirring on temperature; the extra cold offsets the acid's sharpness |
| Egg / dairy drinks | −4 to 0 °C / 25–32 °F | Foam is less stable at extreme cold; protein networks want the milder end |
| Spirit + ice, rocks (Old Fashioned) | 0 to +4 °C / 32–39 °F | An ice-in-glass system pins near 0 °C and stays there while ice remains |
| Highball / carbonated | 0 to +4 °C / 32–39 °F | CO₂ retention demands the coldest practical liquid — see §6.9 |
| Blended / frozen | −4 to −1 °C / 25–30 °F | Below this the slush seizes and stops pouring |
| Hot drinks (toddy, Irish coffee) | 60–70 °C / 140–158 °F | Above ~75 °C, ethanol and volatile aromatics escape rapidly and the drink scalds; never boil |
| Room-temperature / low-dilution builds | 18–20 °C / 64–68 °F | Deliberate: some amaro and vermouth service is warmer by design |

### 5.5 Standard Drinks and Responsible Service

A finished drink's strength (%ABV) tells you how it tastes. The **ethanol volume** tells you what it does. Only the second number matters for service.

| Jurisdiction | One standard drink | Pure ethanol |
|---|---|---|
| United States (NIAAA) | 0.6 fl oz | 14 g |
| United Kingdom | 1 unit = 10 mL | 8 g |
| Australia / New Zealand | 12.5 mL | 10 g |
| Canada | ~17 mL | ~13.5 g |

Worked back to the examples above: the stirred build in Example A is **1.8 US standard drinks** and the shaken sour in Example B **1.33**, before any garnish, second round, or the fact that a 3.7 fl oz drink is finished in ten minutes. A three-cocktail evening of spirit-forward stirred drinks is five to six standard drinks. Design accordingly — that is what low-ABV templates, split bases and long builds are *for*, not merely a stylistic preference.

Practical service rules, stated once and without moralising: serve water alongside; do not serve anyone underage; do not serve anyone already impaired; keep a genuine zero-proof option on the list that was designed rather than subtracted; and when a guest asks how strong something is, give them the standard-drink number, not the ABV.

---

## Section 6: Build Methods {#build-methods}

### Overview: The Method Is Determined by the Ingredients

Build method is not a stylistic choice. It is determined by what is in the glass. Every ingredient class has a physical requirement — needs emulsifying, needs aerating, needs suspending, must not be agitated — and the method is whichever one satisfies all of them simultaneously. *Cocktail Codex* (Alex Day, Nick Fauchald and David Kaplan, 2018) organises the entire cocktail canon into six root templates — Old-Fashioned, Martini, Daiquiri, Sidecar, Whisky Highball, Flip — and each root carries its method with it. Knowing the root tells you the method before you have read the recipe.

### 6.1 Stirred

**When:** every component is a spirit, fortified wine, liqueur, bitter or syrup. No citrus, no dairy, no egg, no purée, no carbonation.

**Why not shake it:** shaking a spirits-only build achieves nothing it needs and inflicts three things it does not want. (1) **Aeration** — the shake whips in a dense cloud of micro-bubbles that clouds the drink and gives it a prickly, frothy, thin mouthfeel; the haze clears in a minute or two, the ruined texture does not, because by then the drink is also over-diluted. (2) **Ice shards** — violent agitation fractures ice into fines that pass a standard strainer and continue melting in the glass. (3) **Over-dilution** — shaking overshoots the 20–25% band. A spirit-forward drink is judged on clarity, on viscosity, and on a dense, slick, cold texture. Stirring produces exactly that; shaking destroys all three. There is no ingredient in an all-spirits build that needs emulsifying or suspending, which is the only reason shaking exists.

**How:** fill the mixing glass with ice above the liquid line, insert the barspoon between ice and glass wall, and rotate smoothly with the wrist so the ice turns as a body rather than tumbling. 25–35 seconds, roughly 40–60 revolutions; the house specs in *Death & Co* sit around 30 seconds, which is a reasonable default. Strain with a julep strainer.

### 6.2 Shaken

**When:** the build contains citrus juice, any other fruit juice, purée, dairy, cream, egg, aquafaba, cream of coconut, or any other cloudy, viscous or non-miscible non-spirit component.

**Why:** three reasons, all mechanical. (1) **Integration** — juice, syrup and spirit are not homogeneous at rest and different densities layer; shaking forces them into a single phase. (2) **Aeration** — a sour *wants* the light, lifted texture and the fine bubble load; that is what makes citrus drinks refreshing rather than merely sour. Opacity is a feature. (3) **Rate of chill** — a sour carries more non-alcoholic volume and therefore more thermal mass, and it needs to get very cold quickly; the ice fracture during a shake spikes surface area and delivers that.

**How:** 8–15 seconds, hard, with 1-inch cubes filling the small tin. Longer does not help much once the ice is fractured; harder does. **Double-strain** (Hawthorne strainer plus fine-mesh cone) any shaken drink served up, to remove ice fines and citrus pulp — the fines keep diluting in the glass and the pulp muddies the texture.

### 6.3 Dry Shake (Egg and Foam Builds)

**Sequence:** shake all ingredients *without ice* first, then add ice and shake again, then double-strain.

**Mechanism:** mechanical shear partially unfolds egg white's globular proteins without heat; the unfolded chains adsorb at the air–water interface and cross-link into an elastic film around each bubble. The protein inventory and the ethanol-destabilization problem are in §1.6.

**Why the ice comes second:** protein unfolding and migration to interfaces both slow markedly at low temperature — cold, viscous liquid foams poorly. The ice-free first shake is warmer and more fluid, so the network builds fast and it builds without adding a drop of water. The second, iced shake then chills and dilutes a foam that already exists. Citrus acid also progressively denatures and eventually coagulates the protein, so do not let a mixed egg build sit before shaking; grainy foam is over-acidified, under-agitated foam.

### 6.4 Reverse Dry Shake

**Sequence:** shake *with ice* first, strain the ice out, then shake the chilled liquid again *without ice*, then pour.

**Why the order matters:** in the standard dry shake, the foam is built first and then subjected to a violent iced shake that partially tears it down and leaves ice fines embedded in it. Reversing the order does the abusive part first — chilling and diluting while there is no delicate structure to damage — and then builds the final foam on already-cold, already-diluted, ice-free liquid. Nothing further dilutes it and no shards remain to pop bubbles. The result is generally a denser, finer-bubbled, glossier head that survives longer on the glass. The technique is widely associated with Jeffrey Morgenthaler, who covers egg drinks and foam handling in *The Bar Book* (2014). The common trick of adding a Hawthorne spring to the dry shake as an agitator is contested — it does add shear, but whether the finished foam is measurably better is not settled; treat it as optional.

**Choosing between them:** dry shake is faster and adequate for a standard whiskey sour or a Pisco Sour with a decorative head. Reverse dry shake is worth the extra pass when the foam is the point — anything where the head carries a garnish, a bitters design, or the drink's whole visual identity.

### 6.5 Whip Shake

**When:** drinks served over crushed ice that carry heavy, integration-resistant ingredients — falernum, orgeat, cream of coconut, fruit purée, thick syrups. Much of the tiki canon.

**How:** add 2–3 pellets or a small scoop of crushed ice and shake until the ice is completely gone, then pour the whole thing unstrained into a glass packed with fresh crushed ice.

**Why:** the goal is aeration and integration at *minimum* dilution, ~10–15%, because crushed-ice service will add another 15–25% within the first few minutes. A full shake plus crushed-ice service produces a drink that is watery before it reaches the table. The disappearance of the ice is the timer — you cannot over-shake a whip because it ends itself.

### 6.6 Throwing

**How:** pour the drink from one vessel to another in a long, high arc, straining the ice out of each pass, then return and repeat. 5–8 passes.

**Why:** the arc drags air through the liquid, so it aerates and integrates, but nothing is fracturing ice, so it dilutes less than shaking (~15–20%) and produces a silkier texture with larger, softer bubble structure rather than the tight foam of a shake. It also chills adequately if the passes are quick. Traditional for Bloody Marys — a hard shake breaks tomato pulp into a froth and gives a broken, foamy texture — and for Spanish and Cuban vermouth and highball service.

### 6.7 Rolling

**How:** pour gently back and forth between two tins with the ice left in, three to five passes.

**Why:** the gentlest wet method. Integrates and chills with minimal aeration and minimal dilution (~10–18%). Where throwing wants air, rolling deliberately avoids it. The correct method for savoury and pulpy builds where any foam reads as a defect, and for delicate builds you want mixed but not lifted.

### 6.8 Building in Glass

**When:** highballs, Old Fashioneds, spritzes, anything served over ice where the serving ice is also the mixing ice.

**How:** ingredients into the serving glass over fresh ice, brief stir (3–8 revolutions), garnish. Dilution at service is only ~5–10% and then climbs continuously — which is the design intent for a long drink. Because so little dilution has occurred at the moment of service, a built drink tastes *stronger* at the first sip than a stirred drink of the same recipe and correctly so; the arc of the drink is part of the recipe.

### 6.9 Carbonated Builds

**The rule: never shake a carbonated drink, and never stir one hard.** This overrides every other rule in this section. If a build contains soda, tonic, sparkling wine, beer or a pre-carbonated base, the method is dictated by CO₂ retention.

**Mechanism:** dissolved CO₂ obeys Henry's law — the amount in solution is proportional to the CO₂ partial pressure above it — and its solubility falls sharply with temperature.

| Temperature | CO₂ solubility in water at 1 atm | Practical meaning |
|---|---|---|
| 0 °C / 32 °F | ~3.3 g/L | Nearly double the room-temperature figure |
| 10 °C / 50 °F | ~2.3 g/L | Refrigerator door |
| 20 °C / 68 °F | ~1.7 g/L | Room temperature; half the carbonation capacity of 0 °C |
| 25 °C / 77 °F | ~1.5 g/L | A warm mixer is already half-flat before you open it |

Agitation destroys carbonation two ways: it creates enormous gas–liquid interfacial area for CO₂ to escape across, and it introduces nucleation sites where bubbles form and grow. Sugar and dissolved solids reduce solubility further, and any rough surface, crystal or dragged bar spoon will nucleate a gush.

**Correct procedure:**
1. Chill everything — mixer, spirit, glass, and ice — as close to 0 °C as you can manage. Arnold's carbonation work in *Liquid Intelligence* treats near-freezing temperature as the precondition, not an optimisation.
2. Build and chill the non-carbonated portion first, in the glass or separately.
3. Add ice, then add the sparkling component last, poured down the wall of a tilted glass or over the back of a spoon, never straight into the middle.
4. Stir once, gently, by lifting the bar spoon vertically from the bottom to the top — one lift, not a rotation. Or do not stir at all; the pour itself mixes adequately.
5. Serve immediately. A highball has a shorter shelf life on the pass than any other drink on the list.

### 6.10 Blending

**When:** frozen drinks, and only frozen drinks.

**Key adjustment:** the ice is simultaneously the coolant, the diluent and the texture, and blended drinks routinely finish above 50% dilution. A blended recipe must therefore be built stronger, sweeter and more acidic than the still version of the same drink. Two independent effects compound: the dilution itself, and the fact that extreme cold suppresses sweetness perception and slows the release of volatile aromatics, so a frozen drink tastes flatter and less sweet than the same liquid at 10 °C. Under-seasoning a frozen drink is the default failure mode.

**Method discipline:** weigh the ice rather than eyeballing it. Volume measures of ice are unreliable because the packing fraction varies wildly with format. Blend to a smooth, pourable slush that mounds slightly on the spoon; a drink blended past that point has warmed from the blade's mechanical energy and will separate.

### 6.11 Swizzling

**How:** pack the glass with crushed ice, add ingredients, insert a swizzle stick (traditionally the *bois lélé* stem from the Caribbean) and spin it between the palms while raising and lowering it, until frost forms on the outside of the glass. Then top with fresh crushed ice and garnish.

**Why:** chills, dilutes and mixes in place, so a drink built directly in the serving vessel arrives fully integrated and aggressively cold with a frozen exterior. The frost line is the doneness cue — a genuinely objective one, unlike "shake until cold." Dilution is high (25–35% and climbing), which is why swizzles are built on assertive, high-proof, high-flavour bases. The Queen's Park Swizzle is the canonical form.

### 6.12 The Decision Rule

Apply in order. The first rule that matches determines the method.

| # | Test on the ingredient set | Method | Reason |
|---|---|---|---|
| 1 | Contains any carbonated component | **Build; add sparkling last; one vertical spoon lift or no stir** | CO₂ retention overrides everything else |
| 2 | Served frozen / slush | **Blend** | Ice is the texture; weigh it |
| 3 | Contains egg, aquafaba, or dairy *and* a foam is wanted | **Dry shake or reverse dry shake, then finish per rule 4** | Protein foams need ice-free agitation to build |
| 4 | Contains citrus, other juice, purée, cream of coconut, or dairy — and is served up or on cubes | **Shake hard 8–15 s, double-strain** | Needs emulsifying, aerating and fast chill |
| 5 | As rule 4, but savoury/pulpy (tomato, vegetable juice) | **Throw** (aerated) or **roll** (unaerated) | A hard shake froths pulp and breaks the texture |
| 6 | As rule 4, but served over crushed ice with heavy syrups or purées | **Whip shake**, pour unstrained over fresh crushed ice | Crushed-ice service supplies the remaining dilution |
| 7 | Built in the serving glass over crushed ice with an assertive base | **Swizzle** | In-glass integration; frost line is the endpoint |
| 8 | Spirit + sugar + bitters, served on ice (Old-Fashioned root) | **Build in glass over one large rock**, or stir and strain over fresh ice | Low service dilution by design; the drink evolves as it is drunk |
| 9 | Long build: spirit + non-carbonated mixer over ice | **Build in glass, brief stir** | Nothing requires emulsifying; the ice does the rest |
| 10 | Everything is spirit, fortified wine, liqueur, bitters or syrup — no juice, dairy, egg, or bubbles | **Stir 25–35 s, strain** | Clarity, viscosity and controlled dilution |

**Ambiguous cases and how they resolve.**

| Case | Resolution | Reason |
|---|---|---|
| A spirits-only drink with a *dash* of citrus juice (e.g. ¼ oz or less) | Stir if the drink is meant to be clear and spirit-forward; shake if the citrus is a stated flavour | Below roughly ¼ oz the juice is a seasoning, not a phase to integrate. Judgement call — state which you chose and why |
| Champagne cocktail with citrus (French 75) | **Shake the non-sparkling portion, strain into the glass, top with sparkling** | Rule 1 applies only to the carbonated component; the rest still needs shaking |
| Cream liqueur with no fresh dairy (e.g. a spirits-only build using an emulsified liqueur) | Shake | It is a pre-formed emulsion that will still separate at rest |
| Milk punch, clarified | Stir or build — it is a clear liquid | Clarification has already removed the phase that required shaking |
| A drink that is genuinely 50/50 between two roots | Follow the root that owns the *texture* you want; document the choice | *Cocktail Codex*'s root templates are the tiebreak, not the ingredient count |


---

## Section 7: Bar Prep Projects — Syrups, Cordials, Infusions, Clarification, Batching {#bar-prep-projects}

Everything in Sections 1–6 happens in the ninety seconds between order and service. This section covers the other half of bar work: the days-scale preparations built in advance, which are where a drink's distinguishing character usually comes from. A Mai Tai is not made at the station — it is made when the orgeat is made. Jeffrey Morgenthaler's *The Bar Book* frames this correctly: the bartender's leverage is upstream of the shaker.

Three disciplines apply to every prep in this section and are not repeated in each subsection:

1. **Weigh, don't measure.** Sugar volumes vary 15–20% with crystal size, packing, and humidity. A syrup specified by weight is reproducible across bartenders and across months; a syrup specified in cups is not. Morgenthaler is emphatic on this point and it is the single highest-yield process change in a home bar.
2. **Label with a date, not a name.** Every prep below has a shelf life measured from production. An unlabeled bottle is a bottle you will eventually have to throw away.
3. **Taste for the endpoint.** Timings given below are starting brackets calibrated to typical ingredient strength. Chile heat, tea tannin, and oak extraction all vary by an order of magnitude between lots. The clock tells you when to start tasting; it does not tell you when to stop.

### 7.1 The Syrup Family: Production, Water Activity, and Shelf Life

Sugar syrups are the sweetening backbone of the entire sour and highball families. **The ratios, sugar-per-mL figures, viscosities, and substitution arithmetic are in §3.6** — that is the design table and it is not repeated here. This section covers what happens between making a syrup and throwing it away.

**Which ratio to actually keep on the shelf.** 2:1 by weight sits at roughly sucrose saturation and will throw crystals in a cold fridge, so **1.5:1 (≈60% sugar) is the ratio most bars run day to day**: most of the shelf life and most of the body of 2:1, with no crystallization risk. Reach for true 2:1 when the drink wants the full viscosity jump, and stabilize it with demerara or a trace of citric acid. Dissolve every ratio **cold** — three minutes of shaking, no heat.

**Why syrups spoil.** Sugar suppresses water activity, but not enough to sterilize: a 1:1 syrup sits around a_w 0.90–0.93 and a 2:1 around 0.85, while osmophilic yeasts (*Zygosaccharomyces* spp.) and common molds grow well below that. Sugar alone buys you weeks, not months. Refrigeration is doing most of the work.

**Extending it — the honest mechanism.** The organisms that ruin syrup are acid-tolerant yeasts and molds, which is why acidification is a weak preservative here and ethanol is a strong one.

- **High-proof neutral spirit** is the effective route. One part 190-proof neutral spirit per 19 parts syrup yields ~4.75% ABV; 1 oz of 80-proof vodka per 8 oz of syrup yields ~4.4%. Either range meaningfully retards yeast and mold and typically doubles to triples refrigerated life. It also adds a trace of ethanol to the finished drink, which is negligible at cocktail dose.
- **Citric acid** at 0.1–0.25% w/w drops pH below ~3.5 and does inhibit bacterial spoilage, but bacteria were never your problem in a 50%-sugar solution. Its real utility is different: acid slowly inverts sucrose to glucose + fructose, and invert sugar resists crystallization. Use citric to stop a rich syrup from throwing crystals, not to sterilize it.
- **Filtration and clean bottling** matter more than either. Decant into a sanitized bottle, never return a used pour spout to the batch, and never top up an old bottle with new syrup.

**Failure modes.** *Crystallization*: 2:1 by weight is ~67% sucrose, which is essentially the saturation limit at 20 °C and above it at refrigerator temperature (~64%). A true 2:1 will drop crystals in the cold. Fixes: make it 1.5:1, use demerara or turbinado (the invert and molasses fraction depresses crystallization), or add 0.1% citric acid. *Scorching*: heating sugar syrup to a boil to "dissolve faster" caramelizes the edges and introduces a burnt note that never leaves; sucrose dissolves in cold water with three minutes of shaking or stirring. *Fermentation*: a syrup that fizzes, smells solvent-like, or has a pressurized cap has been colonized — discard, do not "cook it off."

### 7.2 Infused Syrups: Cinnamon and Friends

Infused syrups carry a spice or botanical into the drink already dissolved in the sweetener, so the aromatic and the sugar arrive together and at a fixed ratio.

| Syrup | Base | Botanical load per 500 mL syrup | Method and timing | Shelf life (refrigerated) |
|---|---|---|---|---|
| Cinnamon | 2:1 demerara | 3–4 cassia sticks, cracked | Bring syrup to a bare simmer, kill the heat, add cinnamon, steep 8–12 h covered, strain | 3–4 weeks |
| Ginger | 1:1 cane | 150 g fresh ginger, juiced or grated | Blend juice into cold syrup, no heat, rest 1 h, fine-strain | 1–2 weeks — fresh ginger juice degrades fast |
| Vanilla | 2:1 demerara | 2 pods, split and scraped | Warm steep 2–4 h, or cold steep 3–5 days | 1–2 months |
| Chile / spiced | 1:1 cane | 1–2 dried chiles, or 1 fresh, sliced | Cold steep, **taste every 10 min**, strain at target | 2–3 weeks |
| Hibiscus / tea / floral | 1:1 cane | 15–20 g dried | Steep at 80 °C for 5–10 min only, strain | 1–2 weeks |
| Mint / delicate herb | 1:1 cane | 30 g leaves | Blanch 10 s, shock, blend into cold syrup, fine-strain | 3–5 days; the color goes first |

**The general rule for infused syrups**: hard, dense, low-volatile material (cinnamon bark, vanilla pod, whole spice, dried root) wants heat and hours. Soft, high-volatile material (fresh herbs, flowers, tea, citrus zest, fresh chile) wants cold or brief warm contact and minutes, because the compounds you want boil off and the compounds you don't — tannins, chlorophyll bitterness, capsaicin — keep extracting.

**Failure mode**: leaving tea, zest, or cinnamon in the syrup "to get stronger overnight." The additional hours extract tannin and bitter phenolics far faster than they extract the aromatic top notes, which were fully extracted in the first thirty minutes. You do not get a stronger syrup; you get a bitter one.

### 7.3 Oleo-Saccharum

The oldest sweetener technique in the punch repertoire and still the highest-return prep in this section. David Wondrich's *Punch* is the standard modern account of it.

**Mechanism.** Citrus essential oil lives in the flavedo — the colored outer layer of the peel — sealed in oil sacs. Sugar in direct contact with cut peel draws water osmotically out of the peel tissue; the cell walls collapse, the sacs rupture, and the released oil dissolves into the syrup that forms as the sugar takes on that water. The result is a syrup carrying the whole terpene fraction of the peel — limonene, citral, linalool — at a concentration you cannot reach with juice or zest alone. Juice is acid; peel oil is aroma. They are different ingredients from the same fruit.

**Formula.** Peel 6 lemons (or 4 large grapefruit, or 8 limes) in wide strips using a Y-peeler, taking flavedo only. Combine with 175–200 g caster sugar — roughly equal weight of sugar to peel, and about 30 g sugar per lemon's worth of peel. Muddle briefly to bruise, cover, and hold.

**Timing and yield.** At room temperature, 4–12 hours; overnight is the standard bar practice. Refrigerated, 12–24 hours. The peels will be limp and pale and sitting in a pool of intensely fragrant syrup. Yield from 6 lemons is roughly 90–120 mL of finished oleo-saccharum, with maybe 20–25% of the sugar still undissolved — stir in 30–60 mL of the fruit's own juice, or an equal volume of hot water, to take the rest into solution.

**Accelerations.** Muddling more aggressively, warming gently (never above ~50 °C, which volatilizes the top notes), or vacuum-sealing the peel-and-sugar in a chamber bag all shorten the wait; *Liquid Intelligence* covers the vacuum route. None of them beat overnight for aroma fidelity.

**Shelf life.** 1 week refrigerated as-is; 2–3 weeks if you dissolve it into syrup and add high-proof spirit. It is not a keeper — the terpenes oxidize.

**Failure mode.** Pith. Any white albedo taken with the peel contributes limonin and naringin, and the syrup turns bitter within hours in a way that no amount of sugar corrects. Peel shallow, and if a strip comes off thick, scrape it.

### 7.4 Orgeat — ⚠ TREE NUT ALLERGEN

Orgeat is an almond syrup with orange flower water, and it is the ingredient that makes a Mai Tai a Mai Tai. **It is a tree nut product.** So are Amaretto, Frangelico, Nocino, crème de noyaux, and most falernum. Nut exposure in a bar arrives almost entirely through sweeteners and liqueurs rather than through anything visibly nutty, and any allergen screen that only looks for the word "almond" on an ingredient list will miss every one of them. See §3.5 for the full allergen mapping.

**Formula (yields ~700 mL).** 300 g blanched almonds, 600 g water, 600 g sugar (adjust to a 1:1 by weight with the strained almond milk), 15 mL orange flower water, 30 mL brandy or overproof rum, optional 5 mL rose water.

**Method and timing.**
1. Toast the almonds lightly at 160 °C for 8–10 minutes if you want the Morgenthaler-style roasted profile; skip for the classic pale, floral version.
2. Soak in the water 4 hours to overnight, refrigerated.
3. Blend hard, 60–90 seconds, to a fine slurry.
4. Steep 2–4 hours refrigerated, then strain through a nut-milk bag or doubled cheesecloth, squeezing hard. You now have almond milk.
5. Weigh the milk; add an equal weight of sugar and dissolve without heat.
6. Add the orange flower water **last and by drops** — it is a fierce ingredient and the difference between "floral" and "soap" is about 5 mL in 700. Add the spirit.

**Shelf life.** 2 weeks refrigerated, and that is optimistic — orgeat is a fat-bearing emulsion and both the almond lipids and the floral top notes are perishable. It freezes well in ice-cube trays for 3 months. Separation on standing is normal; shake before use. Souring, a sharp paint-like smell, or any sign of gas means discard.

**Failure modes.** Over-toasting the almonds (bitter, and it dominates); over-dosing the orange flower water (unrecoverable); under-straining (a gritty syrup that clogs a Hawthorne and reads as sandy on the palate).

### 7.5 Falernum — ⚠ CONTAINS ALMOND IN MOST FORMULATIONS

A Barbadian lime-clove-ginger-almond sweetener, sold both as a non-alcoholic syrup and as a low-proof liqueur (John D. Taylor's Velvet Falernum is ~11% ABV). It is a load-bearing ingredient in the Corn 'n' Oil, the Zombie, and a large fraction of the tiki canon.

**Formula (yields ~700 mL, ~11–18% ABV).** Zest of 9 limes, 40 whole cloves lightly cracked, 30 g fresh ginger sliced, 180 mL overproof rum (Wray & Nephew or similar). Combine, seal, and infuse 24 hours at room temperature. Strain. Add 400 g sugar dissolved in 250 mL water, 15 mL fresh lime juice, and 1–2 mL almond extract (or 60 mL of the orgeat above, in which case say so on the label).

**Shelf life.** 4–6 weeks refrigerated; the ethanol content earns it more life than orgeat gets. Failure mode: leaving the cloves in past 24 hours, which pushes eugenol from "warm spice" into "dentist's office" — clove is the most over-extracting botanical on this list.

### 7.6 Cordials and Acid-Adjusted Citrus

In modern bar usage a **cordial** is a sweetened, acidified, flavored syrup that replaces the juice-plus-sugar pair in a spec with a single shelf-stable ingredient. The technique is Dave Arnold's territory; *Liquid Intelligence* is the primary reference and the source of the practice of treating acidity as a dial you set rather than a property you inherit from a fruit.

**The numbers that make it work** are the titratable-acidity figures in §3.7 — lime 5–7%, lemon 5–6%, grapefruit 1.5–2.5%, orange and pineapple around 1%, apple lower still.

A sour built on lime is calibrated to ~6% acid. Substituting orange juice one-for-one delivers roughly one-fifth the acid, which is why the drink collapses into sweetness. **Acid adjustment** fixes this: dissolve crystalline acid into the low-acid juice until it reaches ~6% w/v, and it now behaves structurally like lime while keeping its own aroma. To bring 1 L of orange juice from ~1% to 6%, you add roughly 50 g of acid.

**Which acid.** The perceptual characters are tabulated in §3.7. For lime specifically, blends in the range of 1:1 to 2:1 citric:malic by weight are the usual approximation; the exact ratio is a taste decision, not a formula. Mix a 6% solution in plain water and taste the blend before committing a litre of juice to it.

**A lime cordial (yields ~750 mL).** Make an oleo-saccharum from the peels of 10 limes and 250 g sugar (§7.3). Dissolve into 500 mL water with 250 g additional sugar. Add citric acid to ~4% w/v and malic to ~2% w/v of the final volume (about 30 g and 15 g respectively for 750 mL). This is a peel-driven cordial — it tastes like lime aroma with lime structure, and unlike lime juice it keeps 4–6 weeks refrigerated. Failure mode: dosing acid into the finished cordial without measuring the volume first. Acidity is nonlinear on the palate above ~7% and an over-acidified cordial cannot be corrected without diluting away the flavor you built.

### 7.7 Shrubs and Drinking Vinegars

A shrub is fruit, sugar, and vinegar. It delivers acidity with a fermented, rounded character that citrus cannot produce, and because it is simultaneously low-pH and high-sugar it is the most shelf-stable prep in this section.

**Cold process (preferred).** 1 part fruit : 1 part sugar by weight. Macerate refrigerated 24–48 hours, stirring once or twice; the sugar draws the juice out osmotically without heat. Strain, pressing lightly. Add vinegar to roughly 1 part vinegar : 1 part strained syrup by volume. Then **rest it** — 1 to 4 weeks refrigerated. A young shrub tastes like a fight between the vinegar and the fruit; the rest is what merges them.

**Hot process.** Simmer fruit, sugar, and vinegar together 10–15 minutes, strain. Ready same-day and better at extracting from hard fruit (quince, cranberry, whole spice). It costs you the fresh volatiles — a hot-process strawberry shrub tastes like jam, a cold-process one tastes like strawberries. Use hot for fruit that needs breaking down, cold for anything whose aroma you care about.

**Vinegar choice.** Apple cider (rounded, fruity), champagne or white wine (clean, lets fruit lead), sherry (nutty, oxidative, excellent with stone fruit), rice (mild, low acid ~4%), balsamic (sweet, dominant — use as an accent). Avoid distilled white vinegar: 5% acetic acid with no aromatic contribution reads as harsh.

**Yield and shelf life.** 500 g fruit + 500 g sugar yields roughly 400–450 mL of syrup pre-vinegar, ~800–900 mL finished. Refrigerated shelf life 6 months and often more; the combination of pH below 3.5 and high sugar is genuinely hostile. Failure mode: serving it young, and using so much that the drink reads as salad dressing — 15–22 mL in a highball is usually the ceiling.

### 7.8 Infusions: Fast Botanicals, Slow Botanicals

Ethanol is a better solvent than water for most aromatic compounds, which is why spirit infusions run on a timescale of minutes to days rather than the weeks a water infusion would need. Higher proof extracts faster and extracts more of the nonpolar fraction — including the harsh, resinous, and bitter compounds you did not want.

| Material | Typical load per 750 mL | Bracket | Endpoint cue |
|---|---|---|---|
| Habanero / scotch bonnet | 1 pepper, halved | 5–20 min | Taste **every 3 minutes**. Heat is irreversible. |
| Jalapeño / serrano | 2–3, sliced | 30–90 min | Vegetal green note arrives before the heat peaks |
| Black or green tea | 8–12 g | 5–30 min | Pull at aromatic, before astringency |
| Hibiscus, lavender, chamomile | 10–15 g | 15–60 min | Floral turns soapy/perfumed if held |
| Cucumber, melon | 300 g, sliced | 2–6 h | Fresh note fades after ~8 h |
| Citrus zest | peel of 4 fruit | 4–24 h | Bitter once pith-adjacent compounds arrive |
| Coffee beans | 60–80 g, cracked | 8–24 h, cold | Roasty; goes ashy past ~36 h |
| Vanilla pod | 2, split | 1–2 weeks | Slow, forgiving, hard to overshoot |
| Cinnamon, whole spice | 3–5 sticks | 2–5 days | Clove and cassia over-extract; check daily |
| Dried fruit | 150 g | 3–7 days | Sweetness and color arrive together |
| Oak (chips, cubes, spiral) | 5–15 g | 3 days – 6 weeks | Taste weekly. Tannin/plank flavor is the overshoot |

**The operating rule**: taste for the endpoint, never trust the clock. Set a timer to remind you to taste, not to tell you when you are done. Two habaneros from the same box can differ threefold in capsaicin. Strain the moment the infusion is where you want it — leaving the solids in "just while I find a bottle" has ruined more infusions than any other error.

**Practical notes.** Infuse in glass, not plastic (chile oils and terpenes both leach into and out of plastic). Keep infusions out of light — many botanical colors, especially hibiscus and butterfly pea, are photolabile. Fine-strain through a coffee filter for anything that will be carbonated (§7.12). An infused spirit keeps essentially as long as the base spirit did if it contains no sugar, fruit pulp, or dairy; add any of those and it becomes a refrigerated prep with a weeks-long life.

### 7.9 Fat-Washing

**Mechanism.** Fat carries a large set of aroma compounds that water does not — the lipophilic fraction: the pyrazines and phenols of smoked bacon, the lactones and furans of browned butter, the terpenes of toasted sesame. Put melted fat in contact with a spirit and those compounds partition out of the lipid phase into the ethanol-water phase, which is a far better solvent for them than water alone. Then you chill until the fat solidifies and remove it mechanically, leaving the aroma behind and the grease gone. Ethanol content matters: higher-proof spirits pull more, and a 40% ABV vodka will extract noticeably less than a 50% ABV rye from the same fat. The technique is documented in *Liquid Intelligence*, and the modern bar practice traces to Don Lee's bacon-washed bourbon for the Benton's Old Fashioned at PDT.

**Ratios.**

| Fat | Per 750 mL spirit | Contact | Notes |
|---|---|---|---|
| Rendered bacon fat | 30–45 mL | 3–4 h | The canonical version; overdose reads as salty and cured |
| Brown butter | 60–90 mL | 3–4 h | More fat needed; the flavor is subtler |
| Toasted sesame oil | 10–15 mL | 2 h | Extremely potent; start low |
| Coconut oil | 60–90 mL | 3–4 h | Solidifies at ~24 °C, so it strains out easily |
| Duck fat, beef tallow | 30–60 mL | 3–4 h | Rich, savory, best with aged spirits |
| Olive oil | 45–60 mL | 4–6 h | Does **not** solidify in a domestic freezer — you must centrifuge, or accept a partial separation |

**Procedure.** Melt the fat, combine with the spirit in a sealed jar, shake, and hold at room temperature 2–4 hours, agitating every 30 minutes. Move to the freezer for 8–12 hours (overnight) at −18 °C. The fat sets as a cap or a raft. Break through it, decant, and strain the spirit through a coffee filter or a fine chinois lined with cheesecloth. Filter cold — every step, including the funnel and the receiving bottle, should be cold.

**Yield.** Expect to lose 5–10% of volume to the fat cap and the filter.

**Shelf life.** 1–2 months refrigerated. Residual lipid at the parts-per-thousand level will eventually oxidize and go rancid; refrigeration is not optional and room-temperature back-bar storage of a fat-washed bottle is a mistake.

**Failure modes.** *Filtering warm*: any fat still liquid passes straight through and produces a spirit that is cloudy, greasy on the lip, and short-lived. Re-freeze and re-filter. *Overdosing*: too much fat mutes the spirit's own aromatics and, in a shaken drink, kills the foam — lipids are surfactant-displacing and will flatten an egg-white head completely. *Using a fat you would not eat off a spoon*: the washing concentrates the character of the fat, including its flaws.

### 7.10 Milk Clarification and Milk Punch

**Mechanism.** Casein micelles in milk are stable at milk's native pH (~6.7) and destabilize as pH approaches casein's isoelectric point (~4.6). Adding an acidic liquid — citrus juice, or a punch containing it — drops the pH through that point and the casein flocculates into a curd. That curd is not just a byproduct: as it forms, it entraps suspended particulates and binds polyphenols and tannins, which is why a milk-clarified punch is not only optically clear but noticeably softer and rounder than the same punch unclarified. The curd bed then acts as the filter medium. The technique is 18th-century English — Wondrich's *Punch* covers the history, and Benjamin Franklin's 1763 letter transcribing a milk punch recipe is the frequently-cited primary document.

**Procedure (for 1 L of punch).**
1. Build the full punch — spirit, sugar, citrus, tea, spice — and make sure it contains enough acid to carry the milk past pH 4.6. Roughly 60–90 mL of citrus juice per litre is a safe floor.
2. Warm 250 mL of whole milk to about 50–60 °C. Whole milk, not skim: fat improves the texture of the finished punch.
3. **Pour the punch into the milk**, slowly, not the other way around. Adding milk to a large volume of acid produces a fine, dispersed curd that will not filter; adding acid gradually to the milk produces a coarse, cohesive curd that will.
4. Rest 1 hour minimum, refrigerated overnight for best results. The curd will consolidate and drop.
5. Strain through a fine mesh, then through a coffee filter, a Superbag, or a jelly bag. **Return the first cloudy runnings to the filter** — the curd bed is the filter, and it needs to build.

**Yield and shelf life.** Expect 10–15% volume loss to the curd. The finished punch is remarkably stable: low pH, meaningful ABV, and with the proteins and most oxidizable particulates removed. Refrigerated and bottled, 2–3 months is realistic; some batches improve over the first few weeks.

**Modern routes, honestly labeled by difficulty.**

| Method | Equipment | Difficulty | Clarity | Flavor effect |
|---|---|---|---|---|
| Milk clarification | A pot and a filter | Easy — do this one | Very good | Softens tannin and acid; adds a faint lactic roundness |
| Gelatin freeze-thaw | Gelatin, a freezer | Easy but slow (2–3 days) | Very good | Nearly flavor-neutral; a large freezer commitment |
| Agar clarification | Agar-agar, scale, thermometer | Intermediate | Excellent | Flavor-neutral. Hydrate agar at 0.2–0.25% of final weight by boiling it in a small portion of water, whisk into the cold liquid, let it set, then either break the gel and drain it through a strainer or freeze-thaw the gel and collect the drip. Arnold's *Liquid Intelligence* is the working reference. |
| Enzyme + centrifuge | Centrifuge at ~4,000 g, pectinase | Hard — requires equipment most bars do not have | Best available | Treat pectin-rich juices with pectinase 15–30 min first, then spin 12–15 min and decant off the pellet |

**Failure modes.** Not enough acid (no curd forms, and you have made a milky punch); adding milk to punch instead of punch to milk (unfilterable haze); squeezing or stirring the filter bed (pushes fines through and you start over); and impatience — a clarification you rush will look like weak tea, and there is no way to un-cloud it except to run it again through fresh milk.

### 7.11 Batching: Removing the Dilution Step Without Removing the Dilution

Batching is not scaling a recipe. When you pre-batch, you delete the ice-contact step, and with it you delete the water that step was contributing. **A batch that omits the dilution water is not a cocktail; it is a cocktail's concentrate, and it will taste hot, sharp, and closed.** This is the single most common batching error.

**Establish your dilution empirically.** Published ranges: stirred spirit-forward drinks typically finish at roughly **20–25% dilution** by volume of the pre-dilution ingredients; hard-shaken drinks run higher, roughly **25–30%**, because the ice is fracturing and the surface area is much greater. *Liquid Intelligence* is the source that put real measurement behind these numbers, and Arnold's point is that you should not adopt a figure from a book — you should measure your own. The method takes two minutes: build the drink to spec, stir or shake it exactly as you normally would, strain it into a graduated cylinder, and subtract the summed volume of the ingredients. The difference, divided by that summed volume, is your dilution percentage. It is a property of your ice, your technique, and your glassware, and it is stable once you know it.

**Worked example — a batched equal-parts stirred drink, 20 servings.**

Spec by role: 30 mL base (47% ABV) : 30 mL bitter aperitivo (24%) : 30 mL sweet vermouth (16%). Undiluted volume 90 mL. Target dilution 25%.

| Component | Per serving | ×20 | Ethanol contributed (×20) |
|---|---|---|---|
| Base, 47% | 30 mL | 600 mL | 282 mL |
| Bitter aperitivo, 24% | 30 mL | 600 mL | 144 mL |
| Sweet vermouth, 16% | 30 mL | 600 mL | 96 mL |
| **Water (25% of 90 mL)** | **22.5 mL** | **450 mL** | 0 |
| Total | 112.5 mL | 2250 mL | 522 mL |

Finished ABV = 522 / 2250 = **23.2%**. Undiluted, the same batch would be 522 / 1800 = 29.0% — a difference you can taste immediately.

**Worked example — a batched 2:1 stirred drink, freezer service.** 60 mL base (50%) : 30 mL sweet vermouth (16%) : 2 dashes bitters. Ethanol = 30 + 4.8 = 34.8 mL in 90 mL, or 38.7% ABV undiluted. Add 25% dilution (22.5 mL water) → 112.5 mL at **30.9% ABV**.

**Why that number matters for storage.** Use the freezing-point table in §5 (Overview): ~20% ABV freezes near −9 °C, ~25% near −12 °C, ~30% near −15 °C, ~35% near −19 °C, ~40% near −23 °C. A domestic freezer runs at about −18 °C, though many run nearer −15 °C. So:

- The 30.9% batch is **thick and just pourable** at −18 °C and fully liquid in a freezer running at −15 °C. Poured straight into a chilled glass with no ice contact, that viscosity is a feature, not a fault — but check your own freezer before promising it.
- The 23.2% batch **will freeze** at −18 °C. Refrigerate it instead (2–4 °C) and pour over a large cube, accepting a small amount of additional dilution.
- Alternatively, batch **without** the water, freeze the concentrate (29% and 38.7% respectively — the second holds fully liquid, the first goes viscous), and add measured chilled water at service. This gains you shelf life and freezer compatibility at the cost of one extra motion per drink, and it is the only route that gets a sub-30% drink into freezer service at all.

**Storage and shelf life of batches.**

| Batch composition | Storage | Practical life |
|---|---|---|
| Spirits + bitters only, diluted | Refrigerated or frozen, sealed | 3–6 months |
| Contains vermouth, sherry, or any aromatized wine | Refrigerated, in a full bottle with minimal headspace | 1–2 weeks before the wine flattens and oxidizes |
| Contains liqueurs and amari, no wine | Refrigerated | 1–3 months |
| Contains citrus juice | Refrigerated | Same service, and **lime specifically degrades within 4–8 hours** |
| Contains dairy or egg | Do not batch | — |

Bottle in glass, fill to minimize headspace (oxygen is what kills a vermouth batch), label with the spec, the dilution percentage, the ABV, and the date. Small bottles beat one large bottle: every pour from a large bottle exchanges the headspace.

**Failure modes beyond forgetting the water.** *Batching a shaken sour and pouring it flat*: shaking contributes aeration and texture, not just cold and water. A batched sour still needs a short shake with a cube or two, or it needs carbonation (§7.12), or it will read as thin. *Batching bitters by dash count at scale*: dashes vary enormously between bottles; convert to millilitres once and batch by volume (a typical dash is 0.6–1.0 mL — measure your own bottle by counting 20 dashes into a graduate). *Scaling a spec with a rounding error*: at 20 servings a 2 mL error per drink is 40 mL of misplaced ingredient.

### 7.12 Carbonation at Home

Carbonated cocktails are a distinct format, not a cocktail with soda poured on top: the entire drink is carbonated at final strength, so it arrives at full effervescence rather than diluting into flatness. *Liquid Intelligence* is the reference and the source of the working parameters below.

**The four conditions.** All four must hold or the drink will foam over and go flat.

1. **Cold.** CO₂ solubility roughly doubles between 20 °C and 0 °C (§6.9 has the numbers). Chill the liquid to 0–4 °C before carbonating and keep it there. Warm liquid cannot hold gas.
2. **Clear.** Any suspended particulate is a nucleation site and will drive violent bubble formation the moment pressure releases. Carbonated drinks must be filtered or clarified (§7.10) — this is the main reason clarification and carbonation appear together in modern bars.
3. **Diluted first.** There is no ice in the glass, so the drink must contain its full dilution water before carbonation. Ethanol lowers CO₂ solubility and increases foaming, so finished carbonated cocktails generally land well below spirit strength — the low-teens to around 20% ABV is the workable band, and the water doing that job is the same water a stirred version would have taken from ice.
4. **No air in the headspace.** Nitrogen and oxygen in the headspace do not dissolve and instead sit as a compressible cushion that drives foaming on release. Fill, pressurize, vent, and repeat three or four times to purge the headspace to near-pure CO₂ before the final charge.

**Working parameters.** Carbonate at roughly 40 psi (about 2.75 bar) for cocktails. Agitate under pressure — shake the bottle for 20–30 seconds — to force gas into solution rapidly, then re-pressurize and rest cold for at least an hour, overnight if you can. Open slowly, over a sink, and pour into a chilled glass. **Never pour a carbonated cocktail over ice**; the ice is a field of nucleation sites and the drink will foam out of the glass and be flat within seconds.

**Equipment and safety.** Use a purpose-built carbonation rig or a carbonation cap on a PET bottle rated for pressure. **Do not pressurize glass bottles that were not designed for it.** A regulator, a check valve, and a bottle rated for the pressure you are applying are not optional; this is the only prep in this section with a physical hazard attached to getting it wrong.

**Shelf life.** Sealed and cold, a carbonated batch holds carbonation for weeks; each opening costs you gas. Bottle in single-serve or two-serve volumes rather than one large bottle.

### 7.13 The Prep Board: Priority Order for Building a Bar

If a drink design in the SYNTHESIZE phase calls for more prep than the user has time for, cut in this order — the top of the list buys the most character per hour invested.

| Rank | Prep | Active time | Elapsed time | What it unlocks |
|---|---|---|---|---|
| 1 | Rich demerara syrup | 5 min | 5 min | Every Old Fashioned, tiki, and rum drink |
| 2 | Oleo-saccharum | 10 min | overnight | Punches, and any drink wanting citrus aroma without citrus acid |
| 3 | Honey or ginger syrup | 10 min | 1 h | Bee's Knees, Penicillin, Moscow Mule family |
| 4 | Chile or tea infusion | 5 min | 20 min – 4 h | A whole modern-riff category from one bottle |
| 5 | Batched stirred drink | 20 min | 1 h chill | Service for a group with no station work |
| 6 | Shrub | 15 min | 3 days – 4 weeks | Non-citrus acidity; the best low/no-ABV tool |
| 7 | Fat-wash | 15 min | overnight | Savory register unavailable any other way |
| 8 | Milk-clarified punch | 45 min | overnight | Clarity, softness, and a 2-month keeper |
| 9 | Orgeat ⚠ nut | 45 min | overnight | Mai Tai, Japanese Cocktail, most tiki |
| 10 | Carbonated bottling | 30 min | overnight + rig | Format nothing else replicates |

---

## Section 8: Glassware, Garnish, and Service {#glassware-garnish-service}

The last three minutes of a drink's life determine a surprising fraction of how it is perceived. Retronasal olfaction accounts for the large majority of what a drinker calls "taste," and the vessel and the garnish are the two variables that control what reaches the nose. Neither is decoration.

### 8.1 Glassware by Family, and Why Shape Does Work

Three physical properties do all the explaining: **surface-to-volume ratio** (governs both warming rate and the rate at which volatiles escape), **mouth aperture relative to bowl width** (governs whether aroma concentrates at the nose or dissipates), and **whether the hand touches the liquid-bearing part of the glass** (governs conductive warming).

| Glass | Capacity | Serves | Why the shape |
|---|---|---|---|
| Nick & Nora | 150–180 mL | Stirred, spirit-forward, up | Bowl tapers inward at the lip, so volatiles concentrate in the headspace and arrive at the nose with the sip. High capacity-to-spill ratio. The best general-purpose up glass. |
| Coupe | 150–210 mL | Shaken sours, up; sparkling | Wide, shallow bowl presents a large surface — aroma reads immediately and then fades, and the drink warms faster than in a Nick & Nora. Excellent for egg-white foam, which wants surface area. |
| Martini / V-glass | 180–300 mL | Martini, classic-era up drinks | Maximum surface area and a fully open mouth: fastest aroma release, fastest warming, highest spill risk. A period and theatre choice more than a functional one. |
| Rocks / Old Fashioned | 180–240 mL | Built or stirred over one large cube | Squat and heavy; the large-format ice inside has a low surface-to-volume ratio and therefore dilutes slowly, which is the whole point. |
| Double rocks | 350–400 mL | Crushed-ice drinks, doubles | Volume for crushed ice plus a garnish canopy. |
| Collins / highball | 300–400 mL | Carbonated long drinks | The narrow tall column minimizes the gas-liquid interface area, which is what preserves carbonation. Fill it completely with ice: more ice keeps the total mass colder and therefore melts *less*, not more. |
| Flute | 170–200 mL | Sparkling wine cocktails | Same carbonation logic, taken further. |
| Julep tin | 350 mL | Julep, smash, anything on crushed ice | Metal conducts, so the exterior frosts and the hand reads the temperature directly. Hold it by the rim or the base. |
| Copper mule mug | 350–470 mL | Mule family | Same conduction argument. **Use lined mugs only** — unlined copper in contact with an acidic drink can leach copper, and food codes generally prohibit copper contact with foods below about pH 6. |
| Tiki mug | 350–500 mL | Crushed-ice tropical drinks | Thick ceramic insulates, which matters because crushed ice has enormous surface area and would otherwise dilute a drink to nothing. |
| Fizz / Delmonico | 240 mL | Ramos and fizz family | Narrow, straight-sided, no ice, so the foam column can stand above the rim. |
| Punch cup | 120–180 mL | Punch service | Small on purpose: punch is served in many small pours from a cold bowl, not one large warming one. |
| Copita / small wine | 150–200 mL | Sherry, low-ABV aperitivo, neat agave | Tulip bowl with an inward taper — nosing geometry at cocktail scale. |
| Snifter / Glencairn | 180–300 mL | Neat spirits | Concentrates volatiles hard. Note the trade-off: it concentrates *ethanol* vapor too, which is why a cask-strength spirit noses hot in a snifter and softer in a wider glass. |

**The chilled glass is the largest single variable you control.** A room-temperature glass at 22 °C absorbs enough heat from a 150 mL up-drink to raise it several degrees on contact — which is the difference between a Martini that is bracing and one that is merely cold. Freeze glassware for at least 20 minutes, or pack it with ice and water while you build and dump it immediately before straining. A chilled glass also slows the aroma release rate, which is why a very cold Martini opens up as it sits.

**Ice format is part of glassware selection**, not a separate decision: one large cube in a rocks glass (slow dilution, long drink life), full column of cubes in a highball (fast chill, slow melt, carbonation preserved), crushed in a julep tin or tiki mug (immediate chill and aggressive dilution, which is why crushed-ice drinks are built strong and sweet).

### 8.2 Garnish as an Aromatic Ingredient

**Expressed citrus oil.** This is the highest-impact garnish move in the repertoire and the most commonly performed without understanding. The colored outer layer of the peel — the flavedo — holds essential oil in discrete sacs. Squeezing the peel skin-side-down over the drink ruptures those sacs and ejects a fine aerosol of oil that lands on the surface and spreads as a monomolecular film. Every subsequent sip pulls the drinker's nose through that film.

What matters mechanically:
- **It is the oil, not the juice.** Peel oil and juice from the same fruit are chemically unrelated products. Lemon oil is limonene-dominant with citral and linalool; lemon juice is citric acid and water with a fraction of the aroma. Expressing a peel adds essentially no acid and no sugar to the drink — it is a pure aroma addition, which is why it can be applied to a Martini or a Manhattan without altering balance.
- **The compounds are extraordinarily potent.** Grapefruit peel carries 1-p-menthene-8-thiol, detectable at parts per trillion, plus nootkatone; this is why a grapefruit twist transforms a drink that a slice of grapefruit would only dilute.
- **Technique**: peel-side down, 5–10 cm above the surface, squeeze firmly and once. Then decide whether to wipe the rim (adds oil to the point of lip contact, a real effect) and whether to drop the peel in. Dropping it in continues to leach — pleasant for the first ten minutes, and increasingly bitter after that if any pith came with it.
- **Match the fruit to the spirit**: lemon to gin and light spirits, orange to whiskey and amaro-forward drinks, grapefruit to blanco tequila and modern gin drinks, lime to rum and agave.

**The flamed peel.** Igniting the expressed spray (the move associated with Pepe Ruiz's Flame of Love at Chasen's) pyrolyzes a fraction of the oil and produces caramelized, singed-citrus notes. Be honest about what it does and does not do: it **does** add a genuine toasted-oil aroma and a visual event, and it **does not** deliver more citrus oil to the drink — combustion destroys some of the delicate volatile top notes it passes through. Use it where the drink is dark, rich, and can carry a burnt note. On a delicate gin drink it replaces the aroma you wanted with a different one.

**Mint.** Slap the sprig once between the palms. Bruising ruptures the surface glands and releases menthol and menthone; it does not tear the leaf. Tearing and hard muddling release chlorophyll and bitter phenolics and turn the drink grassy — this is the single most common mint error, and it is the reason a properly made julep never has shredded mint in it. Place the sprig directly against the straw or the side of the glass where the drinker's nose will be. A mint sprig on the far side of a highball is doing nothing.

**Load-bearing vs cargo-cult garnish.** The test is simple: **remove it and see whether a blind taster notices.** If nothing changes, it was decoration and it is costing you prep time and cost of goods.

| Garnish | Load-bearing when | Cargo cult when |
|---|---|---|
| Citrus twist | Expressed over the drink | Dropped in unexpressed |
| Citrus wheel / slice | Perched at the rim where it is squeezed or smelled | Floating flat on the surface, untouched |
| Mint sprig | Slapped and positioned at the nose | Standing on the opposite side of a tall glass |
| Freshly grated nutmeg | Grated to order over foam or a flip | Pre-ground, shaken from a tin |
| Brandied cherry | Quality fruit, eaten at the end, in a spirit-forward drink | Neon maraschino at the bottom of a highball nobody reaches |
| Olive / onion / pickle | Specified as an ingredient — brine adds sodium and acid | Added without accounting for the brine it drags in |
| Bitters float / spritz | Applied on the surface, entering the nose first | Stirred in, where it merges and disappears |
| Absinthe rinse | Coats the glass; aroma leads the sip | Poured into the body of the drink |
| Dehydrated wheel, edible flower, skewer | It smells of something at the nose | Purely visual, and it is fine to say so — just do not claim it is flavor |

**Salt, inside the drink.** A few grains of salt, or 3–5 drops of a 20% w/v saline solution, suppresses bitterness and raises perceived sweetness and aromatic intensity — the same mechanism described in Pillar 3 for food. It is one of the most reliable fixes for a drink that tastes technically correct but muted, and it is invisible to the drinker.

### 8.3 Rim Treatments

| Rim | Standard application | Notes |
|---|---|---|
| Salt (Margarita, Salty Dog) | Coarse or flaked salt, **outside edge only** | Rimming the inside dumps uncontrolled salt into the drink and destroys the balance you measured. Wet only the outer edge with a citrus wedge, then roll. |
| Half-rim | Salt one hemisphere | Lets the drinker choose per sip. This should be the default courtesy, not a special request. |
| Sugar (Sidecar, Crusta, Lemon Drop) | Fine caster sugar, outer edge | Fine crystal dissolves on the lip and reads as immediate sweetness; coarse sanding sugar persists through the drink. |
| Tajín / chile-lime salt | Outer edge | Pairs with agave and with anything containing grapefruit. |
| Celery salt (Bloody Mary) | Outer edge | Functions as seasoning, not decoration. |
| Smoked or spiced salt | Outer edge, half-rim | Potent; use a coarser grind so less lands per lick. |

Crystal size is the controllable variable most people ignore: fine salt dissolves instantly and delivers a salt slug on the first sip, while flaked or coarse salt meters itself out across the whole drink. Match the grind to how long the drink will take to consume.

### 8.4 Service Order at the Station

The sequence exists because each step has a decay clock attached to it.

1. **Chill the glass first**, before touching a bottle. It is the step with the longest lead time and zero active attention.
2. **Prepare the garnish next**, while the glass chills. A finished drink standing on the rail waiting for someone to cut a twist is a drink losing its temperature.
3. **Jigger every ingredient.** Free-pouring introduces error at the exact place — the modifier and the sweetener — where the drink is least tolerant of it. The modern American insistence on measured pours and fresh juice is generally traced to Audrey Saunders's Pegu Club and the bars that came out of it.
4. **Add ice last**, immediately before shaking or stirring, and take it from a fresh scoop rather than a wet well. Wet ice has already begun melting and will over-dilute.
5. **Shake or stir to your measured target** (§7.11), not to a fixed count. Frost on the outside of the tin is the traditional cue and it is a real temperature signal — the metal has dropped below the dew point of the room air — but it is a lagging one, it reads the tin rather than the liquid, and it says nothing about dilution. Harry Craddock's instruction in *The Savoy Cocktail Book* (1930) is about vigor rather than endpoint: shake hard, do not merely rock the tin. That is good instruction and not a measurement. Measure the endpoint once with a thermometer and a scale, in your own bar, and calibrate the count against it.
6. **Double-strain** (Hawthorne plus fine mesh) any shaken drink containing fruit, herbs, ice shards, or egg. Single-strain stirred drinks.
7. **Express and place the garnish over the finished drink**, not before.
8. **Serve immediately.** An up-served drink has a working life of roughly 10–15 minutes before warming and residual dilution flatten it; a drink on a large cube holds for 25–40 minutes.

**Order within a round.** Build the most durable drink first and the most perishable last: stirred-on-rocks → stirred-up → shaken sour → egg or dairy → carbonated. Carbonated drinks are poured last and never over ice. If one drink in the round contains egg white, it is built last regardless, because its foam begins collapsing the moment it is strained.

**Order across a menu.** Palate fatigue is real and monotonic: sequence low-ABV and aperitivo-bitter drinks early, spirit-forward and sweet drinks later, and put water on the table alongside. A second Negroni tastes measurably less bitter than the first, which is a fact about the drinker, not the drink.

**Failure modes.** Building into a warm glass; garnishing before straining; ice from a slushy well; holding a strained up-drink while you talk; and pouring a carbonated cocktail over ice, which converts a week of preparation into flat liquid in about four seconds.

### 8.5 Quick Reference: Glass and Garnish by Drink Family

| Family | Glass | Ice | Default garnish | Load-bearing? |
|---|---|---|---|---|
| Old Fashioned | Rocks | One large cube | Expressed orange peel | Yes — the oil is a stated ingredient of the drink |
| Martini | Nick & Nora or coupe | None (up) | Expressed lemon peel, or olive | Yes — and the choice changes the drink's category |
| Manhattan | Nick & Nora or coupe | None (up) | Brandied cherry, or expressed orange | Cherry: partly; orange: yes |
| Daiquiri / gin sour | Coupe | None (up) | Lime wheel, or none | Often cargo cult — the drink is complete without it |
| Whiskey sour (egg) | Coupe or rocks | None, or one cube | Angostura on the foam | Yes — the aroma leads every sip |
| Negroni / spirit-forward bitter | Rocks | One large cube | Expressed orange peel | Yes |
| Highball / Collins | Collins | Filled with cubes | Lemon wedge or expressed peel | Yes if expressed; decoration if dropped |
| Mule | Lined copper mug | Cubes | Mint sprig at the nose, lime | Yes for the mint if positioned |
| Julep / smash | Julep tin | Crushed, mounded | Large mint bouquet at the nose | Yes — it is the primary aroma |
| Tiki / tropical | Tiki mug or hurricane | Crushed | Mint, citrus shell, spent lime hull | Mint yes; the rest is theatre, honestly |
| Ramos / fizz | Fizz glass | None in glass | Nothing, or a drop of orange flower water | Yes |
| Milk punch (clarified) | Coupe or small wine | None, or one cube | Grated nutmeg | Yes — nutmeg is part of the historical form |
| Carbonated bottled cocktail | Chilled coupe or flute | **None, ever** | Expressed peel | Yes |
| Aperitivo / low-ABV | Copita or wine glass | Cube or none | Olive, peel, or nothing | Situational |

---

## References & Sources

**Primary modern bar literature**

- Arnold, D. (2014). *Liquid Intelligence: The Art and Science of the Perfect Cocktail*. W. W. Norton. [Chilling and dilution as one variable; ice and directional freezing; acid adjustment and cordials; fat-washing; clarification; carbonation and bottling. The primary source behind Sections 5 and 7.]
- Day, A., Fauchald, N., & Kaplan, D. (2018). *Cocktail Codex: Fundamentals, Formulas, Evolutions*. Ten Speed Press. [The six-root template argument — Old Fashioned, Martini, Daiquiri, Sidecar, Whisky Highball, Flip — that organizes Section 1 and carries the build method with each root into Section 6.]
- Kaplan, D., Fauchald, N., & Day, A. (2014). *Death & Co: Modern Classic Cocktails*. Ten Speed Press. [House specs, ratios, split-base practice, and the ~30 second stir default.]
- Day, A., Fauchald, N., & Kaplan, D. (2021). *Death & Co: Welcome Home*. Ten Speed Press. [Batching practice and home-scale service.]
- Morgenthaler, J. (2014). *The Bar Book: Elements of Cocktail Technique*. Chronicle Books. [Weigh rather than measure; 2:1 rich syrup as the house default; juice handling; orgeat; the argument that the bartender's leverage sits upstream of the shaker. The primary source behind Section 7.]
- Meehan, J. (2011). *The PDT Cocktail Book*. Sterling Epicure. [Station discipline and specs.]
- Berry, J. ("Beachbum"). (2007). *Sippin' Safari*. SLG Publishing; (2013). *Potions of the Caribbean*. Cocktail Kingdom. [Recovered tiki formulas, split-base construction, and whip-shake service over crushed ice.]
- Difford, S. *Difford's Guide for Discerning Drinkers* (diffordsguide.com). [Ongoing reference for historical and contemporary specs; used for cross-checking ratios rather than as a mechanism source.]

**Historical sources**

- Thomas, J. (1862). *How to Mix Drinks; or, The Bon-Vivant's Companion*. Dick & Fitzgerald. [The first published American drink book; the source of the gum-syrup and improved-cocktail vocabulary.]
- Craddock, H. (1930). *The Savoy Cocktail Book*. Constable & Co. [Canonical interwar specs; the "Hints for the Young Mixer" instruction on shaking is about vigor — shake hard rather than rock the tin — and not an endpoint measurement. Consulted for specs and for the equal-parts Dry Martini in §1.3, not for technique targets.]
- Embury, D. A. (1948). *The Fine Art of Mixing Drinks*. Doubleday. [The first systematic ratio argument in English; the base/modifier/special-flavoring decomposition that the functional-role model in Section 3 descends from.]
- Wondrich, D. (2007). *Imbibe!*. Perigee. [Nineteenth-century technique and the Jerry Thomas canon.]
- Wondrich, D. (2010). *Punch: The Delights (and Dangers) of the Flowing Bowl*. Perigee. [The standard modern account of oleo-saccharum and of punch as a designed-dilution form; the source behind §7.3 and the punch template in §1.8.]
- Wondrich, D., & Rothbaum, N. (Eds.). (2021). *The Oxford Companion to Spirits and Cocktails*. Oxford University Press. [Category definitions, production methods, and provenance.]

**Practitioner attributions**

- Bergeron, V. ("Trader Vic"). Mai Tai, 1944. [The orgeat-and-split-base construction in §1.5.]
- Saunders, A. Pegu Club, New York. [The Gin-Gin Mule; the 1:1 Regans' No. 6 / Fee Brothers West Indian orange bitters house blend; the measured-pour and fresh-juice discipline in §8.4.]
- Petraske, S., with Moger-Petraske, G. (2016). *Regarding Cocktails*. Phaidon. [Milk & Honey house ratios and the minimal-service argument.]
- González, G. Trinidad Sour. [Angostura bitters at 1.5 oz in the base slot — the demonstration that the dash is a dosage convention, not a property of the ingredient.]
- Morris, N. Expo Bar, Louisville. ["Super juice" — peel oleo extraction plus citric and malic acid, applied to yield rather than to flavor (§3.7).]
- English, C. *Alcademics* (alcademics.com). [Directional freezing and the insulated-cooler clear ice method (§5.2).]

**Physical and regulatory data**

- CRC Handbook of Chemistry and Physics. [Latent heat of fusion of water, specific heats of water, ice and ethanol, ethanol density, freezing-point depression of ethanol-water mixtures — the constants tabulated in Section 5.]
- National Institute on Alcohol Abuse and Alcoholism (NIAAA). "What Is A Standard Drink?" [US standard drink = 0.6 fl oz / 14 g pure ethanol (§5.5). UK, Australian, New Zealand and Canadian figures from their respective national health guidance.]
- US Department of Agriculture grading standards for maple syrup. [Grade A minimum soluble solids (§3.6).]

**A note on numbers.** Every figure in this document is one of three kinds: an arithmetic identity (ABV_final = ethanol volume ÷ post-dilution volume; dilution stated as water added over pre-dilution volume), a definitional ratio (1:1 syrup by weight is 50% sucrose w/w, 2:1 is ~67%), or a published physical constant. Dilution percentages by build method are stated as **ranges from bar practice**, because they are not constants — they move with ice temperature, ice wetness, ice size, agitation and vessel. Where a mechanism is well established but a specific number is not defensible, the mechanism is stated without a number and without an attribution.

---

**Document Metadata**
- **Length**: ~28,400 words
- **Sections**: 8 main sections (Drink Families & Templates, Base Spirits, Modifiers & Sweeteners & Bitters, Balance & Rescue, Dilution & Temperature & ABV Math, Build Methods, Bar Prep Projects, Glassware & Garnish & Service)
- **Scope**: Cocktails and bar prep. Fermentation, brewing, winemaking and distillation are deliberately out of scope.
- **Depth**: Encyclopedic, with structural templates, spirit taxonomies, worked ABV and dilution arithmetic, a symptom-driven rescue table, thirteen bar prep formulas with shelf lives and failure modes, and explicit allergen screening lists for nuts, dairy, egg, gluten, sulfites and the savory paths
- **Intended Use**: Foundation for AI skill training (the `beverage-craft` skill), professional bar reference, educational material
