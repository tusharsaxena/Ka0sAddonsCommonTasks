# LibKa0s v1.105.0 adoption (phase [3])

This run adopts the LibKa0s v1.105.0 surfaces in the addons. It is phase [3] of
`docs/2026-11-16-LIBKA0S_ISSUES_75_PLUS/03_ADOPTION_PLAN.md`, which is the source of the surfaces, the affected addons
and the order. Every addon already vendors v1.105.0, merged on 2026-11-17. The owner asked for this run as the next
milestone after that merge.

- **Branch:** `feat/2026-11-17-libka0s-adoption`, created in each repo a wave touches from its default branch
  (`main` for CombatTrail and SkillMaster).
- **Library:** read-only. If adoption finds a library defect, the lead fixes it on its own LibKa0s branch, cuts a new
  tag and re-vendors it as its own commit. A vendored copy is never edited.
- **State:** git only. An item is done when a commit whose subject starts `<ID>: ` is on the run branch, or when
  `plan-data/exceptions.tsv` lists it with a proof command. Run `bash plan-data/resume-state.sh` to see where it stands.
- **Rules:** WowAddonStandards v2.113.0 (preview-mode "Where the strip sits", standalone-windows "The footer" and
  "Window chrome geometry", "Tooltip placement", launcher-§2 and §7, skinning-§2) and LibKa0s's `docs/api/`.
  DropWatcher on `master` is the reference for #88 and #89.

## Waves

Each wave ends with a lead checkpoint: every touched addon is gated under each client it ships, and its run branch is
pushed. The owner then smokes the wave's sheet. A later wave starts once the earlier one's code is pushed. Its smoke
does not need to have passed first, because each wave touches different code.

| Wave | Surfaces | Addons |
|---|---|---|
| **A** | Default skin compliance (skinning-§2); #88 docked test/sim strip; #89 `W.Footer` 24 px | AT, AM, KC, BL, CT, DR, LH, ST, MM, OR, SM, PGFE, WG |
| B | #86 `W.HeaderButtons` (settings mark on every own window; drag-handle settings mark) | per `03_ADOPTION_PLAN.md` |
| C | #92 tooltip placers (and the two player-option rulings below) | all but PM and PFE |
| D | #79 `D:Report`; #87 `Sim.Sample`; #80 `W.Bar` and #81 Journal (SM); #85 Callout (DR); #82 host hot tokens | per `03_ADOPTION_PLAN.md` |

A wave's items are added to `items.tsv` when the wave starts, after its addons' candidate lists have been checked
again. The candidate lists are `docs/revendor/2026-11-16-v1.105.0/02_CANDIDATES.md` in each addon.

## Rulings (the lead's, under the owner's standing guidelines)

1. **#85:** adopt the recommendations. DpsRace replaces `modules/Countdown.lua` with the Callout major in wave D.
   DropWatcher and QuickComms are "not now" and Skill Master is "never", each recorded on #85 at wave D.
2. **KickCD #88:** the HUD strip follows v2.110.0, which retired the HUD exemption. This reverses KickCD's ruling
   D-13. `tests/test_sim_marker.lua` is inverted in the same commit.
3. **Skin Tester #88:** the showroom's per-cell strips are specimens of the widget, not markers of test data.
   They stay as they are, and the item is recorded in `exceptions.tsv`.
4. **One commit per surface per addon** (`AD-<issue>-<ABBR>`, `AD-DS-<ABBR>` for the default skin). #88 and #89 in
   one addon may share a commit (`AD-88-XX + AD-89-XX: ...`) when they move the same window's geometry. The addon's
   smoke checks and docs move in the same commit as its code.

## Owner calls (needed by wave C, not before)

- **AuraMaster `tooltipAnchor`** and **MultiMeters' tooltip anchor** are player options that offer the cursor and
  the corner anchors, which the placement rule retires. Recommendation: keep each option, offer only the
  rule-compliant placements, and migrate a saved cursor or corner value to the default.
