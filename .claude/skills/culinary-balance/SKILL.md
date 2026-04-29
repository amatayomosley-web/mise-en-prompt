---
name: culinary-balance
description: Use when diagnosing an off-balance dish (too flat, too salty, too sweet, too sharp, lacks depth), planning flavor layering for depth, sequencing when to add aromatics / spices / salt / acid during cooking, scoring a dish against a regional cuisine's balance philosophy (Thai rot chart, Sichuan má-là, Indian masala, Mexican picante-fresco, Vietnamese nước chấm), or running a professional tasting protocol.
---

# Culinary Balance

Reasoning about balance: diagnosing off-balance dishes, layering depth, and timing aromatics so volatiles survive into the finished dish.

## When the chef agent calls this skill

Invoked in the GROUNDING, SYNTHESIZE, and GUIDE phases — and any time the user reports a taste problem. Match the question to one of the procedures below.

### "My dish tastes wrong"
**This is the flagship use.** Always start here when the user describes a taste problem.

1. Open `reference.md` → **The Master Rescue Table** (`#the-master-rescue-table`)
2. Identify the symptom: too flat / too salty / too sweet / too sour / too bitter / too sharp / lacks depth / muddled
3. Return: primary, secondary, and tertiary remedies in order — instruct the user to taste between each adjustment

### "When do I add this ingredient?"
1. Open `reference.md` → **Staggered Timing** (`#staggered-timing`) and **Aromatic Volatility Hierarchy** (`#aromatic-timing-volatility`)
2. Return: timing prescription with reasoning
   - Volatile aromatics (cilantro leaf, raw garlic, citrus zest) → late or finishing
   - Salt → early for diffusion, late for finishing pop
   - Acid → mostly late (preserves brightness; early acid toughens proteins, dulls greens)
   - Whole spices → early (need time to bloom); ground spices → mid-to-late (volatiles flash off)

### "Layer this ingredient for depth"
1. Open `reference.md` → **Layering the Same Ingredient in Different Forms** (`#layering-same-ingredient`)
2. For garlic / onion / tomato / citrus / chile / mushroom: return the multi-form layering plan (raw + sautéed + roasted + fried + powdered + fermented) — using the same ingredient in 2–4 forms compounds the flavor without distorting the dish

### "Does this dish hit the cuisine's balance philosophy?"
1. Open `reference.md` → **Global Flavor Balance Philosophies** (`#global-flavor-balance-philosophies`)
2. Find the cuisine
3. Score the dish against that cuisine's framework
   - Thai *rot* chart (sweet / salty / sour / spicy quadrants)
   - Sichuan *má-là* (numbing-spicy axis)
   - Mexican picante-fresco (heat / brightness)
   - Vietnamese nước chấm balance (fish-sauce / lime / sugar / chili)
   - Indian masala layering (whole spice base → aromatic build → finishing tadka)

### "Run the tasting protocol"
1. Open `reference.md` → **Professional Tasting Protocol** (`#tasting-protocol`)
2. Walk the user through the spoon-and-adjust loop with the five-question diagnostic

## Worked example
Pinto bean stew tastes flat:
1. Master Rescue Table → "lacks depth" row →
   - **Primary**: umami amplification — add cured pork, dried mushroom, or a glutamate source appropriate to Central American cuisine (Maggi, Worcestershire if cuisine-permissive)
   - **Secondary**: acid kicker — lime juice or curtido at finish to brighten and reveal existing flavors
   - **Tertiary**: roast a portion of the aromatics (chile, garlic, onion) for Maillard depth, then stir back in
2. Taste between each step. Most "flat" dishes are fixed by step 1 alone.

## Reference

The Master Rescue Table, layering frameworks, timing rules, and tasting protocol live in `reference.md`. **When you read a section, cite the H2 heading and the anchor** so the user can verify the recommendation against source.
