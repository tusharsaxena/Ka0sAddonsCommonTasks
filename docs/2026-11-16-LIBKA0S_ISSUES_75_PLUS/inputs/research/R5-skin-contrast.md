# R5-skin-contrast — LibKa0s #82 (hot vs rest/heading, list.hover) and #84 (Ka0s Default row stripe)

Read-only research against LibKa0s master `9bc9cc51` (v1.104.0). The numbers come from loading the
real payload through the repo's own loader (`tests/_kit/loader.lua` + `tests/wow_mock.lua`) and
calling `Skin:ResolveSkin(key)` for all nine skins. The scratch scripts are in
`/tmp/claude-1000/-mnt-d-Profile-Users-Tushar-Documents-GIT-Ka0sAddonsCommonTasks/863375de-78c0-419b-a2d4-628965f6eb81/scratchpad/r5/`
(`dump.lua`, `lab.lua`, `fix.lua`). Run them from the LibKa0s root as
`lua <scratch>/r5/lab.lua <scratch>/r5/fix.lua`.

## 1. Where the tokens live

| Token | Ka0s Default | The eight other skins |
|---|---|---|
| `icon.tint` (a mark at rest) | `GRAY {0.7,0.7,0.72}`, `LibKa0s/SkinDefs.lua:418` | the mockup's `muted`, through `MOCK_MAP` (`SkinDefsOthers.lua:119`) |
| `icon.hot` (a mark under the pointer) | `WHITE`, `SkinDefs.lua:418` | the mockup's `accent`, through `MOCK_MAP` (`SkinDefsOthers.lua:120-121`); overridden in the extras by Glass `#FFFFFF` (:538), Ember `#FFB45A` (:637) and Midnight `#F6D27A` (:751) |
| `text.heading` | `GOLD {1,.82,0}`, `SkinDefs.lua:334` | `titleColor`, then `headColor` (MOCK_MAP rows); Azeroth's comes from its extras |
| `list.stripe` | `{1,1,1,0.03}`, `SkinDefs.lua:410` | the mockup's `rowAlt` (:414, :461, :510, :558, :613, :668, :726, :775) |
| `list.hover` | `{1,.82,0,0.10}`, `SkinDefs.lua:411` | `TEXT_WASH` (`SkinDefsOthers.lua:161-162`): the body text at .15. High Contrast is the exception at yellow .20 (:582) |
| `list.sel` | `{1,.82,0,0.18}` | the mockup's `rowSel` |

**How a row is drawn.** `S.ListRow` (`SkinPaintControls.lua:1047-1075`) lays three color-texture
regions over the row: `stripe`, `hover` and `sel` (`rowWash`, :1050). Each is a `SetColorTexture`
at the token's alpha, composited over whatever sits under the row. That is the window's `win.bg`,
which is itself translucent for Ka0s Default (.92) and Glass (.88), and which is a gradient for
Midnight and Forever. A hovered striped row draws hover on top of stripe. The suite already
composites the same way (`over(t["list.stripe"], over(t["win.bg"], BLACK))`,
`tests/test_skin_defs.lua:705-719`), so I measure that way and take both gradient stops into account.

**How a mark goes hot.** `S.Mark` (`SkinPaintExtras.lua:388-408`) tints with `opts.token or
"icon.tint"`. The host chooses the hot state: Skill Master's `modules/Chrome.lua:112` does
`Mark(b.icon, hot and { token = "icon.hot" } or rest(b))`, where `rest(b)` can be `text.heading`
(:185). Library sites that do the same are the step arrows (`SkinPaintControls.lua:523`, rest
`icon.arrow` = the accent, hot `icon.hot`), OptionsIdList's help mark (`OptionsIdList.lua:576`),
the footer marks (`Widgets.lua:776-780`) and the drag handle's help (`WidgetsDragHandle.lua:260-261`).

## 2. Today's numbers (all nine skins)

ΔL* is the CIE L* difference, which measures lightness alone and is what the issue asks for. CR is the
WCAG contrast ratio. ΔE is CIE76, shown only to make a point about hue. Stripe, hover and sel are
composited over the window as described above, and the minimum over both gradient stops is shown.

| skin | hot–rest ΔL* (CR, ΔE) | hot–heading ΔL* (ΔE) | stripe ΔL* (max channel) | hover ΔL* | hover-plain vs stripe ΔL* | hovered-stripe vs stripe ΔL* |
|---|---|---|---|---|---|---|
| ka0s | 27.1 (2.10, 27) | 14.5 (87) | **3.0 (2.8%)** | **9.0** | 6.0 | 9.1 |
| obsidian | **7.4** (1.26, 41) | 23.9 (50) | 9.5 (8.6%) | 15.0 | 5.4 | 14.0 |
| azeroth | **9.2** (1.33, 31) | **0.0** (0) | 9.8 (8.3%) | 13.2 | 3.4 | 11.1 |
| glass | 17.0 (1.56, 18) | **0.0** (0) | 10.3 (8.4%) | 16.1 | 5.8 | 13.8 |
| contrast | **1.5** (1.04, 90) | **0.0** (0) | 13.2 (13.3%) | 18.6 | 5.4 | 17.4 |
| ember | **7.5** (1.25, 42) | **0.0** (0) | 10.1 (8.7%) | 15.3 | 5.2 | 13.4 |
| wow | **10.7** (1.36, 87) | **0.0** (0) | 9.8 (8.1%) | 15.9 | 6.2 | 13.7 |
| midnight | **13.0** (1.46, 62) | **0.0** (0) | 9.8 (8.2%) | 14.9 | 5.2 | 12.8 |
| forever | **3.4** (1.11, 24) | **8.2** (41) | 9.9 (8.9%) | 14.7 | 4.8 | 12.6 |

What this shows:

- **#82 is real, and Forever is the worst case.** Forever's hot `#C9A07A` (L* 68.7) sits 3.4 L* from its rest `#A39E97` (65.3). Only High Contrast is closer (1.5), and its yellow-versus-gray hue split carries it (ΔE 90).
- **ΔE76 is no use as the yardstick.** Forever's heading-to-hot pair scores ΔE 41, but the owner saw it "nearly disappear". CIE76 overweights chroma in the yellows. Lightness is the right axis, as the issue says.
- **Six skins have `icon.hot == text.heading`, ΔL* 0:** Azeroth, Glass, High Contrast, Ember, WoW Default and Midnight. On those skins, a host mark resting at `text.heading` (Skill Master's block header) gets no visible hover. This is wider than #82 reported.
- **`list.hover` on Forever is fine.** At ΔL* 14.7 it is in line with the family (13.2–16.1). The faint hover is Ka0s Default's (9.0).
- **#84 is real.** Ka0s Default's stripe is ΔL* 3.0 against ~10 for every other skin. The suite exempts it on purpose (`tests/test_skin_defs.lua:704-710`, "Ka0s Default's own 3% stays").
- **The library fix does not reach Combat Trail, where #84 was seen.** CT has its own owner token, `ct.list.stripe = { default = {1,1,1,0.025}, follow = "list.stripe" }` (CombatTrail `main:core/SkinSetup.lua:248`). `SkinOwnerTokens.lua:162-166` answers the `default` under Ka0s Default, so a stripe that is 2.5% under Ka0s Default stays 2.5% whatever the library's `list.stripe` says. `ct.list.hover` (white .04, :249) is fainter still. DpsRace has the same pair (`dr.list.stripe` .025 and `dr.list.hover` .04, `core/SkinSetup.lua:233-234`). MultiMeters' `mm.rowStripe` is .05 (:132).

## 3. Proposed values (computed, every skin passes §4)

| skin | change | after: hot–rest | hot–heading | notes |
|---|---|---|---|---|
| ka0s | `list.stripe` {1,1,1,**0.08**}, `list.hover` gold **0.16**, `list.sel` gold **0.26** | 27.1 | 14.5 | stripe ΔL* 9.0 (7.6% channel) matches the family. hover 14.6, hover-plain vs stripe 5.6, hovered-stripe 12.9, sel 23.6 (hover to sel 9 L*). A lighter alternative is .07 / .14 / .24 (stripe 7.8, hover 12.7, sel 21.8) |
| obsidian | `icon.hot` **#A6DAFF** (the accent, lifted) | 20.5 | 10.8 | keeps the blue hue |
| azeroth | `icon.hot` **#FFE7A6** (pale gold) | 25.1 | 15.9 | |
| glass | `icon.tint` **#9AA2B3**, `icon.hot` **#D8CCFF** (pale lilac) | 18.0 | 15.5 | the heading is pure white, so hot cannot go above it. Rest drops instead, and still reads at CR 7.2 on the window. `icon.grip` and `list.ghostIcon` FOLLOW `icon.tint` and move too |
| contrast | `icon.tint` **#A0A0A0**, `icon.hot` **#FFFFFF** | 34.1 | **9.3** | yellow cannot get lighter (L* 90.7). Needs a named exemption from the hot–heading floor (white against yellow, ΔE 91), or a floor of 9 |
| ember | `icon.hot` **#FFE0B8** (pale amber) | 19.5 | 12.0 | |
| wow | `icon.hot` **#FFFFFF** | 25.2 | 14.6 | the client's own hovered icon is white |
| midnight | `icon.hot` **#FFFFFF** | 27.4 | 14.5 | |
| forever | `icon.hot` **#FFFFFF** (the issue's own suggestion) | 34.7 | 23.0 | Forever's titles and body are already white |

Every rest color still reads on its own window at CR ≥ 5.65 (the lowest is Forever, unchanged) and
every hot color at CR ≥ 12.3. The eight non-Ka0s stripe and hover values do not move. Where a hot
value is set, it lands in that skin's `extra` table, as Glass, Ember and Midnight already do. `MOCK_MAP` stays as it is.

## 4. The contrast check: thresholds that every skin passes after §3

Put it in **`tests/test_skin_defs.lua`**, the library's own per-skin legibility suite, next to the
stripe and hover cases at :698-735. The skin-values kit (`testkit/skin_values.lua`) is a
**source scanner** for typed literals in host code, and it never resolves a skin, so it is the
wrong home for a token-against-token check. Measure in CIE L*, composite every wash over `win.bg`
over black, and check both stops of a gradient window.

| Case | Rule | Today's failures | After §3 (minimum) |
|---|---|---|---|
| hot vs rest | ΔL*(`icon.hot`, `icon.tint`) ≥ **15** | obsidian, azeroth, contrast, ember, wow, midnight, forever | 18.0 (glass) |
| hot vs heading | ΔL*(`icon.hot`, `text.heading`) ≥ **10**, High Contrast named as signed off (or the floor at 9) | azeroth, glass, contrast, ember, wow, midnight, forever | 10.8 (obsidian), contrast 9.3 |
| marks read at rest | CR(`icon.tint`, window) ≥ 3 | none | 5.65 |
| stripe shows | ΔL*(stripe over window, window) ≥ **6**, **Ka0s Default included**. The 8% channel floor `STRIPE_STEP` stays for the eight | ka0s | 9.0 (ka0s) |
| hover shows | ΔL*(hover over window, window) ≥ **12** | ka0s | 13.2 (azeroth) |
| hover vs stripe | ΔL*(hover-plain, stripe) ≥ **3**, Ka0s Default included (today it is held at 3% channel for the eight only) | none | 3.4 (azeroth) |
| hover vs sel (Ka0s Default, one hue) | ΔL*(sel, hover) ≥ **6** | (today 7.4, passes) | 9.0 |

Implementation: one `lstar(c)` helper beside the existing `luminance` (:38-49). Each case names the
failure it would turn red under, in the file's own style. The Ka0s exemption at :710 goes.

Optional and deferred to adoption: a small kit helper (`testkit/skin_contrast.lua`, kit revision +1)
that runs the same stripe, hover and hot floors over a **host's owner tokens** under every skin. It
would catch `ct.list.stripe` .025 and `dr.list.stripe` .025 under Ka0s Default, which the library
suite cannot see.

## 5. Minors, tests and doc ripple

- **LibStub minors:** `SkinDefs.lua` DEFS_MINOR **27 → 28** (Ka0s Default stripe, hover and sel), and `SkinDefsOthers.lua` OTHERS_MINOR **9 → 10** (seven `icon.hot` and two `icon.tint` values). The `Skin.lua` shell stays at 18, because no schema token is added. Each gets a header history line.
- **LibKa0s tests that move:** `tests/test_skin.lua:295-296` pins Ka0s Default's `list.stripe` .03 and `list.hover` .10. It must be updated, and `list.sel` should be pinned there too if it is not already. `tests/test_skin_defs.lua:704-719` loses the Ka0s exemption, and the new cases in §4 are added. The rest read tokens live: `test_skin_paint_controls.lua:712-714`, `test_widgets_skin.lua:326`, `test_skin_step_arrows.lua:99` and `test_options_skin.lua:407`.
- **Docs:** a new `docs/api/Skin/version-18.1.28.10.…-docs.md`. Its Ka0s Default token table (the old docs carry it at ~:692-702) and its "eight skins" table (~:1485-1498 in the older doc: `list.stripe`, `list.hover`, `icon.hot` rows) take the new values, plus CHANGELOG. The member manifest is unchanged (no API surface).
- **Revendor breakages, which are part of "fix what arises":** each host's `test_surface_parity` holds its `NS.SKIN_FALLBACK` copy to the library's resolved Ka0s Default (LootHistory `tests/test_surface_parity.lua:383-405`). These copies must move in the same revendor commit, or that repo goes red:
  - LootHistory `core/SkinSetup.lua:137-138` (`list.stripe`, `list.hover`)
  - BankLedger `core/SkinSetup.lua:172-173`
  - DropWatcher `master:core/SkinSetup.lua:185` (`list.stripe`). Another session owns DW's feature branch, so coordinate.

  No host fallback copies `icon.hot`, `icon.tint` or `list.sel` (grep over every sibling). Other hosts' skin tests should be re-run and checked. DropWatcher's `tests/test_skin_chrome.lua`, Skill Master's `tests/test_round2_icons.lua` and `tests/test_round8.lua`, and OutfitterReborn's `tests/test_skinsetup.lua` mention `icon.hot`, and may pin a resolved per-skin value.
- **Semantic ripple (adoption, not revendor):**
  - OutfitterReborn `of.bar.worn = { default = GOLD, follow = "icon.hot" }` (`core/SkinSetup.lua:139`, drawn at `modules/Bar_Buttons.lua:208,287`). Under WoW, Midnight and Forever, the worn mark and edge would turn **white** instead of the accent or gold. Recommend that OR follows `text.accent` instead.
  - CT and DpsRace `*.list.stripe` and `*.list.hover` defaults (.025 and .04) need raising to the new Ka0s values, or #84's reported symptom stays.
  - MultiMeters `mm.rowStripe` .05 is borderline.
- **Standard:** `skinning.md:82` already has the precedent "an enabled control reads as enabled in every skin (MUST) ... the library's suite guards it". A sibling bullet, "a hover or hot state and a row stripe read in every skin (MUST), guarded by the library's suite", is a small standard minor. That is optional, and the owner decides.
- **Skin Tester** (`../LibKa0sSkinTester`, master): `modules/ShowroomLists.lua:36-42` already draws the ListRow normal, stripe, hover and selected states, which makes it the smoke surface for #84. `modules/ShowroomOverlays.lua:112-123` shows `Mark` at tint and `sem.good` only, with **no hot sample**. Recommend adding "Mark rest / hot / at text.heading + hot" to the showroom, as a tester change in the adoption phase or as part of this item if the owner wants in-game smoke of #82 in one place.
- **Screenshots:** `tools/skin_gallery.py` reads only the skin labels and the four picker swatches from SkinDefs (:67-73). None of the changed tokens is a swatch, so the tool needs no change. Existing shots (`LibKa0s/media/screenshots/skins/v1,v2`, `LootHistory/media/screenshots/skins`) do not capture hover or hot. The only stale pixels would be Ka0s Default table stripes, so a re-shoot is optional, as a vN+1 run after smoke.

## 6. Risks

- **Changing seven skins' `icon.hot` is a visible design change.** Every hot mark, step arrow, ID-list help mark, dropdown confirm tick and drag-handle help moves: WoW, Midnight and Forever go to white, and the others to a paler accent. The owner signed off these skins' looks over five smoke rounds, so smoke is needed per skin.
- **Ka0s Default's selection gets heavier** (gold .18 → .26), and so does every host row selection drawn through `list.sel` under Ka0s Default. Hosts with their own `default`, such as CT's `ct.list.sel` GOLD .10, do not move.
- **Ka0s Default's window is .92 alpha.** A bright game world behind it lifts the base to about L* 13 and shrinks the stripe step a little. The proposed .08 keeps ΔL* above 6 even then.
- **The `TEXT_WASH` rows stay.** `test_skin_defs.lua:606-619` pins hover = body text at .15 for the eight, and nothing here moves that.

## 7. Decisions for the owner (recommended answer first)

1. **D-1: the scope of #82.** Fix only Forever, or every skin that fails? **Recommend every failing skin** (§3), with the suite floors in §4. The issue says "Other skins may have the same gap", and the numbers say seven do.
2. **D-2: is hot vs heading a library invariant?** **Recommend yes, at ΔL* ≥ 10.** This forces `icon.hot ≠ text.heading` in six skins. The alternative is to leave it to hosts, which would have Skill Master pass a different hot token for heading-rest marks.
3. **D-3: High Contrast** cannot reach 10 (yellow is already near the lightness ceiling). **Recommend a named exemption**, documented like the existing Ember and Midnight band sign-off, with HC rest dimmed to #A0A0A0 and hot set to white.
4. **D-4: Forever's hot.** **Recommend #FFFFFF.** A brighter gold such as #FFE7A6 is the alternative.
5. **D-5: Ka0s Default's rows.** **Recommend stripe .08, hover gold .16, sel gold .26.** The lighter alternative is .07 / .14 / .24. Either way, drop the Ka0s exemption from the stripe test.
6. **D-6: the Combat Trail and DpsRace owner defaults** (.025 and .04), which keep #84 visible in CT, where it was reported. **Recommend raising them in the adoption phase**, to the library's new Ka0s values, with #84 left open until then. If the owner wants #84 closed in this run, the alternative is a two-line fix per repo during revendor. CT is not in ADDONS.md, so confirm it is in scope.
7. **D-7: OutfitterReborn's `of.bar.worn` follows `icon.hot`.** **Recommend repointing it to `text.accent`** in the revendor fix-ups for OR, because otherwise its worn mark turns white under three skins. This is a change in meaning rather than a test failure.
8. **D-8: a standard bullet in skinning-§4.** **Recommend yes**, as a small minor, mirroring the "enabled control reads as enabled" rule.
9. **D-9: a hot-state sample in the Skin Tester.** **Recommend yes**, as one showroom row, so #82 can be smoked in one window across all nine skins.

## 8. Test plan

- **Red first:** add the §4 cases to `tests/test_skin_defs.lua` and confirm they fail on today's values with the exact list in the §4 table. Then apply the §3 values and confirm they pass. Then update the pins at `tests/test_skin.lua:295-296`.
- **Gate:** run `lua tests/run.lua` and `~/.claude/dev-copilot/bin/ka0s-bounded luacheck .` in LibKa0s, and confirm `diff -r testkit tests/_kit` is empty.
- **Revendor:** every host's battery. Expect `test_surface_parity` red in LootHistory, BankLedger and DropWatcher until their fallback copies move.
- **Smoke (owner):** in the Skin Tester, for each of the nine skins: the ListRow stripe, hover and selected rows are told apart at a glance; a mark goes hot visibly from `icon.tint` and from `text.heading` (Skill Master's block header under Forever). Then Combat Trail's Fights tab under Ka0s Default, once D-6 lands.
