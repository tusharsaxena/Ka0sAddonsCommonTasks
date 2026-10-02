=================== LibKa0s#41
Core.MakeResizable has no lock gate, and the first host to adopt it needs one
[enhancement,state:triaged,severity:low]
## What

A suspect shape found by the v1.66.0 consumer census (#9), filed so the contract is settled before a first host adopts it.

`Core.MakeResizable(frame, opts)` has **no host consumer**: only the library's console, copy window and perf panel call it. Three hosts still hand-roll the grip, and the census files an adoption issue in each (BankLedger, LootHistory, MultiMeters). One of them cannot adopt it as it stands:

- **LootHistory gates its resize on *Lock frame*** (`modules/Browser.lua:1069-1071`, options-ui-§15: "both change the window's geometry"). `MakeResizable`'s `opts` (`minWidth` / `minHeight` / `maxWidth` / `maxHeight` / `widthOnly` / `onResize`) have no way to refuse a resize. The OnMouseDown handler (`LibKa0s/Core.lua`, `wireGrip`) always calls `StartSizing`.

## The question

Should `opts` take a predicate, for example `opts.canResize = function() return not locked end`, read at mouse-down? Or should a locked host hide the grip, which the library answers as `frame.resizeGrip`? The second needs no new field, but the host then has to re-show the grip on every lock change. A library-owned predicate keeps that in one place. Additive within `-1.0` either way.

## Library doc

`docs/api/Core/version-9-docs.md`, *The resize grip*. Also `docs/api/CONSUMERS.md`.

---
*Filed by GI-LK-13 of Ka0sAddonsCommonTasks/docs/2026-10-01-GITHUB_ISSUE_PASS (LibKa0s#9 census)*

=================== LibKa0s#42
Options descriptor addonName has no consumer, so every IdList help mark draws the fallback glyph
[enhancement,state:triaged,severity:low]
## What

A suspect shape found by the v1.66.0 consumer census (#9), filed so the contract is settled before a first host adopts it.

The **Options descriptor's optional `addonName`** is the only route to the shipped `media/icons/info.tga` art for `IdList` help marks (`LibKa0s/OptionsIdList.lua:463-471`, `idHelpIcon`). **No host passes it to `lib:New`**. So every help mark in all three `IdList` hosts (AuraMaster `settings/Filters.lua:673` and `settings/GeneralSpells.lua:855`, BankLedger `settings/Panel.lua:388`, LootHistory `settings/Panel.lua:336`) draws the client's fallback glyph (`ID_HELP_FALLBACK`). The document, though, describes the `info` art as the default.

## Why it is a shape question rather than a host task

Every other major that draws collection art takes `addonName` (DebugLog: all 11 hosts pass it; Perf defaults it to `name`). Options has no `name` to default from. The field is optional, and its absence costs nothing visible except the art. So nobody passes it, and nothing tells anyone it is missing. The options:

1. Default it from something every Options descriptor already carries, as Perf defaults `addonName` to `name`.
2. Keep it optional and tell the hosts: one line in each Options seam.
3. Accept the fallback glyph as the real default and correct the document.

Additive-only either way (`-1.0`). Nothing is renamed or removed.

## Library doc

`docs/api/Options/version-27.2.34.2.2.8.1.7.4.2-docs.md`, *Reaching the art across a major boundary*. Also `docs/api/CONSUMERS.md`.

---
*Filed by GI-LK-13 of Ka0sAddonsCommonTasks/docs/2026-10-01-GITHUB_ISSUE_PASS (LibKa0s#9 census)*

=================== AbsorbTracker#33
Adopt LibKa0s Slash.SplitVerb, Slash.ProfileNames and Core.SECRET in place of the host copies at settings/Slash.lua and modules/Diagnostics.lua
[enhancement,state:triaged,severity:low]
## What

The census of LibKa0s v1.66.0 finds three zero-consumer exports that this addon duplicates.

### 1. `Slash.SplitVerb(rest)`: the verb split

No host calls it. It lowercases the verb and keeps the remainder's case, which is exactly what this addon spells inline:

- `settings/Slash.lua:373-374` (`runDebug`) and `:589-590` (`runProfile`) both run `(rest or ""):match("^(%S*)%s*(.*)$")` and then `:lower()` the verb.

### 2. `Slash.ProfileNames(store)`: the profile list

No host calls it by name. `Sl:CliProfile("")` lists through it in every host, including this one: the bare `/at profile` at `settings/Slash.lua:594`. But `/at profile list` (`PROFILE_VERBS.list`, `settings/Slash.lua:522-529`) still prints its own list from `db:GetProfiles()`. That list is unsorted, and it can omit the current profile, which `ProfileNames` always lists. So the two routes to the same list can disagree.

### 3. `Core.SECRET`, the `"<secret>"` sentinel

`modules/Diagnostics.lua:73` (`secretSafe`) returns the literal `"<secret>"` outside the degradation stub. The library exports the constant so a host's copy cannot drift.

## Library doc

`LibKa0s/docs/api/Slash/version-19.1-docs.md`, sections *The sub-command vocabulary* and *The profile verb* (`lib.ProfileNames`). `LibKa0s/docs/api/Core/version-9-docs.md`, section *Lib-level surface* (`SECRET`). Also `LibKa0s/docs/api/CONSUMERS.md`.

---
*Filed by GI-LK-13 of Ka0sAddonsCommonTasks/docs/2026-10-01-GITHUB_ISSUE_PASS (LibKa0s#9 census)*

=================== BankLedger#21
Adopt LibKa0s Core.MakeResizable in place of the host copy at modules/Browser.lua and modules/SessionWindow.lua
[enhancement,state:triaged,severity:low]
## What

`LibKa0s-Core-1.0` exports `MakeResizable(frame, opts)` (Core minor 9). The census of LibKa0s v1.66.0 finds **no host that calls it**. The library's own console, copy window and perf panel are its only callers. This addon still builds the same bottom-right grip by hand on both of its windows.

## Evidence (v1.66.0 vendored, branch `feat/2026-10-01-github-issue-pass`)

- `modules/Browser.lua:1018` calls `SetResizable(true)` and sets the bounds through the `SetResizeBounds` / `SetMinResize` ladder at `:1020-1024`. `:1101-1112` builds a 16x16 `Button` with the chat size-grabber art, and its OnMouseDown / OnMouseUp run `StartSizing("BOTTOMRIGHT")` / `StopMovingOrSizing()`, then `B:SaveGeometry()`.
- `modules/SessionWindow.lua:482` and `:557-568` repeat the same thing for the session window, with `SW:SaveGeometry()`.

`Core.MakeResizable` does the same work: `SetResizable`, the same bounds ladder, a 16x16 grip with the same art, and `StartSizing` / `StopMovingOrSizing`. On top of that it hooks `OnSizeChanged` and keeps the frame's user-placed flag as it was. The host's geometry save maps onto `opts.onResize(w, h)`.

## Library doc

`LibKa0s/docs/api/Core/version-9-docs.md`, section *The resize grip*. Also `LibKa0s/docs/api/CONSUMERS.md`, the v1.66.0 census row for `lib.MakeResizable`.

## Notes

- Adopting it is optional. Nothing here is broken. The cost is two hand-rolled copies of a grip the library already publishes, and the library's copy is pinned only by the library's own suite.
- The library's grip sits at `-1, 1` inside the 1px edge, where this addon's sits at `-2, 2`. Check the size label's inset (`modules/Browser.lua:1085`) when switching.

---
*Filed by GI-LK-13 of Ka0sAddonsCommonTasks/docs/2026-10-01-GITHUB_ISSUE_PASS (LibKa0s#9 census)*

=================== ConsumableMaster#44
Adopt LibKa0s Slash.SplitVerb, FindCommand and CommandRows in place of the host copy at core/SlashCommands.lua
[enhancement,state:triaged,severity:low]
## What

The census of LibKa0s v1.66.0 finds three zero-consumer exports that this addon duplicates. They are LibKa0s-Slash-1.0's sub-command vocabulary. The library added it because "two hosts had already copied byte-identical `lowerFirst`/`findCommand` file-locals out of this dispatcher and hand-rolled a SECOND row format beside the library's own" (`LibKa0s/Slash.lua`). This addon is one of the two.

- `core/SlashCommands.lua:83-86`: `lowerFirst` is `lib.SplitVerb`, byte for byte.
- `core/SlashCommands.lua:88-92`: `findCommand` is `lib.FindCommand`, minus the nil-list guard.
- `core/SlashCommands.lua:466-469` (`priorityHelp`), and the same loop in `statHelp` (`:613`), `aioHelp` (`:820`) and `barHelp` (`:943`), print `("  |cffffff00/cm ... %s|r — |cffffffff%s|r")`. That is `lib.CommandRows(prefix, COMMANDS, "  ")`. `lib.FormatRow` differs only in hex case.

## Library doc

`LibKa0s/docs/api/Slash/version-19.1-docs.md`, section *The sub-command vocabulary* (`SplitVerb`, `FindCommand`, `CommandRows`). Also `LibKa0s/docs/api/CONSUMERS.md`.

---
*Filed by GI-LK-13 of Ka0sAddonsCommonTasks/docs/2026-10-01-GITHUB_ISSUE_PASS (LibKa0s#9 census)*

=================== KickCD#36
Adopt LibKa0s SplitVerb, FindCommand, CommandRows, Core.SECRET and Options LAYOUT in place of the host copies at core/KickCD.lua, core/Compat.lua and core/Constants.lua
[enhancement,state:triaged,severity:low]
## What

The census of LibKa0s v1.66.0 finds five zero-consumer exports that this addon duplicates. They are grouped here so the pass files one issue per host.

### 1-3. `Slash.SplitVerb`, `Slash.FindCommand`, `Slash.CommandRows`: the sub-command vocabulary

The library added these three because "two hosts had already copied byte-identical `lowerFirst`/`findCommand` file-locals out of this dispatcher and hand-rolled a SECOND row format beside the library's own" (`LibKa0s/Slash.lua`). This addon is one of the two, and the copies are still here:

- `core/KickCD.lua:594-597`: `lowerFirst` is `SplitVerb`, byte for byte.
- `core/KickCD.lua:436-440`: `findCommand` is `FindCommand`, minus the nil-list guard.
- `core/KickCD.lua:466-468`: the debug sub-help prints `("  |cffffff00/kcd debug %s|r — |cffffffff%s|r")`, which is `CommandRows("/kcd debug", DEBUG_COMMANDS, "  ")`. `lib.FormatRow` differs only in hex case (`|cFFFFFF00`).

### 4. `Core.SECRET`

`core/Compat.lua:370` (`safeRender`) returns the literal `"<secret>"` outside a degradation stub.

### 5. `Options lib.LAYOUT`

`core/Constants.lua:113` (`PANEL_HEADER_TOP = 20`) and `:119` (`PANEL_HEADER_HEIGHT = 54`) copy `lib.LAYOUT.HEADER_TOP` / `HEADER_HEIGHT`. Nothing outside `tests/test_constants.lua` reads them. The file's own comment at `:101-107` already explains why `PANEL_PADDING_X` was removed ("the host copy is the one that goes stale"), and the same reasoning covers these two. Delete them, or read `lib.LAYOUT` where a value is needed.

## Library doc

`LibKa0s/docs/api/Slash/version-19.1-docs.md`, section *The sub-command vocabulary*. `LibKa0s/docs/api/Core/version-9-docs.md`, section *Lib-level surface*. `LibKa0s/docs/api/Options/version-27.2.34.2.2.8.1.7.4.2-docs.md`, section *The four `lib.LAYOUT` constants*. Also `LibKa0s/docs/api/CONSUMERS.md`.

---
*Filed by GI-LK-13 of Ka0sAddonsCommonTasks/docs/2026-10-01-GITHUB_ISSUE_PASS (LibKa0s#9 census)*

=================== LootHistory#33
Adopt LibKa0s Core.MakeResizable in place of the host copy at modules/Browser.lua
[enhancement,state:triaged,severity:low]
## What

`LibKa0s-Core-1.0` exports `MakeResizable(frame, opts)` (Core minor 9). The census of LibKa0s v1.66.0 finds **no host that calls it**. The library's own console, copy window and perf panel are its only callers. The History browser still builds the same grip by hand.

## Evidence (v1.66.0 vendored, branch `feat/2026-10-01-github-issue-pass`)

- `modules/Browser.lua:956` calls `SetResizable(true)`, with the `SetResizeBounds` / `SetMinResize` ladder at `:958-962`.
- `modules/Browser.lua:1055-1077` builds the grip with the chat size-grabber pair. OnMouseDown runs `StartSizing("BOTTOMRIGHT")`, gated on `B:IsLocked()`. OnMouseUp runs `StopMovingOrSizing()`, `SaveWindow()` and a table refresh.

`Core.MakeResizable` does the same work, and the save and refresh map onto `opts.onResize(w, h)`.

## Blocker to settle first

**The library's grip has no lock gate.** This addon gates the resize on *Lock frame* (options-ui-§15), and `MakeResizable` has nowhere to put that check. This would be the first host to adopt it, and that is the moment to settle the contract (LibKa0s#9: "first contact is the last moment the contract can be argued about"). The question is filed as tusharsaxena/LibKa0s#41. Adopt once it is answered.

## Library doc

`LibKa0s/docs/api/Core/version-9-docs.md`, section *The resize grip*. Also `LibKa0s/docs/api/CONSUMERS.md`, the v1.66.0 census row for `lib.MakeResizable`.

---
*Filed by GI-LK-13 of Ka0sAddonsCommonTasks/docs/2026-10-01-GITHUB_ISSUE_PASS (LibKa0s#9 census)*

=================== MultiMeters#58
Adopt LibKa0s Core.MakeResizable and Core.SECRET in place of the host copies at modules/Window.lua and core/Diagnostics.lua
[enhancement,state:triaged,severity:low]
## What

The census of LibKa0s v1.66.0 finds two zero-consumer exports that this addon duplicates:

### 1. `Core.MakeResizable(frame, opts)` (Core minor 9)

No host calls it. The library's own console, copy window and perf panel are its only callers.

- `modules/Window.lua:467` calls `anchor:SetResizable(true)`.
- `modules/Window.lua:643-651` builds a hand-rolled grip with the chat size-grabber pair. OnMouseDown runs `anchor:StartSizing("BOTTOMRIGHT")` and OnMouseUp runs `onResizeStop`.

Possible misfits: the grip is 12x12 where the library's is 16x16, and it sizes the clean `anchor` frame rather than the frame that carries the art. `MakeResizable` takes the frame it sizes, so the grip would have to sit on `anchor`. Read this as an adoption to evaluate, not a mechanical swap.

### 2. `Core.SECRET`, the `"<secret>"` sentinel

No host reads it by name. Every host's degradation stub spells the literal, which is correct for a stub. This addon also spells it **outside** a stub:

- `core/Diagnostics.lua:132` has `local SECRET = "<secret>"`, published as `Diagnostics.SECRET` at `:194`.

The library exports the constant so that "a host's tests, its docs and this implementation cannot drift apart" (`LibKa0s/docs/api/Core/version-9-docs.md`, *Lib-level surface*). Read it through the Core seam (`core/CoreSetup.lua` already binds the library), with the literal kept only for the library-absent path.

## Library doc

`LibKa0s/docs/api/Core/version-9-docs.md`, sections *The resize grip* and *Lib-level surface*. Also `LibKa0s/docs/api/CONSUMERS.md`.

## Not filed

`settings/Schema_Compose.lua` keeps its own `OUTLINE_VALUES` (`:178-184`) and `MASTERVIS_VALUES` (`:606-611`) beside the library's `O.FONT_FLAGS` and `O.VISIBILITY_VALUES`, which have no consumers. These copies are deliberate, and the reason is recorded at `:165-169` and `:602-605`: the display strings are localized, and the library carries no locale. The census records them and re-opens neither.

---
*Filed by GI-LK-13 of Ka0sAddonsCommonTasks/docs/2026-10-01-GITHUB_ISSUE_PASS (LibKa0s#9 census)*

=================== PanelMaster#56
Adopt LibKa0s O.PADDING_X in place of the host copy at settings/Panel.lua
[enhancement,state:triaged,severity:low]
## What

`LibKa0s-Options-1.0` publishes `O.PADDING_X`, the inset the library draws its own header, divider and body to. It is published so that a host aligning a bespoke widget can read the value instead of restating it (options-ui-§8). The census of LibKa0s v1.66.0 finds **no host that reads it**. This addon keeps a copy:

- `settings/Panel.lua:58` has `local PADDING_X = 16`, commented "still needed for the Profiles page's hand-anchored container". It is read at `:513-514` to anchor that container.

The Profiles page is the case the published value exists for. Read `O.PADDING_X` off the instance there, and the local goes away.

## Library doc

`LibKa0s/docs/api/Options/version-27.2.34.2.2.8.1.7.4.2-docs.md`, the `PADDING_X` row of *The instance surface*. Also `LibKa0s/docs/api/CONSUMERS.md`.

---
*Filed by GI-LK-13 of Ka0sAddonsCommonTasks/docs/2026-10-01-GITHUB_ISSUE_PASS (LibKa0s#9 census)*

