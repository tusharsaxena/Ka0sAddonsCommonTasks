# PanelMaster — settings layout analysis

Item 020. Analysed read-only at `../PanelMaster` (branch `master` at `e0a9ee3`, v1.3.0), using the
vendored LibKa0s `OptionsCompose.lua` for the composed rows. Every proposal below changes **only**
placement, order, grouping, headings, labels or tooltips. No setting key, default, range or behaviour
changes.

**Keybindings (item 015) do not reach this addon.** PanelMaster has no primary window. Its product is
the panels, and the launcher passes no `isWindowShown` / `toggleWindow`, so its menu has no *Show window*
entry (`core/LauncherSetup.lua:28-29`, `:236`). It also ships no `Bindings.xml` and no `BINDING_*`
globals. So it gets no `Keybindings` tab, and its General page stays at three tabs while the seven
windowed addons go to four. That is consistent: the new tab belongs to the addons that have a window to
toggle. It is listed under *Cross-addon notes* so the plan records the omission as a decision and not as
an oversight.

## Current map

Four canvas pages. They are registered through `O.RegisterOptionsPage` in `settings/Panel.lua:341-514`.
Widget types: **cb** checkbox, **dd** dropdown, **sl** slider, **eb** edit box, **cp** colour swatch
plus its *Use class color* companion checkbox (two widgets, one control), **btn** button. On the Panels
page the "key" is the **panel-record field** written through `NS.Registry:Set`. Those fields are not
profile schema rows; their `panel.<field>` rows are hidden (`settings/PanelSchema.lua:171-191`).

```
1. Ka0s Panel Master (landing)            OptionsSetup.lua:256 -> Panel.lua:275-292 (O.BuildLandingPage)
   ├─ logo (300px), tagline
   └─ [heading] Slash Commands -> one Label per Sl:LandingRows() row

2. General                                Panel.lua:352-416, O.RenderTabbedSchema at :413
   │                                      header Defaults button = Reset this profile (Panel.lua:357-358)
   ├─ Tab "Master controls"               composed: Schema.lua:571-735 (lib OptionsCompose.lua:458-579)
   │   ├─ row: Enable Ka0s Panel Master (cb, settings.enabled)  | General visibility (dd, settings.visibility)
   │   ├─ row: Master scale (sl, settings.scale)                 | Master alpha (sl %, settings.alpha)
   │   ├─ row: Lock frame (cb, state.locked, session)            | Debug console (cb, state.debugConsole, session)
   │   ├─ row: Minimap button (cb, global.minimap.shown)         | —   (no testModePath, Schema.lua:608-610)
   │   └─ afterGroup: [Reset position] (btn) | [Reset all settings] (btn)
   ├─ Tab "Editing"                       Schema.lua:52-96, afterGroup Panel.lua:396-408
   │   ├─ row: Show names while unlocked (cb, settings.showLabels) | Snap to grid (cb, settings.snapToGrid)
   │   ├─ row: Grid size (sl px, settings.gridSize)                | Unlock outline thickness (sl px, settings.unlockOutlineSize)
   │   └─ afterGroup: [Recover panels] (btn, alone)
   └─ Tab "New panels"                    Schema.lua:108-132
       ├─ row: Default width (sl, settings.defaultWidth)           | Default height (sl, settings.defaultHeight)
       └─ row: Default frame strata (dd, settings.defaultStrata)   | Default opacity (sl 0-1, settings.defaultAlpha)

3. Panels                                 Panel.lua:421-459; body PanelEditor.lua + PanelEditorTabs.lua
   │                                      header Defaults button = Delete every panel (Panel.lua:425, :434-441)
   ├─ Band (one row, PageHeader)          PanelEditor.lua:498-613
   │   └─ row: Panel (dd picker, selection — not stored) | Create new panel (eb, act)
   ├─ Strip (H.TabStrip)                  PanelEditor.lua:463-479; tab list PanelEditorTabs.lua:64-75
   ├─ (empty state Label when no panels)  PanelEditor.lua:685-690
   ├─ Tab "General"                       PanelEditorTabs.lua:296-399
   │   ├─ row: Panel name (eb, name — rename act)      | Copy settings from panel (dd, act)
   │   ├─ row: Enabled (cb, enabled)                    | Unlock (cb, session per-panel unlock)
   │   └─ row: [Reset] (btn)                            | [Delete] (btn)
   ├─ Tab "Position and size"             PanelEditorTabs.lua:402-444 (no subsection headings)
   │   ├─ row: Width (sl, width)                        | Height (sl, height)
   │   ├─ row: X offset (sl, x)                         | Y offset (sl, y)
   │   ├─ row: Anchor (dd, point)                       | Frame strata (dd, strata)
   │   ├─ row: Frame level (sl, level)                  | —
   │   └─ row: Panel scale (sl full width, scale)
   ├─ Tab "Background and border"         PanelEditorTabs.lua:452-487
   │   ├─ [heading] Background
   │   │   ├─ row: Background texture (LSM dd, bgTexture)  | —
   │   │   └─ row: Background color (cp, bgColor)          | Use class color (cb, bgClassColor)
   │   └─ [heading] Border                 composed O.BorderGroup, :476-486
   │       ├─ row: Border style (LSM dd, borderTexture)    | Border thickness (px) (sl, borderSize)
   │       ├─ row: Border color (cp, borderColor)          | Use class color (cb, borderClassColor)
   │       └─ row: Border offset (sl, borderOffset)        | —
   ├─ Tab "Accent bar"                    PanelEditorTabs.lua:498-565
   │   ├─ [heading] Bar
   │   │   ├─ row: Enable accent bar (cb, accentEnabled)   | —
   │   │   ├─ row: Bar texture (LSM dd, accentTexture)     | Bar opacity (sl 0-1, accentAlpha)      (composed O.BarGroup :514-539)
   │   │   ├─ row: Bar color (cp, accentColor)             | Use class color (cb, accentClassColor)
   │   │   └─ row: Bar thickness (sl, accentThickness)     | Bar offset (sl, accentOffset)
   │   ├─ [heading] Edges
   │   │   └─ row: Top | Bottom | Left | Right (4 x cb quarter width, accentEdges)
   │   └─ [heading] Border                 composed O.BorderGroup :554-564
   │       ├─ row: Border style (LSM dd, accentBorderTexture)  | Border thickness (px) (sl, accentBorderSize)
   │       ├─ row: Border color (cp, accentBorderColor)        | Use class color (cb, accentBorderClassColor)
   │       └─ row: Border offset (sl, accentBorderOffset)      | —
   ├─ Tab "Artwork"                       PanelEditorTabs.lua:569-748
   │   ├─ [heading] Image
   │   │   ├─ row: Artwork (dd full width, artTexture)
   │   │   └─ row: Custom texture path (eb, artCustomPath)     | [Fit to artwork] (btn, act)
   │   ├─ [heading] Layout
   │   │   ├─ row: Fill (dd, artFill)                          | Artwork position (dd, artPoint)
   │   │   ├─ row: Artwork scale (sl, artScale)                | Rotation (dd, artRotation)
   │   │   ├─ row: Flip horizontal (cb, artFlipH)              | Flip vertical (cb, artFlipV)
   │   │   └─ row: Artwork X offset (sl, artX)                 | Artwork Y offset (sl, artY)
   │   └─ [heading] Appearance
   │       ├─ row: Artwork opacity (sl, artAlpha)              | Draw layer (dd, artLayer)
   │       ├─ row: Artwork color (cp, artColor)                | Use class color (cb, artClassColor)
   │       └─ row: Desaturate (cb, artDesaturate)              | Blend mode (dd, artBlend)
   └─ Tab "Opacity and fade"              PanelEditorTabs.lua:751-784
       ├─ row: Panel opacity (sl, alpha)                       | Faded opacity (sl, mouseoverAlpha)
       └─ row: Show on mouseover only (cb, mouseover)          | —

4. Profiles                               Panel.lua:472-509 — AceDBOptions via AceConfigDialog (exempt, options-ui-§13)
```

**Counts.** 4 pages, 2 of them tabbed. 3 + 6 = **9 tabs**. General page: **15 schema rows** (7 + 4 + 4)
and 3 buttons. Panels page: 2 band controls, then 6 / 8 / 6 / 11 / 16 / 3 = **50 editor controls**
(a cp counts as one control and the four Edges as one), with 3 of them buttons. The six editor tabs are
laid out in **3 + 5 + 5 + 8 + 9 + 2 = 32 control lines**, plus 2 + 3 + 3 = 8 subsection headings on the
three appearance tabs.

## Problems

| id | where | problem |
|---|---|---|
| PAN-P01 | `settings/Schema.lua:52-96`; contradicted by its own comments at `:65-66` and `settings/Panel.lua:385-386` | **Snap to grid is not on the line with Grid size.** The rows are declared in the order showLabels, snapToGrid, gridSize, unlockOutlineSize, and the flow engine pairs consecutive rows (options-ui-§6; none of the four carries `startsLine`/`solo`). So the lines come out as *[Show names][Snap to grid]* and *[Grid size][Unlock outline thickness]*. The switch and the slider it governs are on different lines, and each one is paired with an unrelated control. The block comment at `Schema.lua:42-43` describes the rendered pairing correctly; the row comment at `:65-66` and `Panel.lua:385-386` claim the opposite. Intent and render have drifted apart. |
| PAN-P02 | `Schema.lua:52`, `:87` | The two unlock-overlay *appearance* rows (Show names while unlocked, Unlock outline thickness) are on different lines, and each is paired with a grid control. |
| PAN-P03 | `Schema.lua:53` (`group = "Editing"`) | The tab name "Editing" is vague. Every row on the tab only matters while panels are **unlocked and being dragged**, but "Editing" also describes the whole Panels page, where the player edits a panel. The two meanings collide. |
| PAN-P04 | `Panel.lua:396-408` vs lib `OptionsCompose.lua:553-557` | **The recovery acts are split across two tabs.** *Recover panels* (Editing) and *Reset position* (Master controls) answer the same question, "where did my panel go?", and a player has to know which tab holds which. They also differ in a way only the tooltips say: *Recover* moves only off-screen panels, *Reset position* moves **every** panel to the middle of the screen and is **not** confirm-gated (`Schema.lua:611-614`). |
| PAN-P05 | `Schema.lua:669` vs `PanelEditorTabs.lua:367` | The editing-mode switch (*Lock frame*, Master controls tab) is on a different tab from the four settings it enables (Editing tab). This is a fixed element (options-ui-§15: the set *MUST NOT* be split across tabs), so it is only mitigated here, by cross-referencing in tooltips. |
| PAN-P06 | `PanelEditorTabs.lua:368` | The per-panel checkbox is labelled just "Unlock". It sits beside "Enabled" and reads as a property of the panel. The global control is "Lock frame", with the opposite sense, so the pair is easy to misread. |
| PAN-P07 | `PanelEditorTabs.lua:351` | "Enabled" is a bare adjective. Elsewhere the collection uses verb phrases for switches ("Enable Ka0s Panel Master", "Enable accent bar"). |
| PAN-P08 | `PanelEditorTabs.lua:344-345`; `modules/Registry.lua:569-572,586-589` | **The Copy-from tooltip under-describes the act.** `Registry.CopyFrom` copies **every** declared field except `id`, `name`, `frameName` and the position (`point`, `relPoint`, `x`, `y`). That includes `enabled`, `strata`, `level`, `scale`, `alpha`, `mouseover`, `mouseoverAlpha` and the whole artwork block. The tooltip lists only "size, textures, colors, border and accent bar", so a player copying a look is surprised when the panel also changes layer, scale, fade or enabled state. The label "Copy settings from panel" is **accurate**; the tooltip is not. |
| PAN-P09 | `PanelEditorTabs.lua:402-444` | The "Position and size" tab holds **three subjects**: size (W/H/scale), position (anchor/X/Y) and **layer** (strata/level). It has no subsection headings, which options-ui-§7/§13 require of a tab that mixes subjects. It is also the only multi-subject editor tab without headings, and its name hides the layer controls. |
| PAN-P10 | `PanelEditorTabs.lua:409-415` | **Anchor sits below the X/Y offsets it is the origin of.** Its tooltip says "which corner or edge of the screen the offsets are measured from". The mental model is to choose the origin and then nudge from it. |
| PAN-P11 | `PanelEditorTabs.lua:416` + `:423-427` | Frame strata and Frame level are one subject, split across two lines: strata shares a line with Anchor, and level sits **alone** on a half-empty line. The comment at `:421` wants them to "read together", but they are not on one line. |
| PAN-P12 | `PanelEditorTabs.lua:434-443` | Panel scale is a full-width footer, three lines below Width/Height. Its tooltip spends most of its length explaining how it differs from Width/Height, which says it belongs next to them. |
| PAN-P13 | `PanelEditorTabs.lua:659-705` | **Artwork position is three lines above the X/Y offsets it anchors.** Its tooltip says "what the offsets below are measured from", and Scale and the Flips sit between them. Same defect as PAN-P10, on a second tab. |
| PAN-P14 | `PanelEditorTabs.lua:659`, `:676` | Fill and Artwork scale are each other's subject (the tooltips cross-reference: "Stretch ignores Scale", "Under Fill and Tile ...") but sit on different lines. |
| PAN-P15 | `PanelEditorTabs.lua:681-692` | Rotation and the two Flips interact ("Applied BEFORE the rotation") but are on different lines, with Rotation paired with Scale. |
| PAN-P16 | `PanelEditorTabs.lua:708` | The subsection heading "Appearance" is vague: on a tab that is entirely about appearance it names nothing. Its rows are opacity, colour, tint, blend and **draw layer**. Draw layer is a stacking choice, not a look. |
| PAN-P17 | `PanelEditorTabs.lua:499-545` | **Edges is separated from Enable accent bar by the whole four-line bar block.** "Is there a bar, and on which edges" is the first decision. Texture, colour and thickness come after it. As laid out, a player enables the bar, scrolls past its styling to choose edges, and then scrolls on to the bar's border. |
| PAN-P18 | `PanelEditorTabs.lua:501-503` | Enable accent bar sits alone on a half-empty line. Every control below it depends on it, but nothing shows that dependency (the dependent controls stay enabled while it is off). |
| PAN-P19 | `PanelEditorTabs.lua:767-778` | On Opacity and fade, the parent switch (Show on mouseover only) is **below** the slider it gates (Faded opacity), and it sits alone on its line. The arrangement is deliberate, argued at `:752-761` from an earlier layout that read worse. A nitpick only. |
| PAN-P20 | `PanelEditorTabs.lua:751`, tab list `:69` | "Opacity and fade" has only 3 controls, the smallest tab, and Panel opacity is closely tied to the other tabs' opacities. The tab is defensible: merging it would overload Position or General (see *Considered and rejected*). Recorded so the call is visible. |
| PAN-P21 | `Schema.lua:98-132`; `PanelEditor.lua:550-561` | **Defaults for new panels live on a different page from the create box.** To make a panel at a chosen size, the player changes General ▸ New panels, switches to Panels and types a name. Nothing on the Panels page mentions the defaults, and the editor's *Reset* tooltip ("back to how a new one starts") does not say where "how a new one starts" is set. |
| PAN-P22 | `Schema.lua:124-125` vs `PanelEditorTabs.lua:417-418` | The two strata tooltips say the same thing in two wordings ("DIALOG and above cover normal UI" and "... will cover normal UI"). Neither warns that DIALOG and higher also covers **this addon's own confirm popups, the debug console and the Settings window** (see the strata analysis, PAN-S05). |
| PAN-P23 | `Schema.lua:130`, `:129` (`fmt %.2f`); lib `OptionsCompose.lua:486` (`isPercent`); `PanelEditorTabs.lua:533` (`accentAlpha isPercent = false`) | **Opacity terminology and units are inconsistent.** The tab says "Master **alpha**", shown as a percentage. Default opacity, Panel opacity, Faded opacity, Bar opacity and Artwork opacity all say "**opacity**", shown as 0–1 ratios (the addon even overrides the composed Bar opacity to 0–1 to match). One concept has two names and two scales on adjacent pages. "Master alpha" is fixed by options-ui-§15; see *Upstream suggestions*. |
| PAN-P24 | lib `OptionsCompose.lua:490` | "Lock frame" is singular for an addon with many panels. Fixed (options-ui-§15 *MUST NOT* rename); mitigated by its tooltip at `Schema.lua:671`. |
| PAN-P25 | `Panel.lua:425`, `:434-441` | The **Panels page's header "Defaults" button deletes every panel.** Under the same label, the General page's button resets the profile. The same word means two different destructive acts on adjacent pages, and only the tooltips tell them apart. Fixed by options-ui-§13 (the per-page Defaults button stays page-wide); see *Upstream suggestions*. |
| PAN-P26 | `PanelEditorTabs.lua:455-457` | Background texture sits alone on a half-empty line. Unavoidable: the colour pair beside it emits two widgets. Recorded, not changed. |
| PAN-P27 | `PanelEditorTabs.lua:480`, `:558` | Border offset sits alone on a half-empty line, twice. Fixed: options-ui-§16 puts the host extra *after* the canonical four. |
| PAN-P28 | `docs/settings-panel.md:161` page-tabs table | Doc drift: it gives the Position and size tab **7** controls, but the code builds **8** (Frame level was added without updating the count). |
| PAN-P29 | `Panel.lua:382-388`, `Schema.lua:65-72` | Stale comments say "*Snap to grid* now sits beside *Grid size*". That is false (PAN-P01), and it will mislead the next editor. |
| PAN-P30 | `PanelEditorTabs.lua:350-386` | The scalar **state** checkboxes (Enabled, Unlock) sit between the identity row and the destructive row. Identity, then state, then acts is a reasonable order, so this is only noted for completeness. |
| PAN-P31 | `PanelEditorTabs.lua:635-653` | *Fit to artwork* is an act that **resizes the panel** (a Position-and-size outcome) but lives on Artwork. It is correct where it is, because it is driven by the art, but its tooltip says "Resizes this panel" without naming the Width/Height it overwrites. |
| PAN-P32 | `PanelEditorTabs.lua:768-771` | **The Panel opacity tooltip is wrong about its reach.** It says "background and border together", but it is the frame's `SetAlpha` (`modules/Canvas.lua:606`), so it also fades the accent bars and the artwork, which those tabs' own opacity tooltips say ("a faded panel fades its bars/art with it"). The three tooltips disagree. |
| PAN-P33 | `Schema.lua:77`, `:91` ("UI units"); `PanelEditorTabs.lua:522` ("screen units"); `docs/settings-panel.md:49` ("screen units"); composed labels "Border thickness (px)"; `fmt "%d px"` | **One unit, three names.** Grid size and outline thickness say "UI units", Bar thickness says "screen units", the composed border rows and the slash output say "px". All four are the same unit (UI-scaled pixels). |
| PAN-P34 | lib `OptionsCompose.lua:553-557` | The composed *Reset position* tooltip is "Move the frame back to where it started." For this addon it moves **every panel** to the middle of the screen, without a confirm. The tooltip is the library's and the host cannot override it (no spec field). Fixed element; see *Upstream suggestions*. |
| PAN-P35 | `README.md:52,54,80`; `docs/settings-panel.md:30-31,47-51,160-161,324` | Tab names ("General → Editing", "Position and size") are quoted in the README and the settings doc, so every rename below ripples into user-facing docs as well as the code. |
| PAN-P36 | `Schema.lua:122` vs `PanelEditorTabs.lua:416` vs the collection | "Default frame strata" / "Frame strata" match MultiMeters and PartyFrameEnhanced, but AuraMaster labels the same control "Strata" (`AuraMaster/settings/Layout.lua:365`). Cross-addon, recorded below. |

## Proposed changes

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| PAN-L01 | General ▸ Editing: reorder the rows to **showLabels, unlockOutlineSize, snapToGrid, gridSize** (`Schema.lua:52-96`), so the lines are *[Show names while unlocked][Unlock outline thickness]* and *[Snap to grid][Grid size]*. | Puts each switch on the line with the slider it governs, and the two overlay-look controls on one line. A pure reorder: options-ui-§6 says re-columning *is* a row-order edit. `/pm list` order follows, which is harmless. | 95% | P01, P02 |
| PAN-L02 | Rename the tab "Editing" → **"Moving panels"** (`group` string on the four rows, `Schema.lua:53,62,76,90`, plus the afterGroup key `Panel.lua:396`, which L03 deletes anyway). `/pm list` groups by the same string (`Slash.lua:694-695`), so its heading follows. | Names what the tab is about: dragging unlocked panels. It stops colliding with the Panels page's editor. `group` is not a stored key and there is no `/pm reset <group>` form (`tests/test_libka0s.lua:345-349` pins its absence), so nothing migrates and no command breaks. Test pins at `tests/test_libka0s.lua:547-560` and `tests/test_schema.lua:279` need the new name. | 70% | P03 |
| PAN-L03 | Move **[Recover panels]** from the Editing tab's afterGroup to the Master controls tab, through the composer's `leadButton` slot (`Schema.lua:575` `MasterControls{ leadButton = {...} }`). The composer draws it on **its own row, left cell, right cell empty** (`OptionsCompose.lua:569`), **above** *Reset position \| Reset all settings*. Delete the Editing afterGroup (`Panel.lua:396-408`). Add to its tooltip: "Unlike **Reset position** below, panels that are on screen stay where they are." | Both "get my panels back" acts end up in one place, the tab a lost player opens first, and the difference between them is stated where they sit side by side. leadButton is the slot options-ui-§15 names for "a one-shot act". The half-empty button row is **moved, not removed**: the composer never pairs a lead with Reset position on a framed addon. Risk: the confirm-free *Reset position* is now one row under a button a lost player clicks; the tooltip line is the mitigation. | 60% | P04 |
| PAN-L04 | Tooltip, Editing/Moving panels rows (`Schema.lua:54,63,77,91`): append "These only matter while panels are unlocked: untick **Lock frame** on Master controls, or tick **Unlock this panel** on Panels ▸ General." | Fixed element (options-ui-§15). This bridges the split between the switch and its settings without moving the switch. "Panels ▸ General" rather than "a panel's General tab", which would be read as the General *page*. | 80% | P05 |
| PAN-L05 | Panels ▸ General: relabel "Unlock" → **"Unlock this panel"** (`PanelEditorTabs.lua:368`, tooltip title `:382`). | Says it is per-panel and is an act on this panel, which stops it being read alongside the inverted global "Lock frame". | 80% | P06 |
| PAN-L06 | Panels ▸ General: relabel "Enabled" → **"Enable this panel"** (`PanelEditorTabs.lua:351`, tooltip title `:358`). | Matches the verb-phrase form of "Enable Ka0s Panel Master" and "Enable accent bar", and pairs with "Unlock this panel" on the same line. | 60% | P07 |
| PAN-L07 | Panels ▸ General: **keep** the label "Copy settings from panel" and rewrite its tooltip (`PanelEditorTabs.lua:344-345`): "Copy everything from another panel **except its name and its position** (anchor and offsets): size and scale, layer, opacity and fade, background, border, accent bar, artwork, and whether it is enabled. This panel stays where it is." | The original proposal (relabel to "Copy appearance from") would have made the label *narrower* than the act, which also copies `enabled`, `strata`, `level`, `scale` and the fade (`Registry.lua:569-572`). The label is right; the tooltip is what misleads. | 85% | P08 |
| PAN-L08 | Panels ▸ "Position and size": add three subsection headings (`editorHeading`): **Size**, **Position**, **Layer**. Optionally rename the tab to **"Position, size and layer"** (`PanelEditorTabs.lua:65`). | Complies with options-ui-§7/§13 for a multi-subject tab and names the layer controls it holds. The longer name makes a six-tab strip more likely to wrap; options-ui-§13 permits a wrap but says a page SHOULD fit one row. Headings alone already expose "Layer". | 85% (headings) / 50% (rename) | P09 |
| PAN-L09 | Under **Size**: [Width][Height], then **Panel scale** (full width, unchanged) directly below them (`PanelEditorTabs.lua:404-405`, `:435`). | Scale sits beside the controls its tooltip contrasts it with, and still directly above the Position block its "nudge the offsets afterwards" advice points to. | 75% | P12 |
| PAN-L10 | Under **Position**: [Anchor][—], then [X offset][Y offset] (Anchor moved from `:414` above the offsets at `:409-410`). | Origin first, then the nudge. The lone Anchor on a half-empty line is the price of putting it first, and it is a smaller cost than having to read upward. | 70% | P10 |
| PAN-L11 | Under **Layer**: [Frame strata][Frame level] on **one** line (`:416` + `:424`). Fix the comment at `:421`. | One subject on one line. Removes the lone Frame level line, and the comment gets what it asked for. | 90% | P11 |
| PAN-L12 | Artwork ▸ Layout: reorder to [Fill][Artwork scale] / [Artwork position][—] / [Artwork X offset][Artwork Y offset] (`:659-705`). | Sizing pair together. Position sits directly above the offsets it anchors ("offsets below" in its tooltip becomes literally true). | 75% | P13, P14 |
| PAN-L13 | Artwork: add a heading **"Orientation"** after Layout: [Rotation][—] / [Flip horizontal][Flip vertical] (`:681-692`). | Rotation and the flips interact (flip before rotate) and form one subject. Costs a half-empty line, the same trade as PAN-L10. | 55% | P15 |
| PAN-L14 | Artwork: rename heading "Appearance" → **"Color and blending"** (`:708`) and move **Draw layer** from it into **Layout**, in the empty right cell beside Artwork position (L12). Color and blending then reads [Artwork opacity][Blend mode] / [Artwork color][Use class color] / [Desaturate][—]. | Draw layer is a stacking choice and belongs with placement; it also fills L12's empty cell. The heading names its contents. Desaturate stays next to the colour it pre-conditions (its tooltip). | 60% | P16 |
| PAN-L15 | Accent bar: reorder to four headings: **Bar** ([Enable accent bar][—]), **Edges** (the four edge checks, heading kept: without it "Top / Bottom / Left / Right" have no caption, and a hand-rolled caption is anti-pattern #71), **Bar style** (the composed O.BarGroup block, unchanged inside), **Bar border** (the composed O.BorderGroup, renamed from "Border" so it cannot be read as the panel's border on the previous tab). | "Is there a bar, and where" comes before "what does it look like". Turning it on and choosing edges becomes one stop at the top of the tab. The composed blocks keep their internal order (options-ui-§16). | 60% | P17, P18 |
| PAN-L16 | Accent bar: tooltip for Enable accent bar (`:503`) gains "Everything below on this tab applies only while this is ticked." | Shows the dependency, because the half-empty cell beside the checkbox cannot. | 75% | P18 |
| PAN-L18 | Panels band: tooltip for *Create new panel* (`PanelEditor.lua:559-560`) gains "New panels start at the size, layer and opacity set on **General ▸ New panels**." The editor's *Reset* tooltip (`PanelEditorTabs.lua:391-393`) gains the same pointer. | Bridges the page split without moving schema rows onto a bespoke per-instance page, where they would read as editing the *selected* panel (options-ui-§14 retargeting). | 85% | P21 |
| PAN-L19 | General ▸ New panels: tooltip for each default (`Schema.lua:112,119,124,131`) gains "Panels are made on the **Panels** page." | The other half of L18. | 65% | P21 |
| PAN-L20 | Unify the two strata tooltips (`Schema.lua:124-125`, `PanelEditorTabs.lua:417-418`) into one string stated once (a `C.STRATA_TIP` constant), worded as the tiers in strata PAN-Z06: "BACKGROUND / LOW: under the HUD (recommended for backdrops). MEDIUM: level with most of the HUD. HIGH: over the HUD. DIALOG and above: over windows, **including this addon's own confirmation popups and the Settings window**." | One wording, and it states the real cost of a high strata. Owned here; strata Z06 is the same change and must not be implemented twice. | 80% | P22 |
| PAN-L21 | *Fit to artwork* tooltip (`:647`): open with "Overwrites this panel's **Width and Height** (Position and size tab) with ...". | Says where the effect lands. | 65% | P31 |
| PAN-L22 | Fix the stale comments (`Schema.lua:65-72`, `Panel.lua:382-388`, `PanelEditorTabs.lua:421`) and the docs (`docs/settings-panel.md`: Position tab count 7 → 8; `README.md:52,54,80` and `docs/settings-panel.md` tab/heading names after L02/L08/L13-L15). | The documentation should describe the code as it is (P28, P29, P35). | 95% | P28, P29, P35 |
| PAN-L23 | Panel opacity tooltip (`PanelEditorTabs.lua:768-771`): "How visible the whole panel is: background, border, accent bars and artwork together. ..." (rest unchanged). | Matches what `SetAlpha` on the frame does and what the Bar opacity and Artwork opacity tooltips already say. | 85% | P32 |
| PAN-L24 | Unit wording: tooltips say **"UI units"** everywhere. Bar thickness (`PanelEditorTabs.lua:522`) "screen units" → "UI units"; `docs/settings-panel.md:49` likewise. The composed "(px)" labels and the slash `fmt` stay (library / CLI). | One word for one unit across the addon's own text. | 70% | P33 |

**Not changed, with the reason:** P19 and P20 (see *Considered and rejected*), P23/P24/P25/P27/P34 (fixed
elements, see *Upstream suggestions*), P26 (unavoidable: the colour pair is two widgets), P30 (the order
is already sensible), P36 (cross-addon, owned by AuraMaster).

## Proposed map

```
1. Ka0s Panel Master (landing)            unchanged

2. General
   ├─ Tab "Master controls"
   │   ├─ row: Enable Ka0s Panel Master (cb, settings.enabled)   | General visibility (dd, settings.visibility)
   │   ├─ row: Master scale (sl, settings.scale)                  | Master alpha (sl %, settings.alpha)
   │   ├─ row: Lock frame (cb, state.locked)                      | Debug console (cb, state.debugConsole)
   │   ├─ row: Minimap button (cb, global.minimap.shown)          | —
   │   ├─ leadButton: [Recover panels] (btn)                      | —                                 <- L03
   │   └─ afterGroup: [Reset position] | [Reset all settings]
   ├─ Tab "Moving panels"                                                                            <- L02 (tooltips L04)
   │   ├─ row: Show names while unlocked (cb, settings.showLabels) | Unlock outline thickness (sl, settings.unlockOutlineSize)  <- L01
   │   └─ row: Snap to grid (cb, settings.snapToGrid)              | Grid size (sl, settings.gridSize)                         <- L01
   └─ Tab "New panels"                                            (tooltips L19, L20)
       ├─ row: Default width (sl, settings.defaultWidth)          | Default height (sl, settings.defaultHeight)
       └─ row: Default frame strata (dd, settings.defaultStrata)  | Default opacity (sl, settings.defaultAlpha)

3. Panels
   ├─ Band: Panel (dd) | Create new panel (eb)                    (tooltip L18)
   ├─ Tab "General"
   │   ├─ row: Panel name (eb, name)                    | Copy settings from panel (dd, act)          (tooltip L07)
   │   ├─ row: Enable this panel (cb, enabled)          | Unlock this panel (cb, session)             <- L06, L05
   │   └─ row: [Reset] | [Delete]                                                                    (tooltip L18)
   ├─ Tab "Position and size"  (optionally "Position, size and layer")                              <- L08
   │   ├─ [heading] Size
   │   │   ├─ row: Width (sl, width)                    | Height (sl, height)
   │   │   └─ row: Panel scale (sl full width, scale)                                                <- L09
   │   ├─ [heading] Position
   │   │   ├─ row: Anchor (dd, point)                   | —                                           <- L10
   │   │   └─ row: X offset (sl, x)                     | Y offset (sl, y)
   │   └─ [heading] Layer
   │       └─ row: Frame strata (dd, strata)            | Frame level (sl, level)                     <- L11 (tooltip L20)
   ├─ Tab "Background and border"                  unchanged
   │   ├─ [heading] Background: Background texture | — ; Background color | Use class color
   │   └─ [heading] Border: Border style | Border thickness (px) ; Border color | Use class color ; Border offset | —
   ├─ Tab "Accent bar"                                                                               <- L15
   │   ├─ [heading] Bar
   │   │   └─ row: Enable accent bar (cb, accentEnabled) | —                    (tooltip L16)
   │   ├─ [heading] Edges
   │   │   └─ row: Top | Bottom | Left | Right (4 x cb, accentEdges)
   │   ├─ [heading] Bar style
   │   │   ├─ row: Bar texture (accentTexture)          | Bar opacity (accentAlpha)
   │   │   ├─ row: Bar color (accentColor)              | Use class color (accentClassColor)
   │   │   └─ row: Bar thickness (accentThickness)      | Bar offset (accentOffset)   (tooltip L24)
   │   └─ [heading] Bar border
   │       ├─ row: Border style (accentBorderTexture)   | Border thickness (px) (accentBorderSize)
   │       ├─ row: Border color (accentBorderColor)     | Use class color (accentBorderClassColor)
   │       └─ row: Border offset (accentBorderOffset)   | —
   ├─ Tab "Artwork"
   │   ├─ [heading] Image
   │   │   ├─ row: Artwork (dd full, artTexture)
   │   │   └─ row: Custom texture path (eb, artCustomPath) | [Fit to artwork]     (tooltip L21)
   │   ├─ [heading] Layout                                                                           <- L12, L14
   │   │   ├─ row: Fill (dd, artFill)                    | Artwork scale (sl, artScale)
   │   │   ├─ row: Artwork position (dd, artPoint)       | Draw layer (dd, artLayer)
   │   │   └─ row: Artwork X offset (sl, artX)           | Artwork Y offset (sl, artY)
   │   ├─ [heading] Orientation                                                                      <- L13
   │   │   ├─ row: Rotation (dd, artRotation)            | —
   │   │   └─ row: Flip horizontal (cb, artFlipH)        | Flip vertical (cb, artFlipV)
   │   └─ [heading] Color and blending                                                               <- L14
   │       ├─ row: Artwork opacity (sl, artAlpha)        | Blend mode (dd, artBlend)
   │       ├─ row: Artwork color (cp, artColor)          | Use class color (cb, artClassColor)
   │       └─ row: Desaturate (cb, artDesaturate)        | —
   └─ Tab "Opacity and fade"                       order unchanged (L17 rejected)                    (tooltip L23)
       ├─ row: Panel opacity (sl, alpha)                 | Faded opacity (sl, mouseoverAlpha)
       └─ row: Show on mouseover only (cb, mouseover)    | —

4. Profiles                               unchanged
```

**Counts after.** 4 pages and 9 tabs, both unchanged. General: 15 schema rows (7 + 4 + 4) and 3 buttons
(Recover panels has moved to Master controls, still on a row of its own). Panels: still 50 controls. The
editor tabs are laid out in **3 + 5 + 5 + 8 + 10 + 2 = 33 control lines** (Artwork gains one, from the
Orientation split), with headings 3 + 2 + 4 + 4 = 13 (Position gains 3, Accent and Artwork gain 1 each).

## Considered and rejected

| id | idea | why rejected | confidence |
|---|---|---|---|
| PAN-L17 | Opacity and fade: put *Show on mouseover only* first, sliders under it. | The current order was chosen deliberately after the reverse layout read worse in game (`PanelEditorTabs.lua:752-761`: a checkbox beside or above a slider reads as governing *that* slider, but this one governs whether the second number is consulted at all). Two lines; the gain is cosmetic. | 35% |
| PAN-R01 | Merge General ▸ Moving panels and General ▸ New panels into one tab with two `subgroup` headings, to cut a tab click. | Two unrelated subjects (dragging vs creating) of two lines each; a merged tab needs a name that collides with the *Panels* page or says nothing. One click on a page visited rarely is cheap. | 35% |
| PAN-R02 | Fold Opacity and fade into Panels ▸ General (under a "Visibility" heading next to *Enable this panel*), cutting the editor to five tabs. | options-ui-§14 makes the editor's General tab the home of the page-wide **acts**; mixing panel styling into it blurs that. The tab was renamed away from "Visibility" because the word promised a rules engine the addon lacks (`PanelEditorTabs.lua:55-56`). | 30% |
| PAN-R03 | Grey out the Accent bar controls while *Enable accent bar* is off. | That changes widget behaviour (disabled state), not layout; out of scope for item 020. L16's tooltip covers the dependency. | 30% |
| PAN-R04 | Move General ▸ New panels onto the Panels page next to the create box. | Schema rows on a per-instance page would read as editing the *selected* panel (options-ui-§14), and the band is one row by rule. L18/L19 bridge the split instead. | 20% |
| PAN-R05 | Relabel "Copy settings from panel" → "Copy appearance from". | The act copies enabled state, layer, scale and fade as well as the look; the new label would be less accurate than the old one. Replaced by L07's tooltip fix. | 10% |
| PAN-R06 | Subsection headings on Moving panels ("Unlock overlay", "Grid"). | One heading per line on a two-line tab. L01's pairing already separates the subjects. | 25% |

## Cross-addon notes / Upstream suggestions

**Cross-addon notes**

- **Keybindings tab (item 015).** PanelMaster has no window, so it gets no tab. When the seven windowed
  addons add `Keybindings` to General, record PanelMaster in the plan as a deliberate exemption: no
  window, so nothing to bind. This addon must not grow an empty tab just to match the others. (A
  "Toggle panel lock" binding would be a new feature, not item 015's scope; raise separately if wanted.)
- **"Opacity" vs "alpha".** The collection already says "opacity" on every hand-written row (AuraMaster,
  MultiMeters, QuickComms, KickCD and others); the composed *Master alpha* is the only "alpha". Display
  units also split: Master alpha is a percent, every PanelMaster opacity is 0–1. Converge on one noun and
  one display.
- **"Frame strata" vs "Strata".** MultiMeters, PartyFrameEnhanced and PanelMaster say "Frame strata";
  AuraMaster says "Strata" (`settings/Layout.lua:365`). Converge on "Frame strata".
- **Per-instance "Unlock this <thing>"**, beside the global "Lock frame". Any addon with per-instance
  unlocks (windows, bars, pads) should label the instance control the same way.
- **Copy-from acts:** whatever an addon's copy-from skips, its tooltip should name exactly what is and is
  not copied. PanelMaster's did not (P08).
- **Recovery acts on Master controls through `leadButton`.** An addon with a "bring it back on screen"
  verb (recover, re-center) should put it there, so "I lost my frame" has one answer in every addon.
- **Strata tooltip.** Every addon that exposes a strata dropdown should use the same tier sentences.
  This would be a good library string (see upstream).
- **Subsection headings on a Position/size/layer tab.** Check the other per-instance editors for the same
  §7 gap PanelMaster has.
- **Unit word.** "UI units" vs "screen units" vs "px": pick one for tooltips collection-wide.

**Upstream suggestions (WowAddonStandards / LibKa0s)**

- **options-ui-§15: "Master alpha" → "Master opacity"** in the canonical set. Players see "opacity"
  everywhere else, and the canonical row is the odd one out (P23). Library: `OptionsCompose.lua:486`.
- **options-ui-§15: "Lock frame" → "Lock frames", or let an addon pass a plural noun** ("Lock panels"),
  for addons whose frames are per-instance (P24). The rule today *MUST NOT* rename.
- **options-ui-§15 / LibKa0s `MasterControls`: let the host override the *Reset position* tooltip**
  (e.g. `resetPositionTooltip`), because "Move the frame back to where it started" is wrong for an addon
  with many frames that all go to the middle of the screen (P34).
- **options-ui-§13 / §12: per-page Defaults on a structural page.** Let a page whose "defaults" act
  means "delete every instance" either relabel the button or opt out of it, keeping the act as an
  explicit confirm-gated *Delete all* control (P25). The same "Defaults" word now means two different
  destructive acts on adjacent pages.
- **options-ui-§7: say "subjects", not "control types".** As written, a tab that mixes a checkbox and a
  slider needs headings, which would put headings on almost every small tab; the rule's own example is
  about subjects (bar / background / border). Also say that **bespoke editors** (no schema rows, no
  `subgroup`) draw the same `Heading` per subject. P09 slipped through because the rule is phrased in
  schema terms.
- **options-ui-§16: host extras.** Allow a host extra to pair into the empty right cell after an odd
  canonical row count, so *Border offset* does not sit alone (P27). Only if the owner considers the
  half-empty cell a defect.
- **LibKa0s: publish `O.STRATA_TIP`** (or a strata dropdown composer) so every strata picker in the
  collection carries the same warning (L20).

## Review

Independent review against `../PanelMaster` at `e0a9ee3` (v1.3.0), 2026-10-24.

- **Current map:** verified every builder (`Schema.lua`, `Panel.lua`, `PanelEditor.lua`,
  `PanelEditorTabs.lua`, lib `OptionsCompose.lua`). Rows, labels and order are accurate. Added the two
  header Defaults buttons to the map, the reason Minimap button is alone, and fixed the
  line-count: the tabs have 3 + 5 + 5 + 8 + 9 + 2 = **32** control lines (the draft said 37 and counted
  General as 2), plus 8 headings.
- **Setting-change check (struck/rewrote):** **L07 rewritten.** `Registry.CopyFrom` copies everything
  except id, name and position, including enabled, strata, level, scale and fade, so "Copy appearance
  from" would have made the label less accurate. The label stays; the tooltip is fixed. P08 rewritten to
  match. No other change touches a key, default, range or behaviour. L02 checked: `group` is not stored
  and no `/pm reset <group>` form exists.
- **Corrected claims:** L03 does not remove a half-empty button row. The composer draws a framed
  addon's `leadButton` alone on its own row (`OptionsCompose.lua:569`). Confidence went from 65% to 60%,
  and a tooltip line now separates it from the confirm-free *Reset position*. L04's "a panel's General
  tab" became "Panels ▸ General". L15 now keeps the **Edges** heading (dropping it leaves four uncaptioned
  checkboxes or a hand-rolled caption, anti-pattern #71) and renames the bar's "Border" to "Bar border".
  L08 rename went from 70% to 50% because §13 says a strip SHOULD fit one row. L20 is marked as the
  single owner of the strata tooltip that strata Z06 duplicates.
- **Added:** P32/L23 (Panel opacity tooltip says background and border, but the frame alpha also fades
  bars and art). P33/L24 (UI units vs screen units vs px). P34 (composed Reset position tooltip is wrong
  for this addon) with an upstream ask. P35 (README and settings doc quote tab names, folded into L22).
  P36 (Frame strata vs AuraMaster's "Strata"). L18 now also points the editor's Reset tooltip at
  General ▸ New panels. Added cross-addon notes on opacity, strata and unit wording, and an upstream
  clarification of §7's "control types".
- **Recalibrated/rejected:** L17 went from 45% to 35% and was rejected, because the current order is an
  argued in-game decision. L13 went from 60% to 55% and L19 from 70% to 65%. New *Considered and
  rejected* section: R01–R06, including both tab-merge options for cutting clicks and the original "Copy
  appearance from" relabel.
