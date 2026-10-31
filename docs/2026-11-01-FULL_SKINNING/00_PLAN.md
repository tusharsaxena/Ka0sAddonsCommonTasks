# Plan: full skinning

Goal: change the skin and every Ka0s addon changes with it, uniformly. Starts after the v1.84.0 merge, on `feat/2026-11-01-full-skinning`. Input: `inputs/SKIN_CAUSES.md`, with `plan-data/SKIN_CAUSES_map.csv` tying each CSV row to a cause.

Owner rulings, 2026-11-01:

- The settings panel stays stock by default (`skin.ignorePanel` true), but every element in it must support skins with the Scope cleared.
- Reverse "HUD colors are the player's": D2 to D7 are Fix.
- Overwriting player choices is accepted: migrate existing profiles to follow the skin, not new profiles only.
- Meaning colors stay (MC).
- The Leave list stands: L10, L11, L12, L13, D8, D9, A6, A7, A8, A9.
- D5: fix glow, leave warning tints.
- A4 is in, and nothing on the Ace profile page changes. Paint the delete confirmation only, scoped to our own use of it, and never for another addon's.

Order: L1 to L9 as one library release; D1; new skin tokens for D2, D3 and D6; default flips and the migration per addon (D2 to D7); A1 to A5; then a gate: a standard rule, a kit check that flags typed colors and textures, and a test that switches skins and fails if a painted surface does not change.

Each addon's migration runs once with a schema step, tested on stored partial values; a player's class and meaning colors are not touched.
