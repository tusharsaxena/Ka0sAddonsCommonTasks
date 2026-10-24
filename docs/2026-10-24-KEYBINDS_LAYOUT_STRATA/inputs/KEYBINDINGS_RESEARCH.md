# Item 015: key bindings research

Research input for the 2026-10-24 KEYBINDS_LAYOUT_STRATA bundle. It is read-only research: nothing in
any repo was changed to produce it.

**Owner brief.** "Add keybinding for all addons with a window, which should do the /xx toggle action
(already done). Changes: proper names and categories for all in Settings > Keybindings. Use the actual
addon name for the category and a logical name for the keybinding. Keybindings in Addon > General >
Keybindings tab (follows global or character-specific from the keybindings menu, and should sync across
both)."

**Owner decisions already taken.** Each addon gets its own top-level category in Settings > Keybindings,
named after the addon (for example "Ka0s Bank Ledger"). Only the 7 windowed addons are in scope:
BankLedger, DpsRace, DropWatcher, LootHistory, MultiMeters, QuickComms and WhatGroup.

**Blizzard source used.** Gethe/wow-ui-source, branch `live`, at commit `15881d5` ("12.1.5 (70575)",
2026-10-23). Paths are cited as `wow-ui-source:<path>:<line>`, and the files were fetched raw from
`https://raw.githubusercontent.com/Gethe/wow-ui-source/live/<path>`.

**Collection standard.** Ka0s WoW Addon Standard v2.87.0 (2026-10-23).

---

## 1. Current state, per windowed addon

### 1.1 Bindings.xml, globals and buttons

Every addon has a root `Bindings.xml`. None is listed in the TOC; the client reads the file by name. All
of them use `category="ADDONS"`. Only the first `<Binding>` in each file carries a `header=`, and none
has a `default=`.

| Addon | `Bindings.xml` lines | Command(s) | Header and name globals (file:line) | Current label(s) |
|---|---|---|---|---|
| BankLedger | `BankLedger/Bindings.xml:2` | `CLICK BankLedgerToggleWindow:LeftButton` | `BankLedger/core/LauncherSetup.lua:154-155`. Header is `NS.BRAND_NAME` = "Ka0s Bank Ledger" (`:95`). | "Toggle the ledger window" |
| DpsRace | `DpsRace/Bindings.xml:8,9,12` | `CLICK DpsRaceToggleHud:LeftButton`, `CLICK DpsRaceToggleResults:LeftButton`, `CLICK DpsRaceArmToggle:LeftButton` | `DpsRace/core/LauncherSetup.lua:40-43`. Header is `L["Ka0s DPS Race"]`. | "Toggle race HUD", "Toggle results window", "Arm / cancel race" |
| DropWatcher | `DropWatcher/Bindings.xml:2` | `CLICK DropWatcherToggleWindow:LeftButton` | `DropWatcher/core/LauncherSetup.lua:44-45`. Header is `NS.BRAND`. | "Toggle Drop Watcher window" |
| LootHistory | `LootHistory/Bindings.xml:2` | `CLICK LootHistoryToggleWindow:LeftButton` | `LootHistory/core/LauncherSetup.lua:96-97`. Header is `NS.BRAND`. | "Toggle Loot History window" |
| MultiMeters | `MultiMeters/Bindings.xml:7` | `CLICK MultiMetersToggleWindows:LeftButton` | `MultiMeters/core/LauncherSetup.lua:161-162`. Header is `L["Ka0s Multi Meters"]`. | "Toggle meter windows" |
| QuickComms | `QuickComms/Bindings.xml:6-9,13` | `CLICK QuickCommsDial1..4:Toggle` (secure dial headers), `CLICK QuickCommsTogglePads:LeftButton` | `QuickComms/modules/Dial.lua:52-55` (header and dial labels) and `QuickComms/settings/SlashVerbs.lua:95` (pads label) | "Open Comms Dial 1".."4", "Toggle Comms Pads" |
| WhatGroup | `WhatGroup/Bindings.xml:3` | `CLICK WhatGroupTogglePopup:LeftButton` | `WhatGroup/modules/Frame.lua:1334-1335`. The header is the literal "Ka0s WhatGroup", not `NS.BRAND` and not passed through `L`. | "Toggle group popup" |

`.luacheckrc` declares the header global in `BankLedger/.luacheckrc:63`, `DropWatcher/.luacheckrc:20,40`,
`DpsRace/.luacheckrc:30` and `LootHistory/.luacheckrc:125` (that one is scoped to a single file). The
other three addons write it in some other way that luacheck accepts.

**The toggle buttons.** Each is a plain, named, hidden, non-secure `Button` registered with
`RegisterForClicks("AnyDown")`. Its `OnClick` asks the stood-down refusal first and then calls the
launcher's `toggleWindow` handler; `BankLedger/core/LauncherSetup.lua:139-149` is representative. The
exception is QuickComms' four dial bindings, which click **secure** dial headers with the `Toggle`
button (`QuickComms/modules/Dial_Secure.lua`). Those headers are QuickComms' Comms Dial feature, not a
launcher-§6 window toggle.

### 1.2 What the player sees today

Every Ka0s binding lands in **one** shared "AddOns" section. Each addon's `header=` row draws as a
**blank 25px spacer** rather than a title, so nothing labels the row "Toggle group popup" as
WhatGroup's. Section 2 shows why. This is very likely the problem the owner is reacting to.

### 1.3 Tests that cover the bindings

| Addon | Bindings.xml shape test | Labels test | Press while stood down (slash-commands-§7 step 8) |
|---|---|---|---|
| BankLedger | `tests/test_launcher.lua:819-827` asserts `header="BANKLEDGER"` and `category="ADDONS"` | `tests/test_launcher.lua:854-857` | `tests/test_disabled.lua:731` |
| DpsRace | `tests/test_launcher.lua:~90-105` counts the headers | `tests/test_launcher.lua:76-78`, `tests/test_slash.lua:348` | `tests/test_disabled.lua:324-341` |
| DropWatcher | `tests/test_bindings.lua:23-33` asserts `"DROPWATCHER"` and `"ADDONS"` | `tests/test_bindings.lua:75-80` | `tests/test_disabled.lua:247-248,293-294` |
| LootHistory | `tests/test_keybinding.lua:26-39` asserts `"LOOTHISTORY"` and `"ADDONS"` | `tests/test_keybinding.lua:68-75` | `tests/test_disabled.lua:651-652` |
| MultiMeters | `tests/test_launchersetup.lua:938-952` asserts `"MULTIMETERS"` and `"ADDONS"` | `tests/test_launchersetup.lua:894-896` | `tests/test_disabled.lua:557` |
| QuickComms | `tests/test_dial.lua:438-453` checks for `header="QUICKCOMMS"` | in `test_dial.lua` | `tests/test_disabled.lua:479-506` (uses `m.SetBinding`) |
| WhatGroup | `tests/test_launcher.lua:355-356` asserts `"WHATGROUP"` and `"ADDONS"` | `tests/test_launcher.lua:387-391,604` | `tests/test_disabled.lua:496,542` |

**Every one of these shape tests will go red** once `category` changes. That is intended: rewrite each
one to the new shape (section 5.3).

The headless mocks differ from addon to addon. QuickComms' `tests/wow_mock.lua:908-940` is the only full
binding model. It has `GetBindingAction`, a two-key `GetBindingKey`, a `SetBinding` that refuses in
combat, a `SaveBindings` that records the set it saved, and `GetCurrentBindingSet`. The shared kit
(`LibKa0s/tests/_kit/`) has no binding mock at all.

### 1.4 Docs that name the path

The path these docs spell will be wrong once each addon has its own category:

- `BankLedger/README.md:52` and `BankLedger/docs/settings-panel.md:178-179`: "Key Bindings → AddOns → Ka0s Bank Ledger".
- `DpsRace/docs/settings-panel.md:123-131`: "Key Bindings → AddOns → Ka0s DPS Race".
- `DropWatcher/README.md:49` and `DropWatcher/docs/settings-panel.md:59`.
- `LootHistory/README.md:54`: "Key Bindings > AddOns > Ka0s Loot History".
- `MultiMeters/docs/settings-panel.md:228`. The README has no binding line.
- `WhatGroup/README.md:36` and `WhatGroup/docs/settings-panel.md:515-516`.
- QuickComms already writes "Options → Keybindings → Ka0s Quick Comms": `README.md:31,34-35,131-132`,
  `docs/settings-panel.md:35`, the locale string at `settings/Share.lua:158`, and the comments at
  `modules/Dial.lua:18-21`, `settings/Dials.lua:34` and `settings/Schema.lua:229`. With
  `category="ADDONS"` that wording is **inaccurate today**: the real path is Keybindings → AddOns. The
  change makes it true.
- The `Bindings.xml` comments that say "under Key Bindings, AddOns": DpsRace `:2-7`, MultiMeters
  `:2-6` and WhatGroup `:2`.

### 1.5 The standard today

The rule is in `WowAddonStandards/standards/standards/launcher.md:116-148` (launcher-§6, "The Show
window key binding (MUST)"). The parts that matter here:

- Line 120: "The binding **MUST** be a `CLICK <Folder>Toggle<Window>:LeftButton` binding in the addon's
  root `Bindings.xml` (layout-§1), with `category="ADDONS"`, and with `header="<FOLDERUPPER>"` on the
  file's **first** `<Binding>` only."
- Lines 126-128: the XML example, with `header="<FOLDERUPPER>" category="ADDONS"`.
- Line 134: "`BINDING_HEADER_<FOLDERUPPER>` is the addon's brand name, `Ka0s <Name>` (launcher-§1)."
- Line 138: "No default key … The player chooses in the client's Key Bindings → AddOns menu."
- Line 141: "Documented. The README's `## Usage` names the binding and where to set it (Key Bindings →
  AddOns → `Ka0s <Name>`)."
- Lines 142-146: "Why this is not a library helper (recorded rejection, LibKa0s#58)". The client reads
  `Bindings.xml` only from the addon root; a helper would own about six lines; and a library writing
  `BINDING_HEADER_*` would split ownership of that global.
- Line 147: "Re-check if … a second binding per addon (*Locked*, *Test mode*) is ruled in. A vendored
  kit check (`test_bindings` …) is deferred with it."
- Anti-pattern #96 (`anti-patterns.md:125`) and step 8 (`slash-commands.md:324`).
- `options-ui.md` says nothing about key bindings.

### 1.6 Prior art: QuickComms already had, and retired, an in-panel key box

QuickComms added a Key box on 2026-10-20 (commits `fa474ab` and `db8f7a6`) and retired it on 2026-10-21
(`b902e35`, "The Binding tab is gone: the key is set only in Options -> Keybindings. Dial.BindKey, the key
validators and the unused Compat binding writers go with it."). The working code is still readable at
`db8f7a6`:

- `settings/Dials.lua:321-345`. AceGUI's `Keybinding` widget showing `GetBindingKey`. An `OnKeyChanged`
  that is refused puts the box back. The page re-reads the key on `OnShow` "so a key set in Options ->
  Keybindings shows on the way back".
- `modules/Dial.lua:84-130`, `rebind()` plus `Dial.BindKey`. It refuses in combat; unbinds every old key
  of the command; checks `GetBindingAction(key)` for a key it is about to take from another action;
  calls `SetBinding(key, command)` then `SaveBindings(GetCurrentBindingSet())`; and prints "%s was %s in
  WoW's key bindings; now it opens this dial."
- `core/Compat.lua:291-320`. `BindingKeys`, `SetBinding` (false in combat) and `SaveBindings` (the set
  in force), all guarded for secret values.
- `modules/Library.lua:1040-1090`. Key normalization (`ALT-CTRL-SHIFT-META-X`) and keys reserved by the
  dial.

The owner's smoke run passed on that code (QuickComms `cf44c98`, 2026-10-21), so the read, write, save
and sync loop has worked in the client once already. **What 015 asks for brings back an in-panel key
editor that QuickComms deliberately removed three days ago.** The owner should know this; the plan
should record it as superseding that decision, not quietly reverse it.

---

## 2. How retail turns `category=` into a Keybindings section

Source: `wow-ui-source:Interface/AddOns/Blizzard_SettingsDefinitions_Frame/Keybindings.lua`.

**The display name is `_G[category]` when that is a string, and the raw attribute text otherwise.**

```lua
-- Keybindings.lua:220-227
local function GetBindingCategoryName(cat)
	local loc = _G[cat];
	if type(loc) == "string" then
		return loc;
	end
	return cat;
end
```

The lookup is called as `cat = securecallfunction(GetBindingCategoryName, cat)` (`:248`). The
`securecallfunction` wrapper exists precisely so that reading an addon-written global cannot taint
Blizzard's list build. Binding labels are read the same way: `securecallfunction(GetBindingName,
action)` at `:204`, and `GetBindingName` returns `BINDING_NAME_<cmd>` or else the raw command
(`Blizzard_SharedXML/BindingUtil.lua:142-149`).

What follows from that:

- **The value does not have to be a global name.** Blizzard ships both forms. `Blizzard_PTRFeedback/
  Bindings.xml:2` uses the raw `category="PTR"`; Blizzard's own files use globals such as
  `category="BINDING_HEADER_PING_SYSTEM"` (`Blizzard_PingUI/Bindings.xml:3`) and
  `category="BINDING_HEADER_MOVEMENT"` (`Blizzard_FrameXML/Bindings_Standard.xml:4`). Today's
  `category="ADDONS"` resolves through the global `ADDONS` ("AddOns"), which is why every Ka0s binding
  shares one section.
- **The convention is `category="BINDING_HEADER_<X>"`, a global holding localized text.** Using a
  global keeps the name localizable and keeps the brand defined in one place, which is the module
  (launcher-§1). A raw `category="Ka0s Bank Ledger"` would work, since spaces are just text in an XML
  attribute and in a Lua table key, but it puts a display string in XML and cannot be localized.
- **There is no `BINDING_CATEGORY_` convention in the client.** Any global name works. Reusing
  `BINDING_HEADER_<FOLDERUPPER>`, which every addon already writes, declares in `.luacheckrc` and tests,
  is the zero-new-globals choice. A new `BINDING_CATEGORY_<X>` would need new luacheck declarations and
  tests for no client-side gain.

**`header=` draws as a blank spacer inside a category, not as a title.**

```lua
-- Keybindings.lua:251-257
if strsub(action, 1, 6) == "HEADER" then
	tinsert(bindingsCategories[cat].bindings, KeybindingSpacer);
elseif strsub(action, 1, 7) == "PREFACE" then
	tinsert(bindingsCategories[cat].bindings, {prefaceText = action});
else
	tinsert(bindingsCategories[cat].bindings, {bindingIndex, action});
end
```

Section 1.2 follows from this: today's `header="BANKLEDGER"` inside the shared "AddOns" section is an
empty row, and the brand never shows. Blizzard's own files have moved header names into comments
(`Bindings_Standard.xml:3`, `<!-- … header="MOVEMENT" -->`, and `Blizzard_PingUI/Bindings.xml:2`).
`Blizzard_Commentator/Bindings.xml:7` is the one that still uses a `header=` inside its own category, to
open a gap before a sub-block. In an addon-named category a header adds only a blank first row, so
**`header=` should be dropped.**

That claim rests on a reading of the source, not an in-game check; smoke-test it (section 5.6, KB-S2).
The legacy wiki text, "displayed under the last header specified previously" (warcraft.wiki.gg,
*Bindings.xml* and *Creating key bindings*), describes the pre-10.0 `KeyBindingFrame` and does not apply
in retail.

**Sections are ordered by first appearance, after a fixed Blizzard list.**

- `KeybindingsOverrides.AddBindingCategories` (`Blizzard_SettingsDefinitions_Frame/Mainline/
  KeybindingsOverrides.lua:3-30`) seeds the order: Movement, Interface, Action Bar, … Misc, Other.
- `AddBindingCategory` (`Keybindings.lua:235-240`) then gives each new category `nextOrder` in
  `GetBinding(index)` order (`:244-259`). In practice that is addon load order.

So each Ka0s category appears **after "Other"**, in load order. This matches the 2014 WoWInterface note
that "custom categories are placed at the bottom". The collection cannot control the position, and a
category with no bindings is skipped (`:268`).

**When the name is read.** `Register()` reads it once at settings registration (`:277-326`), and the
whole list is rebuilt on every `ADDON_LOADED` whose second argument (`containsBindings`) is true
(`:330-354`). An addon's `ADDON_LOADED` fires after all of its TOC files have run, so a global assigned
at file scope is set by then. Every Ka0s addon assigns at file scope. This only becomes a risk if an
addon ever assigns the label lazily.

**Names with spaces.** Binding commands may contain spaces and colons (`CLICK X:LeftButton`). The label
global is then `BINDING_NAME_CLICK X:LeftButton`, which can only be written with `rawset`, as every
addon already does. Category and header globals are identifiers.

**Search.** `CreateSearchableSettings` (`:179-218`) indexes every binding by its `GetBindingName` text,
whatever its category, so the Keybindings search box keeps finding the bindings.

---

## 3. Reading and setting a binding from an addon's own settings UI

### 3.1 API facts

**`GetBindingKey(command)`** returns `key1, key2`: the two slots the Blizzard UI shows
(`Blizzard_Keybindings.lua:105`, `:154`, `:417`). A key string is upper-case, with modifiers in
ALT-CTRL-SHIFT-META order (`BindingUtil.lua:116-134`, `CreateKeyChordStringUsingMetaKeyState`).
`GetBindingText(key)` gives the display form; Blizzard uses it at `Keybindings.lua:522` and
`BindingUtil.lua:88`.

**`GetBindingAction(key)`** returns the command a key is bound to, or `""` when it is free
(`Blizzard_Keybindings.lua:127`).

**`SetBinding(key [, command [, context]])`.** `command = nil` unbinds the key. warcraft.wiki.gg
*API_SetBinding*: "This function is **restricted**", "`#nocombat` - This cannot be called while in
combat", and "bindings are not saved without an explicit SaveBindings() call". It returns a truthy value
on success; Blizzard checks that return at `Blizzard_Keybindings.lua:167`.

**`SaveBindings(which)`** writes the live bindings to a set. `which` is `1`/`ACCOUNT_BINDINGS` or
`2`/`CHARACTER_BINDINGS` (`0` is the defaults). warcraft.wiki.gg *API_SaveBindings* says it "Triggers
UPDATE_BINDINGS". Blizzard always passes `GetCurrentBindingSet()`: `Blizzard_Keybindings.lua:144`
(`KeybindListener:Commit`) and `Blizzard_SettingsPanel.lua:310` (`CommitBindings`).

**`GetCurrentBindingSet()`** returns `Enum.BindingSet.Account` (1) or `Enum.BindingSet.Character` (2).
The "Character Specific Keybindings" checkbox is a proxy setting on exactly that value
(`Keybindings.lua:288-317`). Turning it **off** shows the confirm popup
`CONFIRM_DELETING_CHARACTER_SPECIFIC_BINDINGS` (`:6-17`, `:308-316`), because the account set
overwrites the character set.

**`UPDATE_BINDINGS`** is how Blizzard's own rows stay in sync. Each binding row registers it while
shown and calls `RenewBindings()` (`Blizzard_Keybindings.lua:272-306`); the panel calls
`RenewKeybinds()` on it as well (`Blizzard_SettingsPanel.lua:148-149`). Blizzard's right-click unbind
(`:434-440`) calls only `SetBinding` and never repaints the row by hand. That strongly implies
`SetBinding` fires `UPDATE_BINDINGS` too, not only `SaveBindings`; the wiki confirms the latter only.
Override-binding changes (`SetOverrideBinding*`, the `SetBindingClick` / `ClearBindings` calls in
QuickComms' secure dial) are also expected to fire it, so it can be frequent: debounce it.

**When Blizzard saves.** Blizzard's UI calls `SetBinding` immediately and saves at `Commit` (Apply or
Close, `Blizzard_SettingsPanel.lua:224-228`) and unconditionally in `SettingsPanel:OnHide` (`:209-221`):
`SaveBindings(bindingSet)` with `bindingSet` read from the checkbox. A binding our tab writes inside
the open settings window is therefore saved even if our own save failed, as long as Blizzard's close
path runs clean (section 3.2).

### 3.2 Combat and taint

The LibKa0s comment is at `LibKa0s/LibKa0s/Options.lua:344-353`; the case file is
`LibKa0s/tests/test_options_combat.lua:9-15`; the fix landed in `7ae1763`, LibKa0s v1.46.0:

> "Through minor 21 that OnShow CLOSED the settings window, running Blizzard's close-and-commit path
> from addon code, tainted (SaveBindings blocked, then ToggleGameMenu re-entering until C stack
> overflow) … Now nothing touches SettingsPanel, HideUIPanel, ToggleGameMenu or Settings.OpenToCategory
> in combat."

What it implies for 015:

1. **`SaveBindings` is blocked when it runs from tainted execution in combat.** In-game evidence shows
   it behaves as a protected call there, whatever the wiki says. `SetBinding` is `#nocombat` outright.
   **No key may be bound, cleared or saved in combat.** LibKa0s' combat lock already covers a page and
   refuses every write through the options surface in combat (`lib.__IsCombatLocked`,
   `Options.lua:362-366`). The keybind rows must ask that same predicate and must also **cancel a
   capture in progress at `PLAYER_REGEN_DISABLED`**.
2. **Addon code must never drive Blizzard's own save path.** That means no `SettingsPanel:Commit`,
   `Close`, `HideUIPanel(SettingsPanel)`, `ApplyButton:Click` or `Settings.SelectCharacterBindings` /
   `SelectAccountBindings`, and no writes to `KeybindListener` (a Blizzard global object). The
   tab saves its own write with `SaveBindings(GetCurrentBindingSet())` out of combat and leaves the
   panel's `OnHide` save to Blizzard.
3. **Do not reuse Blizzard's row template or `KeybindListener`.** `KeyBindingFrameBindingTemplate` is
   driven by a `bindingIndex` and by Settings initializers, and it writes `KeybindListener.pending` and
   `SettingsPanel` output text. Using it from addon code would taint the object Blizzard's own
   Keybindings page runs through, and through it the `OnHide` save. **Rejected.**
4. **Taint from writing a binding out of combat is not a concern.** Bindings live in the client.
   QuickComms ran exactly this write-and-save path out of combat with the smoke run passing (section
   1.6). The binding's target buttons are unchanged: plain buttons, and QuickComms' secure headers,
   whose secure state `SetBinding` does not touch.
5. **Keyboard capture.** Use `EnableKeyboard(true)` only while listening, and only out of combat. Do not
   call `SetPropagateKeyboardInput`, which is protected in combat. A frame that is listening with
   keyboard enabled swallows Escape, so Escape cancels the capture and does not close the settings
   window.

### 3.3 How Blizzard's UI behaves, which the tab should copy

From `Blizzard_Keybindings.lua`:

| Behaviour | Blizzard (file:line) | Tab should |
|---|---|---|
| Start a capture | Left-click a slot button starts `KeybindListener:StartListening(action, slot)`. A second click on the selected slot cancels. (`:424-433`) | Same |
| Cancel | Escape cancels when Escape is the game-menu key (`:89-92`). | Escape cancels. **AceGUI's `Keybinding` widget does the opposite: Escape *clears* (`AceGUIWidget-Keybinding.lua:60-61`).** |
| Clear a slot | Right-click unbinds that slot's key (`:434-440`). | Same, plus a visible Clear button (a right-click alone is hard to discover) |
| Ignored input | Meta keys alone, `UNKNOWN`, `BUTTON1`, `BUTTON2` (`BindingUtil.lua:21-25`, `:90-92`). Screenshot still fires (`:82-86`). | Same |
| Mouse buttons | `GetConvertedKeyOrButton` maps `MiddleButton` and `Button4..31` to `BUTTON3..31`; the wheel gives `MOUSEWHEELUP/DOWN` (`BindingUtil.lua:27-68`, `Blizzard_Keybindings.lua:14-16`). | Same, through the client's functions where they exist. AceGUI's widget stops at `BUTTON5` (`:89-100`). |
| Modifiers | `CreateKeyChordStringUsingMetaKeyState`: ALT, CTRL, SHIFT, **META** (`BindingUtil.lua:116-134`) | Same. AceGUI's widget has no META. |
| Bind | Unbind both of the action's old keys, then rebind them in order with the new key in the chosen slot (`:103-110`, `:176-188`) | Same slot semantics |
| Conflict | `UnbindKey` takes the key away from its previous action. If that leaves the other action with no key, it reports `KEY_UNBOUND_ERROR` / `PRIMARY_KEY_UNBOUND_ERROR` ("… Function is Now Unbound!") (`:123-141`, `Blizzard_SettingsPanel.lua:971-974`). It never asks first. | Same: take the key and show an inline line naming the action that lost it, through `GetBindingName(oldAction)` |
| Feedback | `KEY_BOUND` on success, `KEYBINDINGFRAME_MOUSEWHEEL_ERROR` on a failed rebind (`Blizzard_SettingsPanel.lua:976-982`) | Same client strings, so the wording matches the client's own |
| Save | `SaveBindings(GetCurrentBindingSet())` (`:143-145`) | Same, right after each change |

### 3.4 "Follows global or character-specific" and "syncs across both"

Both UIs read and write the same client store, and both save to `GetCurrentBindingSet()`. That gives
the owner's two requirements:

- **The tab follows the set the player chose.** It never offers its own account/character switch.
  Switching from character to account destroys the character set behind a Blizzard confirm, and that
  must stay Blizzard's. The tab shows one line: "Saved for: all characters" or "Saved for: this
  character only", followed by "(Options → Keybindings → Character Specific Keybindings)".
- **Changes show in both places.** A key set in the tab appears on Blizzard's rows through their own
  `UPDATE_BINDINGS`. A key set in Blizzard's page, or a switch of binding set (which goes through
  `LoadBindings` and fires `UPDATE_BINDINGS`), repaints the tab through its `UPDATE_BINDINGS` listener,
  and through a re-read on the page's `OnShow` as a fallback. QuickComms used that fallback at
  `db8f7a6:settings/Dials.lua:409-412`.

---

## 4. What already exists in the collection

**The AceGUI `Keybinding` widget is vendored in all 7.**
`<Addon>/libs/AceGUI-3.0/widgets/AceGUIWidget-Keybinding.lua` (widget version 27) is listed in each
`libs/AceGUI-3.0/AceGUI-3.0.xml`, so `AceGUI:Create("Keybinding")` works in every one. Its behaviour:

- Click toggles capture. It enables keyboard, mouse wheel and gamepad input and shows a message frame.
  `OnKeyDown` builds `ALT-CTRL-SHIFT-` plus the key and fires `OnKeyChanged(key)` (`:28-87`).
- **Escape fires `OnKeyChanged("")`, which clears.** Blizzard cancels instead.
- No META modifier. Only `BUTTON3`..`BUTTON5` are captured. `LeftButton` and `RightButton` are
  swallowed (`:89-100`).
- **It has no binding semantics at all.** It never calls `SetBinding` or `SaveBindings`, has no
  conflict check, no second slot and no `UPDATE_BINDINGS` handling. The host does all of that, as
  QuickComms did.
- Its message text is a hard-coded English literal, "Press a key to bind, ESC to clear the binding or
  click the button again to cancel." (`:228`), so it breaks the localization rule.
- Its `msgframe` is a `UIParent` child at strata `FULLSCREEN_DIALOG`, frame level 1000, with
  `SetToplevel(true)` (`:219-225`). That is relevant to item 030 (strata): it sits above everything,
  the settings window included.
- The kit's AceGUI fake has no `SetKey` (`db8f7a6:settings/Dials.lua:325`), so QuickComms had to guard
  that call.

**LibKa0s has no key-capture surface and no binding code.** There is no `UPDATE_BINDINGS`,
`SetBinding`, `GetBindingKey` or `SaveBindings` anywhere in `LibKa0s/LibKa0s/*.lua`; the only mention is
the comment cited in section 3.2. The kit has no binding mock either.

**The Options API can host a Keybindings tab today**
(`LibKa0s/docs/api/Options/version-29.2.34.2.5.9.1.7.4.2.1-docs.md`):

- **Host tabs (T4).** The fifth argument of `O.RenderTabbedSchema` takes
  `tabs = { { key, label, tooltip, before, render = function(ctx, rows) } }`. A key that matches no
  schema group is placed before `before`, or last when `before` is absent (doc lines ~436-447).
  DropWatcher (`settings/Pages.lua:41-47`) and QuickComms (`settings/Editors.lua:676`) already use it.
- **`O.RenderGrid(ctx, items, parent, opts)` with `make` items (W34)** draws custom widgets in the flow
  (doc lines ~158-173).
- **Hand-drawn strips.** LootHistory's General page draws its own strip from a `GENERAL_TABS` list of
  `{ key }` and `{ key, build = fn }` entries (`LootHistory/settings/Panel.lua:956-1035`). A
  Keybindings entry fits there as `{ key = "Keybindings", build = … }`, and
  `tests/test_panel.lua` pins the list against the schema groups.

How each General page is drawn:

| Addon | General page drawn by | Where the tab goes |
|---|---|---|
| DpsRace | `settings/General.lua:153`, `RenderTabbedSchema(c, PAGE, afterGroup)` | add `opts.tabs` |
| MultiMeters | `settings/General.lua:248`, `RenderTabbedSchema` | add `opts.tabs` |
| DropWatcher | `settings/Panel.lua:73`, `RenderTabbedSchema(…, { rerender = renderGeneral })` | add `opts.tabs` |
| QuickComms | `settings/Panel.lua:91`, `RenderTabbedSchema(c, "general", AFTER_GROUP)` | add `opts.tabs` |
| WhatGroup | `settings/Panel.lua:326`, `RenderTabbedSchema(c, "general", AFTER_GROUP)` | add `opts.tabs` |
| BankLedger | `settings/Panel.lua`, which partitions through `O.RenderTabbedSchema` (`:22`); its Filters tab is a renderer-only row with a sub-strip (`:440-475`) | add `opts.tabs` (to be confirmed against `Panel.lua` at implementation time) |
| LootHistory | hand-drawn `O.TabStrip` from `GENERAL_TABS` (`settings/Panel.lua:978-985`) | add a `build` entry |

Every addon hand-writes a degradation stub of the Options instance (for example
`DpsRace/settings/OptionsSetup.lua:110`, `DropWatcher/settings/OptionsSetup.lua:38`,
`QuickComms/settings/OptionsSetup.lua:49`). A new instance member must be added to each stub, and
`Kit.assertSurfaceParity` turns that case red on re-vendor until it is.

---

## 5. Recommended design

### 5.1 The LibKa0s surface: `O.KeybindingsTab` and `O.KeybindRows`

A new file `LibKa0s/LibKa0s/OptionsKeybinds.lua`, minor 1, inside the `LibKa0s-Options-1.0` major. It
loads after `OptionsCombat.lua`, because it uses the combat predicate, and it extends the version key and
`lib.MODULES` like every other Options file. It is attached the same way `OptionsTabs` is
(`lib.__AttachKeybinds(O, d)`). It adds two instance members.

```lua
--- A host-tab entry for O.RenderTabbedSchema's opts.tabs (or a hand-drawn strip's build).
--- @param spec table
---   bindings  { { command = "CLICK BankLedgerToggleWindow:LeftButton", tooltip = L["…"] }, … }  (order = row order)
---   key       tab key, default "Keybindings"; label default L-less "Keybindings" via descriptor locale
---   before    optional tab key to sit before (default: last)
---   intro     optional string drawn above the rows
--- @return { key, label, tooltip, before, render = function(ctx) } 
function O.KeybindingsTab(spec) end

--- Draw the rows into `parent` (default: the page scroll). Usable by a hand-drawn strip.
--- @return rows table (for tests), or nil when the binding API is absent (one honest TextRow instead)
function O.KeybindRows(ctx, spec, parent) end
```

**Each row shows four things:**

1. A label. **No label is passed in.** The row reads `GetBindingName(command)`, so it shows the exact
   `BINDING_NAME_` text Blizzard's page shows, and the two names cannot drift apart.
2. **Key 1** and **Key 2** slot buttons, showing `GetBindingText(key)`, or `NOT_BOUND` when the slot is
   empty. Two slots, because Blizzard keeps two per action and a one-slot box would hide a second key
   set in Blizzard's page. That would break "sync across both".
3. A **Clear** button that unbinds both slots.
4. When the row has a tooltip, it explains how to bind.

**Below the rows** there are two lines. The first says which binding set is in force (section 3.4). The
second is the outcome of the last action: the client's own `KEY_BOUND`, or `KEY_UNBOUND_ERROR` naming
the action that lost its key, or "Key bindings can be changed after combat."

**Capture** uses one library-level listener frame, `lib.__keybindListener`, which persists across a
LibStub upgrade the same way `lib.__parkFrame` does:

- Left-click a slot to start listening, and click it again to cancel. Only one row can listen at a time.
- **Escape cancels**, as in Blizzard's UI. A right-click on a slot clears that slot.
- A key press is turned into a key string with `GetConvertedKeyOrButton` and
  `CreateKeyChordStringUsingMetaKeyState`. When the client lacks them (the headless harness, older
  flavours) a bundled copy of the same logic does the job, META included.
- `IsKeyPressIgnoredForBinding` decides which presses to ignore. Mouse buttons 3-31 and the mouse wheel
  can be captured.
- Listening stops on the page's `OnHide`, on a tab change, on `PLAYER_REGEN_DISABLED` and on a
  structural refresh.

**Writing a key** uses one model function, `lib.__keybindSet(command, slot, key)`. It is pure apart from
the client API, so it can be tested without frames.

1. Refuse when `lib.__IsCombatLocked()`.
2. Read the current keys with `key1, key2 = GetBindingKey(command)`.
3. Unbind both of them.
4. Take the new key from its previous action: read `old = GetBindingAction(key)`, call
   `SetBinding(key, nil)`, and record whether `old` is now left with no key.
5. Rebind in slot order, using Blizzard's `RebindKeysInOrder` semantics. If `SetBinding` fails, put the
   old key back.
6. Call `SaveBindings(GetCurrentBindingSet())`.
7. Return `ok`, the displaced action and a reason.

`lib.__keybindClear(command, slot|nil)` works the same way.

**Syncing** uses one library-level `UPDATE_BINDINGS` registration, held **only while a keybind row is
on screen**. That is the same discipline as the combat frame (`lib.__syncCombatEvents`). Each event
repaints every row on screen, debounced to one repaint per frame. The page's `OnShow` re-reads the keys
as a fallback.

**Rules the surface follows:**

- It never touches `SettingsPanel`, `KeybindListener`, `Settings.*BindingSet*` or `HideUIPanel`.
- It sets no default key.
- It writes no `BINDING_*` global, so launcher-§6's reason "a library writing `BINDING_HEADER_*` would
  split ownership" still holds.
- It does not edit `Bindings.xml`, which stays per addon.

**When the API is absent** (for example, a future flavour with no `SetBinding`), the tab draws one text
row pointing at Options → Keybindings, as the Options major does when AceGUI is missing.

**Why not reuse AceGUI's `Keybinding` widget:**

- Escape clears instead of cancelling.
- No META, and mouse buttons stop at 5.
- The message text is English-only.
- Its message frame sits at FULLSCREEN_DIALOG, level 1000, toplevel.
- It has one slot and no binding semantics.

Wrapping it would mean patching its scripts on a pooled widget, which options-ui-§19 forbids ("leave
nothing on a widget's frame"). Instead, build each row from AceGUI `SimpleGroup`, `Label` and `Button`
widgets, plus the one library listener frame, which owns no pooled frame. Confidence: medium-high.
Using the AceGUI widget would be about 40% less code, but it breaks Blizzard parity on Escape, and that
key matters most.

### 5.2 What each addon declares

DropWatcher:

```lua
-- settings/Panel.lua (DropWatcher; the same shape in the five RenderTabbedSchema hosts)
Helpers.RenderTabbedSchema(c, "general", AFTER_GROUP, nil, {
  rerender = renderGeneral,
  tabs = { O.KeybindingsTab({ bindings = {
    { command = "CLICK DropWatcherToggleWindow:LeftButton", tooltip = L["Shows or hides the drop feed."] },
  } }) },
})
```

LootHistory instead adds `{ key = "Keybindings", build = function(ctx) O.KeybindRows(ctx, SPEC) end }`
to `GENERAL_TABS`. **The command list should come from one table per addon** (for example
`NS.BINDINGS`), declared beside the button in the module that creates it. Both the tab and the tests
read that table, and a test compares it against the `<Binding name=…>` lines in `Bindings.xml`.

Per-addon tab content:

- BankLedger: 1 row.
- DpsRace: 3 rows: HUD, Results, Arm/cancel.
- DropWatcher: 1 row.
- LootHistory: 1 row.
- MultiMeters: 1 row.
- QuickComms: 5 rows: Toggle Comms Pads, then Open Comms Dial 1-4. For the dial rows, an `intro` line
  says that a dial's key follows its place in the dial list (`modules/Dial.lua:18-24`).
- WhatGroup: 1 row.

Tab placement: **last** on the General page (`before` is nil). Master controls stays first, as
options-ui-§15 requires. Final placement is item 020's call.

### 5.3 Bindings.xml and global changes, per addon

**The shape.** Every `<Binding>` gets `category="BINDING_HEADER_<FOLDERUPPER>"`, and `header=` is
removed:

```xml
<Bindings>
  <Binding name="CLICK BankLedgerToggleWindow:LeftButton" category="BINDING_HEADER_BANKLEDGER"/>
</Bindings>
```

| Addon | New category value | Lines changed | Global (unchanged name) |
|---|---|---|---|
| BankLedger | `BINDING_HEADER_BANKLEDGER` | 1 | `NS.BRAND_NAME` |
| DpsRace | `BINDING_HEADER_DPSRACE` | 3 | `L["Ka0s DPS Race"]` |
| DropWatcher | `BINDING_HEADER_DROPWATCHER` | 1 | `NS.BRAND` |
| LootHistory | `BINDING_HEADER_LOOTHISTORY` | 1 | `NS.BRAND` |
| MultiMeters | `BINDING_HEADER_MULTIMETERS` | 1 | `L["Ka0s Multi Meters"]` |
| QuickComms | `BINDING_HEADER_QUICKCOMMS` | 5 | `NS.BRAND` |
| WhatGroup | `BINDING_HEADER_WHATGROUP` | 1 | the literal "Ka0s WhatGroup". **Change it to `NS.BRAND`** (or the brand constant) so it cannot drift. |

**No player loses a key.** The client stores a key against the binding's **name**, not its category or
header, and no name changes. Button names stay permanent (launcher-§6).

**Labels.** In an addon-named category, a label that repeats the addon's name is noise. Proposed labels,
with a confidence for each:

| Addon | Today | Proposed | Confidence |
|---|---|---|---|
| BankLedger | Toggle the ledger window | Toggle ledger window | 0.7 (drops the article, for parity with the others) |
| DpsRace | Toggle race HUD / Toggle results window / Arm / cancel race | Toggle race HUD / Toggle results window / Arm or cancel race | 0.6 |
| DropWatcher | Toggle Drop Watcher window | Toggle drop feed (ADDONS.md names the window "the drop feed") | 0.6 |
| LootHistory | Toggle Loot History window | Toggle history browser (ADDONS.md: "the History browser") | 0.6 |
| MultiMeters | Toggle meter windows | keep | 0.9 |
| QuickComms | Toggle Comms Pads / Open Comms Dial n | keep | 0.9 |
| WhatGroup | Toggle group popup | keep | 0.9 |

A label is a locale key, so changing one means editing `locales/enUS.lua`. The existing tests assert the
English strings and need the same edit (for example `BankLedger/tests/test_launcher.lua:857` and
`LootHistory/tests/test_keybinding.lua:75`).

**Tests to change.**

- Rewrite the shape tests listed in section 1.3 to assert:
  - `category="BINDING_HEADER_<FOLDERUPPER>"` on **every** `<Binding>`;
  - **no** `header=` and no `default=`;
  - the `<Binding>` names equal `NS.BINDINGS`;
  - each name has a `BINDING_NAME_` label;
  - `_G[category] == NS.BRAND`.
- DpsRace's header count becomes 0.
- **Comments and docs.** Rewrite the `Bindings.xml` comments, the README `## Usage` lines and the
  `docs/settings-panel.md` rows in section 1.4. The path becomes "Options → Keybindings → Ka0s <Name>",
  and "or General → Keybindings in this addon's settings" is added.

### 5.4 Test strategy for the headless harness

**Kit.** Add `tests/_kit/mock_bindings.lua`, ported from `QuickComms/tests/wow_mock.lua:908-940`. It
models:

- `bindingActions` / `bindingKeys`;
- `GetBindingKey` returning both slots;
- `GetBindingAction`, which returns `""` for a free key;
- `SetBinding`, which refuses in combat, records the refusal and fires `UPDATE_BINDINGS`;
- `SaveBindings(set)`, which refuses in combat, records the set and fires `UPDATE_BINDINGS`;
- `GetCurrentBindingSet` / `bindingSet`, with a `LoadBindings` that switches the set and fires the event;
- `GetBindingText` (identity) and `GetBindingName`, which reads `BINDING_NAME_`;
- `NOT_BOUND`, `KEY_BOUND` and `KEY_UNBOUND_ERROR`.

QuickComms then drops its own copy when it re-vendors. **Also consider a shared kit check**,
`Kit.assertBindingsXml(path, { category = "BINDING_HEADER_X", commands = NS.BINDINGS, brand = NS.BRAND })`.
It is exactly the "vendored kit check (`test_bindings` …)" that launcher-§6 (line 147) deferred until a
second binding per addon is ruled in. DpsRace and QuickComms already ship more than one, so the trigger
has fired.

**Library cases** (`LibKa0s/tests/test_options_keybinds.lua`):

- `__keybindSet`: slot 1 or 2 on a command with zero, one or two keys; slot order kept; old keys unbound.
- Taking a key from another action reports that action by name, and only when it is left with no key.
- A failed `SetBinding` restores the old key.
- `SaveBindings` is called once with `GetCurrentBindingSet()` (1 and 2 both covered).
- Combat: refused, with no `SetBinding` or `SaveBindings` call; a capture in progress is cancelled at
  `PLAYER_REGEN_DISABLED`.
- Capture: a key with modifiers gives `ALT-CTRL-SHIFT-X`. Escape cancels without writing. A meta key
  alone, `BUTTON1` or `BUTTON2` is ignored. A right-click clears the slot. The mouse wheel and
  `Button4` give `MOUSEWHEELUP` and `BUTTON4`.
- Sync: an external `SetBinding` followed by `UPDATE_BINDINGS` repaints the row text. Several events in
  one frame give one repaint. There is no registration while no row is on screen.
- **Never touches the settings window.** Run every case under the `SettingsPanel` recorder from
  `test_options_combat.lua`, so it fails if the library reads or calls `SettingsPanel`, `HideUIPanel`
  or `KeybindListener`.
- Pooling hygiene (options-ui-§19): after `ClearScroll`, no script is left on any released widget.
- The degradation path: with no `SetBinding`, one text row is drawn and nothing else.
- Regenerate the member manifest (`tools/gen-api-members.lua`); `test_versioning` covers it.

**Per-addon cases:**

- The General page's tab strip includes "Keybindings".
- Its rows equal `NS.BINDINGS`, in order.
- The labels shown equal the `BINDING_NAME_` globals.
- Binding a key through the tab makes `GetBindingKey` return it.
- The `Bindings.xml` shape check (section 5.3).
- The degradation stub carries the two new members (`assertSurfaceParity`).
- Step 8 is unchanged: pressing the button while stood down still refuses.

### 5.5 Standard changes

**launcher-§6** (`launcher.md:116-148`):

- Line 120 and the example at 126-128: `category="BINDING_HEADER_<FOLDERUPPER>"` on **every**
  `<Binding>`, and **no** `header=` attribute. Give the reason: the retail Keybindings page groups by
  `category`, reads its name from `_G[category]`, and draws a `header` as a blank spacer, citing
  `Keybindings.lua:220-227,251-257`. An addon that already ships bindings uses the same category on
  every line.
- Line 134: `BINDING_HEADER_<FOLDERUPPER>` is the brand name, and **it is also the category's title**.
  It is assigned at file scope, never lazily, because the client reads it at `ADDON_LOADED`.
- Lines 138 and 141: the path becomes "Options → Keybindings → `Ka0s <Name>`", and the in-addon
  Keybindings tab is named beside it.
- Lines 142-146 (the recorded rejection) need a sentence that separates the two things. The
  `Bindings.xml` file and its globals stay per addon, and that rejection stands. The **settings-panel
  editor** is a library surface (`O.KeybindingsTab`), because it is high-content (capture, slot
  semantics, conflicts, combat, sync) and identical in 7 addons. The rejection did not cover it.
- Line 147: record that the re-check trigger fired, since DpsRace and QuickComms ship more than one
  binding, and that the kit check is now adopted.
- Anti-pattern #96: add "a `category` other than `BINDING_HEADER_<FOLDERUPPER>`, a `header=` attribute,
  or a category global that is not the brand name". Add a new anti-pattern for a settings key editor
  that writes in combat, offers its own account/character switch, closes or commits Blizzard's
  settings window, or reuses Blizzard's `KeybindListener` or binding template.

**options-ui**, a new section, "The Keybindings tab (MUST, for an addon that ships launcher-§6
bindings)":

- The General page carries a `Keybindings` tab drawn by `O.KeybindingsTab`, listing every binding in
  the addon's `Bindings.xml` in file order.
- Its labels come from `GetBindingName`.
- It writes the client's own bindings and saves them to the set in force. It never keeps a binding in
  SavedVariables or a profile, so a profile copy, a reset or an import never carries a key. That
  matches QuickComms' "shared dials arrive without a key".
- It follows Blizzard's Escape, right-click and conflict behaviour, refuses in combat, and repaints on
  `UPDATE_BINDINGS`.
- Cross-reference options-ui-§2 (combat), §13 (tabbed pages), §15 (Master controls stays first) and §19
  (pooling).
- **Reset all settings and the Defaults button do not touch key bindings.** They are client state, not
  addon settings. Say so in the tab's intro line.

**ADDONS.md** is unaffected, beyond the bindings already listed. **Version:** a minor bump of the
standard (2.88.0). Commencement is each addon's next release.

### 5.6 Risks

1. **The header-as-spacer behaviour and the category title rest on reading the source.** Both are
   verified against the 12.1.5 source, but they need an in-game smoke test.
   - KB-S1: each addon's own section appears, titled "Ka0s <Name>".
   - KB-S2: no blank first row.
   - KB-S3: a key the player already had survives the change.
2. **`SaveBindings` under taint.** Calling it from addon code out of combat is the same as QuickComms'
   smoke-passed path. In combat it would be blocked. Mitigation: refuse before calling, cancel any
   capture at `PLAYER_REGEN_DISABLED`, and leave the panel's own `OnHide` save to Blizzard. Smoke test:
   bind in the tab, `/reload`, and confirm the key persisted in both the account set and the character
   set.
3. **Taking a key silently.** Blizzard takes a key from another action without asking, and the tab
   copies that. A player who binds, say, `M` in our tab loses the world map's key. Mitigation: show the
   client's own `KEY_UNBOUND_ERROR` line inline. A confirm step would diverge from Blizzard, so it is not
   recommended (confidence 0.7). Revisit if the owner wants one.
4. **Escape and keyboard capture inside the settings window.** While a capture is listening, our frame
   must take Escape before the settings window does. If keyboard input propagates, Escape would close
   the window mid-capture. Test this in the client. Never call `SetPropagateKeyboardInput`, which is
   protected in combat.
5. **The `UPDATE_BINDINGS` rate.** It also fires for override bindings: QuickComms' dial calls
   `SetBindingClick` / `ClearBindings` on every open and close, and other addons fire it too. Hold the
   registration only while a row is on screen, and debounce the repaint.
6. **Reversing a decision.** QuickComms removed its in-panel key box on 2026-10-21 (`b902e35`). The
   bundle should record that 015 supersedes that decision, so a later audit does not read the new tab
   as a regression of that commit.
7. **Load-order position is not controllable.** Ka0s categories appear after "Other", in addon load
   order, and cannot be grouped or sorted by the collection.
8. **Every `Bindings.xml` shape test goes red** across 7 repos, and the stubs need the new members.
   That is planned churn, not a defect, but every repo's green gate depends on it landing in the same
   item as the XML change.
9. **Character-specific semantics.** If the player switches the binding set while our tab is open, the
   tab repaints from `UPDATE_BINDINGS` (through `LoadBindings`). The tab must never cache keys.
10. **Strata (item 030).** If the AceGUI widget were used, its message frame (FULLSCREEN_DIALOG, level
    1000, toplevel) would be one more out-of-family strata in every addon. The custom row avoids it.
    Put any capture hint inside the row, not in a floating frame.

---

## Sources

- Gethe/wow-ui-source, `live` at commit `15881d5` (12.1.5.70575):
  - `Interface/AddOns/Blizzard_SettingsDefinitions_Frame/Keybindings.lua`
  - `Interface/AddOns/Blizzard_SettingsDefinitions_Frame/Mainline/KeybindingsOverrides.lua`
  - `Interface/AddOns/Blizzard_Settings_Shared/Blizzard_Keybindings.lua`
  - `Interface/AddOns/Blizzard_Settings_Shared/Blizzard_SettingsPanel.lua`
  - `Interface/AddOns/Blizzard_SharedXML/BindingUtil.lua`
  - `Interface/AddOns/Blizzard_FrameXML/Bindings_Standard.xml`
  - `Interface/AddOns/Blizzard_PingUI/Bindings.xml`
  - `Interface/AddOns/Blizzard_Commentator/Bindings.xml`
  - `Interface/AddOns/Blizzard_PTRFeedback/Bindings.xml`
  - Repository: <https://github.com/Gethe/wow-ui-source>
- warcraft.wiki.gg:
  - [API SetBinding](https://warcraft.wiki.gg/wiki/API_SetBinding)
  - [API SaveBindings](https://warcraft.wiki.gg/wiki/API_SaveBindings)
  - [Bindings.xml](https://warcraft.wiki.gg/wiki/Bindings.xml)
  - [Creating key bindings](https://warcraft.wiki.gg/wiki/Creating_key_bindings)
- WoWInterface forum note on custom `category` values and their placement:
  <https://www.wowinterface.com/forums/showthread.php?p=296684>, found by web search; a secondary
  source only.
