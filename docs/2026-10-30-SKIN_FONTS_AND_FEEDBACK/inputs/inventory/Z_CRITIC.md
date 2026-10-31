# Z_CRITIC: completeness and consistency review of inventories A to K

Read-only review, 2026-10-30. I read OWNER_FEEDBACK.md and all 11 reports, spot-checked 2 or 3 claims per report against
the code, the SavedVariables and the font files, and looked at image-30. Paths are relative to `GIT/`.

## 0. State the run starts from (none of the reports has this)

- **The finalize is half done.** `LibKa0s` master is `667fb51` (it merges v1.81.0, and the `v1.81.0` tag exists).
  `WowAddonStandards` master is `9c4837e` (v2.92.0). **All 16 addon repos, the Skin Tester included, are still on
  `feat/2026-10-30-skin-library-followups` and not merged into master** (`git merge-base --is-ancestor`). Every tree
  is clean. The owner said to finalize first, so the addon merges have to finish before this run branches. This run
  also needs a branch name of its own.
- The line numbers the reports cite are still good. `git diff aefeba9 667fb51` is empty for LibKa0s, and the addon
  heads have not moved.
- The roster is 15 addons plus the Skin Tester, so 16 adopters. Each one vendors the **whole** font payload: 26 files
  and 3.7 MB under `libs/LibKa0s/media/fonts/`. There is no font prune, only `prune-icons.lua`.

## 1. Coverage: each owner item

| # | Item | Reports | Verdict |
|---|---|---|---|
| 1 | Overrides reset on a skin change | A, K 1d | Covered, with evidence. The picker preview and Apply to all are designed too. |
| 2-4 | Expressway, Prototype, Fira Sans Medium | B, C, K 7 | Covered. The license block is flagged in three reports (B §2, C §5, K Q4). **The reports disagree on what to do instead (§2 C13).** |
| 5 | Equal widths | C, K 1c | Covered by a measured model. **Gaps:** C fits only image-17, -18 and -28, and cites image-20 once. image-21..27 (the other skins' truncations) are never checked against C's predictions, and **image-25 does not exist** in `screenshots/`. Outline is not in the model (§2 C6). |
| 5b | Characters some faces cannot draw (image-19) | D, K 6 | Covered for the sites that render. **D's "Friz" column is wrong** (§3 E1). |
| 5 stray | The second "Change the font of" line | (owner) | Moot. |
| 6 | Reset buttons and Scope alignment | A, K 1d | Covered. The "stray icons" are a guess (A Q4), but image-30 agrees with it: a knob and a down button at the right edge. |
| 7 | Remove unused fonts | B §6 | Covered for option A only. Under option B or C the delete list changes. |
| 8 | PGFE expand/collapse | G | Covered. The Blizzard template geometry is "from memory, not verified" (G §2b). |
| 9a | AuraMaster TEST marker | H, K 2b | Covered. It conflicts with the preview-mode MUST, and the HUD-versus-window boundary is unresolved (§2 C18). |
| 9b | Glow regression | H | Covered, with a bisect and the owner's SavedVariables. **The same cause in KickCD is missed** (§4 R5). |
| 10a-c | DropWatcher dropdown, glow defaults, hidden sections | I | Covered. |
| 10 issues | LibKa0s MUST issue, toast stack | I, J, K 4 | Covered. **K contradicts I on the mechanism** (§2 C10). |
| 11a | Anchor title truncation | E, J 4 | Covered. Root cause 2 is speculative (§3 E3). |
| 11b | Sim placeholder anchor | E, K 2a | Covered. The normative strength differs between them (§2 C9). |
| 12 | `/xx skin` | F, K 1f/3 | Covered. **They contradict each other on the disabled and combat behavior** (§2 C8). |
| 13 | Outline (All / HUD / Off) | B §8, K 1d/1e | Partly covered. **K's wording makes "All text" a no-op, and B's "stored flags win" makes Off a no-op on most HUD text** (§2 C5, C6). |
| 14 | MultiMeters issues | J | Covered (drafts). Which animation is meant still has to be asked. |
| 15 | QuickComms | J | Covered. #13 exists, so the plan is a comment on it. |

No owner item is missing. The weak spots are 13 (semantics), 5 (the evidence base, and HUD) and 2-4 (the license path).

## 2. Contradictions between reports (each needs one answer before planning)

- **C1. Friz Quadrata coverage.** D measured `_retail_/Fonts/FRIZQT__.TTF`. **That file is Prototype on the owner's
  client.** Its md5 `0483b4ee…` matches `Ka0s Prototype.ttf`, and so do ARIALN, FRIENDS, MORPHEUS and skurri (I
  verified this). C says the same, and K says real Friz cannot be measured (it is only in CASC). D's "Friz lacks →
  ▲▼ €" rows are a copy of its Prototype rows. **Resolution:** treat real Friz as unmeasured everywhere (D §1, the D
  tables, K's coverage table and C's WoW Default row).
- **C2. Which Fira Sans Medium build.** B recommends google 4.203 at pinned `e345593d`. C measured the pack's 4.301
  (`plan-data/font_metrics.py:31`). D's and K's coverage tables are also for 4.301, and B says 4.203 lacks ▲▼▶◀
  (D's "▸ ▾ drawn by Fira" is a 4.301 fact too). **Resolution:** pick the build first. Then C's `WIDTH` guard table,
  D's safe set and K's allow-list are regenerated from the **shipped bytes**.
- **C3. WoW Forever titles and HUD face.** B recommends Fira Sans **SemiBold** for both (B Q3). C recommends **Medium**
  and computes Forever's HUD 12 on Medium (C Q5). K's text names only "Ka0s Fira Sans Medium". One answer is needed.
  I recommend B's SemiBold for the HUD, which follows the R-4 heavier-HUD rule, with C re-running the HUD row.
- **C4. Does "All text" outline the mono role?** B Q6 says yes. K Q6 says no, and writes it into the rule. I
  recommend **no**: debug digits clog, and D shows the mono face is where the symbol glyphs live.
- **C5. What "All text" applies to window text.** K 1e says *All text* "lets `font.outline` ... resolve as the skin
  states it". Every skin states `font.outline = ""` (`LibKa0s/LibKa0s/SkinDefs.lua:236`, which all skins inherit),
  so under K's wording the default does nothing for window text. B's table derives the flag from `hud.outline`
  (falling back to `"OUTLINE"`). **The standard text must follow B's table.**
- **C6. Outline against the addons' stored `fontFlags`.** B recommends that the stored value wins (B Q5). Then:
  - *Off* and *HUD only* leave the stored OUTLINE on AuraMaster, KickCD, PFE, QuickComms and AbsorbTracker HUD text.
  - *All text* never outlines MultiMeters (`"NONE"`) or DpsRace (`""`).

  The owner's answer defines the setting as "where the font flags apply", and *Off* that visibly does nothing on
  the HUD will read as broken. K is silent on it. **This goes to the owner** (Q1 in §5).
  - C also says outline "should barely move the ratios". B says the sizing must be measured with outline on. Both
    can hold: the ratios survive, but every **absolute** width grows. That includes Ka0s Default's own, and every
    layout today is built unoutlined (§4 R6).
- **C7. Where the reset buttons go.** A puts them on a row under the dropdowns, with reasons (label top-alignment).
  K's standard text says "beside it". **K's text should say "under".**
- **C8. `/xx skin` while disabled and in combat.**
  - **Disabled:** F makes `skin` a feature verb that refuses while disabled and stays out of `LIVE_VERBS`
    (`Slash.lua:124-127`, verified, 13 verbs). K 1f says it "answers while the addon is disabled", and K Q8 says
    yes.
  - **Combat:** F prints the refusal on **every** call, and deliberately not through `O.__combatRefused`, which
    prints once per combat. K says it "prints the refusal `config` prints".
  - **Resolution:** F's design, because it is backed by code. Fix K's text.
- **C9. How strong the sim-marker rule is.** E proposes **SHOULD NOT** on a non-window display. K proposes **MUST
  NOT**, plus "the step panel is the one marker on screen". The step panel can be closed (`SimPanel.lua:266`), so
  K's MUST is broken the moment the player closes it, unless E Q2(i) (`close = false`) is adopted. **Decide the two
  together.**
- **C10. The conditional-sections mechanism.** K's proposed options-ui-§22 says "the library has no `hiddenIf` ...
  issue to be filed". I shows that W22 **`shownWhen` already exists** (`OptionsWidgets.lua:1280-1326`, verified), and
  AuraMaster and PFE use it; only the OR form (W23 `any`) is missing. **The §22 text should name `shownWhen`, not
  invent `hiddenIf`.**
- **C11. Glyph allow-list against what is safe.** K's localization-§7 allow-list leaves out characters that D shows
  every shipped face draws and that are in use: `›` (DpsRace, MultiMeters), `±` (DpsRace ×9), `§`, NBSP (CM, LH,
  PrettyChat), `£ ¥`, and the accented Latin letters. K's MUST would turn those into violations and force the sweep
  that D's option A avoids. **The allow-list should be D's §1 set**, regenerated from the shipped faces (C2).
- **C12. Anchor-width issue shape.** E recommends one issue per addon (9). J recommends one LibKa0s tracker. The
  owner said "File **an** issue", so J.
- **C13. What replaces Expressway and Prototype if not shipped.**
  - B recommends option B: name them by LSM key, do not ship them, and add a per-face fallback.
  - K recommends an OFL look-alike, Overpass or **Barlow** Semi Condensed. Barlow was retired at Media minor 8
    because it "read blurry" (`tests/test_skin_defs.lua:406`).
  - C sized only the requested faces. Under B's option B, a skin draws one of two faces depending on the player, so
    width parity has to hold for both, and C has not measured the stand-ins.
- **C14. Equalizing HUD size.** C wants it now (`HUD_SIZE` and `S.HudFontSize`, across 8 addons and 16 SkinSetup
  lists). K 1c's bullet includes `hud.fontSize`, so it agrees. B and the others say nothing. The risk is in §4 R5.
- **C15. QuickComms `·`.** J says `Dial_Layout.lua:321` "belongs in item 5's sweep". D shows U+00B7 is drawn by
  every face. **No change.**
- **C16. "No addon change is needed".** A says this, and it holds for items 1 and 6 only. Items 13 (B: a profile key
  plus a schema row in 16 addons), 12 (F: a row, a handler and a stub in 16) and 5-HUD (C: 8 addons plus 16 facade
  lists) all change addons. Do not carry A's sentence into the plan.
- **C17. Minor-number collisions.** These are proposed independently:
  - OptionsAppearance 3→4 (A, and B's outline dropdown lands in the same file).
  - OptionsSkinPicker 2→3, claimed by both A and F.
  - SkinDefs 16→17 (B and C).
  - Skin: A says the "Skin major unchanged" and its Q3 rejects a Skin minor 9. B's outline adds
    `GetOutline`/`SetOutline`, `opts.outline`, `media.outline` and a cache-key change in `withOverrides`, so **Skin
    minor 9 happens anyway**, and A Q3 is moot.

  All current minors are verified (APPEARANCE 3, PICKER 2, DEFS 16, DRAG 7, EUI 2, CONTROLS 10). The plan needs
  **one minor per file per release**.
- **C18. Where the HUD carve-out ends.** H and K carve HUD displays out of the v2.86.0 marker MUST. Neither read the
  other two candidates:
  - DpsRace's race HUD carries a TestStrip (`DpsRace/modules/Hud.lua:541`), and ADDONS.md calls it "Show window
    (the race HUD)".
  - DropWatcher's compact chrome has a `TEST` word (`modules/CompactChrome.lua:57`).

  Whether these are "HUD" or "window" decides whether they keep their markers.

## 3. Evidence problems

- **E1 (D).** The Friz coverage is Prototype's (C1). The rest of D checks out: `LootHistory/modules/Browser.lua:591`
  and `BankLedger/modules/Browser.lua:754` both hold `\226\137\136`, and `LootHistory/core/Constants.lua:117` holds
  `MOVE = "\226\135\132"`.
- **E2 (B).** The list of tests that pin a font is incomplete. These LibKa0s pins are missing:
  - `tests/test_skin_paint.lua:632`: `BarStyle().fontKey == "Ka0s Oxanium SemiBold"`. Red.
  - `tests/test_skin_paint.lua:637`: Obsidian's `"Ka0s Inter SemiBold"`. Red.
  - `tests/test_tool_windows_scope.lua:99` and `tests/test_widgets_skin_scope.lua:77`: `OXANIUM =
    "Fonts\\Ka0s Oxanium SemiBold"`. Probably red.
  - `tests/test_skin_paint.lua:519`, `test_skin_paint_controls.lua:188,802` and `test_options_appearance.lua:514`:
    fake-LSM keys. These stay green.

  Before planning, rerun `grep -rln 'Oxanium\|Ka0s Inter\|"Ka0s Fira Sans"' */tests` over all 17 trees. Today it
  returns 27 files.
- **E3 (E).** Root cause 2 is a hypothesis: the measurer's hidden host returns a fallback face. E says so itself
  ("likely, needs an in-client check"). Root cause 1 is certain: `dhRepaint` never re-fits. It is
  `WidgetsDragHandle.lua:235-237`, verified, with `Castbar_Handle.lua:115` measuring once at build. E does not ask
  whether image-43..45 were taken **after a skin switch** or **after a /reload in that skin**. If the strip is
  already truncated after a fresh /reload, cause 1 does not explain it, and the hidden-host change becomes the
  actual fix. **Ask the owner, or add it to the smoke check.**
- **E4 (H).** The glow simulation H cites is at the session scratchpad path `/tmp/claude-1000/.../scratchpad/sim.png`.
  That path does not survive the session. Copy the image into `plan-data/` if the bundle cites it. H also says the
  CAMRY1 account was not checked. I checked it: no `Ka0s Kait` anywhere in CAMRY1's SavedVariables.
- **E5 (C).** The model is fitted to 15 strings at one UI scale, and C says so. C's own Q6 (`/skt widths`, an
  in-client probe) is the right check before the sizes are frozen. It also means the guard test's `WIDTH` table is
  only as good as the build in C2.
- **E6 (G).** The template geometry is from memory. The fix sets an explicit size and anchor, so it does not depend on
  that, but G's Risk 1 (`SetMinimizedLook` re-showing art) can only be checked in the client.
- **E7 (K).** "DpsRace Hud and DropWatcher CompactChrome (grep hits, not yet read)" is unfinished, as C18 shows.

## 4. Cross-cutting risks the reports miss

- **R1. Run precondition.** The addon finalize is unfinished (§0). Nothing in the inventories accounts for it.
- **R2. One re-vendor carries every stub change.**
  - F's `O.SkinVerb` makes `Kit.assertSurfaceParity` red until each Options stub gains it.
  - C's `S.HudFontSize` must be added to each SkinSetup noop facade list, and each `test_skinsetup.lua` pins those
    lists.
  - B's Skin `GetOutline`/`SetOutline` may need host facade or stub parity too. No report checked this.

  All three land in the same tag, so each addon's re-vendor commit has to add all of them at once, or that addon's
  suite goes red in between.
- **R3. Payload and licensing at scale.** The fonts ship in full in 16 repos (§0). Under option A, a "Do not
  distribute" Expressway goes out 16 times on CurseForge, and every addon README's credits change (B §7). A
  font-prune tool or declaration, like the icons have, would cut the exposure, but nobody proposes one.
- **R4. No test baselines.** No report records the current green-gate totals (`lua tests/run.lua` plus `ka0s-bounded
  luacheck .`) per repo. `checkpoints.tsv` needs before and after totals. **Add an M0 step that captures them for
  all 17 repos.**
- **R5. The skin face already replaces the owner's own picks, and HUD scaling would compound it.**
  - **AuraMaster** (H): `fontFromSkin = true` on every container (MigrateV13). The 137 stored `"Ka0s Prototype"`
    picks and the 3 `"Ka0s Kait"` picks all draw Ka0s Default's Oxanium today. Item 3 (Prototype) brings back the
    look of the 137 by coincidence. H does not mention this.
  - **KickCD has the same problem, and H misses it.** The owner's target label stores `font = "Ka0s Kait"`
    (`WTF/.../ADD1KTED2KA0S/SavedVariables/KickCD.lua:1051`). `label.style.fontFromSkin` defaults to true
    (`KickCD/defaults/Profile.lua:194,331`), and `HUD_SKIN_COMPANIONS` forces it on (`core/Database_Migrations.lua:348-357`).
    So that label draws the skin face too. Tell the owner along with H's AuraMaster finding.
  - **C's `S.HudFontSize` scales only when fromSkin is on.** That is now true on essentially every HUD element, so it
    would rescale sizes the owner tuned by hand: AuraMaster's 36 pt text becomes about 39 under Obsidian's 13/12.
    It would also move every AuraMaster and KickCD layout and anchor width, which item 11 then has to re-check.
    **Recommendation:** do not ship HUD size equalization in this run. File it as an issue, or make it a separate
    opt-in (a size companion), because "Use the skin's font" governs the face, not the size.
- **R6. Default outline everywhere changes every layout's absolute width.** Every existing profile gets outlined
  window text on update (*All text* is the default), Ka0s Default included. Layouts and the drag-strip fits were
  built unoutlined. The smoke must re-check LootHistory (image-17's truncation set) under Ka0s Default **with outline
  on**, not only across skins.
- **R7. The 1500-line cap.** `LibKa0s/LibKa0s/OptionsWidgets.lua` is **1447 lines**, and I's W23 `any` form goes
  there, leaving 53 lines of headroom. The file probably has to be split first. Others are below the cap but
  growing: `Skin.lua` 1081, `SkinDefs.lua` 1005 and `test_options_skin_picker.lua` 1064 (F already adds a new
  suite). CCN 15 is at risk in `withOverrides` (B), `euiCall` (G) and `dhRepaint` (E), which all gain branches.
- **R8. Sequencing that no single report owns.** The order is:
  1. The license and build decision (B, C2).
  2. The faces (B).
  3. The outline semantics (13).
  4. The re-measured sizes (C).
  5. The drag-strip re-fit (E).
  6. The glyph allow-list and the standard text, computed from the shipped faces (D, K).
  7. The anchor-width issue, filed only after the font freeze (owner).

  G (PGFE/EUI), H, I, J and F are independent of this chain.
- **R9. Stale galleries.** The skin screenshots in `media/screenshots/skins/vN` (round-5 convention) and
  `tools/skin_gallery.py` go stale when the faces change. B covers the script's Inter dependency but no new gallery
  version.
- **R10. GitHub write volume.** J counts 6 writes. The reports also propose these:
  - the LibKa0s Toast minor 2 issue (I Q7);
  - an AuraMaster glow-scaling issue (H Q3);
  - a PGFE TitleBand issue (G Q5);
  - a real-Friz retune issue (C Q4);
  - a `fontFlags` FromSkin companion issue (B Q5);
  - a HUD size issue (R5).

  That is up to 12 writes. Space them out, per the standing rule.
- **R11. A readability note for the owner.** In image-30 the button reads "Copy to every **KaOs** addon". Prototype's
  zero has no slash or dot, so under the new Ka0s Default the brand reads as "KaOs" everywhere. It is a matter of
  taste, but it is worth a line when the owner confirms Prototype.

## 5. Spot-check log

| Report | Claim | Result |
|---|---|---|
| A | `choose()` calls SetChoice, then `spec.set(source, skin)`, with no media (`OptionsAppearance.lua:330-338`) | Confirmed |
| A | The Scope toggle uses `W_CHOICE` (`:394`) | Confirmed |
| A | The test pins persistence (`test_options_appearance.lua:691-705`) | Confirmed |
| B | Ka0s Default `font.outline ""`, `hud.outline "OUTLINE"` (`SkinDefs.lua:236,337`) | Confirmed |
| B | The license test requires the OFL text for every face (`test_media.lua:611-629`) | Confirmed |
| B | `QuickComms/core/SkinSetup.lua:160` names Oxanium | Confirmed |
| B | The list of tests that pin font names is complete | **Incomplete** (E2) |
| C | FRIZQT__.TTF is Prototype (md5) | Confirmed: 0483b4ee… ×6 files |
| C | Obsidian `fs = 12, titleSize = 14` at `SkinDefs.lua:611`; reference 12/14 at `:279` | Confirmed |
| C | Measured Fira is the pack's copy | Confirmed (`font_metrics.py:31`), which conflicts with B's build (C2) |
| D | The footer `≈` in LH `Browser.lua:591` and BL `:754`; `MOVE = ⇄` at LH `Constants.lua:117` | Confirmed |
| D | LibKa0s display text holds no unsafe glyph | Confirmed (escapes found are only `—`, `…` and `×`) |
| D | Friz coverage | **Wrong** (C1) |
| E | The measurer host is hidden (`WidgetsDragHandle.lua:237`); KickCD measures once (`Castbar_Handle.lua:115`) | Confirmed |
| E | The sim-strip hosts are KC, BL, LH, MM and DW | Confirmed (DW through the `NS.MakeTestStrip(..., "sim")` wrapper) |
| E | The DragHandle consumers are AT, AM, CM, KC, QC and SkT | Confirmed |
| F | `LIVE_VERBS` holds 13 verbs, without `skin` (`Slash.lua:124-127`) | Confirmed |
| G | PGFE passes `"up"`/`"down"` (`Panel.lua:783-787`); PageButton is a native EUI name (`SkinEUI.lua:84-87`) | Confirmed |
| H | `ApplyMarker` is at `Preview.lua:270` and called at `Container.lua:928`; `MigrateV13` exists | Confirmed |
| H | The SavedVariables hold `Ka0s Kait` (3) and `fontFromSkin = true` | Confirmed (137 `Ka0s Prototype` too) |
| I | `SIT_COL` and the widths (`PageEditors.lua:119-120`); `glowMain` #FFF468, off-spec already #3FC7EB | Confirmed |
| I | `shownWhen` W22 exists (`OptionsWidgets.lua:1280+`) | Confirmed, which contradicts K (C10) |
| J | `TEST_COUNTS` (`Surfaces.lua:41`); `DEFAULT_ICON` is the question mark (`Dial_Render.lua:47`) | Confirmed |
| K | The reserved list at `slash-commands.md:40`; the marker MUST at `preview-mode.md:11`; standard v2.92.0 | Confirmed |

## 6. Consolidated decisions for the lead (my recommendation in bold)

1. **The outline (13) against the stored `fontFlags`.** Ask the owner whether *Off* must remove the HUD outlines that
   addons store. **Recommendation: ask.** If yes, the run adds a `fontFlags` FromSkin companion. That is a
   FontGroup-wide change, and it touches profiles. If no, the Skin tab says that HUD elements keep their own flags.
2. **The license path (2-4): A, B or C.** **Owner, explicitly. Recommendation: Fira ships; Expressway does not ship
   while its own notice says "Do not distribute"; Prototype ships only with its terms file, on a recorded ruling.**
   Everything in C, D and K is recomputed for the faces that actually ship.
3. **The Fira build.** **Pick before any measuring.** Use the pack's 4.301 for exact parity with the owner's client,
   or google 4.203 for provenance. Re-measure either way.
4. **The Forever titles and HUD.** **SemiBold for the HUD, Medium for body and titles.**
5. **HUD size equalization.** **Defer it to an issue (R5).**
6. **`/xx skin` disabled and combat behavior.** **F's design.**
7. **The sim marker strength.** **MUST NOT on a HUD display, with KickCD's step panel `close = false`** (C9).
8. **The HUD-versus-window boundary for the marker carve-out.** **Read DpsRace `Hud.lua:541` and DropWatcher
   `CompactChrome.lua:57` first, then rule.** The ADDONS.md "Show window" entries suggest they are windows and keep
   their markers.
9. **The allow-list.** **D's safe set from the shipped faces**, not K's shorter list.
10. **Plan prerequisites.** Finish the addon finalize. Capture the test baselines for 17 repos (M0). Split
    `OptionsWidgets.lua` before W23. Assign each file one minor.
