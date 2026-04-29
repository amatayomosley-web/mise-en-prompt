---
name: culinary-technique
description: Use when selecting a cooking method for a protein or cut, diagnosing a broken or under-developed sauce, calculating reduction targets, choosing temperature and time for braising / searing / sous-vide / pressure-cooking, or explaining what heat and time do chemically (Maillard, caramelization, collagen breakdown, emulsion formation).
---

# Culinary Technique

Reasoning about transformations: what heat, time, and pressure do to ingredients.

## When the chef agent calls this skill

Invoked in the GROUNDING, SYNTHESIZE, and GUIDE phases. Match the question to one of the procedures below.

### "What technique should I use for this protein or cut?"
1. Open `reference.md` → **Section 2: State Changes & Structural Breakdown**
2. Identify the cut by collagen content + fat content
3. Return: braise vs. pressure-cook vs. sous-vide vs. dry-heat with target temps and times
   - Collagen-rich, tough → braise (70–80°C / 160–180°F, 3–6 hr) or pressure (115–120°C / 240–250°F, ~3× faster)
   - Lean, tender → dry-heat (sear, roast) or precise sous-vide
   - High fat, intermediate → sous-vide for control + finishing sear

### "How do I get the right browning?"
1. Open `reference.md` → **Section 1: Maillard Reaction & Caramelization**
2. Identify the desired flavor outcome (sweet caramel, savory crust, bitter complex char)
3. Return: target temperature + time + visual cues + the chemistry
   - **Maillard** (140–165°C / 285–330°F): amino acid + reducing sugar → pyrazines, thiazoles, melanoidins
   - **Caramelization** (160–190°C / 320–375°F): pure sugar pyrolysis
   - **Strecker degradation** at higher temps: bitter, complex notes

### "My sauce is broken / too thin / too thick"
1. Open `reference.md` → **Section 4: Troubleshooting & Decision Trees** FIRST
2. If emulsion-related, also consult **Section 3: Emulsification & Reduction**
3. Return: diagnosis + rescue procedure (yolk re-emulsion, lecithin add, water drizzle, additional reduction, starch slurry, butter mount)

### "What is this technique doing chemically?"
1. Open `reference.md` for the relevant section
2. Return: the mechanism in plain language + the temperature / time thresholds where the chemistry shifts (so the user knows what to watch for)

## Worked example
Pinto beans slow-simmered with pork shoulder:
- Pork shoulder = high collagen, high fat → braise at 70–80°C / 160–180°F for 3–4 hr so collagen → gelatin
- Beans cook in the same liquid → starch gelatinization + slow flavor diffusion from the pork's rendered fat and gelatin
- Final reduction concentrates glutamates and raises gelatin viscosity → glossy, body-rich pot liquor

## Reference

The full chemistry, temperatures, decision trees, and worked examples live in `reference.md`. **When you read a section, cite the H2 heading** so the user can verify and trace the source.
