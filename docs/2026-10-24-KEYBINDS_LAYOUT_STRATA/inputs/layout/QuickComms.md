# QuickComms — settings layout analysis

Item 020. A read-only analysis of `../QuickComms` at `master` (2026-10-24). The map was built from the
source (`settings/*.lua`) and checked against `docs/settings-panel.md`. Line numbers refer to that tree.
The options library orders a page's tabs by the first schema row of each `group` (options-ui-§13). Inside
a tab, rows pair two per line unless a row carries `startsLine`. A composed color pair
(`O.ColorPair`, `libs/LibKa0s/OptionsCompose.lua:222`) always starts its own line, with the swatch on the
left and *Use class color* on the right.

Notation: `[cb]` checkbox, `[dd]` dropdown, `[sl]` slider, `[sw]` color swatch with its *Use class color*
companion (two keys: `<k>` and `useClassColor<K>`), `[eb]` edit box, `[btn]` button, `[media]` LSM
dropdown. `FONT6` is the composed font block (`font | fontSize`, `fontColor | useClassColorFont`,
`fontFlags | fontShadow`). `BORDER4` is the composed border block (`borderStyle | borderSize`,
`borderColor | useClassColorBorder`). `SL` means the row starts a line. `(alone)` means the row sits by
itself on its line. `(session)` means `sessionOnly`. `»` marks a subsection heading (a row `subgroup`).

The planned change is factored in. General gains a **Keybindings** tab, after Behavior, for *Toggle Comms
Pads* and *Open Comms Dial 1-4* (`Bindings.xml:6-13`), synced with Blizzard's Keybindings, where the
addon's own category is "Ka0s Quick Comms". The research file (`../KEYBINDINGS_RESEARCH.md` §1.6) records
that QuickComms put an in-panel key box on the Dial page on 2026-10-20 and removed it on 2026-10-21. The
new tab supersedes that decision. QUI-L29 below only points at the tab and adds no second key editor.

## Current map

**Counts.** There are 7 sidebar entries: the landing page, 5 flow-rendered pages (General, Groups, Pad,
Dial, Share) and Profiles. There are **26 tabs**: General 2, Groups 4, Pad 8, Dial 10 and Share 2. Profiles
is AceDBOptions and has none. About **233 setting keys** are drawn: General 16, Groups 8 (band 1, General
6, When 1, a single structured row with 12 drawers), callout popup 5, Pad 100 (Icons shows 18 to 29,
depending on the glow style) and Dial 104. The Dial strip **wraps to a second row** with 10 tabs
(settings-panel.md:535-536).

```
Landing "Ka0s Quick Comms"                       settings/Panel.lua:25 (BuildLandingPage) — logo, notes, Slash Commands

General page                                     Panel.lua:82 (CreatePanel), :91 (RenderTabbedSchema), :96 (Register)
├─ Tab "Master controls"                         Panel.lua:44 (MasterControls composer)
│    Enable Ka0s Quick Comms [cb] enabled SL     | General visibility [dd] visibility
│    Master scale [sl] scale SL                  | Master alpha [sl] alpha
│    Lock frame [cb] locked SL                   | Debug console [cb] state.debugConsole (session)
│    Minimap button [cb] global.minimap.shown SL | Test mode [cb] state.testMode (session)
│    Preview as [dd] state.previewAs (session) SL (alone)                  ← composer `extra`, Panel.lua:60-66
│    [btn] Reset position                        | [btn] Reset all settings
└─ Tab "Behavior"                                settings/SchemaRows.lua:36-62 (no subsections)
     When you are solo [dd] behavior.soloFallback | Spam guard (seconds) [sl] behavior.spamGuard
     Note dropped callouts in chat [cb] behavior.dropNotes | Explain why groups show [cb] behavior.whyTooltips
     Show the lockdown tag [cb] behavior.lockdownChip | Play a sound on send [cb] behavior.sounds
     Promote specific groups [cb] behavior.autoPromote (alone)

Groups page                                      settings/Groups.lua:725 (render), :731-737 (Ed.Tabs), :766 (RegisterPage)
├─ band (O.PageHeader, G.BAND_H = 72 px: TWO rows) Groups.lua:599, 686-723
│    [dd] Group (picker, green dot = active now)  | [btn] New group
│    Preview while editing [cb] behavior.previewOnEdit (left half of row 2, Groups.lua:648-653; skipRender row, SchemaRows.lua:66)
├─ Tab "General"                                 Groups.lua:342-371
│    Name [eb] group.name                        | Enabled [cb] group.enabled
│    Parent group [dd] group.parent              | Inherit when conditions [cb] group.inheritWhen   (host items, :135, :168)
│    Icon (label) / [icon][btn Choose icon…][clear glyph] Icon color [sw-host] group.icon + group.iconColor (Ed.IconChooser)
│    [btn] Duplicate                             | [btn] Delete
│    [btn] Restore built-in groups (alone)       Groups.lua:206
├─ Tab "Callouts"                                Groups.lua:441-466
│    [btn] Add callout (full row)
│    [dd] Reuse callout ………………… [btn] Add
│    reorder list: handle · icon · name · channel · text · [edit] [remove]
│    → Callout popup (CalloutPopup.lua): Name [eb] callout.name | Channel [dd] callout.channel;
│      Text [eb] callout.text (full width, token glyph); Icon chooser callout.icon + callout.iconColor;
│      » Preview (baked line, host-drawn h.Section, CalloutPopup.lua:386); [btn] Save | [btn] Cancel (:393-397)
├─ Tab "When"                                    settings/Groups_When.lua:665-687
│    active-now line; (inheriting: "Uses <parent>'s conditions. Untick Inherit when conditions on the General tab…" :681)
│    gray hint line (:684)
│    12 drawers over group.when: Content, Instance, Difficulty, Key level, Group, Leader or assist, Class,
│    Specialization, Role, Character, Battleground, Arena
└─ Tab "Preview"                                 Groups.lua:500-520 — active-now line, Callout | What it sends here table

Pad page                                         settings/Pads.lua:254 (render), :269-278 (Ed.Tabs), :281 (RegisterPage)
├─ band (O.PageBanner): [dd] Pad | [btn] New pad                Pads.lua:259
├─ Tab "General"                                 Pads.lua:149-167; rows SchemaMembers.lua:221-241
│    Name [eb] pad.name                          | Enabled [cb] pad.enabled
│    » Visibility
│    Visibility [dd] pad.look.visibility         | Fade [dd] pad.look.fade
│    Faded alpha [sl] pad.look.fadeAlpha (alone)
│    [btn] Unlock pads / Lock pads (writes master `locked`) | [btn] Delete pad
├─ Tab "Groups"                                  Pads.lua:169-193; SchemaMembers.lua:242
│    Show groups as [dd] pad.groupsAs (alone)
│    hint line ("Higher groups come first…", or "This pad lists no group. Add one below."); reorder list (remove glyph)
│    [dd] Add a group                            (below the list, :191)
├─ Tab "Layout"                                  Pads.lua:217-229; SchemaMembers.lua:246-272
│    Orientation [dd] pad.layout.orientation     | Grid columns [sl] pad.layout.columns (grayed unless Grid)
│    Growth [dd] pad.layout.growth               | Button style [dd] pad.layout.style
│    Scale [sl] pad.layout.scale                 | Spacing [sl] pad.layout.spacing
│    Position (host-drawn h.Section, :225)
│    X offset [eb] pad.point[3]                  | Y offset [eb] pad.point[4]
│    [btn] Reset this pad's position (alone)
├─ Tab "Pad header"                              SchemaMembers.lua:414-419
│    » Size:       Header height [sl] pad.header.height SL (alone)
│    » Font:       FONT6 pad.header.*
│    » Background: Background [sw] pad.header.background
│    » Border:     BORDER4 pad.header.*
├─ Tab "Section header"                          SchemaMembers.lua:420-425
│    » Size:       Section header height (0 = automatic) [sl] pad.section.height SL (alone)
│    » Font:       FONT6 pad.section.*
│    » Background: Background [sw] pad.section.background
│    » Border:     BORDER4 pad.section.*
├─ Tab "Window"                                  SchemaMembers.lua:427
│    » Background: Background [sw] pad.look.background
│    » Border:     BORDER4 pad.look.*
├─ Tab "Buttons"                                 SchemaMembers.lua:485-522
│    » Size:   Button width [sl] pad.button.width SL | Button height (0 = automatic) [sl] pad.button.height
│    » Color:  Background [sw] pad.button.background
│    » Border: BORDER4 pad.button.*
│    » Font:   FONT6 pad.button.*
│    » Glow:   Glow [cb] pad.button.glowEnabled SL | Glow style [dd] pad.button.glowType (grayed while off)
│              Glow color [sw] pad.button.glowColor
│    » Shine:  Shine look [dd] pad.button.shineLook SL | Shine strength [sl] pad.button.shineStrength
│              Shine tint [sw] pad.button.shineTint      (swatch grayed at None)
│              Bloom color A [sw] pad.button.shineBloomA (grayed unless Fluid glass)
│              Bloom color B [sw] pad.button.shineBloomB (grayed unless Fluid glass)
└─ Tab "Icons"                                   settings/SchemaIcons.lua:95-191, render Pads.lua:244
     » Size and crop: Icon size [sl] pad.icon.size | Zoom [sl] pad.icon.zoom
     » Color:  Desaturate [cb] pad.icon.desaturate | Icon opacity [sl] pad.icon.alpha
               Tint [sw] pad.icon.tint
     » Border: Show border [cb] pad.icon.borderShow SL (alone); BORDER4 pad.icon.* (style, thickness grayed while off)
     » Glow:   Glow [cb] pad.icon.glowEnabled SL | Glow when [dd] pad.icon.glowWhen
               Glow style [dd] pad.icon.glowType (alone); Glow color [sw] pad.icon.glowColor
     » Offset: Glow X offset [sl] pad.icon.xOffset | Glow Y offset [sl] pad.icon.yOffset
     » <selected style> knobs only (Settings.ShownIconRows, SchemaIcons.lua:198):
         Pixel border: Lines | Line speed; Line length (0 = automatic) | Line thickness; Dark border
         Auto cast sparkles: Sparkles | Sparkle speed; Sparkle size
         Button (rotating rays): Ray speed
         Proc (flipbook): Loop duration (seconds) | Start animation

Dial page                                        settings/Dials.lua:290 (render), :305-317 (Ed.Tabs), :320 (RegisterPage)
├─ band (O.PageBanner): [dd] Dial | [btn] New dial               Dials.lua:295
├─ Tab "General"                                 Dials.lua:178-189
│    Name [eb] dial.name                         | Enabled [cb] dial.enabled
│    [btn] Delete dial (alone)
├─ Tab "Groups"                                  Dials.lua:191-215
│    Show groups as [dd] dial.mode (alone); hint; reorder list; [dd] Add a group (below the list)
├─ Tab "Wheel"                                   Dials.lua:259-271; SchemaMembers.lua:288-307
│    Wedges per ring [dd] dial.slices            | Ring radius [sl] dial.radius
│    Open at [dd] dial.openAt (alone)
│    Position (host h.Section, :267): X offset [eb] | Y offset [eb] dial.point; [btn] Reset this dial's position
├─ Tab "Slices"                                  SchemaMembers.lua:574-601
│    » Background: Slice color [sw] dial.slice.background
│    » Gap:        Slice gap [sl] dial.slice.gap SL (alone)
│    » Highlight:  Highlight color [sw] dial.slice.highlight
│    » Shine:      Shine look | Shine strength; Shine tint [sw]; Bloom color A [sw]; Bloom color B [sw]  (dial.slice.shine*)
├─ Tab "Hub"                                     SchemaMembers.lua:543-571, 604-618
│    » Hub:     Hub style [dd] dial.hub.style SL | Hub size [sl] dial.hub.size
│               Circle size [sl] dial.hub.circleSize SL | Line width [sl] dial.hub.lineWidth (grayed under Solid)
│               Backdrop color [sw] dial.hub.background
│               Hub border size [sl] dial.hub.borderSize SL (alone)
│               Hub border color [sw] dial.hub.borderColor
│               Circle color [sw] dial.hub.circleColor
│    » Pointer: Show pointer [cb] dial.slice.pointerShow SL | Pointer size [sl] dial.slice.pointerSize
│               Pointer offset (0 = automatic) [sl] dial.slice.pointerOffset SL (alone)
│               Pointer color [sw] dial.slice.pointerColor (grayed while off)
├─ Tab "Paging"                                  SchemaMembers.lua:630-692
│    » Position:       Offset [sl] dial.page.offset SL (alone)
│    » Arrows:         Arrow size [sl] SL | Arrow spacing [sl]; Arrow color [sw]; Arrow background [sw] (plateColor)
│    » Page indicator: Dot size [sl] SL | Current page width [sl] (pillWidth)
│                      Dot spacing [sl] dotGap SL (alone)
│                      Current page color [sw]; Other pages color [sw]
│                      Show indicator background [cb] dotBackShow SL (alone)
│                      Indicator background [sw] dotBackColor (grayed while off)
│                      Background padding [sl] dotBackPadding SL (alone, grayed while off)
│                      Dot border (0 = none) [sl] dotBorder SL (alone)
│                      Dot border color [sw] dotBorderColor (grayed at 0)
├─ Tab "Slice labels"                            SchemaMembers.lua:702-731
│    Show labels [cb] dial.label.show SL         | Label offset (0 = automatic) [sl] dial.label.offset   (no subgroup: no heading)
│    » Font:    FONT6 dial.label.* (all grayed while labels off, the color too)
│    » Tooltip: Tooltip side [dd] dial.label.tooltipSide SL | Tooltip offset [sl] dial.label.tooltipOffset
├─ Tab "Group labels"                            SchemaMembers.lua:739-753
│    Show group labels [cb] dial.title.show SL (alone)
│    » Font:    FONT6 dial.title.* (grayed while off, the color too)
├─ Tab "Icons"                                   SchemaMembers.lua:762-773 + SchemaIcons.lua
│    » Size and crop: Icon offset (0 = automatic) [sl] dial.iconOffset | Icon size (0 = automatic) [sl] dial.icon.size
│                     Zoom [sl] dial.icon.zoom (alone)
│    » Color / Border / Glow / Offset / style knobs: as the Pad page's Icons tab, under dial.icon.*
└─ Tab "Preview"                                 Dials.lua:273-282 — one text block: rings, wedge by wedge

Share page                                       settings/Share.lua:217-229
├─ Tab "Export": intro line; » one heading per kind (Groups / Comms Pads / Comms Dials) with a checkbox grid;
│                summary line; [btn] Export | [btn] Clear
└─ Tab "Import": paste box; report; [btn] Import | [btn] Clear

Profiles page                                    settings/Profiles.lua:46 (AceDBOptions)
```

## Problems

General page

- **QUI-P01**: Behavior mixes three subjects under one label with no subsection heading: what a send
  does (solo fallback, spam guard, sound, drop note), what the pads and dials show (lockdown tag, why
  tooltips) and how groups are ordered (promote). options-ui-§7 requires subsection headings on a mixed
  tab. `settings/SchemaRows.lua:36-62`.
- **QUI-P02**: Behavior's pairing does not follow the subject. *Play a sound on send*, a send option, is
  paired with *Show the lockdown tag*, a display option. *Promote specific groups* is left alone at the end.
  `SchemaRows.lua:54-62`.
- **QUI-P03**: Three Behavior labels are vague.
  - *Promote specific groups* does not say promoted over what, or where. Its tooltip says "groups for a
    specific dungeon or battleground move above general ones".
  - *Explain why groups show* does not say that it acts in tooltips.
  - *Show the lockdown tag* does not show the tag as it appears (LOCKDOWN).
  `SchemaRows.lua:51, 54, 60`.
- **QUI-P04**: "Preview" means five different things across the panel:
  - *Preview as* (Master controls)
  - *Preview while editing* (Groups band)
  - the Groups page's *Preview* tab, a table of what each callout sends
  - the Dial page's *Preview* tab, a text listing of the rings
  - the callout popup's *Preview* heading

  The two tabs are listings, not previews. The real previews are the drawn pads and dials. A player who
  reads "Preview" on a tab expects the dial to be drawn. `Panel.lua:60`, `SchemaRows.lua:66`,
  `Groups.lua:736`, `Dials.lua:315`.

Groups page

- **QUI-P05**: The *Inherit when conditions* checkbox is on General (`Groups.lua:357`), but what it does
  shows on When. While it is ticked, the When tab tells the player to "Untick Inherit when conditions on
  the General tab to set this group's own" (`Groups_When.lua:681`). Writing a group's own conditions
  therefore takes two tabs: When, then General to untick, then back to When.
- **QUI-P06**: General splits the group's identity. Name and Enabled come first, then nesting (Parent group
  and Inherit), then the Icon. The icon is the other half of what the pad and the dial draw for the group.
  `Groups.lua:356-358`.
- **QUI-P07**: *Restore built-in groups* sits directly under *Duplicate | Delete*, with no gap and no
  heading. It reads as a fourth act on the selected group, but it acts on the whole library: it adds back
  every built-in group the profile no longer has. `Groups.lua:206-210, 370`.
- **QUI-P08**: The delete button is labeled *Delete* here but *Delete pad* and *Delete dial* on the other
  two editor pages. `Groups.lua:364`, `Pads.lua:165`, `Dials.lua:186`.
- **QUI-P09**: The Defaults tooltip is stale. It says Defaults will "stop it opening the dial". That
  setting (*Open the dial on this group*) was retired by the dial rework (settings-panel.md:566-567). The
  tooltip also leaves out that the icon and the parent are kept (`Schema.lua:193-195`). `Groups.lua:767`.
- **QUI-P10**: Where the add control sits is inconsistent. The Callouts tab puts *Add callout* and *Reuse
  callout* **above** the list (`Groups.lua:448-449`). The Pad and Dial Groups tabs put *Add a group*
  **below** the list (`Pads.lua:191`, `Dials.lua:213`), where a long list pushes it out of view. The verbs
  differ too: "Add callout" against "Add a group".

Pad page

- **QUI-P11**: The three look tabs run Pad header, Section header, Window. That orders the parts before the
  frame that holds them. The mental model works from the outside in: the window, its header, its section
  titles, its buttons, their icons. `SchemaMembers.lua:395-431` (the order of the first rows decides the
  tab order).
- **QUI-P12**: *Pad header* and *Section header* each open with a "Size" heading that holds one row
  (Header height, Section header height). Two lonely headings, and both rows are geometry like everything
  on Layout. `SchemaMembers.lua:414-424`.
- **QUI-P13**: The blocks run in a different order on each styled tab. Pad header and Section header run
  Size, Font, Background, Border (`SchemaMembers.lua:403-406`). Buttons runs Size, Color, Border, Font
  (`:499-510`). A player who has learned one tab cannot find Font on the next.
- **QUI-P14**: On Buttons the background block is headed **Color** (`SchemaMembers.lua:491, 507`). On Pad
  header, Section header and Window the same block is headed **Background**. On the Dial page's Slices tab,
  a heading named Background holds a row labeled *Slice color* (`:592`).
- **QUI-P15**: There are two **Glow** headings with the same row labels (*Glow*, *Glow style*, *Glow
  color*). One is the Buttons tab's glow, around the whole button (`SchemaMembers.lua:511-516`). The other
  is the Icons tab's glow, around the icon (`SchemaIcons.lua:161-167`). The button glow also draws at the
  Icons tab's knob defaults (settings-panel.md:491-492), and nothing on the Buttons tab says so.
- **QUI-P16**: The Icons tab's **Offset** heading holds *Glow X offset* and *Glow Y offset*
  (`SchemaIcons.lua:71-74`). On the Dial Icons tab the first row is *Icon offset* (`SchemaMembers.lua:764`),
  so an "Offset" heading lower down reads as more icon placement.
- **QUI-P17**: The terms disagree. The tab is "Section header", the label "Section header height", and its
  tooltip says "each section title's row" (`SchemaMembers.lua:397, 422-423`). Code and docs call them
  section titles throughout (`Pad.lua:134`, settings-panel.md:449). The headings are "Pad header" and
  "Section header", while Window has no "Pad" prefix.
- **QUI-P18**: *Unlock pads / Lock pads* on Pad > General is the **master** lock. It is the same switch as
  *Lock frame* on Master controls and `/qc lock` (`Pads.lua:158-164`). It sits on a page that edits one pad,
  and its label does not say that it moves every pad.
- **QUI-P19**: *Faded alpha* stays live while *Fade* is Never, so the dependent row is not gated.
  `SchemaMembers.lua:239`. *Grid columns* is gated on the same tab pattern (`:252`).
- **QUI-P20**: *Button style* (icon and label, icon only, or label only) is on Layout
  (`SchemaMembers.lua:257`). It decides what the button draws, and every other button property (width,
  height, font) is on Buttons. Button width moved from Layout to Buttons on 2026-10-20 for the same reason.
- **QUI-P21**: The Pad Defaults tooltip lists "groups-as, layout, headers, window, buttons and icons" but
  not General's Visibility, Fade and Faded alpha, which Defaults also resets. `Pads.lua:282`.
- **QUI-P22**: The Position heading is drawn by the host (`h.Section`, `Pads.lua:225`, `Dials.lua:267`),
  while every other heading comes from a row's `subgroup` (options-ui-§7: a subsection is declared by a
  row, never drawn by a builder). The `pad.point` and `dial.point` rows are structured rows the flow engine
  skips (`Editors.lua:190-200`), so no row can declare the heading. That is a library gap; see the upstream
  suggestions.

Dial page

- **QUI-P23**: With 10 tabs the strip wraps to two rows (settings-panel.md:535-536). options-ui-§13 says a
  page SHOULD keep one row. The tab a player wants is often on the row they are not looking at.
  `Dials.lua:305-317`.
- **QUI-P24**: *Slice labels* and *Group labels* are two tabs for one subject, the text drawn around the
  dial. Each is a Show toggle plus a font block. Group labels holds 7 rows. Comparing the two fonts means
  switching tabs. `SchemaMembers.lua:700-755`.
- **QUI-P25**: *Tooltip side* and *Tooltip offset* are on Slice labels (`SchemaMembers.lua:721-729`), but
  they place **every** dial tooltip: a wedge's, a page arrow's and the hub's *Why is this showing?*
  (settings-panel.md:595-597). They are not label settings.
- **QUI-P26**: *Slice gap* sits alone under its own **Gap** heading on Slices (`SchemaMembers.lua:593`).
  It feeds the Auto wedge count on Wheel: "fewer when the icons no longer fit … (the Slice gap counted)"
  (settings-panel.md:573-575). Tuning Auto takes both tabs.
- **QUI-P27**: Slices has two lonely headings. *Background* holds one color pair, labeled *Slice color*,
  and *Highlight* holds one color pair. `SchemaMembers.lua:592, 597`.
- **QUI-P28**: The Hub heading interleaves three sub-parts. Circle size is on line 2 and Circle color on
  line 6. Hub border size sits alone between the backdrop's color and the border's color. Line width (a
  ring-style setting) is paired with Circle size. `SchemaMembers.lua:553-570`.
- **QUI-P29**: Paging's **Position** heading holds one row labeled just *Offset*
  (`SchemaMembers.lua:654`). That is a lonely heading, and the label does not say offset of what from what.
- **QUI-P30**: *Page indicator* holds 14 rows across three sub-parts: the dots, their background and their
  border. Four rows sit alone on their lines (Dot spacing, Show indicator background, Background padding,
  Dot border). Background padding sits after the background color, away from the toggle it depends on.
  `SchemaMembers.lua:662-690`.
- **QUI-P31**: The tab names disagree for one concept. Pad says **Layout** (geometry plus Position). Dial
  says **Wheel** for the same thing (count, radius, open at, Position). `Dials.lua:49`, `Pads.lua:258`.
- **QUI-P32**: The Dial Icons tab opens its **Size and crop** heading with *Icon offset*
  (`SchemaMembers.lua:764`). An offset is neither a size nor a crop. *Zoom*, the only crop, is pushed alone
  onto the next line.
- **QUI-P33**: The Dial General tab holds only Name, Enabled and Delete. The dial's key, which is how the
  dial is opened, appears nowhere on the Dial page. After the planned General > Keybindings tab ships, it
  will be two pages away with nothing pointing there. `Dials.lua:178-189`.
- **QUI-P34**: The Dial Defaults tooltip lists "groups-as, wedges per ring, ring radius, icon offset, where
  it opens, its slices, paging, labels and icons". It leaves out the Hub tab and the tooltip placement,
  which Defaults resets (settings-panel.md:664-665). `Dials.lua:321`.
- **QUI-P35**: Some color swatches gray out with their gate:
  - Shine tint, Bloom A and Bloom B (`SchemaMembers.lua:478`)
  - Pointer color (`:616`)
  - Indicator background (`:676`)
  - Dot border color (`:688`)
  - both label font colors (`:718`, `:749`)

  options-ui-§17 forbids `disabledIf` on a color row (anti-pattern #74), and the Icons tab follows that
  rule (`SchemaIcons.lua:17-19`). Inside one addon, the Icons tab's color pairs never gray out, while
  these do. This is presentation only, not a setting.

Cross-page

- **QUI-P36**: The page names disagree. "Groups" is plural, while "Pad" and "Dial" are singular, for the
  same editor shape (one of many, picked in the band). The page keys are `pads` and `dials`
  (`Pads.lua:255`, `Dials.lua:46`). `Pads.lua:281`, `Dials.lua:320`. The rest of the addon uses the full
  nouns: the Share page's headings are *Comms Pads* and *Comms Dials* (`Share.lua:36-37`), and the bindings
  are *Toggle Comms Pads* and *Open Comms Dial N*.
- **QUI-P37**: The Groups band is **two rows** (`G.BAND_H = 72`, `Groups.lua:599`): picker and New group,
  then *Preview while editing* on the left half of a second row (`bandToggle`, `Groups.lua:648-653`, "the
  left half, so the Flow layout puts it on its own row"). Pad and Dial bands are one row, so the strip
  starts at a different height on the three editor pages. options-ui-§14 does **not** sanction this:
  "The band is ONE ROW". It sanctions a page-wide control in the band only beside the picker on that one
  row. *(Review: the draft said §14 sanctions the shape; it does not.)*
- **QUI-P38**: The Dial page uses two words for one thing. The tabs and most labels say **slice** (*Slices*,
  *Slice gap*, *Slice color*, *Slice labels*, and the keys `dial.slices` and `dial.slice.*`). *Wedges per ring*,
  the *Show labels* tooltip and the *Tooltip side* tooltip say **wedge** (`SchemaMembers.lua:289-290, 708, 724`).
  A player reads *Wedges per ring* and *Slice gap* as two different parts.
- **QUI-P39**: *Show labels* (Slice labels tab) and *Show group labels* (Group labels tab) are named
  asymmetrically. The first doesn't say which labels, and that gets worse if the two tabs are merged
  (QUI-L19). `SchemaMembers.lua:707, 744`.
- **QUI-P40**: The Pad Layout tab's *Scale* and *Spacing* don't say what they apply to. Master controls
  already has *Master scale*, and Paging has *Arrow spacing* and *Dot spacing*. The tooltips say "This pad's
  size, on top of the master scale" and "Pixels between buttons" (`SchemaMembers.lua:261-266`).
- **QUI-P41**: The empty-list hint on Pad > Groups and Dial > Groups says "Add one **below**"
  (`Pads.lua:179`, `Dials.lua:201`). The hint is tied to where the add control sits, so moving the control
  (QUI-L07) also has to change the hint.
- **QUI-P42**: The Dial page's *Preview* tab, a listing of each ring wedge by wedge, shows the result of the
  order set on Dial > Groups, but it is a separate tab. Checking a reorder takes two tabs, and with 10
  tabs those two sit on different strip rows. `Dials.lua:273-282, 305-317`.
- **QUI-P43**: The in-dial keys are fixed: 1-8 pick a wedge, the mouse wheel or Left/Right turns the page,
  Escape closes (`Dial_Secure.lua:149-159`). No settings page mentions them. The planned Keybindings tab is
  where a player will look for them.
- **QUI-P44**: Bindings.xml lists *Open Comms Dial 1-4* first and *Toggle Comms Pads* last
  (`Bindings.xml:6-13`), and Blizzard's Keybindings page draws them in that order. QUI-L32 proposes the
  reverse order in the panel, so the two lists the owner wants synced would disagree.

## Proposed changes

Every change moves, regroups or relabels. No setting key, default, range or behavior changes. "Schema
reorder" means moving a row's position in `settings/SchemaMembers.lua` or `settings/SchemaRows.lua`, which
is how the library orders tabs and lines.

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| QUI-L01 | Behavior: add subsections. **» Sending** holds *When you are solo* \| *Spam guard (seconds)*, then *Play a sound on send* \| *Note dropped callouts in chat*. **» Pads and dials** holds *Promote specific groups* \| *Show the lockdown tag*, then *Explain why groups show*. A `subgroup` on each row plus a reorder in `SchemaRows.lua`. | options-ui-§7 requires headings on a mixed tab, and the pairs then share a subject. | 80% | P01, P02 |
| QUI-L02 | Relabel: *Promote specific groups* becomes **Put instance-specific groups first**. *Explain why groups show* becomes **Explain why groups show (tooltips)**. *Show the lockdown tag* becomes **Show the LOCKDOWN tag**. Tooltips unchanged. | Each label then says what it does and where, without the tooltip. | 60% | P03 |
| QUI-L03 | Move *Inherit when conditions* (`group.inheritWhen`) from Groups > General to the **top of When**, under the active-now line and above the gray hint line. It is still drawn by hand (`inheritItem`) and stays grayed while Parent group is None. Its tooltip adds "Set the parent on the General tab." The inheriting line (`Groups_When.lua:681`) becomes "Uses <parent>'s conditions. Untick Inherit when conditions above to set this group's own." The row's `group` becomes When. Its schema position (`SchemaMembers.lua:211`, before `group.when` at :215) keeps When after General, and Callouts stays `before = WHEN`. | Choosing between the group's own conditions and its parent's is a When decision, and the read-only drawers below then have their cause right above them. The player finishes the task on one tab. | 75% | P05 |
| QUI-L04 | Groups > General order: *Name* \| *Enabled*, then the **Icon chooser**, then *Parent group* (alone after L03), then *Duplicate* \| **Delete group**. | Identity first (what the pad and the dial draw), then placement, then acts. | 60% | P06, P08 |
| QUI-L05 | Separate *Restore built-in groups* from the group's acts **without a heading**: a spacer, then a gray hint line, "Adds back the built-in groups and callouts you deleted. Changes nothing you have.", then the button. *(Review: the draft used a host-drawn heading, `h.Section`. options-ui-§7 says a heading is "never drawn by a builder", and that is the defect P22 already reports. A text line is not a heading.)* | It acts on the library, not on the selected group, and the gap and the hint say so. It stays on General because options-ui-§14 keeps page-wide acts out of every other tab. | 55% | P07 |
| QUI-L06 | Rewrite the Groups Defaults tooltip: "Turn the selected group back on, turn Inherit when conditions back on, and turn Preview while editing back on. Its name, icon, parent, callouts and own When are kept." | The current tooltip promises the reset of a retired setting. No group row is about the dial (`SchemaMembers.lua:184-218`), and `resetExempt` keeps the icon and the parent (`Schema.lua:193-195`). | 90% | P09 |
| QUI-L07 | Pad > Groups and Dial > Groups: draw the add dropdown **above** the list, right after *Show groups as*, and relabel it **Add group**. Change the empty-list hint to "This pad lists no group. Add one above." (and the same for the dial). | It matches the Callouts tab, and a long list no longer pushes the control off screen. The hint has to follow the control (P41). | 55% | P10, P41 |
| QUI-L08 | Rename the listing tabs and heading. The Groups page's *Preview* tab becomes **What it sends** (its own tab tooltip already says "What each callout sends here"). The callout popup's **» Preview** heading becomes **» What it sends**. The Dial page's *Preview* tab becomes **Ring map**, unless L33 folds it into Groups. Keep "Preview" for the drawn previews only (*Preview as*, *Preview while editing*). | It resolves five meanings of one word. A tab that lists text is not a preview, and the popup then uses the Groups tab's term for the same line. | 50% | P04 |
| QUI-L09 | Pad tab order: General, Groups, Layout, **Window**, **Header**, **Section titles**, Buttons, Icons. A schema reorder: move the `pad.look.*` window rows ahead of `pad.header.*` in `windowRows()` (`SchemaMembers.lua:411-427`). The library orders tabs by each group's first row (`OptionsTabs.lua:1186`). | Outside in: frame, then header, then titles, then buttons, then icons. | 55% | P11 |
| QUI-L10 | Rename the tabs *Pad header* to **Header** and *Section header* to **Section titles**. Relabel *Section header height (0 = automatic)* to **Section title height (0 = automatic)**. Keys are unchanged. | One term that matches the code, the docs and the tooltip, and the "Pad" prefix is redundant on the Pad page. | 50% | P17 |
| QUI-L12 | Buttons subsection order: **Size, Font, Background, Border**, Glow, Shine. That moves the Font block up, and the heading **Color** becomes **Background**. Label the swatch **Background color** on every styled tab (Header, Section titles, Window, Buttons). | The same block order and names on every styled tab. options-ui-§16 binds the rows inside a block, and this extends the same idea to the order of the blocks. | 70% | P13, P14 |
| QUI-L13 | Rename the glow headings: Buttons > *Glow* becomes **Button glow**, and Icons > *Glow* becomes **Icon glow** (both editors). The Buttons tab's *Glow style* tooltip adds: "Drawn at the Icons tab's default knobs." | Two subjects that look identical become two names, and the hidden dependency is stated. | 65% | P15 |
| QUI-L14 | Fold the Icons tab's **Offset** heading into **Icon glow**: *Glow X offset* \| *Glow Y offset* follow *Glow color* \| UCC under the same heading, on the Pad and Dial Icons tabs. The rows stay right after the glow, as the owner asked on 2026-10-20 (`SchemaIcons.lua:12-13`). *(Review: the draft only renamed the heading to "Icon glow offset". Both rows are glow rows, so a separate heading is not needed.)* | One fewer heading, and an offset can no longer be read as icon placement. | 60% | P16 |
| QUI-L15 | Relabel *Unlock pads / Lock pads* to **Unlock all pads / Lock all pads**. Its tooltip adds "The same switch as Lock frame on General > Master controls." | It is the master lock, so the label says it moves every pad. | 70% | P18 |
| QUI-L16 | Gray out *Faded alpha* while *Fade* is Never (`disabledIf`, presentation only; not a color row, so options-ui-§17 does not apply). | It matches *Grid columns* on the same page: a dependent row is gated. | 65% | P19 |
| QUI-L17 | Move *Button style* (`pad.layout.style`) from Layout to Buttons. The **» Size** heading becomes **» Size and style**: *Button style* \| *Button width*, then *Button height (0 = automatic)*. Layout then pairs *Growth* \| *Spacing* and leaves *Scale* alone. **Implementation:** the row has to move physically into `buttonRows()`, not just change its `group`. At `SchemaMembers.lua:257` it would become the Buttons group's first row and pull the Buttons tab ahead of the Header tabs. | Everything about one button is on one tab, the same reasoning as the owner's 2026-10-20 move of Button width. Against it: Button style also changes the pad's overall shape, and that is Layout's subject. | 45% | P20 |
| QUI-L18 | Rewrite the Pad Defaults tooltip: "Put the selected pad's visibility, groups-as, layout, header, section titles, window, buttons and icons back to their defaults, and turn it on. Its name, groups and position are kept." | It names everything Defaults resets. | 80% | P21 |
| QUI-L19 | Dial: merge *Slice labels* and *Group labels* into one **Labels** tab, with **two** headings, each holding its toggle and its font block. **» Slice labels**: **Show slice labels** \| *Label offset (0 = automatic)*, then FONT6 `dial.label.*`. **» Group labels**: *Show group labels*, then FONT6 `dial.title.*`. Pass each heading as the font group's `subgroup`. *(Review: the draft had four headings, "Slice labels", "Slice label font", "Group labels" and "Group label font". That is close to the second tab level options-ui-§7 forbids faking, and options-ui-§16 asks for only one heading per group.)* | One subject on one tab, the strip loses a tab, and the relabel makes the two toggles symmetrical (P39). | 55% | P23, P24, P39 |
| QUI-L20 | Move *Tooltip side* \| *Tooltip offset* (`dial.label.tooltip*`) to Wheel (L22: Layout), under **» Tooltip**, after Position. Relabel them **Tooltip side** and **Tooltip distance**. **Implementation:** `renderWheel` draws the rows and then the Position block (`Dials.lua:259-271`), so the host renders the Tooltip rows after Position. | They place every dial tooltip, which is dial placement and not label styling. Against it: the offset is measured from the labels and the page arrows (its tooltip, `:728`), and after L19 the Labels tab would be a natural home too. | 45% | P25 |
| QUI-L21 | Wheel (L22: Layout) regroup. *Wedges per ring* \| *Ring radius*, then *Slice gap* (moved from Slices > Gap) alone. *Open at* moves to the top of the Position block, alone, above X \| Y and the reset button (the host renders it after `h.Section`). *(Review: the draft paired Slice gap with Open at, which puts geometry beside placement. Open at's own tooltip says "at its place (set below)", so its home is the Position block.)* | The gap changes the Auto count beside it, a lonely heading goes, and every placement control then sits under Position. | 60% | P26 |
| QUI-L22 | Rename the Dial tab *Wheel* to **Layout**. | It matches the Pad page's tab for the same concept. | 50% | P31 |
| QUI-L23 | Slices: merge the **Background** and **Highlight** headings into **» Colors**: *Slice color* \| UCC, then *Highlight color* \| UCC. Shine follows. | Two one-pair headings become one. | 65% | P27, P14 |
| QUI-L24 | Hub regroup, with the rows reordered within the tab. **» Hub** holds *Hub style* \| *Hub size*, then *Backdrop color* \| UCC. **» Hub border** holds *Hub border size* alone, then *Hub border color* \| UCC. **» Hub circle** holds *Circle size* \| *Line width*, then *Circle color* \| UCC. **» Pointer** is unchanged. | Each sub-part's size sits next to its color, and the interleaving goes. | 60% | P28 |
| QUI-L25 | Paging: rename the heading **Position** to **Page row**, and relabel *Offset* to **Distance below labels**. | The label then says what it measures. The heading stays lonely, but its name now earns it. | 55% | P29 |
| QUI-L26 | Paging: split *Page indicator* into three headings. **» Page indicator** holds *Dot size* \| *Current page width*, *Dot spacing*, *Current page color* \| UCC, then *Other pages color* \| UCC. **» Indicator border** holds *Dot border (0 = none)*, then *Dot border color* \| UCC. **» Indicator background** holds *Show indicator background* \| *Background padding*, then *Indicator background* \| UCC. *(Review: the draft's heading names, "Page dots", "Dot border" and "Dot background", invented a third term beside the labels' "indicator". These names keep the existing one.)* | Three sub-parts get three headings, padding pairs with its own toggle, and one lonely line goes. | 60% | P30 |
| QUI-L27 | Dial Icons: rename the **Size and crop** heading to **Size, offset and crop**. Order the rows *Icon size (0 = automatic)* \| *Icon offset (0 = automatic)*, then *Zoom*. | The heading names what it holds, and size comes first as on the Pad tab. The owner moved Icon offset here from Wheel on 2026-10-21, so it is not moved back. | 50% | P32 |
| QUI-L28 | Rewrite the Dial Defaults tooltip: "Put the selected dial's groups-as, layout, slices, hub, paging, labels, tooltip placement and icons back to their defaults, and turn it on. Its name, groups, position and key are kept." | It names everything Defaults resets, and it says the key is kept. A binding is not a schema row, so Defaults cannot reach it. | 85% | P34 |
| QUI-L29 | Dial > General: add one read-only gray line under *Name* \| *Enabled*: "Key: <bound key, or Not bound>. Set it on General > Keybindings." It is re-read on show. There is no key box here, so the Keybindings tab stays the one editor. | The dial's main control is discoverable from the dial's own page without duplicating the editor. This respects the 2026-10-21 removal of the Dial key box. | 55% | P33 |
| QUI-L30 | Drop `disabledIf` from every **color pair**, the swatch and its *Use class color* companion together: Shine tint and Blooms on Buttons and Slices, Pointer color, Indicator background, Dot border color, and both label font colors. Every other row keeps its gray-out. Presentation only. *(Review: the draft kept the companion grayed beside a live swatch. That splits one pair, and the Icons tab's precedent is that "every color pair … is never dimmed", `SchemaIcons.lua:17-18`.)* | options-ui-§17 and anti-pattern #74, and it matches the Icons tab. If the owner prefers the gray-out, record that under upstream suggestion U1 instead. | 50% | P35 |
| QUI-L31 | Rename the sidebar entries *Pad* to **Comms Pads** and *Dial* to **Comms Dials** (the `Ed.RegisterPage` titles). The band labels stay *Pad* and *Dial*. *(Review: the draft said "Pads" and "Dials". The full nouns match Share, the binding names and the README.)* | It matches the plural *Groups* and the addon's own nouns. The band label names the single instance picked. | 40% | P36 |
| QUI-L32 | General page: add the planned **Keybindings** tab after Behavior. Rows follow **Bindings.xml order** (or item 015 reorders Bindings.xml and the tab follows it): *Open Comms Dial 1* to *4*, then *Toggle Comms Pads*. A dial's row shows its current name, and Blizzard's Keybindings list shows the same label (`BINDING_NAME_*` is set at `modules/Dial.lua:54` and can carry the name), so the two lists read alike. | The planned item 015 placement. The name tells the player which dial a binding numbered by place opens, and one order and one label keep the "synced" lists identical (P44). | 60% | P33, P44 |
| QUI-L33 | **New.** Dial: fold the *Preview* listing into **Dial > Groups**, under the reorder list, as a gray **"What the rings hold"** block that is refreshed live (`Ed.Live`, as now). Drop the Preview tab. | The listing is the result of the order set right above it (P42), and the strip loses a tab: 8 tabs with L19, which should fit one row. | 45% | P42, P23 |
| QUI-L34 | **New.** Groups band to **one row**: [Group picker] [New group] [x Preview while editing]. Narrow the picker and give the checkbox the rest (`bandToggle` drops its 0.5 relative width, `G.BAND_H` becomes the one-row height). If the label does not fit at minimum panel width, shorten it to **Preview group** with the full text in the tooltip. | options-ui-§14: "The band is ONE ROW" (P37). All three editor pages then start their strips at the same height. | 55% | P37 |
| QUI-L35 | **New.** One word on the Dial page: relabel *Wedges per ring* to **Slices per ring**, and say "slice" for "wedge" in the Dial page's tooltips (`SchemaMembers.lua:290, 708, 724`). | "Slice" is what the tabs, the other labels and the keys (`dial.slices`, `dial.slice.*`) already say (P38). | 50% | P38 |
| QUI-L36 | **New.** Pad > Layout: relabel *Scale* to **Pad scale** and *Spacing* to **Button spacing**. | They then can't be confused with *Master scale*, *Arrow spacing* or *Dot spacing*, and they say what they act on (P40). | 50% | P40 |
| QUI-L37 | **New.** Keybindings tab: under the dial rows, one gray hint line: "While a dial is open: 1-8 pick a slice, the mouse wheel or Left/Right turns the page, Escape closes." Read-only. | It is where a player looks for the dial's keys, and today nothing says them (P43). | 45% | P43 |

That is **36 layout changes**: 7 at 70% or more, 24 from 50% to 69%, and 5 from 40% to 49%. One draft change
(L11) moved to "Considered and rejected".

## Considered and rejected

| id | change | why rejected | confidence |
|---|---|---|---|
| QUI-L11 (draft) | Move *Header height* and *Section title height* to a **Layout > » Rows** heading. | *Section title height* at 0 "grows it to hold its font" (`SchemaMembers.lua:423`), and the header row is sized against its font. Height and font are tuned together, so the move adds a tab switch to the commonest task, to save two lonely headings. Keep the **Size** headings, which U4 already allows when the name explains the row. | 35% |
| — | Merge *Slices* and *Hub* into one tab, to reach 8 Dial tabs. | The owner split Hub off Slices on 2026-10-21 (`SchemaMembers.lua:526-533`). L19 plus L33 reach 8 tabs without undoing that. | 25% |
| — | Merge *Header*, *Section titles* and *Window* back into one look tab. | The owner split them on 2026-10-20 (`SchemaMembers.lua:319-323`), and the merged tab would hold three font, background and border sets. | 20% |
| — | Hide *Inherit when conditions* on When for a group with no parent, rather than gray it out. | It hides a row the player can read about in Enabled's and Parent group's tooltips, and a hidden row reads as a missing setting. | 35% |
| — | Fold the Groups page's *Preview* into the Callouts tab as a column. | The Callouts list already draws the text cut at 40 characters, and a second text column would not fit the stride (options-ui-§18). | 30% |

## Proposed map

```
Landing "Ka0s Quick Comms"                       (unchanged)

General page
├─ Tab "Master controls"                         (unchanged: canonical set + Preview as + reset pair, options-ui-§15)
├─ Tab "Behavior"
│    » Sending
│    When you are solo [dd] behavior.soloFallback | Spam guard (seconds) [sl] behavior.spamGuard
│    Play a sound on send [cb] behavior.sounds    | Note dropped callouts in chat [cb] behavior.dropNotes
│    » Pads and dials
│    Put instance-specific groups first [cb] behavior.autoPromote | Show the LOCKDOWN tag [cb] behavior.lockdownChip
│    Explain why groups show (tooltips) [cb] behavior.whyTooltips (alone)
└─ Tab "Keybindings"                             (planned item 015; Bindings.xml order, L32)
     Open Comms Dial 1 (<name>) [key] … Open Comms Dial 4 (<name>) [key]
     gray hint: "While a dial is open: 1-8 pick a slice, the mouse wheel or Left/Right turns the page, Escape closes." (L37)
     Toggle Comms Pads [key]

Groups page
├─ band (ONE row): [dd] Group | [btn] New group | Preview while editing [cb] behavior.previewOnEdit   (L34)
├─ Tab "General"
│    Name [eb] group.name                         | Enabled [cb] group.enabled
│    Icon / [icon][Choose icon…][clear] Icon color   group.icon + group.iconColor
│    Parent group [dd] group.parent (alone)
│    [btn] Duplicate                              | [btn] Delete group
│    (spacer) gray hint "Adds back the built-in groups and callouts you deleted. Changes nothing you have."
│    [btn] Restore built-in groups                (no heading, L05)
├─ Tab "Callouts"                                (unchanged, except the popup's » Preview heading becomes » What it sends)
├─ Tab "When"
│    active-now line
│    Inherit when conditions [cb] group.inheritWhen   (grayed while no parent)
│    (inheriting: "Uses <parent>'s conditions. Untick Inherit when conditions above to set this group's own.")
│    gray hint line; 12 drawers over group.when
└─ Tab "What it sends"                           (was Preview; content unchanged)

Comms Pads page   (sidebar "Comms Pads"; band label "Pad")
├─ band: [dd] Pad | [btn] New pad
├─ Tab "General"
│    Name [eb] pad.name | Enabled [cb] pad.enabled
│    » Visibility: Visibility [dd] pad.look.visibility | Fade [dd] pad.look.fade; Faded alpha [sl] pad.look.fadeAlpha (grayed at Never)
│    [btn] Unlock all pads / Lock all pads | [btn] Delete pad
├─ Tab "Groups"
│    Show groups as [dd] pad.groupsAs; [dd] Add group; hint ("… Add one above."); reorder list
├─ Tab "Layout"
│    Orientation [dd] pad.layout.orientation | Grid columns [sl] pad.layout.columns
│    Growth [dd] pad.layout.growth           | Button spacing [sl] pad.layout.spacing
│    Pad scale [sl] pad.layout.scale (alone)
│    Position: X offset | Y offset (pad.point); [btn] Reset this pad's position
├─ Tab "Window"
│    » Background: Background color [sw] pad.look.background
│    » Border:     BORDER4 pad.look.*
├─ Tab "Header"
│    » Size: Header height [sl] pad.header.height   » Font: FONT6 pad.header.*   » Background: Background color [sw]   » Border: BORDER4
├─ Tab "Section titles"
│    » Size: Section title height (0 = automatic) [sl] pad.section.height   » Font: FONT6 pad.section.*   » Background: Background color [sw]   » Border: BORDER4
├─ Tab "Buttons"
│    » Size and style: Button style [dd] pad.layout.style | Button width [sl] pad.button.width; Button height (0 = automatic) [sl]
│    » Font: FONT6 pad.button.*
│    » Background: Background color [sw] pad.button.background
│    » Border: BORDER4 pad.button.*
│    » Button glow: Glow [cb] | Glow style [dd] (tooltip names the Icons tab's default knobs); Glow color [sw]
│    » Shine: Shine look | Shine strength; Shine tint [sw]; Bloom color A [sw]; Bloom color B [sw]  (color pairs never grayed)
└─ Tab "Icons"
     » Size and crop: Icon size | Zoom
     » Color: Desaturate | Icon opacity; Tint [sw]
     » Border: Show border; BORDER4
     » Icon glow: Glow | Glow when; Glow style; Glow color [sw]; Glow X offset | Glow Y offset
     » <selected style> knobs

Comms Dials page   (sidebar "Comms Dials"; band label "Dial")
├─ band: [dd] Dial | [btn] New dial
├─ Tab "General"
│    Name [eb] dial.name | Enabled [cb] dial.enabled
│    gray line: "Key: <key or Not bound>. Set it on General > Keybindings."
│    [btn] Delete dial
├─ Tab "Groups"
│    Show groups as [dd] dial.mode; [dd] Add group; hint ("… Add one above."); reorder list
│    gray block "What the rings hold" (was the Preview tab, live; L33)
├─ Tab "Layout"                                   (was Wheel)
│    Slices per ring [dd] dial.slices | Ring radius [sl] dial.radius
│    Slice gap [sl] dial.slice.gap (alone)
│    Position: Open at [dd] dial.openAt (alone); X offset | Y offset (dial.point); [btn] Reset this dial's position
│    » Tooltip: Tooltip side [dd] dial.label.tooltipSide | Tooltip distance [sl] dial.label.tooltipOffset   (L20, 45%)
├─ Tab "Slices"
│    » Colors: Slice color [sw] dial.slice.background; Highlight color [sw] dial.slice.highlight
│    » Shine: Shine look | Shine strength; Shine tint [sw]; Bloom color A [sw]; Bloom color B [sw]
├─ Tab "Hub"
│    » Hub:        Hub style [dd] | Hub size [sl]; Backdrop color [sw] dial.hub.background
│    » Hub border: Hub border size [sl]; Hub border color [sw]
│    » Hub circle: Circle size [sl] | Line width [sl]; Circle color [sw]
│    » Pointer:    Show pointer | Pointer size; Pointer offset (0 = automatic); Pointer color [sw] (never grayed)
├─ Tab "Paging"
│    » Page row:             Distance below labels [sl] dial.page.offset
│    » Arrows:               Arrow size | Arrow spacing; Arrow color [sw]; Arrow background [sw]
│    » Page indicator:       Dot size | Current page width; Dot spacing; Current page color [sw]; Other pages color [sw]
│    » Indicator border:     Dot border (0 = none); Dot border color [sw]
│    » Indicator background: Show indicator background | Background padding; Indicator background [sw]
├─ Tab "Labels"                                   (Slice labels + Group labels)
│    » Slice labels: Show slice labels [cb] dial.label.show | Label offset (0 = automatic) [sl] dial.label.offset; FONT6 dial.label.*
│    » Group labels: Show group labels [cb] dial.title.show; FONT6 dial.title.*
└─ Tab "Icons"
     » Size, offset and crop: Icon size (0 = automatic) | Icon offset (0 = automatic); Zoom
     » Color / Border / Icon glow (with its offsets) / style knobs   (as Comms Pads > Icons, dial.icon.*)

Share page, Profiles page                        (unchanged)
```

The new counts are 25 tabs: General 3 (the new Keybindings tab), Groups 4, Comms Pads 8, Comms Dials 8 and
Share 2. With L33 rejected, Dials has 9 and the Dial Preview tab becomes *Ring map* (L08). Eight short labels
should fit one row at default UI scale, and nine might; both need in-client confirmation. These one-row
headings go: Slices > Gap, Background and Highlight, the Icons tab's Offset, and the lonely Paging line.
These stay: Header > Size and Section titles > Size (L11 rejected), Paging > Page row, and the host-drawn
Position headings (U2).

## Cross-addon notes

- **Position block.** QuickComms draws X offset \| Y offset plus *Reset this <thing>'s position* under a
  Position heading on the instance's Layout tab. The collection should agree on that shape, and on the tab
  name **Layout**, for every per-instance positionable frame (MultiMeters windows, KickCD, AuraMaster
  bars).
- **Styled-tab block order.** Recommend one collection order for every styled element: Size, Font,
  Background, Border, then any effects (Glow, Shine). Background swatches should be labeled **Background
  color** under a **Background** heading everywhere. QuickComms has two orders today (QUI-P13).
- **Glow naming.** QuickComms, DropWatcher (the knob table QuickComms copied) and AuraMaster all carry glow
  blocks. Name the heading after what glows (**Icon glow**, **Button glow**, **Bar glow**) and the knob
  heading after the style, as QuickComms already does.
- **"(0 = automatic)" plus `zeroText = "Automatic"`.** QuickComms uses it on 7 sliders (`SchemaMembers.lua:422,
  503, 611, 711, 764`, `SchemaIcons.lua:56, 117`). It is a good pattern to make the collection convention
  for any slider whose 0 means "computed".
- **Per-instance Visibility on the instance's General tab.** QuickComms puts a pad's Visibility, Fade and
  Faded alpha under a Visibility heading on Pad > General. Other addons with per-instance windows should
  do the same, so per-instance visibility is never on a look tab.
- **Delete wording.** Use "Delete <thing>" on every instance editor (QuickComms has *Delete* against *Delete
  pad* and *Delete dial*). Use "New <thing>" in the band, and "Add <thing>" for list membership, with no
  article.
- **Lock acts on instance pages.** When an instance page offers the master lock, its label should say
  "all" (QUI-L15). Check MultiMeters and DpsRace for the same shape.
- **Listing tabs named "Preview".** Reserve "Preview" for drawn previews (preview-mode). A tab that lists
  text should be named after what it lists.
- **Keybindings tab.** QuickComms is the one addon whose bindings are numbered by **place** (Open Comms
  Dial 1-4). The shared Keybindings tab should allow a dynamic label suffix (the dial's name), and the
  other six addons need none. The Blizzard Keybindings category header today is `header="QUICKCOMMS"`
  with `category="ADDONS"` (`Bindings.xml:6`), which item 015 replaces with the addon-named category.

- **One noun per part.** Name a part the same everywhere in one addon (QuickComms: *slice*, not *wedge*,
  QUI-L35), and name a scoped setting after its scope where a master or sibling setting exists (*Pad
  scale* beside *Master scale*, *Button spacing* beside *Dot spacing*, QUI-L36).
- **Show toggles name their subject.** *Show slice labels* and *Show group labels*, never a bare *Show
  labels* beside a qualified sibling (QUI-L19).
- **Confirm pair order.** QuickComms' callout popup draws *Save* \| *Cancel*, the affirmative on the left as
  Blizzard's StaticPopup does. Check the other addons' modal button pairs for the same order.
- **One-row bands.** QuickComms' Groups band is the only two-row band found here (QUI-P37). Check the
  other per-instance editors (MultiMeters, AuraMaster, KickCD) against options-ui-§14's ONE ROW.
- **Keybindings tab order and labels.** The in-panel tab and Blizzard's Keybindings list should use one
  order (Bindings.xml's) and one label per binding, so "synced" also reads as identical (QUI-L32).

## Upstream suggestions

- **U1 (options-ui-§17, anti-pattern #74).** The ban on `disabledIf` for a color row was written for the
  class-color companion, where the swatch is still read for its alpha. It also catches the case where the
  **whole feature** is off (Show labels off, Show pointer off, a None shine). There the swatch is truly not
  read, and graying it out is accurate. Suggest amending §17: forbid gating a swatch on its own companion,
  but allow gating it on its feature's on/off row. Until then, QUI-L30 complies.
- **U2 (options-ui-§7, host controls).** A structured row (a position, a key) has no flow-engine widget, so
  it cannot declare its `subgroup`, and the host has to draw the heading (`h.Section`), which §7 forbids in
  letter. Suggest a library **Position block composer** (X \| Y edit boxes, plus a Reset button, driven by
  one `point` row and drawing its heading from that row's `subgroup`). QuickComms (2 pages) and every
  per-instance window addon would consume it.
- **U3 (options-ui-§13, strip length).** "A page SHOULD hold its section count low enough for one row" has
  no number. Suggest a concrete SHOULD: at most 8 tabs, or 9 short labels, at default UI scale. Past that,
  merge tabs or adopt the nav rail.
- **U4 (options-ui-§7, lonely headings).** Suggest a SHOULD: a subsection holding a single row merges into
  a neighbor, unless the heading's name is the only thing that explains the row.
- **U5 (options-ui-§16, block order).** §16 fixes the rows **inside** each block. Suggest fixing the order
  **of** the blocks on a styled tab: Size, Font, Background, Border, then effects.
- **U6 (options-ui-§14, a page-wide setting in the band).** §14's General-tab escape names *acts* (rename,
  copy-from, enable, unlock, reset, delete). It does not say whether a page-wide **setting**, such as
  QuickComms' *Preview while editing*, may take the same escape when it does not fit beside the picker on
  one row. Suggest stating it either way. Until then, QUI-L34 keeps it in the band, on one row.

## Review

Independent review against `../QuickComms` at `master` (`bdce9d4`), 2026-10-24. Every map row and cited
line touched below was re-read from the source. The counts (about 233 keys) were not recounted.

- **Map corrections.** The callout popup's buttons are *Save* \| *Cancel*, not *Cancel* \| *Save*
  (`CalloutPopup.lua:393-397`), and its Preview heading is host-drawn. The Groups band is 72 px and two
  rows (`Groups.lua:599, 648-653`). The empty-list hint "Add one below." is now noted. Slice labels'
  first line has no heading. The tab order claim (each group's first schema row, with host tabs keyed by
  group taking that slot) was confirmed in `OptionsTabs.lua:1186`.
- **Problems.** P37 was wrong: options-ui-§14 says "The band is ONE ROW", so the two-row Groups band is a
  deviation and not a sanctioned shape. Added P38 (slice against wedge), P39 (Show labels asymmetry), P40
  (unqualified Scale and Spacing), P41 (the hint tied to the control's position), P42 (Dial Preview apart
  from Groups), P43 (the in-dial keys are undocumented) and P44 (Bindings.xml order against the proposed
  tab order). P36 now cites the Share headings and the binding names.
- **Standard violations in the draft, rewritten.** L05 used a host-drawn heading, which options-ui-§7
  forbids. It is now a spacer and a hint. L19's four headings came close to a faked second tab level
  (options-ui-§7) and went past one heading per group (options-ui-§16). It is now two. L30 grayed a
  companion beside a live swatch, which splits a pair. It now un-gates the whole pair, as the Icons tab
  already does.
- **Implementation traps added.** L17: a row that changes only its `group` moves the Buttons tab ahead of
  the Header tabs, so the row has to move physically into `buttonRows()`. L20 and L21: the Wheel tab draws
  its rows before its host Position block, so rows meant to sit after Position, or inside it, need the
  host render changed.
- **Changes revised.** L14 now folds the glow offsets into the Icon glow heading instead of renaming theirs.
  L21 puts Open at under Position, where its tooltip already points ("set below"), instead of pairing it
  with Slice gap. L26 keeps the existing "indicator" term in its headings. L31 uses *Comms Pads* and
  *Comms Dials*. L32 follows Bindings.xml's order and uses the same labels as Blizzard's list.
- **New changes.** L33 folds the Dial ring listing into Groups, giving 8 Dial tabs. L34 brings the Groups
  band to one row. L35 settles on slice. L36 qualifies Scale and Spacing. L37 adds an in-dial keys hint.
- **No setting changes found.** No change alters a key, a default, a range or a stored value. L16 and L30
  touch only `disabledIf`, which is presentation, and no change adds or removes a row.
- **Recalibrated.** L04 65 → 60, L05 60 → 55, L09 60 → 55, L14 80 → 60, L20 60 → 45, L21 65 → 60, L24 65 → 60,
  L30 55 → 50 and L32 70 → 60. L11 50 → 35 moved to the new "Considered and rejected" section. The
  increase in tab switching it causes, height tuned against font on another tab, was not weighed in the
  draft. Four other options are recorded there with their reasons.

