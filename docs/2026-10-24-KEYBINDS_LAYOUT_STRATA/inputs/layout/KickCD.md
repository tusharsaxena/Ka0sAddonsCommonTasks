# KickCD — settings layout analysis

Scope: item 020, layout only. No setting key, default, range or behaviour changes. I read `../KickCD` on `master`
on 2026-10-24: `settings/{OptionsSetup,SchemaSetup,Panel,Panel_Render,Panel_Widgets,General,Grid,Icons,Castbar,Label,Spells,Spells_Header,Spells_Rows,Profiles}.lua`,
`core/{Units,Constants}.lua`, `defaults/Profile.lua`, the frame-building parts of `modules/`, `docs/settings-panel.md`,
the vendored `libs/LibKa0s/OptionsCompose.lua` (for the composed row labels) and the standard's `options-ui.md`.

KickCD is **not** one of the seven addons with a primary window, so the planned General > Keybindings tab does not
apply. It has no `Bindings.xml`, and its displays are HUD frames that the lock switch controls.

Notation: `u.` stands for `units.<unit>.` (`<unit>` is `target` or `focus`, depending on the Grid page's Unit picker).
Widget types: CB checkbox, SL slider, DD dropdown, LSM shared-media dropdown, CP colour picker, EB edit box,
BTN button. `[A | B]` is one two-column line, and `(solo)` is a row that owns its line.

## Current map

Pages are registered in TOC order (`KickCD.toc`, Settings block): landing, General, Grid, Spells, Profiles.

```
Ka0s KickCD (landing)                    settings/OptionsSetup.lua:266 -> settings/Panel.lua:275 (BuildLandingPage)
  untabbed (options-ui-§13 exemption): logo, tagline, "Slash Commands" heading + one label per COMMANDS row

General                                  settings/General.lua:299-375 (CreatePanel :310, RenderTabbedSchema :326)
  Tab "Master controls"                  composed, settings/General.lua:66-92 (+ visibility override :102-114)
    [Enable KickCD       CB enabled]              | [General visibility  DD visibility
                                                     (Always / In combat / When target is casting /
                                                      When target is casting an interruptible spell)]
    [Master scale        SL scale]                | [Master alpha        SL alpha]
    [Lock frame          CB locked]               | [Debug console       CB state.debugConsole (session)]
    [Minimap button      CB global.minimap.shown] (alone: no Test mode, options-ui-§15 exemption)
    [Reset position BTN]                          | [Reset all settings BTN -> KICKCD_RESET_ALL]
  Tab "Units"                            rows settings/General.lua:191-201, 230-245; afterGroup :350-369
    [Enable Target grid  CB units.target.enabled] | [Enable Focus grid   CB units.focus.enabled]
    [Use same styling as Target  CB units.focus.link (skipRender, drawn by afterGroup)]
                                                  | [Copy styling from Target  BTN]

Grid                                     settings/Grid.lua:19-41 (CreatePanel :24, renderer Panel_Render.lua:335)
  Band: [Unit  DD Target / Focus (session NS.State.viewedUnit)]          Panel_Render.lua:113-130
  Rail (Panel_Render.lua:346, order :280): Icons | Cast bar | Text Label
  Linked Focus (Panel_Render.lua:207-258): inert strip + "Linked to Target. Untick ... on the General page's
    Units tab ..." link row, which jumps to General > Units. No row of any tab is drawn.

  Rail "Icons"                           settings/Icons.lua:34-567, registered :573
    Tab "Sizing" (4)                     :83-110
      [Primary size (in px)  SL u.icons.primarySize] | [Secondary size  SL u.icons.secondarySize]
      [Gap (in px)           SL u.icons.gap]         | [Icon zoom       SL u.icons.zoom]
    Tab "Layout" (6)                     :113-156
      [Anchor point (of secondary icons relative to primary)  DD u.icons.anchor]
                                                     | [Growth direction (of secondary icons)  DD u.icons.secondaryGrow]
      [Rows      SL u.icons.secondaryRows]           | [Columns   SL u.icons.secondaryCols]
      [X offset (in px)  SL u.icons.secondaryOffsetX] | [Y offset (in px)  SL u.icons.secondaryOffsetY]
    Tab "Visual states" (5)              :159-196
      [Ready alpha     SL u.icons.readyAlpha]        | [Cooldown alpha  SL u.icons.cooldownAlpha]
      [Cooldown tint   CP u.icons.cooldownTint]      | [Use class color CB u.icons.useClassColorCooldownTint]
      [Suppress GCD swipe + text  CB u.icons.suppressGCDSwipe]
    Tab "Border" (5)                     :209-220 (H.BorderGroup)
      [Show border   CB u.icons.borderShow]
      [Border style  LSM u.icons.borderTexture]      | [Border thickness (px)  SL u.icons.borderSize]
      [Border color  CP u.icons.borderColor]         | [Use class color  CB u.icons.useClassColorBorder]
    Tab "Annotations" (11)               :238-316
      sub "Icon"
        [Show cooldown text  CB u.icons.showCooldownText] | [Show tooltip on hover  CB u.icons.showTooltip]
      sub "Font"                         (H.FontGroup :260-279)
        [Font        LSM u.icons.cooldownTextFont]   | [Font size        SL u.icons.cooldownTextSize]
        [Font color  CP  u.icons.cooldownTextColor]  | [Use class color  CB u.icons.useClassColorCooldownText]
        [Font flags  DD  u.icons.cooldownTextFlags]  | [Font shadow      CB u.icons.cooldownTextShadow]
      sub "Charges"
        [Show charges  CB u.icons.showCharges] (solo)
        [Charges X offset (in px)  SL u.icons.chargesOffsetX] | [Charges Y offset (in px)  SL u.icons.chargesOffsetY]
    Tab "Ready glow" (34)                :408-566
      sub "Effect"
        [Primary glow trigger  DD u.icons.primaryGlowTrigger] | [Secondary glow trigger  DD u.icons.secondaryGlowTrigger]
          (Never / Always / When target is casting / When target is casting an interruptible spell)
        [Primary glow style    DD u.icons.primaryGlowType]    | [Secondary glow style    DD u.icons.secondaryGlowType]
        [Primary glow color    CP u.icons.primaryGlowColor]   | [Use class color CB u.icons.useClassColorPrimaryGlowColor]
        [Secondary glow color  CP u.icons.secondaryGlowColor] | [Use class color CB u.icons.useClassColorSecondaryGlowColor]
      sub "Button (rotating rays)"  [Primary frequency | Secondary frequency]       u.icons.{primary,secondary}GlowButtonFrequency
      sub "Proc (flipbook)"         [Primary duration (in seconds) | Secondary ...]  ...GlowProcDuration
                                    [Primary start animation | Secondary ...]        ...GlowProcStartAnim
      sub "Pixel border"            lines | frequency | line length (0 = automatic) | thickness (in px) | dark border
                                    (5 lines, primary | secondary)                   ...GlowPixel{Lines,Frequency,Length,Thickness,Border}
      sub "Auto cast sparkles"      particles | frequency | scale (3 lines)          ...GlowAutocast{Particles,Frequency,Scale}
      sub "Offset"                  [Primary X offset (in px) | Secondary ...], [Primary Y offset | Secondary ...]
                                    ...Glow{XOffset,YOffset}
      (every knob is dimmed under a style it does not apply to, or under trigger Never)

  Rail "Cast bar"                        settings/Castbar.lua:77-576, registered :581
    Tab "General" (5)                    :104-210
      [Enable cast bar  CB u.castbar.enabled] (solo)     tooltip "Show the target cast bar."
      [Orientation      DD u.castbar.orientation]        | [Growth direction  DD u.castbar.growDirection]
      [Auto-size to icon grid  CB u.castbar.autoSize]    | [Show spark        CB u.castbar.showSpark]
    Tab "Size and position" (7)          :245-308
      sub "Size"
        [Cast bar width (in px)  SL u.castbar.width]     | [Cast bar height (in px)  SL u.castbar.height]
      sub "Position"
        [Anchor mode  DD u.castbar.anchorMode] (solo)
        [Anchor on primary icon  DD u.castbar.anchorPoint] | [Anchor on cast bar  DD u.castbar.castbarPoint]
        [X offset (in px)  SL u.castbar.anchorOffsetX]   | [Y offset (in px)  SL u.castbar.anchorOffsetY]
    Tab "Icon" (2)                       :316-335
      [Icon position  DD u.castbar.iconPosition]         | [Icon size (in px)  SL u.castbar.iconSize]
    Tab "Font" (6)                       :377-396 (H.FontGroup)
      [Font             LSM u.castbar.font]              | [Font size        SL u.castbar.fontSize]
      [Cast time color  CP  u.castbar.textColor]         | [Use class color  CB u.castbar.useClassColorText]
      [Font flags       DD  u.castbar.fontFlags]         | [Font shadow      CB u.castbar.fontShadow]
    Tab "Spell name" (5)                 :404-439
      [Show spell name  CB u.castbar.showName]           | [Anchor  DD u.castbar.namePosition]
      [X offset (in px) SL u.castbar.nameOffsetX]        | [Y offset (in px)  SL u.castbar.nameOffsetY]
      [Truncate after (characters)  SL u.castbar.nameTruncate]
    Tab "Cast time" (4)                  :447-475
      [Show cast time   CB u.castbar.showTime]           | [Anchor  DD u.castbar.timePosition]
      [X offset (in px) SL u.castbar.timeOffsetX]        | [Y offset (in px)  SL u.castbar.timeOffsetY]
    Tab "Interruptible" (13)             :512-542
      sub "Bar"        [Bar texture LSM u.castbar.interruptible.statusBarTexture] | [Bar opacity SL ...barAlpha]
                       [Bar color CP ...barColor] | [Use class color CB ...useClassColorBar]
      sub "Background" [Background color CP ...bgColor] | [Use class color CB ...useClassColorBgColor]
      sub "Text"       [Spell name color CP ...nameTextColor] | [Use class color CB ...useClassColorNameTextColor]
      sub "Border"     [Show border CB ...borderShow]
                       [Border style LSM ...borderTexture] | [Border thickness (px) SL ...borderSize]
                       [Border color CP ...borderColor] | [Use class color CB ...useClassColorBorder]
    Tab "Non-interruptible" (13)         :545-575, the same 13 rows under u.castbar.uninterruptible.*

  Rail "Text Label"                      settings/Label.lua:89-207, registered :212
    Tab "General" (2)                    :91-111
      [Show label  CB u.label.show]                      | [Label text  EB u.label.text (max 32)]
    Tab "Placement" (8)                  :127-170
      [Attach to  DD u.label.style.attach] (solo)
      [Label anchor point  DD u.label.style.point]       | [Attach point  DD u.label.style.relPoint]
      [X offset (in px)  SL u.label.style.offsetX]       | [Y offset (in px)  SL u.label.style.offsetY]
      [Horizontal justify  DD u.label.style.justifyH]    | [Vertical justify  DD u.label.style.justifyV]
      [Rotation (degrees)  SL u.label.style.rotation]
    Tab "Font" (6)                       :186-206 (H.FontGroup)
      [Font         LSM u.label.style.font]              | [Font size        SL u.label.style.size]
      [Label color  CP  u.label.style.color]             | [Use class color  CB u.label.style.useClassColor]
      [Font flags   DD  u.label.style.flags]             | [Font shadow      CB u.label.style.shadow]

Spells                                   settings/Spells.lua:724-862 (CreatePanel :724, registered :866)
  Band (PageHeader :672; Spells_Header.lua:148-246)
    [Specialization  DD class/spec pairs] (full width)
    [Add a spell  IdInput + Add BTN]
  Tab "Spell list" (one tab, hand-drawn :686)
    ReorderList rows (Spells_Rows.lua:278-305), in cell order:
      [drag handle][spell icon][spell name][enabled CB][known/not-known glyph][Category DD (120px)][remove BTN]
  Defaults -> KICKCD_RESET_SPELLS (this spec's list)

Profiles                                 settings/Profiles.lua:38-90 (AceDBOptions via AceConfigDialog; untabbed exemption)
```

Counts: **5 pages** (landing plus 4 subcategories). **20 tabs**: General 2, Icons 6, Cast bar 8, Text Label 3 and
Spells 1. Profiles and the landing page have no strip. **Schema rows:** General 10 (7 composed, 2 unit enables and
the `link` row), plus 136 per unit (Icons 65, Cast bar 55, Text Label 16), so 136 rows are on screen for the viewed
unit and 282 rows exist in total. Each Spells list row holds 7 hand-built widgets.

## Problems

| id | file:line | problem |
|---|---|---|
| KIC-P01 | General.lua:191-245, 350-369; Panel_Render.lua:250-255 | **The controls for a single unit live on another page.** These are the per-unit enable, the Focus styling link and Copy styling. The Grid page picks the unit, but turning that unit on or off, or unlinking Focus, needs a trip to General > Units. On a linked Focus the Grid page shows *nothing* except a link back to General. options-ui-§14 lists enable and copy-from among the acts on the selected instance that belong in the band or on a `General` first tab or rail entry. |
| KIC-P02 | Label.lua:9-11, 106-111; Panel_Render.lua:181 | **Focus's label text cannot be edited while Focus is linked.** `label.text` is per-unit by design (`defaults/Profile.lua:339`: "enabled/anchors/label.text stay per-unit even while linked") and it still renders, but the linked page draws no rows. To rename the Focus label you have to unlink, which forks Focus's whole look. No row is marked `alwaysPerUnit` even though the partition code exists for exactly this case (Panel_Render.lua:36-46). |
| KIC-P03 | General.lua:195 | "Enable Target grid" / "Enable Focus grid" undersell what the switch does. `units.<u>.enabled` gates the icon grid, the cast bar (`modules/Castbar.lua:251`) and the label (`modules/UnitLabel.lua` Apply). |
| KIC-P04 | Castbar.lua:196-202 vs :245-260 | `autoSize` overrides width (horizontal) or height (vertical), but it sits on Cast bar > General while the two sliders it overrides are one tab away, on Size and position. A dependent row is split from its parent. |
| KIC-P05 | Castbar.lua:316-335 | The cast bar "Icon" tab holds 2 rows. It is a lonely tab that costs a click, and its two rows are a position and a size, which is the question the neighbouring "Size and position" tab answers. |
| KIC-P06 | Castbar.lua:377-475 | Text styling is spread over **three** tabs: Font (typography plus the *cast time* colour), Spell name and Cast time. Styling the cast-time text means visiting Font for its colour and Cast time for its toggle and position, and the spell name's colour is on a fourth and fifth tab (Interruptible / Non-interruptible > Text). |
| KIC-P07 | Castbar.lua:383 | The Font tab's colour row is labelled "Cast time color", but the tab is named Font and governs both texts. That is correct, yet surprising on a tab the reader takes to be shared. |
| KIC-P08 | Castbar.lua:529, 562 | Subsection "Text" on Interruptible / Non-interruptible holds only *Spell name color*. "Text" overlaps the Font tab's subject, and the cast time colour is not under it. |
| KIC-P09 | Castbar.lua:108 | The "Enable cast bar" tooltip says "Show the **target** cast bar." This is wrong on the Focus page. |
| KIC-P10 | Castbar.lua:298, 306 | The cast bar anchor X/Y offset tooltips state no sign convention, unlike the spell name, cast time and label offsets ("positive = up"). |
| KIC-P11 | Icons.lua:83-156 | Icons "Sizing" (4) and "Layout" (6) are split, but both answer *how big and where is the block*. Cast bar folds the same pair of questions into one tab, "Size and position", with Size / Position subsections. The two entries on the same rail are shaped differently. |
| KIC-P12 | Icons.lua:116, 124 | The labels are overlong and use parentheses: "Anchor point (of secondary icons relative to primary)" and "Growth direction (of secondary icons)". The cast bar says the same thing as "Anchor on primary icon" and "Growth direction". |
| KIC-P13 | Icons.lua:93 | "Secondary size" is a 0.40-1.00 fraction, but the label gives no unit, while its neighbour reads "(in px)". A reader expects pixels. |
| KIC-P14 | Icons.lua:145-156 | The Layout tab's "X offset / Y offset" do not say they move only the secondary block. The Y sign is also **inverted** relative to every other Y offset in the addon (`IconGrid_Layout.lua:229`: positive = down). The tooltip says so, but nothing on the label does. |
| KIC-P15 | Icons.lua:159-220 | "Visual states" (5) and "Border" (5) are two short tabs about how one icon looks. Two clicks cover what one tab with two subsections could show. |
| KIC-P16 | Icons.lua:193 | "Suppress GCD swipe + text" uses a `+` where the rest of the addon writes words ("and"). |
| KIC-P17 | Icons.lua:238-279 | Annotations > subsection "Font" does not say *which* text it styles. It governs only the cooldown countdown, because the charges badge is `NumberFontNormal` (`IconGrid_Render.lua:263`). Its on/off switch ("Show cooldown text") sits in a different subsection ("Icon"), paired with an unrelated tooltip toggle. |
| KIC-P18 | Icons.lua:249-252 | "Show tooltip on hover" is interaction, not an annotation drawn on the icon. It is filed under "Icon" next to the cooldown text toggle. |
| KIC-P19 | Icons.lua:408-566 | Ready glow is a 34-row tab, the longest page in the addon. 26 of its rows are style knobs, and at most 10 of them (5 per slot, Pixel) apply at once. The rest are drawn dimmed. Layout alone cannot hide them, because the library has no `hiddenIf` (see the upstream suggestions). |
| KIC-P20 | General.lua:107-108; Icons.lua:343-344 | The value labels "When target is casting" / "...an interruptible spell" are used for General visibility and for both glow triggers. On the Focus grid they mean *the focus* (`IconGrid.lua:15-18`: "on the instance's unit"). "target" also collides with the Target unit name. |
| KIC-P21 | Panel_Render.lua:280; Label.lua:212 | The rail reads "Icons | Cast bar | Text **L**abel". "Text Label" is Title Case among sentence-case siblings. |
| KIC-P22 | Grid.lua:24, 44 | The page is named "Grid", but it configures the grid, the cast bar and the label of one *unit*. The name describes one of three entries. |
| KIC-P23 | Label.lua:133-142 | "Label anchor point" / "Attach point" is a third phrasing of the two-point anchor. The others are the cast bar's "Anchor on primary icon / Anchor on cast bar" and the icons' "Anchor point (of ...)". The tooltip's "the **target** widget" is ambiguous in a Target/Focus addon. |
| KIC-P24 | Label.lua:153-162 | "Horizontal justify" / "Vertical justify" use a verb as a noun. The file's own comments and the docs call it *alignment*. |
| KIC-P25 | Label.lua:127-170 | Placement mixes two subjects, *where it sits* (attach, points, offsets) and *how the text is set* (justify, rotation), with no subsection headings. The analogous Cast bar tab has them. options-ui-§7 ("a tab that mixes control types MUST carry subsection headings") arguably applies, but its example is about *subjects* (bar / background / border rows), and read literally as widget types it would also flag Icons > Layout, Cast bar > General and > Spell name, which carry DD + SL + CB with no headings today. Treat this as a SHOULD-level fix, not a MUST violation (see the upstream suggestions). |
| KIC-P26 | Label.lua:166-170 | "Rotation (degrees)" ends Placement alone on its line. That is harmless, but it reads as an orphan under the justify pair. |
| KIC-P27 | OptionsCompose.lua:554-556 (composer) | The "Reset position" tooltip, "Move the frame back to where it started.", is inaccurate here. `Helpers.ResetIconPosition` (Panel_Render.lua:463-482) moves **both units' icon grids** and leaves a FREE-mode cast bar where it is. The tooltip is the composer's, and the host cannot override it today. |
| KIC-P28 | General.lua:3-33 | The Master controls labels use "alpha" ("Master alpha", "Ready alpha", "Cooldown alpha"), and the BarGroup's "Bar opacity" sits on the same addon's cast bar. The standard's own composed labels mix the two words, so this is not KickCD's to fix alone. |
| KIC-P29 | OptionsCompose.lua:371 vs Icons.lua:86 etc. | The unit suffix is inconsistent: the composer says "Border thickness (**px**)", while every KickCD row says "(**in px**)" and "(in seconds)". |
| KIC-P30 | Spells_Rows.lua:230-243 | Every spell row spends 120px on a Category dropdown whose tooltip says "Currently informational only." This is a control with no effect. It cannot be removed under the brief, but it is the widest cell in the row. |
| KIC-P31 | Spells_Header.lua:161 | The picker is captioned "Specialization", but its entries are class+spec pairs (the value is `classFile/specID`). "Class and specialization" is what it picks. |
| KIC-P32 | Spells_Rows.lua:294-301 | The row order is handle, icon, name, **enable**, known glyph, category, remove. The on/off checkbox is buried in the middle of the row instead of leading it, as checkboxes lead every other row in the panel. |
| KIC-P33 | Panel_Render.lua:207-258 | The linked-Focus page deadens the whole strip and replaces every tab with the same note. With P01 fixed, the note is still needed, but it should point at a control on the same page instead of another page. |
| KIC-P34 | Castbar.lua:316-335 | "Icon position" has an **Off** value and "Icon size" says "0 hides the icon". These are two hide paths, and only one says so on its label. A tooltip cross-reference is enough. |
| KIC-P35 | Icons.lua:541-548 | (review) The Ready glow "Primary/Secondary X offset (in px)" and "Y offset" rows are not offsets: the tooltip says "How far the glow **reaches past** the icon's sides". Every other "X offset" in the addon is a shift. The label promises one behaviour and the slider does another. |
| KIC-P36 | General.lua:113 | (review) The General visibility tooltip says "(icon grid + cast bar)", the same `+` as P16, and leaves out the label, which follows visibility too (UnitLabel.lua:131-145 parents it to the grid for exactly that reason). |
| KIC-P37 | Grid.lua:28 | (review) The Grid page's Defaults tooltip says it restores "the selected unit's settings in the **section on screen**". On a railed page "section" reads as the visible tab, but the blast radius is the whole **rail entry** (every tab of Icons, say), per options-ui-§13 and the ratified deviation in docs/ARCHITECTURE.md (`Documented deviations`, options-ui-§13 row). The tooltip undersells what one click resets. |
| KIC-P38 | Icons.lua:573-574; Castbar.lua:581-582 | (review) The rail-entry tooltips list the entry's tabs in prose ("their size, layout, states, border, annotations and ready glow"). Any tab merge or rename (L08, L12, L14-L15, L16-L18) leaves them stale unless they are reworded in the same change. |
| KIC-P39 | Castbar.lua:377-396 | (review) After L18 the composed Font block sits under a subsection called just "Font", but its font, size, flags and shadow style **both** texts while its colour styles only the cast time. The heading should say the font is shared. |
| KIC-P40 | Panel_Render.lua:115 | (review) The Unit picker's tooltip says "Target and Focus are configured independently unless Focus is set to use Target's styling", but does not say where that switch is. After L01 the answer is "beside this picker"; today it is "on another page". |

## Proposed changes

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| KIC-L01 | Move the unit controls into the Grid page band, on one row beside the picker: `[Unit DD] [Enable <Unit> CB units.<u>.enabled] [Use same styling as Target CB units.focus.link] [Copy styling from Target BTN]`. The last two cells draw only while Focus is viewed. All three rows keep their `panel = "general"` stamp and become `skipRender`, drawn by the band (as `link` already is), so General's Defaults keeps its exact blast radius. **Mechanism:** the band is drawn today by `O.PageBanner`, which draws exactly one Dropdown and is documented as the page's only picker; a band holding a picker plus acts must be one `O.PageHeader` block with the picker inside it (options-ui-§14, "at most one such block"; LibKa0s Options docs, `PageHeader`). **Caveat (owner call):** with the stamp kept, General's Defaults goes on resetting both units' enables and the link even though none of them is drawn on General any more, which is a reset of rows the player cannot see; re-stamping them `panel = "grid"` would move the blast radius and is out of scope. **Fallback:** if four cells do not fit one band row at default scale, use options-ui-§14's escape and make them the rail's first entry, `General` (rows marked `alwaysPerUnit`). | Everything about *this unit* is then on the page that picks the unit. The linked state stops sending the player to another page. AbsorbTracker already draws its link and copy pair in its unit band. | 55% | P01, P33, P40 |
| KIC-L02 | Delete the General page's "Units" tab, because its content moves in L01. General keeps one tab, "Master controls" (a one-tab strip, options-ui-§13). | It removes a whole tab whose only purpose was to be the far end of a cross-page jump. | 55% (depends on L01; same Defaults caveat) | P01 |
| KIC-L03 | Reword the enable row label to "Enable Target" / "Enable Focus" (it reads with the band's picker). Tooltip: "Track this unit: its icon grid, cast bar and label. Off hides all three." | The switch gates all three displays, not just the grid. | 85% | P03 |
| KIC-L04 | Reword the linked-Focus note (Panel_Render.lua:250-255) to "Linked to Target. Untick *Use same styling as Target* above to give Focus its own look.", with no cross-page link. | After L01 the control is on the same page, a few pixels up. | 60% (with L01) | P33 |
| KIC-L05 | Mark `u.label.text` as `alwaysPerUnit` so a linked Focus still draws it, on Text label > General, above the link note. Re-enable the strip on that entry (a live strip wherever any tab of the entry has `alwaysPerUnit` rows), because `deadenStrip` assumes no tab has per-unit rows (Panel_Render.lua:181-205). ~~or open the linked page on the General tab~~ (struck in review: forcing the tab on a unit switch breaks options-ui-§14, "changing instance MUST leave the rail's selection and each entry's tab alone"; a player on Target's Text label > Placement who flips to a linked Focus would otherwise be stuck on a dead strip with no way to the text row). | The text is per-unit by design and is rendered while linked, yet it cannot be edited. This is the most-asked "why can't I rename my focus label" trap. | 65% | P02 |
| KIC-L06 | Rename the page "Grid" to "Units" (label only; key `grid` and the deep links are unchanged). | The page edits one unit's displays. "Units" is free once L02 removes the General tab of that name. Alternative: "Display". | 50% | P22 |
| KIC-L07 | Rename the rail entry "Text Label" to "Text label". | Sentence case, like "Cast bar" beside it. | 85% | P21 |
| KIC-L08 | Icons: merge "Sizing" and "Layout" into one tab, **"Size and layout"**, with subsections **"Size"** (`[Primary size | Secondary size]`, `[Gap | Icon zoom]`) and **"Secondary block"** (`[Anchor on primary icon | Growth direction]`, `[Rows | Columns]`, `[X offset | Y offset]`). | It is one question: how big the block is and where it sits. This mirrors Cast bar's "Size and position" and saves a tab. | 75% | P11 |
| KIC-L09 | Relabel `u.icons.anchor` "Anchor point (of secondary icons relative to primary)" as "Anchor on primary icon", and `u.icons.secondaryGrow` "Growth direction (of secondary icons)" as "Growth direction". The "Secondary block" heading from L08 carries the context. | Shorter, and identical to the cast bar's labels for the same concepts. | 80% | P12 |
| KIC-L10 | Relabel `u.icons.secondarySize` "Secondary size" as "Secondary size (fraction of primary)". | It states the unit the way its neighbour does. ASCII only, never "×" (Label.lua:163-165's glyph rule). | 80% | P13 |
| KIC-L11 | Relabel the Icons block's "Y offset (in px)" as "Y offset (in px, positive = down)"; X is unchanged. Keep the tooltips. (Review: "+ is down" reworded, because L13 removes `+` from labels as house style.) | The sign is the opposite of every other Y slider in the addon. Only the label can warn without a behaviour change. | 55% | P14 |
| KIC-L12 | Icons: merge "Visual states" and "Border" into one tab, **"Appearance"**, with subsections **"States"** (`[Ready alpha | Cooldown alpha]`, `[Cooldown tint | Use class color]`, `[Suppress GCD swipe and text]`) and **"Border"** (the composed block, unchanged). The tab moves from TAB_SINGLE_SUBJECT to TAB_MIXED in `tests/test_schema.lua`. | Two five-row tabs about one icon's look become one. options-ui-§16 explicitly allows merging groups under per-group headings. | 55% | P15 |
| KIC-L13 | Relabel "Suppress GCD swipe + text" as "Suppress GCD swipe and text". | House style uses words. | 90% | P16 |
| KIC-L14 | Annotations: replace subsections "Icon / Font / Charges" with **"Cooldown text"** (`[Show cooldown text]` solo, then the composed font block unchanged), **"Charges"** (unchanged) and **"Tooltip"** (`[Show tooltip on hover]`). | The font heading then names the text it styles, and the text's on/off switch heads its own block, the same "toggle with its controls" rule Cast bar's Spell name tab follows. The tooltip toggle stops posing as an annotation. | 80% | P17, P18 |
| KIC-L15 | Rename the tab "Annotations" to "Text and tooltip". | "Annotations" is jargon. After L14 the tab is exactly cooldown text, charges (a number) and tooltip. | 45% | P17 |
| KIC-L16 | Cast bar: move `u.castbar.autoSize` from General to the head of Size and position > Size, solo, above `[width | height]`. General becomes `[Enable cast bar]` (solo), `[Orientation | Growth direction]`, `[Show spark]`. | The override sits directly above the two sliders it overrides. | 80% | P04 |
| KIC-L17 | Cast bar: fold the "Icon" tab into Size and position as a third subsection, **"Spell icon"**: `[Icon position | Icon size (in px)]`. | It removes a two-row tab, and the icon's position and size belong with the bar's own geometry. | 60% | P05 |
| KIC-L18 | Cast bar: merge "Font", "Spell name" and "Cast time" into one tab, **"Text"**, with subsections in this order: **"Spell name"** (5 rows unchanged), **"Cast time"** (4 rows unchanged) and **"Font (both texts)"** (composed block unchanged, still labelled "Cast time color"; review added the heading wording, P39). 15 rows on one tab is long but below Ready glow's 34. | Three tabs for one surface become one. The colour labelled "Cast time color" now sits directly under the Cast time subsection it colours. | 70% | P06, P07 |
| KIC-L19 | Cast bar Interruptible / Non-interruptible: rename subsection "Text" to "Spell name". | That is the only text it colours, and it no longer collides with the new "Text" tab. | 75% | P08 |
| KIC-L20 | Reword the `u.castbar.enabled` tooltip "Show the target cast bar." as "Show this unit's cast bar." | It is correct on the Focus page. | 95% | P09 |
| KIC-L21 | Append the sign convention to the cast bar anchor offset tooltips: "(positive = right)" and "(positive = up)". | Every other offset tooltip says it. | 85% | P10 |
| KIC-L22 | Reword the value labels for General visibility (General.lua:107-108) and both glow triggers (Icons.lua:343-344): "When target is casting" becomes "When the tracked unit is casting", and "...an interruptible spell" becomes "When the tracked unit is casting an interruptible spell". The keys are unchanged. Update the visibility override's entry in docs/ARCHITECTURE.md `Documented deviations` / docs/settings-panel.md in the same change, because they quote the value list. | Correct on both units' pages and on the unit-less General page ("the unit" alone has no referent there; review changed it to "the tracked unit"), with no false "target" reading. | 65% | P20 |
| KIC-L23 | Text label > Placement: add subsections **"Position"** (`[Attach to]` solo, `[Anchor on label | Anchor on attached widget]`, `[X offset | Y offset]`) and **"Alignment"** (`[Horizontal alignment | Vertical alignment]`, `[Rotation (degrees)]`). | options-ui-§7 says a mixed tab must carry subsection headings, and this matches Cast bar's Size and position. Rotation then sits under a heading instead of orphaned. | 65% | P25, P26 |
| KIC-L24 | Relabel `style.point` "Label anchor point" as "Anchor on label", and `style.relPoint` "Attach point" as "Anchor on attached widget". In the tooltip, "the target widget" becomes "the widget chosen in Attach to". | One phrasing for the two-point anchor across the addon. The word "target" now means only the Target unit. | 75% | P23 |
| KIC-L25 | Relabel "Horizontal justify" / "Vertical justify" as "Horizontal alignment" / "Vertical alignment". | Plain English, and the word the docs use. | 80% | P24 |
| KIC-L26 | Spells: recaption the picker "Specialization" as "Class and specialization". | It says what it picks. | 60% | P31 |
| KIC-L27 | Spells rows: move the enabled checkbox to the first content cell, after the drag handle: handle, **enable**, icon, name, known glyph, category, remove. The icon desaturation hook stays wired. | Checkbox first, like every other on/off row in the panel. It is also the most-used control in the row. | 40% | P32 |
| KIC-L28 | Cast bar `iconPosition` tooltip: append "Off hides the icon; so does Icon size 0." The `iconSize` tooltip already says it. | The two hide paths name each other. | 70% | P34 |
| KIC-L29 | (review) Relabel the Ready glow > Offset rows "Primary/Secondary X offset (in px)" / "Y offset (in px)" as "Primary/Secondary horizontal reach (in px)" / "vertical reach (in px)", and the subsection "Offset" as "Reach". Tooltips unchanged. | The slider sets how far the glow extends past the icon, not a shift; "offset" means a shift everywhere else in the addon. The LibCustomGlow parameter is called xOffset, which is where the word came from. | 50% | P35 |
| KIC-L30 | (review) Reword the General visibility tooltip: "When KickCD's displays (icon grids, cast bars and labels) are shown. Enable KickCD still wins: off hides everything." | Words instead of `+`, and it names the label, which follows visibility too. | 80% | P36 |
| KIC-L31 | (review) Reword the Grid page's Defaults tooltip: "Restore every tab of the entry selected on the left, for the unit in the band, to its defaults. The other unit keeps its own." | It states the real blast radius (the rail entry, not the tab on screen). | 80% | P37 |
| KIC-L32 | (review) Reword the rail-entry tooltips in the same change as the tab merges. Icons: "The interrupt icons: size and layout, appearance, text and tooltip, and ready glow." Cast bar: "The cast bar: size and position, text, and the colors for casts you can and cannot interrupt." | They name the tabs that exist after L08/L12/L14-L18. | 85% (conditional on the merges) | P38 |
| KIC-L33 | (review) Unit picker tooltip: append "Focus's link to Target is the tick beside this picker." (after L01), or "...on the General page's Units tab." if L01 is not taken. | Says where the switch the tooltip mentions lives. | 70% | P40 |

33 changes (28 proposed, 5 added in review; one alternative inside L05 struck). Tab count goes from 20 to 14
(General 2→1, Icons 6→4, Cast bar 8→5, Text label 3, Spells 1). Without L01/L02 it is 15. No row is added or removed, and every key, default, range and Defaults blast radius is unchanged.

## Proposed map

```
Ka0s KickCD (landing)                    unchanged (options-ui-§5 fixed)

General
  Tab "Master controls"                  unchanged canonical set (options-ui-§15 fixed)
    [Enable KickCD] | [General visibility  (Always / In combat / When the tracked unit is casting /
                                            When the tracked unit is casting an interruptible spell)]   <- L22, L30
    [Master scale]  | [Master alpha]
    [Lock frame]    | [Debug console]
    [Minimap button]
    [Reset position BTN] | [Reset all settings BTN]
  (Tab "Units" removed: L02)

Units  (was "Grid": L06)
  Band (one O.PageHeader block, picker inside): [Unit DD] [Enable <Unit> CB units.<u>.enabled]
        [Use same styling as Target CB units.focus.link]* [Copy styling from Target BTN]*
        (* Focus only; rows keep panel = "general")                                   <- L01, L03, L33
  Defaults tooltip: "Restore every tab of the entry selected on the left ..."           <- L31
  Rail: Icons | Cast bar | Text label                                                   <- L07
  Linked Focus: inert strip (Text label > General stays live, L05) +
        "Linked to Target. Untick Use same styling as Target above to give Focus its own look."   <- L04

  Rail "Icons"
    Tab "Size and layout" (10)                                                          <- L08
      sub "Size"
        [Primary size (in px)] | [Secondary size (fraction of primary)]                 <- L10
        [Gap (in px)]          | [Icon zoom]
      sub "Secondary block"
        [Anchor on primary icon] | [Growth direction]                                   <- L09
        [Rows]                   | [Columns]
        [X offset (in px)]       | [Y offset (in px, positive = down)]                  <- L11
    Tab "Appearance" (10)                                                               <- L12
      sub "States"
        [Ready alpha]   | [Cooldown alpha]
        [Cooldown tint] | [Use class color]
        [Suppress GCD swipe and text]                                                   <- L13
      sub "Border"
        [Show border]
        [Border style] | [Border thickness (px)]
        [Border color] | [Use class color]
    Tab "Text and tooltip" (11)                                                         <- L14, L15
      sub "Cooldown text"
        [Show cooldown text] (solo)
        [Font]       | [Font size]
        [Font color] | [Use class color]
        [Font flags] | [Font shadow]
      sub "Charges"
        [Show charges] (solo)
        [Charges X offset (in px)] | [Charges Y offset (in px)]
      sub "Tooltip"
        [Show tooltip on hover]
    Tab "Ready glow" (34)                unchanged (P19 needs upstream hiddenIf)
      sub "Effect" (triggers read "When the tracked unit is casting ...": L22)
      sub "Button (rotating rays)" / "Proc (flipbook)" / "Pixel border" / "Auto cast sparkles" /
          "Reach" (was "Offset"; rows "... horizontal / vertical reach (in px)": L29)

  Rail "Cast bar"
    Tab "General" (4)                                                                   <- L16
      [Enable cast bar] (solo)   tooltip "Show this unit's cast bar."                   <- L20
      [Orientation] | [Growth direction]
      [Show spark]
    Tab "Size and position" (10)
      sub "Size"
        [Auto-size to icon grid] (solo)                                                 <- L16
        [Cast bar width (in px)] | [Cast bar height (in px)]
      sub "Position"
        [Anchor mode] (solo)
        [Anchor on primary icon] | [Anchor on cast bar]
        [X offset (in px)]       | [Y offset (in px)]        (tooltips gain the sign: L21)
      sub "Spell icon"                                                                  <- L17
        [Icon position] | [Icon size (in px)]                (tooltip cross-ref: L28)
    Tab "Text" (15)                                                                     <- L18
      sub "Spell name"
        [Show spell name] | [Anchor]
        [X offset (in px)] | [Y offset (in px)]
        [Truncate after (characters)]
      sub "Cast time"
        [Show cast time] | [Anchor]
        [X offset (in px)] | [Y offset (in px)]
      sub "Font (both texts)"                                                           <- L18 (P39)
        [Font]            | [Font size]
        [Cast time color] | [Use class color]
        [Font flags]      | [Font shadow]
    Tab "Interruptible" (13)
      sub "Bar" / "Background" / "Spell name" (was "Text": L19) / "Border"
    Tab "Non-interruptible" (13)
      sub "Bar" / "Background" / "Spell name" (L19) / "Border"

  Rail "Text label"
    Tab "General" (2)
      [Show label] | [Label text]   (Label text alwaysPerUnit: editable while linked, L05)
    Tab "Placement" (8)
      sub "Position"                                                                    <- L23
        [Attach to] (solo)
        [Anchor on label] | [Anchor on attached widget]                                 <- L24
        [X offset (in px)] | [Y offset (in px)]
      sub "Alignment"                                                                   <- L23
        [Horizontal alignment] | [Vertical alignment]                                   <- L25
        [Rotation (degrees)]
    Tab "Font" (6)                       unchanged

Spells
  Band: [Class and specialization DD] (L26), [Add a spell]
  Tab "Spell list": rows = [handle][enabled CB][icon][name][known glyph][Category DD][remove]   <- L27

Profiles                                 unchanged (options-ui-§3 fixed)
```

Counts after: 5 pages, 14 tabs, the same 282 schema rows.

## Considered and rejected

| change | why rejected | confidence it would help |
|---|---|---|
| Merge Cast bar "Interruptible" and "Non-interruptible" into one "Colors" tab with the two states as subsections | 26 rows on one tab, and the two states are the same 13 rows twice; the tab names already say which state you are in, and the split lets the player flip between the two to compare. Saves one click at the cost of a long scroll. | 30% |
| Give Ready glow its own rail entry (Icons \| Ready glow \| Cast bar \| Text label) to take the 34-row tab off Icons | A rail entry is a folded sub-page (options-ui-§13), so the rows would need a new `panel` stamp, which moves the Grid page's Defaults blast radius: out of scope. It also adds an entry instead of removing a tab. | 30% |
| Move "Show tooltip on hover" to General > Master controls | It is per-unit (`u.icons.showTooltip`), and options-ui-§15 forbids per-instance rows there. | 10% |
| Rename "Lock frame" to "Lock frames" | Fixed composer label, options-ui-§15 "MUST NOT rename". Kept under upstream suggestions. | n/a (forbidden) |
| Hide or drop the Spells row's informational Category dropdown | Removes a control; forbidden by the brief. Its width (P30) stays. | n/a (forbidden) |
| Swap the Grid page's band and nav rail so Unit is a rail entry | §14: "The rail is not a picker". | n/a (forbidden) |

## Cross-addon notes / Upstream suggestions

Cross-addon (the same concept should have the same name and place everywhere):

- **Per-instance enable and link controls.** KickCD keeps them on General > Units. AbsorbTracker keeps the enables on
  General > Bars and the link/copy pair in its unit band (`inputs/layout/AbsorbTracker.md`). Choose one
  collection-wide answer. I recommend the band (or §14's `General` rail entry) for everything about the selected
  instance.
- **Link vocabulary.** KickCD says "Use same styling as Target" / "Copy styling from Target" / "Linked to Target".
  AbsorbTracker's key is `mirror` with the same label. Choose one verb ("link") for the hint text in every addon
  with the feature.
- **The "Size and position" shape.** Every addon whose surface has a size and an anchor should use one tab with
  "Size" and "Position" subsections (KickCD's Cast bar now, and its Icons after L08). That gives "where is width"
  one answer.
- **Two-point anchors.** Use "Anchor on <this element>" / "Anchor on <the thing it attaches to>" everywhere (L09,
  L24), not "Anchor point", "Attach point" or "relative point".
- **Text toggles head their own block.** "Show X" is the first, solo row of the subsection that styles X (KickCD
  L14 and Cast bar's Spell name / Cast time). Check siblings for a show toggle separated from its styling.
- **Unit suffixes.** KickCD uses "(in px)" and "(in seconds)", while the composer uses "(px)". Pick one form
  collection-wide (AbsorbTracker's analysis recommends "(px)"). That is a sweep of every host label, not a
  KickCD-only fix.
- **Sentence case** in rail entries and tabs ("Text label", not "Text Label").
- **Railed-page Defaults tooltips** should say the blast radius is the whole rail entry (L31). Check AuraMaster's
  Containers page and MultiMeters' Windows page, the other railed pages.
- **Glow knobs.** DropWatcher shares `Const.GLOW_KNOBS`; if L29 ("reach") is taken, rename the same rows there.
- **No `+` in labels or tooltips** ("icon grid + cast bar", "swipe + text"): a quick collection-wide grep.
- **"alpha" vs "opacity".** The canonical composer labels say "Master alpha" and "Bar opacity". Host rows follow
  whichever is nearest. Pick one word.

Upstream suggestions (WowAddonStandards / LibKa0s):

- **LibKa0s Options: `hiddenIf`** beside `disabledIf`. Ready glow's 26 style knobs are the worst case in the
  collection: a 34-row tab where at most 10 rows apply. DropWatcher's upgrade glow shares `Const.GLOW_KNOBS` and
  would gain the same.
- **LibKa0s OptionsCompose: a host override for the Reset position tooltip** (and a `tooltips` map beside `labels`
  in general). KickCD's reset moves the icon grids only (P27), and the canonical sentence misdescribes it.
- **options-ui-§14: the band at one row.** L01 needs four cells for Focus (picker, enable, link, copy). If that
  overflows at default scale, the escape costs a rail entry that Target would fill with one checkbox.
  AbsorbTracker raised the same tension. Suggest allowing a second band row holding only acts on the selected
  instance.
- **options-ui-§15 "Lock frame".** The singular reads oddly in an addon with four movable frames (two grids, two
  cast bars). Allow "Lock frames", or keep it and say why. This is flagged, not violated.
- **options-ui-§7: define "mixes control types".** The example is about subjects (bar / background / border), but
  the words read as widget types, under which most KickCD tabs (and most of the collection's) would be MUST
  failures today. Suggest "a tab that covers more than one subject" (P25).
- **LibKa0s Options: `PageBanner` plus acts.** L01 has to drop `PageBanner` for a hand-drawn `PageHeader` only to
  put a checkbox and a button beside the picker. A `PageBanner{ acts = {...} }` arm would keep the picker
  library-drawn.
- **LibKa0s OptionsTabs: an inert-tab flag on the strip spec.** KickCD's `deadenStrip` (Panel_Render.lua:193-205)
  is host-local. With L05 the linked page needs per-tab live/inert, which belongs in the library if a second addon
  links instances.

## Review

Independent review against `../KickCD` on `master`, 2026-10-24. I re-read `settings/{General,Grid,Icons,Castbar,Label,Panel_Render,Spells_Header,Spells_Rows}.lua`,
`defaults/Profile.lua`, `modules/UnitLabel.lua`, `docs/ARCHITECTURE.md` (Documented deviations), the LibKa0s
`PageBanner` / `PageHeader` docs and options-ui §7, §13-§18.

- **Current map: accurate.** Every tab, subsection, label, key and row count I checked matches the code (Icons 65,
  Cast bar 55, Text label 16, General 10; 20 tabs). The Test mode omission is the §15 "unlocked view is the test
  mode" exemption, as stated. I made no corrections to the map.
- **No proposed change alters a key, default, range or behaviour.** L05 exposes a row that is already per-unit
  while linked (`defaults/Profile.lua:339`); L01/L02 keep the `panel = "general"` stamp, so no Defaults blast
  radius moves.
- **Struck:** L05's alternative "open the linked page on the General tab". Forcing the tab on a unit switch breaks
  options-ui-§14 ("changing instance MUST leave ... each entry's tab alone"), and it would leave a player stuck on a
  dead strip.
- **Rewritten:** L01 now names the mechanism (`O.PageBanner` draws exactly one Dropdown, so the band has to become
  one `O.PageHeader` block with the picker inside it, per §14's one-block rule). It also records the side effect
  of keeping the stamp: General's Defaults would reset rows that are no longer drawn on General. That is the
  owner's call, not a reason to move the stamp. L11 "+ is down" became "positive = down", because L13 bans `+`
  in labels. L18's Font subsection is now "Font (both texts)". L22 now reads "the tracked unit", because "the
  unit" has no referent on the unit-less General page, and it notes the docs that quote the value list.
- **Softened:** P25's options-ui-§7 claim. Read literally, "mixes control types" would make most KickCD tabs MUST
  failures today, so the rule's intent is subjects. Clarifying it is now an upstream suggestion.
- **Added:** P35-P40 and L29-L33. Glow "offset" rows are really a reach. The General visibility tooltip uses `+`
  and leaves out the label. The Grid page's Defaults tooltip says "section on screen", but the blast radius is the
  whole rail entry. The rail-entry tooltips list tab names that the merges make stale. The Unit picker tooltip
  does not say where the link switch is.
- **Added sections:** "Considered and rejected" (merging the two cast-state tabs, a Ready glow rail entry, and
  three forbidden moves), plus cross-addon and upstream notes (railed Defaults wording, glow-knob naming shared
  with DropWatcher, no `+` in labels, the §7 wording, `PageBanner` with acts).
- **Confidence recalibrated:** L01 60→55, L02 60→55 (the Defaults caveat), L05 70→65 (it needs a host-local
  strip change), L22 70→65 (docs ripple). No change fell under 40%. L27 stays at the 40% floor: the
  checkbox-first argument is real, but the row's icon-name-checkbox reading order is also defensible.
