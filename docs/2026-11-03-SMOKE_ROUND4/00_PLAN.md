# Smoke round 4: plan

Input: `inputs/OWNER_FEEDBACK.md` (2026-11-03, images `inputs/images/1-22.png`). Diagnosis: `inputs/INVESTIGATION.md`
(read-only workflow wf_f2e8c9bf-4fb, every area challenged by an independent skeptic; all held).

Branch: `feat/2026-11-01-full-skinning` in every repo, as rounds 1-3. LibKa0s tag v1.85.0 stays local and is re-cut.
**Outfitter is never touched** (owner, 2026-11-03: a separate agent is converting it). The 16 addons are the ones in
round 3's `resume-state.sh`.

## Milestones

- **M1** (no sign-off needed): R4-L1, R4-ST1..4, R4-DR1..6, R4-MM1, then R4-REL and R4-RV. R4-MOCK in parallel.
- **M2** (waits for the owner's sign-off on the mockup): R4-L2 header, R4-L3 icon border colours, R4-REL2, R4-RV2.
- **M3**: R4-GATE.

## Lead's calls (owner asked to decide; each can be reversed at smoke)

1. **Dropdown close scope (R4-L1).** Only dropdowns on Ka0s-owned surfaces close on an outside press (a Ka0s
   settings page, including its AceDBOptions Profiles page, or a Ka0s window). Other authors' AceGUI dropdowns in
   the same client keep AceGUI's behaviour. Escape is not added: it is not cheap to do safely, and on a settings page
   Escape already closes the panel. A press on the pullout, its scrollbar or the owning dropdown never closes it.
2. **Item 3 answer.** The element is the Skin Tester's own "TreeGroup via PaintAce" showroom sample, not a real
   page. The only real AceGUI TreeGroup in the collection is PrettyChat's string editor, which already has the fix.
   The sample collapses to 20 px because AceGUI's auto-height runs on an empty List layout; the fix is PrettyChat's
   `SetAutoAdjustHeight(false)`, plus a placeholder label so the right pane reads as a page.
3. **Tester ignorePanel.** Default false in the tester only; recorded in the tester's deviation register (skinning
   §3 default). No migration: a stored profile keeps its own value. The Skin tab's "Copy to every Ka0s addon" keeps
   copying the Scope as the library does today.
4. **DpsRace centring.** Each block's contents are centred; Results detail row 2 centres Delta + New best as a pair
   under the three boxes. The Stop! and waiting tiles get the same centring for consistency.
5. **Consumables on Your best.** Icons (12 px) with "xN" when used more than once, names in the hover; every kind
   DpsRace already records counts (potions, flasks, food, augment runes, Healthstones). Blank when none. The hover
   keeps the top 3 spells and adds the consumables.
6. **DpsRace sim Racing step.** The race clock plays about 3x fast during the Racing step, so ~10 s of wall time
   covers the 30 s sample race with dense damage events and the buzzer follows by itself; the chart fills with no
   gaps. The stepper contract comment and the SF-DR-8 / SG-SIM wording change with it.
7. **MultiMeters sim.** Every fight step in every scenario lasts about 10 s of wall time at the default step delay.
   Step labels show the wall duration, e.g. "Pull Trash (10 s)".
8. **Header and icon borders** are not decided by the lead: the owner asked to sign off on the mockup (R4-MOCK).
   The mockup also fixes the Showroom double paint (R4-ST4), so what the owner sees matches the tokens.

## Rules

Every addon's green gate is its CLAUDE.md's. Commit subjects start `<ID>: `. Never push a tag, merge, or bump a
version. Push the branch at M1 and M3 checkpoints (owner's standing guidelines). Owner runs every smoke check.
