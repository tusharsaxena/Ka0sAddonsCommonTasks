# PrettyChat — settings layout analysis

Item 020. Read-only analysis of `../PrettyChat` at `master` (`b08c579`, v1.7.0; LibKa0s vendored at `libs/LibKa0s/`).
Sources read: `settings/Panel.lua`, `settings/OptionsSetup.lua`, `settings/Schema.lua`, `settings/Profiles.lua`,
`defaults/Defaults.lua`, `locales/enUS.lua`, `modules/Override.lua` (`NS.SortedStringNames`),
`libs/LibKa0s/OptionsCompose.lua` (`MasterControls`), `libs/LibKa0s/OptionsWidgets.lua` (flow engine),
`libs/LibKa0s/Options.lua` (`SetRenderer`, refresh tiers), `libs/AceGUI-3.0/widgets/AceGUIContainer-TreeGroup.lua`,
`docs/settings-panel.md`, and `WowAddonStandards/standards/standards/options-ui.md` §5/§6/§7/§13/§15.

**Keybindings (item 015) does not touch this addon.** PrettyChat is frameless (no primary window, no
`Bindings.xml`), so it is not one of the seven addons that gain a General > Keybindings tab. Its General page
stays a single `Master controls` tab.

**Terminology.** In this file *sidebar* means Blizzard's Settings left-hand category list (the entries
`RegisterCanvasLayoutSubcategory` creates). PrettyChat has **no** LibKa0s nav rail (`O.NavRail`, options-ui-§13);
`settings/OptionsSetup.lua:138` only stubs it for the degraded path.

## Current map

On-screen order. `[a] [b]` is one two-column line from the flow engine; `(—)` is an empty cell.
Widget types: chk = CheckBox, dd = Dropdown, btn = Button, eb = EditBox, lbl = Label, tree = AceGUI TreeGroup.

```
Ka0s Pretty Chat  (landing; parent canvas)            Panel.lua:715-721, 794 (H.BuildLandingPage)
  logo · tagline (TOC Notes "Prettier chat messages")
  Section "Slash Commands"
    lbl  "/prettychat is an alias for /pc"            Panel.lua:708
    lbl  one row per COMMANDS entry (LandingRows)     Panel.lua:709-711

General  (sub-page 1; sidebar + title are the literal "General")   Panel.lua:736-752; body Panel.lua:150-159
  header Defaults btn -> ConfirmResetAll (same act as Reset all settings)  Panel.lua:739-749
  Tab "Master controls"   (composed, H.MasterControls; Schema.lua:123-196, OptionsCompose.lua:466-566)
    line 1  [chk Enable PrettyChat            General.enabled]
            [dd  General visibility           General.visibility]  (Always / Only in combat / Only out of combat / Never)
    line 2  [chk Debug console                state.debugConsole (session)]  (—)
    line 3  [chk Minimap button               global.minimap.shown]          (—)
    line 4  [btn Test]  [btn Reset all settings]   (InlineButtonPair; Test = leadButton, Schema.lua:191-195)

Categories  (sub-page 2)                               Panel.lua:754-791; body Panel.lua:617-661
  header Defaults btn -> ConfirmResetCategories (all 8 tabs); the Settings
         window's own footer Defaults resets directly (already confirmed)   Panel.lua:781-787
  Tab strip: Loot | Currency | Money | Reputation | Experience | Honor | Tradeskill | Misc   Panel.lua:635-648
             (label = the raw category key; no per-tab tooltip)
  (each tab, identical shape)
    lbl  gray footnote "Strings on these tabs are rewritten only while the master
         Enable on the General page is on." (always drawn)  Panel.lua:655-658
    chk  "Enable <Category>" full width              <Cat>.enabled            Panel.lua:463
    tree (200px list | editor pane)                  Panel.lua:482-516
      list pane: one entry per string, sorted by GLOBALNAME (NS.SortedStringNames, Override.lua:33-44),
                 entry text = friendly label (Defaults.lua);
                 hover = AceGUI's built-in tooltip repeating the label text (TreeGroup OnAcquire
                 EnableButtonTooltips(true), AceGUIContainer-TreeGroup.lua:200-209, 292)
      editor pane (selected string only)             Panel.lua:242-348
        [chk Enable  <Cat>.<G>.enabled  30%] [lbl GLOBALNAME gray 70%]
             (Enable greyed while Enable PrettyChat or Enable <Cat> is off, Panel.lua:338)
        eb  Original (disabled)  - read-only snapshot, no key; a disabled AceGUI EditBox, so its
                                   text cannot be selected or copied
        eb  New                  <Cat>.<G>.format   (commits on Enter; greyed while the string,
                                   its category or the addon is off, Panel.lua:340)
        eb  Preview (disabled)   - NS.RenderSample of the stored (New) format, no key
        btn Reset (40%)          -> ResetString (both keys)

Profiles  (sub-page 3)                                 Profiles.lua:72-115
  AceDBOptions table drawn by AceConfigDialog into a Fill SimpleGroup parented to ctx.body (not a scroll);
  no Defaults button, no strip (§13 exemption)
```

List-pane order as shipped (sorted by GLOBALNAME, shown by label). Verified against `defaults/Defaults.lua`
by loading it and sorting each category's keys.

| Tab | n | Entries in on-screen order |
|---|---|---|
| Loot | 17 | Battle Pet Loot · Currency Refund · Disenchant Credit · Item Looted (Other) · Bonus Roll (Other) · Bonus Roll Multiple (Other) · Bonus Roll (Self) · Bonus Roll Multiple (Self) · Item Looted Multiple (Other) · Item Pushed (Other) · Item Pushed Multiple (Other) · Item Pushed (Self) · Item Pushed Multiple (Self) · Item Refund · Item Refund Multiple · Item Looted (Self) · Item Looted Multiple (Self) |
| Currency | 4 | Currency Gained · Currency Gained Multiple · Currency Gained Multiple (Bonus) · Currency Lost (Death) |
| Money | 8 | Quest Reward Money · Generic Money Gained · Money Looted (Other) · Money Refund · Money Split · Money Looted (Self) · Money Looted (Guild Bank) · Money Looted (Modifier) |
| Reputation | 14 | Standing Changed · Standing Changed (Guild) · Standing Changed (Guild Name) · Standing Decreased · Standing Decreased (Generic) · Standing Increased · (Achievement Bonus) · (Achievement Part) · (RAF Bonus) · (Double Bonus) · (Generic) · (Guardian) · (RAF Part) · (Rested Part) |
| Experience | 20 | XP Gain (Rested) ×solo/Group/Raid · (Normal) ×3 · (Tired) ×3 · (Exhausted) ×3 · (First Person) ×3 · (Unnamed) ×3 · XP Gain (Quest) · XP Loss (Unnamed) |
| Honor | 6 | Dishonorable Kill · Honor Award · Honor Gain · Honor Gain (Rested) · Honor Gain (No Rank) · Honor Gain (No Rank, Rested) |
| Tradeskill | 8 | Created Item (Other) · Created Item Multiple (Other) · Created Item (Self) · Created Item Multiple (Self) · Open Lock (Other) · Open Lock (Self) · Tradeskill Log (Self) · Tradeskill Log (Other) |
| Misc | 2 | Quest Reward XP · Zone Explored XP |

**Counts.** Pages: 4 (landing + 3 sub-pages). Tabs: 9 (General 1, Categories 8; Profiles and the landing
page carry no strip). Schema rows: 170 (General 4; Categories 166 = 8 category toggles + 79 strings × 2).
Controls on screen at once: General 4 rows + 2 buttons; a Categories tab shows 1 footnote + 1 toggle + a
list of 2–20 entries + one 6-widget editor.

**Refresh facts that constrain the proposals below.** A page body renders once and is not redrawn on
`OnShow` unless marked dirty (Options.lua:1109-1127). A value write runs `RefreshScalars` plus the visible
tab's `Schema.refreshers` closure (Schema.lua:968-989), and that closure re-syncs only the six editor widgets
(Panel.lua:331-347, 558-563). It does **not** re-run `tree:SetTree`, redraw the footnote or redraw the tab
strip. Anything below that makes the list, the footnote or a tab label state-dependent needs new plumbing:
either the closure also calls `SetTree`/`RefreshTree`, or the write triggers a structural refresh
(`H.RefreshPanel(ctx, true)`).

## Problems

| id | Where | Problem |
|---|---|---|
| PRC-P01 | Override.lua:33-44, Panel.lua:403-409, 468 | **The string list is sorted by the hidden GLOBALNAME but shows the friendly label**, so it reads as unsorted. Loot puts *Item Looted (Other)* 4th and *Item Looted (Self)* 16th, with *Bonus Roll* and *Item Pushed* between them; Money opens on *Quest Reward Money*; Tradeskill lists *Created Item (Other)* before *(Self)* but *Tradeskill Log (Self)* before *(Other)*; Reputation splits the two RAF entries (9th, 13th). The one task the page is for, finding a message, means scanning the whole list. The worst problem in the addon's settings. |
| PRC-P02 | Panel.lua:403-409 | The list gives no sign of state. A disabled string and a customised string look the same as an untouched one, so finding "what did I change?" or "what is switched off?" means clicking every entry in every tab, up to 79 clicks. |
| PRC-P03 | Defaults.lua (labels) | Label grammar is inconsistent, so siblings do not sit together even when sorted by label. *Generic Money Gained* (adjective first) against *Standing Decreased (Generic)* (qualifier in parentheses); *Quest Reward Money* (Money tab), *Quest Reward XP* (Misc tab) and *XP Gain (Quest)* (Experience tab) use three patterns for one concept; *Item Refund Multiple* has no parenthesised qualifier where its siblings do; *Bonus Roll Multiple (Self)* puts "Multiple" before the qualifier while *Currency Gained Multiple (Bonus)* treats "Multiple" as part of the noun. |
| PRC-P04 | Defaults.lua (Experience labels) | Jargon labels. *XP Gain (First Person)* is Blizzard's global-name word for a kill with no rest bonus ("%s dies, you gain %d experience."). *XP Gain (Unnamed)* is XP with no named source ("You gain %d experience."). A player cannot tell from the label which chat line either one is. |
| PRC-P05 | Panel.lua:655-657, locales/enUS.lua:49 | The footnote says "the master **Enable** on the General page", but that control is labelled **Enable PrettyChat**, so it names a control by a word that does not appear on it. It also leaves out **General visibility**: *Never* and the two combat modes stop rewriting too (`ApplyStrings` gates on `IsVisible()`, Override.lua:332-342), so a player with visibility on *Only in combat* who edits a string out of combat sees nothing happen and the footnote does not say why. |
| PRC-P06 | Panel.lua:655 | The footnote is drawn on every tab on every render, even when both master gates are open. A permanent gray sentence above every tab soon goes unread, so it is not read on the day it applies. |
| PRC-P07 | Panel.lua:258-259, 284-285, 295-296, 303-304 | Tooltip titles do not match the widget labels: *Original* has the tooltip title *Original Format String* and *New* has *New Format String*, while *Preview* matches. Two names for one control (the addon's own rule, Panel.lua:171-173, which borrows options-ui-§7's "same label twice" reasoning). |
| PRC-P08 | Schema.lua:409-410, Panel.lua:259, 296 | One thing has three names. The category tooltip says "string **overrides**", the per-string tooltip says "the **rewritten** format", and the New box tooltip says "Your **replacement**". The page footnote says "rewritten". |
| PRC-P09 | Panel.lua:252 | The per-string checkbox label is a bare **Enable**, directly under the full-width **Enable Loot** toggle. Two "Enable" checkboxes stacked in one pane, one governing all 17 strings and one governing a single string, are told apart only by position. |
| PRC-P10 | Panel.lua:637, Schema.lua:18-22 | Tab labels are the raw path segments. **Misc** is an abbreviation, and it holds two **XP** messages (quest reward XP, exploration XP) that a player looks for under **Experience**. They cannot move there: the row keys are `Misc.*`, and *Enable Experience* would not govern them. **Tradeskill** is the pre-Dragonflight term; the client now says *Professions*. |
| PRC-P11 | Panel.lua:635-638 | Tabs carry no tooltip, though `H.TabStrip` takes one per tab (`tab.tooltip`, OptionsTabs.lua:761). The "what each tab covers" sentences exist only in `docs/settings-panel.md` (lines ~112-119), and the cross-tab oddities are discoverable only by clicking around: *Currency Refund* is under **Loot**, not **Currency**, and *Created Item (Self)* is under **Tradeskill**, not **Loot**. |
| PRC-P12 | Panel.lua:635-648 | A tab label does not show whether the category is on. With **Enable Money** off, the strip looks the same as with it on, so a full check of the eight category switches means eight tab clicks. |
| PRC-P13 | Schema.lua:191-195, Panel.lua:130-134 | **Test** (one report for all eight categories) lives on General, while everything it reports on is edited on Categories. Checking one category means leaving the page, clicking Test and reading a few hundred lines in the console. `TestToConsole(filter)` already takes `{kind="category", value=...}` (`/pc test category` uses it, Slash.lua:610), but nothing on the Categories page reaches it. |
| PRC-P14 | OptionsCompose.lua:487-501 | The General tab draws **two half-empty lines**, `[Debug console] (—)` and `[Minimap button] (—)`. A frameless addon loses *Lock frame*, so *Debug console* falls to column 1, and *Minimap button* is forced onto a new line by `startsLine`. Fixed element: options-ui-§15 fixes the order and puts *Minimap button* in column 1. See Upstream suggestions. |
| PRC-P15 | OptionsCompose.lua:471-475 | The *General visibility* tooltip is "When this addon's display is shown at all." PrettyChat has no display, and here the setting means *when chat messages are rewritten*. The composer lets a host override `labels` but not tooltips (`emit`, OptionsCompose.lua:156-175). The host could mutate the returned row in `Schema.InstallMasterControls` (Schema.lua:885-905, which already sets `kind`/`get`/`set` on it), but that is a per-addon edit of composed wording, which is the drift §15 exists to stop. Fixed element; see Upstream suggestions. |
| PRC-P16 | Panel.lua:739-749 vs Schema.lua:180 | General has two buttons for one act: the header **Defaults** and the in-body **Reset all settings** both run ConfirmResetAll. Fixed by options-ui-§5 (every sub-page has Defaults) and §12 (General's Defaults is the global reset). Recorded, not changed. |
| PRC-P17 | Panel.lua:460-464 | The category toggle is full width and alone on its line, with nothing in its right half, while the tab has no per-category act. The empty half is where a per-tab act (PRC-P13) fits without adding a line. |
| PRC-P18 | Panel.lua:271-305 | The editor's **Original** box shows the raw, pipe-doubled format string, while **Preview** shows the rendered sample of the **New** string. Nothing renders the original, so "before/after" compares a raw string with a rendered one. Layout only: the order Original, New, Preview puts the rendered line two rows away from the raw original it would be compared with. |
| PRC-P19 | Panel.lua:316 | The per-string button says **Reset**, while the page-level buttons say **Defaults** and **Reset all settings**. A bare *Reset* next to *Preview* can be read as "reset the preview". |
| PRC-P20 | Panel.lua:736-737, 751 vs 755, 790 | The General page title and sidebar name are the literal `"General"`, while Categories and Profiles go through `L[...]`. This is a localisation inconsistency on fixed chrome, not a layout change, fixed by PRC-L15. |
| PRC-P21 | Panel.lua:755, 790 | **Categories** is a meta name. What the page edits is chat messages; "categories" names how they are grouped. The sidebar reads *General · Categories · Profiles*, and a new player has to open the page to learn that it is where messages are rewritten. |
| PRC-P22 | docs/settings-panel.md:123 | Doc wording found while mapping: the "Why a list" paragraph says "Experience is twenty, Loot is nineteen". It describes the page's history, and Loot *was* 19 before migration v2 moved `LOOT_ITEM_CREATED_SELF[_MULTIPLE]` to Tradeskill (Schema.lua:495-499), but the present tense reads as today's count (17). Not a layout change; listed so the doc pass picks it up. |
| PRC-P23 | Override.lua:22-27 | *(review)* **One ordering rule.** `NS.SortedStringNames` is documented as the ONE place string order is decided (PRETTYCHAT-R-09), so that `ApplyStrings`, `/pc list`, `/pc test`, the schema build and the panel all walk the same order. A display-only order in Panel.lua, which is what PRC-L01 first proposed, would make the panel list disagree with `/pc list` and the `/pc test` report, and add a second order to keep in step. |
| PRC-P24 | AceGUIContainer-TreeGroup.lua:200-209, 292 | *(review)* The list already has a hover tooltip, AceGUI's default, and it only repeats the entry's label. The tooltip slot carries no information today. |
| PRC-P25 | Panel.lua:262-268, 271-286 | *(review)* The **GLOBALNAME** caption is an AceGUI Label, and the **Original** box is a *disabled* EditBox. Neither can be selected or copied. The comment at Panel.lua:262-264 says the GLOBALNAME is "the one identifier on this pane a player has to be able to copy out of it", and the natural edit flow (copy Blizzard's original into New, then change it) is impossible. This is widget behaviour, not layout. Recorded under *Considered and rejected* as a follow-up issue. |
| PRC-P26 | Schema.lua:354, locales/enUS.lua:84 | *(review)* The blank-format refusal says "Use **Reset** to restore the default." It names the per-string button by its label, so renaming that button (PRC-L14) without this message would leave a chat line naming a control that no longer exists. |
| PRC-P27 | Schema.lua:191-195 | *(review)* The one-shot report button is labelled **Test**. Elsewhere in the collection §15's **Test mode** is a session toggle that shows placeholder content. PrettyChat's button is a report written to the console, and a bare *Test* beside *Reset all settings* says neither what it tests nor where the output goes. The tooltip explains it; the label does not. |
| PRC-P28 | Panel.lua:224-229 | *(review)* The editor's tick/caption split (0.3 / 0.7) is sized on the comment's premise that "the tick's label is one word". Any longer per-string label (PRC-L08) needs the split changed or it wraps under a 200px tree in a ~600px pane. |

## Proposed changes

None of these changes a setting key, default, range or behaviour, or adds or removes a setting. Order,
labels, tooltips, list text colouring and the per-tab Test button are display or act changes. PRC-L01 now
changes the *order* of `NS.SortedStringNames` (see P23). That reorders the `/pc list` and `/pc test` output
and the in-memory schema row order, and it changes no stored value. The `_G` writes `ApplyStrings` makes are
independent of walk order because duplicate globals are refused at load (Schema.lua:495-513).

| id | Change | Reason | Confidence | Fixes |
|---|---|---|---|---|
| PRC-L01 | Give the strings a **curated order at the single source**. Add a display rank to each `NS.Defaults[cat].strings[G]` entry (e.g. `order = n`, data only, no SavedVariables key), and have `NS.SortedStringNames` sort by `(order, GLOBALNAME)`, with an entry missing `order` falling back to GLOBALNAME after the ranked ones, so a new default can never vanish. The panel list, the first auto-selected string, `/pc list`, `/pc test` and the schema walk then share one order (PRETTYCHAT-R-09 kept). The rule is **kind → Self before Other → single before Multiple**, with odd ones last. Exact orders are in *Proposed map*. `tests/` assertions that pin alphabetical order move with it. | The list is the page's selector. Today its order is one the player cannot see, the global name. Siblings (Self/Other, single/Multiple) belong side by side, and one order everywhere is the addon's own rule. | 85% | P01, P23 |
| PRC-L02 | **Mark state in the list text.** A disabled string's entry text is wrapped in a gray color escape. A string whose format differs from its default gets a trailing gold `*`. A category that is off grays the whole list. Implementation notes from the review: use the color escape in `text` **only**, never TreeGroup's `disabled` field, which calls `EnableMouse(false)` and makes the entry unclickable (AceGUIContainer-TreeGroup.lua:85-88). The existing refresher does **not** re-run `SetTree` (see *Refresh facts*), so the category closure must also call `tree:SetTree(stringTree(...))` or `RefreshTree()`. The legend goes into the category toggle's tooltip (PRC-L07). | Lets a player answer "what did I change / what is off" at a glance, not by clicking 79 entries. | 70% | P02 |
| PRC-L03 | Relabel for one grammar, **noun first, qualifier in parentheses** (Defaults.lua `label` fields only): *Generic Money Gained* → **Money Gained (Generic)**; *Quest Reward Money* → **Money Gained (Quest Reward)**; *Item Refund Multiple* → **Item Refund (Multiple)**. Leave *Quest Reward XP* and *XP Gain (Quest)*, because they are different Blizzard lines ("Experience gained: %d." / "You gain %d experience. (…bonus)"), but see L04 and L09 for their tooltips and tab. A label is a display string: the path is `Money.GENERIC_MONEY_GAINED_RECEIPT.format` either way, and no test or doc outside `defaults/Defaults.lua` names these three labels (checked by grep). | Siblings then sort and scan together, and one concept reads one way. | 65% | P03 |
| PRC-L04 | Clarify the jargon labels: *XP Gain (First Person)* → **XP Gain (Kill, No Bonus)** (×3 with ", Group" / ", Raid"); *XP Gain (Unnamed)* → **XP Gain (No Source)** (×3); *XP Loss (Unnamed)* → **XP Loss**. **Replace** the list's built-in label-only tooltip with a useful one: `tree:EnableButtonTooltips(false)`, then draw on `OnButtonEnter`/`OnButtonLeave` with the label as title, the GLOBALNAME as a gray second line, and the Blizzard original **rendered** through `NS.RenderSample(NS.OriginalFormat(...))` as the body, so the tooltip shows the chat line as the game prints it. Use `AceGUI.tooltip` (what the built-in uses) or GameTooltip, but not both. With the built-in left on, two tooltips draw. | The label then says which chat line it is, and the hover answers the rest without a click. The rendered original also gives the before half of before/after that P18 lacks. | 60% (labels) / 80% (tooltip) | P04, P11, P18, P24 |
| PRC-L05 | Reword the footnote (Panel.lua:656, locales/enUS.lua:49) to name the gate that is actually closed. Addon off: "**PrettyChat is off (*Enable PrettyChat*, General page), so no message is rewritten.**" Visibility not *Always*: "***General visibility* (General page) is *%s*, so messages are rewritten only then.**" (*Never*: "…is *Never*, so no message is rewritten.") | Names the control by its on-screen label, and adds the second gate that today goes unexplained. A sentence for the gate that is closed beats one sentence that lists both. | 80% | P05 |
| PRC-L06 | Draw the footnote **only when a gate is closed** (`not IsAddonEnabled()` or visibility ≠ `always`), in the warning color, not gray. Plumbing (review): this page renders once and its refresher redraws no label (see *Refresh facts*), so a `General.enabled` / `General.visibility` write must mark the Categories page for a structural refresh (`H.RefreshPanel(ctx, true)`, or a dirty flag the next `OnShow` honours). `fitTree` already measures the height above the tree (Panel.lua:428-446), so the tree resizes itself when the line comes and goes. | A notice that is always there goes unread. One that appears when it matters gets read, and it appears exactly when the per-string controls are greyed (addon off), which is when a player needs the reason. | 55% | P06 |
| PRC-L07 | Unify the vocabulary on **"rewrite"**. Category tooltip (Schema.lua:410): "**Rewrite %s messages. When off, every %s message uses Blizzard's original wording, whatever the switches below say. In the list, gray = off, \* = changed from default.**" Per-string tooltip (Panel.lua:259): "**Rewrite this message. When off, Blizzard's original wording is used.**" New box tooltip (Panel.lua:296): "**Your rewritten format. Type `\|\|` for a literal `\|` (color codes use this).**" The legend sentence ships only together with PRC-L02. | Removes the three-word drift and puts the list legend somewhere discoverable. | 75% | P08, P02 |
| PRC-L08 | Rename the per-string checkbox **Enable** → **Rewrite this message**, and rebalance the editor's first line from `TICK_W 0.3 / CAPTION_W 0.7` to **0.5 / 0.5** (layout constants, Panel.lua:228-229) so the longer label does not wrap. The longest GLOBALNAME, `COMBATLOG_XPGAIN_FIRSTPERSON_UNNAMED_GROUP`, still fits half a ~600px pane in the gray caption font, but check it in-client. Make the tooltip titles **equal to the widget labels** (*Original Format String* → *Original*; *New Format String* → *New*). | Separates the per-string switch from the per-category *Enable Loot* above it, and removes the second names. | 55% (rename + rebalance) / 85% (titles) | P07, P09, P28 |
| PRC-L09 | Add **tab tooltips** (`tabs[i].tooltip`, Panel.lua:637) using the doc's *Covers* sentences, plus the cross-tab pointers. **Loot**: "Item pickups, your own and group loot, bonus rolls, refunds. Crafted items are under Tradeskill." **Currency**: "Currency gained and lost. Currency refunds are under Loot." **Money**: "Gold looted, split, refunded or rewarded." **Reputation**: "Faction standing going up and down." **Experience**: "XP from kills and quests, by rest state, solo, group or raid. Quest-reward and exploration XP lines are under Misc." **Honor**: "Honor you earn." **Tradeskill**: "Professions: crafting (yours and others') and opening locks." **Misc**: "Quest-reward XP and zone exploration XP." | The tab's subject and its oddities, available on hover with no clicking. This is the least invasive answer to P10/P11, given that rows cannot change tabs, and it is how the client's term *Professions* reaches the player without renaming the CLI-visible tab (see the rejected L10). | 80% | P10, P11 |
| PRC-L11 | Gray the **tab label** of a category whose `<Cat>.enabled` is off (a color escape in the label). Review notes: the escape overrides the strip's own selected-tab font color, so a selected disabled tab reads as unselected, and the escape must not reach the strip's width measurement or the wrap invariant (options-ui-§13; escapes have no width, but pin it). The strip redraws only on a structural render, so a `<Cat>.enabled` write must trigger one. | Category state across all eight tabs at a glance, with no clicks. | 45% | P12 |
| PRC-L12 | Put a **Test this category** button in the empty right half of the *Enable \<Category\>* line: render the toggle at 0.5 and the button at `BUTTON_PAIR_REL` 0.492 (options-ui-§6) in one Flow line. It calls `PrettyChat:TestToConsole({kind="category", value=category})`, the call `/pc test category` already makes. General's Test stays as it is (§15 leadButton). *Adds an act, not a setting.* With the category off, the report shows that category's strings as inactive; say so in the tooltip. | Checking a category no longer needs a trip to General, and it fills the lonely half-line. | 55% | P13, P17 |
| PRC-L13 | Reorder the editor to **Original → Preview → New**? **Rejected**, kept for the record. Preview renders *New*, so it belongs directly under the box it renders, and moving it away to sit under Original would only trade one confusion for another. **Instead** keep the label **Preview** (it already sits directly under New) and give it the tooltip "Your rewritten format, rendered with sample values. Hover the entry in the list to see Blizzard's original rendered the same way." The earlier *Preview (New)* relabel is dropped: it adds a parenthesis to fix a confusion that the tooltip and PRC-L04 already fix. | Says what each box is relative to the others without breaking the edit-then-see loop. | 50% (tooltip only) | P18 |
| PRC-L14 | Rename the per-string **Reset** → **Reset to default** (button stays at 40% width), and in the same change reword the blank-format refusal (Schema.lua:354, locales/enUS.lua:84) "Use Reset to restore the default." → "Use **Reset to default** to restore it." | Removes the "reset the preview?" reading, matches the page's *Defaults* vocabulary, and keeps the one chat line that names this button correct. | 60% | P19, P26 |
| PRC-L15 | Route the General page title and sidebar name through `L["General"]` (Panel.lua:737, 751), and add `"General"` to the enUS manifest. The page **key** passed to `RegisterOptionsPage` stays the literal (options-ui-§5 names the first sub-page "General"). | Matches Categories/Profiles. Chrome only. | 90% | P20 |
| PRC-L16 | Rename the **Categories** page (sidebar entry and breadcrumb) to **Messages**. The page key `Schema.CATEGORY_PAGE = "Categories"` and every row's `page` stay as they are; only `L["Categories"]` at Panel.lua:755 and 790 changes. The Defaults tooltip and confirmation text say "every category tab", and stay true. Ripple: README.md, docs/settings-panel.md, docs/smoke-tests.md and docs/test-cases.md name the page "Categories". | The sidebar then reads *General · Messages · Profiles*, which says where messages are rewritten. | 45% | P21 |
| PRC-L19 | *(review)* Relabel the General leadButton **Test** → **Test messages** (`leadButton.text`, Schema.lua:192; the host's own string, not composed wording). Tooltip unchanged. `/pc test` stays the verb. | Says what is tested, and stops a bare *Test* reading as a §15 *Test mode* toggle to a player who knows the other Ka0s addons. | 45% | P27 |

Fixed-element constraints honoured: the General page and its first tab `Master controls` (§15) keep the
composer's rows, order and wording; L19 changes only the host-supplied leadButton text. The *Test*
leadButton stays on General (§15). The header Defaults stays on every sub-page, and is page-wide on
Categories (§5, §13). The landing body stays the library's `BuildLandingPage` (§5). The Profiles page has no
strip (§13). The string list is still a TreeGroup inside the scroll (the existing recorded §13/§6
deviations), with no third level.

### Considered and rejected

| id | Idea | Why rejected | Confidence it would help |
|---|---|---|---|
| PRC-L10 | Display label of the **Misc** tab → **Quest & Exploration** (keys `Misc.*` kept; needs a `tabLabel[category]` map because today the label *is* the key, Panel.lua:637, Schema.lua:409). | The tab label and the *Enable %s* label would then differ from `/pc set Misc.enabled`, `/pc test category Misc` and `/pc list Misc`, which the landing page teaches, and the category name is a recorded English path segment (localization-§1 deviation in docs/ARCHITECTURE.md). A two-entry tab is cheap to click. PRC-L09's tooltip carries the meaning instead. | 35% |
| PRC-L10b | *(review)* Display label **Tradeskill** → **Professions**. | Same cost as L10, for a term players still recognise. L09's tooltip opens with "Professions:". | 35% |
| PRC-L17 | Move the eight `<Cat>.enabled` toggles onto one "Overview" tab or onto General. | That would split each category's governing switch from the list it governs, and a copy of the toggle on each tab as well would be two declarations of one row. PRC-L11 meets the same need. | — |
| PRC-L18 | A two-level list (e.g. *XP Gain (Rested)* ▸ Solo / Group / Raid) using TreeGroup children. | It shortens Experience from 20 to 8 top-level entries, but a nested tree inside a tab is arguably the third level that options-ui-§13 forbids, and the curated order (L01) gets most of the benefit. Listed under Upstream suggestions (U3). | 30% |
| PRC-L20 | *(review)* Move **Misc** next to **Experience** in the strip (reorder `CATEGORY_ORDER`). | `CATEGORY_ORDER` also orders `/pc list`, `/pc test` and `ApplyStrings`, and the code records Misc as the deliberate trailing "drawer" (Panel.lua:596-600). L09's pointer on the Experience tab is enough. | 30% |
| PRC-L21 | *(review)* Make the GLOBALNAME caption and the Original box copyable (read-only but enabled EditBoxes) (P25). | It changes widget behaviour, not layout, so it is outside 020's brief. It is a real usability gap (the copy-original-then-edit flow), so file it as a GitHub issue on PrettyChat rather than fold it in here. | n/a (out of scope) |

## Proposed map

Changed items are marked with `«»`.

```
Ka0s Pretty Chat  (landing)                                  unchanged
  logo · tagline · "Slash Commands" (alias row + LandingRows)

«General»  (sub-page 1; title via L["General"])             PRC-L15
  header Defaults btn -> ConfirmResetAll                     unchanged (§5/§12)
  Tab "Master controls"                                      unchanged rows (§15 fixed)
    [chk Enable PrettyChat      General.enabled]   [dd General visibility  General.visibility]
    [chk Debug console          state.debugConsole] (—)
    [chk Minimap button         global.minimap.shown] (—)
    [btn «Test messages»]  [btn Reset all settings]          PRC-L19

«Messages»  (sub-page 2; page key still "Categories")        PRC-L16
  header Defaults btn -> ConfirmResetCategories              unchanged
  Tab strip (tooltip on each tab; label gray when that category is off)   PRC-L09, L11
    Loot | Currency | Money | Reputation | Experience | Honor | Tradeskill | Misc      (labels unchanged)
  (each tab)
    «lbl warning footnote, only when a master gate is closed, naming that gate:
         "PrettyChat is off (Enable PrettyChat, General page), so no message is rewritten." /
         "General visibility (General page) is <mode>, so messages are rewritten only then."»   PRC-L05, L06
    [chk Enable <Category>  <Cat>.enabled  «tooltip reworded + legend»]  [«btn Test this category»]   PRC-L07, L12
    tree (200px list | editor)
      list: «curated order (shared with /pc list, /pc test); gray = off; * = changed;
             hover = label + GLOBALNAME + Blizzard original rendered»   PRC-L01, L02, L04
      editor (selected string)
        [chk «Rewrite this message»  <Cat>.<G>.enabled  «50%»] [lbl GLOBALNAME gray «50%»]   PRC-L08
        eb  Original (disabled)       «tooltip title "Original"»                  PRC-L08
        eb  New   <Cat>.<G>.format    «tooltip title "New"; "rewritten" wording»  PRC-L07, L08
        eb  Preview (disabled)        «tooltip reworded»                          PRC-L13
        btn «Reset to default»                                                   PRC-L14

Profiles  (sub-page 3)                                       unchanged
```

Curated order (PRC-L01), with PRC-L03/L04 labels applied:

| Tab | Display order |
|---|---|
| Loot (17) | Item Looted (Self) · Item Looted Multiple (Self) · Item Looted (Other) · Item Looted Multiple (Other) · Item Pushed (Self) · Item Pushed Multiple (Self) · Item Pushed (Other) · Item Pushed Multiple (Other) · Bonus Roll (Self) · Bonus Roll Multiple (Self) · Bonus Roll (Other) · Bonus Roll Multiple (Other) · Battle Pet Loot · Disenchant Credit · Item Refund · Item Refund (Multiple) · Currency Refund |
| Currency (4) | Currency Gained · Currency Gained Multiple · Currency Gained Multiple (Bonus) · Currency Lost (Death) *(unchanged)* |
| Money (8) | Money Looted (Self) · Money Looted (Other) · Money Looted (Modifier) · Money Looted (Guild Bank) · Money Split · Money Refund · Money Gained (Quest Reward) · Money Gained (Generic) |
| Reputation (14) | Standing Increased · Standing Increased (Generic) · (Achievement Bonus) · (Achievement Part) · (Double Bonus) · (Guardian) · (Rested Part) · (RAF Bonus) · (RAF Part) · Standing Decreased · Standing Decreased (Generic) · Standing Changed · Standing Changed (Guild) · Standing Changed (Guild Name) |
| Experience (20) | XP Gain (Rested) ×solo/Group/Raid · (Normal) ×3 · (Tired) ×3 · (Exhausted) ×3 · XP Gain (Kill, No Bonus) ×3 · XP Gain (No Source) ×3 · XP Gain (Quest) · XP Loss *(order unchanged; the GLOBALNAME order already follows rest state)* |
| Honor (6) | Honor Gain · Honor Gain (Rested) · Honor Gain (No Rank) · Honor Gain (No Rank, Rested) · Honor Award · Dishonorable Kill |
| Tradeskill (8) | Created Item (Self) · Created Item Multiple (Self) · Created Item (Other) · Created Item Multiple (Other) · Tradeskill Log (Self) · Tradeskill Log (Other) · Open Lock (Self) · Open Lock (Other) |
| Misc (2) | Quest Reward XP · Zone Explored XP *(unchanged)* |

Counts after: pages 4, tabs 9, schema rows 170 (no change). New on-screen widgets: one *Test this category*
button per tab (an act). The footnote is drawn conditionally.

## Cross-addon notes / Upstream suggestions

**Cross-addon notes**

- **Per-item reset wording.** PrettyChat's per-string act becomes *Reset to default* (L14). Every addon with a
  per-row or per-entity reset (QuickComms pads, AuraMaster entries, MultiMeters meters) should use the same
  verb, distinct from the page's *Defaults* and the global *Reset all settings*. Any chat message that names
  the button moves with it (P26).
- **Notices that name another page's control** should quote its exact on-screen label (*Enable PrettyChat*,
  *General visibility*), not a paraphrase like "master Enable", and should name the gate that is actually
  closed. This applies to every addon that prints a "this only works while …" footnote.
- **Lists that select one subject** (PrettyChat's TreeGroup, AuraMaster spell lists, QuickComms pad lists)
  should all sort by what is displayed, or by a declared order kept in **one** place that the CLI also uses,
  and never by a hidden key. They should also show per-entry state (off / changed) in the list itself. An
  AceGUI TreeGroup's default hover tooltip repeats the label, so either turn it off or give it content.
- **Tab tooltips.** `H.TabStrip` already takes a per-tab tooltip, and none of PrettyChat's tabs uses it. Worth a
  collection-wide check: a tab whose subject is not obvious from a one-word label should carry one.
- **Page titles through `L[...]`.** PrettyChat's General is a literal. Check the other addons' General
  page registration for the same thing.
- **One-shot "Test" buttons vs §15 *Test mode*.** Any addon whose `leadButton` or verb is a bare *Test* should
  name what it tests (L19), so it is not mistaken for the collection's *Test mode* toggle.
- **"Rail" means two things.** Proposals across the bundle should say *sidebar* for Blizzard's Settings list and
  keep *nav rail* for `O.NavRail`.
- **Keybindings (015).** PrettyChat is out of scope, having no window. Its General page will be the one-tab
  shape while the seven windowed addons gain a second *Keybindings* tab; that is the intended difference, not
  drift. If the owner ever wants a *Toggle debug console* binding collection-wide, it would be the one binding
  PrettyChat could offer, but that is not requested.

**Upstream suggestions (WowAddonStandards options-ui / LibKa0s OptionsCompose)**

- **U1 — frameless Master controls packing (options-ui-§15).** For a frameless addon, the canonical order plus
  *Minimap button*'s column-1 rule leaves two half-empty lines (`[Debug console] (—)` / `[Minimap button] (—)`).
  Suggest: when *Lock frame* is omitted, *Debug console* and *Minimap button* share one line, so the frameless
  shape is `[Enable] [General visibility] / [Debug console] [Minimap button] / [Test…] [Reset all settings]`.
  The column-1 rationale (no hole before a lone control) does not apply when the line is full. Affects every
  frameless Ka0s addon.
- **U2 — composer tooltip override for General visibility (§15, OptionsCompose `emit`).** Let a host pass
  `tooltips = { visibility = "…" }` (the wording stays the composer's unless overridden), or let a frameless
  spec pick a variant: "When this addon is active at all." The current "addon's display is shown" is wrong for
  an addon whose output is chat text. Doing it in the composer keeps PrettyChat from patching the returned
  row in `InstallMasterControls`, which would be the drift §15 exists to stop.
- **U3 — nested subject lists (§13).** State whether TreeGroup children *inside* a secondary selector count as
  the forbidden third level. If they do not, PrettyChat's Experience list could collapse 20 entries to 8.
- **U4 — conditional notices.** options-ui could codify "a page notice about a gate on another page is drawn
  only while that gate is closed, names that gate by its label, and uses the warning color", and the library
  could offer a refresh hook for it (the gate lives on another page, and today a value write does not redraw
  labels), so the collection stops shipping always-on gray footnotes.

## Review

Independent review against `PrettyChat@b08c579` (code, vendored AceGUI and LibKa0s, options-ui.md). What changed and why:

- **Current map corrected and completed.** Added the TreeGroup's built-in label-only hover tooltip, the editor's
  greyed states (Panel.lua:338, 340), the fact that Original is not selectable, the footer-Defaults path on
  Categories, that tab labels are raw keys without tooltips, and the Profiles container's real parent
  (`ctx.body`, not a scroll). Fixed the composer line range. Verified every list row by loading
  `defaults/Defaults.lua` and sorting it. Added a *Refresh facts* paragraph, because three proposals assumed
  refresh paths that do not exist.
- **Wrong claims fixed.** L02 said the refresher re-runs `SetTree`, and it does not. L02 also had to warn off
  TreeGroup's `disabled` field, which makes an entry unclickable. L06's footnote is never redrawn by a General
  write, so I added the plumbing and cut confidence from 60% to 55%. P05 and P07 cited options-ui-§7 for "two
  names" and §7 is the heading rule; I re-cited them to the addon's own rule. P22 was not plain drift, since
  Loot was 19 before migration v2, so I softened it. "Rail" is now *sidebar*, because PrettyChat has no nav rail.
- **L01 reworked (90% → 85%).** A display-only order in Panel.lua would break PRETTYCHAT-R-09's one-order rule
  and make the panel disagree with `/pc list` and `/pc test`. It now moves the order into the single source.
- **Settings check.** No proposal changes a key, default, range or stored behaviour. L01 changes walk order
  only, and ApplyStrings is order-independent because duplicate globals are refused. L12 adds an act and no
  setting. L19 changes only host-owned leadButton text, not composed §15 wording.
- **Recalibrated.** L08 80% → 55% with a 0.5/0.5 rebalance (P28). L11 50% → 45% (selected-tab colour clash,
  needs a structural refresh). L13 55% → 50%, with the *Preview (New)* relabel dropped. L14 kept at 60%, and
  it now carries the refusal message (P26). L05 85% → 80%, reworded per gate.
- **Moved to Considered and rejected.** L10 (Misc → Quest & Exploration) went from 40% to 35%: it splits the tab
  name from the CLI name. Also rejected: a Tradeskill → Professions relabel (L09's tooltip carries it
  instead), moving Misc next to Experience, and copyable Original/GLOBALNAME (widget behaviour, so a
  follow-up issue).
- **Added.** P23–P28; L04 now replaces the built-in tooltip and renders the original, which also covers P18;
  L19 (*Test messages*); L09's Tradeskill tooltip names *Professions*; cross-addon notes on Test naming,
  sidebar/rail terminology and the one-tab General page next to the seven Keybindings addons; U2/U4 sharpened.
