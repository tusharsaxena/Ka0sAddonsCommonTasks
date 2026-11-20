# GAP list: fix items

Every GAP row in `tables/` appears below as a fix item, or as part of one. The library comes first, because a widget
that takes the token by itself fixes every host at once. The addons follow in roster order.

- Library items are `SD-LK-97.n`. They land under SD-LK-97, except SD-LK-97.18 and SD-LK-97.19, which are the test-kit
  work of SD-LK-GUARD.
- Addon items are `SD-SK-<abbr>.n`, landing under that addon's `SD-SK-<abbr>` item in
  `docs/2026-11-20-LIBKA0S_94_97_99_100/plan-data/items.tsv`.
- Evidence paths are relative to the repo that owns the item. In an addon item, `libs/LibKa0s/...` is the vendored
  v1.107.0 copy.
- Each addon item that adds a `FromSkin` companion also owes its key in the addon's `Skin.FollowOnce` step (skinning-§6)
  and a schema row, and each item that touches a painted surface owes its `Kit.skinSwitch` declaration. Those are said
  once here rather than repeated in every row.

Counts: 83 GAP rows became 19 library items and 56 addon items. Seven addon GAP rows moved to the library outright
(AuraMaster 1, CombatTrail 1, LibKa0sSkinTester 1, OutfitterReborn 3, QuickComms 1), and six more were split, with a
library part here and an addon part below (BankLedger, CombatTrail, LootHistory, MultiMeters and two SkillMaster rows).
Six pairs of addon rows were merged because one fix closes both (BankLedger, MultiMeters, OutfitterReborn twice,
QuickComms, SkillMaster), and Combat Trail's call-out row merged into the library's Callout outline row. Each merge is
named in its item.

## Library (LibKa0s)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-LK-97.1 | Owner-less library widget built inside an owned window | Widgets.lua:66-76; WidgetsBar.lua:110; Charts.lua:413; Callout.lua:491-499; WaypointArrow.lua:356-360; Toast.lua:327 | A headless kit check, or a debug-mode warning, for a library widget built under a painted ancestor with no owner. Optionally infer the owner from the nearest painted ancestor | Each concrete omission is the host's (CombatTrail's ChartsHost is the live case, SD-SK-CT.1) |
| SD-LK-97.2 | Bar widget border ignores the skin's `bar.borderStyle` | WidgetsBar.lua:81 `borderFromSkin = false`; :252-258 | Default `borderFromSkin = true` (R-2). `borderShow = false` stays the no-border default under None. Hosts that resolve the border themselves (SkillMaster modules/BarStyle.lua:127) keep passing false | Fixes RangeMaster's indicator bar (modules/Elements_Indicator.lua:58), which the RangeMaster table marks OK on the fill |
| SD-LK-97.3 | Bar widget draws no gloss under Glass | WidgetsBar.lua:527 (fill is a Texture, no gloss); SkinPaintHud.lua:47-50 (BarGloss takes only a StatusBar); SkinDefsOthers.lua:570, :604 | A Texture-target gloss in the facade, or BarGloss accepting the Bar's fill Texture, with `style.glossFromSkin` (default true) and a repaint on switch | Extending the same gloss to Charts bars waits on U-4 |
| SD-LK-97.4 | Context-menu submenu arrow keeps Ka0s Default gray | WidgetsDropdown.lua:161-169 (set once), :244-253 (never retinted) | Tint `b.__sub` from the menu palette in paintRowMarks on every paint, as `dd.arrow` is (SkinPaintControls.lua:429-444); give the gray back for an owner-less open | |
| SD-LK-97.5 | DragHandle host-drawn edge (`spec.edge`) not repainted on switch (latent) | WidgetsDragHandle.lua:657, :696-705 | Keep `spec.edge` and re-call it with the new `pal.edge` in dhRepaint | Low priority: no consumer passes `spec.edge` today |
| SD-LK-97.6 | FontGroup face follows the skin only on opt-in | OptionsCompose.lua:40-42, :693-697, :373, :837 | Emit the "Use the skin's font" companion, default true, unless the host passes `fromSkin = false` (R-2) | Lands with each host drawing through `S.Resolve`. Hosts that compose without it today: RangeMaster (SD-SK-RM.1), PanelMaster (held by U-23) |
| SD-LK-97.7 | FontGroup font flags default `"OUTLINE"` | OptionsCompose.lua:833, :855 | `flagsFromSkin` on by default, host opt-out (skinning-§6: From skin is the default for every element) | Pairs with SD-SK-RM.1, which also moves RangeMaster's stored default |
| SD-LK-97.8 | Composer color and shadow rows carry no FromSkin companion (FontGroup `fontColor`/`fontShadow`, BarGroup `barColor`, BorderGroup `borderColor`, ColorPair) | OptionsCompose.lua:766-779, :850-860, :898, :928 | The composers emit `<color key>FromSkin` (and `fontShadowFromSkin`) bool rows defaulting true, governing the swatch and shadow rows, behind the same opt-out | Every host hand-writes these today. RangeMaster's missing companions (SD-SK-RM.2 to RM.4) get their rows from this once it lands |
| SD-LK-97.9 | BarGroup texture and BorderGroup border style follow the skin only on opt-in | OptionsCompose.lua:891, :921, :693-697 | Emit the companion (default true) unless the host opts out (R-2) | The Combat Trail failure shape. Pairs with SD-SK-RM.5 |
| SD-LK-97.10 | Callout look defaults: outline `THICKOUTLINE`, face Ka0s Oxanium SemiBold (not Skin font), `glowColorFromSkin = false`, black shadow | Callout.lua:158-159, :160, :172-183, :520, :524-527, :652-653 | Default `font = lib.FONT_SKIN`, an "@skin" outline value through S.FontFlags, `glowColorFromSkin = true`, a shadow companion through S.HudShadow; a one-time move only for stored values still equal to the old defaults, through a FollowOnce key list the hosts call | **Depends on U-1.** Merges the LibKa0s outline GAP row with Combat Trail's "Race call-out look" GAP row (CombatTrail table, GAP (missed)), which moves here. Combat Trail then calls the key list from its own FollowOnce step |
| SD-LK-97.11 | Callout "number" kind color is a white literal | Callout.lua:177, :360-366, :642-643 | A FromSkin companion (default true) reading `hud.text` for "number", the swatch live when off | The other kinds wait on U-2 |
| SD-LK-97.12 | Callout text face, size and shadow set by direct `SetFont`/`SetShadow*` | Callout.lua:530-532, :648-657 | Route the text and the halo's face through the owner facade's HudFont and HudFontSize; keep the direct path for the owner-less case | Independent of U-1: whatever the defaults, a 12.0.7 client draws no runtime FontString shadow (skinning-§6) |
| SD-LK-97.13 | WaypointArrow distance and name text color has no skin companion | WaypointArrow.lua:124, :129-131, :628-637 | `fontColorFromSkin` (default true) in DEFAULTS and SETTINGS reading `facade.HudTextColor()`, class color ahead of it, swatch live when off | Merges SkillMaster's arrow color GAP (library part). SkillMaster then adds its path (SD-SK-SM.2) |
| SD-LK-97.14 | WaypointArrow text shadow hard-codes `shadowFromSkin = false` | WaypointArrow.lua:657 | `fontShadowFromSkin` (default true) in DEFAULTS and SETTINGS, passed to HudFont in place of the literal | Merges SkillMaster's arrow shadow GAP (library part). SkillMaster then adds its path (SD-SK-SM.3) |
| SD-LK-97.15 | Charts falls back to the host's flat `fill` for bars of data | Charts.lua:364 `ctx.barFill = host.barFill or host.fill or plainFill` | Bars of data paint through S.BarTexture when the host passes no `barFill`, even when it passes `fill`; document `barFill` as the bar seam | From the library part of Combat Trail's Insights GAP. Hardening only: Combat Trail also passes no owner, so SD-SK-CT.1 is still needed |
| SD-LK-97.16 | `lib.ApplySkin` with a host skin never draws the skin's gradient or background art | Core.lua:242-249 (facade only when `skin == nil`); SkinPaint.lua:962-975 shellBands; SkinDefsOthers.lua:337-342, :770 | Let `lib.ApplySkin(frame, hostSkin, owner)`, or a Shell option that keeps a host edge, draw the skin's gradient and art bands when the host's background is the skin's own | Moves QuickComms' pad-window GAP here; it closes that row. The addon fallback (Shell under the pad edge in `R.ApplyWindowLook`) is needed only if this is declined |
| SD-LK-97.17 | `ApplyBarFill` on a texture-less StatusBar sets only a color, so the bar is invisible | SkinPaintControls.lua:986-995; OutfitterReborn modules/Dialog_Progress.lua:37-42 | ApplyBarFill also applies `bar.texture` (recorded, as S.BarTexture does, SkinPaintExtras.lua:780-788) when the StatusBar has no texture | Moves OutfitterReborn's progress-fill GAP here; it closes that row. The progress bar's background stays an addon item (SD-SK-OR.1) |
| SD-LK-97.18 | Kit skin-switch guard cannot see a texture-only regression (SD-LK-GUARD) | testkit/skin_switch.lua:78, :241-259 (any one setter passes a surface); tests/fixture_skin_paint.lua:42-52 (no `lsm`, so BarTexture paints WHITE8X8 under every skin); tests/run.lua:128-129 | (a) An LSM fake mapping each skin's statusbar key to its own path. (b) Compare each setter family on its own (texture, color, font, shadow), so a surface whose texture never moves fails while its color still moves; and flag a FontString whose face moves while its color never set. (c) Read the `SetTexture` path on Texture fills, not only `SetStatusBarTexture`, and let a consumer mark clear StatusBars (alpha 0) as skipped. (d) An optional per-surface `expect = "texture"`. (e) Declare library surfaces: a Bar, a Charts bar row, a TestStrip, a Footer, a DragHandle and a Dropdown row | Moves here and closes: AuraMaster "statusbar-texture check shape", LibKa0sSkinTester "whole-surface comparison", OutfitterReborn "switch-test coverage of statusbar textures and button labels". Takes the library halves of BankLedger's and LootHistory's guard rows. Part (b) is also AbsorbTracker's U-5 |
| SD-LK-97.19 | Kit typed-value scanner misses common literal shapes (SD-LK-GUARD) | tests/_kit/skin_values.lua:195-226; misses OutfitterReborn OutfitTooltip.lua:28-29, Tooltips.lua:38, Constants.lua:76 and MultiMeters Row.lua:321, Tooltip.lua:248-253 | Scan 3- and 4-number tables, keyed r/g/b tables, multi-assigned numeric triples, `return r, g, b` color triples and `RGBA(...)` fallbacks | Moves OutfitterReborn's "typed-value scanner shapes" here and closes it; takes the library half of MultiMeters' classless-fill row. Merges the two scanner requests |

Considered for the library and kept in the addon: S.Button finding a label named `.label` and S.Checkbox painting a
custom `cb.label` (OutfitterReborn names its fields off-convention; SD-SK-OR.2, OR.3), and the Launcher handing
`onTooltipShow` its palette (one host line; SD-SK-OR.8). Each table marks these "Library (optional)". They can be taken
later without changing the addon items.

## AbsorbTracker (AT)

No GAP rows. Its one UNCLEAR (U-5) is answered by SD-LK-97.18 if the owner agrees.

## AuraMaster (AM)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-SK-AM.1 | Painted surfaces not declared in `Kit.skinSwitch` | tests/skin_gate.lua omits the Text style's line pieces (modules/Style_Text.lua:343-354), the bar gloss (modules/Style_Bars.lua:239), the preset picker window (settings/PresetPicker.lua:419-605), the Aura type and Style dropdown values, the GeneralSpells marks, the Layout and Text page escapes and CastAura's tag | Declare them in tests/skin_gate.lua | The table's "statusbar-texture check shape" row moved to SD-LK-97.18. U-8, U-9 and U-10 may add addon items (flip a companion default plus a FollowOnce step) |

## BankLedger (BL)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-SK-BL.1 | Row stripe and row hover opacities default to the addon's own alphas | defaults/Profile.lua:61-62 (0.03, 0.10); settings/Schema.lua:115, :122; core/Util.lua:191-197. Ka0s Default's `list.stripe` is 0.08 and `list.hover` 0.16 (libs/LibKa0s/SkinDefs.lua:428-429, D-5) | The alpha follows `S.Color("list.stripe")` and `S.Color("list.hover")` through a FROM_SKIN sentinel or a companion defaulting on, or the sliders retire in favour of the library's row wash; a one-time move for profiles still at 0.03 and 0.10 | Merges the stripe and hover GAP rows (one mechanism). The rollout's D2 kept the sliders, but D2 is a lead decision. skinning-§6 forbids a stripe fainter than the library's |
| SD-SK-BL.2 | Minimum-quality option labels built once from the client hex | core/Constants.lua:241-256; settings/Schema.lua:61 | Build the labels lazily, or rebuild on OnLooksChanged and on a Scope change, through `NS.QualityColor` behind a panel-aware escape (as `NS.SkinPanelEscape` does) | R-8 of 2026-10-30 removed the rollout's reason for the client hex |
| SD-SK-BL.3 | Three Insights data fills not declared | modules/Insights_Render.lua:36; modules/InsightsWidgets.lua:693, :772; tests/skin_facts.lua:200-231 | Declare the ranked-bar fill, the stacked segments and the back-to-back sides as their own surfaces, each asserting the texture | The kit's texture-path check is SD-LK-97.18 |

## CombatTrail (CT)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-SK-CT.1 | Insights charts paint every bar of data flat | core/ChartsSetup.lua:51-71 (`fill = Style.Fill`, no `barFill`, no `owner`); libs/LibKa0s/Charts.lua:364; ChartsRender.lua:353, :382, :419, :530 | Add `barFill = function(tex, c, a) NS.Style.Bar(tex, c, a) end` to NS.ChartsHost (Style.Bar goes through NS.Skin.BarTexture and replays on a looks change), pass the owner, and declare one Insights bar in `Kit.skinSwitch` | This is #97's acceptance case for Combat Trail. SD-LK-97.15 hardens the library side but does not replace this item |
| SD-SK-CT.2 | Insights "damage tail after the buzzer" bars use the best-mark blue | modules/Results_Insights.lua:646 `color = C.blue` | Drop `color = C.blue`, so ChartsRender.lua:419 falls back to `ctx.colors.bar` (`ct.chart.bar`) | |
| SD-SK-CT.3 | HUD spell-row bar border companions default off | defaults/Profile.lua:204-205 `borderStyleFromSkin = false, borderColorFromSkin = false` | Default both true and keep `borderShow = false`; a FollowOnce step | The owner's 2026-11-11 call (306b2c0, G16) was "Bar border off by default", which `borderShow = false` already gives. If the owner meant "no border under any skin", record an override instead |
| SD-SK-CT.4 | HUD damage chart pace line color has no companion | defaults/Profile.lua:196; modules/Hud_Chart.lua:388; core/SkinSetup.lua:269 (`ct.chart.diag` declared, never read) | `hud.chart.bestColorFromSkin = true` reading `S.Color("ct.chart.diag")`, a skin row on the Pace line color | D13 is a run call, not an owner ruling |
| SD-SK-CT.5 | Lane background texture keeps the addon's flat pick | defaults/Profile.lua:99-100; modules/LaneRender.lua:512-519 | `lanes.<lane>.bgTextureFromSkin = true` resolving `S.Resolve("bar.texture", cfg.bgTexture, true)`, with a FromSkin row on the Lanes page | Precedent: AuraMaster `bgTextureFromSkin = true` |
| SD-SK-CT.6 | Lane tick and now line colors have no companion | defaults/Profile.lua:106-107; modules/LaneRender.lua:504, :525 | `tickColorFromSkin` and `nowColorFromSkin` (default true) through owner tokens following `chart.grid` and `chart.marker`; the lines stay flat (A7) | Reclassified from OVERRIDE by the skeptic. If the owner rules the stored colors a Leave, this becomes an override row |
| SD-SK-CT.7 | Lane icon stack count and spell-name text: literal outline, no color, no shadow | modules/LaneRender.lua:328-331, :373-374 | Draw both through `NS.Skin.HudFont(fs, { face, size, flags = FROM_SKIN, shadowFromSkin = true })`, color with `S.HudTextColor()`, re-applied on a looks change | Also declare a lane count string as a surface (the table's guard note) |
| SD-SK-CT.8 | Lane edit overlay text hard-codes `"OUTLINE"` | modules/LaneAnchor.lua:402-404 | `S.FontFlags(S.FROM_SKIN)` in place of the literal | Size 11 is the text-size Leave class |
| SD-SK-CT.9 | HUD pet-row paw mark draws untinted | modules/Hud_Breakdown.lua:135-136, :198-200 | `Style.Vertex(row.paw, "icon.tint")`, recorded and repainted on a looks change | L10 keeps only the shape |

The table's "Race call-out look" GAP moved to SD-LK-97.10. Its closing note also asks for one `Kit.skinSwitch` surface
per bar family (a Hud_Chart column, a Hud_Breakdown bar, the pace ahead half, a Results_Table cell bar, a Compare row
bar, the RaceWindow time-bar fill, an Insights bar), each checked for `bar.texture` under the probe skin. Those ride with
SD-SK-CT.1 and need SD-LK-97.18 to bite. U-14 may add an item (the HUD fight clock's outline).

## ConsumableMaster (CM)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-SK-CM.1 | Helpers.Label "medium" descriptions set the font on the FontString, behind the library's hook | settings/Panel.lua:708-716; libs/LibKa0s/SkinAce.lua:751, :808-827; callers settings/Category.lua:470, :523, :526, :530, :788, :974; CategoryComposite.lua:66, :147, :199; MacroBar.lua:786; StatPriority.lua:685, :750 | Call the widget's own `lbl:SetFontObject(_G.GameFontHighlight)` (hooked: it forgets the font, then repaints), or set the font before the paint; declare a scope=panel surface for it | Visible only with Ignore settings panel cleared |
| SD-SK-CM.2 | Painted surfaces not declared in `Kit.skinSwitch` | tests/skin_switch_facts.lua:153-185 omits KCMIconButton hoverBG (modules/KCMIconButton.lua:32), the flyout entries' backdrop, edge and count (MacroBarFlyout.lua:427-445), drag-icon hover art and icon edges (KCMMacroDragIcon.lua:61, :84; KCMItemRow.lua:209), MacroDisplay tooltip lines (core/MacroDisplay.lua:258-268), the `cm.warn`/`cm.tip*` escapes (settings/Category.lua:153-169), the reorder ghosts (StatPriority.lua:585-596, MacroBarSlots.lua:343-353) and the Helpers.Label face | Declare them, the settings ones with scope=panel (tests only) | U-16 and U-17 may add an item (the owner tokens' Ka0s Default values) |

## DropWatcher (DW)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-SK-DW.1 | Painted surfaces not declared in `Kit.skinSwitch` | tests/skin_switch_facts.lua:121-228 omits the Rolls panel (modules/RollsPanel.lua:360-408), the Roll popup card (modules/RollPopup.lua:274-275, :320), the History, Pending and compact rows (WindowHistory.lua:413-416, WindowPending.lua:432-435, CompactGroup.lua:226-229), the compact filters button (CompactChrome.lua:320-341), the Edit message box (DetailCard.lua:736-747), the scrollbars, the trade countdown bar and track (WindowGroup.lua:642, :909) and the Drops empty state (DropsStrip.lua:150-153) | Declare them in tests/skin_switch_facts.lua | All read tokens today. U-18 and U-19 may add items (the open-row wash, the Edit box face) |

## KickCD (KC)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-SK-KC.1 | Icon grid charges badge draws the template's shadow under every skin | modules/IconGrid_Render.lua:381, :965-980 (raw `SetFont`, never `S.HudFont`) | Paint through `NS.Skin.HudFont(icon.chargesText, { face, size, flags, shadowFromSkin = true })`, keep `HudTextColor` after it; add a shadow probe to the badge surface in tests/skin_facts.lua | Cause D6 is an owner Fix item |
| SD-SK-KC.2 | Profile default and pre-store fallback write the skin literal | defaults/Profile.lua:384 `skin = "ka0s"`; core/SkinSetup.lua:119, :265-267 | `NS.DEFAULT_SKIN = (Skin and Skin.DefaultSkin and Skin:DefaultSkin()) or "ka0s"` at load, used by Profile.lua and SkinChoice; keep `skin.source = "ka0s"` | skinning-§2. No visible effect while KickCD is Retail-only |

## LibKa0sSkinTester (ST)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-SK-ST.1 | Faces and widths: per-skin body and title sample lines never colored | modules/ShowroomFonts.lua:175-197 | In drawLine, after setFace, `SetTextColor(NS.Skin.Color("text.body"))` (the title line takes the heading role). Not `R.Paint("Text")`, which resets the per-skin face | The cell passes the guard today because its face moves |
| SD-SK-ST.2 | HUD faces: per-skin `hud.font` lines never colored | modules/ShowroomHud.lua:43-55; tests/skin_surfaces.lua:61-63 leaves them out | In drawSkin, `setColor(fs, R.Paint("HudTextColor"))`, then declare the lines with a note that only their color moves | The worn skin's color is the default proposal; the owner may prefer each skin's own resolved HUD text color |
| SD-SK-ST.3 | Values: GetFont readout line uncolored, typed flags `""` | modules/ShowroomValues.lua:71-79 | `R.Paint("Text", fs, "body")` at build, and `R.Paint("FontFlags", NS.Skin.FROM_SKIN, "window")` in place of `""` | Size 14 is the text-size Leave class |

The table's "whole-surface comparison" row moved to SD-LK-97.18. U-6 and U-20 may change a `Kit.skinValues` row or a
LEFT_OUT note.

## LootHistory (LH)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-SK-LH.1 | Bar fills and hosted controls not declared | tests/skin_surfaces.lua:310-409 declares only "a strip bar's fill" (:379) | Declare a ledger half (modules/AnalyticsLedger.lua:138, :141), a Timeline flow column (modules/Timeline.lua:349-355), a dropdown, the search box, a scrollbar, the line chart and a legend entry | The kit's `expect = "texture"` half moved to SD-LK-97.18. Runtime paint is correct; this is guard only. U-7 may add an item (the StaticPopup heading) |

## MultiMeters (MM)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-SK-MM.1 | Tooltip spell-bar switch surface is a proxy that records no texture | tests/skin_facts.lua:131-152 | Make the surface draw a real spell line through `Tooltip_Lines` and record `SetStatusBarTexture` | |
| SD-SK-MM.2 | Cell bar Custom swatch `bars.customColor` has no companion | defaults/Profile.lua:360; modules/Row.lua:314 | `bars.customColorFromSkin` default true drawing `S.BarFillColor()` under custom, cached in skinLooks; FOLLOW_ONCE_KEYS (core/Database_Migrations.lua:940) | Default Color mode stays class |
| SD-SK-MM.3 | Classless row fill is a gray literal under the default class mode | modules/Row.lua:321 `return 0.45, 0.45, 0.5` | Answer a skin neutral (`S.BarFillColor()`, or owner token `mm.barNeutral` {0.45,0.45,0.5} following `bar.fill`) through skinLooks | The scanner half moved to SD-LK-97.19 |
| SD-SK-MM.4 | Cell background Custom swatch `bars.bgColor` has no companion | defaults/Profile.lua:369; modules/Row.lua:343-345 | `bars.bgColorFromSkin` default true drawing `S.Color("bar.bg")` color only, `bgAlpha` kept (SF-MM-3) | The tooltip's twin already has one |
| SD-SK-MM.5 | Tooltip spell bar Custom swatch, which is also the classless fallback under the default class mode | defaults/Profile.lua:523; modules/Tooltip_Lines.lua:426-439, :484-485 | `tooltip.barColorFromSkin` default true drawing `S.BarFillColor()` under custom and as the classless fallback | Visible by default on every NPC and enemy tooltip and their death-recap bars |
| SD-SK-MM.6 | GameTooltip lines with literal colors: the classless name line, and a stat line with no palette entry | modules/Tooltip.lua:248-253 (`return 1, 1, 1`), used at Tooltip_Builders.lua:434-437, :763-765, :933; Tooltip_Builders.lua:832-834 (`1,1,1` and `0.62,0.62,0.62`) | `gtip.value` for the classless name and the unpaletted stat value, `gtip.muted` (`mm.tipHint`) for the muted line | Merges two GAP rows (both literal GameTooltip line colors, skinning-§7) |

U-21 may add an item (drop the combat MenuUtil fallback once the library measures safely).

## OutfitterReborn (OR)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-SK-OR.1 | Optimize progress bar has no background | modules/Dialog_Progress.lua:37-42 (no BACKGROUND region under `f.bar`) | A BACKGROUND texture under `f.bar` painted from `bar.bg` through a recorded primitive | The fill-texture row moved to SD-LK-97.17. If that is declined, the addon calls `NS.Skin.BarTexture(f.bar, NS.Skin.Color("text.accent"))` itself |
| SD-SK-OR.2 | Dialog push-button labels never painted | modules/UIDialogs.lua:51-58 (`b.label`, which `labelOf` does not find: libs/LibKa0s/SkinPaintControls.lua:133-136); used at Dialog_Outfit.lua:229, :232; Dialog_Trigger.lua:235, :238; Dialog_Rebuild.lua:166, :172, :175; Dialog_Progress.lua:48; Dialog_TriggerFields.lua:201, :273 | Name it `b.text`, or `b:SetFontString(b.label)`, in D.Button | |
| SD-SK-OR.3 | Dialog checkbox labels never painted | modules/UIDialogs.lua:62-70; S.Checkbox paints only box, mark and hover (SkinPaintControls.lua:346-380) | `NS.Skin.Text(cb.label, "body")` in D.Check | |
| SD-SK-OR.4 | Outfit window item-row name face | modules/Window_Rows.lua:341-343, :421 | `NS.Skin.Font(row.itemName)` at build; keep the per-render quality color | |
| SD-SK-OR.5 | Outfit tooltip title and trigger-description lines use literal colors | modules/OutfitTooltip.lua:28-29 (`NORMAL`, `HIGHLIGHT`), :60-61, :72-73 | Title `NS.SkinColor("gtip.title")` (as NS.ShowTitleTip does, core/CoreSetup.lua:46-47), description `gtip.body`; drop NORMAL and HIGHLIGHT | Merges two GAP rows (one tooltip, one fix) |
| SD-SK-OR.6 | Item tooltip "Equipment Sets:" line is a gold literal | modules/Tooltips.lua:38, :144 | Read a token at draw time (`gtip.body`, or `gtip.title` for the gold role); clear the line cache on OnLooksChanged | |
| SD-SK-OR.7 | Window-row tooltips and the bar-button test-sample tooltip are uncolored | modules/Window_Rows.lua:195-196, :226-227, :234-235; modules/Bar_Buttons.lua:169-170 | One helper: line 1 `gtip.title`, the rest `gtip.body`, with PlaceBodyTip placement | Merges two GAP rows (same shape, same helper) |
| SD-SK-OR.8 | Minimap launcher host line "Current outfit: %s" uncolored | core/LauncherSetup.lua:168 | Pass `NS.SkinColor("gtip.line")` | The library's own lines already read `pal.line` (libs/LibKa0s/Launcher.lua:473, :530-537) |
| SD-SK-OR.9 | Hotkey equipped/unequipped message on UIErrorsFrame is a green literal | core/Constants.lua:76; core/LauncherSetup.lua:41-43; pinned by tests/test_keybinds.lua:349 | An owner token (for example `of.message.equip`, default {0.2,0.75,0.3}, follow `sem.good`) read at AddMessage time; update the pin | skinning-§9: lines the addon writes into a client frame take their colors from the skin |

The guard rows ("switch-test coverage", "typed-value scanner shapes") moved to SD-LK-97.18 and SD-LK-97.19. U-7 and
U-22 may add items (the character-sheet tooltip, the uncolored glyph tint).

## PanelMaster (PM)

No GAP rows. U-23 decides whether the new-panel look defaults become one.

## PartyFrameEnhanced (PFE)

No GAP rows. U-24 may add a small item (paint the `(test)` mark with `text.muted`) and a re-cite of the stand-in rows.

## PremadeGroupsFilterExtension (PGFE)

No GAP rows and no UNCLEAR rows.

## PrettyChat (PC)

No GAP rows. U-25 may add an item (the `/pc test` report labels through owner tokens).

## QuickComms (QC)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-SK-QC.1 | Auto-thank toast main line and note line never painted | modules/AutoThank_Toast.lua:47, :51, :105; core/ToastSetup.lua and libs/LibKa0s/Toast.lua:326-330 paint only the frame | In `regions()`: `NS.Skin.Font` plus `NS.Skin.Text(fs, "body")` for the main line and `NS.Skin.Text(fs, "disabled")` for the note; declare "the toast's text" | Merges two GAP rows (same function) |
| SD-SK-QC.2 | Auto-thank toast Thank button has no body or edge and a client-gold label | modules/AutoThank_Toast.lua:76-86, :81; modules/SendEngine.lua:87 | On first build (always out of combat), `NS.Skin.Button(b)`, or Shell plus `btn.*` if Button's script hooks would disturb the secure button; label `NS.Skin.Font` plus `Text("btn")`; declare it | |

The pad-window gradient and art row moved to SD-LK-97.16. U-28 may add an item (the End-preview button).

## RangeMaster (RM)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-SK-RM.1 | HUD text outline default `"OUTLINE"` (number, text, caption) | defaults/Profile.lua:95, :99, :101; settings/Containers_Display.lua:164-176; modules/Style.lua:71 | `flagsFromSkin = true` (with `fromSkin = true`) on FontGroup, default `outline = "@skin"`, and a per-profile step moving stored `"OUTLINE"` to `"@skin"` | SD-LK-97.6 and SD-LK-97.7 make the composer side the default; the stored default and its move stay here |
| SD-SK-RM.2 | HUD text shadow: the player's row and the skin's shadow fight on the string | modules/Style.lua:71-77; libs/LibKa0s/SkinPaintHud.lua:96-103 | Pass `shadow = cfg.shadow, shadowFromSkin = cfg.shadowFromSkin` to `S.HudFont`, drop the direct `SetShadowOffset`, add `shadowFromSkin` defaulting true | |
| SD-SK-RM.3 | Caption text color is a fixed white | defaults/Profile.lua:95; modules/Container.lua:599; modules/Style.lua:46 | A `colorFromSkin` companion (or a Skin value in Color from) defaulting on, drawing `S.HudLabelColor()` | Visible on every preset install |
| SD-SK-RM.4 | Fixed-mode swatches have no follow companion (number, text, indicator, border, background) | modules/Style.lua:45; defaults/Profile.lua:87-88, :100, :102, :105; settings/Containers.lua:102-110 | A Skin value or a companion per swatch (`S.HudTextColor()`, `bar.border`, `bar.bg`); Band and class keep their branch ahead of it | Grows if U-30 rules the band border and background chrome rather than meaning |
| SD-SK-RM.5 | Container border style and thickness never read the skin | defaults/Profile.lua:87; settings/Containers_Display.lua:131-141, :330-334; modules/Style.lua:160-175 | `fromSkin = "bar"` on BorderGroup, a `borderFromSkin` companion defaulting true, resolved through `S.BarBorder(style, show, size, fromSkin)` | Pairs with SD-LK-97.9 |
| SD-SK-RM.6 | No `Skin.FollowOnce` step for the HUD companions | no `FollowOnce`, `fullSkinReset` or `ResetToSkin` in core/, modules/, settings/, defaults/; core/Database.lua | One per-profile step from `Database:Init` and `OnProfileChanged`, key paths built per container | Depends on SD-SK-RM.1 to RM.5 |
| SD-SK-RM.7 | Mock nameplate health fill is flat | modules/Anchors_Mockplate.lua:74 `SetColorTexture` | `NS.Skin.BarTexture(p.fill, color("sem.bad", ...))` (recorded); `SetColorTexture` only on the degraded path | The Combat Trail trigger class |
| SD-SK-RM.8 | Mock nameplate name line has no face or color | modules/Anchors_Mockplate.lua:91 | Draw it through `S.HudFont` and `S.HudTextColor()` in `paint()` | |
| SD-SK-RM.9 | Frame-picker overlay label face | modules/FramePicker.lua:135, :153 | `NS.Skin.Text(label, "accent")` in `paint()` | |
| SD-SK-RM.10 | Spell chip answers read the band ramp ends, not semantic tokens | modules/Elements_Spells.lua:26-27, :76-86; tokens at libs/LibKa0s/SkinDefs.lua:474, :498 | Read `sem.good`, `sem.bad`, `sem.unknown` through `NS.Skin.Color` with the ramp as fallback, repainted on OnLooksChanged | Soft dependency on U-30: if the owner ties the chips to the band ramp, this becomes an override row |
| SD-SK-RM.11 | A picked face LSM no longer resolves draws `FRIZQT__` | modules/Style.lua:59-63; core/Constants.lua:10 | Answer nil, so `S.HudFont` draws the skin's face | Minor |
| SD-SK-RM.12 | Settings Style tiles wear the skin while Ignore settings panel is on | settings/Containers_Display.lua:602-608, :665-669 (`NS.Skin.Color` knows no Scope) | Paint through a Scope-aware primitive with `panel = true` (`S.Inset` or `S.Card`) | |
| SD-SK-RM.13 | `Kit.skinSwitch` declares three surfaces | tests/run.lua:95-125 | Declare the caption, Text element, indicator (art and W.Bar), spell chips, container border and background, preset picker, mock nameplate, frame-picker overlay and the Display tiles, with scope and companion marks once the companions land | The mock nameplate and frame picker fail today; the rest pass |

## SkillMaster (SM)

| ID | Element | Evidence | Fix | Closes, merges, notes |
|---|---|---|---|---|
| SD-SK-SM.1 | Settings BoxList eye mark resets to untinted white | settings/BoxList.lua:189; settings/Layout.lua:239, :245; settings/Rows.lua:201-209 | Tint through `NS.Skin.Mark` or `S.Color("icon.tint")` while the Scope paints the panel, the dim as alpha only, and restore on release for the AceGUI pool | Visible only with Ignore settings panel cleared |
| SD-SK-SM.2 | Waypoint arrow text color has no skin companion | defaults/Profile.lua:226 | Add `waypoints.arrowFontColorFromSkin = true` and its path | Needs SD-LK-97.13, which carries the library half of this row |
| SD-SK-SM.3 | Waypoint arrow text shadow has no skin companion | defaults/Profile.lua:229 | Add `waypoints.arrowFontShadowFromSkin = true` and its path | Needs SD-LK-97.14, which carries the library half of this row |
| SD-SK-SM.4 | Undeclared surfaces: the waypoint arrow, the broker tooltip's classic style, a BoxList row with the Scope cleared | tests/run.lua:65-135, :120-129; modules/WaypointArrow.lua:208 | Declare the arrow (test mode's sample target), a `tooltips.ldb.style = "classic"` surface and a BoxList row with Ignore settings panel cleared | Merges two guard rows |

U-7 may change SkillMaster's tooltip line colors to the `gtip.*` family, and U-31 files a hover wash for trainer
cards outside #97.

## WhatGroup (WG)

No GAP rows and no UNCLEAR rows.

## GAP fixes that depend on an UNCLEAR answer

| Item | Waits on | Why |
|---|---|---|
| SD-LK-97.10 | U-1 | The Callout's look defaults are the owner's L17 settings. If L17 stands, the outline GAP is recorded with it as an override and Combat Trail's call-out row closes as OVERRIDE |
| SD-LK-97.3 (Charts part only) | U-4 | The Bar widget's gloss is a plain GAP; carrying it to window chart bars is the open question |
| SD-LK-97.18 (b) | U-5 | Per-setter-family comparison. Two GAP rows (LibKa0sSkinTester, OutfitterReborn) already need it, so the answer mostly decides whether AbsorbTracker's texture pins can retire |
| SD-SK-RM.4, SD-SK-RM.6 | U-30 | If the band border and background are chrome, they gain companions and FollowOnce keys |
| SD-SK-RM.10 | U-30 | If the band ramp is the chips' meaning, the row becomes an override |
| SD-SK-CT.3, SD-SK-CT.6 | owner intent, no U row | Each table offers an override reading ("no border under any skin"; tick colors as a Leave). Neither is an UNCLEAR row, so both stand as GAP unless the owner says otherwise |

Answers that, taken as recommended, add new fix items are listed with each question in `02_UNCLEAR.md`.
