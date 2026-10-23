# AbsorbTracker — settings layout analysis

Scope: item 020 (layout only: no key, default, range or behaviour changes). Read from `../AbsorbTracker`
at `master` on 2026-10-24: `settings/{OptionsSetup,General,Appearance,UnitPanel,About,Profiles,Schema,Slash}.lua`,
`core/Units.lua`, `core/Data.lua`, `modules/{Bar,Display}.lua`, `locales/enUS.lua`, `docs/settings-panel.md`,
`docs/schema.md`, `docs/smoke-tests.md`, and the vendored `libs/LibKa0s/{OptionsCompose,Options,OptionsTabs}.lua`
(row labels, `RestoreDefaults`, `disabledReplaces`).

AbsorbTracker is **not** one of the seven addons with a primary window, so the planned General > Keybindings
tab does not apply. It has no bindable action at all (no `Bindings.xml`); the bars are HUD frames toggled by
`/at toggle <unit>`. Nothing in this analysis assumes a Keybindings tab here.

## Current map

Page order is TOC order (`AbsorbTracker.toc:93-101`): the landing page, then General, Appearance, Profiles.
Widget types: CB checkbox, SL slider, DD dropdown, LSM LibSharedMedia dropdown, CP colour picker, BTN button.

```
Ka0s Absorb Tracker (landing)            settings/OptionsSetup.lua:161-163 -> settings/About.lua:23-36 (BuildLandingPage)
  untabbed (options-ui-§13 exemption)
  - logo, tagline (TOC Notes)
  - Section "Slash Commands": one label per NS.COMMANDS row (NS.Slash:LandingRows)

General                                  settings/General.lua:358-410 (CreatePanel :363, RenderTabbedSchema :401)
  Defaults button tooltip: "Restore every General setting on this profile to its addon default." (:366)
  Tab "Master controls"                  composed: H.MasterControls, settings/General.lua:94-128
    [Enable Absorb Tracker  CB enabled]        [General visibility  DD visibility]
    [Master scale           SL scale]          [Master alpha        SL alpha]
    [Lock frame             CB locked]         [Debug console       CB state.debugConsole (session)]
    [Minimap button         CB global.minimap.shown]   (no Test mode: unlock is the preview)
    [Reset position BTN]                       [Reset all settings BTN -> StaticPopup ABSORBTRACKER_RESET_ALL]
                                               (button pair = the composer's afterGroup tail, General.lua:401)
  Tab "Bars"                             settings/General.lua:264-325
    Subsection "Tracked units"
      [Enable Player Bar   CB units.player.enabled]   [Enable Target Bar  CB units.target.enabled]
      [Enable Focus Bar    CB units.focus.enabled]
        tooltip: "Track and display absorbs on your player/target/focus. Target and focus bars additionally
                  need that unit to exist before they appear." (:279-280)
    Subsection "Updates"
      [Update throttle (in sec)  SL throttleWindow  0.05-1 step 0.05, "%.2f sec"]
        tooltip: "Fastest the bar repaints during a burst of changes. Lower = snappier but more CPU." (:315)

Appearance                               settings/Appearance.lua:281-319 (renderer settings/UnitPanel.lua:246-328)
  Defaults button tooltip: "Restore every Appearance setting on this profile to its addon default, on every
                            unit." (:289) — RestoreDefaults ignores ctx.unit (libs/LibKa0s/Options.lua:962-969)
  Chrome band (PageHeader)               settings/UnitPanel.lua:162-219
    row 1: [Unit  DD (session ctx.unit): Player / Target / Focus]          full width
           tooltip: "Which bar the settings on this page apply to. Each unit is styled independently unless
                     it is linked to the Player." (:183)
    row 2 (target/focus only):
           [Use same styling as Player  CB units.<u>.mirror]  [Copy styling from Player  BTN]
  (mirrored unit: every tab shows "Linked to Player — uncheck to customize." instead of its rows, UnitPanel.lua:280-288)
  Tab "Size"                             settings/Appearance.lua:122-147 (hand-written)
    [Bar Width (in px)   SL units.<u>.barWidth  50-500 "%d px"]   [Bar Height (in px)  SL units.<u>.barHeight  10-100 "%d px"]
  Tab "Bar"                              settings/Appearance.lua:157-169 (H.BarGroup)
    [Bar texture  LSM units.<u>.barTexture]   [Bar opacity      SL units.<u>.barAlpha]
    [Bar color    CP  units.<u>.barColor]     [Use class color  CB units.<u>.useClassColorBar]
  Tab "Background"                       settings/Appearance.lua:177-203 (hand-written texture + H.ColorPair)
    [Background Texture  LSM units.<u>.bgTexture]
    [Background color    CP  units.<u>.bgColor]   [Use class color  CB units.<u>.useClassColorBg]
  Tab "Border"                           settings/Appearance.lua:213-226 (H.BorderGroup)
    [Border style  LSM units.<u>.border]       [Border thickness (px)  SL units.<u>.borderSize]
    [Border color  CP  units.<u>.borderColor]  [Use class color        CB units.<u>.useClassColorBorder]
  Tab "Text"                             settings/Appearance.lua:233-248 (H.FontGroup)
    [Font        LSM units.<u>.font]        [Font size        SL units.<u>.fontSize]
    [Font color  CP  units.<u>.fontColor]   [Use class color  CB units.<u>.useClassColorText]
    [Font flags  DD  units.<u>.fontFlags]   [Font shadow      CB units.<u>.fontShadow]
  (hidden group "Link": units.<u>.mirror for target/focus only, skipRender, drawn in the band; Appearance.lua:260-274;
   kept off the strip by untabbedSkipRender, UnitPanel.lua:281)

Profiles                                 settings/Profiles.lua:41-88 (AceDBOptions via AceConfigDialog; untabbed exemption)
```

Counts: **4 pages** (landing, General, Appearance, Profiles); **7 tabs** (General 2, Appearance 5; landing and
Profiles are untabbed); **2 subsections**, both on General > Bars (Tracked units, Updates). **Rendered schema rows:
11 on General** (7 Master controls + 4 Bars) **+ 19 per unit on Appearance** (57 across three units), plus the band's
picker, mirror checkbox and copy button and the two reset buttons. 70 schema rows in all (11 + 57 + 2 mirror rows).
The 19 per-unit rows are exactly `NS.Units.APPEARANCE_KEYS` (core/Units.lua:25-31), which mirror resolution and
`CopyFromPlayer` walk; `enabled` and `mirror` are not in that list and carry `alwaysPerUnit`.

## Problems

| id | file:line | problem |
|---|---|---|
| ABS-P01 | settings/General.lua:264-297; settings/UnitPanel.lua:162-219 | **Turning a bar on and styling it is a two-page task.** `units.<u>.enabled` lives on General > Bars, while everything else about the same bar (size, fill, border, text, mirror, copy) is on Appearance behind the Unit picker. options-ui-§14 names *enable* among the page-wide acts on "the instance the page edits" that belong in the band, and options-ui-§15 says per-instance settings "stay on the instance's own page"; the per-unit enable is exactly that, and it is on another page. The mirror tooltip even says "Position and enable stay independent" about a control the player cannot see from there (UnitPanel.lua:201). |
| ABS-P02 | settings/UnitPanel.lua:120-128, 190-216 | **No indication on Appearance that the selected bar is switched off.** Picking Focus and restyling it while `units.focus.enabled` is false gives no feedback at all; the bar never appears. Follows from P01. |
| ABS-P03 | settings/General.lua:310-312 | **Lonely one-row subsection.** "Updates" holds only *Update throttle*. If P01 moves the three enables out, the whole Bars tab becomes a one-row tab, which General.lua:29-36 itself names as the shape to avoid ("a click that reveals one widget"). |
| ABS-P04 | settings/General.lua:274; settings/Appearance.lua:160 | **"Bars" (General tab) vs "Bar" (Appearance tab).** Two tabs one letter apart on adjacent pages, holding unrelated things (which bars exist vs. the fill's texture/colour). A player told "the Bar tab" cannot tell which. |
| ABS-P05 | settings/Appearance.lua:122-147 | **Lonely two-row tab.** Size holds Width and Height only, one line, and is the tab the page opens on. Width/height describe the bar's frame and are read with the fill, so a whole tab click buys one line. |
| ABS-P06 | settings/Appearance.lua:177-203 | **Background is a three-row tab split from the Bar tab it sits behind.** The backdrop is the unfilled part of the same bar (Display.lua:189-203 draws it under the fill); choosing a fill colour that contrasts with the background needs two tabs flipped back and forth. options-ui-§16 last bullet explicitly allows merging groups onto one tab with a subsection heading per group. |
| ABS-P07 | settings/Appearance.lua:130, 142 | **"Bar Width (in px)" / "Bar Height (in px)"**: Title Case, unlike every composed label on the same page ("Bar texture", "Border thickness (px)"), and "(in px)" differs from the canonical "(px)". |
| ABS-P08 | settings/Appearance.lua:184 | **"Background Texture"**: Title Case; every other label on the page is sentence case. |
| ABS-P09 | settings/Appearance.lua:185 | Background texture tooltip says "LibSharedMedia statusbar texture", which is implementation jargon to a player. |
| ABS-P10 | settings/General.lua:278 | **"Enable Player Bar / Target Bar / Focus Bar"**: Title Case "Bar"; the addon's own strings say "Target bar" (Bar.lua:35, 156, locales "%s bar hidden"). |
| ABS-P11 | settings/General.lua:314 | **"Update throttle (in sec)"**: "(in sec)" differs from the collection's suffix form ("(px)", no "in"). |
| ABS-P12 | settings/UnitPanel.lua:183, 194, 206, 215, 286; settings/Appearance.lua:270-271 | **One concept, five names.** The mirror is "Use same styling as Player" (checkbox), "Linked to Player" (hint), "linked to the Player" (Unit picker tooltip), "Unlinks this unit" (copy tooltip), "Mirror every Player bar appearance setting" (tooltip). The hint's "uncheck to customize" also does not say *what* to uncheck; the checkbox is in the band above, not on the tab. The picker tooltip already says "linked", so "link" is the word the page is closest to. |
| ABS-P13 | settings/UnitPanel.lua:125-128; options-ui-§14 "The band is ONE ROW" | **The chrome band is two rows for Target and Focus** (picker, then mirror checkbox + copy button), and one row for Player, so the strip and every row below it jump down by ~30px when the picker moves off Player. §14 says the band is one row and acts that do not fit go to a `General` first tab. This is a standard deviation today, not recorded anywhere in `docs/`. |
| ABS-P14 | settings/Appearance.lua:131, 143 | Width/height tooltips ("Width of the absorb bar in pixels.") do not say they are per-unit or that Master scale multiplies them; the panel explains the addon-wide/per-unit split only in a code comment (Appearance.lua:154-156). |
| ABS-P15 | libs/LibKa0s/OptionsCompose.lua:400; core/Data.lua; modules/Display.lua:229 | **"Bar opacity" tooltip is wrong for this addon.** The composer's text says "How opaque the bar's fill is", but `barAlpha` is applied as `bar:SetAlpha` on the whole frame (fill, background, border, text and the unlocked drag strip), multiplied by Master alpha. The label is canonical (§16) and the composer's `emit` honours `labels` but has no `tooltips` override (OptionsCompose.lua:156-175), so the host cannot fix the wording without hand-patching a composed row. Upstream item. |
| ABS-P16 | settings/General.lua:94-128 | "Lock frame" (canonical, §15) governs three bars; the addon's own strings say "Lock the bars" (Bar.lua:166). Fixed element, cannot be renamed; noted for the cross-addon list only. |
| ABS-P17 | locales/enUS.lua:58-61; modules/Bar.lua:25, 35, 127; README.md; docs/smoke-tests.md BAR-13 | The drag strip's close-mark tooltip and chat line hard-code the path "General > Bars". Any rename or move of that tab (L01/L06) must carry these strings, the README FAQ and smoke PANEL-3/BAR-4/BAR-13 with it, or the way back points nowhere. |
| ABS-P18 | settings/Appearance.lua:60-62 | Tab order Size > Bar > Background > Border > Text: Size leads "because dimensions are what a player opens this page for". Ordering nit only; resolved by L03/L04. |
| ABS-P19 | settings/General.lua:279-280 | **"Track and display absorbs on your player."** The tooltip is generated from `LABEL[unit]:lower()`, which reads naturally for target/focus and oddly for the player ("your player"). The second sentence ("Target and focus bars additionally need...") is printed on the Player row too, where it does not apply. |
| ABS-P20 | settings/General.lua:315 | Throttle tooltip says "Fastest **the bar** repaints"; the window is one value for all three bars. |
| ABS-P21 | settings/Appearance.lua:289; libs/LibKa0s/Options.lua:962-969 | The Appearance Defaults tooltip ("on every unit") is accurate today, but any row moved onto the page (L01) widens what it resets, and the tooltip has to say so or the button's blast radius changes silently (options-ui-§13 last bullet, §12's reasoning). |
| ABS-P22 | settings/UnitPanel.lua:280-288 | **A mirrored unit's tabs are all replaced by the hint** (`disabledReplaces`). Anything per-unit-but-not-mirrored (enable, the link itself) therefore cannot live on a tab of this page without disappearing for a linked unit: it must be in the band. This is the constraint that decides L01's placement and rules out the §14 `General`-tab escape (see Considered and rejected). |

## Proposed changes

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| ABS-L01 | Move the three rows `units.player.enabled`, `units.target.enabled`, `units.focus.enabled` from General > Bars > Tracked units to the **Appearance chrome band**, drawn bespoke (like the mirror checkbox) for the selected unit only: label `Enable <Unit> bar` (L08). Rows change `page` to `appearance`, gain `skipRender`, move into the hidden band group (rename "Link" → "Unit", still all-skipRender so `untabbedSkipRender` keeps it off the strip), keep key/default/`alwaysPerUnit`/onChange; the bespoke checkbox writes through `NS.SetByPath` so the existing onChange fires. Mirror and copy are unaffected: both walk `APPEARANCE_KEYS`, which does not contain `enabled`. **Consequences the owner must accept (no setting changes, but visible):** (a) the Appearance page's Defaults now also restores the three enables (player on, target/focus off) and General's Defaults no longer does (L15 rewords the tooltip); (b) `/at list` prints the enables under `[appearance / <unit>]` instead of `[general]` (Slash.lua:173, 791-794). | options-ui-§14 (*enable* on the edited instance is a band act) and §15 (per-instance settings stay on the instance's own page). One page now answers "turn the Focus bar on and make it look like this", and P02 disappears because the enable is in view whenever its unit is picked. The band, not a tab, is forced by P22: a linked unit's tabs are replaced by the hint. | 60% | P01, P02, P22 |
| ABS-L02 | If L01 is taken, the Bars tab is left with one row: move `throttleWindow` to **General > Master controls** as an `extra` row (`MasterControls{ extra = {...} }`, `startsLine = true`), after *Minimap button*, before the reset pair; the Bars tab disappears and General draws a one-tab strip. **If L01 is declined:** keep the Bars tab, rename it per L06, and keep both subsections; §7 requires a heading per kind of control, so the one-row "Updates" subsection stays. | options-ui-§15 last bullet permits addon-wide extras through the composer, after the set and before the reset pair, on its own line; the throttle is addon-wide (one window for all bars). Avoids a tab whose only content is one slider. Lower confidence because §15's example of an extra is a player-facing switch, and a CPU knob on Master controls is a judgement call (upstream question below). | 45% (depends on L01) | P03 |
| ABS-L03 | Merge tab **Size** into tab **Bar**: Bar tab gains subsections. Order: subsection "Size" [Bar width][Bar height], then subsection "Fill" holding the composed BarGroup block unchanged (`H.BarGroup{ subgroup = "Fill" }`). Size rows take `group = "Bar"`, `subgroup = "Size"`. | Removes a one-line tab and a click; size and fill are read together. §16 keeps the mandated block contiguous and first *within its subsection*; §7 requires the subsection headings because the tab now mixes kinds, and neither heading repeats "Bar". Update the header comment at Appearance.lua:48-63, which argues the opposite. | 70% | P05, P18 |
| ABS-L04 | Merge tab **Background** into tab **Bar** as a third subsection "Background" after "Fill": [Background texture] / [Background color][Use class color] (`H.ColorPair{ group = "Bar", subgroup = "Background" }`, texture row likewise). Appearance strip becomes **[ Bar ][ Border ][ Text ]**. | The backdrop is the empty part of the same bar; fill and background colours are chosen against each other. §16's last bullet explicitly allows merging groups onto one tab with a subsection heading per group. Three tabs fit one row at any UI scale; the Bar tab grows to 5 lines under 3 headings, still short of a scroll. Two "Use class color" rows on one tab are disambiguated by their headings. | 60% | P06 |
| ABS-L05 | Relabel `barWidth` "Bar Width (in px)" → **"Bar width (px)"**, `barHeight` → **"Bar height (px)"**; tooltips → "Width of this bar, in pixels. Master scale (General) multiplies it." / same for height. | Sentence case and the collection's "(px)" form, as "Border thickness (px)" on the same page; the tooltip names the addon-wide multiplier. | 85% | P07, P14 |
| ABS-L06 | If the Bars tab survives (L01 declined): rename tab "Bars" → **"Tracking"**, subsection "Tracked units" → **"Bars shown"**, "Updates" unchanged; update the "General > Bars" strings (enUS.lua:58-61, Bar.lua:35/127 and the Bar.lua:25 comment) to "General > Tracking". If L01 is taken, the strings instead become **"Re-enable it on the Appearance page or with /at toggle %s."** (and the "%s bar hidden. …" variant). Locale keys are the English strings, so key and value change together. | Ends the Bars/Bar near-collision; the way-back strings must follow the move (P17). | 60% | P04, P17 |
| ABS-L07 | Relabel `bgTexture` "Background Texture" → **"Background texture"**; tooltip → "Texture drawn behind the fill, across the whole bar." | Sentence case; drop LSM jargon. | 90% | P08, P09 |
| ABS-L08 | Relabel `units.<u>.enabled` "Enable Player Bar" → **"Enable Player bar"** (same for Target/Focus). | Matches the addon's own "Target bar" wording everywhere else. | 70% | P10 |
| ABS-L09 | Relabel `throttleWindow` "Update throttle (in sec)" → **"Update throttle (sec)"**; tooltip → "Fastest the bars repaint during a burst of changes. Applies to every bar. Lower = snappier but more CPU." | Unit stated once in the collection's form; scope stated (matters most if L02 moves it). Keep the `%.2f sec` display format: it is the value readout, not the label. | 75% | P11, P20 |
| ABS-L10 | One word for the mirror: checkbox **"Link to Player"**; its tooltip "Use the Player bar's look for this bar (all appearance settings). Position and enable stay this bar's own."; hint **"Linked to Player — untick Link to Player above to customize."**; copy button **"Copy from Player"**, tooltip "Copy the Player bar's look once, then unlink so you can edit it."; Unit picker tooltip unchanged (it already says "linked"). Row label/desc of `units.<u>.mirror` (Appearance.lua:270-271) follow, so `/at list` shows the same words. | Five names for one state become one ("link"), and the hint says which control to use and where it is. Shorter labels also make L11 fit. | 65% | P12 |
| ABS-L11 | **One band row for every unit, four quarter cells**: [Unit DD][Enable <Unit> bar CB][Link to Player CB][Copy from Player BTN]; for Player the last two cells stay empty, so every control sits at the same x and the band height is the same for all three units. Host-only change in `UnitPanel.lua` (`place()` gains quarter anchors; `chromeBlockHeight` returns `BANNER_H` for every unit); checkboxes and button bottom-aligned with the dropdown. Requires L01 and L10 (short labels). **Fallback:** if the cells truncate at the Settings canvas's narrowest width, keep the two-row band and record the §14 deviation (upstream suggestion below). | options-ui-§14 "the band is ONE ROW"; the strip no longer jumps when the picker leaves Player (P13). No library work, unlike the §14 `General`-tab escape (rejected below). Risk: ~150 px cells; "Enable Target bar" and "Copy from Player" must fit without truncation, which needs an in-client look. | 45% (depends on L01, L10) | P13 |
| ABS-L12 | Upstream only (no host change possible): composer `tooltips` override beside `labels`, so "Bar opacity" can say "Opacity of this whole bar (fill, background, border, text); multiplied by Master alpha." | The canonical tooltip misdescribes what this addon's row does (P15). | 70% (as an upstream ask) | P15 |
| ABS-L13 | Per-unit enable tooltips, written per unit instead of from `LABEL:lower()`: Player "Show the Player bar and track absorbs on yourself."; Target "Show the Target bar and track absorbs on your target. It appears only while you have a target."; Focus likewise with "focus". | Removes "your player" and the sentence about target/focus printed on the Player row. Tooltip text only. | 70% | P19 |
| ABS-L14 | With L01 taken, reword the two Defaults tooltips: Appearance → "Restore every Appearance setting on this profile to its addon default, on every unit, including which bars are shown."; General unchanged in text (it still says "every General setting", which stays true). | The button's blast radius widens with L01, and options-ui-§13/§12 require the button to say what it resets; a silent widening is the failure those rules exist for. | 80% (depends on L01) | P21 |

Changes that would also touch docs (not layout, but owed in the same commit): `docs/schema.md` row table
(group/subgroup/page/label columns), `docs/settings-panel.md` page sketch and the chrome-block paragraph (:159-161),
`README.md` (the "General > Bars" FAQ), smoke tests PANEL-3, PANEL-4, BAR-4, BAR-13 wording, the ASCII sketches at
`settings/General.lua:14-27` and `settings/Appearance.lua:10-25`, and the rationale comments at General.lua:67-70
("they stay on the Bars tab") and Appearance.lua:48-63 (one subject per tab), which L01/L03/L04 contradict.
`tests/test_panelpages.lua` / `tests/test_panelmirror.lua` will need their page/group expectations moved.

## Proposed map

With L01, L02, L03, L04, L05, L07, L08 (labels follow), L09, L10, L11, L13, L14 taken; L06 is moot apart from
its string half, because the Bars tab is gone.

```
Ka0s Absorb Tracker (landing)            unchanged
  - logo, tagline
  - Section "Slash Commands": NS.COMMANDS rows

General
  Tab "Master controls"                  (one-tab strip, options-ui-§13)
    [Enable Absorb Tracker  CB enabled]        [General visibility  DD visibility]
    [Master scale           SL scale]          [Master alpha        SL alpha]
    [Lock frame             CB locked]         [Debug console       CB state.debugConsole]
    [Minimap button         CB global.minimap.shown]
    [Update throttle (sec)  SL throttleWindow]                       <- extra, own line (L02, L09)
    [Reset position BTN]                       [Reset all settings BTN]

Appearance
  Chrome band (one row, every unit)                                                                 (L11)
    [Unit DD] [Enable <Unit> bar CB units.<u>.enabled] [Link to Player CB units.<u>.mirror] [Copy from Player BTN]
              (L01, L08, L13)                          (target/focus only; empty cells for Player)   (L10)
  (linked unit: "Linked to Player — untick Link to Player above to customize.")
  Tab "Bar"
    Subsection "Size"                                                                               (L03)
      [Bar width (px)   SL units.<u>.barWidth]     [Bar height (px)  SL units.<u>.barHeight]        (L05)
    Subsection "Fill"
      [Bar texture  LSM units.<u>.barTexture]      [Bar opacity      SL units.<u>.barAlpha]
      [Bar color    CP  units.<u>.barColor]        [Use class color  CB units.<u>.useClassColorBar]
    Subsection "Background"                                                                         (L04)
      [Background texture  LSM units.<u>.bgTexture]                                                (L07)
      [Background color    CP  units.<u>.bgColor]  [Use class color  CB units.<u>.useClassColorBg]
  Tab "Border"
    [Border style  LSM units.<u>.border]           [Border thickness (px)  SL units.<u>.borderSize]
    [Border color  CP  units.<u>.borderColor]      [Use class color        CB units.<u>.useClassColorBorder]
  Tab "Text"
    [Font        LSM units.<u>.font]               [Font size        SL units.<u>.fontSize]
    [Font color  CP  units.<u>.fontColor]          [Use class color  CB units.<u>.useClassColorText]
    [Font flags  DD  units.<u>.fontFlags]          [Font shadow      CB units.<u>.fontShadow]

Profiles                                 unchanged
```

Counts after: 4 pages, **4 tabs** (General 1, Appearance 3; was 7), 3 subsections (Size, Fill, Background; was 2).
Same 70 schema rows, same keys, defaults and ranges. Tasks that drop a page or tab switch: "turn a bar on and
style it" (2 pages → 1), "set size and colour" (2 tabs → 1), "match fill to background" (2 tabs → 1).

If the owner declines L01: General keeps a second tab, renamed "Tracking" (L06), holding "Bars shown"
[Enable Player bar][Enable Target bar] / [Enable Focus bar] and "Updates" [Update throttle (sec)]; L02, L11 and L14
are dropped; the Appearance band stays as today (full-width picker, plus the two-row link/copy row for Target/Focus,
relabelled by L10).

## Considered and rejected

| id | change | why rejected | confidence |
|---|---|---|---|
| ABS-R01 | The §14 escape for P13: a first Appearance tab named **"General"** holding [Link to Player][Copy from Player] (and, with L01, the enable). | `disabledReplaces` replaces every tab of a linked unit with the hint, so the tab holding the unlink control would itself be replaced (P22); it needs an OptionsTabs per-tab exemption, and adds a tab that Player could only draw half of. L11 gets the one-row band without library work. | 25% |
| ABS-R02 | Also merge **Border** into the Bar tab (strip [Bar][Text]). | Four subsections and seven lines on one tab is long enough to scroll, and Border is its own tab in sibling addons; cross-addon consistency wins. | 30% |
| ABS-R03 | Rename tab "Text" → "Font". | The tab holds the value text's settings, and "Text" says what is styled; the name is a cross-addon decision (see notes), not an AbsorbTracker one. | 35% |
| ABS-R04 | Move `throttleWindow` onto the Appearance page. | It is addon-wide; a per-unit page would imply a per-unit value. | 10% |
| ABS-R05 | Rename "Lock frame" to "Lock bars", or move Master scale/alpha next to the per-unit size/opacity rows. | Fixed elements (options-ui-§15: the set may not be renamed or split, and addon-wide rows must not be conflated with per-instance ones). Listed upstream instead. | n/a (forbidden) |

## Cross-addon notes / Upstream suggestions

Cross-addon (same concept, same name and place everywhere):

- **Per-instance enable placement.** AbsorbTracker keeps per-unit enable on General while its per-unit page has a
  picker. Check every addon with a per-instance picker (MultiMeters windows, KickCD/PanelMaster panels, QuickComms
  pads) for the same split; §14 says the instance's enable is a band act and §15 says per-instance settings stay on
  the instance's page. Pick one answer collection-wide.
- **Size tab.** If other addons have a two-row Size/Dimensions tab, fold it the same way (subsection "Size" first
  on the surface's main tab), so "where is width" has one answer.
- **Unit suffixes.** Collection form should be "(px)", "(sec)" — not "(in px)", "(in sec)", "(pixels)". Sweep all
  addons.
- **Sentence case** for every row label (the composers already are). AbsorbTracker has three Title Case strays
  (P07, P08, P10); expect others in hand-written rows elsewhere.
- **Font tab name**: AbsorbTracker calls the FontGroup tab "Text". Check whether siblings say "Text", "Font" or
  "Fonts" and pick one.
- **Mirror / link / copy-from vocabulary**: pick one verb ("link") for "this instance follows another's look"
  across any addon that has it, and one label for the one-shot copy ("Copy from <source>").
- **Throttle/update-rate rows**: if several addons have an addon-wide update-rate knob, place it the same way
  (Master controls extra, or a named tab) everywhere.
- **Defaults tooltips** should list anything non-obvious the page's Defaults resets (here, which bars are shown,
  after L01), in the same sentence shape in every addon.
- **Band geometry independent of the selected instance**: a band whose height changes with the picker (P13) is the
  §13 "geometry must not depend on selection" failure one level up; check every picker page.

Upstream suggestions (WowAddonStandards / LibKa0s):

- **options-ui-§14 one-row band vs. a picker plus two acts.** If L11's quarter cells do not fit, AbsorbTracker's
  two-row band is the readable shape and the §14 escape is worse here (R01). Suggest: allow a second band row when
  it holds only acts on the selected instance and the band height is the same for every instance, or state that the
  escape tab is exempt from `disabledReplaces`.
- **options-ui-§13/§14: the band's height MUST NOT depend on the selected instance**, mirroring the strip's
  selection-independence rule.
- **LibKa0s OptionsCompose: a `tooltips` override** beside `labels`, for when a canonical label is right but the
  canonical tooltip misdescribes the host's wiring (Bar opacity applied as frame alpha, P15).
- **LibKa0s OptionsTabs: per-tab exemption from `disabledReplaces`** if the §14 escape is ever taken on a
  linked-instance page.
- **options-ui-§15 extras**: say whether an addon-wide performance knob (update throttle) is a fit for the
  `extra` slot, or name where such rows go, so addons do not each decide.
- **options-ui-§15 "Lock frame"** reads oddly in an addon with several frames ("Lock the bars" in its own
  strings). Consider allowing a plural form ("Lock frames") or leaving it; flagged, not violated.

## Review

Independent review, 2026-10-24, against `../AbsorbTracker` `master` (code read directly, not from the draft).

- **Current map verified** row by row against General.lua, Appearance.lua, UnitPanel.lua and the composer. Fixed:
  "2 + 2 subsections" was wrong (there are 2, both on General > Bars); TOC range is 93-101; added the two Defaults
  tooltips, the Unit picker tooltip, the enable/throttle tooltips, the reset pair's afterGroup source, the
  Link group being target/focus only, and the `APPEARANCE_KEYS` fact that keeps L01 from touching mirror/copy.
  Dropped the unverified claim that the "%d px" readout states the unit twice (it is a value readout, not a label).
- **Setting-change check.** No proposal changes a key, default, range or behaviour of a setting. L01 does change
  which page's Defaults button resets the three enables and how `/at list` groups them; both are now stated as
  explicit consequences, with L14 added so the Appearance Defaults tooltip says what it resets. L01's confidence
  raised 55% → 60%: mirror and copy are confirmed unaffected, and §15 backs the move, but the Defaults side effect
  keeps it from going higher.
- **Standard check.** L01 now cites §15's per-instance bullet as well as §14; L02 checked against §15's `extra`
  terms (after the set, before the reset pair, own line, addon-wide): compliant. L03/L04 checked against §13
  ("one tab per section") and §16's last bullet, which permits merged groups with subsection headings. P13 restated
  as an unrecorded deviation.
- **Added problems** P19 (player enable tooltip "your player", target/focus sentence on the Player row), P20
  (throttle tooltip singular), P21 (Defaults tooltip blast radius), P22 (`disabledReplaces` forces per-unit
  non-mirrored controls into the band); P12 extended to five names (picker tooltip). Added changes L13 (enable
  tooltips) and L14 (Defaults tooltip).
- **L11 rewritten**: the old library-dependent `General`-tab escape (35%) moved to Considered and rejected as R01,
  replaced by a host-only one-row, four-cell band (45%) that also removes the per-unit band-height jump.
- **Recalibrated**: L04 55% → 60% (§16 explicitly allows it); added "Considered and rejected" with R01-R05.
- **L06** way-back string for the L01 case reworded to a full sentence; L09 tooltip made concrete.
- Added cross-addon notes on Defaults tooltips and selection-independent band height, and a matching upstream rule.
