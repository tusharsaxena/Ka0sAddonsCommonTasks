# Decisions: the skinning rollout

Calls made during the run, each with its reason, for the owner to review at the smoke test. Cross-cutting calls first; they override an addon inventory's recommendation where the two differ.

## Cross-cutting (lead, 2026-10-29)

- **X1. Near-miss colors keep Ka0s Default's exact pixels** through owner tokens (LK-01), never by snapping to the nearest library token. Snapping would move Ka0s Default by 2 to 8 levels per channel, which O1 rules out without asking.
- **X2. Owner token names are namespaced by the addon** (`dw.upgrade`, `dr.ahead`), and each follows the nearest library ROLE token (a gain follows `sem.good`, a note gray follows `text.muted`, a tooltip hint follows `gtip.muted`), so every skin draws them in its own palette.
- **X3. The `fromSkin` companions default to TRUE** in every addon's defaults, so a new or reset profile follows the skin as an adopted one does after the one-time reset (O2). The reset migration still runs once, as the record. (AT D2, CM, MM, KC, QC, PF, DR, DW.)
- **X4. Only texture, border and font follow the skin on the HUD** (skinning-§6). HUD COLORS the player set (bar fill, background, border color, text color, a class-color highlight) stay the player's and are not reset. (AT D5, QC-G2's highlight default.)
- **X5. The O2 reset visibly changes HUD bars under Ka0s Default** (the Ka0s Default bar, Oxanium, and the skin's border in place of Blizzard Raid Bar, Friz Quadrata and Blizzard Tooltip). That is O2 plus v1.79.0's Ka0s Default, both owner rulings, so it is expected; every affected addon's smoke checks say so.
- **X6. The picker's eye** appears only in an addon with a primary window or a test mode to preview in; otherwise `onPreview` is omitted and only the `settings` icon is declared. The picker opens at login when `skin.pickerSeen` is false and the addon is not stood down; `page = "general"`.
- **X7. Chat output is not a skinned surface.** Chat tags and colored chat lines stay as slash-commands mandates.
- **X8. GameTooltip LINES an addon writes take skin colors** (owner tokens where needed); the frame stays Blizzard's (skinning-§7).
- **X9. Inline content markup** (`|cffffff00` command/path highlights in help text) stays, as LibKa0s's own FormatRow does (PM-G1).
- **X10. QuickComms' callout popup and icon browser** keep the stock settings-window look under Ka0s Default and skin under every other skin (LK-05), honoring the earlier ruling that they match the settings window.

## Per addon

Each addon's implementer applies its inventory's recommendations below unless a cross-cutting call overrides one, and records any change of mind here in its own commit.

### AbsorbTracker

- D1: The R3 reset changes AT's bars on Ka0s Default (Ka0s Default bar texture, borderStyle None size 1, Oxanium instead of Blizzard Raid Bar / Blizzard Tooltip 12 / Friz). This is O2 plus v1.79.0's 'Ka0s Default looks different', not a regression. Recommend: proceed, and say so in the smoke checks and the CHANGELOG.
- D2: Defaults for the composer companions are false (OptionsCompose.lua:516), so a new or reset profile would bring back the pre-skin look. Recommend: default barTextureFromSkin/borderStyleFromSkin/fontFromSkin to true in defaults/Profile.lua and in the composer defaults, and keep the v6 ResetToSkin step as the explicit record.
- D3: No bar.bgTexture token, and bgTexture is a hand-written row. Recommend: barTextureFromSkin governs both textures, and the bgTexture row is disabledIf that companion. No library gap.
- D4: fontFromSkin governs the face only, and borderFromSkin disables only the style picker. Recommend: resolve borderSize from bar.borderSize while borderFromSkin is on (otherwise None plus 12 leaves a 3px inset). Font size and outline stay the player's (equal in Ka0s Default).
- D5: The HUD colors (fill, background, border, text) have no companion, and bar.bg/bar.border are nil in Ka0s Default. Recommend: they stay player settings and are not reset. If the consolidation shows other HUD addons need it, add one collection-wide LibKa0s composer color companion, not one per addon.
- D6: Picker eye: AT has no Test mode, and unlocking is a stored write. Recommend: omit onPreview (no eye) and declare only the 'settings' icon. The alternative is an eye that paints NS.PaintPlaceholder without touching locked.
- D7: The value text shadow literal (modules/Display.lua:224-230) is the font block's on/off shadow, not chrome. Recommend: keep it as a named constant and note it in the #107 review.
- D8: Debug ON/OFF chat colors (core/DebugLogSetup.lua:65) equal sem.goodAlt/sem.badAlt byte for byte. Recommend: leave them literal, because chat is not a skinned surface (E7).
- D9: Picker timing. Recommend: show at OnEnable/PLAYER_LOGIN when skin.pickerSeen is false and the addon is not stood down, with page='general' and the default tab. onClose writes pickerSeen through NS.SetByPath.
- D10: AT already has an 'Appearance' page, and the library tab key is 'Appearance' but its label is 'Skin' (A3). Recommend: no rename; the docs say 'Skin tab on General' and 'Appearance page'.

### AuraMaster

- D1: Border style stays out of the R3 reset and gets no fromSkin companion. bar.borderStyle is 'None' in all nine skins and would strip every Icons border; AM's Solid is a secret-safe strip path. Recommend: reset fonts and bar textures only.
- D2: New-container template defaults barTextureFromSkin, bgTextureFromSkin and fontFromSkin to true, so new containers match migrated ones. Recommend yes; this moves 24 Friz/Blizzard test pins.
- D3: The glow color does not follow glow.color (Ka0s Default's is gold, AM's default glow is black). Recommend: keep it a user color.
- D4: HUD font size and flags do not follow hud.fontSize and hud.outline (no composer companion; per-element sizes are layout). Recommend: keep them user-owned.
- D5: The TEST tag uses sem.warn (exact ff8000), not sem.modeTest (red, LootHistory's). Recommend sem.warn unless the owner wants every TEST mark unified.
- D6: The frame-picker hint |cffaaaaaa uses cover.text (exact 0.667). Recommend cover.text, no new token.
- D7: The |cff808080 settings notes use text.disabled (exact) rather than text.muted (0.7). Recommend text.disabled; the consolidation may want one note-gray token.
- D8: The identity palette for unit, aura type and style stays a rung-4 exception rather than becoming 3-10 tokens. Recommend: exception.
- D9: Chat line colors are out of scope (Blizzard's chat frame; LootHistory precedent). Recommend: exception.
- D10: AM-G2..G9 near-miss colors: new exact tokens (the others FOLLOW text.muted, sem.good/bad, sem.info, sem.warn, text.headingAlt, text.accent) or fold into the nearest token, which changes Ka0s Default by a few percent. Recommend new tokens in the M1 release, merged with other addons' near-misses where they coincide.
- D11: AM-G1 could instead retire AuraMasterDropdown, but the library's makers acquire the schema-row dropdowns, so a host OnRelease cannot restore justification. Recommend the library primitive-option.
- D12: A skin switch in combat restyles the HUD only when combat ends (the apply queue waits under lockdown). Recommend: accept it and note it in the smoke tests.

### BankLedger

- D1 Close control: BL's own 24x24 button with rest 0.85 and hover = player class color (Browser.lua:101-133) vs the skin's close.rest/close.hot. Recommend S.CloseButton on BL's own button (keeps geometry and the mark) and accept the skin tints, as LootHistory did. This changes Ka0s Default's look (class hover lost), so ask the owner.
- D2 rowStripeAlpha/rowHoverAlpha player sliders (Schema.lua:112,119): recommend keeping them, with RGB from list.stripe/list.hover and alpha from the slider (Ka0s Default unchanged). Not HUD, so O2 does not apply; the alternative is to retire them or add a fromSkin companion.
- D3 Store identity palette C.StoreRGB: recommend a rung-4 exception (the addon's own categorical meaning); the owner may move it to rung 2 with four sem.store* tokens.
- D4 Gold movement color: recommend a new token sem.goldAlt (BL-G1) over reusing sem.gold (a 0.05 green shift on Ka0s Default).
- D5 Tab labels: recommend LH's S.Text(label, accent/muted) over tab.onText/tab.text; both equal today's values under Ka0s Default.
- D6 Shell's title.bg band and SortHeaderBar's list.header.bg (bands BL does not draw today): accept them on the 30px main-window title bars and the table headers (LH precedent); the export modal's 26px bar uses Shell{noTopBar=true} + S.TitleBar.
- D7 Insights data bars: recommend S.BarTexture (Ka0s Default bar texture) like LH's NS.SkinBar; keep the legend chip flat.
- D8 Picker onPreview: recommend B:Show plus LT:SetTestMode(true); test mode refuses in combat, so no preview in combat.
- D9 W.QualityColor fallback {0.60,0.60,0.62}: recommend sem.unknown {0.6,0.6,0.6} (same role in LH; reached only for an unknown quality id); no token for a 0.02 shift.
- D10 BL-G2 gtip.valueAlt or gtip.body for the one legend tooltip line: recommend BL-G2 to stay exact; gtip.body is acceptable if the owner wants no token.
- D11 Remove SessionWindow.lua:628's degraded bare-backdrop arm: NS.Browser always loads first, and the Skin degraded facade covers the no-library case.

### ConsumableMaster

- D1: R3 reset on Ka0s Default visibly changes the bar (4px Blizzard Tooltip edges vanish via bar.borderStyle 'None', border/button-edge colors go black, labels Oxanium). Recommend applying O2 as ruled to border styles, labelFont and color keys (with CM-G5); leave sizes/flags/shadow/offset the player's; record the change in smoke tests.
- D2: button fill {0,0,0,0.6}, flyout fill {0,0,0,0.85}, indicator shade {0,0,0,0.8} have no HUD token. Recommend keeping them the player's (outside the R3 list), not a rung-2 gap; fallback literals read the AceDB default.
- D3: the picker's eye needs onPreview, and CM has no test mode. Recommend no onPreview and declaring only the 'settings' icon (alternative: onPreview shows the bar unlocked, and declare 'eye' too).
- D4: unlock wash {1,0.82,0,0.15} equals menu.hover exactly. Recommend menu.hover unless the consolidation finds the wash in 2+ HUD addons, then rung-2 hud.unlockWash.
- D5: 'Macro not created yet' |cff999999 (0.6) equals sem.unknown. Recommend sem.unknown.
- D6: count text (NumberFontNormal) takes hud.font face and hud.outline, keeping its size. Recommend yes.
- D7: label shadow color (0,0,0,1) offset (1,-1) is a legibility constant. Recommend keeping it.
- D8: KCMItemRow 0.4 alpha for non-applicable rows is state, not chrome. Recommend keeping it.
- D9: flyout arrow ChatFrameExpandArrow untinted. Recommend icon.arrow tint, smoke-checked; fall back to an exception if gold-on-yellow reads wrong.
- D10: Profiles page via AceConfigDialog. Recommend Skin:PaintAceTree(owner, container) after each dialog:Open.
- D11: chat colors. Recommend an exception (chat frame is Blizzard's).
- D12: class color vs fromSkin precedence. Recommend the class color wins when its companion is on.
- D13: CM-G1 alternative is to remove KCMIconButton's gold hover, as was done for the score button (test_widgets.lua:115-135). Recommend keeping it with the btn.iconHover token so Ka0s Default does not change unasked.
- D14: CM's own AceGUI acquisitions. Recommend creating through H.AceGUI (the Options proxy) instead of raw AceGUI; the four custom widget types paint themselves from KCM.Skin in OnAcquire/SetDisabled.

### DpsRace

- D-1: HUD/table text {.93,.93,.95} and dim {.62,.62,.68} (also |cff9e9ead) have no exact token. Recommend text.body and text.muted (shift <=.08), no new tokens.
- D-2: Primary/selected buttons ({1,.82,0,.12}/.75) vs btnPrimary ({.2,.16,.03,.95}/.8), and DR's fill/edge dimming when disabled. Recommend accepting btnPrimary and the library's disabled treatment; draw a selected preset as primary.
- D-3: DR's faint white panel wash {1,1,1,.03}/{1,1,1,.10} has no token. Recommend S.Card for KPI boxes and cards, S.Panel for list panels, S.Inset for strip segments; accept the slightly brighter edge.
- D-4: Chips and badges tint a meaning color at .08 fill and .55/.6 edge. Recommend composing from S.Color(token), with the alphas as named Style constants; escalate to an S.Badge primitive only if #107 is read strictly.
- D-5: List and scroll near-values (stripe .025 vs .03, hover white .04 vs gold .10, selection .10 vs .18, new list.header.bg, breakdown track, white scroll thumbs). Recommend accepting the library tokens for one collection-wide list look.
- D-6: HUD colors, sizes, outline and shadow have no fromSkin companion and no bar-fill token. Recommend resetting only faces and textures (R3's wording) and leaving the colors with the player; file a LibKa0s issue if the owner wants color companions.
- D-7: Chart near-values (diagonal vs chart.marker, pace track vs chart.grid, Insights bar blue vs chart.bar, Compare separator vs divider). Recommend accepting the chart tokens.
- D-8: Timeline cover dim .45 vs cover.dim .6. Recommend accepting S.Cover.
- D-9: DR's close control turns gold on hover through the strip; skinning-§7 gives the close tints to the skin (close.hot, red). Recommend S.CloseButton owns the close control (red on hover); the other controls keep gold via text.accent.
- D-10: S.IconBorder would add a black 1px edge (icon.border, set since SkinDefs minor 8) to spell icons that have none today. Recommend no edge on HUD spell icons; use it only on the gear mark edge, which is already black.
- D-11: Countdown fallback number (typed font, GOLD, THICKOUTLINE). Recommend keeping it with the exception.
- D-12: The resize grip takes no owner. Recommend leaving it.
- D-13: S.Checkbox replaces the UICheckButtonTemplate look under Ka0s Default. Recommend accepting it and smoke-checking.
- D-14: The note box's edge is gold even without focus. Recommend S.EditBox (border at rest, gold on focus).
- D-15: Should the monospace race clocks follow the skin under R3? Recommend excluding them from the reset; they draw font.mono only while the player has not picked a face. No library change (otherwise DR-G5).
- D-16: Do the resultsTable.* bar and text groups count as HUD style for the reset? Recommend yes: give them fromSkin and include them in the one-time reset.
- D-17: Default for the *FromSkin companions. Recommend true in defaults/Profile.lua (via the composer's spec.defaults), so new profiles and Restore defaults follow the skin; keep the per-profile migration.
- D-18: The flags box's .06 fill and its .01-off text tints would collapse onto DR-G3's single callout values. Recommend accepting.
- D-19: 'HUD Appearance' (HUD page) and 'Appearance' (General) tab names sit side by side. Recommend keeping both, since the standard fixes the General label.
- D-20: Ka0s Default itself changes at adoption (Oxanium faces, the Ka0s Default bar). Expected per v1.79.0; re-pin golden values and re-look in smoke.

### DropWatcher

- D1 TextButton: compose backdrop from btn.bgAlt/btn.borderAlt (G10) rather than S.Button, because S.Button's hover recolor would overwrite DW's state-toned labels. Recommend compose.
- D2 UIPanelScrollFrameTemplate scroll bars: S.ScrollBar (corridor + flat knob, Ka0s Default's look since SkinDefs minor 10) vs stock. Recommend S.ScrollBar as LootHistory; flag the Ka0s Default change in smoke.
- D3 Title bar: Shell's top bar adds a title.bg band DW never drew. Recommend Shell's top bar (LootHistory parity), or noTopBar=true for zero change; ask in smoke.
- D4 Glow colors: keep as exception E6 (not reset at R3), since one glow.color token cannot carry main vs off-spec. Recommend E6.
- D5 Countdown bar: flat SetColorTexture in token colors, not S.BarTexture (a 3px bar would show texture noise and change Ka0s Default); track chart.track if accepted, else G11. Recommend flat.
- D6 Edit message box keeps ChatFontNormal (it previews a whisper); paint only its box. Recommend keep.
- D7 Tooltip hint gray: its own gtip.hint vs reuse text.idle. Recommend gtip.hint.
- D8 Profiles page AceConfigDialog container: PaintAceTree as LootHistory. Recommend PaintAceTree.
- D9 icons.borderColorFromSkin is a hidden flag (no composer color companion); clear it on the Border color row's onChange. Recommend accept, or fold a color companion into G14.
- D10 Chat colors (prefix, command yellow, ON/OFF) stay. Recommend leave.
- D11 Tab strip: compose label+underline (tab.onText/tab.onLine/text.idle) instead of S.Tab, which would add a tab.bg backing. Recommend compose.
- D12 ~15 new tokens vs snapping DW's chrome grays (G4-G7, G10-G13) to the nearest existing token (deltas <= 0.08/channel or 0.1 alpha) at the cost of a Ka0s Default pixel change. Recommend tokens per O1; semantic ones (G1-G3, G8, G9, G15) are tokens either way.

### KickCD

- D1 (STOP-AND-ASK, alters Ka0s Default): Ka0s Default bar.borderStyle is "None"; KickCD's three border pickers default to "Blizzard Tooltip" 2px, so resetting them to follow the skin erases every icon and cast-bar border on Ka0s Default. Recommend: add the border fromSkin companion but leave it OUT of the R3 reset and default it false; fonts and bar textures take the reset. Consolidator alternative: rule whether Ka0s Default's bar.borderStyle should move off "None" (library minor touching every adopter).
- D2: Companion defaults for new profiles: true for the five font/texture companions, false for the three border companions; set through spec.defaults.<leaf>FromSkin and mirrored in defaults/Profile.lua.
- D3: Reset scope is only the eight picker keys per unit; colors, sizes, flags, shadows, glow colors, label gold stay player settings (no composer companion).
- D4: Charges badge (NumberFontNormal, no setting) follows hud.font face only (size/flags from the font object); becomes Oxanium on Ka0s Default, consistent with v1.79.0.
- D5: GameTooltip:SetText(str) with no color in Spells_Rows.lua:102,207: pass the gtip token equal to the client default (gtip.title gold vs gtip.value white), verified in client, so Ka0s Default is pixel-identical.
- D6: Keep the cast-bar spark (UI-CastingBar-Spark, ADD blend) untouched under every skin.
- D7: Delete the unreachable disabled arm of makeRowIconBtn (0.45 gray tint, Spells_Rows.lua:86-90) rather than add a token.
- D8: AceGUI-missing fallback label (Spells.lua:523, GameFontNormal gold) -> S.Text(fs, "accent").
- D9: Sim descriptor name literal "KickCD" (modules/Sim.lua:346) -> addonName.
- D10: Chat colors (NS.PREFIX cyan, NS.GRAY 9d9d9d, |cff33ff99 list header) exempt as chat output; if ruled in scope, NS.GRAY has no exact token (would become a gap).
- D11: deadenStrip (Panel_Render.lua:265-296) desaturates the skin's tab fills on a linked Focus too; keep (inert must read inert) and re-look in smoke.
- Remove-mark tint {1,0.3,0.3} (Spells_Rows.lua:249) maps to close.hot (exact) rather than sem.danger (1/3, would move a pixel).

### MultiMeters

- D1 Meter window fill and edge (backdropColor 0,0,0,0.75 + 2px Blizzard Tooltip edge) become HUD style reset to the skin's win.* via S.Shell: recommend yes (O2 intends the visible change); alternative leaves the meter window never following a skin
- D2 Header/column-header faces resolve hud.font (the FontGroup companion's token), not font.title: recommend hud.font; MM ApplyTitle must re-run after every Shell repaint
- D3 header.bgColor has no mode: recommend a header.bgColorFromSkin companion (what ResetToSkin sets on a color key) -> title.bg, not reviving a mode
- D4 Header control hover color: recommend btn.hover (gold), rest icon.tint; do not use S.CloseButton for the close control (close.hot is red)
- D5 Transparent/class-tinted backgrounds (columnHeader.bgColor, tooltip.barBgColor): offer skin mode but exclude from the R3 reset so no fill appears
- D6 Cell bars via S.Resolve('bar.texture', ...) + MM's LSM fetch + one OnLooksChanged re-ApplyConfig, not S.BarTexture (which reads secret-valued StatusBars back and keeps records after the companion is unticked)
- D7 Near-miss reds: TEST MODE |cffff2020 -> sem.modeTest (1,0.15,0.15); export warning (0.9,0.25,0.25) -> sem.off (0.9,0.3,0.3): recommend accept rather than two more red tokens
- D8 Export modal adopts S.Button / S.EditBox / S.TitleBar: fill 0.06->0.1, edge alpha .85->.9, icon white->0.85, disabled 0.4->0.5, adds a title.bg band: recommend accept (collection-wide duplicate frame)
- D9 No S.IconBorder on row icons (Ka0s Default icon.border would add a black edge): recommend leave bare
- D10 Keep Tooltip.lua's font swap on GameTooltip TextLeftN lines (restored on teardown) with the tooltip face resolve; flag to the reviewer against skinning-§7
- D11 Meta broadcast rows: add skin to window.colorMode and a meta companion pair broadcasting the per-surface FromSkin companions
- D12 Font sizes and outlines stay the player's (hud.fontSize/hud.outline have no composer companion): recommend not reset
- D13 New windows follow the skin: WINDOW_TEMPLATE and the composer rows' defaults set companions true and modes skin (needs a composer default override or host row patch)
- D14 Stat colors stay meaning (E7), not chart.series
- D15 Diagnostics report escapes stay (chat/copy-window content)
- D16 Use a 'skin' value in MM's existing color modes (resolved in surfaceColor with a token arg; relabel 'Ka0s skin' to 'Skin') rather than per-color FromSkin companions; companions only for composed media pickers and header.bgColor

### PanelMaster

- D1: Are the panels the HUD that O2's one-time reset covers? Recommend NO. They are player-authored content and stay unskinned, PM-03 covers only the unlock overlay, and there is no reset migration (record it in exceptions.tsv). R3 would restyle every saved layout and change Ka0s Default's look: the accent bar would go from Blizzard to the Ka0s Default bar, and the 1px black accent border would become None. Fallback if overruled: opt-in fromSkin companions on the editor's BarGroup and accent BorderGroup, defaulting false, with no reset.
- D2: Should new panels (C.PANEL_TEMPLATE) start in the skin's colors? Recommend NO. No token equals the template fill {0.05,0.05,0.07,0.85}, and the New panels tab already gives the player a house style.
- D3: Unlock outline token. Recommend list.dropLine: Ka0s Default {1,0.82,0,0.9} exact, every skin's accent at 0.9, and it already means 'drag marker'. input.focus is the alternative with the same value. The label uses S.Text(label, 'accent').
- D4: Inline |cffffff00 emphasis in tooltip bodies (PM-G1). Recommend rung 2, the token gtip.emphasis = {1,1,0,1}, if other inventories show the same shape. Otherwise rule it rung 4 content markup. Either way, make one collection-wide ruling.
- D5: Chat output color codes and the [PM] prefix. Recommend an exception: the chat frame is Blizzard's and the prefix is the standard's. Rule it once for the collection.
- D6: The picker's eye (onPreview). PanelMaster has no test mode, and under D1 the skin shows only on the settings pages and the console. Recommend omitting onPreview and declaring only the 'settings' icon. Alternative: also declare 'eye', unused.
- D7: Profile shape for the skin keys. Recommend a top-level profile.skin = {source, skin, ignoreFonts, ignorePanel, font, texture, pickerSeen=false} as skip-render rows through NS.SchemaRuntime.Set. Keep them out of the General page's ordinary rendering and reset rows (settings/PanelSchema.lua view).
- D8: The editor heading's SetFontObject(GameFontNormalLarge) (settings/PanelEditor.lua:260) mirrors the library's O.Section (OptionsWidgets.lua:568). Recommend keeping it in step with O.Section rather than treating it as a #107 finding.

### PartyFrameEnhanced

- D1: PF-G1 'mover.bg' token versus an exception if no other addon has a drag plate. Recommend adding the token, because every movable HUD needs an unlock affordance.
- D2: Resetting borderStyleFromSkin. Ka0s Default bar.borderStyle is 'None', so a player with borderShow=true would lose their border. Recommend setting borderStyleFromSkin=true in the migration only on sections whose stored borderShow is not true.
- D3: bgColor and bar.bg. Recommend leaving bgColor as player data (ColorPair has no fromSkin companion; bar.bg is nil in Ka0s Default).
- D4: Cast-icon edge via S.IconBorder on a new icon holder frame (castbars only, insecure). Invisible in Ka0s Default. Recommend adding it, at low priority.
- D5: The SetShadowColor(0,0,0,1) literal at modules/Element.lua:153 (only when fontShadow is on). It is the client's stock shadow, the same as the library's P.font. Recommend keeping it with a comment.
- D6: The picker's eye. PFE has no test mode; unlock is its preview. Recommend onPreview = NS.SetByPath('locked', false) through the write seam, which leaves the addon unlocked; the alternative is to omit the eye.
- D7: Chat-line color escapes (the [PFE] prefix, ON/OFF, gray refusals). Recommend an exception: the chat frame is Blizzard's and the prefix color is set by slash-commands.
- D8: NS.SKIN and NS.ApplySkin (core/CoreSetup.lua:52-54,107-108) are published with no owner and have no caller. Recommend deleting them and their stub entries rather than binding an owner.
- D9: The EllesmereUIDB read in modules/Providers.lua:315 (stand-in sizing, not the skin gate). Recommend keeping it under its ratified library-stack-§6 register row and adding a line citing skinning-§5's carve-out, so #107 is not raised.
- D10: The default for the companion keys on new profiles. Recommend true (follow the skin), matching O2.
- D11: Adoption changes PFE's Ka0s Default look (the Blizzard bar and Friz become the Ka0s Default bar and Oxanium SemiBold). This is v1.79.0's stated consequence and ruled by O2. Recommend proceeding and recording it in the smoke checks, not stopping.

### PremadeGroupsFilterExtension

- D1 The panel's Ka0s Default look: adopting via today's primitives turns the ratified PGF-matching metal panel (docs/ARCHITECTURE.md:473) into Ka0s slate/gold Oxanium under a PGF dialog that stays metal. Recommend STOP and ask the owner (plan's stop rule); recommend keeping the PGF look on Ka0s Default via PG-G1, the panel following the other eight skins and EllesmereUI.
- D2 The PGF-skin gate condition after PG-06: recommend taking PG-G2 into M1; if declined, a host advisory line on the Filters tab (C_AddOns installed/loaded only, link box), dropping the 'off' state that needs an EllesmereUIDB read.
- D3 Migration of profile.euiSkin (default true, AceDB strips defaults): recommend NS.MIGRATIONS[2] walking db.sv.profiles raw: euiSkin == false -> skin.source 'ka0s'; otherwise 'eui' only when EllesmereUI is present (GetEUIStatus conditions eui ok at OnInitialize), else 'ka0s'; delete euiSkin; SCHEMA_VERSION 1 -> 2.
- D4 Drop PGFE-only EllesmereUI decorations (accent ring, whole-pixel mark, UI_SCALE/DISPLAY_SIZE re-layout, min/max minus/plus glyphs, 12pt box font); keep host geometry (checkbox shrink to 24, 25px EUI header height constant, flush anchor) keyed on GetEUIStatus(owner).painted; re-look under EllesmereUI at smoke.
- D5 Collapse/expand control under a skin: S.PageButton(b, 'up'/'down'); Ka0s Default per D1.
- D6 GameFontHighlight white labels vs text.body 0.9 (no Text role for text.highlight): S.Text(fs,'body') if D1 accepts the flat look, else PG-G1 give-back; typed setLocked/setCopyEnabled colors become S.Color('text.highlight') / S.Color('text.disabled') either way.
- D7 GameTooltip lines: keep white title / gold body (Blizzard convention) as gtip.value / gtip.title, exact today, with a comment on the crossed names.
- D8 Skin tab own-condition hint: opts.label = brand, spec.strings.COND_own_HINT names the folder PremadeGroupsFilterExtension (EllesmereUI's list shows the folder).
- D9 Region preview TextRow fontObject GameFontHighlightLarge: keep (a size to a library maker; colors are player region markup).
- D10 Library repaints recorded frames whatever the stand-down latch (EUISkin refused while stood down, pinned tests/test_disabled.lua:207-226): accept; rewrite the pin to 'nothing built or registered while stood down'; gate the picker on the latch.
- D11 Picker combat retry PLAYER_REGEN_ENABLED vs PGFE's all-events-in-FEATURE_EVENTS rule and the 8-event pin (tests/test_disabled.lua:21-26): recommend LootHistory's one-shot private frame, documented beside the latch.

### PrettyChat

- D1: Add text.note and gtip.note (#aaaaaa) in M1 (PC-G2), not text.muted/gtip.subtle, which would shift Ka0s Default by 9 levels per channel. Recommend the new tokens; three more addons share the gray.
- D2: Tooltip title SetText(label,1,1,1) at settings/Panel.lua:427 becomes S.Color('gtip.value'), exact WHITE on Ka0s Default. The library's own O.AttachTooltip still types 1,1,1, which can be a later library item.
- D3: Keep the /pc test report's markup (brand green and gold) as report content even inside the skinned debug console; the same lines go to chat.
- D4: Keep the console descriptor's font = NS.Const.FONT_MONO (core/DebugLogSetup.lua:193). The console is the library's frame and Ka0s Default font.mono is the same JetBrains Mono; making the console read font.mono for an owner can be a later library item.
- D5: TreeGroup painter's scrollbar under Ka0s Default should use scroll.track like PAINT.ScrollFrame, which differs from stock 0,0,0,0.4. Recommend consistency with other painted AceGUI scrollbars.
- D6: The picker's eye. PrettyChat has no test mode. Recommend onPreview = PrettyChat:TestToConsole() (opens the skinned console with a report) and declaring both eye and settings icons; the alternative is to omit onPreview and declare settings only.
- D7: Skin keys stored at db.profile.skin.{source,skin,ignorePanel,ignoreFonts,font,texture,pickerSeen} with schema paths skin.*, page General, group Appearance, skipRender, declared host-side (custom get/set like every PC row). Check that /pc list does not show 'skin' as a message category.
- D8: Schema.Set's announce runs PrettyChat:ApplyStrings() on every non-sessionOnly write (settings/Schema.lua:837-839, ResetRows :1068). Recommend a row flag (e.g. noReapply) so a skin pick does not re-apply 79 globals.

### QuickComms

- D1: Retire QC's own EllesmereUI bridge (core/EUIBridge.lua, settings/CalloutPopup_Skin.lua, tests/test_eui_skin.lua, harness OPTIONAL_SUITES, Diagnostics.lua:59 / CalloutPopup.lua:467 / IconBrowser.lua:576 callers) in QC-01, applying O4 to the second addon that has one: it registers EllesmereUI.RegisterSkin('QuickComms') exactly as SkinEUI.lua:419 does, so the two collide. Recommend retire; no migration (QC never stored a choice); first-run picker offers EllesmereUI.
- D2: Modal windows on SettingsFrameTemplate: recommend keep the template look under every Ka0s skin via QC-G4 (= PG-G1 stockDefault), paint through the facade so eui reaches EllesmereUI as today, page and controls follow the skin; fallback chrome takes S.Shell. If declined, Ka0s shell under every skin (Ka0s Default change) and ARCHITECTURE rows 260-261 retire.
- D3: Icon browser scroller (IconBrowser.lua:373-384): recommend S.ScrollBar(slider,{track=track}) (Ka0s Default change: Blizzard knob + black .35 track become scroll.thumb/scroll.track) rather than a track token.
- D4: Dial plates/indicator back/border: follow the token's hue (win.bg, win.border) and keep the player's stored opacity; exact under Ka0s Default, no new token. Recommend.
- D5: HUD colors with no exact token (button body/edge #3F3F3F, hub disc .12/.12/.14, other-page dots .4, header/section band colors) stay player style, not reset, no gap. Recommend; alternative is four hud.* tokens.
- D6: Shine overlays (Shine.lua, shine* leaves): player art, not skinned and not reset. Recommend.
- D7: Fold near shades (Ka0s Default shifts slightly): a0a0a0 hints -> sem.neutral; ff6060 -> sem.bad; 19ff19 PREVIEW/TEST marks -> sem.goodAlt; LOCKDOWN {1,.1,.1} -> sem.modeTest; flash dropped {.9,.15,.15} -> sem.modeTest; modal catcher dim .45 -> S.Cover/cover.dim .6 (DpsRace D-8 same); dial end-arrow .4 -> text.disabled. Recommend fold; else tokens text.hint, sem.badSoft, sem.modePreview, sem.lockdown, sem.dropped, cover.modal, icon.off.
- D8: Exact values from another role's token: c9a66b=log.tag (magnifier, Groups group label), #aaaaaa=cover.text (prefer PC-G2 text.note if M1 adds it, else text.muted), b3b3b3=gtip.subtle, .9/.9/.92=sem.stepReady and .6=sem.unknown for the Preview window (it copies the step panels), MARK_GRAY .54 ~ icon.dim .55. Recommend taking the exact token where the role is close; cell hilight and info glyph stay client art.
- D9: Preview window S.Shell adds Ka0s Default's title.bg band at title.height 30 over a TITLE_H 24 layout; recommend S.Shell + move the title into the band (as the perf/sim panels it copies); button via step-panel tokens, not S.Button (which whitens the rest label).
- D10: Debug console descriptor font FONT_MONO (DebugLogSetup.lua:93) equals font.mono in every skin; recommend leave.
- D11: O2 reset moves every pad/dial face from Friz Quadrata to hud.font (Oxanium under Ka0s Default, v1.79.0's ruling); label metrics move pad widths, truncation and dial label ring. As ruled; flag for smoke.

### WhatGroup

- D1: drop the inline |cffFFD700 (1,0.843,0) on the title brand span and the field labels (modules/Frame.lua:859,883,909) and use title.text / text.heading (1,0.82,0). That is a 6/255 green delta. Recommend accepting it, since the Oxanium face change dwarfs it and a new token is sprawl.
- D2: for the field labels, use S.Font(label) with S.Color('text.heading') in one OnLooksChanged reskin function, rather than S.Text(label,'heading'), which switches them to the bold title face. Recommend S.Font plus the token.
- D3: for the |cff888888 placeholders and teleport note (0.533 gray, modules/Frame.lua:610,618,1051-1057,1081,1090), recommend text.disabled (0.5). The delta is 8/255, and it is the role LootHistory uses for 'no value'.
- D4: give the Close UIPanelButtonTemplate button the full S.Button(closeBtn). Under Ka0s Default that replaces the red Blizzard art with the flat control, per the leg-1 'Ka0s Default sets everything' ruling. Recommend the full paint over keepKeys; flag it to the owner as a Ka0s Default look change.
- D5: do not add S.IconBorder to the secure teleport button. Recommend no edge: it is a rung-3/4 exception, and the protected frame should get no new children.
- D6: chat output colors (FFD700 summary labels at core/WhatGroup.lua:811, the green link, the cyan [WG] prefix, the yellow command hints) are not a skinned surface. Recommend leaving them.
- D7: 00_PLAN says 'Skin tab', but skinning-§3 requires the label to be exactly 'Appearance', before Keybindings. Recommend 'Appearance'.
- D8: the skin.* skip-render rows need a schema group, and tests/test_settings.lua:517-569 pins the General partition and the set of group names. Recommend group 'Appearance', or confirm skip-render rows are excluded, and move the test pins in the WG-01 commit.
