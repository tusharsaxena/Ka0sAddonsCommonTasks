# Smoke map — BankLedger (SP-BL-03)

Baseline: `docs/smoke-tests.md` at BankLedger commit `16398dd` on `feat/2026-09-29-smoke-and-profile`,
which is master's doc plus S-30 (added by SP-BL-01). That doc is 1073 lines with 32 `## S-` sections
(S-1 … S-30, plus S-12a and S-12b), 246 numbered steps and one unnumbered note (S-29). Master's doc
is 1022 lines and has no S-30. New: 879 lines, 218 checks in 14 themes (INSTALL 10, SLASH 4,
PANEL 31, PROFILE 14, STATE 9, COMBAT 8, CAPT 17, LEDG 46, INS 18, FILT 14, SESS 12, DIAG 19,
DEGRADED 11, LOC 5). Dropped: 0. Seven checks are new (PROFILE-8 – 13, DEGRADED-6: the `/bl profile`
verb). The old doc had no Result lines and no filled-in sign-off batches, and its checks are owed:
besides its NOT YET RUN marks (S-24 – S-27), Session BL of the 2026-09-23 remediation's checklist
(`2026-09-23-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/06_SMOKE_TESTS.md`, BL.1 – BL.19, no recorded
result; `RESUME.md` still owes "the in-client sessions") names STATE-7 (BL.13), COMBAT-5/6 (BL.15),
CAPT-16 (BL.16), SESS-9 and CAPT-9 (BL.17), and in BL.19 a walk of the whole doc. Under the clarified
Pending policy (spec S4, 2026-09-29) "Pending sign-off" lists 210 of the 218 checks by new ID with
origin and reason: the seven new checks; the steps whose expectations SP-BL-01 rewrote for profiles
(S-12 step 3 and S-16 step 3 → PANEL-27, PANEL-28; S-16 step 5 → PANEL-29; S-17 step 15 → SESS-10;
S-20 step 9 → DIAG-19; `git diff master 16398dd -- docs/smoke-tests.md`); every check whose
expectation SP-BL-03 or SP-BL-03R corrected against the code (INSTALL-2, SLASH-3, PANEL-17, PANEL-19,
PANEL-29, PANEL-31, COMBAT-4, CAPT-12, CAPT-14, CAPT-15, LEDG-19, INS-18, FILT-8, DIAG-19,
DEGRADED-1 – 5, DEGRADED-7, DEGRADED-8, DEGRADED-11); the never-run S-24 – S-27 and S-30; and every other
carried-over check, none of which has a recorded pass. Eight checks are not pending, because a recorded
pass covers them and their expectation is unchanged: INSTALL-4 (S-1 step 5 as M6-BL `328c119`
wrote it, unchanged since: `06_SMOKE_TESTS.md` X1.4, "Recorded 2026-09-25: PASS (after M6)", every
addon) and DIAG-13 – 18 and COMBAT-8 (S-14 steps 14–17 as DR-BL-05 `331b4d0` wrote them, unchanged
since: `2026-09-25-DIAGNOSTICS_COMMAND/99_REPORT.md` rows BL-S1 – BL-S5, BL-S7, BL-S8, BL-X1, PASS owner
2026-09-26). Partly covered and so still pending: INSTALL-3 (X1.4 recorded the status tooltip,
not the button's own logo or the same art beside Ka0s Bank Ledger in the AddOns list, which
`0b556b7` added on 2026-09-16), INSTALL-5 (X1.4 recorded the menu opening, not the
Show window entry opening, ticking and closing the ledger), INSTALL-6 (X1.4 recorded the menu opening, not the
Test mode and Locked echoes), STATE-4 (X1.4 recorded the disabled clicks, not the grayed menu entries),
DIAG-1 – 12 (the diagnostics run recorded only S-14's report steps) and DEGRADED-5 (BL-X2 recorded its
diagnostics line; the rest was corrected). No other plan records a BankLedger pass: X1.3's
`/bl set settings.visibility bogus` refusal (PASS 2026-09-24) matches no check, the NAVRAIL RV-S1 pass
compares pages with an earlier build rather than any check's expectation, and the 2026-09-22 sweep's
"all 20 passed" names no check (and S-12 and S-16 were rewritten on 2026-09-24, after it).

Stale items fixed on the way: the hardcoded `v1.2.0` (S-1, S-18) is now `v<version>`; S-23 step 3's
`/bl export` (not a verb) is now the Export button; S-18 step 7's pointer to a non-existent "S-21 step 10"
is now DEGRADED-9; S-12 step 7's "`/bl` reports the same entry count" (bare `/bl` opens the panel) is
now History's row count; S-25's "v1 → v2" title now matches its v1 → v4 steps. S-25 steps 3–4 and 7
could never pass: `NS:RunMigrations` logs `[Migrate]` only when `NS.State.debug` is on
(`core/Database.lua:201`), it runs from `NS:InitDB` in `addon:OnInitialize` (`core/Database.lua:14`,
`core/BankLedger.lua:36`) before any slash command, and the flag is session-only and off at every
login (`core/State.lua:27`). INSTALL-8 now reads the stamp from `/bl debug diagnostics`' `[State]`
line (`modules/Diagnostics.lua:74`), INSTALL-9 reads the stripped `vendorPrice` from the file, and
INSTALL-10 watches the ladder re-run on a profile switch (`NS.OnProfileEvent` calls
`NS:RunMigrations`), the one place logging can already be on. S-18 carried expectations the degraded
arm does not meet: step 5's complete `/bl list` is now the one CLI-unavailable line the stub prints
(`settings/Slash.lua:241-247`), so step 8's byte-for-byte compare now uses a healthy `/bl list` taken
before the rename (Before you start); step 6's console opening is now the one-line unavailable answer
of `core/DebugLogSetup.lua:28`; step 7's console and Copy box, unreachable in that state, leave
DEGRADED-7 to the ▲/▼ columns and DEGRADED-11 to the console font. Steps 3, 4 and 6 also missed that
`addon:OnInitialize` registers the settings category (`core/BankLedger.lua:41`), which ends in the
stub's once-only `CreateOptionsPanel` (`settings/Panel.lua:780`, `settings/OptionsSetup.lua:146-151`);
that is the addon's first printed line, so the notice (`core/CoreSetup.lua:79-93`) and the
settings-panel-unavailable line both print at login (DEGRADED-1), `/bl version` prints only
`[BL] v<version>` (DEGRADED-3), and `/bl config` opens nothing and prints nothing (DEGRADED-5).
Reproduced headlessly: a degraded TOC load, `addon:OnInitialize`, then the slash handler.

Third review (SP-BL-03R), every expected string re-read against the code and `libs/LibKa0s`:
- PANEL-31 dropped old S-20 step 6's "Database size line updates": Yes keeps the ledger
  (`settings/Slash.lua:105-113`, `db:ResetProfile()` only) and the line is estimated from the ledger
  alone (`settings/Panel.lua:130-143`, `core/Database.lua:874`). PANEL-29 reads the count.
- PANEL-29 now has a setup a client can arrange (ledger window on Insights, General ▸ History's
  read-out beside it, `/bl resetall`), and keeps only the history half; the live list-empty half is
  PANEL-31's.
- DIAG-19 starts with a reset while logging is off: `countResetRows` (`settings/Slash.lua:73-83`)
  counts every profile row off its default, and earlier checks leave some (SESS-11's Session window,
  FILT-5's and CAPT-15's Minimum quality). It also reopens the console after each reset, because
  `endSessionState` (`core/Database.lua:274-279`) closes it.
- COMBAT-4: a click on the Test mode box in combat is refused by the Options combat lock
  (`libs/LibKa0s/OptionsCombat.lua`, COMBAT-3), so the refused start is read from `/bl test`
  (`modules/LedgerTable_TestMode.lua:242`) and the box after combat.
- CAPT-12 turns logging on before it reopens the guild bank: old S-17 step 13 watched for the
  `[Store] GUILD_BANK opened` line without it, and S-14 steps 6–7 had turned it off and reloaded; the
  line is gated on `NS.State.debug` (`modules/Ledger.lua:790-796`). Listed under Pending sign-off.
- CAPT-14 and CAPT-15 turn logging on after the `/reload`: the flag is session-only
  (`core/State.lua:27`) and the `[Store]` and `[Skip]` lines are gated on it
  (`modules/Ledger.lua:519-522`, `:790-796`).
- SLASH-3: while disabled, an unknown verb prints the index with its refusal line under the header
  (`libs/LibKa0s/Slash.lua` `PrintHelp`, `OnSlash`).
- PANEL-17 and PANEL-19: the AceGUI slider box reads `2`, `1` and `10%`
  (`libs/AceGUI-3.0/widgets/AceGUIWidget-Slider.lua:20-27`; Master alpha is `isPercent`).
- FILT-8: `Looking up items...` (`libs/LibKa0s/OptionsIds.lua:195`, three periods).
- INS-18: the two empty-state lines of `modules/Insights.lua:538-540`; Character: Current is a filter
  (`modules/Browser.lua:475-485`).

| Old location | Behavior | New ID |
|---|---|---|
| S-1 steps 1, 3 | Log in with zero Lua errors | INSTALL-1 |
| S-1 step 2 | `/bl version` line | INSTALL-2 |
| S-1 step 4 | Minimap button art and tooltip | INSTALL-3 |
| S-1 step 5 | Left-click opens the landing page | INSTALL-4 |
| S-1 step 6 | Right-click options menu: shape, Show window opens and (clicked again) closes the ledger; Test mode and Locked echo their verbs and undo | INSTALL-5, INSTALL-6 |
| S-1 step 7 | Broker display plugin | INSTALL-7 |
| S-2 steps 1–3 | Character bank deposit row | CAPT-1 |
| S-2 steps 4–5 | Partial withdrawal row | CAPT-2 |
| S-3 steps 1–3 | Loot or mail with the bank open records nothing | CAPT-3 |
| S-4 steps 1–3 | Warband items in and out, round-trip delay | CAPT-4 |
| S-4 step 4 | Store dropdown lists only stores the data holds | LEDG-5 |
| S-5 steps 1–4 | Warband gold row shape, tooltip, withdrawal | CAPT-5 |
| S-5 step 5 | Character bank purse change is not gold | CAPT-6 |
| S-5 step 6 | Spending at the bank is not a deposit | CAPT-7 |
| S-5 step 7 | `debug scan` money API block | CAPT-8 |
| S-6 steps 1–2 | Guild bank item row, CSV `guild` column | CAPT-9 |
| S-6 step 3 | Guild gold row; closed frame's 0 balance not read as a gain | CAPT-10, CAPT-11 |
| S-6 step 4 | Guild bank arms (`openContext=GUILD_BANK`) | CAPT-12 |
| S-6 step 5 | Guild bank disarms on close | CAPT-13 |
| S-7 step 1 | Toggle and Esc | LEDG-1 |
| S-7 step 2 | Ledger geometry persists (drag, resize-only, reload while open) | LEDG-2 |
| S-7 step 3 | Minimum width | LEDG-3 |
| S-7 step 4 | windowScale rescales both windows, slash and slider | PANEL-16 |
| S-8 step 1 | Search lowers the row count | LEDG-4 |
| S-8 step 2 | Store multi-select label | LEDG-5 |
| S-8 step 3 | Column sort and reverse | LEDG-6 |
| S-8 step 4 | Group by Store | LEDG-7 |
| S-8 step 5 | Sub-type and Quality options, quality order and colors | LEDG-8 |
| S-8 step 6 | Type/Sub-type ▸ Gold | LEDG-9 |
| S-8 step 7 | Direction and Store menu colors | LEDG-10 |
| S-8 step 8 | Character: Current by default; test mode opens unscoped | LEDG-11, LEDG-21 |
| S-8 step 9 | Class icons and colors | LEDG-12 |
| S-8 step 10 | Group by Type, Sub-type, Quality | LEDG-13 |
| S-8 step 11 | Clear returns to defaults | LEDG-14 |
| S-8 step 12 | Save · Reset · Clear cluster | LEDG-15 |
| S-8 step 13 | Save a view, Clear and reload land on it | LEDG-16 |
| S-8 step 14 | Character scope never saved | LEDG-17 |
| S-8 step 15 | Reset the view; resetall and Defaults discard it | LEDG-18, PANEL-28 |
| S-8 step 16 | Test mode ignores the saved view and restores it | LEDG-21 |
| S-9 step 1 | Fourteen stat cards and hover text | INS-1 |
| S-9 step 2 | Card headline fits | INS-2 |
| S-9 step 3 | Net colors | INS-3 |
| S-9 step 4 | Deposits vs Withdrawals bar and caption | INS-4 |
| S-9 step 5 | By Character and × Store | INS-5 |
| S-9 step 6 | Back-to-back companions | INS-6 |
| S-9 step 7 | Companion titles | INS-7 |
| S-9 step 8 | By Quality | INS-8 |
| S-9 step 9 | Type and Sub-type bars | INS-9 |
| S-9 step 10 | Per-day strip | INS-10 |
| S-9 step 11 | By Hour Of Day | INS-11 |
| S-9 step 12 | Enriched slice spreads | INS-12 |
| S-9 step 13 | Top Of The List grid | INS-13 |
| S-9 step 14 | GOLD block | INS-14 |
| S-9 step 15 | One filter across both tabs | INS-15 |
| S-9 step 16 | Resize re-flow | INS-16 |
| S-9 step 17 | Live update | INS-17 |
| S-9 step 18 | Empty ledger after purge | INS-18 |
| S-10 steps 1–2 | Copy window opens preselected, monospace; Ctrl+C; Esc | LEDG-28, LEDG-29, LEDG-31 |
| S-10 step 3 | Row count matches the table | LEDG-29 |
| S-10 step 4 | wowhead column bonus URLs | LEDG-33 |
| S-10 step 5 | Insights export is the sectioned summary | LEDG-34 |
| S-11 step 1 | Blacklist from a row, chat names tab and sub-tab | FILT-1 |
| S-11 step 2 | Blacklisting is point in time | FILT-2 |
| S-11 step 3 | List entry shape, tooltip, X removes | FILT-3 |
| S-11 step 4 | Add box's three forms, uncached id fills in | FILT-4 |
| S-11 step 5 | Whitelist beats the quality floor | FILT-5 |
| S-11 step 6 | Defaults clears both lists; no Filters page in the tree | PANEL-28, PANEL-2 |
| S-11 step 7 | Name dropdown, rank labels, `+N more` | FILT-6 |
| S-11 step 8 | Picking adds; ambiguous name refused | FILT-7 |
| S-11 step 9 | Name not seen this session resolves | FILT-8 |
| S-11 step 10 | Unknown name refused with the full sentence | FILT-9 |
| S-12 step 1 | `/bl config`, bare `/bl`, `/bl help` | SLASH-1 |
| S-12 step 2 | Landing page logo, tagline, commands | PANEL-1 |
| S-12 step 3 | General header and skinned Defaults; tab strip and Loot History parity; Master controls rows; minimap checkbox and CLI; alpha floor; reset popup and what Yes resets; Capture, Interface, History, Filters tabs; tab revisit | PANEL-3, PANEL-4, PANEL-5, PANEL-15, PANEL-19, PANEL-27, PANEL-28, PANEL-6, PANEL-7, PANEL-8, PANEL-9, PANEL-10 |
| S-12 steps 4–5 | Panel and CLI read one value | SLASH-2 |
| S-12 step 6 | Scrollbar on both pages | PANEL-12 |
| S-12 step 7 | Blizzard's footer Defaults reaches the addon | PANEL-27 (footer route and its Yes; outcome as PANEL-28) |
| S-12a step 1 | Default row tints | PANEL-21 |
| S-12a steps 2–3 | Stripe slider live, 0 removes banding | PANEL-22 |
| S-12a step 4 | Hover slider | PANEL-23 |
| S-12a step 5 | Session table shares the tints | PANEL-24 |
| S-12a step 6 | CLI clamps tint values | PANEL-25 |
| S-12a step 7 | resetall restores 0.03 / 0.10 | PANEL-28 |
| S-12b step 1 | Master alpha fades ledger, session, export | PANEL-18 |
| S-12b step 2 | Alpha floor keeps windows findable | PANEL-19 |
| S-12b step 3 | Lock frame on all three windows | STATE-8 |
| S-12b step 4 | Reset position | PANEL-20 |
| S-12b step 5 | General visibility Never | STATE-9 |
| S-12b step 6 | Only out of combat, window open | COMBAT-5 |
| S-12b step 7 | Only out of combat, window closed | COMBAT-6 |
| S-12b step 8 | Only in combat | COMBAT-7 |
| S-13 steps 1–3 | `/bl config` refused in combat, no auto-open | COMBAT-1 |
| S-13 step 4 | Ledger works in combat | COMBAT-2 |
| S-13 step 5 | Open panel's combat cover | COMBAT-3 |
| S-14 step 1 | Console opens, Debug: OFF | DIAG-1 |
| S-14 step 2 | Logging on, `[Init]` summary | DIAG-2 |
| S-14 step 3 | One `[Move]` per pass | DIAG-3 |
| S-14 step 4 | Scrollbar and 3000-line counter | DIAG-4 |
| S-14 step 5 | Copy and Clear | DIAG-5 |
| S-14 steps 6–7 | Logging off; reload resets the flag | DIAG-6 |
| S-14 step 8 | Console chrome and smaller close | DIAG-7 |
| S-14 step 9 | Three title-bar marks | DIAG-8 |
| S-14 step 10 | No tooltips on the marks | DIAG-9 |
| S-14 step 11 | Monospace log | DIAG-10 |
| S-14 step 12 | Indistinguishable from another Ka0s console | DIAG-11 |
| S-14 step 13 | Addon-owned dumps with logging off | DIAG-12 |
| S-14 step 14 | Diagnostics report: appends, sections, second report and copy, guild cache caveat | DIAG-13, DIAG-14, DIAG-15, DIAG-16 |
| S-14 step 15 | Diagnostics while disabled; `debug diag` / `diag` | DIAG-17 |
| S-14 step 16 | Diagnostics in combat | COMBAT-8 |
| S-14 step 17 | Buffer cap | DIAG-18 |
| S-15 steps 1–2 | Test mode badge, features work on the sample | LEDG-20 |
| S-15 step 3 | Sample reads like a real bank | LEDG-22 |
| S-15 steps 4–5 | Sample row menu grays mutating actions; lists unchanged | LEDG-23 |
| S-15 step 6 | Back to real data; Delete on a real row | LEDG-24 |
| S-15 step 7 | Master controls box is the same switch | LEDG-25 |
| S-15 step 8 | Combat ends test mode, refuses a start | COMBAT-4 |
| S-15 step 9 | Refused start leaves the box unticked | LEDG-26 |
| S-15 step 10 | Resets end test mode; never saved | LEDG-27 (reload); reset routes: PANEL-27, PANEL-28 |
| S-16 step 1 | Retention prunes on reload | CAPT-16 |
| S-16 step 2 | Purge | CAPT-17 |
| S-16 step 3 | Reset all settings confirm, recenters, keeps ledger, one button placement | PANEL-27, PANEL-28 (placement: PANEL-5, PANEL-8) |
| S-16 step 4 | Capture sees the reset without a reload | PANEL-30 |
| S-16 step 5 | Open views keep the history, lists empty at once | PANEL-29 (lists empty at once: PANEL-31) |
| S-16 step 6 | Reset while disabled re-enables | STATE-7 |
| S-17 step 1 | Session window opens with the bank, empty | SESS-1 |
| S-17 step 2 | Session window shape and columns | SESS-2 |
| S-17 step 3 | Headers do not sort | SESS-3 |
| S-17 steps 4–5 | Deposit and withdraw rows at once | SESS-4 |
| S-17 step 6 | Gold row | SESS-5 |
| S-17 steps 7–9 | Drag, close with the bank, reopen empty in place | SESS-6 |
| S-17 steps 10–11 | History holds the visit; delete propagates | SESS-7 |
| S-17 step 12 | Warband and guild drive the same window | SESS-8 |
| S-17 step 13 | Guild bank OnShow/OnHide; `[Store]` baseline; hooks line | SESS-9, CAPT-12, CAPT-13 |
| S-17 step 14 | No guild session away from a bank (#12) | CAPT-14 |
| S-17 step 15 | Session geometry across reload and characters | SESS-10 |
| S-17 step 16 | Session window setting | SESS-11 |
| S-17 step 17 | `/bl session` preview and refusal | SESS-12 |
| S-18 steps 1–2 | Degraded login, zero errors (now also the two login lines) | DEGRADED-1 |
| S-18 step 3 | Exact notice text, shared clause (read at login, not after `/bl version`) | DEGRADED-2 |
| S-18 step 4 | Notice said once (`/bl version` prints only the version line) | DEGRADED-3 |
| S-18 step 5 | Degraded `/bl list` (now the CLI-unavailable line) | DEGRADED-4 |
| S-18 step 6 | Ledger works; no panel and no line on `/bl config` (its line printed at login); console and diagnostics answer one unavailable line each | DEGRADED-5 (login line: DEGRADED-1) |
| S-18 step 7 | Media fallbacks on the reachable surfaces | DEGRADED-7 (console font: DEGRADED-11) |
| S-18 step 8 | Restore; `/bl list` matches the healthy listing | DEGRADED-11 (listing kept under Before you start) |
| S-19 steps 1–4 | No raw locale keys on screen or in chat | PANEL-14 |
| S-20 steps 1–2 | Slash `set` repaints the Enable box | PANEL-26 |
| S-20 step 3 | windowScale slider and both windows | PANEL-16 |
| S-20 steps 4–5 | Scale clamp and reset | PANEL-17 |
| S-20 steps 6–8 | resetall repaints once (step 6's Database size line no longer changes; PANEL-29 reads the count); list empties; closed panel | PANEL-31 |
| S-20 step 9 | One `[Set] reset profile` line | DIAG-19 |
| S-21 step 1 | Ledger close mark | LEDG-35 |
| S-21 step 2 | Session and Export close marks; copy window's library close | LEDG-35, LEDG-36 |
| S-21 step 3 | Dropdown chevrons and the white tick | LEDG-37 |
| S-21 step 4 | Gold sort arrows and group chevrons | LEDG-38 |
| S-21 step 5 | No marks on bar buttons; Export to CSV mark and width | LEDG-39 |
| S-21 step 6 | Search magnifier | LEDG-40 |
| S-21 step 7 | No mark tooltips | LEDG-41 |
| S-21 step 8 | No marks in the settings panel | PANEL-13 |
| S-21 step 9 | Degraded: filter bar refuses; fallback marks gold; modal unreachable | DEGRADED-8, DEGRADED-9, DEGRADED-10 (the filter-bar chat line is expected at DEGRADED-5's first `/bl show`, the only one that builds the window) |
| S-22 step 1 | First click opens the menu, glyph rows | LEDG-42 |
| S-22 step 2 | Escape closes window and menu, modal too | LEDG-43 |
| S-22 step 3 | `/bl hide` and `/bl toggle` close the menu | LEDG-44 |
| S-22 step 4 | One menu at a time; click-through lands | LEDG-45 |
| S-22 step 5 | Collapsed multi-select keeps its filter's name | LEDG-46 |
| S-23 step 1 | Item seam loads before Constants (zero errors) | INSTALL-1 |
| S-23 step 2 | Minimum quality names and colors; client's own names | PANEL-6, LOC-5 |
| S-23 step 3 | Quality words in table, filter and export | LEDG-19 |
| S-23 step 4 | Uncached item refused (F-006) | CAPT-15 |
| S-24 steps 1–2 | Copy window centered on the ledger, preselected | LEDG-28 |
| S-24 step 3 | Whole CSV with `\r\n` | LEDG-29 |
| S-24 step 4 | Same window reused | LEDG-30 |
| S-24 step 5 | Esc leaves the modal open | LEDG-31 |
| S-24 step 6 | Copy window follows the ledger | LEDG-32 |
| S-24 step 7 | Library close glyph, 18×18, red hover | LEDG-36 |
| S-25 steps 1–4 | v1 → v4 migration on a real store (evidence now `[State]` stamp; the `[Migrate]` line is unobservable in a client) | INSTALL-8 (rows touched: INSTALL-9) |
| S-25 steps 5–6 | Stamp survives a logout; planted `vendorPrice` stripped | INSTALL-9 |
| S-25 step 7 | No migration on a stamped store (watched on a profile switch, since login cannot be logged) | INSTALL-10 |
| S-26 steps 1–4 | Tab strip survives pooling | PANEL-11 |
| S-27 step 1 | Type facets in the client's language | LOC-1 |
| S-27 step 2 | Export contract on a non-English client | LOC-2 |
| S-27 step 3 | Sort and search over non-ASCII | LOC-3 |
| S-27 step 4 | Nothing else moved: walk S-1, S-2, S-8 | LOC-4 (INSTALL-1 – 7, CAPT-1, CAPT-2, LEDG-4 – 18, LEDG-21) |
| S-28 steps 1–2 | Disable takes both windows down at once | STATE-1 |
| S-28 step 3 | Nothing recorded while disabled | STATE-2 |
| S-28 step 4 | Silent on combat edges | STATE-3 |
| S-28 step 5 | Minimap button and menu while disabled | STATE-4 |
| S-28 step 6 | Live verbs answer while disabled | SLASH-3 |
| S-28 step 7 | Feature verbs refused once | SLASH-4 |
| S-28 step 8 | Disabled survives a reload | STATE-5 |
| S-28 step 9 | Re-enable resumes; settings changed while disabled honored | STATE-6 |
| S-29 steps 1, 3 | Two to a row, both lists | FILT-10 |
| S-29 step 2 | Odd count | FILT-11 |
| S-29 step 4 | Long names truncate, hover names | FILT-12 |
| S-29 step 5 | Remove and add repack | FILT-13 |
| S-29 steps 6–7 and the closing note | One-column fallback and back | FILT-14 |
| S-30 step 1 | Schema v3 lift on a real store | PROFILE-14 |
| S-30 step 2 | Profiles page | PROFILE-1 (tree: PANEL-2) |
| S-30 step 3 | New profile is fresh over the same history | PROFILE-2 |
| S-30 step 4 | Switching back restores | PROFILE-3 |
| S-30 step 5 | Enable is per profile | PROFILE-4 |
| S-30 step 6 | Reset Profile keeps history; resetall wording and Yes | PROFILE-5; resetall half: PANEL-27, PANEL-28 |
| S-30 step 7 | One debug line per profile event | PROFILE-6 |
| S-30 step 8 | Retention account-wide, nothing prunes (D6) | PROFILE-7 |

New checks with no old location: PROFILE-8 (`/bl profile` lists), PROFILE-9 (switch and already-current),
PROFILE-10 (unknown name refused, did-you-mean, never created), PROFILE-11 (quotes and spaces), PROFILE-12
(answers while disabled), PROFILE-13 (combat refusal), DEGRADED-6 (library-absent line).

Inbound references re-pointed: `docs/debug.md:6` (S-14 → the DIAG checks), `docs/media.md:88`
(S-21 step 3 → LEDG-37), `docs/media.md:97` (S-14 → DIAG-8), `docs/midnight-quirks.md:121` (S-21 step 9
→ DEGRADED-9), `tests/test_database.lua:391-396` and `:413-415` (S-25 → INSTALL-8 to 10, and the note that no in-game check can read the `[Migrate]` line; the case `RunMigrations announces the v1->v4 pass the smoke step reads` is renamed `… in one [Migrate] line`, with `docs/test-cases.md` regenerated), `tests/test_docs.lua:15` (S-27 → the
Non-English client section, LOC-1 on). The doc's own citations of `ConsumableMaster … § 3c` and
`KickCD … § 9b` are now `ConsumableMaster LOC-1` and `KickCD LOC-1`. Left as history: frozen bundles under
`docs/audits`, `docs/reviews`, `docs/revendor`, `docs/automated-tests`, and the 2026-07-26 design spec
under `docs/superpowers/specs/` (cites S-17 and S-9).
