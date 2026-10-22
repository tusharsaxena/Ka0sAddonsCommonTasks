| Major | Export | Evidence | Hits by class | Verdict |
|---|---|---|---|---|
| Lifecycle | `Hold` (instance) | stubs only (18 stub lines across 6 hosts) | call 0 · stub 24 · test 72 | zero — kept, documented |
| Lifecycle | `PrintHolds` (instance) | stubs only | call 0 · stub 12 · test 5 | zero — kept, documented |
| Lifecycle | `Release` (instance) | stubs only; the 7 name hits are other tables' `Release` | call 0 · name-only 13 · def 5 · stub 23 · test 112 | zero — kept, documented |
| Lifecycle | `name` (instance) | instance data field | call 0 · name-only 439 · def 3 · stub 104 · test 7587 | zero — kept, documented |
| Schema | `lib.STRINGS` | no host reads the table by name | call 0 · name-only 1 · stub 4 · test 150 | zero — kept, documented |
| Media | `lib.FONTS` | no host reads the table by name | call 0 · test 29 | zero — kept, documented |
| Media | `lib.TEXTURES` | no host reads the table by name | call 0 · test 3 | zero — kept, documented |
| Media | `lib.Texture` | ConsumableMaster's two `Texture` hits are its own `MacroDisplay.Texture` | call 0 · name-only 11 · def 2 · test 71 | zero — kept, documented |
| Media | `lib.VENDOR_PATH` | default value | call 0 · test 1 | zero — kept, documented |
| Widgets | `lib.AUTOCOMPLETE` | no host reads it | call 0 | zero — kept, documented |
| Widgets | `lib.ChartMath` | no host calls it; LootHistory aligns its in/out strip through the chart instance's `XToPixel` instead | call 0 · test 2 | zero — kept, documented |
| Widgets | `backdrop` (descriptor) | no `CopyWindow` descriptor passes it | call 0 | zero — kept, documented |
| Widgets | `hoverXs` (descriptor) | hit scan sees no descriptor literal naming it | call 0 | zero — kept, documented |
| Widgets | `integer` (descriptor) | hit scan sees no descriptor literal naming it | call 0 | zero — kept, documented |
| Widgets | `makeCloseButton` (descriptor) | no `CopyWindow` descriptor passes it | call 0 | zero — kept, documented |
| Widgets | `markers` (descriptor) | hit scan sees no descriptor literal naming it | call 0 | zero — kept, documented |
| Widgets | `scrollName` (descriptor) | library-internal caller only | call 0 | zero — kept, documented |
| Widgets | `series` (descriptor) | hit scan sees no descriptor literal naming it | call 0 | zero — kept, documented |
| Widgets | `xMax` (descriptor) | hit scan sees no descriptor literal naming it | call 0 | zero — kept, documented |
| Widgets | `xMin` (descriptor) | hit scan sees no descriptor literal naming it | call 0 | zero — kept, documented |
| Widgets | `yMax` (descriptor) | hit scan sees no descriptor literal naming it | call 0 | zero — kept, documented |
| Widgets | `yMin` (descriptor) | hit scan sees no descriptor literal naming it | call 0 | zero — kept, documented |
| DebugLog | `lib.AT_ENABLE_MAX` | tuning constant | call 0 | zero — kept, documented |
| DebugLog | `lib.BUFFER_SLACK` | tuning constant | call 0 · test 1 | zero — kept, documented |
| DebugLog | `lib.DIAG_MAX_LINES` | tuning constant | call 0 · test 1 | zero — kept, documented |
| DebugLog | `lib.DIAG_MAX_PER_LIST` | tuning constant | call 0 | zero — kept, documented |
| DebugLog | `lib.GATE_MAX_KEYS` | tuning constant | call 0 | zero — kept, documented |
| DebugLog | `lib.MAX_BUFFER` | read by host tests only | call 0 · test 8 | zero — kept, documented |
| DebugLog | `lib.MakeCloseButton` | the 21 name hits are `Core.MakeCloseButton` calls | call 0 · name-only 29 · def 14 · stub 25 · test 128 | zero — kept, documented |
| DebugLog | `lib.STRINGS` | no host reads the table by name | call 0 · name-only 1 · stub 4 · test 150 | zero — kept, documented |
| DebugLog | `lib.TIME_COPY` | diagnostic switch | call 0 | zero — kept, documented |
| DebugLog | `BufferSize` (instance) | read by host tests only (62 hits) | call 0 · stub 12 · test 62 | zero — kept, documented |
| DebugLog | `BuildDiagnostics` (instance) | read by host tests only | call 0 · stub 18 · test 32 | zero — kept, documented |
| DebugLog | `CopyText` (instance) | read by host tests only | call 0 · stub 6 · test 22 | zero — kept, documented |
| DebugLog | `FindLine` (instance) | read by host tests only (88 hits) | call 0 · stub 12 · test 89 | zero — kept, documented |
| DebugLog | `LastLine` (instance) | read by host tests only | call 0 · stub 12 · test 50 | zero — kept, documented |
| DebugLog | `MakeCloseButton` (instance) | mirror of the lib-level member | call 0 · name-only 29 · def 14 · stub 25 · test 128 | zero — kept, documented |
| DebugLog | `Text` (instance) | the 15 name hits are `Sl:Text` (LibKa0s-Slash-1.0) calls | call 0 · name-only 18 · def 1 · stub 12 · test 261 | zero — kept, documented |
| DebugLog | `buffer` (instance) | read by host tests only (478 hits) | call 0 · stub 16 · test 508 | zero — kept, documented |
| DebugLog | `diagnosticsEnablesLogging` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
| DebugLog | `makeCloseButton` (descriptor) | BankLedger core/DebugLogSetup.lua:146 and LootHistory core/DebugLogSetup.lua:163 record why | call 0 | zero — kept, documented |
| DebugLog | `skin` (descriptor) | no descriptor passes it (MultiMeters settings/Schema_Compose.lua:248 is a locale key) | call 0 | zero — kept, documented |
| Slash | `CliResetAll` (instance) | LootHistory settings/Slash.lua:433-435 and BankLedger settings/Slash.lua:478-479 record why | call 0 · name-only 6 · def 3 · stub 9 · test 64 | zero — deliberate host copy |
| Launcher | `lib.STRINGS` | no host reads the table by name | call 0 · name-only 1 · stub 4 · test 150 | zero — kept, documented |
| Launcher | `Object` (instance) | read by host tests only (110 hits) | call 0 · stub 10 · test 114 | zero — kept, documented |
| Launcher | `L` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
| Options | `lib.LAYOUT` | KickCD core/Constants.lua:109-116 records the deletion; no host reads the table by name | call 0 · name-only 7 · test 97 | zero — kept, documented |
| Options | `lib.PatchAlwaysShowScrollbar` | reached through `EnsureScroll` | call 0 · stub 11 · test 20 | zero — kept, documented |
| Options | `lib.STRINGS` | no host reads the table by name | call 0 · name-only 1 · stub 4 · test 150 | zero — kept, documented |
| Options | `CHROME_GAP` (instance) | no host draws such chrome today | call 0 · name-only 3 · stub 6 · test 19 | zero — kept, documented |
| Options | `FONT_FLAGS` (instance) | MultiMeters settings/Schema_Compose.lua:165-184 records why | call 0 · name-only 1 · stub 4 · test 14 | zero — deliberate host copy |
| Options | `FONT_FLAGS_SORT` (instance) | MultiMeters settings/Schema_Compose.lua:184 | call 0 · stub 3 · test 12 | zero — deliberate host copy |
| Options | `ID_NAME_HINT` (instance) | reached through `IdInput` | call 0 · stub 17 · test 3 | zero — kept, documented |
| Options | `PatchAlwaysShowScrollbar` (instance) | reached through `EnsureScroll` | call 0 · stub 11 · test 20 | zero — kept, documented |
| Options | `RenderSchema` (instance) | superseded in practice | call 0 · stub 16 · test 24 | zero — kept, documented |
| Options | `SetChromeHeight` (instance) | reached through the chrome makers | call 0 · stub 15 · test 4 | zero — kept, documented |
| Options | `TAB_H` (instance) | no host measures its own strip today | call 0 · name-only 5 · stub 5 · test 20 | zero — kept, documented |
| Options | `UnnamedCandidates` (instance) | reached through `IdInput` | call 0 · stub 16 · test 1 | zero — kept, documented |
| Options | `VISIBILITY_SORT` (instance) | MultiMeters settings/Schema_Compose.lua:602-611 records why | call 0 · stub 3 · test 12 | zero — deliberate host copy |
| Options | `VISIBILITY_VALUES` (instance) | MultiMeters settings/Schema_Compose.lua:602-611 records why | call 0 · stub 3 · test 12 | zero — deliberate host copy |
| Options | `afterRestoreAll` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
| Perf | `lib.DEFAULT_RING` | default value | call 0 · test 2 | zero — kept, documented |
| Perf | `lib.EncodeJSON` | read by host tests only | call 0 · test 14 | zero — kept, documented |
| Perf | `lib.SCHEMA` | read by host tests only | call 0 · stub 1 · test 24 | zero — kept, documented |
| Perf | `lib.STRINGS` | no host reads the table by name | call 0 · name-only 1 · stub 4 · test 150 | zero — kept, documented |
| Perf | `Announce` (instance) | reached through `OnCommand` | call 0 · name-only 3 · def 1 · test 20 | zero — kept, documented |
| Perf | `BuildRecord` (instance) | reached through `OnCommand` | call 0 · name-only 1 · def 1 · test 21 | zero — kept, documented |
| Perf | `Cancel` (instance) | reached through `OnCommand` | call 0 · name-only 68 · def 5 · test 88 | zero — kept, documented |
| Perf | `Close` (instance) | no host brackets with `Open`/`Close` | call 0 · name-only 18 · def 5 · stub 2 · test 87 | zero — kept, documented |
| Perf | `Context` (instance) | reached through `OnCommand` | call 0 · name-only 12 · def 1 · test 12 | zero — kept, documented |
| Perf | `ContextLines` (instance) | reached through `OnCommand` | call 0 | zero — kept, documented |
| Perf | `EXPERIMENTS` (instance) | library-internal table (not in the instance table) | call 0 | zero — kept, documented |
| Perf | `EncodeJSON` (instance) | read by host tests only | call 0 · test 14 | zero — kept, documented |
| Perf | `FormatReport` (instance) | reached through `OnCommand` | call 0 · test 3 | zero — kept, documented |
| Perf | `HidePanel` (instance) | reached through `OnCommand` and the panel | call 0 · name-only 4 · test 31 | zero — kept, documented |
| Perf | `IsPanelShown` (instance) | read by host tests only | call 0 · name-only 4 · test 30 | zero — kept, documented |
| Perf | `LABELS` (instance) | library-internal table (not in the instance table) | call 0 · name-only 8 · test 14 | zero — kept, documented |
| Perf | `Log` (instance) | reached through `OnCommand` | call 0 · name-only 3 · def 1 · test 17 | zero — kept, documented |
| Perf | `MarkReviewed` (instance) | reached through `OnCommand` | call 0 · test 1 | zero — kept, documented |
| Perf | `Measure` (instance) | reached through `OnCommand` | call 0 · name-only 1 · test 6 | zero — kept, documented |
| Perf | `Open` (instance) | no host brackets with `Open`/`Close` | call 0 · name-only 39 · def 14 · stub 3 · test 357 | zero — kept, documented |
| Perf | `PanelIsActionable` (instance) | no `decorate` host | call 0 | zero — kept, documented |
| Perf | `PanelStateOf` (instance) | no `decorate` host | call 0 · test 2 | zero — kept, documented |
| Perf | `Progress` (instance) | reached through the panel | call 0 | zero — kept, documented |
| Perf | `RefreshPanel` (instance) | reached through the library's own transitions | call 0 · name-only 36 · stub 11 · test 28 | zero — kept, documented |
| Perf | `Reset` (instance) | reached through `OnCommand` | call 0 · name-only 4 · def 4 · stub 8 · test 451 | zero — kept, documented |
| Perf | `Resume` (instance) | reached through `OnCommand` | call 0 · name-only 12 · def 15 · test 77 | zero — kept, documented |
| Perf | `SCHEMA` (instance) | read by host tests only | call 0 · stub 1 · test 24 | zero — kept, documented |
| Perf | `STEPS` (instance) | reached through the panel | call 0 · test 13 | zero — kept, documented |
| Perf | `Save` (instance) | reached through `OnCommand` | call 0 · name-only 3 · def 3 · test 111 | zero — kept, documented |
| Perf | `ShowPanel` (instance) | reached through `OnCommand` | call 0 · name-only 5 · test 27 | zero — kept, documented |
| Perf | `Start` (instance) | reached through `OnCommand` | call 0 · name-only 12 · def 10 · test 181 | zero — kept, documented |
| Perf | `StatusLines` (instance) | reached through `OnCommand` | call 0 · test 1 | zero — kept, documented |
| Perf | `Stop` (instance) | reached through `OnCommand` | call 0 · name-only 43 · def 10 · test 123 | zero — kept, documented |
| Perf | `Suspend` (instance) | reached through `OnCommand` | call 0 · name-only 4 · def 15 · test 101 | zero — kept, documented |
| Perf | `TogglePanel` (instance) | reached through `OnCommand` | call 0 · name-only 3 · test 1 | zero — kept, documented |
| Perf | `Usage` (instance) | reached through `OnCommand` | call 0 · test 47 | zero — kept, documented |
| Perf | `context` (instance) | instance data field (not in the instance table) | call 0 · name-only 2 · def 2 · test 200 | zero — kept, documented |
| Perf | `descriptor` (instance) | instance data field (not in the instance table) | call 0 · stub 10 · test 761 | zero — kept, documented |
| Perf | `name` (instance) | instance data field (not in the instance table) | call 0 · name-only 439 · def 3 · stub 104 · test 7587 | zero — kept, documented |
| Perf | `ringMax` (instance) | instance data field (not in the instance table) | call 0 | zero — kept, documented |
| Perf | `slash` (instance) | instance data field (not in the instance table) | call 0 · name-only 3 · stub 75 · test 1445 | zero — kept, documented |
| Perf | `title` (instance) | instance data field (not in the instance table) | call 0 · name-only 108 · def 7 · stub 2 · test 729 | zero — kept, documented |
| Perf | `L` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
| Perf | `decorate` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
| Perf | `onChange` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
| Perf | `ring` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
| Sim | `lib.STRINGS` | no host reads the table by name; LootHistory settings/Slash.lua:233 is LibKa0s-Slash-1.0's `lib.STRINGS` | call 0 · name-only 1 · stub 4 · test 150 | zero — kept, documented |
| Sim | `PanelRows` (instance) | reached through the library's step panel; the host defs are library-absent stubs | call 0 · def 3 · test 20 | zero — kept, documented |
| Sim | `Pause` (instance) | BankLedger's only "call" is its library-absent stub (core/SimSetup.lua:76-91, host contract H9), which the scan's block detector misses; DropWatcher's and LootHistory's name hits are their own stubs and other tables' members | call 1 · name-only 3 · def 1 · test 3 | zero — kept, documented (read by hand) |
| Sim | `RefreshPanel` (instance) | BankLedger's only "call" is its library-absent stub (core/SimSetup.lua:76-91, host contract H9), which the scan's block detector misses; the name hits are other tables' members and the other hosts' stubs | call 1 · name-only 35 · stub 11 · test 28 | zero — kept, documented (read by hand) |
| Sim | `Restart` (instance) | BankLedger's only "call" is its library-absent stub (core/SimSetup.lua:76-91, host contract H9), which the scan's block detector misses; DropWatcher's and LootHistory's name hits are their own stubs and other tables' members | call 1 · name-only 2 · test 7 | zero — kept, documented (read by hand) |
| Sim | `Resume` (instance) | BankLedger's only "call" is its library-absent stub (core/SimSetup.lua:76-91, host contract H9), which the scan's block detector misses; DropWatcher's and LootHistory's name hits are their own stubs and other tables' members | call 1 · name-only 11 · def 15 · test 77 | zero — kept, documented (read by hand) |
| Sim | `Run` (instance) | BankLedger's only "call" is its library-absent stub (core/SimSetup.lua:76-91, host contract H9), which the scan's block detector misses; DropWatcher's and LootHistory's name hits are their own stubs and other tables' members | call 1 · name-only 15 · def 5 · stub 3 · test 265 | zero — kept, documented (read by hand) |
| Sim | `Step` (instance) | AuraMaster's hits are `E.LuaCurveType.Step`; the host defs are library-absent stubs | call 0 · name-only 3 · def 3 · test 71 | zero — kept, documented |
| Sim | `TogglePanel` (instance) | BankLedger's only "call" is its library-absent stub (core/SimSetup.lua:76-91, host contract H9), which the scan's block detector misses; the name hits are other tables' members and the other hosts' stubs | call 1 · name-only 2 · test 1 | zero — kept, documented (read by hand) |
| Sim | `Unwrapped` (instance) | read by host tests only (all three Sim hosts); the host defs are library-absent seam stubs | call 0 · def 3 · test 13 | zero — kept, documented |
| Sim | `addonName` (descriptor) | library-internal: SimPanel.lua's renderer reads `d.addonName` off the table its adapter builds (`renderer`, SimPanel.lua:827), not off the host's descriptor | call 0 | zero — kept, documented |
| Sim | `close` (descriptor) | library-internal: SimPanel.lua's renderer reads `d.close` off the table its adapter builds (`renderer`, SimPanel.lua:827), not off the host's descriptor | call 0 | zero — kept, documented |
| Sim | `footer` (descriptor) | library-internal: SimPanel.lua's renderer reads `d.footer` off the table its adapter builds (`renderer`, SimPanel.lua:827), not off the host's descriptor | call 0 | zero — kept, documented |
| Sim | `onClick` (descriptor) | library-internal: SimPanel.lua's renderer reads `d.onClick` off the table its adapter builds (`renderer`, SimPanel.lua:827), not off the host's descriptor | call 0 | zero — kept, documented |
| Sim | `rows` (descriptor) | library-internal: SimPanel.lua's renderer reads `d.rows` off the table its adapter builds (`renderer`, SimPanel.lua:827), not off the host's descriptor | call 0 | zero — kept, documented |
| Sim | `tooltip` (descriptor) | library-internal: SimPanel.lua's renderer reads `d.tooltip` off the table its adapter builds (`renderer`, SimPanel.lua:827), not off the host's descriptor | call 0 | zero — kept, documented |
