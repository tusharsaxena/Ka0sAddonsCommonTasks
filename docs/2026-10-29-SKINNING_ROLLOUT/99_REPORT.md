# Report: the skinning rollout to the fourteen remaining addons

The execution record for `00_PLAN.md`. The plan and `DECISIONS.md` are frozen and are not edited. Calls
made during M2 that add to or differ from `DECISIONS.md` are recorded here, under "Decisions made in M2".

Branch `feat/2026-10-29-skinning-rollout` in LibKa0s, LibKa0sSkinTester, WowAddonStandards, the fourteen
addons and this repo. All of them are pushed. Nothing is merged. The LibKa0s tag `v1.80.0` (912f1b4) is
**local only**.

## Milestones

| M | Result |
|---|---|
| M0 | 46 gaps inventoried, 35 real, consolidated in `01_INVENTORY.md` |
| M1 | LK-01..05 + LK-90, ST-01/02, WS-01 landed and reviewed; LibKa0s v1.80.0 cut as a local tag; standard v2.91.0 |
| M2 | 85/85: 80 items by commit, 5 by exception (`exceptions.tsv`); every addon independently reviewed and its fixes landed |
| M3 | This report and `06_SMOKE_TESTS.md` |
| M4 | Waiting for the owner's smoke test and go-ahead |

The first M2 workflow (wf_c486ff27-bc7) died mid-run. Its relaunch (wf_a2d24504-cd0) also stopped
while the QuickComms fix round was in progress. The lead finished that round by hand: the pad inner rule
(5df98bd), SKIN-1/SKIN-3 (b2ba537) and the review note. No library re-cut was needed in M2. Every
library gap an implementer hit was worked around in the addon (gap policy rung 1). They are listed below
as follow-ups.

## M2 per addon

Gates were re-run by the lead on the pushed heads, through `ka0s-bounded`. Tests are passed/failed/skipped.
Every addon's luacheck shows 0 warnings / 0 errors. The one skip in each addon is the kit's declared
diagnostics opt-out.

| Addon | Commits | Head | Tests | Exceptions | Smoke checks |
|---|---|---|---|---|---|
| AbsorbTracker | 9 | 02bd260 | 954/0/1 | AT-02 (no window of its own) | SKIN-1..26 |
| AuraMaster | 9 | fd376e7 | 2212/0/1 | — | SKIN-1..24 |
| BankLedger | 9 | efbf369 | 1508/0/1 | BL-03 (no HUD) | SKIN-1..26 |
| ConsumableMaster | 8 | e7eb736 | 1292/0/1 | — | SKIN-1..23 |
| DpsRace | 9 | 228cf04 | 1145/0/1 | — | SM-DR-SK1..24 |
| DropWatcher | 10 | 759646b | 1790/0/1 | — | SKIN-1..24 |
| KickCD | 9 | 2b11c13 | 1554/0/1 | — | SKIN-1..29 |
| MultiMeters | 11 | 6a6a821 | 2403/0/1 | — | SKIN-1..24 |
| PanelMaster | 7 | 6f41ca9 | 1140/0/1 | — (PM-03 landed; no O2 reset by D1) | SKIN-1..20 |
| PartyFrameEnhanced | 10 | 3a0dd72 | 538/0/1 | — | SKIN-1..25 |
| PremadeGroupsFilterExtension | 9 | 484c48d | 432/0/1 | PG-03 (no HUD) | SKIN-11..32 (SKIN-1..10 retired with the bridge) |
| PrettyChat | 7 | 99140a8 | 631/0/1 | PC-03 (no HUD) | SKIN-1..17 |
| QuickComms | 10 | b2ba537 | 1254/0/1 | — | SKIN-1..23 |
| WhatGroup | 7 | ce2c96b | 1025/0/1 | WG-03 (no HUD) | SKIN-1..24 |

Only one file is over the 1500-line cap: PrettyChat's `GlobalStrings/GlobalStrings.lua`. It is Blizzard's
string dump and was already on master, so it predates this run.

## Owner calls

These are the questions the implementers could not settle, because the answer changes how Ka0s Default
looks. Each one is written into that addon's smoke checks, so the in-game result settles it. Each is
also a one-line change either way.

1. **KickCD cast-bar borders.** The two cast-bar borders follow `bar.borderStyle`, which is `None` in
   every skin. After the O2 reset, cast bars draw no border under any skin, Ka0s Default included. That is
   X3/X5 as written, and PartyFrameEnhanced's cast bar matches it. To keep an edge, either give both
   BorderGroups `fromSkin = "icon"` (a flat 2 px edge) or default the companions false and drop them from
   the reset. The checks are KickCD SKIN-1 and SKIN-6.
2. **Ignore fonts does not reach any HUD.** `S.Resolve`/`Token` for `hud.font` ignore the Scope's Ignore
   fonts; only `P.font` checks it. AbsorbTracker and ConsumableMaster worked around it in the addon. In
   AuraMaster, KickCD and QuickComms the HUD keeps the skin's face with Ignore fonts on. This is
   documented as current behaviour (AM SKIN-10, KC SKIN-14, QC). The right fix is in the library (see
   follow-ups), so the owner's call is whether Ignore fonts should cover the HUD at all.
3. **Oxanium on addon-drawn text under Ka0s Default.** Since v1.79.0, Ka0s Default's faces are Oxanium.
   Most addons now draw their own window strings in it, through S.Text, S.Font or S.Shell. Examples:
   DropWatcher's windows, the MultiMeters export modal, ConsumableMaster's KCM rows, the PanelMaster
   unlock label, the PartyFrameEnhanced holder caption, the BankLedger and DpsRace labels, and the
   QuickComms Preview title. Where an implementer could keep the old face without a decision, it did:
   the QuickComms icon browser (83b8dc0), the AuraMaster frame picker, the DpsRace custom-length box
   and the MultiMeters column labels. Each addon's SKIN-1..3 names its face changes.
4. **New title bands and flat controls under Ka0s Default.**
   - DropWatcher D3 adds the Shell's title.bg band (`noTopBar = true` reverts it). DW SKIN-2 asks.
   - The DpsRace modals take the Shell.
   - The WhatGroup Close button becomes the flat control (D4).
   - DropWatcher's scroll bars become the library's (D2).
   - The QuickComms icon browser scroll bar becomes a flat knob (D3).
5. **MultiMeters window chrome stays the player's under every skin** (X4 over D1/D3/D4/D16). Only the
   faces, bars, rows, inner rule and divider follow the skin. MM SKIN-4 puts this to the owner; if it is
   overruled, it becomes a follow-up item.
6. **BankLedger close control.** BL's own button is kept, with
   `S.CloseButton(close, { stockDefault = true })`, so Ka0s Default is exact and other skins paint it.
   Dropping `stockDefault` takes the skin's close tints on Ka0s Default too.
7. **X11 (from M1).** PrettyChat's settings TreeGroup takes the library's flat edge under Ka0s Default.
8. **Commit trailers.** The first commit or two on several branches (for example DW-RV 6920689, BL-RV
   d66414f, DR-RV 302c2ba, PF-RV 5c5448a and WG-RV 058a033) carry the Claude-Session line of the session
   that wrote them before it was interrupted. That attribution is accurate. The branches are pushed now,
   so rewording would need a force-push. The recommendation is to accept them as they are.

## Decisions made in M2 (not in DECISIONS.md)

- **Icon borders use the LK-04 icon family** (`BorderGroup{ fromSkin = "icon" }`) in KickCD,
  ConsumableMaster, QuickComms and DropWatcher. The inventories predate LK-04 and named
  `bar.borderStyle`. The companion also governs thickness, so a stored 1 px (QC) or 3–4 px (KC) icon
  border becomes the skin's 2 px after the reset. ConsumableMaster's buttons get a flat 2 px edge in the
  player's own color instead of none.
- **Owner tokens without `follow` (X2 exceptions).** QuickComms `qc.veil`/`qc.veilCool` have none,
  because `cover.dim` is the same in every skin and following it would merge the two states.
  ConsumableMaster keeps the disabled icon at `text.disabled` RGB with a fixed 0.5 alpha, because an
  owner token would lose the half alpha under other skins.
- **Quality colors keep the client's hex.** BankLedger's Minimum-quality labels and DropWatcher's
  `NS.QualityColor` use `ITEM_QUALITY_COLORS`. The library's `q.*` tokens are rounded to two decimals and
  would move Ka0s Default by one byte.
- **Game-meaning glyph.** QuickComms `Ed.ACTIVE_DOT` keeps Blizzard's Indicator-Green.
- **QuickComms dial hub labels** (stale, LOCKDOWN, TEST) keep their font-object faces. They take token
  colors only, and Ka0s Default is unaffected.
- **PanelMaster has no O2 reset** (its D1: panels are player content). PM-03 landed with a commit, so it
  needs no exception row. Proof: `git -C ../PanelMaster diff master..HEAD -- core/Database.lua core/Namespace.lua | grep -c ResetToSkin`
  prints 0.
- **PartyFrameEnhanced D4 not adopted.** S.IconBorder on the cast icon would add an edge that Ka0s
  Default does not draw; DpsRace's D-10 is the same call. PFE keeps the picker's eye, because its
  unlocked view is its preview mode.
- **DropWatcher token picks.** The countdown track uses `list.boxEdge`, which is exact at .12.
  `dw.offSpec` follows `sem.warband`, so Off-spec stays distinct from Offer.
- **PrettyChat picker timing.** The picker shows synchronously at OnEnable, with no timer and no combat
  hold, because PrettyChat arms nothing while running. A login in combat skips it until the next one.
- **Picker timers** use each addon's own timer seam (AceTimer, C_Timer, or InCombatLockdown plus a bus
  target) where it has no `NS.After`. Each one is cancelled by the stand-down.

## Library follow-ups (gap policy rung 1 workarounds in place)

None of these blocked the run. They are candidates for a LibKa0s issue each, to be filed with the owner's
agreement.

1. `S.Resolve`/`Token("hud.font")` and `hud.outline` ignore the owner's Ignore fonts, and the composer's
   font picker previews the skin's face even with Ignore fonts on. Found by AT, CM, AM, KC and QC.
2. `opts.stockDefault` is not honoured by Checkbox, FadeRegions or Text/Font, and PageButton does not
   forward opts. LK-05's documented `stock = { win.Bg }` does nothing when Bg is a frame. FadeRegions'
   doc row ("Ka0s Default fades nothing") is stale. Found by PG and QC.
3. There is no public "which key does this owner draw by": `Skin:__DrawsKey` is internal (PG).
4. `S.Text` and `WidgetsReorder` ignore the owner's Ignore settings panel scope (CM; PM and PC composed
   the same guard).
5. `Skin.ResetToSkin` writes the `"@skin"` sentinel into an absent bool companion (AT, QC, AM).
6. `S.CloseButton` does not save the art's prior tint, so the switch back to Ka0s Default under
   `stockDefault` has nothing to restore (BL).
7. WidgetsDragHandle's tooltip title and body colors are literals, not the owner's `gtip.*` (AM).
8. The `q.*` tokens' Ka0s Default values are rounded from the client's hex (BL, DW).
9. Under the eight non-Ka0s skins, `hud.font` falls back to Friz Quadrata (SkinDefs' KEEP). Each skin
   could carry its own HUD face (AT SKIN-5 records the current behaviour).

Standard follow-up: skinning-§3 says the tab is labeled "Appearance", but the library has rendered
"Skin" since OptionsAppearance minor 3 (WG review F5).

## Next

1. The owner runs the in-game smoke test (`06_SMOKE_TESTS.md`) and rules on the owner calls above.
2. Follow-up fixes, if any, land on the same branches.
3. M4, on the go-ahead only: `/dev-copilot:finalize` in RESUME §6's order, push the v1.80.0 tag, and
   delete the branches, stashes and worktrees.

## After M3: the owner's rulings (2026-10-29)

The owner's rulings are in `OWNER_RULINGS_M3.md`. They produced three addendum items, each reviewed, with
its gate re-run by the lead:

- **KC-A1** (72969e1): the cast-bar borders follow the icon border family, a flat 2 px edge under Ka0s
  Default. KickCD 1555/0/1.
- **BL-A1** (d20a28b): the close control is the library's `S.CloseButton` under every skin, and
  `bl.closeRest` is retired. LEDG-35 is re-opened for the owner. BankLedger 1509/0/1.
- **MM-A1** (44b21ad..0aed7f5): the meter window's fill, edge, header strip and header controls follow the
  skin (a `skin` mode, the default), and step v20 → v21 resets every profile once. The independent review
  found 8 minors; 5 were fixed and the gradient title band is documented. MultiMeters 2415/0/1.

The owner accepted calls 3–4 as built and left the trailers as they are. Call 2 (Ignore fonts and the
HUD) was not ruled on and stays library follow-up 1. The owner gave the go-ahead to sync docs, merge,
push and delete the branches without waiting for the in-game smoke test, so every smoke check in
`06_SMOKE_TESTS.md` is still owed.

## M4: finalized (2026-10-29)

On the owner's go-ahead, `/dev-copilot:finalize` ran in dependency order: WowAddonStandards → LibKa0s (tag
`v1.80.0` at 912f1b4 **pushed**) → LibKa0sSkinTester and the fourteen addons → this repo.

- **Doc sync:** content only, one agent per repo (wf_9effca84-081), with `SD-FIN-04` commits in 14 repos
  and none needed in WowAddonStandards, BankLedger or PartyFrameEnhanced. Every gate was green after the
  sync.
- **Merges:** each was `--no-ff` onto an unmoved master, so each merge tree equals the gated branch tree.
  Each was pushed with its `ka0s-review` notes, and the branch was deleted locally and on origin.
- **Heads:** WowAddonStandards f5e5009, LibKa0s ea1d92d, LibKa0sSkinTester 9dab27b, AbsorbTracker a41affd, AuraMaster e565220, BankLedger 647e34f, ConsumableMaster 86dfb1b, DpsRace 4816414, DropWatcher 8851923, KickCD c006208, MultiMeters 6c5e837, PanelMaster febaed5, PartyFrameEnhanced b64ba84, PremadeGroupsFilterExtension 2fc7ae3, PrettyChat cfd8c58, QuickComms c77daa1, WhatGroup d8e52f4.
- **Clean-up:** none of the 18 repos has a stash or an extra worktree. No version was bumped.
- **Not done:**
  - No `docs/revendor/` bundle exists for the v1.80.0 re-vendor in any addon.
    `/dev-copilot:wow-revendor-libka0s` owns that.
  - A few repos' docs/testing.md and DEPENDENCIES.md still show a bare `luacheck .` where CLAUDE.md
    names the bounded runner.
  - Dead exports, reported and not removed: `NS.SkinPaintAce` in PrettyChat and `NS.SkinOnRelease` in
    AuraMaster, both used only by tests.
- **Still owed:** every smoke check in `06_SMOKE_TESTS.md`, and LEDG-35 in BankLedger.

## After M4: owner ruling on call 2 (2026-10-30)

**Ignore fonts covers the HUD too.** With it on, HUD text ignores "From skin" for the face and outline and
uses the face set in that HUD element's own font setting. This turns library follow-up 1 into planned work:
`S.Resolve`/`Token` honour Ignore fonts for `hud.font` and `hud.outline`, the composer's font picker stops
previewing the skin's face, LibKa0s is released and re-vendored, and the AbsorbTracker and ConsumableMaster
workarounds are removed. AuraMaster SKIN-10, KickCD SKIN-14 and the QuickComms check are then rewritten to
expect the HUD's own face. Not started; it needs its own run.
