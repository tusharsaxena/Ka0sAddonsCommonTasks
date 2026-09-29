# WhatGroup smoke-test coverage map (SP-WG-03)

Old `docs/smoke-tests.md`: 1070 lines, 160 checks plus 5 composite or pointer rows (§ 7 steps 2-4,
§ 8 twice, § 13 twice), 166 old rows below (§ 11.2 takes two: a layout row and a comparison row). New: 734 lines, 147 checks: 134 carry the old behaviors
(duplicates merged) and 13 are new PROFILE checks; DEGRADED-4 also gained the `/wg profile` line.
Dropped: one old check whole (§ 2.14) and one in part (§ 11.2's comparison with the pre-adoption
build); both have a `dropped:` row below. The old
file had no `Result:` lines, so under the clarified Pending sign-off rule (spec S4, 2026-09-29) every
carried-over check is owed unless a Ka0sAddonsCommonTasks plan records the owner's pass. Only
`2026-09-25-DIAGNOSTICS_COMMAND/99_REPORT.md` § 6 does (WG-S1 to WG-S11 and WG-X1, PASS 2026-09-26,
procedure "section 2a" and "row 2.8b-ii"), so DIAG-5 and DIAG-17 to DIAG-24 are the only checks not
listed; every other old check, the 13 new PROFILE checks and every check corrected in this rework are
under Pending sign-off. The 2026-09-23 plan's WhatGroup session (WG.1 to WG.13) is recorded as still
owed, and the 2026-09-22 sweep's "20 passed" names no WhatGroup check. Line ranges are the old file
at `a8dfe5a`.

Contradictions in the old file, resolved against the code: 2.13 and § 13 said a bare `/wg reset`
raises the confirm popup (it prints a deprecation notice, `settings/Slash.lua` `runReset`; 11.6 was
right); 2.18 said the debug console keeps its position (it does not, 11.10); 1.3's repeat list said
"`/wg reset` confirm" (now `/wg resetall`); 3.9 step 1 put *Test mode* alone on its line (it pairs with
*Minimap button*); 3.7h, 3.8 step 4 and 4.6 step 5 expected *Only in combat* to open a hidden popup on
the pull, while 4.5 step 9 and `docs/frame.md` call that a known limitation (COMBAT-10 follows
frame.md and asks the tester to record it if it does open).

Corrected against the code in the third SP-WG-03R pass (each now under Pending sign-off): 5.5 steps 3
and 6 said a disabled `/wg help` and the typo's index print no refusal (the library's `PrintHelp`
prints `DisabledLine` under the header while disabled, `libs/LibKa0s/Slash.lua` `Sl:PrintHelp`); 9
step 3 expected a complete `/wg list` (the degraded Slash stub's `CliList` prints the settings-CLI
line, `settings/Slash.lua`); § 9 omitted the launcher's login notice (`core/LauncherSetup.lua`
stub `Register`); § 12's closing expected the console to open with the library absent (the degraded
`Toggle` only announces, `core/DebugLogSetup.lua`); § 9 renamed one copy of LibKa0s while any other
loaded Ka0s addon hands WhatGroup its own; 4.5 step 7 omitted the join summary `RunTest` prints before
`ShowFrame` defers (`core/WhatGroup.lua` `RunTest`); PROFILE-1 named scope dropdowns AceDBOptions does
not have.

| Old location | Behavior | New ID |
|---|---|---|
| § 1.1 (:18-24) | Cold load: no errors, no debug chatter | INSTALL-1 |
| § 1.2 (:26-31) | `/reload`: no errors or taint warnings | INSTALL-2 |
| § 1.3 (:33-41) | ESC → Logout clean after a `/reload` | INSTALL-3 |
| § 1.3 repeat list (:43-52) | Logout re-run after test notify, ESC in combat, fresh login, config, reset confirm, teleport click, LFG apply | INSTALL-4 (ESC in combat → COMBAT-7 last step; fresh login → INSTALL-3; "reset confirm" corrected to `/wg resetall`) |
| § 1.4 (:54-69) | Reset popup shows and accepts in and out of combat, then Logout clean | COMBAT-1 (the in-combat raise is now `/wg resetall` → Yes from a fresh `/reload`, since the Defaults button sits under the library's combat cover; the popup's first `StaticPopupDialogs` write still happens in combat) |
| § 1.5 (:71-86) | `/reload` in combat: Settings category lands at combat end, then Logout clean | COMBAT-2 (now expects the Profiles subcategory beside General) |
| § 2.1 (:96) | Bare `/wg` opens the landing page, no help | SLASH-2 |
| § 2.2 (:97) | `/wg help` prints the index | SLASH-1 |
| § 2.3 (:98) | `/whatgroup help` alias | SLASH-1 |
| § 2.4 (:99) | `/wg list` colors and headers | SLASH-4 |
| § 2.5 (:100) | `/wg get enabled` | SLASH-5 |
| § 2.6 (:101) | `/wg set notify.delay 2.5` and get | SLASH-6 |
| § 2.7 (:102) | `/wg set ... toggle` | SLASH-7 |
| § 2.8 (:103) | `/wg debug` opens/closes the console, state untouched | DIAG-1 |
| § 2.8a (:104) | `/wg debug on/off` colored acks, `[Debug]` and `[Init]` lines | DIAG-2 |
| § 2.8b (:105) | Title-bar toggle, Copy, Clear | DIAG-3 |
| § 2.8b-i (:106) | Scrollbar and line counter, first open does not error | DIAG-4 |
| § 2.8b-ii (:107) | Buffer cap pins at 3000, Copy holds newest 3000 | DIAG-5 |
| § 2.8c (:108) | One `[Set]` line per write | DIAG-6 |
| § 2.8d (:109) | `/wg resetall` logs one `[Set] reset profile` line with row count; console closes | DIAG-7 |
| § 2.9 (:110) | `/wg show` with nothing captured | SLASH-12 |
| § 2.10 (:111) | `/wg test notify` fires chat + popup | POPUP-1 |
| § 2.10a (:112) | `/wg test` toggles, `on`/`off`, bad arg usage | TEST-2, TEST-4 (merged) |
| § 2.11 (:113) | `/wg show` reopens the popup | POPUP-2 |
| § 2.12 (:114) | `/wg config` opens landing page with General in the sidebar | SLASH-2 |
| § 2.13 (:115) | `/wg reset` confirm popup (stale) | SLASH-11 (corrected to `/wg resetall`; bare `/wg reset` is SLASH-9) |
| § 2.14 (:116) | `/wg gibberish` → unknown command + help | dropped: asserted by `tests/test_slash.lua` "slash: an unknown verb says so and then prints the help index" (the disabled-state typo stays as STATE-5) |
| § 2.15 (:117) | `/wg config` in combat refused | COMBAT-3 |
| § 2.16 (:118) | `/wg version` matches the TOC | SLASH-3 |
| § 2.17 (:119) | Help header has no trailing colon, lists version | SLASH-1 |
| § 2.18 (:120) | Popup and console reopen where left after `/reload` | POPUP-6 (popup); console half corrected by DIAG-11 |
| § 2.19 (:121) | Library-absent `disable`/`enable`/`test on` say unavailable; library-present behave with one `[Set]` | DEGRADED-4 (absent); present half merged into SLASH-6, TEST-4, DIAG-6 (DIAG-6 now logs one `[Set]` line each for `/wg disable`, `/wg enable`, `/wg test on` and `/wg test off`) |
| § 2a step 1 (:131-140) | Diagnostics appends after the trace, section order, chat line | DIAG-17 |
| § 2a step 2 (:141-144) | Copy holds the report with no escapes | DIAG-18 |
| § 2a step 3 (:145-149) | Ungated, flag untouched | DIAG-19 |
| § 2a step 4 (:150-155) | Both forms, alias, no short form | DIAG-20 |
| § 2a step 5 (:156-160) | Runs while disabled | DIAG-21 |
| § 2a step 6 (:161-166) | Report never builds the popup | DIAG-22 |
| § 2a step 7 (:167-173) | Report in combat | DIAG-23 |
| § 2a step 8 (:174-177) | README bug-report steps | DIAG-24 |
| § 3.1 (:185-189) | Landing page: logo, notes, command rows, scrollbar | PANEL-1 |
| § 3.2 (:191-203) | General tab strip and per-tab layout | PANEL-2 |
| § 3.3 (:205-215) | Widget ↔ get/set round-trip, refresh in place | PANEL-3 |
| § 3.4 (:217-226) | Defaults button: deferred build, skin, reset, chat line | PANEL-5 |
| § 3.5 (:228-232) | Test button runs the notify flow | PANEL-6 |
| § 3.5a steps 1-3 (:236-243) | Width/Height defaults 420/260, live resize on release | PANEL-7 |
| § 3.5a steps 4 and 6 (:244-246, :250) | Size clamps, per-row reset | PANEL-8 |
| § 3.5a step 5 (:247-249) | Resize refused in combat, applied after | COMBAT-5 |
| § 3.6 layout (:254-264) | Master controls grid order | PANEL-2 |
| § 3.6 steps 1-4 (:266-269) | Console checkbox shows/hides window only, never flips logging | DIAG-8 |
| § 3.6 step 5 (:270) | Checkbox re-syncs after closing the console | DIAG-9 |
| § 3.6 step 6 (:271, :276) | Checkbox session-only after relog, no `state`/`debug` in SavedVariables | DIAG-10 |
| § 3.6 step 7 (:273-274) | `/wg resetall` closes the console | DIAG-7 |
| § 3.7a (:285) | Master scale slider | PANEL-9 |
| § 3.7b (:286) | Scale clamp at 2× | PANEL-9 |
| § 3.7c (:287) | Scale refused in combat, applied later | COMBAT-5 (the in-combat change is `/wg set scale 1.5`; the slider is under the combat cover) |
| § 3.7d (:288) | Master alpha, also in combat | PANEL-10 (the in-combat change is `/wg set alpha 0.4`; the slider is under the combat cover) |
| § 3.7e (:289) | Lock frame blocks drag | PANEL-11 |
| § 3.7f (:290) | Reset position, survives reload | PANEL-12 |
| § 3.7g (:291) | Visibility Never: nothing opens, summary still prints | PANEL-13 |
| § 3.7h (:292) | Visibility Only in combat: nothing shows out of combat; the pull; `/wg show` in combat | COMBAT-10 (the pull's expectation corrected per frame.md; the in-combat `/wg show` step kept: `Popup deferred until combat ends.`, no popup, no error, and nothing opens at combat end, per `modules/Frame.lua` `ShowFrame` and `replayFirstShow`) |
| § 3.7i (:293) | Setting Never closes an open popup | PANEL-13 |
| § 3.7j (:294) | Enum parser refuses a bad visibility | SLASH-8 |
| § 3.8 steps 1-3 (:310-313, :320-324) | Only out of combat hides on the pull, returns with the capture, no taint | COMBAT-9 |
| § 3.8 step 4 (:314-315, :325-326) | Only in combat mirror | COMBAT-10 |
| § 3.8 step 5 (:316-317, :327-328) | No capture: combat edge opens nothing | COMBAT-11 |
| § 3.8 "Also here" (:333-339) | No ticker behind a gate-hidden popup | TELE-5 |
| § 3.9 step 1 (:351-352) | Test mode checkbox unticked, tooltip | TEST-1 |
| § 3.9 step 2 (:353-354) | Tick shows the sample, one line, no summary | TEST-2 |
| § 3.9 step 3 (:355-356) | Untick closes, position kept | TEST-3 |
| § 3.9 step 3a (:357-359) | `/wg test` drives the checkbox | TEST-4 |
| § 3.9 step 4 (:360) | Lock holds in test mode | PANEL-11 |
| § 3.9 step 5 (:361-362) | Test mode overrides Never and autoShow off | TEST-5 |
| § 3.9 step 6 (:363-364) | Close and ESC untick | TEST-6 |
| § 3.9 step 7 (:365-367) | Pull ends test mode, no block, no return | TEST-7 |
| § 3.9 step 8, first half (:368-369) | `/wg test` refused in combat | TEST-8 |
| § 3.9 step 8, second half (:370-373) | Panel covered and locked in combat, one line | COMBAT-4 |
| § 3.9 step 9 (:374-375) | `/wg test notify` ends test mode and runs the one-shot | TEST-9 |
| § 3.9 step 10 (:376) | `/wg resetall` ends test mode | TEST-10 |
| § 3.9 step 11 (:377) | Test mode not persisted | TEST-10 |
| § 3.9 step 12 (:378-380) | Real join during test mode; details link replaces the sample | TEST-11 |
| § 4 main (:391-406) | `/wg test notify` chat lines and six popup rows | POPUP-1 |
| § 4.1 (:408-418) | Teleport click: tooltip, cast, no forbidden, one `[Frame]` line | TELE-1 |
| § 4.1a display (:422-431, :435-436) | Cooldown swipe, note, tooltip, dead click, log line, chat tag | TELE-3 |
| § 4.1a ticker (:432-434) | Countdown once per second, stops on close, never stacks | TELE-4 |
| § 4.1a expiry (:438) | Button rearms at expiry, live | TELE-6 |
| § 4.1b (:440-448) | Not learned: note, no tooltip, dead click | TELE-2 |
| § 4.2 (:450-455) | Test chat link reopens the popup | POPUP-3 |
| § 4.3 (:457-462) | ESC out of combat closes popup, not the menu; second ESC opens menu | POPUP-4 |
| § 4.3a (:464-482) | ESC in combat: no block, stays closed, Logout clean | COMBAT-7 |
| § 4.4 (:484-488) | Drag moves the whole popup, clamps | POPUP-5 |
| § 4.5 steps 1-3 (:499-504) | Close in combat takes the popup away and it stays gone | COMBAT-6 |
| § 4.5 step 4 (:505-506) | ESC in combat, same as Close | COMBAT-7 |
| § 4.5 steps 5-6 (:507-510) | Out of combat value hides on pull, returns | COMBAT-9 |
| § 4.5 steps 7-8 (:511-514) | Show requested in combat is deferred with one line | COMBAT-12 (corrected: the eight-line join summary prints first, then the deferred line) |
| § 4.5 step 9 (:515-516) | In combat value cannot open a hidden popup (known limitation) | COMBAT-10 |
| § 4.6 steps 1-4 (:526-532) | A dismissed popup stays closed across combat, Close and ESC | COMBAT-8 |
| § 4.6 steps 5-6 (:533-536) | In combat value opens on the pull | COMBAT-10 (contradicted 4.5 step 9; resolved per frame.md) |
| § 5.1 (:546-570) | Real application: trace and notification | LFG-1 |
| § 5.1a (:572-585) | Real join's details link, click and shift-click | LFG-2 |
| § 5.2 (:587-608) | Concurrent applications pair correctly, decline drops its capture | LFG-3 |
| § 5.3 (:610-620) | Group leave trace, `/wg show` afterwards | LFG-4 |
| § 5.4 (:622-631) | Master enable gate is inert, registrations gone | STATE-1 |
| § 5.5 steps 1-2 (:635-640) | Feature verbs refuse with one line and do nothing | STATE-2 |
| § 5.5 step 3 (:642-646) | Every other verb answers while disabled | STATE-3 (corrected: `/wg help` prints the refusal line under its header) |
| § 5.5 step 4 (:648-651) | Test button previews while disabled | STATE-4 |
| § 5.5 step 5 (:653-659) | Minimap left-click opens settings; right-click menu grayed | LAUNCH-8 (left-click), LAUNCH-7 (menu) |
| § 5.5 step 6 (:661-665) | Typo while disabled is unknown command | STATE-5 (corrected: the index it prints carries the refusal line under its header) |
| § 5.5 step 7 (:667-670) | `/wg enable` acts at once, honors changes | STATE-6 (the change made while off is Popup Width, which `/wg test notify` reads; `notify.delay` is read only on the real join path) |
| § 5.5a steps 1-2 (:679-683) | Disable/enable then Logout clean | STATE-7 |
| § 5.5a steps 3-4 (:685-691) | Details link works enabled, dead disabled | STATE-8 |
| § 6 steps 1-3 (:700-704) | Value persists across `/reload` | PROFILE-10 |
| § 6 steps 4-6 (:706-711) | Value shared by a second character on `Default` | PROFILE-10 |
| § 7 step 1 (:719-721) | No out-of-date warning after an Interface bump | INSTALL-5 |
| § 7 steps 2-4 and API note (:723-727) | Pointer: run sections 1, 4, 5.1 | Before you start, "An `## Interface:` bump" row: § 1 → INSTALL-1 to INSTALL-4, COMBAT-1, COMBAT-2; § 4 → POPUP-1, POPUP-3 to POPUP-5, TELE-1 to TELE-4, TELE-6, COMBAT-6 to COMBAT-10, COMBAT-12; § 5.1 → LFG-1; plus INSTALL-5 (§ 7 step 1) and LOC-5 (§ 7a's patch-day re-run) |
| § 7a (:729-745) | `C_SpellBook.IsSpellKnown` and `IsSpellKnown` agree | LOC-5 (Pending sign-off) |
| § 8 steps 1-3 and TOC note (:751-757) | Lib refresh: reload, AceGUI renders, test notify | Before you start, "A `libs/` refresh" row (INSTALL-2, PANEL-1, PANEL-2, POPUP-1) |
| § 8 closing (:759) | After a LibKa0s re-vendor, run 10, 11, 12 | Before you start, "A LibKa0s re-vendor" row: § 10 → PANEL-14; § 11 → PANEL-1, PANEL-2 (via the `libs/` row), PANEL-4, PANEL-5, SLASH-9 to SLASH-11, POPUP-6, POPUP-8, DIAG-11; § 12 → DIAG-12 to DIAG-16, POPUP-7, DEGRADED-5 |
| § 9 steps 1-3 (:767-769, :779-780) | Degraded load: zero errors, complete `/wg list` | DEGRADED-1 (corrected: `/wg list` prints the settings-CLI line; schema completeness is `tests/test_libka0s.lua` "degraded: every HAND-WRITTEN schema row survives the options library's absence (options-ui-§1)"); the setup now also disables every other Ka0s addon |
| § 9 notices (:771-774, :781-782) | Notice wording and exact counts | DEGRADED-2 (the launcher's login notice added) |
| § 9 debug flag (:783) | `/wg debug on` still flips the flag | DEGRADED-3 |
| § 9 step 9 (:775, :784-786) | Diagnostics forms unavailable, write nothing | DEGRADED-4 (both forms name `/wg diagnostics`, as § 9 said) |
| § 10 (:792-801) | No raw locale keys on panel, console or chat | PANEL-14 |
| § 11.1 (:809-810) | Landing rows use one formatter, single spaces | PANEL-1 |
| § 11.2 (:811-812), layout | General tab strip and layout after adoption | PANEL-2 |
| § 11.2 (:811-812), comparison | Carried-over values unchanged from the previous build; five new keys arrive at their defaults; the Debug console tooltip wording differs | dropped: a one-time comparison with the pre-adoption build, which no longer ships (a thing that no longer exists). The defaults half is asserted by `tests/test_settings.lua` "settings: BuildDefaults covers every schema row" and "settings: the master rows keep this addon's own shipped defaults"; the library-owned wording by "settings: the Master controls rows are the COMPOSER's, not hand-written" |
| § 11.3 (:813-814) | Slider commits on release | PANEL-4 |
| § 11.4 (:815) | Defaults resets everything | PANEL-5 |
| § 11.5 (:816-817) | `/wg resetall` reaches the same confirm | SLASH-11 |
| § 11.6 (:818-819) | Bare `/wg reset` prints a deprecation notice, resets nothing | SLASH-9 |
| § 11.7 (:820-821) | `/wg reset <path>` resets one row, no confirm | SLASH-10 |
| § 11.8 (:822-823) | Popup and console share the window edge | POPUP-8 |
| § 11.9 (:824-825) | Popup position survives `/reload` | POPUP-6 |
| § 11.10 (:826-827) | Console position is not remembered (LIBKA0S-05) | DIAG-11 |
| § 12.1 (:842) | Console title-bar marks, not words | DIAG-12 |
| § 12.2 (:843) | Copy window close mark | DIAG-13 |
| § 12.3 (:844) | Log font is the library's JetBrains Mono | DIAG-14 |
| § 12.4 (:845) | Footer Close is the bare word | POPUP-7 |
| § 12.5 (:846) | One JetBrains Mono entry in LSM dropdowns | DIAG-15 |
| § 12.6 (:847) | Two Ka0s consoles match | DIAG-16 |
| § 12 closing (:849-852) | Art falls back with the library absent | DEGRADED-5 (corrected: no console opens with the library absent; the footer `Close` half kept) |
| § 12a.1 (:869) | Pooled tab labels over three passes | PANEL-15 (Pending sign-off) |
| § 12a.2 (:870) | Selection highlight | PANEL-16 (Pending sign-off) |
| § 12a.3 (:871) | Band height constant | PANEL-17 (Pending sign-off) |
| § 12a.4 (:872) | Body follows the selection | PANEL-18 (Pending sign-off) |
| § 12a.5 (:873) | Same on a fresh build | PANEL-19 (Pending sign-off) |
| § 12b step 1 (:917-924) | Localized activity name in the popup | LOC-1 (Pending sign-off) |
| § 12b step 2 (:925-929) | Long names fit or truncate | LOC-2 (Pending sign-off) |
| § 12b step 3 (:930-937) | Playstyle globals non-nil, row reads as words | LOC-3 (Pending sign-off) |
| § 12b step 4 (:938-946) | Teleport casts by the client's own name | LOC-4 (Pending sign-off) |
| § 12b step 5 (:947-972) | Run § 7a on this client, record six readings | LOC-5 (merged with § 7a; Pending sign-off) |
| § 12b step 6 (:974-978) | Boot, test notify and one real LFG flow unchanged | LOC-6 (Pending sign-off; § 1, § 4 and § 5.1 expanded as in the § 7 row, less INSTALL-5 and LOC-5) |
| § 12c.1 (:994-995) | AddOns list icon | LAUNCH-1 |
| § 12c.2 (:996-998) | Minimap button draws the logo | LAUNCH-2 |
| § 12c.3 (:999-1000) | Left-click opens the landing page, popup stays | LAUNCH-3 |
| § 12c.4 menu + Show window (:1001-1005) | Menu title, four entries, Show window toggles | LAUNCH-4 |
| § 12c.4 Test mode (:1006-1007) | Test mode entry | LAUNCH-5 |
| § 12c.4 Locked (:1008-1009) | Locked entry | LAUNCH-6 |
| § 12c.4 Enabled (:1010-1013) | Enabled entry stands down, others gray | LAUNCH-7 |
| § 12c.5 (:1014-1015) | Minimap drag persists | LAUNCH-9 |
| § 12c.6 (:1016-1017) | Minimap row hides at once | LAUNCH-10 |
| § 12c.7 (:1018-1023) | Hidden button survives profile switch, resetall, Defaults, Reset all | LAUNCH-11 (profile switch now via `/wg profile`) |
| § 12c.8 (:1024-1030) | Broker display entry | LAUNCH-12 |
| § 12c.9 (:1031-1036) | Launcher tooltip, enabled and disabled | LAUNCH-13 |
| § 13 checklist (:1038-1063) | 23 pointer items for a pre-release pass | Before you start, "Release pass" (re-pointed to new IDs; `/wg reset` item corrected to SLASH-9 and SLASH-11; the § 3.8 "both directions" item → COMBAT-9 to COMBAT-11, all three of its step groups; § 12a and § 12b listed by ID, PANEL-15 to PANEL-19 and LOC-1 to LOC-6, so they stay in the pass after sign-off) |
| § 13 closing (:1066-1070) | Re-vendor run list (§ 9, § 12, § 12a, the rest of § 11); § 7a never run; 80% note | Before you start, "A LibKa0s re-vendor, or a change to a seam file" row: § 9 → all of DEGRADED; § 12 as in the § 8 row; § 12a → PANEL-15 to PANEL-19; § 11 as in the § 8 row. The seam list is now the ten files CLAUDE.md names. § 7a status → Pending sign-off; the 80% note → the release row of "When to run what" |
| (new) | Profiles page: last, no Defaults, Ace controls | PROFILE-1 (the AceDBOptions controls named; no scope control exists) |
| (new) | Switch on the page re-applies, one `[Profile]` line | PROFILE-2 |
| (new) | `/wg profile` lists, sorted, current marked | PROFILE-3 |
| (new) | `/wg profile <name>` switches, open panel refreshes | PROFILE-4 |
| (new) | Already on the profile | PROFILE-5 |
| (new) | Unknown name refused, did-you-mean, nothing created | PROFILE-6 |
| (new) | Quotes stripped, spaces kept | PROFILE-7 |
| (new) | `profile` live while disabled; switch re-syncs the enable latch | PROFILE-8 |
| (new) | Switch refused in combat | PROFILE-9 |
| (new) | Popup position is account-wide across a switch | PROFILE-11 |
| (new) | Copy and Reset Profile log one `[Set]` line | PROFILE-12 |
| (new) | Reset all settings touches the active profile only | PROFILE-13 |
| (new) | Profiles page in combat: covered, refuses, draws at combat end | PROFILE-14 (headless: `tests/test_profiles.lua` "profiles: a page first shown in combat draws nothing, then draws once at combat end") |
| (new) | `/wg profile` unavailable without LibKa0s | DEGRADED-4 (added to the existing check) |
