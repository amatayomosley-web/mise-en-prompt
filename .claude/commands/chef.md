---
description: Activate the chef agent in the active conversation. Walks the user through the 8-phase mise-en-place flow with AskUserQuestion firing role-by-role in CURATE, for a dish or for a drink. Designed for interactive cooking and cocktail design, not one-shot recipe generation.
---

# /chef

Activate the chef agent in the **active conversation** (not as a Task subagent).

## Why this command exists

The chef agent is a user-experience product, not a recipe-generation product. Its core
value is the interactive 8-phase walk: the user picks ingredients role-by-role in CURATE
via `AskUserQuestion`, opts into cross-cuisine vectors in CURATE Step 5, and sees the
deconstruction grow in `state.yaml` turn by turn.

Spawning the chef as a Task subagent (`subagent_type: chef`) breaks this:
- Subagents cannot fire `AskUserQuestion` to the human's keyboard
- Each subagent invocation is one-shot; no continuity across user turns
- The phase walk collapses into a single turn that produces a finished recipe
  without the user ever picking anything

This command activates the chef *as the active conversation*, where every user turn
advances exactly one phase or one CURATE step.

## What this command does

1. Reads `.claude/agents/chef.md` into the active context as operating instructions
2. Loads `AskUserQuestion` and `WebSearch` tool schemas (deferred-tool surface)
3. Enters Phase 1 — INTAKE — by asking the user what they want to make

The active session then runs the full 8 phases (INTAKE → CLARIFY → GROUNDING →
RESEARCH → CURATE → SYNTHESIZE → ENHANCE → GUIDE), persisting state to
`sessions/<session_id>/state.yaml` after each meaningful decision and writing the
final `recipe.md` only at GUIDE.

## Dishes and drinks

`/chef` covers both. INTAKE settles the medium and writes `intent.medium`
(`dish` | `drink`); everything downstream branches off that one field:

- **dish** — grounded by `culinary-ingredients`, `culinary-technique` and
  `culinary-balance`; CURATE walks the six functional roles; GUIDE writes the
  method-and-mise recipe
- **drink** — grounded by `beverage-craft` and `culinary-balance`; CURATE walks
  the eight drink roles (base, modifier, sweet, acid, bitter, aromatic, dilution,
  texture); GUIDE writes a spec table in oz and ml with the build, ice, glass,
  garnish, computed ABV, standard drinks, and dilution target

The phase walk is identical in both, and so is the interaction: `AskUserQuestion`
role-by-role in CURATE, vector opt-in in Step 5, soft-conflict overrides in the
active conversation.

There is deliberately **no `/bartender` command and no second agent.** Drinks are
structures inside the chef, not a parallel system — a second entry point would
fork the state schema, the phase ladder, and the conflict rules for no gain. Ask
`/chef` for a cocktail and it branches on its own; say "a drink" at INTAKE if it
guesses wrong.

## When subagents *are* useful inside this flow

The chef-as-active-conversation can still delegate bursts to Task subagents for
work that benefits from a fresh context window:

- **ENHANCE pass** — running both lenses (physics + flavor) over a long Method
  draft is a good subagent task; the result populates `state.enhancements` and
  the active chef renders it. For a drink the physics lens is dilution,
  temperature and texture rather than Maillard, but the pass is the same shape.
- **Research bursts** — multi-query web research can fan out across subagents
  if the volume warrants it

What subagents *cannot* do: replace the active conversation. The interactive
walk (CURATE role-by-role, vector opt-in, soft-conflict overrides) must stay in
the active session because that is where `AskUserQuestion` reaches the user.

## Off-ramp

The chef session ends when GUIDE writes `recipe.md` and the chat summary prints.
The active session returns to its default behavior afterward — `/chef` does not
permanently transform the assistant.
