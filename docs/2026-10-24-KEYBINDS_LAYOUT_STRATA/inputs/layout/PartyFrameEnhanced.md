# PartyFrameEnhanced — settings layout analysis

Scope: item 020, layout only. No setting key, default, range or behaviour changes. Read from `../PartyFrameEnhanced`
at `master` on 2026-10-24: `settings/{OptionsSetup,About,General,ElementRows,CastBars,TargetFrames,PetFrames,Profiles,Schema}.lua`,
`defaults/Profile.lua`, `locales/enUS.lua`, `docs/settings-panel.md`, `PartyFrameEnhanced.toc` (page order), the
vendored `libs/LibKa0s/OptionsCompose.lua` (LibKa0s v1.76.0) for the composed rows' labels, tooltips, orders and line
breaks, and `tests/test_optionssetup.lua` for what the suite pins about the layout.

PartyFrameEnhanced is **not** one of the seven addons with a primary window. It has no `Bindings.xml` and no
bindable action (its displays are HUD elements attached to party frames), so the planned General > Keybindings
tab does not apply here. Nothing below assumes one.

## Current map

Page order is registration order, which is the TOC's settings block (`PartyFrameEnhanced.toc:111-117`: General,
then CastBars, TargetFrames, PetFrames, Profiles; `settings/ElementRows.lua` sits in that block but registers no page).
Tab order is first-registration order of `group`, and rows sort by `order` inside a group (`settings/Schema.lua:341-356`).
Subsection headings are drawn whenever `subgroup` changes inside a tab (`libs/LibKa0s/OptionsWidgets.lua:219-236`).
Composed blocks number their rows `order + n * ORDER_STEP` (`OptionsCompose.lua:169`), so a block declared at
`order = 10` takes 10, 20, 30, ...
Widget types: CB checkbox, SL slider, DD dropdown, LSM LibSharedMedia dropdown, CP colour picker, BTN button.
`[a][b]` is one two-column line; `(solo)` is a row alone on its line by `solo`/`startsLine`.

```
Ka0s Party Frame Enhanced (landing)        settings/OptionsSetup.lua:87-89 -> settings/About.lua:14-23 (BuildLandingPage)
  untabbed (options-ui-§13 exemption): logo, TOC Notes tagline, "Slash Commands" + one label per NS.COMMANDS row

General                                    settings/General.lua:235-258 (CreatePanel :238, RenderTabbedSchema :250)
  Tab "Master controls"                    composed: H.MasterControls, settings/General.lua:76-95, registered :132
    [Enable Party Frame Enhanced CB enabled]     [General visibility DD visibility]
    [Master scale SL scale]                      [Master alpha SL alpha]
    [Lock frame CB locked]                       [Debug console CB state.debugConsole (session)]
    [Minimap button CB global.minimap.shown]     (no Test mode: unlocking IS the preview, options-ui-§15)
    [Reset position BTN]                         [Reset all settings BTN -> PARTYFRAMEENHANCED_RESET_ALL]
  Tab "Party frames"                       settings/General.lua:134-182 (no subgroups)
    [Frame system DD general.provider]           [Include my own row CB general.includePlayer]
    [Fade with party frames CB general.rangeFade][Frame strata DD general.strata]
  Tab "Health updates"                     settings/General.lua:187-215 (no subgroups)
    [Update health CB general.updateHealth]      [Health refresh (seconds) SL general.tickInterval  (dims: updateHealth off)]

Cast Bars                                  settings/CastBars.lua:81-85 -> settings/ElementRows.lua:140-153
  Tab "General"                            settings/CastBars.lua:31-39 (no subgroups)
    [Enable cast bars CB castbar.enabled] (solo)
    [Fade out CB castbar.fadeOut]
  Tab "Size & Position"                    settings/ElementRows.lua:36-84 (orders 10-100)
    Subsection "Size"
      [Width SL castbar.width (dims: attached + matchWidth)]   [Height SL castbar.height]
    Subsection "Placement"
      [Anchor mode DD castbar.anchorMode]        [Match party frame width CB castbar.matchWidth (dims: free)]
    Subsection "Attached to party frames"  (drawn only when anchorMode = attached, shownWhen)
      [Anchor point DD castbar.point]            [Party frame point DD castbar.relativePoint]
      [X offset SL castbar.offsetX]              [Y offset SL castbar.offsetY]
    Subsection "Free placement"            (drawn only when anchorMode = free, shownWhen)
      [Growth direction DD castbar.growth]       [Spacing SL castbar.spacing]
  Tab "Bar"                                settings/CastBars.lua:43-55, ElementRows.lua:112-131
    Subsection "Fill"                      composed BarGroup at order 10 (10-40), barColor relabelled "Cast color"
      [Bar texture LSM castbar.barTexture]       [Bar opacity SL castbar.barAlpha]
      [Cast color CP castbar.barColor]           [Use class color CB castbar.useClassColorBar]
    Subsection "Cast colors"               orders 50-80; palette, no companion (options-ui-§17 exemption)
      [Channel color CP castbar.channelColor]    [Empowered color CP castbar.empowerColor]
      [Can't be interrupted color CP castbar.uninterruptibleColor] [Interrupted color CP castbar.failedColor]
    Subsection "Background"                composed ColorPair at order 100 (100, 110)
      [Background color CP castbar.bgColor]      [Use class color CB castbar.useClassColorBg]
  Tab "Border"                             settings/CastBars.lua:57, ElementRows.lua:87-96 (composed BorderGroup, order 10, no subgroup)
    [Show border CB castbar.borderShow] (solo)
    [Border style LSM castbar.borderStyle]       [Border thickness (px) SL castbar.borderSize]
    [Border color CP castbar.borderColor]        [Use class color CB castbar.useClassColorBorder]
  Tab "Text"                               settings/CastBars.lua:59-65, ElementRows.lua:99-108
    Subsection "Font"                      composed FontGroup at order 10 (10-60) + two host rows at 70/80 in the same subgroup
      [Font LSM castbar.font]                    [Font size SL castbar.fontSize]
      [Font color CP castbar.fontColor]          [Use class color CB castbar.useClassColorFont]
      [Font flags DD castbar.fontFlags]          [Font shadow CB castbar.fontShadow]
      [Show spell name CB castbar.showName]      [Show time left CB castbar.showTime]
  Tab "Icon"                               settings/CastBars.lua:67-77 (no subgroups, no dims)
    [Show spell icon CB castbar.showIcon]        [Icon side DD castbar.iconSide  (live while Show spell icon is off)]
    [Show shield CB castbar.showShield]          [Show spark CB castbar.showSpark]

Target Frames                              settings/TargetFrames.lua:94-98
  Tab "General"                            settings/TargetFrames.lua:35-44
    [Enable target frames CB target.enabled] (solo)
    [Click to target CB target.clickToTarget]
  Tab "Size & Position"                    as Cast Bars, paths target.*
  Tab "Bar"                                settings/TargetFrames.lua:48-62
    Subsection "Fill"                      [Bar texture LSM][Bar opacity SL] / [Bar color CP target.barColor][Use class color CB]
    Subsection "Reaction colors"           orders 50-80
      [Color NPCs by reaction CB target.colorReaction] [Hostile color CP target.hostileColor]
      [Neutral color CP target.neutralColor]     [Friendly color CP target.friendlyColor]
    Subsection "Background"                [Background color CP target.bgColor][Use class color CB target.useClassColorBg]
  Tab "Border"                             as Cast Bars, paths target.*
  Tab "Text"                               settings/TargetFrames.lua:66-73
    Subsection "Font"                      the font block (6 rows), then
      [Show name CB target.showName]             [Show health percent CB target.showPercent (dims: general.updateHealth off)]
  Tab "Marker"                             settings/TargetFrames.lua:75-90
    [Show raid marker CB target.showMarker] (solo)
    [Anchor point DD target.markerPoint] (solo, dims: marker off)
    [X offset SL target.markerOffsetX]           [Y offset SL target.markerOffsetY]   (dim: marker off)

Pet Frames                                 settings/PetFrames.lua:73-77
  Tab "General"                            settings/PetFrames.lua:31-39
    [Enable pet frames CB pet.enabled] (solo)
    [Click to target CB pet.clickToTarget]
  Tab "Size & Position"                    as Cast Bars, paths pet.*
  Tab "Bar"                                settings/PetFrames.lua:42-43
    Subsection "Fill"                      the bar block (Use class color = the OWNER's class)
    Subsection "Background"                composed ColorPair at order 50 (50, 60)
  Tab "Border"                             as Cast Bars, paths pet.*
  Tab "Text"                               settings/PetFrames.lua:45-52   as Target Frames, paths pet.*
  Tab "Marker"                             settings/PetFrames.lua:54-69   as Target Frames, paths pet.*

Profiles                                   settings/Profiles.lua:10-54 (AceDBOptions via AceConfigDialog; untabbed, no Defaults)
```

**Counts.** 6 pages (landing + 5 subcategories); 21 tabs (General 3, Cast Bars 6, Target Frames 6, Pet Frames 6;
landing and Profiles untabbed); **126 schema rows** (General 13: 7 master + 4 party frames + 2 health; Cast Bars 39;
Target Frames 39; Pet Frames 35) plus 2 buttons (the Master controls reset pair).

**What the suite pins** (any change below that moves these must update the test in the same commit; none is a
setting change): `tests/test_optionssetup.lua:83-95` (every feature page has a `L["Size & Position"]` tab whose
first subgroup is Size and third row's subgroup is Placement), `:123-135` (the drawn label sequence of that tab,
starting with the tab name), `:176-180` (`general.updateHealth` and `general.tickInterval` sit in group
`L["Health updates"]`). `tests/test_schema.lua:95,122` use `group = "Party frames"` only on probe rows and do not
care whether the real tab exists.

## Problems

| id | file:line | problem |
|---|---|---|
| PAR-P01 | settings/General.lua:187-215 | **Lonely tab.** *Health updates* is a whole tab for two rows, one of which only dims. A tab click to reach two controls. |
| PAR-P02 | settings/General.lua:134-182, 187-215 | *Party frames* and *Health updates* are the same kind of thing: settings shared by all three element kinds (every tooltip on both tabs names the cast bar, target frame and pet frame, or target and pet frames). Splitting them across two tabs is a split of one subject. |
| PAR-P03 | settings/TargetFrames.lua:70-73, PetFrames.lua:49-52 | **Cross-page dependency with no signpost.** *Show health percent* (Target/Pet > Text) dims when *Update health* (General > Health updates) is off. The player sees a gray box and has to know to go to another page. Neither tooltip names the parent. |
| PAR-P04 | settings/CastBars.lua:60-65, TargetFrames.lua:67-73, PetFrames.lua:46-52 | **Misgrouped rows.** *Show spell name / Show time left* (and *Show name / Show health percent*) sit under the subsection heading **Font**. They decide what text is shown, not how it looks. options-ui-§16 lets a block take extra rows "of the same kind" after it; these are not the same kind. |
| PAR-P05 | settings/CastBars.lua:60-65 | **Order against the mental model.** Inside Text, "what to show" comes after six "how it looks" rows. Everywhere else in the addon the show toggle comes first (*Show spell icon* opens Icon, *Show raid marker* opens Marker, *Show border* opens Border). |
| PAR-P06 | settings/CastBars.lua:57, TargetFrames.lua:64, PetFrames.lua:44 | **Short tab, extra click.** *Border* is a five-row tab on all three feature pages; its subject (the frame around the bar) is the same subject as *Bar*'s Fill and Background. options-ui-§16 names merging a background and a border group on one tab as legitimate, and MultiMeters already ships a *Background and border* tab. |
| PAR-P07 | settings/CastBars.lua:31-39 (and Target/Pet :35-44 / :31-39) | **Short tab.** Each feature page's *General* tab is two rows on two lines. Kept as is (see Kept): it is the page-wide act (enable) and the page opens on it. Nitpick only. |
| PAR-P08 | settings/ElementRows.lua:50-63 | **Parent below its dependant.** *Width* (Size, first line) dims when *Match party frame width* (Placement, the line below) is on, which is the cast-bar default (`defaults/Profile.lua:45`). A player opening Cast Bars > Size & Position meets a gray Width slider first, before the switch that grays it. Neither tooltip says why it is dimmed. |
| PAR-P09 | settings/ElementRows.lua:60-63 | *Match party frame width* dims in free placement but its tooltip only starts "Attached: ..."; it does not say it is ignored in free placement. |
| PAR-P10 | locales/enUS.lua, settings/ElementRows.lua:37 | **Capitalisation and spelling.** *Size & Position* is the only Title Case tab label in the addon; every other tab is sentence case. The collection spells this tab **Size and position** (13 uses: KickCD `settings/Castbar.lua:246`, MultiMeters), and joins two-subject tab names with "and" (*Background and border*, *Size and crop*, *Icon and label*); `&` appears once (AuraMaster *Background & border*). |
| PAR-P11 | settings/TargetFrames.lua:78-82, PetFrames.lua:57-61 | **One label, two meanings.** *Anchor point* on the Marker tab is "the point on the bar the marker's center sits on"; *Anchor point* on Size & Position is "the point on the element that is pinned". Same words, different subject, two tabs apart. |
| PAR-P12 | settings/TargetFrames.lua:83-90 | *X offset / Y offset* on Marker repeat Size & Position's labels for a different nudge. The Marker tab label already disambiguates, and "X offset" is the collection's plain spelling (10 uses). Nitpick. |
| PAR-P13 | settings/CastBars.lua:36-38 | **Ambiguous label.** *Fade out* sits a page away from *Fade with party frames* and *Master alpha*, three different fades. "Fade out" alone does not say *what* fades out *when*. It applies to every ended cast, including after an interrupted cast's hold (`modules/CastBars.lua:197-200, :225-228`), so "finished" would be too narrow. |
| PAR-P14 | settings/CastBars.lua:43-54 | **Split palette.** The plain-cast colour (*Cast color*, barColor) lives in Fill; the other four cast-state colours live in a subsection called *Cast colors*. The heading reads as if it holds every cast colour, and the plain one is not there. (barColor must stay in the composed Bar block, options-ui-§16.) |
| PAR-P15 | settings/General.lua:200-213 | *Health refresh (seconds)* only paces **target** frames (its tooltip says pets use the game's events), but the label reads as if it governs both. |
| PAR-P16 | settings/General.lua:148-156 | *Include my own row*: "row" is party-frame jargon; the tooltip does the explaining. Nitpick. |
| PAR-P17 | settings/ElementRows.lua:20, :64-75 | The Anchor mode value *Attach to party frames* (imperative) heads a subsection called *Attached to party frames* (past participle), while its sibling value is *Free placement* (a noun phrase, same as its subsection). Two spellings of one choice on one tab. Nitpick. |
| PAR-P18 | libs/LibKa0s/OptionsCompose.lua:489-491 (composed row) | **The addon's one preview switch is undiscoverable.** *Lock frame*'s tooltip is the composer's "Stop the frame being dragged." In this addon, unlocking also turns on preview mode (placeholders, plus a stand-in party frame out of a party; `modules/Preview.lua:8-21`), it is refused in combat and re-locked when combat starts (`:23-34`), and there is no Test mode row. Nothing in the panel says so. |
| PAR-P19 | libs/LibKa0s/OptionsCompose.lua:553-557 | *Reset position*'s tooltip "Move the frame back to where it started." only moves the **free-placement stacks** (`modules/Anchor.lua:400-408` clears each feature's `position`); attached elements are untouched. The composer does not let the host change the tooltip. Upstream. |
| PAR-P20 | settings/TargetFrames.lua:49-61 | The three reaction swatches stay live when *Color NPCs by reaction* is off (correctly: no `disabledIf` on a colour, options-ui-§17, anti-pattern #74), but their tooltips do not say they are unused then. |
| PAR-P21 | libs/LibKa0s/OptionsCompose.lua:355-378 | Border style, thickness and colour stay live with *Show border* off, while the Marker tab dims its rows when the marker is off. The pattern is inconsistent within the addon, but it is behaviour owned by the composer, so it is upstream only. |
| PAR-P22 | settings/General.lua:3-16, CastBars.lua:3-14, TargetFrames.lua:3-15, PetFrames.lua:3-14, docs/settings-panel.md:14 | **Doc drift.** The General header diagram shows two tabs and omits *Health updates*; `docs/settings-panel.md:14` lists the Party frames tab without *Frame strata*. Every change below also touches these diagrams, `docs/settings-panel.md`, `docs/schema.md:24`, `docs/smoke-tests.md` (PANEL-6, CAST-7, UNIT-10, PREV-3, PROFILE-4), `docs/test-cases.md:518-522`, `README.md:50-52` and the `modules/RangeFade.lua:36` comment ("General → Party frames → Frame strata"). |
| PAR-P23 | settings/CastBars.lua:67-77 | *Show spark* is a decoration of the **fill** (it rides the fill's edge, `modules/Element.lua:105-108`), filed under *Icon*. *Show shield* is an icon and belongs there; the spark does not. |
| PAR-P24 | settings/CastBars.lua:67-77 | **Inconsistent dimming of host-written dependants.** *Icon side* stays live while *Show spell icon* is off, while the host-written Marker rows dim with *Show raid marker* (`TargetFrames.lua:33, :82-90`). Unlike P21 this one is the host's own row. |
| PAR-P25 | settings/General.lua:134-182 | **Tab named after one of its subjects.** The *Party frames* tab holds *Frame strata* and *Fade with party frames*, which are about the elements, not the party frames. Folded into PAR-L01. |

## Proposed changes

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| PAR-L01 | General page: **merge** tabs *Party frames* and *Health updates* into one second tab, named **All elements**, with two subsections: **Party frames** (the four rows of today's tab, same order and pairs: `general.provider`, `general.includePlayer`, `general.rangeFade`, `general.strata`) and **Health updates** (`general.updateHealth`, `general.tickInterval`). Implementation: both groups become `L["All elements"]`, the rows gain `subgroup`, and the health rows' orders move to 50/60 so they sort after 10-40. | One tab instead of two, with no lonely 2-row tab. Everything on it is shared by cast bars, target frames and pet frames, which is what the name says. The tab now mixes two subjects, so it carries subsection headings (options-ui-§7; neither repeats the tab's name). Two subsections rather than three: today's four Party frames rows already read as one block about how the elements relate to the party frames, and a third heading over two rows is noise. Test `tests/test_optionssetup.lua:176-180` moves from group to subgroup. | 70% | P01, P02, P25 |
| PAR-L02 | All three feature pages: **merge** the *Border* tab into the *Bar* tab, renamed **Bar and border**; the border block becomes subsection **Border** after *Background*. Implementation: `ElementRows.Border` passes `group = L["Bar and border"], subgroup = L["Border"], order = 120` (sorts after Background's 100/110 on Cast/Target and 50/60 on Pet); `ElementRows.Bar`/`Background` and the host rows in the palette subsections take the new group name. | Removes one tab on three pages (3 clicks saved per full pass). Fill, background and border are one subject, "how the bar is drawn". options-ui-§16 explicitly allows a merged background + border tab with subsection headings; MultiMeters' *Background and border* is the precedent and the spelling. The tab becomes 15 rows on Cast/Target (16 with L16) and 11 on Pet: long, but one scroll instead of a tab click. | 65% | P06 |
| PAR-L03 | Cast Bars > Text: move `castbar.showName`, `castbar.showTime` out of subsection *Font* into a new subsection **Shown text** placed **before** Font. Implementation: the two host rows take `subgroup = L["Shown text"]`, orders 10/20, and `ElementRows.Font` is declared at `order = 30` (composed 30-80). Target and Pet > Text: the same for `showName`, `showPercent`. | They are content toggles, not font rows (P04), so they may not ride as §16 extras under the Font heading. Show-first matches the addon's own pattern on Icon, Marker and Border (P05). Keeps the composed Font block contiguous and pure. | 75% | P04, P05 |
| PAR-L04 | Target and Pet > Text > *Show health percent* tooltip: append "Dimmed while General > All elements > Update health is off." (L01's name; "General > Health updates" if L01 is declined). | The only cross-page dependency in the addon. It cannot be removed without duplicating a shared row, so name it where the player meets it. | 85% | P03 |
| PAR-L05 | Size and position: *Width* tooltip append "Dimmed while attached with Match party frame width on." *Match party frame width* tooltip: "Attached only (dimmed in free placement): stretch each element across its party frame, edge to edge. Width is then ignored." | Says why a slider is gray without reordering the tab (see L06). Matters most on Cast Bars, where the gray Width is the default state. | 80% | P08, P09 |
| PAR-L06 | Size and position: put subsection **Placement** (Anchor mode, Match party frame width) **before** **Size** (Width, Height). | Parent before dependant: Anchor mode decides which of the remaining blocks is shown and whether Width applies. **Held back by cross-addon consistency**: KickCD and MultiMeters open the same-named tab with size. Do this only if the collection adopts "mode first" (see Upstream). Inverts the pin at `tests/test_optionssetup.lua:92-94`. | 45% | P08 |
| PAR-L07 | Rename tab label *Size & Position* → **Size and position** (all three pages; `group` string in ElementRows.lua:37 and its locale key). | Sentence case like every other tab in the addon, and the collection's existing spelling of this exact tab (P10). `group` is not a stored path, so no migration (options-ui-§15 says the same of tab renames). Tests at `tests/test_optionssetup.lua:83-135` reference the locale key and follow it. | 80% | P10 |
| PAR-L08 | Target and Pet > Marker: relabel `markerPoint` *Anchor point* → **Point on bar**. Offsets keep *X offset / Y offset* (see Considered and rejected). | Removes the two-meanings clash with Size and position's *Anchor point* (P11). The tooltip already says "The point on the bar the marker's center sits on." | 60% | P11 |
| PAR-L09 | Cast Bars > General: relabel *Fade out* → **Fade out when a cast ends**; tooltip "Fade the bar out when a cast ends, including after an interrupted cast's hold, instead of hiding it at once." | Separates it from the other two fades without a tooltip read, and describes what the code does (P13: it is not only finished casts). | 60% | P13 |
| PAR-L10 | Cast Bars > Bar: rename subsection *Cast colors* → **Cast state colors**; relabel the Fill block's barColor *Cast color* → **Normal cast color** (via the composer's `labels`, as today). | barColor cannot leave the composed Fill block, so the labels have to make the split read as intended: the normal colour in Fill, the four state colours below. "Cast state colors" reads better as a heading than "Other cast states". | 55% | P14 |
| PAR-L11 | General: relabel *Health refresh (seconds)* → **Target health refresh (seconds)**. | The label then matches the tooltip's own scope. | 60% | P15 |
| PAR-L12 | General: relabel *Include my own row* → **Include myself**. Update `README.md:50` in the same commit. | Plain words; the tooltip keeps the detail. Low because "Include myself" without the tooltip is vaguer about *in what*. | 45% | P16 |
| PAR-L13 | Relabel the Anchor mode value *Attach to party frames* → **Attached to party frames** (matches the subsection heading; the stored value `attached` is unchanged). | One spelling for one choice on one tab, and both values then read as noun phrases (*Free placement*). `docs/smoke-tests.md` PANEL-6 quotes the old value. | 45% | P17 |
| PAR-L14 | Master controls > *Lock frame*: give the row a tooltip that says it is also the preview switch: "Unlock to preview and place the elements: placeholder content on your party frames, or a stand-in party frame when you are not in a party. Cannot unlock in combat; combat locks again." Label unchanged (options-ui-§15). **Preferred route is upstream** (a composer option, see Upstream suggestions), so AbsorbTracker and PFE get identical words; stamping the tooltip host-side onto the composed row (as General.lua:119-131 stamps get/set/onChange/validate) is the fallback. | The addon's only preview switch is invisible in the panel today. Lowered from 70%: §15 and the composer's own comments treat the canonical rows' wording as the library's ("the composer stays the only writer of that text", OptionsCompose.lua:448-452, the `leadButton` note), so a host rewrite of a composed tooltip is against the rule's spirit even if no MUST names tooltips. | 50% | P18 |
| PAR-L15 | Target > Bar and border > the three reaction swatches: append to each tooltip "Used only while Color NPCs by reaction is on." | Explains a live control that does nothing in one state, in words, which is what options-ui-§17 asks for instead of dimming a colour. | 60% | P20 |
| PAR-L16 | Cast Bars: move `castbar.showSpark` from tab *Icon* to *Bar and border* > Fill, appended after the composed block through `BarGroup{ extra = ... }` (options-ui-§16 allows extra same-kind rows after the block; `ElementRows.Bar` gains an `extra` pass-through used by Cast Bars only). The Icon tab is then [Show spell icon][Icon side] / [Show shield]. | The spark is a fill decoration (P23). The Icon tab then holds only icons. Held at 50% because "same kind" is arguable (§16's examples are fill direction and bar spacing, which are fill properties too) and the Icon tab shrinks to three rows. | 50% | P23 |
| PAR-L17 | Cast Bars > Icon: dim *Icon side* while *Show spell icon* is off (`disabledIf`, as the Marker rows already do). | Same pattern as the Marker tab for the same shape of dependency (P24). It is a panel affordance only: no key, default, range or stored behaviour moves. If the owner reads "do not change any settings" as covering dims too, drop it. | 50% | P24 |
| PAR-L18 | Update the General.lua / CastBars.lua / TargetFrames.lua / PetFrames.lua header diagrams, `docs/settings-panel.md` (including the missing *Frame strata*), `docs/schema.md:24`, `docs/test-cases.md:518-522`, the affected `docs/smoke-tests.md` steps, `README.md:50-52`, the `modules/RangeFade.lua:36` comment and the pinned tests to the final map, in the same commit as the layout change. | Doc drift (P22), and the suite pins three of the moved names. | 90% | P22 |

**Kept as they are, deliberately**
- Master controls rows, order and labels: fixed by options-ui-§15. No Test mode row: §15 exempts an addon whose unlocked view is its test mode.
- Feature pages' *General* first tab (P07): it holds the page's enable act and the page opens on it. Folding it into another tab would put *Enable cast bars* below unrelated rows. A 2-row tab is the smaller cost.
- *Health updates* stays on the General page rather than Target Frames: the switch is shared by target and pet frames (one row, two consumers). Moving it would put a pet-frame control on the target page.
- Marker tab: stays its own tab. It is a separate decoration with its own show toggle and three dependants, and it does not fit Text or Bar and border.
- `solo` on *Show raid marker* and *Point on bar* stays: un-soloing would pair *Point on bar* with *X offset* and leave Y alone.
- Page titles *Cast Bars / Target Frames / Pet Frames* stay Title Case: they are sidebar category names, which Blizzard's own list title-cases; tab labels are sentence case.

## Considered and rejected

| idea | why rejected | confidence |
|---|---|---|
| Relabel the Marker offsets *Marker X offset / Marker Y offset* (part of the original L08). | The tab is named *Marker*, so the prefix repeats it on every row; "X offset" is the collection's plain spelling (10 uses). The tooltips already say "of the marker". | 35% |
| Split L01's merged tab into three subsections (*Party frames*, *Fading & layer*, *Health updates*), as first proposed. | A heading over every two rows; today's four Party frames rows are already one subject. Also used `&` against the collection's "and". | 35% |
| Fold the General page's non-master rows into *Master controls* through `MasterControls{ extra = ... }` (they are addon-wide), leaving General one tab. | §15's extension is for a row the player looks for beside the canonical set (QuickComms' single *Preview as*). Six extras with no subsection headings would dwarf the canonical set, and extras cannot carry their own subsections without faking a second level. | 30% |
| Rename each feature page's *General* tab (it shares its name with the General page). | Every Ka0s feature page that has one opens on a tab called *General* (KickCD's Cast bar entry too). Changing it in one addon breaks a collection-wide convention for a nitpick. | 30% |

## Proposed map

```
Ka0s Party Frame Enhanced (landing)        unchanged

General
  Tab "Master controls"                    unchanged rows; Lock frame tooltip (L14, preferably upstream)
    [Enable Party Frame Enhanced CB enabled]     [General visibility DD visibility]
    [Master scale SL scale]                      [Master alpha SL alpha]
    [Lock frame CB locked]                       [Debug console CB state.debugConsole]
    [Minimap button CB global.minimap.shown]
    [Reset position BTN]                         [Reset all settings BTN]
  Tab "All elements"                       (L01)
    Subsection "Party frames"
      [Frame system DD general.provider]         [Include myself CB general.includePlayer]          (L12)
      [Fade with party frames CB general.rangeFade] [Frame strata DD general.strata]
    Subsection "Health updates"
      [Update health CB general.updateHealth]    [Target health refresh (seconds) SL general.tickInterval]  (L11)

Cast Bars
  Tab "General"
    [Enable cast bars CB castbar.enabled] (solo)
    [Fade out when a cast ends CB castbar.fadeOut]                                                   (L09)
  Tab "Size and position"                  (L07; L06 optional: Placement before Size; tooltips L05)
    Subsection "Size"                      [Width SL castbar.width][Height SL castbar.height]
    Subsection "Placement"                 [Anchor mode DD castbar.anchorMode][Match party frame width CB castbar.matchWidth]
                                           (Anchor mode values: Attached to party frames / Free placement, L13)
    Subsection "Attached to party frames"  [Anchor point DD castbar.point][Party frame point DD castbar.relativePoint]
                                           [X offset SL castbar.offsetX][Y offset SL castbar.offsetY]
    Subsection "Free placement"            [Growth direction DD castbar.growth][Spacing SL castbar.spacing]
  Tab "Bar and border"                     (L02)
    Subsection "Fill"
      [Bar texture LSM castbar.barTexture]       [Bar opacity SL castbar.barAlpha]
      [Normal cast color CP castbar.barColor]    [Use class color CB castbar.useClassColorBar]
      [Show spark CB castbar.showSpark]                                                      (L16)
    Subsection "Cast state colors"         (L10)
      [Channel color CP castbar.channelColor]    [Empowered color CP castbar.empowerColor]
      [Can't be interrupted color CP castbar.uninterruptibleColor] [Interrupted color CP castbar.failedColor]
    Subsection "Background"
      [Background color CP castbar.bgColor]      [Use class color CB castbar.useClassColorBg]
    Subsection "Border"
      [Show border CB castbar.borderShow] (solo)
      [Border style LSM castbar.borderStyle]     [Border thickness (px) SL castbar.borderSize]
      [Border color CP castbar.borderColor]      [Use class color CB castbar.useClassColorBorder]
  Tab "Text"
    Subsection "Shown text"                (L03)
      [Show spell name CB castbar.showName]      [Show time left CB castbar.showTime]
    Subsection "Font"
      [Font LSM castbar.font]                    [Font size SL castbar.fontSize]
      [Font color CP castbar.fontColor]          [Use class color CB castbar.useClassColorFont]
      [Font flags DD castbar.fontFlags]          [Font shadow CB castbar.fontShadow]
  Tab "Icon"
    [Show spell icon CB castbar.showIcon]        [Icon side DD castbar.iconSide (dims: icon off, L17)]
    [Show shield CB castbar.showShield]

Target Frames
  Tab "General"                            [Enable target frames CB target.enabled] (solo) / [Click to target CB target.clickToTarget]
  Tab "Size and position"                  as Cast Bars, paths target.*
  Tab "Bar and border"
    Subsection "Fill"                      [Bar texture][Bar opacity] / [Bar color][Use class color]
    Subsection "Reaction colors"           [Color NPCs by reaction CB target.colorReaction][Hostile color CP]
                                           [Neutral color CP][Friendly color CP]   (swatch tooltips: L15)
    Subsection "Background"                [Background color CP target.bgColor][Use class color CB target.useClassColorBg]
    Subsection "Border"                    [Show border] (solo) / [Border style][Border thickness (px)] / [Border color][Use class color]
  Tab "Text"
    Subsection "Shown text"                [Show name CB target.showName][Show health percent CB target.showPercent]  (tooltip: L04)
    Subsection "Font"                      the font block (6 rows)
  Tab "Marker"
    [Show raid marker CB target.showMarker] (solo)
    [Point on bar DD target.markerPoint] (solo)                                              (L08)
    [X offset SL target.markerOffsetX]           [Y offset SL target.markerOffsetY]

Pet Frames
  Tab "General"                            [Enable pet frames CB pet.enabled] (solo) / [Click to target CB pet.clickToTarget]
  Tab "Size and position"                  as Cast Bars, paths pet.*
  Tab "Bar and border"
    Subsection "Fill"                      the bar block (owner's class)
    Subsection "Background"                [Background color CP pet.bgColor][Use class color CB pet.useClassColorBg]
    Subsection "Border"                    the border block
  Tab "Text"                               as Target Frames, paths pet.*
  Tab "Marker"                             as Target Frames, paths pet.*

Profiles                                   unchanged
```

**Counts after.** 6 pages (unchanged); **17 tabs** (General 2, Cast Bars 5, Target Frames 5, Pet Frames 5), down from
21; 126 schema rows (unchanged) plus the 2 buttons. Every strip fits one row.

## Cross-addon notes

- **Tab name for size and placement.** The collection already says *Size and position* (KickCD, MultiMeters); PFE is
  the outlier with *Size & Position* (L07). KickCD and MultiMeters also order size before position, which is why
  PAR-L06 is held at 45%.
- **"and", not "&", in two-subject tab names.** *Background and border* (MultiMeters), *Size and crop*, *Icon and
  label*; AuraMaster's *Background & border* is the one `&`. PFE's new *Bar and border* follows the majority; the
  AuraMaster report should consider the same.
- **Frame strata as a setting.** Three addons expose it, each in a different place and with different value
  spellings. PFE has `general.strata` on General (L01: All elements > Party frames), lowercase keys, default `auto`
  ("Match party frames"). MultiMeters has `window.frame.strata`, uppercase, default `MEDIUM`. AuraMaster has
  `container.layout.strata` plus a *Frame level* row. The label is already the same (*Frame strata*). Put it in the
  same kind of tab everywhere (wherever the display's position or layer lives) and give it the same tooltip shape
  (item 030's guidance should define that wording).
- **Cross-page dependencies.** Whenever a row dims because of a row on another page, the tooltip should name the
  parent's location (PAR-L04). Check the other addons for the same pattern.
- **"Shown text" before "Font".** Any addon that appends content toggles (*Show name*, *Show time*) under a
  composed Font block has the same P04. Name the subsection the same way collection-wide.
- **Lock = preview.** AbsorbTracker (per its report) and PFE both have no Test mode row because unlocking is the
  preview. Both need the same *Lock frame* tooltip wording, which is the argument for doing L14 upstream.
- **Feature pages open on "General".** Kept here for the same reason everywhere; not a per-addon decision.
- **Keybindings.** PFE is not in the seven-window set, so its General page gets no Keybindings tab. After L01 its
  General page has two tabs (*Master controls*, *All elements*).

## Upstream suggestions

- **options-ui-§15 / LibKa0s `MasterControls`:** add a spec flag for the §15 "unlocked view is the test mode"
  exemption (for example `lockIsPreview = true`) that swaps in one canonical *Lock frame* tooltip saying it is the
  preview switch, and a `resetPositionTooltip` (or a canonical "Move the movable parts back to where they started"
  wording) for addons whose Reset position moves only some frames. Labels stay fixed; the wording stays the
  library's, so every such addon reads the same (P18, P19).
- **options-ui-§13 "one tab per section":** add a SHOULD on minimum tab size, for example "a section of three or
  fewer rows SHOULD be a subsection of a related tab rather than its own tab, unless it is the page's first
  (General) tab". This is the rule that produces lonely tabs like *Health updates* (P01) and *Border* (P06).
- **options-ui-§16 `BorderGroup` with `show = true`:** dim the non-colour border rows (style, thickness) while
  *Show border* is off, as host-written show toggles in the collection already do for their dependants (P21).
  Colour rows stay undimmed per §17.
- **options-ui-§16 extras:** say whether a "show" decoration of the fill (a spark) counts as a same-kind extra of the
  bar block, so L16 is a rule rather than a judgement.
- **Collection convention for Size and position order:** decide "mode first, then size" vs "size first" once,
  in options-ui, so PAR-L06 and KickCD's tab agree.
- **Cross-page dependency rule:** a SHOULD that a dimmed row whose parent is on another page names the parent's
  location (page > tab) in its tooltip.
- **Tab-name style:** a SHOULD that tab labels are sentence case and join two subjects with "and".

## Review

Independent review against the code at `master` (LibKa0s v1.76.0), 2026-10-24.

- **Current map.** Verified every row, pair, dim and subgroup against `settings/*.lua` and the composer; counts
  (21 tabs, 126 rows) are right. Corrected: ElementRows is in the TOC settings block but registers no page; added
  the composed blocks' order ranges (needed to check that L02/L03's reorders actually sort as claimed); added that
  *Icon side* has no dim; added Pet's Background order (50/60); added the "What the suite pins" note, since
  L01/L06/L07 each move a name `tests/test_optionssetup.lua` asserts.
- **No setting changes.** None of the proposals moves a key, default, range or stored value. L17 (new) adds a dim,
  which is a panel affordance, and is flagged so the owner can strike it. L14's original wording was accurate
  against `modules/Preview.lua` but is now worded to include the combat refusal.
- **Standard compliance.** L14 lowered 70% → 50% and re-routed upstream: §15 and the composer treat the canonical
  rows' wording as the library's. All subsection names checked against §7's "MUST NOT repeat its tab's name".
- **Collection spelling.** L07 changed from *Size & position* to **Size and position** and L02 from *Bar & border*
  to **Bar and border**: the collection uses "and" (13 uses of *Size and position*, 4 of *Background and border*);
  the original report cited KickCD's spelling and then proposed a different one.
- **Rewritten.** L01 now keeps today's four Party frames rows as one subsection (two headings instead of three);
  L08 keeps only *Point on bar* (offset prefix rejected); L09 says "when a cast ends" because `fadeOut` also covers
  interrupted casts after their hold; L10 heading is *Cast state colors*; L03 gives concrete orders (font block
  moved to 30) instead of 2/4; L12 and L13 name the docs they touch.
- **Added.** P24/L17 (Icon side dim), P25 (tab named after one subject), wider P22 doc list (README, schema.md,
  smoke and test-case docs, RangeFade comment, missing *Frame strata* in settings-panel.md), a "Considered and
  rejected" section, two cross-addon notes and three upstream suggestions.
- **Confidence recalibrated.** L02 70→65, L07 75→80, L08 65→60, L09 65→60, L14 70→50; offsets relabel and the
  three-subsection split moved under 40% and rejected.
