# WhatGroup — settings layout analysis

Read from `../WhatGroup` on `master` (clean), 2026-10-24: all of `settings/` (`Schema.lua`, `SchemaSetup.lua`,
`OptionsSetup.lua`, `Panel.lua`, `Profiles.lua`, `Slash.lua`), `defaults/Profile.lua`, `Bindings.xml`,
`modules/Frame.lua` (binding button, popup), `core/WhatGroup.lua` (the chat summary's print order),
`locales/enUS.lua`, `docs/settings-panel.md`, and the vendored composer `libs/LibKa0s/OptionsCompose.lua`
(`O.MasterControls`, :458). Standard: `options-ui.md` §3, §5, §7, §12, §13, §14, §15.

WhatGroup is small. It has 12 settings of its own and 8 composed Master controls rows. Every finding below is
about the 12 own rows and the wording around them. The Master controls block, the landing page and the Profiles
page are fixed by the standard and are only reworded at the tooltip level.

## Current map

Pages: **3** (landing, General, Profiles). **1** of them (General) holds settings. Primary tabs: **3** (all on
General). Secondary tabs: **0**. Nav rail: none. Schema rows: **20** (8 composed + 12 declared). Non-row
controls: **4**: the header Defaults button, Reset position, Reset all settings, and Test.

Two-column grid. `|` separates the two cells of one line and `—` is an empty cell.

```
Ka0s WhatGroup (landing)             OptionsSetup.lua:222 buildMain -> Panel.lua:112 BuildMainContent -> lib BuildLandingPage
  logo 300x300 · TOC Notes tagline · "Slash Commands" heading · 15 command labels (Slash.lua:41-81 via LandingRows)
  (no settings)

General                               Panel.lua:303 buildGeneralPage, registered Panel.lua:333; renderer Panel.lua:326 RenderTabbedSchema
  [header Defaults button]            Panel.lua:306-316 (tooltip :307), confirm popup Schema.lua:655
  Tab 1  Master controls              composed Panel.lua:146-189, spliced at head Panel.lua:239-240; hooks :199-231
    line 1  Enable WhatGroup (CheckBox, enabled)                 | General visibility (Dropdown, visibility)
    line 2  Master scale (Slider, scale)                         | Master alpha (Slider, alpha)
    line 3  Lock frame (CheckBox, locked)                        | Debug console (CheckBox, state.debugConsole, session)
    line 4  Minimap button (CheckBox, global.minimap.shown, global) | Test mode (CheckBox, state.testMode, session; tooltip Panel.lua:222)
    tail    [Reset position] | [Reset all settings]              composer tail, keyed Panel.lua:293-295
  Tab 2  Chat                         Schema.lua:153-241
    -- Timing --
    line 1  Notification Delay (Slider 0-10 s, notify.delay)     | —            (solo, Schema.lua:153)
    -- Text --
    line 2  Print to Chat (CheckBox, notify.enabled)             | —            (solo, Schema.lua:177)
    line 3  Instance (CheckBox, notify.showInstance)             | Type (CheckBox, notify.showType)            Schema.lua:186,194
    line 4  Leader (CheckBox, notify.showLeader)                 | Playstyle (CheckBox, notify.showPlaystyle)  Schema.lua:202,210
    line 5  Details link (CheckBox, notify.showClickLink)        | Teleport spell (CheckBox, notify.showTeleport) Schema.lua:218,226
    line 6  Role (CheckBox, notify.showRole)                     | —            (Schema.lua:235)
    tail    [Test]  160 px, left-aligned                         Panel.lua:260-273 -> Panel.lua:42 InlineButton -> WhatGroup:RunTest
  Tab 3  Popup                        Schema.lua:247-287
    -- Behavior --
    line 1  Open Automatically (CheckBox, frame.autoShow)        | —            (solo, Schema.lua:247)
    -- Layout --
    line 2  Width (Slider 320-700 px, frame.width)               | Height (Slider 200-520 px, frame.height)    Schema.lua:269,279

Profiles                              Profiles.lua:35 build, registered Profiles.lua:89
  AceDBOptions table drawn by AceConfigDialog (Profiles.lua:75); no Defaults button (options-ui-§3); no schema rows

Key binding (not in the panel)        Bindings.xml:3  CLICK WhatGroupTogglePopup:LeftButton, category="ADDONS"
  header "Ka0s WhatGroup" (Frame.lua:1334), name "Toggle group popup" (Frame.lua:1335, enUS.lua:144)
```

Tooltips and wording the map does not show, verified against the code: the composed rows carry the library's generic
tooltips (OptionsCompose.lua:474-555; "Reset position" says "Move the frame back to where it started.", :555). The
seven line toggles say "in the chat notification" (Schema.lua:190-239), while *Print to Chat* says "group-details
summary" (:181). Three tooltips spell the window "group-info popup", hyphenated (:251, :273, :283). The landing list's
`resetall` line says "Reset every setting to defaults" (Slash.lua:66, enUS.lua:122). The file-header comment at
Schema.lua:78-104 and `docs/settings-panel.md` draw this same map, and `tests/test_panel.lua` selects the tabs by
name ("Chat" at :283-496, "Popup" at :329).

Counts: General has 3 tabs and 20 rows on 12 lines, plus 3 tail buttons. The longest tab is Chat, with 9 rows
on 6 lines. The shortest is Popup, with 3 rows on 2 lines.

## Problems

| id | where | problem |
|---|---|---|
| WHA-P01 | Schema.lua:153-161, :157 | **The delay is split from one of the two things it delays.** `notify.delay` holds back both the chat summary *and* the popup (its own tooltip says so), but it lives on the Chat tab. A player who wants the popup to wait for the zone-in looks on Popup and does not find it. |
| WHA-P02 | Schema.lua:247-287 | **The Popup tab is thin.** It has 3 rows on 2 lines and two one-line subsections. A whole tab switch buys almost nothing. |
| WHA-P03 | Panel.lua:260-273, :265-267 | **The Test button sits on Chat but tests both tabs.** `RunTest` runs "the full notification + popup flow", so it also previews `frame.autoShow` and the popup's size, which live on another tab. Its tooltip only mentions "the chat-output toggles". |
| WHA-P04 | Schema.lua:78-104 | **Setting up "what happens when I join a group" takes 3 tabs**: Chat for the delay and the lines, Popup for auto-open and size, and Master controls for visibility, scale and lock. The last hop is fixed by §15, but the Chat/Popup split is not. |
| WHA-P05 | Schema.lua:178-236 (`subgroup = "Text"`) | **The subsection name "Text" is vague.** Every row on the tab is about text. What the subsection holds is the *lines of the chat summary*. |
| WHA-P06 | Schema.lua:186-241, core/WhatGroup.lua:858-880, :917 | **The toggle order does not match the output order.** Chat prints Group, Instance, Type, Leader, **Role**, Playstyle, Teleport, then the link last. The panel reads Instance, Type, Leader, Playstyle, **Details link**, Teleport, Role. Role is last only "so the six toggles before it keep the pairs they have always had" (Schema.lua:234): history, not the player's model. The link is a clickable affordance, not an info line, but it sits mid-list. |
| WHA-P07 | Schema.lua:248, :270, :280 | **Two lonely subsections on Popup.** "Behavior" holds 1 row and "Layout" holds 1 line. Both headings name a single control. |
| WHA-P08 | Panel.lua:264, :222; Slash.lua:45 | **"Test" names two things one row apart in the player's head.** Master controls has *Test mode* (a persistent preview) and Chat has a button labeled just *Test* (a one-shot run). The verb that matches the button is `/wg test notify`, not `/wg test`, which is the mode. |
| WHA-P09 | Schema.lua:239 vs :190-230 | **The "popup always shows it" note is inconsistent.** Only Role's tooltip says so, but every `notify.show*` row gates chat only (settings-panel.md, "The popup dialog always renders every field"). A player reading Instance's tooltip can fairly believe it hides the popup's Instance row. |
| WHA-P10 | Schema.lua:273, :283 | **Sizing the popup is blind.** Width and Height commit on release against a popup that is usually not on screen. Nothing tells the player that *Test mode* (on another tab) is how to see it while sizing. |
| WHA-P11 | Panel.lua:225-231; OptionsCompose.lua:478-490 | **Composed tooltips are generic** ("Scales the whole addon's display.", "Stop the frame being dragged.") while every one of them acts on the popup. Scale is also refused in combat (Frame.lua:149-152), which the row never says. The host already overrides *Test mode*'s tooltip for exactly this reason (Panel.lua:221-223), so the precedent exists. |
| WHA-P12 | Panel.lua:307 | **The header Defaults tooltip overstates its reach.** "Reset every WhatGroup setting to its default" is really a reset of the *current profile* (Schema.lua:590-619). The minimap row survives it (launcher-§3) and other profiles are untouched. *Reset all settings* (same act, options-ui-§12) says this correctly, so the two controls for one act describe it differently. |
| WHA-P13 | Schema.lua:156, :180, :250 | **Capitalization is inconsistent.** "Notification Delay", "Print to Chat" and "Open Automatically" are Title Case. Every other row, including the canonical §15 block ("Lock frame", "Debug console"), is sentence case. |
| WHA-P14 | Schema.lua:156 | **"Notification Delay" undersells the row.** It delays the popup too (P01). Once the row sits above both, the label should say *what it waits for*. |
| WHA-P15 | Schema.lua:250 | **"Open Automatically" leaves out the when.** It means "open the popup when you join a group". Away from its subsection it reads as an always-open window. |
| WHA-P16 | Slash.lua:43, :47; Frame.lua:828 | **One window, four names.** The landing list says "group info **dialog**", the tooltips say "group-info **popup**", the window title says "Group Info", the binding says "group popup", and `config` says "Settings panel" with a capital S. |
| WHA-P17 | Panel.lua:146-189 vs Schema.lua:269-287 | **The popup's controls are spread over two tabs.** Scale, alpha, lock and reset position sit on Master controls, and width and height on Popup. **Constrained**: options-ui-§15 fixes the first four on the first tab ("MUST NOT … split them across tabs"), so this is not changed (see Upstream suggestions). |
| WHA-P18 | Schema.lua:177-241 | **Dependents do not show their master.** With *Print to chat* off, the 7 line toggles stay fully active, so the panel does not show that they do nothing. This is not fixable as a layout change (it would be new widget behavior), so it goes to Upstream suggestions. |
| WHA-P19 | Bindings.xml:3; Frame.lua:1334-1335 | **The planned Keybindings tab needs a slot and a name.** The binding is listed under the generic AddOns category today, and the label "Toggle group popup" does not use the window's own name ("Group Info"). |
| WHA-P20 | Schema.lua:153 (`subgroup = "Timing"`) | **Timing is a one-row subsection.** It survives the proposed merge (L01), and there it becomes the tab's lead-in, governing both subsections below it. It is kept on purpose, because options-ui-§7 needs a heading where a slider stands above checkboxes. |
| WHA-P21 | Schema.lua:251 vs :218-222 | **The Popup tab points at a control on the Chat tab.** *Open Automatically*'s tooltip says you can re-open the popup "with /wg show or the chat link". That link exists only while *Print to Chat* and *Details link* are both on, and both are on the other tab (Schema.lua:177-222). This is one more cross-tab dependency of the join flow, and it argues for L01. |
| WHA-P22 | Schema.lua:181, :190-239 | **Two nouns for the chat output.** The master's tooltip says "summary"; the seven line toggles say "chat notification"; the button tooltip says "notification + popup flow". After L02 names the subsection "Chat summary", the tooltips should say the same word. |
| WHA-P23 | Slash.lua:66; enUS.lua:122 | **The landing page repeats P12's overstatement.** `/wg resetall` reads "Reset every setting to defaults" on the landing page (a settings page) while the act is a reset of the current profile with the minimap row vetoed (Schema.lua:586-619). L12 fixed the header tooltip and missed this one. |
| WHA-P24 | Panel.lua:222-223; Frame.lua:816-818 | **Test mode's tooltip promises a drag that *Lock frame* can refuse.** "so you can drag it into place" is false while *Lock frame* is ticked, one row above it. Nothing says so. |

## Proposed changes

| id | change | reason | confidence | fixes |
|---|---|---|---|---|
| WHA-L01 | **Merge the Chat and Popup tabs into one tab, "Notifications".** Every declared row's `group` goes from `"Chat"` / `"Popup"` to `"Notifications"` (Schema.lua:154, 178-236, 248, 270, 280). The `AFTER_GROUP` key goes from `"Chat"` to `"Notifications"` (Panel.lua:262). Subsections in order: Timing, Chat summary, Popup window (L02, L04). `section` (`/wg list` key) is untouched. | One tab now holds the whole join flow: when it fires, what chat says, and whether and how big the popup opens. The delay sits above both of the things it delays (P01), the Test button sits under everything it previews (P03), a 3-row tab disappears (P02), and setting up the flow takes 2 tabs instead of 3 (P04). It is 12 rows on 9 lines, still one screen. options-ui-§13 "one tab per section" holds, because this is one subject with mixed control types and §7 requires headings for that. §7's "MUST NOT fake a second tab level" is the judgment call: a 3-row subject does not "want its own tab". The strip shrinks to Master controls, Notifications, Keybindings. The merge also puts *Open on join*'s "re-open with the chat link" on the same tab as the two toggles that make that link exist (P21). Implementation cost, not a setting change: the file-header map (Schema.lua:78-104), `docs/settings-panel.md` and the `selectTab(mock, "Chat"/"Popup")` cases in tests/test_panel.lua move with it. | 65% | P01 P02 P03 P04 P21 |
| WHA-L02 | Rename subsection `"Text"` → **`"Chat summary"`** (Schema.lua:178-236). | Names what the rows choose: the lines of the chat summary. The tab is no longer called Chat, so the subsection has to say "chat" itself. | 75% | P05 |
| WHA-L03 | **Reorder the chat-line toggles to the print order**, with the link last and alone. Line 1 Instance \| Type, line 2 Leader \| Role, line 3 Playstyle \| Teleport spell, line 4 Details link \| —. Move `notify.showRole` (Schema.lua:235) up to right after `notify.showLeader` (:202), and move `notify.showClickLink` (:218) to after `notify.showTeleport` (:226). Replace the comment at :234. | The panel then reads top to bottom like the summary it configures (core/WhatGroup.lua:858-880). The odd one out, a clickable link rather than an info line, closes the list, as it closes the output (:917). The line count is unchanged (4). | 85% | P06 |
| WHA-L04 | **Collapse "Behavior" + "Layout" into one subsection, "Popup window"** (Schema.lua:248, 270, 280). Open on join \| —, then Width \| Height. | Two one-line headings become one heading over the popup's three rows (P07). The subject is the window, and §7's mixed-type rule is met at tab level by the three headings. The checkbox stays `solo`, so it does not read as pairing with a size. | 65% | P07 |
| WHA-L05 | **Sentence case for the three Title Case labels**: "Print to Chat" → **"Print to chat"** (Schema.lua:180). The other two are reworded in L06 and L07. | Matches the canonical §15 rows and every other label in the addon (P13). Label text only; the path is untouched. | 85% | P13 |
| WHA-L06 | "Notification Delay" → **"Delay after joining"** (Schema.lua:156). The tooltip keeps its wording and starts "Applies to both the chat summary and the popup." | It sits above both subsections after L01, so the label names the event it waits on rather than one of its two consumers (P14). | 70% | P13 P14 |
| WHA-L07 | "Open Automatically" → **"Open on join"** (Schema.lua:250). | Says when, in three words, under a heading that already says "Popup window" (P15). | 70% | P13 P15 |
| WHA-L08 | Rename the button "Test" → **"Test notification"** (Panel.lua:264). Tooltip (:265-267) → "Run the join notification once with sample group info: the chat summary, then the popup. Same as `/wg test notify`. For a popup that stays up while you adjust it, use Test mode on Master controls." | Separates the one-shot run from the persistent *Test mode* (P08), names the verb it mirrors, and says it previews the popup too (P03). It still fits the fixed 160 px width. It is not moved to the composer's `leadButton`: that would put a chat preview on Master controls and draw it at half width on its own line above the resets (OptionsCompose.lua:564-570). | 80% | P03 P08 |
| WHA-L09 | Tooltips of the 7 line toggles: **one consistent sentence**. *Print to chat* (Schema.lua:181) gains "The popup always shows every line; these choose the chat summary only." Role's "The popup always shows it." (:239) is dropped to match its siblings. | One statement of the chat-only rule, on the master, instead of on one of seven rows (P09). | 70% | P09 |
| WHA-L10 | Width and Height tooltips (Schema.lua:273, :283) gain "Tick Test mode on Master controls to see the popup while you size it." | Turns a blind slider into a guided one without moving a §15 row (P10). Depends on the popup staying above the Settings panel while you drag a slider, which is true at DIALOG today and is why the strata review keeps it there (strata WHA-Z02). | 60% | P10 |
| WHA-L11 | **Stamp popup-specific tooltips onto 4 composed rows** beside the existing Test mode override (Panel.lua:221-231). visibility → "When the group info popup may be on screen."; scale → "Scale of the group info popup. Not changed in combat; applies on the next open."; alpha → "Opacity of the group info popup."; locked → "Stop the group info popup being dragged by its title bar." | Labels, order and rows are untouched (§15 forbids only reorder, rename and split). The tooltip is the one place a host can say what "the display" is, and this addon already does it for Test mode (P11). | 60% | P11 |
| WHA-L12 | Header Defaults tooltip (Panel.lua:307) → **"Reset this profile to WhatGroup's defaults. Your other profiles are not affected. Asks for confirmation."** | Same act as *Reset all settings*, so the same story (options-ui-§12, P12). If the library ever composes this tooltip, take it from there instead (Upstream U3). | 75% | P12 |
| WHA-L13 | **One name for the window: "group info popup".** Slash.lua:43 "Show the last group info dialog" → "Show the group info popup again". Slash.lua:47 "Open the Ka0s WhatGroup Settings panel" → "Open the Ka0s WhatGroup settings". Locale keys move with the strings (enUS.lua). The three hyphenated "group-info popup" tooltips (Schema.lua:251, :273, :283) lose the hyphen. The window title "WhatGroup — Group Info" (Frame.lua:828) stays: it is not a settings element. Both Slash.lua strings also print in `/wg help`, which is the same list by construction (Panel.lua:105-110). | The landing page is a settings page, and it should use the word every tooltip uses (P16). | 55% | P16 |
| WHA-L14 | **Keybindings tab, last on General** (after Notifications), for the 015 work. One row: the window toggle, primary and secondary key, synced with Settings > Keybindings > **Ka0s WhatGroup**. Binding name "Toggle group popup" (enUS.lua:144) → **"Toggle group info popup"**. | Last is the one slot all 7 windowed addons can share without displacing a §15 tab or an addon's own tabs. Bindings are touched rarely, so they go at the end of the strip. The name matches L13's single noun (P19). The `CLICK WhatGroupTogglePopup:LeftButton` command name is unchanged, so no player's key is lost (Frame.lua:1308-1309). The tab should carry one line saying keys are not part of the profile, so neither the header Defaults button nor *Reset all settings* touches them (options-ui-§13 keeps Defaults page-wide, and a player will otherwise expect it to clear the new tab too). | 75% | P19 |
| WHA-L15 | **One noun for the chat output: "chat summary".** The seven line-toggle tooltips (Schema.lua:190-239) say "in the chat summary" instead of "in the chat notification"; *Open on join*'s tooltip (:251) says "the chat summary still prints". Tooltip text only. | Matches the new subsection heading (L02) and the master's own tooltip (P22). | 70% | P22 |
| WHA-L16 | Landing `resetall` description (Slash.lua:66, enUS.lua:122) "Reset every setting to defaults" → **"Reset this profile to defaults"**. | Same act as the header Defaults button and *Reset all settings*, so the same claim (options-ui-§12, P23). It is a command description, not a setting. | 70% | P23 |
| WHA-L17 | Test mode tooltip (Panel.lua:222-223) gains **"Untick Lock frame first if you want to move it."** | The tooltip promises a drag the row above it can refuse (P24). Tooltip only; the §15 row, its label and its position are unchanged. | 55% | P24 |

**Not changed, on purpose.** The Master controls order and labels (options-ui-§15). The landing body
(options-ui-§5). The Profiles page (options-ui-§3: AceConfigDialog-drawn, no Defaults). There is no page banner,
because there is no instance to name (options-ui-§14, Panel.lua:324-325). `section` keys stay put, because they
are `/wg list`'s grouping and not part of the layout (settings-panel.md, "section is not group").

## Considered and rejected

| change | confidence | why not |
|---|---|---|
| Move Width and Height onto Master controls through the composer's `extra` slot, so every popup control sits on one tab (P17). | 35% | For a one-window addon they are addon-wide, but §15's `extra` exists for controls "the player looks for in the same place" in every addon. No other addon would carry a window size there, so this would break cross-addon consistency to fix a one-addon split. |
| Move the Test button to the composer's `leadButton` (options-ui-§15 names it as a one-shot test action's home). | 30% | It would put a chat preview on Master controls, away from every row it previews, and draw it at half width above the resets (OptionsCompose.lua:564-570). §15 says MAY, so leaving it on the join-flow tab is compliant. |
| Drop the *Timing* heading and make the delay the first row of *Chat summary*. | 20% | The delay governs the popup too; filed under the chat heading it repeats P01. §7 also wants a heading where a slider stands above checkboxes. |
| Stamp a popup-specific tooltip on *Reset position* too. | 35% | It is a composer tail button, not a schema row, so there is no `row.tooltip` seam to stamp (Panel.lua:225-231 stamps rows only). It would need a composer option (fold into Upstream U2). |
| Name the merged tab "Join notice" (the word `/wg help` uses, Slash.lua:45) instead of "Notifications". | 35% | Shorter strip labels win, and "Notifications" covers both the chat summary and the popup. Worth the owner's call only if another addon already uses "Notifications" for something else. |

## Proposed map

```
Ka0s WhatGroup (landing)             unchanged except two command descriptions (L13)
  logo · tagline · "Slash Commands" · 15 command labels
    /wg show    — Show the group info popup again                      (L13)
    /wg config  — Open the Ka0s WhatGroup settings                     (L13)
    /wg resetall — Reset this profile to defaults                      (L16)

General
  [header Defaults button]  tooltip: "Reset this profile to WhatGroup's defaults. ..."      (L12)
  Tab 1  Master controls              (composed, order and labels unchanged; 4 tooltips stamped, L11; Test mode tooltip +1 sentence, L17)
    line 1  Enable WhatGroup (CheckBox, enabled)                 | General visibility (Dropdown, visibility)
    line 2  Master scale (Slider, scale)                         | Master alpha (Slider, alpha)
    line 3  Lock frame (CheckBox, locked)                        | Debug console (CheckBox, state.debugConsole, session)
    line 4  Minimap button (CheckBox, global.minimap.shown)      | Test mode (CheckBox, state.testMode, session)
    tail    [Reset position] | [Reset all settings]
  Tab 2  Notifications                (was Chat + Popup, L01)
    -- Timing --
    line 1  Delay after joining (Slider 0-10 s, notify.delay)    | —                                    (L06)
    -- Chat summary --                                                                                  (L02)
    line 2  Print to chat (CheckBox, notify.enabled)             | —                                    (L05, L09; line tooltips L15)
    line 3  Instance (CheckBox, notify.showInstance)             | Type (CheckBox, notify.showType)
    line 4  Leader (CheckBox, notify.showLeader)                 | Role (CheckBox, notify.showRole)     (L03)
    line 5  Playstyle (CheckBox, notify.showPlaystyle)           | Teleport spell (CheckBox, notify.showTeleport) (L03)
    line 6  Details link (CheckBox, notify.showClickLink)        | —                                    (L03)
    -- Popup window --                                                                                  (L04)
    line 7  Open on join (CheckBox, frame.autoShow)              | —                                    (L07, L13, L15)
    line 8  Width (Slider 320-700 px, frame.width)               | Height (Slider 200-520 px, frame.height) (L10)
    tail    [Test notification]  160 px, left-aligned                                                   (L08)
  Tab 3  Keybindings                  (new, item 015, L14)
    Toggle group info popup  [key 1] [key 2]   (synced with Settings > Keybindings > Ka0s WhatGroup)
    note: Keys are saved by the game, not in your profile; Defaults and Reset all settings leave them alone. (L14)

Profiles                              unchanged
```

Counts after: 3 pages, 3 tabs on General (Master controls, Notifications, Keybindings), 20 schema rows on 12
lines plus 1 binding row, and 4 non-row controls. Tabs that hold the join flow: 1 (was 2).

## Cross-addon notes

- **Keybindings tab slot.** Make it the **last** General tab in all 7 windowed addons, named exactly
  `Keybindings`, with the window toggle as its first row. BankLedger's analysis proposes the same slot.
- **Binding names.** Use a verb plus the window's own noun with no article: "Toggle group info popup", in the
  same shape as "Toggle ledger window". The category is the brand ("Ka0s WhatGroup"), which equals
  `BINDING_HEADER_WHATGROUP` today (Frame.lua:1334).
- **One-shot test buttons vs Test mode.** Any addon that has both a *Test mode* row and a one-shot test button
  should name the button for what it runs ("Test notification", "Test alert"), never a bare "Test".
- **Sentence case** for every row label, to match the canonical §15 block. Title Case labels are a WhatGroup
  leftover and likely exist elsewhere.
- **Composed-row tooltips naming the display.** Wherever "the display" or "the frame" is one concrete window,
  stamp a tooltip that names it, as WhatGroup already does for Test mode.
- **Header Defaults tooltip.** Every addon's Defaults button triggers the same §12 act, so all of them should carry
  the same profile-reset wording as *Reset all settings*.
- **One noun per window** across the landing list, tooltips, the window title and the binding.
- **Keybindings tab vs the reset acts.** Every windowed addon's Keybindings tab should say, in the same words,
  that keys are not part of the profile and that Defaults / *Reset all settings* leave them alone (L14).
- **Landing `resetall` description.** Wherever the header tooltip is reworded (L12), the landing page's
  `resetall` line should carry the same claim (L16). Check every addon's COMMANDS table.
- **Test mode vs Lock frame.** Any addon whose Test mode does not unlock should say so in its Test mode tooltip
  (L17), or adopt §15's "MAY unlock as a side effect".

## Upstream suggestions

- **U1, options-ui-§13 / §7, thin tabs.** Say when a small subject should be a subsection rather than a tab, for
  example "a subject of four rows or fewer SHOULD be a subsection of the tab its rows act with". Also say that
  merging two related thin tabs under one name with subsections is *not* "faking a second tab level". Without
  this, L01 is a judgment call that every addon can make differently.
- **U2, options-ui-§15, composed tooltips.** State that a host MAY override a composed row's **tooltip** (never
  its label or order) to name the concrete display. WhatGroup's Test mode override is the existing precedent.
- **U3, options-ui-§12 / §5, header Defaults tooltip.** Have the library compose the header Defaults tooltip
  from the same descriptor fields (`resetProfile`, `profilesPage`) it already uses for *Reset all settings*.
  Then the two controls for one act cannot describe it differently (P12).
- **U4, library: dependents of a master.** A schema `dependsOn = "<path>"` that grays a row while its master is
  off. This is UI state, not a setting. It would fix P18 here (7 rows under *Print to chat*) and the same
  pattern in other addons.
- **U5, options-ui: label case.** No rule fixes capitalization today (only US spelling, localization.md:140). Add
  "row labels are sentence case".
- **U6, options-ui-§15 vs per-window size (P17).** For one-window addons the popup's controls end up split across
  Master controls and the addon's own tab. Leave the rule as it is (the cross-addon value is real), but say in §15
  that a window's size belongs on the tab that holds the window's behavior, so the split is at least the same
  split in every addon.
- **U7, library: composer tail tooltips.** `MasterControls` takes no tooltip override for *Reset position*
  ("Move the frame back to where it started.", OptionsCompose.lua:555). A `resetPositionTooltip` field, the
  tail-button half of U2, would let a one-window addon name the window there too.

## Review

Independent review, 2026-10-24, checked against `../WhatGroup` on `master` (Schema.lua, Panel.lua, Slash.lua,
OptionsSetup.lua, Profiles.lua, Frame.lua, core/WhatGroup.lua, enUS.lua, tests/test_panel.lua, vendored
OptionsCompose.lua) and options-ui.md §6, §7, §12, §13, §15.

- **Current map: accurate.** Every row, path, label, range, subgroup, `solo` flag, tail button and line ref
  checked out, as did the counts (20 rows on 12 lines, 15 command labels, 4 non-row controls) and the chat print
  order (core/WhatGroup.lua:858-917). Added a paragraph under the map for what it did not show: the generic
  composed tooltips, the two nouns for the chat output, the hyphenated "group-info popup", the landing
  `resetall` line, and the comment, doc and test sites that pin the current tab names.
- **No change alters a setting.** All 17 changes touch only `group` / `subgroup` / declaration order / label /
  tooltip / command description text. No path, default, range or `onChange` moves. L03 also reorders `/wg list`
  inside the `notify` section, which is display order and not a setting. No change breaks a standard rule:
  L01 is one section with subsections (§13 "one tab per section" holds, §7 judgment call already flagged), and
  L08 keeps the one-shot button off `leadButton`, which §15 allows ("MAY").
- **Added problems P21-P24 and changes L15-L17.** P21: *Open Automatically*'s tooltip relies on the chat link from
  the other tab, which makes L01 stronger. P22/L15: "chat notification" vs "summary", unified on "chat summary".
  P23/L16: the landing `resetall` line repeats P12's overstatement. P24/L17: Test mode's "drag it into place"
  is refused by *Lock frame*. L13 now also removes the hyphen in three tooltips and notes that the Slash strings
  also feed `/wg help`. L14 now asks the Keybindings tab to say that resets leave keys alone.
- **Confidence recalibrated.** L01 went from 60% to 65% (P21 is one more cross-tab dependency, and the implementation
  cost of comments, docs and tests is now stated). L10 went from 65% to 60%, because it only works while the popup stays
  above the Settings panel, which ties it to the strata review's decision to keep DIALOG. The others are unchanged.
- **Considered and rejected.** The inline 35% alternative became a section, and four more alternatives were added
  with their reasons: the `leadButton` move, dropping *Timing*, a *Reset position* tooltip (no seam, so it went
  to U7) and the "Join notice" tab name.
- **Cross-addon notes and upstream.** Added notes on the Keybindings tab and the resets, the landing `resetall` line,
  and Test mode vs Lock frame. Added U7.
