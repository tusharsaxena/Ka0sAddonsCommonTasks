# AuraMaster — settings layout analysis

Read from `../AuraMaster` on `master` (clean), 2026-10-24: all of `settings/` (`OptionsSetup.lua`, `Schema.lua`,
`General.lua`, `GeneralSpells.lua`, `GeneralUserCategories.lua`, `GeneralDispel.lua`, `Containers.lua`,
`Filters.lua`, `Layout.lua`, `Bars.lua`, `Icons.lua`, `Text.lua`, `Profiles.lua`, `About.lua`),
`defaults/Profile.lua`, `core/Constants.lua`, `docs/settings-panel.md`. Standard: `options-ui.md` §5, §7, §13,
§14, §15, §16, §17. Row inventory checked headlessly: the addon was loaded through the repo's own test loader
(scratch script, no repo writes) and `NS.SchemaForPage` was walked page by page.

**Keybindings (item 015) do not apply here.** AuraMaster has no primary window (the roster's *Show window*
column is empty for it, and `docs/settings-panel.md` → Launcher says so), so it gets no General → Keybindings
tab and no Bindings.xml. Nothing below plans for one.

## Current map

Pages: **4** in the Settings tree (landing, General, Containers, Profiles); 2 untabbed by rule (landing,
Profiles). Containers is one page with a **nav rail** of 4 entries per container (General, Filters, Layout,
and the one style section: Bar | Icon | Text). Tabs: General page **4**; rail General **1**, Filters **5**,
Layout **5**, Bar **7**, Icon **6**, Text **5**. A player sees at most 4 + 1 + 5 + 5 + 7 = **22 tabs**
(bars container). Schema rows: **276** (General 18, Containers 5, Filters 57 across both aura types (36 on
a buff container, 35 on a debuff one: 3 General + 3 Sorting + 10 Situations + 19 category rows on each
type, plus *Hide enchants without a duration* on buffs), Layout 38, Bars 72, Icons 42, Text 44). `docs/settings-panel.md`
says 269 and Text 37, and lists Text as "Four tabs" over a five-tab table: it predates the glow rows (7).

Notation: `|` separates the two cells of one line. `(skip)` = schema row drawn by a bespoke renderer.
Rows that a mode/aura type hides are marked `[only …]`.

```
Ka0s Aura Master (landing)              settings/About.lua:23 BuildLandingPage (buildMain OptionsSetup.lua:190)
  logo · Notes tagline · "Slash Commands" heading · one line per NS.COMMANDS row           (no settings)

General (page)                          settings/General.lua:191 build, :206 RenderPage(PAGE_SPEC :184)
  Tab 1  Master controls                composed: General.lua:53 H.MasterControls, tail :187
    Enable Aura Master (bool, enabled)          | General visibility (dropdown, visibility)
    Master scale (slider, scale)                | Master alpha (slider, alpha)
    Lock frame (bool, locked)                   | Debug console (bool, state.debugConsole, session)
    Minimap button (bool, global.minimap.shown) | Test mode (bool, state.testMode, session)
    [Reset position] | [Reset all settings]     (composer tail)
  Tab 2  Display                        General.lua:139-154
    -- Blizzard frames --
    Hide Blizzard buffs (bool, hideBlizzardBuffs) | Hide Blizzard debuffs (bool, hideBlizzardDebuffs)
  Tab 3  Spell Categories               bespoke: GeneralSpells.lua:806 renderSpells, tab :952
    lead-in text
    Category (dropdown, page state UC.SetSelected) | [Restore this category's starter list]
    (yours only) Rename this category (edit box) | [Delete this category]       GeneralUserCategories.lua:514
    (only with broken records) count line + [Forget unreadable categories]
    answer line
    -- Make a new category --  New category's name (edit) | Aura type (dropdown) / [Create category]
    -- Spells in this category --  Add a spell (IdList, writes categorySpells) + 2-column entry list
    [Weapon enchants entry instead:] lead-in, -- Weapon slots -- 2 notes,
       Main hand | Off hand / Ranged  (bool, enchantSlots.mainHand/offHand/ranged, skip)   GeneralSpells.lua:793
  Tab 4  Dispel Colors                  bespoke: GeneralDispel.lua:61 renderDispel, tab :75
    lead-in + 4 bullets
    Magic | Curse / Disease | Poison / Bleed  (color, dispelColors.<type>)

Containers (page)                       settings/Containers.lua:266 build, :278 RenderContainerPage (OptionsSetup.lua:603)
  band   Container (dropdown, NS.State.activeContainerId) | [New container]        Containers.lua:257 BAND
  rail   General · Filters · Layout · Bar|Icon|Text                               OptionsSetup.lua:239 SECTION_ORDER
  Rail: General                         Containers.lua:246 RegisterContainerSection
    Tab 1  General                      Containers.lua:229 render
      Name (edit box, container.name)   | Enabled (bool, container.enabled)
      -- What it shows, and how --
      Unit (dropdown, container.unit)   | Aura type (dropdown, container.auraType)
      Style (dropdown, container.style) |
      [Duplicate] | [Delete]
      -- Copy settings from -- (2+ containers)  Source container (dd) | What to copy (dd) / [Copy onto this container]
  Rail: Filters                         settings/Filters.lua:950 RegisterContainerSection; intro = warnings
    Tab 1  General                      Filters.lua:64-78
      Cast by (dd, filter.castBy)               | Duration (dd, filter.durationMode)
      Max duration (slider, filter.maxDuration) | Preset (dd, same path, pairWith :93)
      -- Filter priority logic --  lead-in + 5 rank lines                         Filters.lua:431 (afterGroup)
    Tab 2  Categories                   bespoke Filters.lua:673 renderCategories
      -- Blizzard Categories --  [Show all] | [Hide all] · ChoiceGrid Show·Hide·Category (+ examples col)
      -- Spell Categories --     [view NOTE (see Situations)] [Show all] | [Hide all] · "These are the lists on
                                 General -> Spell Categories…" · grid (+ See spells col) ·
                                 tie line + Hide enchants without a duration (bool, filter.hidePermanentEnchants) [only buffs]
                                 · debuff CC note [only debuffs] · Uncategorized cost note [only player/pet buffs]
      -- Dispel Types --         [only debuffs] bulk pair + grid
      -- Who Cast It --          [only debuffs] bulk pair + grid
      (one ChoiceGrid row per filter.categories.<key>, 19 per aura type with the shipped lists, Weapon enchants
       and Uncategorized included, + player-made, all skip)
    Tab 3  Overrides                    bespoke Filters.lua:877 renderOverrides (before = Sorting, :966)
      [view NOTE (see Situations)]
      -- Whitelist --  blurb · Add a spell + list (filter.whitelist, not a row)
      -- Blacklist --  blurb · Add a spell + list (filter.blacklist, not a row)
    Tab 4  Sorting                      Filters.lua:190-204
      Sort by (dd, filter.sortMethod) | Direction (dd, filter.sortDirection)
      Max auras per group (0 = no limit) (slider, filter.maxAuras) |
    Tab 5  Situations                   bespoke Filters.lua:926 renderSituations
      -- Unit type --   Unit type (dd, filter.unitFilter.kind) | Reaction (dd, filter.unitFilter.reaction)  [only target/focus]
                        else "Always your own character or pet."
      -- Where spell lists don't apply --  unit line · On NPCs (dd, filter.situations.npcs) | On players (dd, .players)
                        (player/pet debuffs: one "Your own and your pet's debuffs" copy of .players) · honor note ·
                        timeless note; or "Spell lists always apply…" on player/pet buffs
      -- Show in --     Open world | Dungeons / Scenarios and delves | Raids / Battlegrounds | Arenas (bool, filter.zones.*)
  Rail: Layout                          settings/Layout.lua:695; intro growthIntro; afterGroup Anchor :698
    Tab 1  Frame                        Layout.lua:355-371
      Scale (slider, layout.scale) | Opacity (slider %, layout.alpha)
      Strata (dd, layout.strata)   | Frame level (slider, layout.level)
    Tab 2  Anchor                       Layout.lua:376-449
      Attach to (dd, attach.mode)
      -- Screen -- [only screen]          Point (position.point) | Relative point (position.relativePoint) / X | Y (position.x/y)
      -- Another container -- [only container]  Parent container (attach.container) | "Its X joins the Y of 'Z'"
                                           Parent container anchor point (attach.relPoint) | This container anchor point (attach.childPoint)
      -- Named frame -- [only frame]       Frame name (edit, attach.frame) | [Pick a frame...]
                                           Named frame anchor point (attach.relativePoint) | This container anchor point (attach.point)
      -- Offset -- [only attached]         X offset (attach.x) | Y offset (attach.y)
      facing-growth hint [frame mode]  ("Point is X and Grow vertically is Y … Set Grow vertically to Z on the Growth tab
                                        instead.", Layout.lua:669/:674, drawn by afterGroup[Anchor] :698; redrawn
                                        only by attach.point's onChange, growH/growV carry none)
    Tab 3  Growth                       Layout.lua:452-482 (inherited-flow note / follower count drawn by the
                                        section intro, gated on ctx.activeTab == Growth, Layout.lua:614-631)
      Fill (dd, layout.axis) | Per row or column (0 = one line) (layout.perLine)
      Grow horizontally (layout.growH) | Grow vertically (layout.growV)
      Spacing (px) (layout.spacing) | Line spacing (px) (layout.lineSpacing)
    Tab 4  Mouse                        Layout.lua:484-505
      Show tooltips (behavior.tooltips) | Tooltips in combat (behavior.tooltipInCombat)
      Tooltip position (behavior.tooltipAnchor) | Right-click to cancel (behavior.cancelOnRightClick)
      Click-through (behavior.clickThrough) |
    Tab 5  Label                        Layout.lua:524-557
      Show name label (label.show) | Justify (label.justifyH)
      X offset (label.x) | Y offset (label.y)
      -- Font --  composed font block, 6 rows (label.font.*)
  Rail: Bar  [only bars]                settings/Bars.lua:206 ("Bar")
    Tab 1  General       -- Size -- Width (px) | Height (px)                              Bars.lua:39-76
                         -- Fill -- Bar texture | Bar opacity / Bar color | Use class color / Color by | Drains toward / Smooth animation
                         -- Spark -- Show spark | Spark width (px) / Spark color | Use class color / Show the spark on auras without a duration
    Tab 2  Background & border  -- Background -- texture | opacity / color | class / Color by
                                -- Border -- Show border | Border style / thickness | color | class          Bars.lua:83-108
    Tab 3  Name text     -- Font -- 6 rows · -- Placement -- Show | Justify / Anchor / X offset | Y offset   Bars.lua:113-137
    Tab 4  Time text     same + -- Countdown -- Time format (bars.timeFormat)                           Bars.lua:138
    Tab 5  Stack text    same as Name text                                                             Bars.lua:143
    Tab 6  Icon          -- Icon -- Icon position | Icon size (0 = bar height) / Icon gap (px) | Icon zoom
                         -- Icon border -- 5-row border block                                         Bars.lua:153-177
    Tab 7  Pandemic      -- Time color -- Recolor the time… | Pandemic window (seconds left) / Pandemic-window time color
                         -- Highlight -- Highlight the pandemic window | Pandemic-window highlight color   Bars.lua:186-204
  Rail: Icon  [only icons]              settings/Icons.lua:120 ("Icon")
    Tab 1  Size          Width (px) | Height (px) / Icon zoom                                       Icons.lua:32-39
    Tab 2  Border        -- Border -- 5-row block + Color the border by dispel type                  Icons.lua:41-53
    Tab 3  Cooldown      Show cooldown swipe | Reverse the swipe / Draw the swipe's edge | Swipe darkness / Blizzard countdown numbers   Icons.lua:55-66
                         (the Blizzard numbers are drawn by the swipe's own Cooldown frame, which Show cooldown swipe
                         hides: modules/Style_Icons.lua:120-128)
    Tab 4  Time text     -- Font -- 6 · -- Placement -- 5 · -- Countdown -- Time format             Icons.lua:92
    Tab 5  Stack text    -- Font -- 6 · -- Placement -- 5                                          Icons.lua:97
    Tab 6  Pandemic      as Bars                                                                   Icons.lua:101-118
  Rail: Text  [only text]               settings/Text.lua:510 ("Text")
    Tab 1  General  (bespoke Text.lua:343 renderGeneral)
                         -- Size -- Size to fit | Width (px) / Height (px) · fit note
                         -- Text Template -- Template (dd, page-built) · Custom template (edit, text.template) [Custom only]
                                              · Preview (read-only edit box) · Tokens (≈9 bullets) · Rules (≈6 bullets + examples)
                         -- Placement -- Justify | Vertical justify · Justify note · X offset | Y offset · centering note
    Tab 2  Font (19 rows) -- Font -- 6 · -- Glow -- Glow behind the text | Glow color / Use class color | Intensity /
                         Thickness (px) | Offset X / Offset Y · -- Countdown -- Time format ·
                         -- Dispel type -- Color the dispel type / Backdrop in the dispel color | Backdrop opacity /
                         Edge in the dispel color | Edge thickness (px)                                Text.lua:366-419
    Tab 3  Icon          -- Icon -- Icon position | Icon size (0 = line height) / Icon gap (px) | Icon zoom
                         -- Icon border -- 5-row block                                               Text.lua:424-449
    Tab 4  Pandemic      -- Time color -- Recolor… | Pandemic window (seconds left) / Pandemic-window time color | Blink in the pandemic window   Text.lua:459-478
    Tab 5  Animation     -- Loop -- Effect | Seconds per cycle / Faded to | Bounce height (px)           Text.lua:484-495

Profiles                                settings/Profiles.lua:55 (AceDBOptions, untabbed by rule)
```

## Problems

| id | file:line | problem |
|---|---|---|
| AUR-P01 | settings/General.lua:139-154 | **Display is a 2-checkbox tab** under a vague name, and its one subsection *Blizzard frames* is the real subject. A whole tab and a heading for two rows. |
| AUR-P02 | settings/Filters.lua:190-204 | **Sorting is a 3-row tab.** Sort by / Direction / Max auras answer "what survives and in which order", the same question as Filters → General's Cast by / Duration / Max duration, one tab click away. |
| AUR-P03 | settings/Filters.lua:483-498, :926-948 | **Categories and Overrides both send the player to another tab** ("…not applied (see Situations)"): the *Where spell lists don't apply* dropdowns are the other half of the decision those two tabs make, and live 2 tabs further right. |
| AUR-P04 | settings/Filters.lua:926-948 | **Situations mixes two subjects.** *Unit type* and *Show in* are container visibility gates (`effect = "visibility"`), while *Where spell lists don't apply* is an aura filter (`effect = "view"`). The tab name says neither. |
| AUR-P05 | settings/Filters.lua:927 | The *Unit type* section heading repeats the label of its own first row (*Unit type*). |
| AUR-P06 | settings/Filters.lua:413-445, :957-959 | **The 5-rank priority block sits under General**, whose three rows take no part in the ranking (ranks are Overrides 1-2, Categories 3-5). The player reads the rule one tab away from the controls it governs. |
| AUR-P07 | settings/Filters.lua:193, :198, :203 | Sort by, Direction and Max auras repeat the same ~70-word "engine group" paragraph in all three tooltips. |
| AUR-P08 | settings/Filters.lua:76 | *Max duration* is in seconds and 0 = no limit, but its label says neither, while its neighbours (*Max auras per group (0 = no limit)*, *Spacing (px)*) do. |
| AUR-P09 | settings/Layout.lua:384-398 vs :415-435 | **Screen mode's point pair is named and ordered differently** from the two attached modes: *Point* / *Relative point* (this container first) vs *Parent container anchor point* / *This container anchor point* and *Named frame anchor point* / *This container anchor point* (target first). Three modes, one concept, two vocabularies and two orders. |
| AUR-P10 | settings/Layout.lua:669-674, :452-482 | **The Anchor tab's facing-growth hint tells the player to fix it "on the Growth tab"**, and Growth's inherited-flow note is about the attachment set on Anchor: the two tabs edit one thing (where the block starts, and which way it runs) and send the player back and forth. |
| AUR-P11 | settings/Layout.lua:355-371 | Tab name *Frame* collides with *Named frame*, *Frame name* and *Pick a frame...* on the next tab; its rows are scale, opacity and draw layer. |
| AUR-P12 | settings/Layout.lua:484-505 | Mouse mixes tooltip rows and click rows with no subsection (options-ui-§7: a tab that mixes subjects carries subsection headings), and *Click-through*, which overrides every other row of the tab, is last. |
| AUR-P13 | settings/Bars.lua:113-135, Icons.lua:68-90 | **In every text tab (Bars Name/Time/Stack, Icons Time/Stack) the *Show* toggle is the 7th row**, under the six font rows it governs. Layout → Label already puts *Show name label* first, so the addon disagrees with itself. |
| AUR-P14 | settings/Bars.lua:124, Icons.lua:79 | Placement's *Anchor* (the text's anchor point) reuses the name of Layout's *Anchor* tab. |
| AUR-P15 | settings/Bars.lua:186-195, Icons.lua:101-110 | **Pandemic → Time color recolors the time text** and owns a threshold no other row reads, while the time text's own font color, format and Show live on the Time text tab. (Note: B2-1 put both pandemic features on one tab on purpose; see AUR-L14's confidence.) |
| AUR-P16 | settings/Bars.lua:6 | Bars has **7 tabs** to the right of a 120px rail; on the rail page that strip wraps to two rows at default scale (options-ui-§13 permits a wrap but asks to keep sections low). |
| AUR-P17 | settings/Icons.lua:25, :32-39 | Icons' first tab is *Size* (3 rows) while Bars and Text open on *General*: three style sections, two shapes for the first tab. |
| AUR-P18 | settings/Icons.lua:64-65, modules/Style_Icons.lua:122-128 | *Blizzard countdown numbers* is a second countdown text, away from Time text and its *Time format*. **But it is drawn by the swipe's Cooldown frame** (`cd:SetHideCountdownNumbers`), and `cd:SetShown(on)` hides that frame when *Show cooldown swipe* is off, so the row only works with the swipe on, and its tooltip does not say so. |
| AUR-P19 | settings/Text.lua:366-419 | **Text → Font holds 19 rows of four subjects**: the font, the glow, *Countdown* (Time format, which is about the template's duration tokens) and *Dispel type* (a backdrop and an edge, which are not font at all). |
| AUR-P20 | settings/Text.lua:459-495 | Text's **Pandemic (4 rows) and Animation (4 rows) are two small tabs about one subject**, motion and emphasis: *Blink in the pandemic window* is on Pandemic, the *Blink* loop is on Animation. |
| AUR-P21 | settings/Text.lua:343-363 | On Text → General the Tokens/Rules cheat sheet (≈15 lines) sits **between** Text Template and Placement, so Placement is pushed below a screen of reference text. |
| AUR-P22 | settings/Text.lua:391-394 | Glow's *Offset X* / *Offset Y* vs *X offset* / *Y offset* everywhere else (Layout, Label, Bars, Icons, Text placement). |
| AUR-P23 | settings/Text.lua:126, General/Filters grid headings | Capitalisation drifts: tabs and subsections are sentence case (*Master controls*, *Background & border*, *Time text*), but *Spell Categories*, *Dispel Colors* (General tabs), *Text Template* (subsection) and the Categories grid headings *Blizzard Categories* / *Spell Categories* / *Dispel Types* / *Who Cast It* are Title Case. |
| AUR-P24 | OptionsSetup.lua:239, Bars.lua:206, Icons.lua:120, Text.lua:510, Containers.lua:159-163 | The style rail entry is *Bar* / *Icon* / *Text*: singular, unlike the Style values *Bars* / *Icons* / *Text*, and unlike Copy settings' *Bar style* / *Icon style* / *Text style*. *Icon* also names a tab inside Bar and Text, so "Icon" means two things on one page. |
| AUR-P25 | Containers.lua:40, :249 | Rail *General* → tab *General*: the strip repeats the rail entry it sits beside (options-ui-§14 names the rail entry; it does not require the tab to repeat it). |
| AUR-P26 | Bars.lua:50, :98, GeneralSpells/GeneralDispel/Filters tooltips | Tooltips say "General -> Dispel Colors" / "General -> Spell Categories" on a page whose own first rail entry and first tabs are also called General; the reference is ambiguous on the Containers page. |
| AUR-P27 | Containers.lua:90 | Style's tooltip says "Bars, Icons and Text each have their own section on this page", which no longer matches the rail labels (P24). |
| AUR-P28 | Layout.lua:361 vs General.lua (composer) | *Opacity* (Layout → Frame) is multiplied by *Master alpha*: one concept, two words (Master alpha is canonical, options-ui-§15). |
| AUR-P29 | Filters.lua:957-969 | Filters tab order after the planned merges must still read left-to-right as "what → which lists → exceptions → when"; today Situations (when) trails Sorting (order), which is the least related neighbour. |
| AUR-P30 | Layout.lua:394-398 | Screen mode's *X* / *Y* are positions; the attached modes' *X offset* / *Y offset* are nudges. The bare *X* / *Y* labels do not say which. |
| AUR-P31 | docs/settings-panel.md:4, :778-780 | Doc drift: 269 rows (276 now), "Four tabs" over a five-tab table, Text "(37 rows)" (44 now). Not a layout fix, but the doc is the owner's map for this preview. |
| AUR-P32 | settings/Layout.lua:669, :674 | The facing-growth hint opens "**Point** is %s…", but it is drawn only in Named frame mode, whose row is called *This container anchor point*: no row named *Point* is on screen when the hint is. |
| AUR-P33 | modules/Anchors.lua:511 | The drag handle's tooltip for an attached container says "Change the anchor points on **Layout > Anchor**." A player-facing string that names a tab, outside `settings/`, so any Layout tab rename must carry it. |
| AUR-P34 | modules/FilterCompiler.lua:181-183, settings/Filters.lua:471, README.md:70, :119 | The Filters intro warnings (`IDS_OWN_DEBUFFS` / `IDS_UNASSISTABLE` / `IDS_ASSISTABLE`, drawn on every Filters tab), the debuff spell-list note and the README all say "**the Situations tab** picks what draws there". They are pinned by tests (test_filterviews.lua:247-251, test_filtercompiler.lua:1054, test_pages_filters.lua:365), so they must move with any change to where those dropdowns live. |
| AUR-P35 | settings/Containers.lua:159-163 | Copy settings' *What to copy* says **Layout**, **Mouse** and **Label** as if they were three equal parts of the Layout rail entry. *Layout* copies `container.layout` only (Scale & strata and Growth rows), never the Anchor tab (position and attach), which the button's tooltip only half says ("Name and position are never copied"). |
| AUR-P36 | settings/Filters.lua:951, Layout.lua:695 | Rail tooltips under-describe their entries: Filters says "Which auras this container shows, and in what order." (nothing about *where it shows at all*, the Situations zone and unit gates); Layout says "Where this container sits, what it attaches to, which way it grows, and how it answers the mouse." (nothing about scale, strata or the name label). |
| AUR-P37 | settings/Filters.lua:102 | The preset dropdown paired beside *Max duration* is labelled only **Preset**, which says nothing about what it presets when read alone. |

## Proposed changes

Every move keeps `path`, default, range, `effect`, `onChange` and `auraTypes`. A row moving between rail
entries changes its `page`, which moves it under a different **Defaults** button; those moves are flagged.

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| AUR-L01 | Retire the General page's **Display** tab: append *Hide Blizzard buffs* and *Hide Blizzard debuffs* to **Master controls** through the composer's `extra` slot (`H.MasterControls{ extra = … }`, General.lua:53), first one with `startsLine`, after *Test mode* and before the reset pair. Drop the *Blizzard frames* subgroup. General page 4 → 3 tabs. **Implementation trap:** General.lua:93-94 writes `row.effect = masterEffect[row.path]` over every composed row, which would nil the extras' `effect = "none"` and make each toggle re-apply every container; the loop must skip paths absent from `masterEffect` (or the map must list both paths as `"none"`). | Both rows are addon-wide display switches, which is exactly what options-ui-§15's `extra` slot is for (its terms: after the set, before the resets, `startsLine`, addon-wide, all met); a 2-row tab costs a click for nothing. | 65% (fallback below) | P01 |
| AUR-L01b | *Fallback if the owner keeps Master controls canonical-only:* rename the tab **Display → Blizzard frames** and drop the now-repeating subgroup. | Says what the tab is; removes a heading that only names the tab. | 85% | P01 |
| AUR-L02 | Merge **Sorting** into Filters → **General**: Cast by, Duration, Max duration + Preset under a new subsection **What to show**, then Sort by, Direction, Max auras per group under **Order and cap**. Filters 5 → 4 tabs. The tab keeps the name *General* (the owner renamed it from *What to show* on 2026-09-20, 6b0bce3), so *What to show* as a subsection does not repeat its tab (options-ui-§7). Overrides' `before = G_SORT` (Filters.lua:966) must become "after Categories", and test_optionssetup.lua:136-144 moves with it. | One tab answers "which auras survive, how many, in what order"; three rows did not earn a tab. | 75% | P02, P29 |
| AUR-L03 | Move the **Where spell lists don't apply** section (unit line, On NPCs / On players or the own-debuffs copy, the honor and timeless notes, or the "always apply" line) from Situations to the **top of Categories**, above *Blizzard Categories*. Replace the Spell Categories NOTE's "(see Situations)" with "(see above)" and the Overrides NOTE's with "(see Categories)". Carries AUR-L29 (the "Situations tab" strings outside the tab). | The choice "every aura, once / only my Blizzard categories set to Show" is about the very grid drawn under it; the player no longer has to leave the tab to read or change it. Costs: Categories is already the longest Filters tab (up to four grids and their notes), and this pushes the grids down by 3-6 lines on the units where the section has dropdowns. | 55% | P03, P04 |
| AUR-L04 | Rename the Situations tab's first heading **Unit type → Which units** (the row under it keeps *Unit type*). Keep the tab name *Situations* and keep it last; Which units stays at the top (the owner moved it there on 2026-10-02, Filters.lua:922-923). | The heading no longer repeats its first row; with L03, what is left (which units, which zones) still reads as "situations". | 60% | P05, P29 |
| AUR-L04b | *Only with L03:* rename **Situations → Conditions**. | Names "when does this container show at all". But *Situations* is the owner's merged feature name (README, smoke tests, diag strings), and it still fits the zones. | 40% | P04 |
| AUR-L05 | Move the **Filter priority logic** block from the foot of General to the **foot of Overrides** (after Blacklist), wording unchanged; Filters.lua:957-959's `afterGroup` moves to the Overrides renderer's tail. | Ranks 1-2 are the Overrides lists and 3-5 the Categories grid next door; General's rows are not ranked. At the foot it is not the "wall above the controls" batch 8 removed. Counter-weight: batch 8 put it at the foot of General **from the owner's screenshots** (624a06b; Filters.lua:378-390 records why: "a footnote to that answer"), so this reverses an owner-reviewed placement. | 45% | P06 |
| AUR-L06 | Shorten the three Sorting tooltips to one sentence each ("…within each engine group; see the note below") and draw the shared engine-group paragraph **once**, as a gray note under *Order and cap*. | One explanation, read once, instead of three copies in three hovers. | 60% | P07 |
| AUR-L07 | Relabel **Max duration → Max duration (s, 0 = no limit)**. | Unit and sentinel visible, as every sibling slider already does. | 70% | P08 |
| AUR-L08 | Screen mode: reorder to **Screen anchor point** (`position.relativePoint`) \| **This container anchor point** (`position.point`), then **X position** \| **Y position**. Rewrite *Point*'s and *Relative point*'s tooltips to the new names ("…measured from the screen anchor point"). | Same order and words as the two attached modes (target first, "This container anchor point" second); positions named as positions. | 70% | P09, P30 |
| AUR-L09 | Merge Layout's **Anchor** and **Growth** tabs into one **Position & growth** tab: Attach to + the mode's subsections + Offset, then a **Growth** subsection (Fill … Line spacing) with the inherited-flow note above it; the facing-growth hint moves under the Growth subsection and says "Set Grow vertically to X below". Layout 5 → 4 tabs. What it takes: `growthIntro`'s `activeTab == G_GROW` gate (Layout.lua:615) becomes a draw above the Growth subsection; the hint, now on the same tab as Grow horizontally / vertically, goes stale after a growth change unless those two rows also request a panel refresh, which is a UI-refresh `onChange`, not a setting change, but it is a new `onChange` and the "every move keeps onChange" rule above has to name it; Layout.lua:386, :435 ("as the Growth tab says"), :669/:674 and Anchors.lua:511 ("Layout > Anchor") are reworded. | The hint and the inherited-flow note both describe the anchor-growth pair; one tab, no switching. 13 rows at most (container mode: Attach to, 3 container rows, 2 offsets, 6 growth) plus notes. | 55% | P10, P33 |
| AUR-L10 | Rename Layout's **Frame** tab → **Scale & strata**. | Names its rows (Opacity and Frame level ride along as the two companions) and stops clashing with *Named frame* / *Frame name*. | 55% | P11 |
| AUR-L11 | Mouse: put **Click-through** first, then subsections **Tooltips** (Show tooltips, Tooltips in combat, Tooltip position) and **Clicks** (Right-click to cancel). | The override first; options-ui-§7 subsections for a tab mixing two subjects. | 60% | P12 |
| AUR-L12 | In every text-element tab (Bars Name/Time/Stack text, Icons Time/Stack text) move **Show** to the first row, alone on its line, ahead of the composed Font block; Placement keeps Justify, Anchor point, X, Y. | The switch above what it switches, as Layout → Label already does. The Font block stays contiguous (options-ui-§16). | 80% | P13 |
| AUR-L13 | Relabel Placement's **Anchor → Anchor point** (Bars, Icons). | No clash with Layout's tab name; matches "…anchor point" on Layout. | 60% | P14 |
| AUR-L15 | Icons: rename **Size → General** and append **Cooldown**'s five rows (Blizzard countdown numbers included) under a *Cooldown* subsection, after Size's rows under *Size*. Icons 6 → 5 tabs. Icons.lua:12-15's S-1 note is rewritten with it. | All three styles open on *General*; Cooldown is the icon's core look and Size alone is 3 rows. The S-1 note's worry (Size landing "arbitrarily") is met by the subsection, but S-1 chose "deliberately not made to match shape-for-shape", so this reverses a recorded decision. | 50% | P17 |
| AUR-L16 | Icons: *Blizzard countdown numbers* tooltip → "Also show the game's own countdown on the icon, as well as the time text. Needs Show cooldown swipe." (text only; no `disabledIf`, which would be new behaviour). | The row does nothing with the swipe off (Style_Icons.lua:122-128), and today nothing says so. | 75% | P18 |
| AUR-L17 | Text: move **Countdown** (Time format) from Font to General → **Text Template**, after the Custom template box and before the Preview. | Time format shapes the template's duration tokens and shows in the Preview right under it. | 65% | P19 |
| AUR-L18 | Text: merge **Pandemic** + **Animation** into one tab **Effects** (subsections *Pandemic window*, *Loop*). Font keeps Font, Glow and Dispel type. Text 5 → 4 tabs. `afterGroup[G_PANDEMIC] = pandemicNote` (Text.lua:510) moves to the Pandemic window subsection's tail. | Both blinks side by side; two 4-row tabs become one 8-row tab. Cost: Bars and Icons keep a *Pandemic* tab (L14 is rejected), so the word survives on Text only as a subsection heading. | 45% | P20 |
| AUR-L19 | Text → General: order **Size** (+ fit note), **Text template** (Template, Custom template, Time format with L17, Preview), **Placement** (+ its two notes), then the Tokens/Rules cheat sheet last under its own subsection **Template reference**. | Controls first, reference text at the tail, so nothing is pushed below a screen of bullets; the template stays next to Size, which *Size to fit* measures from it. (The proposal put the template after Placement, which separated it from the Size rows that follow it.) | 65% | P21 |
| AUR-L20 | Relabel Glow **Offset X / Offset Y → X offset / Y offset**. | One spelling across the addon. | 85% | P22 |
| AUR-L21 | Sentence case: **Spell categories**, **Dispel colors** (tabs), **Text template** (subsection), **Blizzard categories**, **Spell categories**, **Dispel types**, **Who cast it** (grid headings), and every string that quotes them ("General -> Spell categories"). | Every other tab and heading in the addon (and options-ui-§15's *Master controls*) is sentence case. | 60% | P23 |
| AUR-L22 | Rail style entries **Bar / Icon / Text → Bar style / Icon style / Text style** (the labels Copy settings already uses), and Style's tooltip → "…each has its own style section on this page's rail." | One name per thing; frees *Icon* to mean only the icon ornament. Fits 120px rail. | 70% | P24, P27 |
| AUR-L23 | Rail General's one tab **General → Container**. | Stops "General › General"; options-ui-§14 fixes the rail entry's name, not the tab's. See Upstream suggestion U2 if read otherwise. | 45% | P25 |
| AUR-L24 | Every cross-page reference reads **"the General page -> …"** (Bars.lua:50, :98, Filters.lua:358, :632, Text.lua:406, :409, :415; GeneralSpells.lua:797-798 and GeneralDispel.lua:51 say "Filters -> Categories" / "Text -> Font" and change with L03/L18). | Unambiguous on a page whose rail and tabs also say General. | 80% | P26 |
| AUR-L25 | Layout tooltips of *Scale* / *Opacity* keep "Multiplied by Master scale / Master alpha on the General page"; no rename (Master alpha is canonical). Raise the word under U3. | Constrained by options-ui-§15. | 90% (no-op, recorded) | P28 |
| AUR-L26 | Correct `docs/settings-panel.md` counts and the Text tab table with whatever lands, and every other doc that names a moved tab: README.md (:70, :119), docs/known-limitations.md (:300 "Layout > Anchor"), docs/smoke-tests.md, docs/test-cases.md, docs/module-map.md, docs/debug.md. | Doc parity (documentation-§3). | 95% | P31 |
| AUR-L27 | Facing-growth hint "Point is %s and Grow…" → "This container anchor point is %s and Grow…" (Layout.lua:669, :674). | Names the row the player sees in Named frame mode. Independent of L09. | 75% | P32 |
| AUR-L28 | Handle tooltip "Change the anchor points on Layout > Anchor." (Anchors.lua:511) follows whatever the Anchor tab is called after L09 ("Layout > Position & growth"). Build both this string and the hint's "on the Growth tab" from the group constants rather than retyping tab names. | A rename that misses a string outside `settings/` is how P33 would happen. | 90% (with L09) | P33 |
| AUR-L29 | *With L03:* the three `FilterCompiler.lua:181-183` warnings, `SPELL_LIST_DEBUFF_NOTE` (Filters.lua:471) and README.md:70/:119 say "*Where spell lists don't apply*, at the top of the Categories tab, picks what draws there" instead of "The Situations tab picks…"; the pinned test strings move with them. | The warnings sit on every Filters tab and would point at a tab that no longer holds the dropdowns. | 90% (with L03) | P34 |
| AUR-L30 | Copy settings → *What to copy*: **Layout → Layout: scale, strata and growth** (label only; the `layout` key and what it copies stay). | Says which half of the Layout entry it copies; *Mouse* and *Label* already name theirs. | 50% | P35 |
| AUR-L31 | Rail tooltips: Filters → "Which auras this container shows, in what order, and where it shows at all."; Layout → "Its scale and strata, where it sits and what it attaches to, which way it grows, how it answers the mouse, and its name label." | Tooltips that list every tab the entry holds. | 60% | P36 |
| AUR-L32 | Preset dropdown label **Preset → Max duration preset**. | Reads on its own, and says which slider it writes. | 45% | P37 |

### Considered and rejected

| change | why not | confidence |
|---|---|---|
| *Was AUR-L14.* Bars and Icons: move Pandemic's *Time color* rows to Time text (as *Pandemic window*) and *Highlight* to Bars → General / Icons → Cooldown, removing the Pandemic tab (Bars 7 → 6, Icons 6 → 5). | B2-1 put both pandemic features on one tab as **the owner's call** (Bars.lua:180-184); *Highlight the pandemic window*'s tooltip says "the seconds set above do not change it", which stops being true once the threshold is on another tab; Time text would grow to 15 rows. Bars' wrapping strip (P16) stays open and goes to U4. | 35% |
| *Was part of AUR-L18.* Move Text → Font's *Dispel type* subsection to the Effects tab. | Smoke batch 2 item 5 moved it **onto** Font because "they color the text" (Text.lua:401-403): a reversal of a recorded owner pass for a weak gain. | 35% |
| Moving *Show in* / *Which units* to rail General. | They would fall under rail General's Defaults, and Copy settings → Filters would copy rows no longer shown under Filters. | 35% |
| Folding the three Bars text tabs into one. | About 34 rows on one tab, and a rail page cannot carry a secondary strip (options-ui-§13). | 20% |
| Moving Dispel Colors or the spell lists onto the Containers page. | They are profile-wide and shared by every container. | 10% |
| Reordering the rail to General · Filters · Style · Layout. | No gain worth the relearning. | 25% |
| A `disabledIf` on *Blizzard countdown numbers* while the swipe is off. | Dimming is new panel behaviour, outside "layout only"; L16's tooltip says the same thing. | 30% |

## Proposed map

All the accepted changes above at their proposed state (L01 primary, not L01b; L04 without L04b). Tabs after:
General page **3**, rail General **1**, Filters **4**, Layout **4**, Bar style **7**, Icon style **5**, Text style
**4**: at most 3 + 1 + 4 + 4 + 7 = **19 tabs** (from 22). Rows: unchanged, **276**.

```
Ka0s Aura Master (landing)   unchanged

General (page)
  Tab 1  Master controls
    Enable Aura Master | General visibility / Master scale | Master alpha / Lock frame | Debug console /
    Minimap button | Test mode
    Hide Blizzard buffs | Hide Blizzard debuffs          (extra, startsLine)
    [Reset position] | [Reset all settings]
  Tab 2  Spell categories       (unchanged content; "-- Weapon slots --" etc.)
  Tab 3  Dispel colors          (unchanged content)

Containers (page)
  band   Container | [New container]
  rail   General · Filters · Layout · Bar style|Icon style|Text style
  Rail: General
    Tab 1  Container
      Name | Enabled / -- What it shows, and how -- Unit | Aura type / Style
      [Duplicate] | [Delete] / -- Copy settings from -- Source | What to copy / [Copy onto this container]
  Rail: Filters
    Tab 1  General
      -- What to show --   Cast by | Duration / Max duration (s, 0 = no limit) | Max duration preset
      -- Order and cap --  Sort by | Direction / Max auras per group (0 = no limit) · engine-group note
    Tab 2  Categories
      -- Where spell lists don't apply --  unit line · On NPCs | On players (or the own-debuffs row) · honor/timeless notes
      -- Blizzard categories --  bulk pair · grid
      -- Spell categories --     NOTE (see above) · bulk pair · lists line · grid · tie + Hide enchants without a duration · notes
      -- Dispel types --  -- Who cast it --
    Tab 3  Overrides
      NOTE (see Categories) · -- Whitelist -- · -- Blacklist -- · -- Filter priority logic -- (5 ranks)
    Tab 4  Situations
      -- Which units --  Unit type | Reaction  (or "Always your own character or pet.")
      -- Show in --      Open world | Dungeons / Scenarios and delves | Raids / Battlegrounds | Arenas
  Rail: Layout
    Tab 1  Scale & strata   Scale | Opacity / Strata | Frame level
    Tab 2  Position & growth   (handle tooltip: "…on Layout > Position & growth")
      Attach to
      -- Screen --             Screen anchor point | This container anchor point / X position | Y position
      -- Another container --  Parent container | join line / Parent container anchor point | This container anchor point
      -- Named frame --        Frame name | [Pick a frame...] / Named frame anchor point | This container anchor point
      -- Offset --             X offset | Y offset
      -- Growth --             (inherited-flow note) Fill | Per row or column (0 = one line) / Grow horizontally | Grow vertically /
                               Spacing (px) | Line spacing (px) · facing-growth hint ("This container anchor point is …
                               Set Grow vertically to X below")
    Tab 3  Mouse     Click-through / -- Tooltips -- Show tooltips | Tooltips in combat / Tooltip position / -- Clicks -- Right-click to cancel
    Tab 4  Label     unchanged
  Rail: Bar style
    Tab 1  General   -- Size -- · -- Fill -- · -- Spark --   (unchanged)
    Tab 2  Background & border   unchanged
    Tab 3  Name text   Show / -- Font -- 6 / -- Placement -- Justify | Anchor point / X offset | Y offset
    Tab 4  Time text   Show / -- Font -- / -- Placement -- / -- Countdown -- Time format
    Tab 5  Stack text  as Name text
    Tab 6  Icon        unchanged
    Tab 7  Pandemic    unchanged (L14 rejected)
  Rail: Icon style
    Tab 1  General     -- Size -- Width | Height / Icon zoom · -- Cooldown -- Show cooldown swipe | Reverse the swipe /
                       Draw the swipe's edge | Swipe darkness / Blizzard countdown numbers ("…Needs Show cooldown swipe.")
    Tab 2  Border      unchanged
    Tab 3  Time text   Show / -- Font -- / -- Placement -- / -- Countdown -- Time format
    Tab 4  Stack text  Show / -- Font -- / -- Placement --
    Tab 5  Pandemic    unchanged (L14 rejected)
  Rail: Text style
    Tab 1  General     -- Size -- (+ fit note) · -- Text template -- Template / Custom template / Time format / Preview ·
                       -- Placement -- (+ notes) · -- Template reference -- Tokens · Rules
    Tab 2  Font (18)   -- Font -- 6 · -- Glow -- Glow behind the text | Glow color / Use class color | Intensity /
                       Thickness (px) | X offset / Y offset · -- Dispel type -- Color the dispel type /
                       Backdrop in the dispel color | Backdrop opacity / Edge in the dispel color | Edge thickness (px)
    Tab 3  Icon        unchanged
    Tab 4  Effects     -- Pandemic window -- Recolor… | Pandemic window (seconds left) / Pandemic-window time color | Blink in the pandemic window
                       (pandemic note when the template has no duration token)
                       -- Loop -- Effect | Seconds per cycle / Faded to | Bounce height (px)

Profiles   unchanged
```

## Cross-addon notes

- **A text element's tab opens with its Show toggle** (L12): the same rule wherever a tab carries one text
  element's font + placement (MultiMeters, AbsorbTracker, PartyFrameEnhanced and the like). Worth one sweep.
- **Offsets are spelled *X offset* / *Y offset*** and positions *X position* / *Y position* in every addon.
- **Sentence case for every tab, subsection and grid heading** (L21); the standard's own canonical names
  are already sentence case.
- **A cross-page reference names the page** ("the General page -> Dispel colors") wherever an addon also
  has a General tab or rail entry.
- **Strata and Frame level** live on a per-instance *Scale & strata* (or equivalent) tab; any addon that
  exposes a strata choice should place and name it the same way, and its value list should match (see the
  strata file's AUR-S01).
- **Pandemic window** naming (time color, highlight, blink) should match any other Ka0s addon that colors
  an expiring timer.
- **A string that names a tab is built from the tab's group constant**, never retyped (AUR-L28): AuraMaster has
  player-facing tab names in `modules/` (Anchors.lua:511, FilterCompiler.lua:181-183) that a settings-only rename
  sweep would miss. Every addon renaming tabs in item 020 should grep `modules/` and `core/` too, not only
  `settings/`.
- **Copy-from labels name what is copied** (AUR-L30) wherever an addon offers a per-section copy.
- AuraMaster has **no Keybindings tab** (no primary window); the 7 window addons' new General → Keybindings
  tab does not need an AuraMaster counterpart.

## Upstream suggestions

- **U1 (options-ui-§15):** let a multi-instance addon's *Lock frame* read *Lock frames* (or allow a plural
  form): AuraMaster locks every container at once.
- **U2 (options-ui-§13/§14):** say explicitly whether a rail entry's tabs may be named independently of the
  entry. A one-tab rail entry that must repeat its own name ("General › General") is the shape AUR-P25
  complains about.
- **U3 (options-ui-§15):** the canonical *Master alpha* is the only place the collection says "alpha" to a
  player; per-instance rows say *Opacity*. Consider *Master opacity*, or a note that per-instance rows use
  *Opacity*.
- **U4 (options-ui-§13):** a rail page's strip is ~120px narrower than a plain page's; recommend a lower tab
  ceiling (5-6) for rail entries so the strip does not wrap at default scale.
- **U5 (options-ui-§14 / deep links):** a link that jumps pages (Filters' *See spells*) should offer a way
  back; today the player has to re-open Containers and find their rail entry and tab. A library-level "back"
  affordance would serve every addon with such links.

## Review

Independent review, 2026-10-24, against `../AuraMaster` at `c77c7fc` (master, clean): every page, tab and
section builder in `settings/`, the `MasterControls` composer and `appendExtra` in the vendored
`libs/LibKa0s/OptionsCompose.lua`, `modules/Style_Icons.lua`, `modules/Anchors.lua`, `modules/FilterCompiler.lua`,
`options-ui.md` §7, §13, §14 and §15, and the git history behind the placements this file proposes to move.

**Map and inventory corrections.**
- Filters' category rows: 19 per aura type (Weapon enchants and Uncategorized included), not "17 buff / 19
  debuff". The proposal's own 36 / 35 per-type totals only add up with 19 on each.
- Text → Font has **19** rows (6 font + 7 glow + 1 countdown + 5 dispel), not 18 (P19).
- Annotated three things the map left out because later changes depend on them: Blizzard countdown numbers
  is drawn by the swipe's Cooldown frame; the facing-growth hint is redrawn only by `attach.point`; the
  inherited-flow note is gated on `activeTab == Growth`.

**New problems found (P32-P37).** The facing-growth hint names a *Point* row that Named frame mode does not
have. There are player-facing tab names outside `settings/`: the drag-handle tooltip's "Layout > Anchor",
and the Filters warnings' "the Situations tab", which tests pin. Copy settings' *Layout* option copies less
than the Layout rail entry holds. Two rail tooltips under-describe their entries. The *Preset* label is
vague. New changes L27-L32 cover them.

**Changes that would have broken behaviour or rested on a wrong premise.**
- L01: General.lua:93-94 overwrites `effect` on every composed row, so the extras would lose
  `effect = "none"` and re-apply every container on each toggle. Added the trap and its fix.
- L16 (old): moving *Blizzard countdown numbers* to Time text would separate it from the switch it depends
  on (`cd:SetShown(on)` hides the numbers with the swipe). Struck, and replaced by a tooltip-only fix (75%).
- L09: the merged tab needs Grow horizontally / vertically to request a panel refresh, or the hint goes
  stale. That is a new UI-only `onChange`, which the "every move keeps onChange" rule has to name. Also
  listed the four strings that name the old tabs.
- L19: reordered so the template stays next to *Size to fit*, which measures from it. The cheat sheet still
  goes last.

**Recalibrated against owner decisions found in history and comments.**
- L05 is down 55 to 45. Batch 8 placed the priority block from the owner's screenshots (624a06b).
- L14 is down 40 to 35 and rejected. B2-1 was the owner's call, and the Highlight tooltip's "set above"
  would break.
- L15 is down 55 to 50. S-1 recorded that it chose not to match the two styles' tab shapes.
- L18 is down 55 to 45. *Dispel type* stays on Font, because smoke batch 2 item 5 put it there.
- L04 now renames only the heading. The *Situations* to *Conditions* rename is split off as L04b at 40%,
  because *Situations* is the owner's feature name.
- L03 is down 65 to 55, because it makes the Categories tab longer.
- L08 is down 75 to 70.
- L09 is down 65 to 55.

**Standard checks.** L01 meets every term of options-ui-§15's `extra` bullet. L02's *What to show*
subsection does not repeat its tab (§7), and the tab keeps the owner's 2026-09-20 name *General*. L23 is
allowed, because §14 fixes the rail entry's name, not its tab's. No proposed change alters a key, default,
range or `effect`.

**Proposed map** updated to match: 19 tabs at most, from 22 (the proposal said 18, but that counted L14).
Bar style keeps 7 tabs and Icon style keeps its Pandemic tab. Considered and rejected is now a table. Added
two cross-addon notes: build tab-naming strings from group constants, and copy labels name what is copied.
