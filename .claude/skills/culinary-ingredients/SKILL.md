---
name: culinary-ingredients
description: Use when picking aromatic foundations for a target cuisine, finding traditional or molecular flavor pairings for an ingredient, identifying functional roles (acid / fat / salt / umami / heat / sweet) needed in a dish, or substituting ingredients across cuisines while preserving their functional role.
---

# Culinary Ingredients

Reasoning about ingredients: what they bring, what they pair with, and what role they fill in a dish.

## When the chef agent calls this skill

Invoked in the GROUNDING and RESEARCH phases. Match the question to one of the procedures below.

### "What aromatic base does this cuisine use?"
1. Open `reference.md` → **Section 1: Aromatic Foundations**
2. Identify the cuisine (and the closest regional variant if it's specified, e.g. Honduran vs. Salvadoran sofrito)
3. Return: ingredient ratios + build technique + the chemistry that makes it work (sulfur compounds in alliums, terpenes in carrots/celery, pyrazine development from gentle browning)

### "What pairs with X?"
1. Open `reference.md` → **Section 2: Flavor Affinities & Pairings**
2. Find the ingredient (or its functional category if it's not listed by name)
3. Return: traditional partners with the cuisines that use them + molecular pairing rationale (shared volatile aromatic compounds, foodpairing logic)

### "What functional roles need to be filled in this dish?"
1. Open `reference.md` → **Section 3: Functional Categories**
2. Six roles to consider for every dish: **acid, fat, salt, umami, heat, sweet**
3. For each, return candidates appropriate to the target cuisine, with intensity notes (chile Scoville, vinegar pH, glutamate concentration)

### "Substitute X while preserving its role"
1. Identify what X is doing in the source dish (consult Section 3 functional categories)
2. Find equivalents in the target cuisine that fill the same role
3. Return ranked options + the trade-off each substitution makes (e.g. parmesan → fish sauce: same umami, different texture and salt level)

## Worked example
Cuisine: Central American (Honduran). Star ingredient: pinto beans.
- **Aromatic base**: Latin sofrito (onion, garlic, sweet pepper) + regional epazote
- **Functional roles to fill**: heat (chile cobanero), acid (lime or curtido), fat (manteca or rendered pork fat), umami (cured pork, cooking-liquid concentration), salt (sea salt), aromatic herb (epazote, cilantro)

## Reference

The full lookup tables, chemistry, and worked examples live in `reference.md`. **When you read a section, cite the H2 heading** so the user (and downstream tooling) can trace the recommendation back to source.
