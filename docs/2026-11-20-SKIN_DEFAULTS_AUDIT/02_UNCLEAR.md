# UNCLEAR rows: questions for the owner

The 42 UNCLEAR rows in `tables/` come down to 31 questions. Where several rows or addons ask the same thing, they share
one question and the addons are listed. Each question can be answered in one line: pick an option, or say "as
recommended". The answers are SD-RULE in the run bundle (`docs/2026-11-20-LIBKA0S_94_97_99_100/`) and are recorded
there, not here.

"Adds" names the fix work that follows if the recommendation is taken. Evidence paths are relative to the repo named in
the brackets.

## Library and cross-addon

### U-1 [LibKa0s, CombatTrail] Callout look: does R-2 supersede your L17 settings?

- **Evidence.** LibKa0s Callout.lua:158-159, :174 `font = FONT_DEFAULT` (Ka0s Oxanium SemiBold), :183 `glowColorFromSkin
  = false` with a black glow, :652-653 black shadow, :174 outline `THICKOUTLINE`. These are your in-game settings of
  2026-11-14 (LibKa0s docs/superpowers/plans/2026-11-13-callout.md:93, L17). The only consumer is Combat Trail's race
  countdown (CombatTrail core/CalloutSetup.lua:57-63), and skinning-§9 leaves "Combat Trail's race clocks". The LibKa0s
  table marks this UNCLEAR; the Combat Trail table marks the same defaults GAP.
- **Options.** (a) R-2 supersedes L17: the call-out follows the skin by default. (b) L17 stands as an override, or the
  call-out counts as a race clock under §9.
- **Recommendation.** (a). The §9 Leave class names the RaceClock, not the call-out. Default `font = "Skin font"`, an
  "@skin" outline, `glowColorFromSkin = true` and a shadow companion, with a one-time move only for stored values still
  equal to the L17 defaults.
- **Adds.** SD-LK-97.10 goes ahead; Combat Trail calls its FollowOnce key list.

### U-2 [LibKa0s] Callout kind colors: are info, go, stop, warn and error meaning colors?

- **Evidence.** Callout.lua:111, :176-179 literal defaults in a player-editable table; `colorOf` (:360-366) reads no
  semantic token. skinning-§9: a meaning with a semantic token reads it.
- **Options.** (a) Meaning colors that read `sem.info`, `sem.good`, `sem.bad`, `sem.warn` by default. (b) Leave the
  literals.
- **Recommendation.** (a), with no companion: the defaults read `sem.*`, and a swatch the player sets wins.
- **Adds.** A library item next to SD-LK-97.11.

### U-3 [LibKa0s] CalloutSettings plain build: exempt as a non-Ka0s-host fallback?

- **Evidence.** CalloutSettings.lua:741-860 (stock UIPanelButton and UICheckButton rows), used whenever
  `opts.options` is absent (:906-916). Nothing paints it. Combat Trail passes an Options instance.
- **Options.** (a) Exempt, documented as the no-Options fallback no Ka0s host may use. (b) Skin it.
- **Recommendation.** (a).
- **Adds.** A doc note in the library.

### U-4 [LibKa0s] Window chart bars: do they take the skin's gloss under Glass?

- **Evidence.** Charts.lua:351-353 `barFill` is S.BarTexture on a Texture, with no gloss. Glass states `gloss = true`
  (SkinDefsOthers.lua:570, :604). §6 puts gloss under HUD style; chart bars are window data.
- **Options.** (a) Yes, through the same Texture gloss the Bar widget gets (SD-LK-97.3). (b) No, gloss stays HUD-only.
- **Recommendation.** (a), so a chart bar and a HUD bar match under Glass.
- **Adds.** The Charts part of SD-LK-97.3.

### U-5 [AbsorbTracker] Skin-switch kit: compare each setter family on its own?

- **Evidence.** AbsorbTracker tests/_kit/skin_switch.lua:241-259: a surface passes when any one setter differs, so the
  bar fill passes on `SetStatusBarColor` alone. The LibKa0sSkinTester and OutfitterReborn tables raise the same point
  as GAP rows (now SD-LK-97.18).
- **Options.** (a) Yes: texture, color, font and shadow each checked, so a texture that stops following fails. (b) Keep
  the whole-surface comparison.
- **Recommendation.** (a), in the library kit. It is the Combat Trail class. Keep AbsorbTracker's tests/test_skin_hud.lua
  texture pins until it lands.
- **Adds.** Part (b) of SD-LK-97.18.

### U-6 [AuraMaster, LibKa0sSkinTester] Kit rows whose cause id is bookkeeping: move them to a named kit category?

- **Evidence.** AuraMaster tests/skin_gate.lua:16-17 cite A7 for unreachable stored-channel defaults (`normal.r or 1`);
  A7 is fades, dims and flat thin bars (FULL_SKINNING inputs/SKIN_CAUSES.md:35). LibKa0sSkinTester tests/run.lua:153-155
  cite A5, the "fix the tester's unpainted rows" item, for the NavItem's white tint base. Neither literal draws a look.
- **Options.** (a) Re-point them to kit categories ("unreachable default", "tint base"). (b) Keep the cited ids.
- **Recommendation.** (a).
- **Adds.** Row edits in both addons; a kit category for unreachable defaults if the kit lacks one (library).

### U-7 [SkillMaster, LootHistory, OutfitterReborn] Lines written into a stock client frame: do they read the `gtip.*` family?

- **Evidence.** SkillMaster writes `text.*`, `sem.*` and `sm.bonus*` lines onto GameTooltip (modules/RowTooltip.lua:210-219,
  :266-274; Journal.lua:623-626; TrainerPopup.lua:118-121, :129-131; WaypointArrow.lua:109-112), so a light-window skin
  can lose legibility on the dark stock tooltip. LootHistory writes a gold `|cffffd100` heading into a StaticPopup
  (settings/Slash.lua:118-127), which the kit admits as "StaticPopup text" (tests/_kit/skin_values.lua:371) against
  skinning-§9 ("lines the addon writes into a client frame still take their colors from the skin"). OutfitterReborn's
  character-sheet button tooltip is uncolored (modules/Dock.lua:787-789); DEV-SKIN-SHEET-BUTTON (docs/ARCHITECTURE.md:421)
  covers the button's look, not its tooltip line.
- **Options.** (a) Every line on a stock client frame reads `gtip.title`, `gtip.body` and `gtip.muted`. (b) Window
  `text.*` tokens are fine. (c) Leave such lines in the client's colors.
- **Recommendation.** (a). It is the library's family for tooltip lines (skinning-§1), drawn for the stock dark backing.
- **Adds.** SkillMaster: its tooltip lines move to `gtip.*`. LootHistory: the popup heading reads `gtip.title`, and the
  kit's "StaticPopup text" category is narrowed. OutfitterReborn: the sheet tooltip line reads `gtip.title`.

## AuraMaster

### U-8 [AuraMaster] SF-AM-3: flip the bar fill, icon border and Text-line color companions to follow the skin?

- **Evidence.** defaults/Profile.lua:269 `barColorFromSkin = false`, :282, :301, :331 `*BorderColorFromSkin = false`,
  :166-171 `t.fontColorFromSkin = false`; set false by core/Database_Migrations.lua:1100, :1118-1122 (v17). SF-AM-3
  (docs/2026-11-01-SMOKE_FEEDBACK/items.tsv:17) is your "accepted deviation"; R-2 of 2026-11-20 says such defaults follow
  the skin. Under Ka0s Default the skin's `bar.fill`, `icon.border` and `hud.text` equal the stored values
  (libs/LibKa0s/SkinDefs.lua:459), so nothing changes there.
- **Options.** (a) R-2 supersedes SF-AM-3 for all three. (b) SF-AM-3 stands.
- **Recommendation.** (a), with a one-time step for stored values still at the v17 defaults.
- **Adds.** AuraMaster default flips, the Text-line FollowOnce exclusion removed, the line pieces declared (that part is
  already SD-SK-AM.1).

### U-9 [AuraMaster] SF-AM-2: flip the bar background, keep the bar border dark?

- **Evidence.** defaults/Profile.lua:273-274 `bgColorFromSkin = false`, :277-278 `borderColorFromSkin = false`;
  Database_Migrations.lua:1115-1116. SF-AM-2 (items.tsv:16) asks a dark background and border in every skin. Every
  skin's `bar.bg` is a translucent dark except Glass (white 0.08); skins' `bar.border` is gold in Midnight, white in High
  Contrast, gray in WoW (SkinDefsOthers.lua:359-376).
- **Options.** (a) Flip the background, keep the border as an override. (b) Flip both. (c) Keep both.
- **Recommendation.** (a).
- **Adds.** AuraMaster background default flip and its one-time step; the border row recorded as OVERRIDE.

### U-10 [AuraMaster] SF-AM-1: does the text glow stay black in every skin?

- **Evidence.** defaults/Profile.lua:349 `glowColorFromSkin = false`; Database_Migrations.lua:1114. SF-AM-1 (items.tsv:15)
  "Default text glow black in all skins". `glow.color` is gold in Ka0s Default (SkinDefs.lua:539) and each skin's accent
  elsewhere, so a flip would break SF-AM-1 in every skin.
- **Options.** (a) Keep it black, recorded as an override. (b) R-2 supersedes it.
- **Recommendation.** (a). SF-AM-1 is the specific, later-tested ruling on this element.
- **Adds.** Nothing; the row is recorded as OVERRIDE.

### U-11 [AuraMaster] Bar spark color: covered by the A6 game-art Leave?

- **Evidence.** defaults/Profile.lua:284 `sparkColor = color(1,1,1,0.9)`, no companion; modules/Style_Bars.lua:70,
  :266-269 (desaturated ADD). Spark art is A6 (FULL_SKINNING 00_PLAN.md:11). No skin token describes a spark highlight.
- **Options.** (a) A6 covers it. (b) Add a token and a companion.
- **Recommendation.** (a), no new token.
- **Adds.** Nothing.

### U-12 [AuraMaster] Preset role bar colors (gray, orange, tan, purple): keep them in every skin?

- **Evidence.** defaults/Presets.lua:332-339, :645-647 write `barColorFromSkin = false` with the role colors, copied
  from your 2026-11-17 SmokeTest profile (commit ea19dd4, smoke PRESETS-42). There is no written ruling that the roles
  keep their colors under every skin.
- **Options.** (a) An override: roles read apart, a meaning use. (b) The roles follow the skin's `bar.fill`.
- **Recommendation.** (a), recorded in the presets spec.
- **Adds.** A line in AuraMaster's presets spec.

## BankLedger

### U-13 [BankLedger] Insights data-fill alphas (0.9 to 0.95): a Leave under fades and dims?

- **Evidence.** modules/Insights_Render.lua:36, :118; modules/InsightsWidgets.lua:622, :693, :772. The hue is a token
  or a meaning color; only the alpha is typed. D7 (docs/2026-10-29-SKINNING_ROLLOUT/DECISIONS.md:58) named S.BarTexture
  only.
- **Options.** (a) Leave (fades, dims). (b) The alpha follows the token's alpha.
- **Recommendation.** (a). No change.
- **Adds.** Nothing.

## CombatTrail

### U-14 [CombatTrail] Is the HUD fight clock one of "Combat Trail's race clocks"?

- **Evidence.** defaults/Profile.lua:182-184 clock `fontFlags = ""` and `fontShadow = false`, commented "the mono role",
  yet `fontFromSkin = true`, so modules/Hud_Appearance.lua:137-141 draws the skin's `hud.font`, not mono.
  tests/skin_surfaces.lua:25-26 says the clock's mono face never follows. skinning-§9 leaves "Combat Trail's race
  clocks" (A9, from DpsRace's elapsed and left clocks).
- **Options.** (a) No: the fight clock follows the Font outline. (b) Yes: it is a race clock and keeps its flags.
- **Recommendation.** (a). Default `fontFlags = "@skin"` with a FollowOnce step; its face already follows.
- **Adds.** A Combat Trail item (clock flags default, FollowOnce key, the test comment corrected).

### U-15 [CombatTrail] Race detail Timing strip bands: flat thin bars (A7) or bars of data?

- **Evidence.** modules/Results_RaceDetail.lua:254-259 `mark()` draws Style.Fill flat; :284-285 race fill at 0.5 and tail
  at 0.45 alpha over a 34 px card strip (:34). The hues themselves are meaning colors (OVERRIDE row).
- **Options.** (a) Leave (A7). (b) Bars of data that take `bar.texture`.
- **Recommendation.** (a). They are translucent time-span washes over a card, not value bars.
- **Adds.** Nothing.

## ConsumableMaster

### U-16 [ConsumableMaster] Macro bar and flyout edge: take the skin's black under Ka0s Default instead of 0.25 gray?

- **Evidence.** modules/MacroBar.lua:405-406; modules/MacroBarFlyout.lua:475-476; core/SkinSetup.lua:150 `cm.barBorder`
  {0.25,0.25,0.25,1}. Ka0s Default's `bar.border` is {0,0,0,1} (libs/LibKa0s/SkinDefs.lua:533), 64 levels off. O1/X1 keep
  near misses of 2 to 8 levels; D4 ruled "Fix: skin colors exist" (FULL_SKINNING inputs/SKIN_CAUSES.md:23).
- **Options.** (a) Take `bar.border`. (b) Keep the gray as an owner token.
- **Recommendation.** (a), as SF1-CM did for `cm.buttonBorder` (docs/2026-11-06-REVENDOR_LIBKA0S_V1_89/SF1_SMOKE_FEEDBACK.md
  item 1).
- **Adds.** A ConsumableMaster item: drop the token and read `bar.border`, or set its default to {0,0,0,1}.

### U-17 [ConsumableMaster] Near-miss owner tokens under Ka0s Default (button fill 0.6, flyout fill 0.85, flyout shade 0.8): keep them?

- **Evidence.** core/SkinSetup.lua:151 `cm.buttonBg` {0,0,0,0.6} against `bar.bg` 0.5; :157 `cm.flyoutBg` 0.85 against
  `popup.bg` 0.92; :158 `cm.flyoutShade` 0.8 against `cover.dim` 0.6 (SkinDefs.lua:449, :451, :533). The first two sit
  inside O1/X1's near-miss band; the shade (0.2) does not, but it has to hold the arrow over bright icon art. Every other
  skin draws the followed token.
- **Options.** (a) Keep all three. (b) Snap all three to the skin's values. (c) Keep the two fills, snap the shade.
- **Recommendation.** (a). The shade needs your sign-off because it is not a near miss.
- **Adds.** Nothing; the three rows are recorded as OVERRIDE.

## DropWatcher

### U-18 [DropWatcher] Expanded-row wash: follow `list.sel` instead of `list.hover`?

- **Evidence.** core/SkinSetup.lua:136-140 `dw.rowOpen` {1,0.82,0,0.16} with `follow = "list.hover"`; modules/WindowGroup.lua:682.
  The follow dates from DW-01 (ec7ecac), a lead call; AD-82-DW (7b257da) raised the default to equal `list.hover`. An open
  row now draws exactly the hover wash in every skin, while ruling Q2 (skinning-§4) holds Ka0s Default's selection apart
  from its hover.
- **Options.** (a) Follow `list.sel`, default = Ka0s Default's `list.sel` (gold 0.26). (b) Keep `list.hover`.
- **Recommendation.** (a).
- **Adds.** A DropWatcher item in core/SkinSetup.lua and a re-pin in tests/test_skin_setup.lua.

### U-19 [DropWatcher] Edit message box: keep chat's face, or skin it?

- **Evidence.** modules/DetailCard.lua:715 `e.box:SetFontObject("ChatFontNormal")`; no skin call on `e.box`, so the
  skin's face, Ignore fonts and `input.text` never reach it. D6 (docs/2026-10-29-SKINNING_ROLLOUT/DECISIONS.md:111) is a
  lead's "recommend keep"; the full-skinning "not gaps" bucket was never put to you. §9's "chat frame's font" covers the
  client's chat frame, not an addon-owned EditBox.
- **Options.** (a) Skin it. (b) Keep the chat face.
- **Recommendation.** (a). The table offers no recommendation; this one follows from §9's wording.
- **Adds.** A DropWatcher item: `NS.Skin.Font(e.box)` and `input.text` for the color.

## LibKa0sSkinTester

### U-20 [LibKa0sSkinTester] The "Stock" comparison twins: keep them stock under every skin?

- **Evidence.** modules/ShowroomOverlays.lua:205, :211 (a UIPanelButtonTemplate button and an InsetFrameTemplate box),
  never painted; tests/skin_surfaces.lua:30 leaves FadeNineSlice out because "its twin shows it".
- **Options.** (a) Keep them stock, recorded. (b) Skin them.
- **Recommendation.** (a). They exist to show the fade against stock. Record it as a LEFT_OUT note or a `Kit.skinValues`
  row.
- **Adds.** A note or row in the tester's tests.

## MultiMeters

### U-21 [MultiMeters] Segment picker in combat: keep the client menu, or fix the library and drop it?

- **Evidence.** modules/Window_Header.lua:1240-1241 falls back to `NS.Compat.OpenContextMenu` while restricted, because
  libs/LibKa0s/WidgetsDropdown.lua:88-103 measures every label even with `opts.width`. A2's ruling was "swap to the Ka0s
  menu"; FULL_SKINNING 99_REPORT.md:56 lists the fallback as an exception, and you passed SKIN-35 expecting the client
  menu mid-pull.
- **Options.** (a) Fix the library (skip measuring when `opts.width` is given, or pcall it), then drop the fallback.
  (b) Keep the client menu as a sanctioned exception.
- **Recommendation.** (a).
- **Adds.** A library item in WidgetsDropdown and a MultiMeters item removing the fallback.

## OutfitterReborn

### U-22 [OutfitterReborn] An outfit glyph with no picked color: draw the skin's `icon.tint`?

- **Evidence.** modules/IconBrowserSetup.lua:60-66 `Glyph.Tint` answers white for none; Window_Rows.lua:322-323 and
  Bar_Buttons.lua:314-316 SetVertexColor. The broker menu markup takes no tint at all, even a picked one
  (Broker.lua:105-118).
- **Options.** (a) No color means the skin's `icon.tint`; a picked color is the player's override. (b) White stays.
- **Recommendation.** (a). R-2 reads "no color" as an option default, and §9 says only the icon's tint follows.
- **Adds.** An OutfitterReborn item (tint resolution, and the broker markup taking the tint).

## PanelMaster

### U-23 [PanelMaster] New-panel look defaults: follow the skin (R-2), or count as the player's content (A8)?

- **Evidence.** core/Constants.lua:346-347, :358-359, :392, :401, :412, :418, :443 (C.PANEL_TEMPLATE); modules/Registry.lua:453
  copies the whole template into each record, so an untouched default cannot be told from a pick. The editor composes
  BorderGroup and BarGroup without `fromSkin` (settings/PanelEditorTabs.lua:518-529, :569-614). Constants.lua:428-436
  says nothing may restyle a panel unasked.
- **Options.** (a) A8 holds: the shipped defaults are content. (b) New panels only are born following the skin through
  `fromSkin` companions; existing records untouched.
- **Recommendation.** (a), recorded as an override.
- **Adds.** Nothing under (a). Under (b), an addon item (editor groups with `fromSkin = true`, companions seeded on for
  new panels).

## PartyFrameEnhanced

### U-24 [PartyFrameEnhanced] Preview stand-in: keep the host frame's look under every skin?

- **Evidence.** modules/StandIn.lua:95-97, :109-110, :123-124 (ground and edge), :31-33, :78-80, :100, :112, :129, :135
  (health and power StatusBars, no `bar.texture`), :175 (name text, no S.Text), :29 (`(test)` mark, gray literal).
  tests/skin_facts.lua:10-15 cite A7, which is the wrong class; the real basis is the rollout's E-PF-3, an agent
  classification. §9 has no class for an imitation of a host frame. Three rows.
- **Options.** (a) Keep the host look: a new §9 class, "an addon-drawn stand-in for a client or foreign frame, during
  preview". (b) Skin the stand-in.
- **Recommendation.** (a). The frame it copies is never skinned, and a skinned stand-in would mislead offset tuning. Paint
  the `(test)` mark with `text.muted`, since it is the addon's own annotation. The skin picker's unlock preview will then
  change only the attached elements.
- **Adds.** A standard line (SD-STD) for the new class, the five StandIn rows re-cited, and a small PFE item for the
  `(test)` mark.

## PrettyChat

### U-25 [PrettyChat] `/pc test` report lines in the debug console: does L13 (chat lines) cover them?

- **Evidence.** modules/Override.lua:16-20, :610, :668, :684, :704, :734-753 write green, gold, gray and white labels;
  settings/Panel.lua:147-155 sends them to the console, and the skin picker's preview fills the console with this sample
  (core/SkinSetup.lua:287-296). Since the 2026-11-08 report-routing ruling the report lives in the skinned console, where
  §7 puts content colors on `log.text`. They pass only through the L13 chat rows (tests/run.lua:82-94).
- **Options.** (a) No: the labels read owner tokens following role tokens. (b) Yes: L13 covers them.
- **Recommendation.** (a). Green labels follow `sem.good` or `log.tag`, the gold header `text.heading`, gray a
  `text.muted` owner token, white `note()` dropped for `log.text`; `Const.Color` stays for `NS.Print` chat paths; the
  console report becomes a switch surface.
- **Adds.** A PrettyChat item. A library report-label token pair would serve every addon that writes colored report
  lines (optional).

## QuickComms

### U-26 [QuickComms] Dial slices and hub: carry the skin's statusbar texture, or stay tinted shape art?

- **Evidence.** modules/Dial_Slices.lua:40, :103; modules/Dial_Render.lua:356. No dial surface reads `bar.texture` or the
  Skin tab override, though a pad button does (modules/Pad_Render.lua:770-776). The inventory row
  (FULL_SKINNING inputs/SKIN_DEFAULT_GAPS.csv:587) never got a cause.
- **Options.** (a) Shape art under the icon-shapes Leave class; only the tint follows. (b) The skin's texture masked to
  the sectors.
- **Recommendation.** (a). A masked texture is new work for little visual gain.
- **Adds.** Nothing.

### U-27 [QuickComms] Pad buttons and hub: wear `btn.bg`'s gradient where a skin has one?

- **Evidence.** core/SkinSetup.lua:173, :187-188 follow only the flat blend; Azeroth, Ember, WoW Default and Midnight give
  `btn.bg` a gradient (SkinDefsOthers.lua:230-239, :524, :690, :735, :744, :804). You passed PLOOK-7 (WoW Default, "clear
  red buttons with a soft sheen") with the flat body and the shine.
- **Options.** (a) No change: the bar texture and the shine are the pad button's gradient. (b) Draw the gradient.
- **Recommendation.** (a), recorded as covered by the full-skinning "fuller look" ruling.
- **Adds.** Nothing. (The pad window's own gradient is a GAP, SD-LK-97.16.)

### U-28 [QuickComms] End-preview button: S.Button, or keep the SimPanel step-box look?

- **Evidence.** modules/PreviewWindow.lua:12, :95-98, :155-166, :326-330: Shell plus Font, label colors from LABEL. It
  follows the skin, but as the library SimPanel's step box, a lead's copy of a private library look.
- **Options.** (a) S.Button with `btn.*`, like every other push button. (b) Keep the step-box look.
- **Recommendation.** (a). Under WoW Default it would then be red.
- **Adds.** A QuickComms item.

### U-29 [QuickComms] Callout row's mark-action violet: a category hue, or follow `text.accent`?

- **Evidence.** core/SkinSetup.lua:192-194 `qc.mark`, "a violet no library role holds", read at settings/Groups.lua:307
  (panel scope). Beside it the emote takes the game's chat color and the ping takes `sem.info` (:304-305).
- **Options.** (a) A category hue under §9 Meaning colors. (b) Follow `text.accent`.
- **Recommendation.** (a). It tells the action kinds apart, and it shows only with the Scope cleared.
- **Adds.** Nothing.

## RangeMaster

### U-30 [RangeMaster] Band-mode container border and background: meaning color, or chrome that defaults to the skin?

- **Evidence.** defaults/Profile.lua:87-88 `colorMode = "band"`, border alpha 0.25 (presets 0.1), `bandAlpha` 0.15;
  modules/Container.lua:585-595. Your 2026-11-19 M12 ruling (modules/Presets.lua:91-95) set the alpha, not skin
  precedence; tests/run.lua:90-91 ("never the skin's") is a lead comment. Two rows.
- **Options.** (a) Meaning color: the band tint is the information, like the number's. (b) Chrome: default to `bar.border`
  and `bar.bg`, with Band as opt-in.
- **Recommendation.** (a), recorded as an override.
- **Adds.** Nothing under (a). Under (b), SD-SK-RM.4 and RM.6 grow (companions and FollowOnce keys for both), and the
  spell-chip item SD-SK-RM.10 is unaffected.

## SkillMaster

### U-31 [SkillMaster] Trainer popup cards: take a `list.hover` wash?

- **Evidence.** modules/TrainerPopup.lua:163-164 OnEnter and OnLeave show only a GameTooltip; compare modules/Rows.lua:391.
  No literal is involved: a state is missing, not a value that ignores the skin.
- **Options.** (a) Yes for the cards, which are clicked; no for the journal rows, which are not. (b) Neither.
- **Recommendation.** (a), filed as a SkillMaster enhancement outside #97.
- **Adds.** A GitHub issue on SkillMaster, not a run item.
