| Major | Export | Evidence | Hits by class | Verdict |
|---|---|---|---|---|
| Lifecycle | `Hold` (instance) | stubs only (18 stub lines across 6 hosts) | call 0 · stub 18 · test 48 | zero — kept, documented |
| Lifecycle | `PrintHolds` (instance) | stubs only | call 0 · stub 9 · test 5 | zero — kept, documented |
| Lifecycle | `Release` (instance) | stubs only; the 7 name hits are other tables' `Release` | call 0 · name-only 7 · def 2 · stub 17 · test 80 | zero — kept, documented |
| Lifecycle | `name` (instance) | instance data field | call 0 · name-only 232 · def 3 · stub 84 · test 5391 | zero — kept, documented |
| Schema | `lib.STRINGS` | no host reads the table by name | call 0 · name-only 1 · stub 4 · test 147 | zero — kept, documented |
| Media | `lib.FONTS` | no host reads the table by name | call 0 · test 29 | zero — kept, documented |
| Media | `lib.ICONS` | no host reads the table by name | call 0 · test 30 | zero — kept, documented |
| Media | `lib.TEXTURES` | no host reads the table by name | call 0 · test 3 | zero — kept, documented |
| Media | `lib.Texture` | ConsumableMaster's two `Texture` hits are its own `MacroDisplay.Texture` | call 0 · name-only 2 · def 1 · test 40 | zero — kept, documented |
| Media | `lib.VENDOR_PATH` | default value | call 0 · test 1 | zero — kept, documented |
| Widgets | `lib.ChartMath` | no host calls it; LootHistory aligns its in/out strip through the chart instance's `XToPixel` instead | call 0 · test 1 | zero — kept, documented |
| Widgets | `lib.LINE_CHART` | no host reads it | call 0 · test 1 | zero — kept, documented |
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
| DebugLog | `lib.MakeCloseButton` | the 21 name hits are `Core.MakeCloseButton` calls | call 0 · name-only 21 · def 11 · stub 19 · test 109 | zero — kept, documented |
| DebugLog | `lib.STRINGS` | no host reads the table by name | call 0 · name-only 1 · stub 4 · test 147 | zero — kept, documented |
| DebugLog | `lib.TIME_COPY` | diagnostic switch | call 0 | zero — kept, documented |
| DebugLog | `BufferSize` (instance) | read by host tests only (62 hits) | call 0 · stub 9 · test 62 | zero — kept, documented |
| DebugLog | `BuildDiagnostics` (instance) | read by host tests only | call 0 · stub 15 · test 31 | zero — kept, documented |
| DebugLog | `CopyText` (instance) | read by host tests only | call 0 · stub 3 · test 22 | zero — kept, documented |
| DebugLog | `FindLine` (instance) | read by host tests only (88 hits) | call 0 · stub 9 · test 88 | zero — kept, documented |
| DebugLog | `LastLine` (instance) | read by host tests only | call 0 · stub 9 · test 50 | zero — kept, documented |
| DebugLog | `MakeCloseButton` (instance) | mirror of the lib-level member | call 0 · name-only 21 · def 11 · stub 19 · test 109 | zero — kept, documented |
| DebugLog | `Text` (instance) | the 15 name hits are `Sl:Text` (LibKa0s-Slash-1.0) calls | call 0 · name-only 15 · stub 6 · test 209 | zero — kept, documented |
| DebugLog | `buffer` (instance) | read by host tests only (478 hits) | call 0 · stub 13 · test 479 | zero — kept, documented |
| DebugLog | `diagnosticsEnablesLogging` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
| DebugLog | `makeCloseButton` (descriptor) | BankLedger core/DebugLogSetup.lua:146 and LootHistory core/DebugLogSetup.lua:163 record why | call 0 | zero — kept, documented |
| DebugLog | `skin` (descriptor) | no descriptor passes it (MultiMeters settings/Schema_Compose.lua:248 is a locale key) | call 0 | zero — kept, documented |
| Slash | `CliResetAll` (instance) | LootHistory settings/Slash.lua:433-435 and BankLedger settings/Slash.lua:478-479 record why | call 0 · name-only 6 · def 3 · stub 6 · test 64 | zero — deliberate host copy |
| Launcher | `lib.STRINGS` | no host reads the table by name | call 0 · name-only 1 · stub 4 · test 147 | zero — kept, documented |
| Launcher | `Object` (instance) | read by host tests only (110 hits) | call 0 · stub 7 · test 110 | zero — kept, documented |
| Launcher | `L` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
| Options | `lib.LAYOUT` | KickCD core/Constants.lua:109-116 records the deletion; no host reads the table by name | call 0 · name-only 7 · test 86 | zero — kept, documented |
| Options | `lib.PatchAlwaysShowScrollbar` | reached through `EnsureScroll` | call 0 · stub 8 · test 20 | zero — kept, documented |
| Options | `lib.STRINGS` | no host reads the table by name | call 0 · name-only 1 · stub 4 · test 147 | zero — kept, documented |
| Options | `CHROME_GAP` (instance) | no host draws such chrome today | call 0 · stub 6 · test 14 | zero — kept, documented |
| Options | `FONT_FLAGS` (instance) | MultiMeters settings/Schema_Compose.lua:165-184 records why | call 0 · stub 4 · test 11 | zero — deliberate host copy |
| Options | `FONT_FLAGS_SORT` (instance) | MultiMeters settings/Schema_Compose.lua:184 | call 0 · stub 3 · test 9 | zero — deliberate host copy |
| Options | `ID_NAME_HINT` (instance) | reached through `IdInput` | call 0 · stub 14 · test 3 | zero — kept, documented |
| Options | `PatchAlwaysShowScrollbar` (instance) | reached through `EnsureScroll` | call 0 · stub 8 · test 20 | zero — kept, documented |
| Options | `RenderSchema` (instance) | superseded in practice | call 0 · stub 13 · test 24 | zero — kept, documented |
| Options | `SetChromeHeight` (instance) | reached through the chrome makers | call 0 · stub 12 · test 3 | zero — kept, documented |
| Options | `TAB_H` (instance) | no host measures its own strip today | call 0 · stub 5 · test 16 | zero — kept, documented |
| Options | `UnnamedCandidates` (instance) | reached through `IdInput` | call 0 · stub 13 · test 1 | zero — kept, documented |
| Options | `VISIBILITY_SORT` (instance) | MultiMeters settings/Schema_Compose.lua:602-611 records why | call 0 · stub 3 · test 9 | zero — deliberate host copy |
| Options | `VISIBILITY_VALUES` (instance) | MultiMeters settings/Schema_Compose.lua:602-611 records why | call 0 · stub 3 · test 9 | zero — deliberate host copy |
| Options | `afterRestoreAll` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
| Perf | `lib.DEFAULT_RING` | default value | call 0 · test 2 | zero — kept, documented |
| Perf | `lib.EncodeJSON` | read by host tests only | call 0 · test 12 | zero — kept, documented |
| Perf | `lib.SCHEMA` | read by host tests only | call 0 · stub 1 · test 24 | zero — kept, documented |
| Perf | `lib.STRINGS` | no host reads the table by name | call 0 · name-only 1 · stub 4 · test 147 | zero — kept, documented |
| Perf | `Announce` (instance) | reached through `OnCommand` | call 0 · name-only 3 · def 1 · test 4 | zero — kept, documented |
| Perf | `BuildRecord` (instance) | reached through `OnCommand` | call 0 · name-only 1 · def 1 · test 14 | zero — kept, documented |
| Perf | `Cancel` (instance) | reached through `OnCommand` | call 0 · name-only 24 · test 30 | zero — kept, documented |
| Perf | `Close` (instance) | no host brackets with `Open`/`Close` | call 0 · name-only 4 · def 1 · stub 2 · test 62 | zero — kept, documented |
| Perf | `Context` (instance) | reached through `OnCommand` | call 0 · name-only 10 · test 6 | zero — kept, documented |
| Perf | `ContextLines` (instance) | reached through `OnCommand` | call 0 | zero — kept, documented |
| Perf | `EXPERIMENTS` (instance) | library-internal table (not in the instance table) | call 0 | zero — kept, documented |
| Perf | `EncodeJSON` (instance) | read by host tests only | call 0 · test 12 | zero — kept, documented |
| Perf | `FormatReport` (instance) | reached through `OnCommand` | call 0 · test 3 | zero — kept, documented |
| Perf | `HidePanel` (instance) | reached through `OnCommand` and the panel | call 0 · test 17 | zero — kept, documented |
| Perf | `IsPanelShown` (instance) | read by host tests only | call 0 · test 6 | zero — kept, documented |
| Perf | `LABELS` (instance) | library-internal table (not in the instance table) | call 0 · test 10 | zero — kept, documented |
| Perf | `Log` (instance) | reached through `OnCommand` | call 0 · test 4 | zero — kept, documented |
| Perf | `MarkReviewed` (instance) | reached through `OnCommand` | call 0 · test 1 | zero — kept, documented |
| Perf | `Measure` (instance) | reached through `OnCommand` | call 0 · name-only 1 · test 6 | zero — kept, documented |
| Perf | `Open` (instance) | no host brackets with `Open`/`Close` | call 0 · name-only 25 · def 7 · stub 3 · test 209 | zero — kept, documented |
| Perf | `PanelIsActionable` (instance) | no `decorate` host | call 0 | zero — kept, documented |
| Perf | `PanelStateOf` (instance) | no `decorate` host | call 0 · test 2 | zero — kept, documented |
| Perf | `Progress` (instance) | reached through the panel | call 0 | zero — kept, documented |
| Perf | `RefreshPanel` (instance) | reached through the library's own transitions | call 0 · name-only 25 · stub 8 · test 24 | zero — kept, documented |
| Perf | `Reset` (instance) | reached through `OnCommand` | call 0 · name-only 4 · def 3 · stub 8 · test 373 | zero — kept, documented |
| Perf | `Resume` (instance) | reached through `OnCommand` | call 0 · name-only 8 · def 14 · test 70 | zero — kept, documented |
| Perf | `SCHEMA` (instance) | read by host tests only | call 0 · stub 1 · test 24 | zero — kept, documented |
| Perf | `STEPS` (instance) | reached through the panel | call 0 · test 13 | zero — kept, documented |
| Perf | `Save` (instance) | reached through `OnCommand` | call 0 · name-only 1 · def 1 · test 20 | zero — kept, documented |
| Perf | `ShowPanel` (instance) | reached through `OnCommand` | call 0 · test 5 | zero — kept, documented |
| Perf | `Start` (instance) | reached through `OnCommand` | call 0 · name-only 4 · def 2 · test 77 | zero — kept, documented |
| Perf | `StatusLines` (instance) | reached through `OnCommand` | call 0 · test 1 | zero — kept, documented |
| Perf | `Stop` (instance) | reached through `OnCommand` | call 0 · name-only 21 · def 5 · test 32 | zero — kept, documented |
| Perf | `Suspend` (instance) | reached through `OnCommand` | call 0 · name-only 4 · def 15 · test 93 | zero — kept, documented |
| Perf | `TogglePanel` (instance) | reached through `OnCommand` | call 0 | zero — kept, documented |
| Perf | `Usage` (instance) | reached through `OnCommand` | call 0 · test 46 | zero — kept, documented |
| Perf | `context` (instance) | instance data field (not in the instance table) | call 0 · name-only 2 · def 1 · test 167 | zero — kept, documented |
| Perf | `descriptor` (instance) | instance data field (not in the instance table) | call 0 · stub 10 · test 733 | zero — kept, documented |
| Perf | `name` (instance) | instance data field (not in the instance table) | call 0 · name-only 232 · def 3 · stub 84 · test 5391 | zero — kept, documented |
| Perf | `ringMax` (instance) | instance data field (not in the instance table) | call 0 | zero — kept, documented |
| Perf | `slash` (instance) | instance data field (not in the instance table) | call 0 · stub 63 · test 1216 | zero — kept, documented |
| Perf | `title` (instance) | instance data field (not in the instance table) | call 0 · name-only 37 · def 2 · stub 2 · test 380 | zero — kept, documented |
| Perf | `L` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
| Perf | `decorate` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
| Perf | `onChange` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
| Perf | `ring` (descriptor) | no descriptor passes it | call 0 | zero — kept, documented |
