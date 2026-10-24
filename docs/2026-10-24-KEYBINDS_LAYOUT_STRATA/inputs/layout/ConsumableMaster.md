# ConsumableMaster — settings layout analysis

Scope: item 020, layout only. No setting key, default, range, behaviour or row set changes. Read from
`../ConsumableMaster` on 2026-10-24: `settings/{OptionsSetup,Panel,OptionsShim,General,Category,CategoryAddByID,StatPriority,MacroBar,Profiles}.lua`,
`defaults/{Categories,Profile}.lua`, `docs/settings-panel.md`, `docs/macro-bar.md`, the vendored
`libs/LibKa0s/OptionsCompose.lua` (composer labels and line shapes), and `options-ui.md` §5-§18.

**Keybindings (item 015).** ConsumableMaster is not one of the seven addons with a primary window. It has no
`Bindings.xml` and no window toggle, so the planned General > Keybindings tab does not apply. Its General page
keeps two tabs. (The macros it writes are bound through the player's own action bars, and the macro bar's
buttons are secure action buttons that nothing binds today. Binding them would be a feature, not part of 015.)

Widget legend: CB checkbox, SL slider, DD dropdown, LSM shared-media dropdown, CP colour picker, BTN button,
RL reorder list (LibKa0s `ReorderList`), LBL label, ID `IdInput` (edit box + Add + status line).
`[a][b]` is one two-column line. `[a][ ]` means the second cell is empty.

## Current map

Sidebar order is `KCM.Settings.order` (`settings/Panel.lua:51-53`): landing, General, Macros, Stat Priority,
Macro Bar, Profiles.

```
Ka0s Consumable Master (landing)      settings/Panel.lua:1051-1064 (Helpers.BuildAboutContent -> BuildLandingPage)
  untabbed (options-ui-§13 exemption): logo, TOC notes, Heading "Slash Commands", one LBL per /cm row

General                               settings/General.lua:425-436 (CreatePanel :429, RenderTabbedSchema :421)
  Tab "Master controls"               composed, H.MasterControls settings/General.lua:182-206
    [Enable Consumable Master CB enabled]          [General visibility DD visibility]
    [Master scale SL scale]                        [Master alpha SL alpha]
    [Lock frame CB macroBar.locked]                [Debug console CB state.debugConsole (session)]
    [Minimap button CB global.minimap.shown]       [ ]                        (no Test mode: unlock is the preview)
    [Reset position BTN]                           [Reset all settings BTN -> KCM_CONFIRM_RESET]
  Tab "Maintenance"                   host tab, drawMaintenance settings/General.lua:390-411, TAB_OPTS :413-417
    [Force resync BTN]                             [Force rewrite macros BTN]
    [Reset all priorities BTN -> KCM_RESET_PRIORITIES]

Macros                                settings/Category.lua:1125-1146 (CreatePanel :1132; strip renderMacros :1080-1108)
  Strip: 15 tabs from KCM.Settings.macroOrder (settings/Panel.lua:69-74), wraps to 2 rows
    Food | Drink | Healing Potion | Mana Potion | Healthstone | AIO Health | AIO Mana |
    Flask* | Combat Potion* | Stat Food* | Weapon Enchant* | Augment Rune | Vantus Rune | Bloodlust | Battle Rez
    (* = spec-aware; tab tooltip "Priority list and add-by-ID for the %s macro." on ALL 15, :1045)
  Single-category tab (13 tabs)        renderSingle settings/Category.lua:817-863
    (no heading) macro drag icon                                    renderCategoryHeader :432-462
    (spec-aware only) LBL "Spec-aware. Viewing: <spec>."            :436-440
    (Battle Rez only) [Cast on mouseover CB categories.BATTLE_REZ.mouseover]   :446-460 (bespoke, row :226-230)
    Section "Add item or spell by ID"                               settings/CategoryAddByID.lua:359
      [Type DD (session O._addKind) 40%]                            :361-373
      [ID, link or name  ID + Add BTN + status]                     :375-382
    Section "Priority list"                                         settings/Category.lua:840
      LBL glyph legend (in bags / not in bags / picked [MH/OH])     :505-517
      RL priority rows: handle | item | score (i) | Remove           :632-680 (bespoke, no schema row)
    [Reset category BTN -> KCM_RESET_CATEGORY]                      :847-853
  Composite tab (AIO Health, AIO Mana)  renderComposite settings/Category.lua:972-1012
    (no heading) macro drag icon                                    :983
    LBL "Composite macro. Toggle and order ..."                     :986-988
    LBL legend (in bags / not in bags)                              :993
    Section "In Combat"     RL rows: handle | pick | [Enabled CB]   :939-970 (rows categories.<K>.enabled / .orderInCombat)
    Section "Out of Combat" RL rows: handle | pick | [Enabled CB]   (categories.<K>.orderOutOfCombat)
    [Reset category BTN]                                            :1002-1006

Stat Priority                         settings/StatPriority.lua:746-758 (CreatePanel :750, render :690-744)
  Banner: [Viewing spec DD (session O._viewedSpec)]                 :702-714
  Strip: 1 tab "Priority"                                           :721-732
    [Primary stat DD, full width]   (part of row statPriority)      :660-671
    Section "Secondary stats"                                       :674
      LBL "Drag to rank. ..."                                       :675
      RL 4 secondary stats: handle | tick/cross | name               :676-679
    [Reset stat priority BTN]                                       :682-686

Macro Bar                             settings/MacroBar.lua:1167-1178 (CreatePanel :1172; strip render :1140-1165, TABS :1116-1125)
  Tab "General"                       drawGeneral :1095-1102
    [Enable macro bar CB macroBar.enabled]          [ ]                        :119
    [Reset slot order BTN]                                                     :1097-1101
  Tab "Layout"
    [Buttons per row SL macroBar.perRow]            [Button size SL macroBar.buttonSize]       :141, :148
    [Button spacing SL macroBar.spacing]            [Bar padding SL macroBar.padding]          :153, :158
    [Bar scale SL macroBar.scale]                   [Orientation DD macroBar.orientation]      :166, :171
    [Horizontal growth DD macroBar.growthH]         [Vertical growth DD macroBar.growthV]      :177, :183
  Tab "Bar appearance"
    Sub "Opacity"     [Bar opacity SL macroBar.alpha] [ ]                                      :202
    Sub "Background"  [Bar background CB macroBar.barBackdrop] [ ]                             :208
                      [Bar background color CP macroBar.barBackdropColor][Use class color CB macroBar.useClassColorBarBackdrop]  :214
    Sub "Border"      [Bar border CB macroBar.barBorder] [ ]                                   :232 (BorderGroup)
                      [Border style LSM macroBar.barBorderStyle][Border thickness (px) SL macroBar.barBorderSize]
                      [Border color CP macroBar.barBorderColor][Use class color CB macroBar.useClassColorBarBorder]
  Tab "Button appearance"
    Sub "Background"  [Button background CB macroBar.buttonBackdrop] [ ]                       :266
                      [Button background color CP macroBar.buttonBackdropColor][Use class color CB ...useClassColorButtonBackdrop]  :272
    Sub "Border"      [Button border CB macroBar.buttonBorder] [ ]                             :290 (BorderGroup)
                      [Border style LSM ...buttonBorderStyle][Border thickness (px) SL ...buttonBorderSize]
                      [Border color CP ...buttonBorderColor][Use class color CB ...useClassColorButtonBorder]
                      [Border offset (px) SL macroBar.buttonBorderOffset] [ ]                  :311 (extra)
    Sub "Icon"        [Icon zoom (%) SL macroBar.iconZoom][Show stack count CB macroBar.showCount]   :330, :336
                      [Show tooltips CB macroBar.tooltips][Show GCD swipe CB macroBar.showGCD]       :342, :348
  Tab "Labels"
    Sub "Text"        [Show button labels CB macroBar.buttonLabel][Label text DD macroBar.labelText] :360, :366
    Sub "Layout"      [Label position DD macroBar.labelPoint][Label placement DD macroBar.labelPlacement] :375, :391
                      [Label offset X (px) SL macroBar.labelOffsetX][Label offset Y (px) SL macroBar.labelOffsetY] :397, :403
    Sub "Font"        [Font LSM macroBar.labelFont][Font size (% of button) SL macroBar.labelScale]  :409 (FontGroup)
                      [Font color CP macroBar.labelColor][Use class color CB macroBar.useClassColorLabel]
                      [Font flags DD macroBar.labelFlags][Font shadow CB macroBar.labelShadow]
  Tab "Flyout"
    Sub "Layout"      [Enable flyout CB macroBar.flyout][Flyout side DD macroBar.flyoutPoint]        :459, :465
                      [Reverse flyout order CB macroBar.flyoutInvert][Maximum flyout entries SL macroBar.flyoutMax] :471, :476
                      [Flyout button size (% of button) SL macroBar.flyoutScale][Flyout spacing (px) SL macroBar.flyoutSpacing] :482, :488
                      [Flyout padding (px) SL macroBar.flyoutPadding][Gap from button (px) SL macroBar.flyoutGap] :494, :500
                      [Auto-close after (seconds) SL macroBar.flyoutAutoClose] [ ]                   :506
    Sub "Background"  [Flyout background CB macroBar.flyoutBackdrop] [ ]                            :512
                      [Flyout background color CP ...flyoutBackdropColor][Use class color CB ...useClassColorFlyoutBackdrop] :518
    Sub "Icon"        [Shaded band thickness (% of icon) SL macroBar.flyoutIndicatorScale][Arrow size (% of band) SL macroBar.flyoutArrowScale] :533, :539
                      [Shaded band color CP macroBar.flyoutShadeColor][Use class color CB ...useClassColorFlyoutShade] :545
  Tab "Visibility"
    [Combat visibility DD macroBar.combatMode]      [Fade unless hovered CB macroBar.fadeUnlessHover]  :563, :572
    [Faded opacity SL macroBar.fadeAlpha]           [ ]                                                 :577
  Tab "Buttons"                       drawButtons :1104-1110
    LBL "Drag a button by its handle ..."
    RL shown slots | rule | hidden slots (dimmed)   rows macroBar.order + macroBar.shown (:596, :601)

Profiles                              settings/Profiles.lua:139-152 (AceDBOptions via AceConfigDialog; untabbed exemption)
```

**Counts.** 6 panels (landing + 5 sub-pages). 26 tabs (General 2, Macros 15, Stat Priority 1, Macro Bar 8).
79 schema rows (7 Master controls, 7 Macros, 1 Stat Priority, 64 Macro Bar; the Macro Bar split is pinned by
`tests/test_schema.lua:511-518`: General 1, Layout 8, Bar appearance 9, Button appearance 13, Labels 12, Flyout 16,
Visibility 3, Buttons 2). The row engine draws 69 of them on screen (7 Master controls + 62 Macro Bar); the other
10 (7 Macros, 1 Stat Priority, the 2 Buttons rows) are drawn by bespoke controls or are whole-value rows behind a
list. There are 7 host buttons outside the composer (Maintenance x3, Reset category, Reset stat priority, Reset
slot order, Add), plus the composer's 2 resets.

## Problems

| id | where | problem |
|---|---|---|
| CON-P01 | settings/Category.lua:436-440, settings/StatPriority.lua:702-714 | **The spec picker for the four spec-aware Macros tabs is on a different page.** Flask, Combat Potion, Stat Food and Weapon Enchant show "Spec-aware. Viewing: X." with no control. To edit your other spec's Flask list you open Stat Priority, change the banner, go back to Macros and find Flask again. That is the worst page-switching path in the addon, and it is the addon's main task. |
| CON-P02 | settings/Category.lua:438 | The spec line does not say where the spec is changed, so a player who has not found the Stat Priority banner cannot change it at all. |
| CON-P03 | settings/StatPriority.lua:704 | The banner tooltip lists the spec-aware tabs as "Stat Food, Combat Potion, Flask and Weapon Enchant". The strip order is Flask, Combat Potion, Stat Food, Weapon Enchant. |
| CON-P04 | settings/MacroBar.lua:1095-1102 | Macro Bar > **General** is a one-row tab (Enable macro bar, with an empty second cell) plus a button. You click a tab to reach one checkbox. |
| CON-P05 | settings/MacroBar.lua:1097-1101 vs :1104-1110 | **Reset slot order** is on General, but slot order is edited on **Buttons**, six tabs away. The order row's own tooltip (:599) sends the player to the Buttons tab. |
| CON-P06 | settings/MacroBar.lua:563-581 | **Visibility** is a three-row tab with a lone **Faded opacity** on the second line. It is a small subject that belongs with the bar's on/off switch (QuickComms made the same move on 2026-10-20: Visibility, Fade and Faded alpha moved under General's Visibility heading). |
| CON-P07 | settings/MacroBar.lua:202-207 vs :577-581 | **Opacity is split across tabs.** *Bar opacity* (the unfaded alpha; its tooltip says "when it is not faded out") is alone under Bar appearance > Opacity, and *Faded opacity* is on Visibility. They are the two ends of one fade, and you can't compare them without switching tabs. |
| CON-P08 | settings/MacroBar.lua:202 | Bar appearance > **Opacity** is a one-row subsection (lonely heading, empty second cell). |
| CON-P09 | settings/MacroBar.lua:141-188 | **The Layout tab's pairing ignores the mental model.** The lines are [per row][button size] / [spacing][padding] / [**bar scale**][**orientation**] / [growth H][growth V]. Orientation decides what "per row" means (row or column), so it belongs on the same line as per row. Bar scale has nothing in common with orientation. |
| CON-P10 | settings/MacroBar.lua:141-188 | Layout mixes dropdowns (orientation, growth) and sliders (sizes) with no subsection headings. options-ui-§7 requires headings on a tab that mixes control types. Visibility (DD + CB + SL) has the same gap. |
| CON-P11 | settings/MacroBar.lua:148-161 | Units are inconsistent. *Button size*, *Button spacing* and *Bar padding* are pixels with no "(px)", while the Flyout tab's *Flyout spacing (px)*, *Flyout padding (px)* and *Gap from button (px)*, plus *Border offset (px)* and *Label offset X (px)*, all carry it. |
| CON-P12 | settings/MacroBar.lua:342-347 | *Show tooltips* sits under Button appearance > **Icon**. It is a hover behaviour for the whole bar, not a property of the icon. |
| CON-P13 | settings/MacroBar.lua:377, :465 | The subsection name **"Layout"** is used on Labels and on Flyout, on a page that also has a **Layout** tab. "Labels > Layout" and "Layout" read as the same place. |
| CON-P14 | settings/MacroBar.lua:533-559 | Flyout > **"Icon"** covers the shaded band and the arrow drawn on the *bar button*, not the flyout's icons. Button appearance has an "Icon" subsection too, which really is about icons. |
| CON-P15 | settings/MacroBar.lua:459-511 | Flyout > Layout puts nine rows of two different kinds under one heading: behaviour (enable, auto-close, max entries, reverse order) and geometry (side, size, spacing, padding, gap). *Enable flyout* is paired with *Flyout side*, and *Auto-close after* closes the block alone. |
| CON-P16 | settings/MacroBar.lua:518-531; modules/MacroBarFlyout.lua:407-419, :463 | Two **hidden cross-tab dependencies**. Flyout entries take the *whole Button appearance block* (background, border, icon zoom), and the flyout panel's border takes the *Bar appearance* border. Only the second is stated, and only inside one swatch's tooltip. A player restyling the flyout looks for those controls on the Flyout tab. |
| CON-P17 | settings/MacroBar.lua:565-570 vs libs/LibKa0s/OptionsCompose.lua:73-79 | **Combat visibility** labels its values *Always visible / Hide in combat / Only in combat*. The Master controls' *General visibility*, which it is intersected with, says *Always / Only in combat / Only out of combat*. The same idea has different words and a different order, and one says "Hide in combat" where the other says "Only out of combat". |
| CON-P18 | settings/General.lua:182-206; OptionsCompose.lua:482-491 | The canonical tooltips are generic: *Lock frame* says "Stop the frame being dragged", *Master scale* says "Scales the whole addon's display". The addon has exactly one frame, the macro bar, whose *own* scale/opacity/visibility sit on another page and multiply with these. Nothing on General says so (the Macro Bar rows' tooltips do, :169, :206, :570). |
| CON-P19 | settings/Category.lua:1045 | Every Macros tab tooltip says "Priority list and add-by-ID for the %s macro.", which is wrong on the two composite tabs: they have neither, only In combat / Out of combat order. |
| CON-P20 | settings/CategoryAddByID.lua:359 | The section heading "**Add item or spell by ID**" undersells the control. The box takes an ID, a shift-clicked link or a name (its own label at :378 says "ID, link or name"). |
| CON-P21 | settings/Category.lua:432-462 | The block above the first section (drag icon, spec line and, on Battle Rez, the **Cast on mouseover** checkbox) has no heading. The only schema-backed setting on a single-category tab floats between the icon and "Add item or spell by ID" and reads as part of the Add block. |
| CON-P22 | settings/Category.lua:930-931 | Section headings "**In Combat**" / "**Out of Combat**" are Title Case. Every other heading in the addon is sentence case ("Priority list", "Secondary stats", "Add item or spell by ID"). |
| CON-P23 | settings/Category.lua:894 | The per-row include checkbox on composite tabs is labelled "**Enabled**". It collides with the addon-wide *Enable Consumable Master* and *Enable macro bar*, and it says nothing about what it enables (inclusion in this macro). Its tooltip says "Include %s in the macro body." |
| CON-P24 | settings/Category.lua:894 vs settings/StatPriority.lua:458-475, settings/MacroBar.lua:886-896 | Three in-list include toggles use two control shapes in one addon: a CheckBox on composite rows, and a tick/cross glyph on Stat Priority and Macro Bar > Buttons. (Changing the widget is beyond 020's latitude; recorded for the owner.) |
| CON-P25 | settings/StatPriority.lua:660-675 | Stat Priority's tab is asymmetric. *Secondary stats* has a heading, but the *Primary stat* dropdown above it does not, so the page reads as one unlabeled control and then a section. |
| CON-P26 | settings/StatPriority.lua:683 | "**Reset stat priority**" does not say its scope (the viewed spec only; its tooltip does). On the Macros tabs the equivalent button's tooltip appends "(viewed spec only)". |
| CON-P27 | settings/Panel.lua:69-74 | The Macros strip has 15 tabs and wraps to two rows (options-ui-§13 SHOULD fit one). Healthstone (an AIO Health member) sits after Mana Potion, away from Healing Potion. The order mirrors the default `macroBar.order` (`defaults/Profile.lua:246-251`), so a reorder would break that stated mirror. |
| CON-P28 | settings/Category.lua:1138-1141 | **Behaviour, not layout:** the Macros page's top-right **Defaults** button resets only the *active tab's* category (`promptResetCategory(activeCategory)`). options-ui-§13 says "The per-page Defaults button stays page-wide ... MUST NOT narrow to the visible tab." It also duplicates each tab's inline *Reset category*. Out of 020's latitude; flagged for the owner / an audit. |
| CON-P29 | settings/Category.lua:700, settings/StatPriority.lua:155, :738 | Three wordings for nearly the same empty state: "No active spec." (Macros), "(no active spec)" (picker), "No spec selected." (Stat Priority). The first and third describe different causes, but the player can't tell that from the words. |
| CON-P30 | settings/MacroBar.lua:352 | The *Show GCD swipe* tooltip is a 90-word paragraph. The setting is a simple toggle, and the caveat (a real cooldown's last second is hidden too) gets lost. |
| CON-P31 | settings/MacroBar.lua:1116-1125 | **Buttons** (which macros are on the bar, and in what order) is the last tab, yet it is what a new player decides first. The source comment (:1065-1066) calls it "set once and left", which is also true of Layout. (Nitpick; see CON-L19.) |
| CON-P32 | settings/MacroBar.lua:1116-1125 | Two appearance tabs (Bar and Button) split one restyling task: to make the bar and its buttons match, you edit two borders and two backgrounds on two tabs. The qualifiers are justified (`docs/settings-panel.md:391-392`), but the split costs a tab switch on the commonest styling task. (See CON-L20, low confidence.) |
| CON-P33 | settings/General.lua:401-410 | *Reset all priorities* sits alone under two troubleshooting buttons. A data reset that wipes added/blocked/pinned items shares a tab with two "fix stale macros" verbs. It is acceptable (all three are one-shot acts), but the tab name "Maintenance" covers only the first two. |
| CON-P34 | settings/MacroBar.lua:1099 | *Reset slot order*'s tooltip says "Restore the default **left-to-right** slot order". With *Orientation: Vertical* the order runs top to bottom, so the tooltip is wrong for half the layouts. |
| CON-P35 | settings/MacroBar.lua:577-581; modules/MacroBar.lua:385-396 | *Faded opacity* is multiplied by Master alpha too (`applyAlpha`: `fadeAlpha * m`), but only *Bar opacity*'s tooltip says so. The faded end of the fade gives no hint that a General-page slider also dims it. |
| CON-P36 | settings/Category.lua:703 | The empty priority list says "Add an **itemID** above". The block above takes an item **or a spell**, by ID, link or name. It is out of step with its own section and with CON-L17. |
| CON-P37 | settings/Category.lua:1004 | The composite *Reset category* tooltip says "Restore **enabled flags** and section order to defaults". "Enabled flags" is internal wording, and after CON-L22 the checkbox it refers to is not labelled "Enabled" any more. |
| CON-P38 | modules/MacroBarFlyout.lua:416-433, :380-391; modules/MacroBarButton.lua:156-161 | CON-P16 understates what the flyout borrows. Entries take **everything** on Button appearance: background, border **including Border offset**, icon zoom, **Show stack count** and **Show GCD swipe**. *Show tooltips* governs their tooltips too. Listing only "background, border and icon zoom" in a tooltip would teach the player a wrong subset. |
| CON-P39 | settings/MacroBar.lua:141-146 | *Buttons per row* means a **column** when Orientation is Vertical (its tooltip says so). The label is wrong for one of the two orientations. |

## Proposed changes

The proposed map applies every change at **≥ 55%** confidence. Changes below that are alternatives for the owner
and are not in the map. "Row" means a schema row whose `group`/`subgroup`/declaration order moves. No path,
default, range or behaviour changes.

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| CON-L01 | Reword the spec line on the four spec-aware Macros tabs (settings/Category.lua:438) from "Spec-aware. Viewing: %s." to "Spec-aware. Showing the list for %s. Change the spec in the Stat Priority page's banner." | Tells the player where the one picker is, without a second picker (options-ui-§14 forbids a mirror). | 85% | P02, part of P01 |
| CON-L02 | **Owner call.** Fold the Stat Priority page into the Macros page as a 16th tab, **Stat priority**, placed just before **Flask**, and move the **Viewing spec** banner (settings/StatPriority.lua:702-714) to the Macros page's chrome band. The banner is shown on every Macros tab, with the tooltip "Applies to the spec-aware tabs: Flask, Combat Potion, Stat Food, Weapon Enchant, and to Stat priority." The sidebar drops to 4 pages. | Removes the cross-page spec round trip (P01) at its root: picker, stat ranking and the four lists it governs sit on one page. Against it: the banner is idle on 11 tabs, the strip grows to 16, and the page's Defaults button (already off-rule, P28) would need a page-wide meaning. Needs `KCM.Settings.order` and `RegisterTab` changes, no data change. For it: options-ui-§14 says a page that edits one instance out of many MUST say which one with a banner carrying the picker, and today four Macros tabs retarget silently from another page's banner, which is the case §14 was written against. | 50% | P01, P25 (by giving the page a real tab label) |
| CON-L03 | Reword the Stat Priority banner tooltip (settings/StatPriority.lua:704) to list the tabs in strip order: "Flask, Combat Potion, Stat Food and Weapon Enchant". | Matches what the player sees. | 90% | P03 |
| CON-L04 | Move row **Show tooltips** (`macroBar.tooltips`, MacroBar.lua:342) from Macro Bar > Button appearance > Icon to Macro Bar > **General**, as the right half of the first line, beside *Enable macro bar*. | It is a bar-wide hover behaviour (it also gates the flyout entries' tooltips, MacroBarFlyout.lua:226-229), and the move fills General's empty second cell. | 60% | P04, P12 |
| CON-L05 | Move rows **Combat visibility** (`macroBar.combatMode`), **Fade unless hovered** (`macroBar.fadeUnlessHover`) and **Faded opacity** (`macroBar.fadeAlpha`) from the Visibility tab to Macro Bar > **General**, under a new subsection **Visibility**, after *Enable macro bar / Show tooltips*. Delete the now-empty **Visibility** tab (8 tabs to 7). | Whether and when the bar shows is one subject with its on/off switch, and it gives General real content. It matches QuickComms' 2026-10-20 owner-requested move. | 75% | P04, P06 |
| CON-L06 | Move row **Bar opacity** (`macroBar.alpha`) from Bar appearance > Opacity to General > Visibility, on the line after *Combat visibility / Fade unless hovered*, paired as [Bar opacity][Faded opacity]. Drop the **Opacity** subsection. | Both ends of the fade sit side by side, and the lonely one-row subsection goes. Against it: *Bar opacity* applies with fading off too, so it is partly an appearance setting. | 70% | P07, P08 |
| CON-L07 | Move the **Reset slot order** button (MacroBar.lua:1097-1101) from General to the **Buttons** tab, below the list. | The reset sits with the control it resets. | 85% | P05 |
| CON-L08 | Re-order the Layout tab and give it two subsections: **Arrangement**: [Orientation][Buttons per row] / [Horizontal growth][Vertical growth]. **Size and spacing**: [Button size (px)][Button spacing (px)] / [Bar padding (px)][Bar scale]. (Declaration order: orientation, perRow, growthH, growthV, buttonSize, spacing, padding, scale.) | Orientation now explains "per row" on its own line, direction pairs with direction and size with size. The headings satisfy §7 under either reading (CON-P10). Against it: two headings on a four-line tab. | 65% | P09, P10 |
| CON-L09 | Add "(px)" to the labels *Button size*, *Button spacing*, *Bar padding* (MacroBar.lua:150, :155, :160). | Every other pixel slider on the page says "(px)". | 70% | P11 |
| CON-L10 | Rename subsection **Labels > Layout** to **Position** (MacroBar.lua:377 ff.). | Stops it reading as a pointer to the Layout tab, and says what the four rows do (anchor, inside/outside, X/Y nudge). | 75% | P13 |
| CON-L11 | Split Flyout > Layout into **Behavior**: [Enable flyout][Auto-close after (seconds)] / [Maximum flyout entries][Reverse flyout order], then **Placement**: [Flyout side][Gap from button (px)] / [Flyout button size (% of button)][Flyout spacing (px)] / [Flyout padding (px)][ ]. | Separates what the flyout does from where and how big it is. *Enable flyout* no longer pairs with a geometry row, and the name no longer echoes the Layout tab. | 60% | P13, P15 |
| CON-L12 | Rename subsection **Flyout > Icon** to **Indicator** (MacroBar.lua:535 ff.). | The rows style the band and arrow on the bar button, not a flyout icon, and the name no longer collides with Button appearance > Icon. | 75% | P14 |
| CON-L13 | Reword tooltips to state the cross-tab dependencies. *Enable flyout* (:463): append "Flyout entries look like the bar's buttons: everything on the Button appearance tab applies to them. The flyout panel's border is the Bar appearance tab's border." *Flyout background color* (:530): replace "Its border matches the bar's own border style, thickness and color." with "Its border is the Bar appearance tab's border." | You can't move rows across tabs to fix this (one row, one place), so the tooltip says where the controls are. "Everything on the tab" is accurate (CON-P38) where a list of three would not be. | 70% | P16, P38 |
| CON-L14 | Reword *Combat visibility*'s value texts (MacroBar.lua:566-568) to *Always* / *Only in combat* / *Only out of combat*, and list them in that order (ALWAYS, ONLY_IN_COMBAT, HIDE_IN_COMBAT). Stored values and accepted `/cm set` inputs unchanged; only the shown texts and the list order move (three new locale strings). | Same words and order as the General visibility it is intersected with. "Hide in combat" and "Only out of combat" mean the same here (`ResolveVisibility`). | 60% | P17 |
| CON-L15 | Add host tooltip decorations on three composed Master-controls rows through `H.RegisterRows`'s decorate map (settings/General.lua:288-308). *Lock frame*: "Stop the macro bar being dragged. Unlocked, the bar shows its drag handle and a gold wash, which is this addon's preview." *Master scale*: append "Multiplies the Macro Bar page's Bar scale." *Master alpha*: append "Multiplies the Macro Bar page's Bar opacity and Faded opacity." Labels and order unchanged. | The General page names the one frame it governs and the composition. §15 fixes the set, order and names, not the tooltips (the Macro Bar page already decorates composed tooltips). Against it: §15's point is the same words in every addon, and per-addon tooltip suffixes are a small step away from that. | 55% | P18 |
| CON-L16 | Per-type Macros tab tooltips (settings/Category.lua:1045): single: "Add-by-ID and the priority list for the %s macro."; composite: "Which categories the %s macro uses, in and out of combat, and their order." | Correct on all 15 tabs. | 80% | P19 |
| CON-L17 | Rename section **"Add item or spell by ID"** (CategoryAddByID.lua:359) to **"Add an item or spell"**. Lands with CON-L31. | It takes an ID, a link or a name, and the box label already says so. | 75% | P20 |
| CON-L18 | Give the top block of every Macros tab a section heading, **Macro**: drag icon, spec line and (Battle Rez) *Cast on mouseover*. On composite tabs the heading covers the drag icon, description and legend. Every tab then reads Macro / Add an item or spell / Priority list, or Macro / In combat / Out of combat. | The one schema-backed setting on a single tab (mouseover) gets a home that says "this macro's behaviour", and the tab structure becomes uniform. Against it: on 11 of 13 single tabs the heading sits over a lone drag icon, which is chrome for nothing and pushes the Add box down. A spacer above the Battle Rez checkbox fixes P21 more cheaply. | 50% | P21 |
| CON-L21 | Sentence-case the composite section headings: "In combat" / "Out of combat" (Category.lua:930-931). | Every other heading in the addon is sentence case. | 70% | P22 |
| CON-L22 | Relabel the composite row checkbox "Enabled" to "**In macro**" (Category.lua:894). The tooltip stays. | Says what is enabled and stops the clash with the addon/bar enables. | 65% | P23 |
| CON-L23 | Add a section heading **Primary stat** above the primary dropdown on Stat Priority > Priority (StatPriority.lua:660), so the tab reads Primary stat / Secondary stats. | Symmetric, and every control is under a heading. Against it: the heading and the dropdown's own label would both say "Primary stat", the same label twice that options-ui-§7 argues against. | 40% | P25 |
| CON-L24 | Relabel **Reset stat priority** to "**Reset this spec's stat priority**" (StatPriority.lua:683). | States the scope in the label, as the banner implies. | 60% | P26 |
| CON-L25 | Align the empty-state wording. Macros (Category.lua:700): "No active spec. Pick one in the Stat Priority banner to see this list." Picker placeholder (StatPriority.lua:155): "(no spec)". Stat Priority body (:738) unchanged. | One term, "spec", and every empty state says where to fix it. | 55% | P29 |
| CON-L26 | Shorten the *Show GCD swipe* tooltip (MacroBar.lua:352) to two sentences: "Off hides the global-cooldown swipe that flashes over every button whenever you cast. A real cooldown still shows, but its last second or so is hidden too." | Same facts, readable. | 60% | P30 |
| CON-L29 | Reword *Reset slot order*'s tooltip (MacroBar.lua:1099) to "Put the buttons back in the shipped order, undoing any drag-and-drop rearranging." | Correct for both orientations. | 70% | P34 |
| CON-L30 | Append to *Faded opacity*'s tooltip (MacroBar.lua:580): "Multiplied by the addon-wide Master alpha on the General page." | The same composition note *Bar opacity* already carries, on the other end of the fade. | 65% | P35 |
| CON-L31 | Reword the empty priority list (Category.lua:703): "Add an item or spell above, or pick up a matching item to trigger auto-discovery." | Matches the block above it and CON-L17. | 70% | P36 |
| CON-L32 | Reword the composite *Reset category* tooltip (Category.lua:1004): "Put back the shipped In macro ticks and the order of both sections." | Uses the label the player sees (after CON-L22), not the internal "enabled flags". | 60% | P37 |
| CON-L33 | **Alternative.** Relabel *Buttons per row* to *Buttons per line* (MacroBar.lua:143). | True for both orientations. Against it: "row" is the word every bar addon uses, and after CON-L08 *Orientation* sits beside it, so the tooltip and the neighbour already explain it. | 45% | P39 |

## Considered and rejected

Changes recalibrated below 40%. Not applied, kept so the owner can see what was weighed.

| id | change | reason rejected | confidence |
|---|---|---|---|
| CON-L19 | Move the **Buttons** tab from last to second on Macro Bar. | The current order follows how a bar is built, Buttons is set once, and its slot-order reset moves to it anyway (CON-L07), so the tab is found when needed. The gain is a nitpick and the cost is retraining everyone who knows the page. | 35% |
| CON-L20 | Merge **Bar appearance** and **Button appearance** into one **Appearance** tab. | 20 rows with five headings is a long scroll, and the source (settings/MacroBar.lua:1071-1075) records why the two surfaces keep separate tabs. It also trades one tab switch for scrolling past the other surface every time. | 35% |
| CON-L27 | Reorder `KCM.Settings.macroOrder` to put Healthstone beside Healing Potion. | It breaks the documented mirror with the default `macroBar.order` (`defaults/Profile.lua`), which 020 may not change, and the gain is small. | 30% |
| CON-L28 | Rename the General tab **Maintenance** to **Maintenance and resets**. | A longer label for one button. The *Reset all priorities* tooltip already says what it wipes and points to the whole-profile reset. | 35% |

Not proposed: anything that touches the composed blocks' internal order or labels (Master controls,
Border/Font/ColorPair; fixed by options-ui-§15/§16), the Profiles page (§3), the landing page (§5), or the
one-tab strip on Stat Priority (§13). P24 and P28 are recorded but are out of 020's latitude (widget shape,
reset behaviour).

## Proposed map

Applies CON-L01, L03-L17, L21, L22, L24-L26 and L29-L32 (everything at 55% or more). Not applied: the
alternatives L02, L18, L23 and L33 (40-50%), and the rejected L19, L20, L27 and L28.
Changed items are marked `«...»`.

```
Ka0s Consumable Master (landing)      unchanged

General
  Tab "Master controls"               unchanged rows/order; «tooltips on Lock frame, Master scale, Master alpha» (L15)
    [Enable Consumable Master][General visibility]
    [Master scale][Master alpha]
    [Lock frame][Debug console]
    [Minimap button][ ]
    [Reset position BTN][Reset all settings BTN]
  Tab "Maintenance"                   unchanged
    [Force resync BTN][Force rewrite macros BTN]
    [Reset all priorities BTN]

Macros                                15 tabs, same order; «per-type tab tooltips» (L16)
  Single-category tab
    (no heading) macro drag icon
    (spec-aware) LBL «"Spec-aware. Showing the list for <spec>. Change the spec in the Stat Priority page's banner."» (L01)
    (Battle Rez) [Cast on mouseover CB categories.BATTLE_REZ.mouseover]
    Section «"Add an item or spell"» (L17)
      [Type DD]
      [ID, link or name ID + Add]
    Section "Priority list"
      LBL legend
      RL priority rows («empty states: "No active spec. Pick one in the Stat Priority banner to see this list."» L25,
                        «"Add an item or spell above, ..."» L31)
    [Reset category BTN]
  Composite tab
    (no heading) macro drag icon
    LBL description
    LBL legend
    Section «"In combat"» (L21)     RL rows: handle | pick | [«In macro» CB] (L22)
    Section «"Out of combat"» (L21) RL rows: handle | pick | [«In macro» CB]
    [Reset category BTN «tooltip names the In macro ticks» (L32)]

Stat Priority
  Banner: [Viewing spec DD]           «tooltip lists Flask, Combat Potion, Stat Food and Weapon Enchant» (L03)
  Tab "Priority"
    [Primary stat DD, full width]
    Section "Secondary stats"
      LBL "Drag to rank. ..."
      RL 4 secondary stats
    [«Reset this spec's stat priority» BTN] (L24)

Macro Bar                             «7 tabs» (Visibility removed)
  Tab "General"
    [Enable macro bar CB macroBar.enabled]          [«Show tooltips CB macroBar.tooltips»]           (L04)
    «Sub "Visibility"» (L05, L06)
      [Combat visibility DD macroBar.combatMode «Always / Only in combat / Only out of combat»] [Fade unless hovered CB macroBar.fadeUnlessHover]  (L14)
      [«Bar opacity SL macroBar.alpha»]             [Faded opacity SL macroBar.fadeAlpha «tooltip names Master alpha» (L30)]
  Tab "Layout"                         (L08, L09)
    «Sub "Arrangement"»
      [Orientation DD macroBar.orientation]         [Buttons per row SL macroBar.perRow]
      [Horizontal growth DD macroBar.growthH]       [Vertical growth DD macroBar.growthV]
    «Sub "Size and spacing"»
      [«Button size (px)» SL macroBar.buttonSize]   [«Button spacing (px)» SL macroBar.spacing]
      [«Bar padding (px)» SL macroBar.padding]      [Bar scale SL macroBar.scale]
  Tab "Bar appearance"
    Sub "Background"  [Bar background CB][ ] / [Bar background color CP][Use class color CB]
    Sub "Border"      [Bar border CB][ ] / [Border style LSM][Border thickness (px) SL] / [Border color CP][Use class color CB]
  Tab "Button appearance"
    Sub "Background"  [Button background CB][ ] / [Button background color CP][Use class color CB]
    Sub "Border"      [Button border CB][ ] / [Border style][Border thickness (px)] / [Border color][Use class color] / [Border offset (px)][ ]
    Sub "Icon"        [Icon zoom (%) SL macroBar.iconZoom][Show stack count CB macroBar.showCount]
                      [Show GCD swipe CB macroBar.showGCD «shorter tooltip» (L26)][ ]
  Tab "Labels"
    Sub "Text"        [Show button labels CB][Label text DD]
    Sub «"Position"» (L10)  [Label position DD][Label placement DD] / [Label offset X (px)][Label offset Y (px)]
    Sub "Font"        (composed six, unchanged)
  Tab "Flyout"                         (L11, L12, L13)
    «Sub "Behavior"»
      [Enable flyout CB macroBar.flyout «tooltip names the two borrowed tabs»] [Auto-close after (seconds) SL macroBar.flyoutAutoClose]
      [Maximum flyout entries SL macroBar.flyoutMax] [Reverse flyout order CB macroBar.flyoutInvert]
    «Sub "Placement"»
      [Flyout side DD macroBar.flyoutPoint]         [Gap from button (px) SL macroBar.flyoutGap]
      [Flyout button size (% of button) SL macroBar.flyoutScale] [Flyout spacing (px) SL macroBar.flyoutSpacing]
      [Flyout padding (px) SL macroBar.flyoutPadding] [ ]
    Sub "Background"  [Flyout background CB][ ] / [Flyout background color CP «tooltip»][Use class color CB]
    Sub «"Indicator"» [Shaded band thickness (% of icon) SL][Arrow size (% of band) SL] / [Shaded band color CP][Use class color CB]
  Tab "Buttons"
    LBL "Drag a button by its handle ..."
    RL shown | rule | hidden
    «[Reset slot order BTN]» (L07, «tooltip without "left-to-right"» L29)

Profiles                              unchanged
```

**Counts after.** 6 panels (5 with L02). 25 tabs (Macro Bar 7, -1). 79 schema rows, unchanged. Lonely
subsections or one-row tabs go from 4 to 0 (Macro Bar General, Bar appearance > Opacity, Visibility's lone line,
Faded opacity's empty cell). The one remaining half-empty line pattern is the composer's own leading
toggle ([Bar background][ ]), which §16 fixes.

**Implementation notes for the executor.** All Macro Bar moves are `group`/`subgroup`/declaration-order edits in
`settings/MacroBar.lua`. Two things must stay true. The rows of each `group` stay contiguous, which
`tests/test_schema.lua` pins. And no `subgroup` may repeat its tab's name: "Visibility" under the tab "General"
is fine. `KCM.Settings.MACROBAR_TABS` loses its Visibility entry, and the suite's tab list and
`docs/settings-panel.md`'s Macro Bar table (8 tabs) must follow. `drawGeneral` keeps calling `drawGroup("General")`
and loses the button. `drawButtons` gains it. The suite pins the per-tab row counts by name
(`tests/test_schema.lua:511-518`: after the moves General 6, Layout 8, Bar appearance 8, Button appearance 12,
Labels 12, Flyout 16, Buttons 2, still 64 in all, with no Visibility entry) and the tab order
(`tests/test_settingsui.lua:774`, `:783`). Those are test edits that follow the layout, not behaviour changes.
Every reworded label, value text or tooltip is a new `L[...]` key, so the locale files follow too. The
General tab's shape (unheaded first line, then a `Visibility` subsection) is the one QuickComms already ships
(`QuickComms/settings/SchemaMembers.lua:222-240`).

## Cross-addon notes

- **Master/instance pairs.** Master scale/alpha/visibility on General and the instance's own Bar scale/opacity/
  Combat visibility are separate (options-ui-§15). Every addon with a per-display copy should say "multiplies"
  or "intersected with" in both tooltips (L15). Check AbsorbTracker, KickCD, MultiMeters and QuickComms for the
  same wording.
- **Opacity vs alpha.** This addon says *Bar opacity* and *Faded opacity*, QuickComms says *Faded alpha*, and the
  canonical set says *Master alpha*. Pick one word for the non-canonical rows collection-wide. Suggest
  "opacity" for player-facing rows and keep "alpha" only where §15 fixes it.
- **Visibility block.** QuickComms (2026-10-20) and this proposal put Visibility, Fade and Faded opacity/alpha
  under the instance's *General* tab as a **Visibility** subsection. That should be the collection shape. Value
  texts should match the composer's (*Always / Only in combat / Only out of combat / Never*).
- **Maintenance.** MultiMeters retired its Maintenance tab (`MultiMeters/settings/Schema.lua:1205-1223`).
  ConsumableMaster keeps one because it has three host verbs and the composer's `leadButton` takes one. For the
  seven windowed addons, the General page will grow a **Keybindings** tab. If ConsumableMaster ever gains a
  binding, it should land under the same tab name, after Master controls.
- **Include toggles in lists.** The tick/cross glyph (MultiMeters columns, Stat Priority, Macro Bar > Buttons)
  and the CheckBox (composite rows here) do the same job in different shapes (P24).
- **Composition notes on both ends.** Wherever a master value multiplies an instance value, every instance row it
  multiplies should say so, not just one (CON-P35 here: Master alpha multiplies Faded opacity too).
- **"(px)" / "(%)" unit suffixes** should be consistent per page at least, and preferably collection-wide.
- **Subsection names that echo tab names** ("Layout" under Labels on a page with a Layout tab) slip past
  `tests/test_schema.lua`'s check, which compares a subgroup only with *its own* tab.

## Upstream suggestions

- **options-ui-§13, per-page Defaults.** This addon's Macros page narrows Defaults to the visible tab (P28),
  which §13 forbids. Either the rule needs a carve-out for a page whose tabs are *instances* (15 categories,
  like a nav-rail entry), or the addon is out of compliance. Worth an explicit ruling. The nav-rail clause
  already scopes Defaults to "the active rail entry", which is this case in all but name.
- **options-ui-§14, banner reach.** When a picker on page A governs tabs on page B (Stat Priority's spec → four
  Macros tabs), §14 forbids a second picker on B, so B can only *state* the selection. The standard could
  either allow a read-only "change it on page A" link, or say outright that such pages should be one page
  (L02).
- **options-ui-§7.** "Mixes control types" is read two ways: kinds of *subject* (bar/border/font) or kinds of
  *widget* (dropdown/slider). The Layout and Visibility tabs here mix widgets but not subjects. Clarify which.
- **options-ui-§16 leading toggles.** *Show border* / *Bar background* open their own line and leave an empty
  second cell, because the swatch must start a line. That is a hole on every composed block that has a toggle.
  The rule could let the toggle pair with the style row ([Show border][Border style] / [Border thickness][ ]...),
  but that breaks the fixed four-row shape, so this is a trade-off for the standard to rule on, not a defect.

## Review

Independent review, 2026-10-24, against `../ConsumableMaster` at `80943b2`, read-only. Every cited builder,
row and line was re-read. What changed in this file, and why:

- **Counts corrected.** The row engine draws 69 rows (7 Master controls + 62 Macro Bar), not 61; 10 rows are
  bespoke or whole-value, not 18. There are 7 host buttons outside the composer, not 8. The Macro Bar split
  (64 rows) was checked against `tests/test_schema.lua:511-518`.
- **Six problems added (P34-P39).** Reset slot order's "left-to-right" tooltip is wrong for vertical bars. Faded
  opacity is multiplied by Master alpha with no note. The empty priority list still says "Add an itemID". The
  composite reset tooltip says "enabled flags". The flyout borrows *all* of Button appearance (border offset, stack
  count and GCD swipe included), not the three items CON-L13 listed. *Buttons per row* is a column when vertical.
- **Five changes added (L29-L33)** for those, with L33 kept as a 45% alternative.
- **CON-L13 rewritten.** Its tooltip named a wrong subset of borrowed controls. It now says "everything on the
  Button appearance tab", which is what `bindEntry` does (70%).
- **CON-L15 corrected.** Master alpha multiplies Faded opacity as well as Bar opacity (`applyAlpha`). Lowered to
  55%, because per-addon suffixes on canonical tooltips are a small step against §15's "same words everywhere".
- **Recalibrated.** L04 65->60, L06 75->70, L08 70->65, L11 65->60, L13 65->70, L14 65->60, L26 55->60.
  L18 55->50 (a heading over a lone drag icon on 11 tabs) and L23 55->40 (the heading would repeat the
  dropdown's own label, which options-ui-§7 argues against). Both leave the map. L02 stays at 50%, and §14's
  banner rule is added as an argument for it.
- **Rejected.** L19, L20, L27 and L28 dropped under 40% and moved to a new "Considered and rejected" section.
- **No change alters a setting.** All 79 rows keep their path, default, range and apply. L14 changes only the
  shown value texts and their list order. The stored values and the `/cm set` inputs stay the same. No standard
  rule is broken: the General tab shape matches QuickComms' shipped precedent, no `subgroup` repeats its tab, and
  the Master controls set, order and names are untouched.
- **Executor notes extended.** The suite pins the per-tab row counts and the tab order by name, so those tests
  must follow the move (General 6, Bar appearance 8, Button appearance 12, no Visibility). Reworded strings need
  locale keys.
