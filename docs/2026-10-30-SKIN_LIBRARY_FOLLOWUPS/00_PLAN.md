# Plan: the skinning rollout's library follow-ups

Created 2026-10-30 on the owner's rulings on the nine LibKa0s follow-ups that
`docs/2026-10-29-SKINNING_ROLLOUT/99_REPORT.md` listed, plus call 2 of that run (Ignore fonts and the HUD) and the
first-run picker's title. The standing run guidelines apply: ask upfront, then decide; a resumable, checkpointed plan;
a branch and incremental commits; push at milestones; merge only on the go-ahead; delete every branch, stash and
worktree the run created once merged; ultracode.

Branch `feat/2026-10-30-skin-library-followups` in every repo the run touches.

## Owner rulings (2026-10-30)

| # | Follow-up (rollout report numbering) | Ruling |
|---|---|---|
| R-1 | Call 2 / follow-up 1: Ignore fonts does not reach the HUD | **Ignore fonts covers the HUD too.** With it on, HUD text ignores "From skin" for face and outline and uses the HUD element's own font setting. The composer's picker stops previewing the skin's face. |
| R-2 | 2: `opts.stockDefault` is honoured only in part | **Retire the stock look under Ka0s Default.** Ka0s Default looks like Ka0s Default everywhere; a player who wants the stock look picks the WoW Default skin. `stockDefault` and `stock` go; PageButton forwards its opts. The **Ignore settings panel** Scope switch is a separate thing and **stays, default on** (owner answer, 2026-10-30). |
| R-3 | 6: `S.CloseButton` does not save the art's prior tint | Fix it in the library. |
| R-4 | 9: under the eight non-Ka0s skins, `hud.font` falls back to Friz Quadrata | **Every skin gets its own HUD font.** The run picks one per skin (OFL only, a face the library already ships where one suits); the owner judges them in the smoke test. |
| R-5 | 4: `S.Text` and `WidgetsReorder` ignore the Ignore settings panel scope | **Skin them and every other custom LibKa0s widget, and make each obey the Scope switches** like the AceGUI widgets (owner answer, 2026-10-30). |
| R-6 | 5: `Skin.ResetToSkin` writes `"@skin"` into an absent bool companion | Incorrect behaviour: fix it. |
| R-7 | 7: WidgetsDragHandle's tooltip colors are literals | Use the skin's tooltip colors (`gtip.*`). |
| R-8 | 8: the `q.*` tokens' Ka0s Default values are rounded | Match the client's values exactly. |
| R-9 | 3: `Skin:__DrawsKey` is internal | Make it a public value. |
| R-10 | Standard: skinning-§3 calls the tab "Appearance" | Rename it to "Skin" in the standard. |
| R-11 | First-run picker (owner screenshots, every addon): "Choose a skin for <addon>" is cut off | Title becomes **"Choose a skin"**; the addon's name goes on its own line **above the skin dropdown**. |
| R-12 | Strategy | The lead's recommendation: one LibKa0s release, then a re-vendor in which each addon deletes the workarounds the release makes unnecessary. |

## Scope

- **LibKa0s**: LK-01..LK-11, released as `v1.81.0` (local tag; pushed only at finalize).
- **WowAddonStandards**: WS-01, the rules the rulings change (§3's tab name, the retired stock look, Ignore fonts on
  the HUD, custom widgets and the Scope), recorded in open-evolutions.
- **LibKa0sSkinTester**: ST-01, re-vendor plus showroom samples for every new token and every custom widget.
- **Every addon that vendors LibKa0s's Skin major**: the fourteen of the rollout and LootHistory (on v1.79.0; it
  joins if M0 finds its gate green on master, else it is an exception with the proof).
- This repo: the plan and the record (CT-01).

## Milestones

| M | What | Checkpoint |
|---|---|---|
| M0 | **Inventory**, read-only: per ruling, the exact library sites; every custom widget and how far it is skinned and scoped; per addon, every workaround the release makes unnecessary, every `stockDefault`/`stock` use, every smoke check whose expectation changes; the HUD font candidates per skin. Written to `inputs/inventory/`, consolidated in `01_INVENTORY.md`. | Consolidated item list; addenda for split items |
| M1 | **Upstreams**: LK-01..11 then LK-90 (release `v1.81.0`, local tag); ST-01; WS-01. Independent review of LibKa0s and its fixes. | Gates green; release run green; reviews recorded; branches pushed; tag local only |
| M2 | **The addons, in parallel**: one implementer per repo (re-vendor, delete workarounds, docs and smoke checks), then an independent review and its fixes. | Every gate green; reviews recorded; branches pushed |
| M3 | **Record**: `99_REPORT.md`, `06_SMOKE_TESTS.md`; stop for the owner's in-game smoke and go-ahead. | Report committed and pushed |
| M4 | **Finalize** on the go-ahead only: `/dev-copilot:finalize` (upstreams first), push the tag, delete every branch, stash and worktree the run created. | — |

## Library items (M1, LibKa0s)

| Id | Ruling | What |
|---|---|---|
| LK-01 | R-1 | `S.Resolve` / `Token` honour the owner's Ignore fonts for `hud.font` and `hud.outline` (the stored value wins); the composer's font picker previews the stored face while Ignore fonts is on. |
| LK-02 | R-2 | Retire `opts.stockDefault` and `opts.stock` from every primitive: Ka0s Default always paints the Ka0s look. Unknown keys are ignored, so a stale caller degrades to the Ka0s look rather than erroring. PageButton forwards its opts. The FadeRegions and LK-05 doc rows corrected. |
| LK-03 | R-3 | `S.CloseButton` saves the art's own tint on first paint and restores it whenever it unpaints (stand-down, release, a scope that leaves it stock). |
| LK-04 | R-4 | `hud.font` (and `hud.outline` where it suits) for each of the eight non-Ka0s skins in SkinDefs; no KEEP fallback left for the HUD face; the font registered and credited if new. |
| LK-05 | R-5 | `S.Text` and `WidgetsReorder` obey the owner's Ignore settings panel / Ignore fonts. |
| LK-06 | R-5 | Every other custom LibKa0s widget (M0 lists them: drag handle, autocomplete, copy window, line chart, toast, launcher, debug log, perf and sim panels, ...) painted from skin tokens and obeying the Scope. M0 may split this into an addendum, one id per widget family. |
| LK-07 | R-6 | `Skin.ResetToSkin` leaves an absent bool companion a bool. |
| LK-08 | R-7 | WidgetsDragHandle's tooltip title and body take `gtip.*`. |
| LK-09 | R-8 | The `q.*` tokens' Ka0s Default values equal the client's quality colors exactly. |
| LK-10 | R-9 | A public `Skin:DrawsKey(owner)` (or the name M0 finds fits the API), documented in `docs/api/`; `__DrawsKey` kept as an alias only if a consumer still calls it. |
| LK-11 | R-11 | OptionsSkinPicker: title "Choose a skin"; the owner's label on its own line above the dropdown, never truncated (the window grows to fit). |
| LK-90 | — | Release `v1.81.0`: the release battery green, CHANGELOG, "What a consumer owes", the local tag. |

Every LK item lands with tests that fail without it, keeps Ka0s Default's look except where a ruling changes it
(R-2, R-11), and gives the eight other skins and the `eui` source a value where it adds a token.

## Addon items (M2)

Prefixes: AT AbsorbTracker, AM AuraMaster, BL BankLedger, CM ConsumableMaster, DR DpsRace, DW DropWatcher, KC KickCD,
LH LootHistory, MM MultiMeters, PM PanelMaster, PF PartyFrameEnhanced, PG PremadeGroupsFilterExtension, PC PrettyChat,
QC QuickComms, WG WhatGroup.

| Id | What |
|---|---|
| XX-RV | Re-vendor LibKa0s from `v1.81.0` (`git archive` of the tag, never the working tree), prune icons, roll the provenance line, meet the release's "What a consumer owes", move the release pins. |
| XX-01 | Delete every workaround the release makes unnecessary (M0's list for the addon): the HUD Ignore-fonts patches, `stockDefault`/`stock` callers, the hand-rolled Scope guards, the ResetToSkin guards, the `__DrawsKey` reach-in, close-button tint handling. Where the addon resolves a HUD face itself, it honours Ignore fonts the library's way. Tests that pinned the old behaviour move to the new one. |
| XX-02 | Docs and smoke checks: every check whose expectation changed (AM SKIN-10, KC SKIN-14, the QuickComms Ignore-fonts check, PGFE SKIN-11, the stock-look rows), the picker check, ARCHITECTURE and testing notes. |

An item with nothing to do in an addon goes in `exceptions.tsv` with a command that proves it.

## Decisions taken by the lead (no need to ask)

- **Version**: LibKa0s `v1.81.0` (a minor: retiring `stockDefault` changes looks, not signatures). No addon version
  is bumped.
- **HUD fonts (R-4)**: the lead picks per skin from OFL faces; the choice and its reasoning go in `DECISIONS.md` and
  each skin's face shows in the Skin Tester and the smoke test.
- **Stale `stockDefault` callers** degrade to the Ka0s look, not an error, so an addon a release behind still loads.
- **LootHistory** joins only on a green gate on master.
- Doubtful calls go in `DECISIONS.md`. The run stops to ask only for something the rulings above do not cover and
  that would change what a player sees.

## Gates

Every repo: `~/.claude/dev-copilot/bin/ka0s-bounded lua tests/run.lua`, `~/.claude/dev-copilot/bin/ka0s-bounded
luacheck .` (0 warnings, 0 errors) and the 1500-line cap, green at every commit; the vendor gate holds each addon to
the tag it names. LibKa0s also passes its release run before the tag. Smoke checks are the owner's; none is marked
passed here.

## State and resume

Git is the only state: an item is done when a commit whose subject starts `<ID>: ` is on the run branch of the repo
that owns it. `items.tsv` is the manifest (addenda in `plan-data/addendum-NN.tsv`), `resume-state.sh` computes
progress, `RESUME.md` tells a fresh session how to pick up, `checkpoints.tsv` logs each milestone's evidence and
pushed heads, and reviews are `refs/notes/ka0s-review` notes pushed with the branch.
