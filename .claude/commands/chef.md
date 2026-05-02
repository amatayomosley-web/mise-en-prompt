---
description: Activate the chef agent in the active conversation. Walks the user through the 8-phase mise-en-place flow with AskUserQuestion firing role-by-role in CURATE. Designed for interactive cooking design, not one-shot recipe generation.
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
3. Enters Phase 1 — INTAKE — by asking the user what they want to cook

The active session then runs the full 8 phases (INTAKE → CLARIFY → GROUNDING →
RESEARCH → CURATE → SYNTHESIZE → ENHANCE → GUIDE), persisting state to
`sessions/<session_id>/state.yaml` after each meaningful decision and writing the
final `recipe.md` only at GUIDE.

## When subagents *are* useful inside this flow

The chef-as-active-conversation can still delegate bursts to Task subagents for
work that benefits from a fresh context window:

- **ENHANCE pass** — running both lenses (physics + flavor) over a long Method
  draft is a good subagent task; the result populates `state.enhancements` and
  the active chef renders it
- **Research bursts** — multi-query web research can fan out across subagents
  if the volume warrants it

What subagents *cannot* do: replace the active conversation. The interactive
walk (CURATE role-by-role, vector opt-in, soft-conflict overrides) must stay in
the active session because that is where `AskUserQuestion` reaches the user.

## Off-ramp

The chef session ends when GUIDE writes `recipe.md` and the chat summary prints.
The active session returns to its default behavior afterward — `/chef` does not
permanently transform the assistant.
