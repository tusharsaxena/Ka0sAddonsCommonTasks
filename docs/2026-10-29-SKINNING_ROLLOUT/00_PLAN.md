# Plan: the skinning rollout to every remaining Ka0s addon

Created 2026-10-29 on the owner's word ("apply the skinning changes to all Ka0s addons (including DpsRace) ...
do each of them in parallel"), under the standing run guidelines: ask upfront, then decide; a resumable,
checkpointed plan; a branch and incremental commits; push at milestones; merge only on the go-ahead; delete
every branch, stash and worktree the run created once merged; ultracode.

This is leg 2 of the skinning run that `docs/2026-10-25-SKINNING/` started (R6: "Rollout to the other addons is
a second leg"). LootHistory (leg 1) and LibKa0sSkinTester already skin, and `docs/2026-10-28-SKIN_OVERRIDES_AND_PICKER/`
added the font and texture overrides and the first-run picker on LibKa0s v1.79.0.

## Scope

Fourteen addons, every row of `WowAddonStandards/standards/ADDONS.md` except LootHistory and LibKa0sSkinTester:
AbsorbTracker, AuraMaster, BankLedger, ConsumableMaster, DpsRace, DropWatcher, KickCD, MultiMeters, PanelMaster,
PartyFrameEnhanced, PremadeGroupsFilterExtension, PrettyChat, QuickComms, WhatGroup. All fourteen are on master,
clean, and vendor LibKa0s v1.77.0 at the start.

Upstreams as needed: LibKa0s (a primitive or token the inventory shows missing), WowAddonStandards (the rollout's
record in open-evolutions, and any rule the rollout shows is missing). This repo carries the plan and the record.

Branch `feat/2026-10-29-skinning-rollout` in every repo the run touches.

## Owner rulings (2026-10-29)

| # | Question | Ruling |
|---|---|---|
| O1 | A component no skin covers | The policy below, as proposed and accepted. |
| O2 | R3, the HUD style reset on adoption, now that the addons are published | **Kept.** The adoption resets saved HUD style values to follow the skin, once, for every player. |
| O3 | The first-run picker for existing players | **Shown to everyone.** `skin.pickerSeen` defaults to false on every profile, old and new. |
| O4 | PremadeGroupsFilterExtension's own EllesmereUI bridge (`core/EUIBridge.lua`, `modules/EUISkin.lua`) | **Retired** in favour of LibKa0s's `eui` source. The player's saved choice carries over in a migration step. |

The leg-1 rulings still hold (`docs/2026-10-25-SKINNING/inputs/OWNER_SCOPE.md`): per-addon choice with a copy to
every Ka0s addon, every visual element including the HUD, the nine skins, OFL fonts only.

## The gap policy (O1)

For a component no primitive covers, the first rung that fits:

1. **Compose it** from the existing primitives and tokens (`S.Panel`, `S.Card`, `S.Text`, `S.BarStyle`,
   `S.IconBorder`, `S.Color`, `S.Token`, ...). No library change.
2. **A new primitive or token in LibKa0s** when the shape recurs or no token describes it: Ka0s Default's value
   reproduces today's look exactly, each of the other eight skins gets a value of its own, the `eui` source gets a
   fallback from EllesmereUI's accent, panel color and font, the Skin Tester's showroom shows it (its coverage
   suite requires every vocabulary name), and tests pin it. All additions land in **one** library release,
   after M0's inventory, not one at a time.
3. **Untouched** where skinning-§7 says a skin never goes (Blizzard shared frames, StaticPopup, GameTooltip's
   frame, ColorPickerFrame, SharedMediaWidgets pull-outs, protected Blizzard frames such as the party frames
   PartyFrameEnhanced decorates; only the addon's own overlays skin). Each goes in `exceptions` with a reason.
4. **Game-meaning colors stay**: class colors, item quality, spell-school colors, spell and item icons, DPS Race's
   per-player colors. Listed as exceptions too, so the owner can overrule one.

A doubtful call goes in `DECISIONS.md` with the reason. The run stops to ask only if a change would alter Ka0s
Default's look today.

## Milestones

| M | What | Checkpoint |
|---|---|---|
| M0 | **Inventory**, one read-only agent per addon: every visual surface and the primitive that paints it, every HUD style setting (for O2), the exceptions, the gaps, and what the v1.77.0 → v1.79.0 re-vendor owes. Written to `inputs/inventory/<Addon>.md`, consolidated in `01_INVENTORY.md`. | The consolidated gap list, each gap ruled to a rung |
| M1 | **Upstreams.** LibKa0s items `LK-NN` for every rung-2 gap, released as v1.80.0 (local tag) with the Skin Tester's showroom sample (`ST-NN`); with no gap, M1 is empty and the addons vendor v1.79.0. WowAddonStandards `WS-NN` for any rule. | Gates green; branches pushed; tag local only |
| M2 | **The fourteen addons, in parallel**, one implementer per repo working its items in order, then an independent review and its fixes. | Every addon's gate green; reviews recorded; branches pushed |
| M3 | **Record**: `99_REPORT.md`, `06_SMOKE_TESTS.md`; stop for the owner's in-game smoke. | Report committed and pushed |
| M4 | **Finalize** on the go-ahead only: `/dev-copilot:finalize` (upstreams first), push the tag, delete every branch, stash and worktree the run created. | — |

## Items, per addon

Every addon gets the same six items under its prefix: AT AbsorbTracker, AM AuraMaster, BL BankLedger, CM
ConsumableMaster, DR DpsRace, DW DropWatcher, KC KickCD, MM MultiMeters, PM PanelMaster, PF PartyFrameEnhanced,
PG PremadeGroupsFilterExtension, PC PrettyChat, QC QuickComms, WG WhatGroup. An item with nothing to do in an addon
(XX-03 in an addon with no HUD) is recorded in `exceptions.tsv` with a command that proves it.

| Id | What |
|---|---|
| XX-RV | Re-vendor LibKa0s from the run's library tag (`git archive`, never the working tree), prune icons to the declaration, roll the provenance line; meet v1.78.0's and v1.79.0's "What a consumer owes" (the Options stub answers `AppearanceTab` and `AppearanceRows`, ...); move the release pins. |
| XX-01 | The skin seam: `core/SkinSetup.lua` registers the owner (the folder name) at file load, with a degradation stub; the `skin.*` profile keys (`source`, `skin`, `ignoreFonts`, scope, `font`, `texture`, `pickerSeen`) as skip-render schema rows written only through the write seam; the Skin tab on General; live repaint on a profile change; the owner handed to every library factory. |
| XX-02 | Every window, panel, dialog and popup the addon draws, painted through the facade. Typed colors, fonts and textures replaced by `S.Color` / `S.Token` (anti-pattern #107). |
| XX-03 | The HUD: bars, icons, glows and HUD text through the facade and `S.Resolve` / `Skin.FROM_SKIN`; the composer's `fromSkin` companions on the HUD style rows; **the one-time reset** (O2) as a per-profile migration step through `Skin.ResetToSkin`. |
| XX-04 | The first-run picker (O3), the addon's own AceGUI acquisitions (`Skin:PaintAce`, `Skin:OnRelease`), and the owner-aware tool surfaces (debug console, perf panel, sim panel, copy windows, test strip). |
| XX-05 | Docs: ARCHITECTURE, module-map, schema, settings-panel, `docs/smoke-tests.md` (per skin and under EllesmereUI), `docs/test-cases.md`, the README badge and font credits. |
| PG-06 | PremadeGroupsFilterExtension only: retire `core/EUIBridge.lua` and `modules/EUISkin.lua` (O4), with a migration step carrying the stored EllesmereUI choice to `skin.source = "eui"`. |

Upstream and record items: `LK-NN` and `ST-NN` (M1, from M0's gaps), `WS-01` (the rollout recorded in
open-evolutions, plus any rule the run shows is missing), `CT-01` (this bundle).

## Gates

Every repo: `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua` and `~/.claude/dev-copilot/bin/ka0s-bounded
luacheck .` (0 warnings, 0 errors) and the 1500-line cap, green at every commit. The vendor gate
(`tests/test_vendor_sync.lua`) holds every addon to the tag it names. Smoke checks are the owner's; none is marked
passed here.

## State and resume

Git is the only state: an item is done when a commit whose subject starts `<ID>: ` is on the run branch of the repo
that owns it. `items.tsv` is the manifest, `resume-state.sh` computes progress, `RESUME.md` tells a fresh session how
to pick up, `checkpoints.tsv` logs each milestone's evidence and pushed heads, and reviews are `refs/notes/ka0s-review`
notes pushed with the branch.
