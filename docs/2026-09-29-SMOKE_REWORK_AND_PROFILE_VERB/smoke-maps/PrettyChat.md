# Smoke map — PrettyChat (SP-PC-03)

Old `docs/smoke-tests.md`: 1186 lines, 83 `####` checks (T-01 … T-107 with letter suffixes, T-26b used
twice, plus SMK-F001) and a 4-step quick recipe, 87 checks in all, in 14 groups with two formats and two
ID schemes. New: 724 lines, 128 checks in 13 themes (INSTALL 7, SLASH 10, PANEL 21, PROFILE 10, STATE 6,
COMBAT 4, OVR 10, TEST 6, RESET 13, LAUNCH 7, DIAG 19, DEGRADED 10, LOC 5). Dropped: 0. Eleven checks
are new: PROFILE-1 – 10 (the Profiles page and the `/pc profile` verb) and DEGRADED-9 (the verb's
library-absent line). OVR-10 is not new: it is quick-recipe step 3 given an ID. The old doc had no
Result lines and no filled-in sign-off batches. "Pending sign-off" follows the
clarified S4 policy (2026-09-29): it lists 115 of the 128 checks by new ID with origin and reason:
the 11 new checks (PROFILE-1 – 10, DEGRADED-9), the 22 whose expectation this rework corrected
against the code, the old checks an owed list names as never run (T-99, T-104 – T-107 marked NOT YET
RUN; T-97/T-98 in `2026-08-24-LIBKA0S_FURTHER_MODULES/08_EXECUTION_RECORD.md` "recorded, not run";
T-29c on the 2026-09-07 owed checklist; SMK-F001 as Q.12 of the 2026-09-23 checklist, whose sign-off
table is empty), and every other old check, none of which has a recorded pass. Thirteen checks are
not pending because a recorded pass covers them and their expectation is unchanged: DIAG-1,
DIAG-3 – 8, DIAG-14, COMBAT-4 and DEGRADED-8 (T-39 steps 1–2 and 4–10, T-29b step 6, T-90 step 7:
`2026-09-25-DIAGNOSTICS_COMMAND/99_REPORT.md` §6, PC-S1 – PC-S11 and PC-X1, PASS owner 2026-09-26),
and LAUNCH-2 – 4 (T-65, T-65a: `2026-09-23-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/06_SMOKE_TESTS.md`
X1.4, "Recorded 2026-09-25: PASS (after M6)", every addon). DIAG-2 (T-39 step 3) stays pending: no
PC-S row covers the `[Globals]` line. An earlier review had the new checks removed from Pending under
the old wording; the SP-PC-03R re-do restored them. The old "When to run what" table is now the "Which
checks to run" table under Before you start, with each row naming the new ID of every check its old
groups held (plus the routine row's four checks, which stand in for the quick recipe), and "Reporting
a failure" is the paragraph after it.

Stale items fixed on the way: T-103 (2) and T-52 said `/pc test` prints to chat with `[PC]` on every
line, but it writes to the debug console (`settings/Slash.lua` `runTest` → `TestToConsole`); the chat
form survives only on a library-absent install (DEGRADED-6). T-51 expected `/pc set … Wrong` to be
skipped by Test; dropping conversions is allowed and saves (SLASH-10). T-55 expected
`unknown category 'Bogus'` from `/pc reset Bogus`; it answers `Setting not found: Bogus` (RESET-7).
T-57 (3) and T-59 used `/pc reset loot`, which now only prints the path deprecation; they use
`/pc reset <path>` now. T-98 expected the landing tagline and a proportional console on a
library-absent install, but both the panel and the console are unavailable there (T-90's own lines).
T-102 said Loot has nineteen strings; `defaults/Defaults.lua` has 17 (the two `LOOT_ITEM_CREATED_SELF`
globals moved to Tradeskill). T-100's layout lacked the Minimap button row. T-43 named
`PrettyChatDB.profile.categories`; the file key is `profiles.Default`. T-31a's headers carried a
trailing colon the code does not print. T-32 / T-33 used pre-library error wording. T-104's
`modules/Override.lua:294-304` citation pointed at `EnsureCategoryDB`; the restore arm is `:332-341`.
T-90 said the missing console window is reported once; the stub reports it once per entry point
(`core/DebugLogSetup.lua` `announcer`), so `/pc debug on` and then `/pc debug` each print it (DEGRADED-3).
T-67's "switch to another AceDB profile (or create one)" now uses the Profiles page and `/pc profile`.
T-106 expected an empty or `nil` `Original:` line for a global the client does not define; both `/pc test`
(`modules/Override.lua` `printStringRow`) and the panel's Original box (`settings/Panel.lua`) print the
gray `(original not available)` placeholder there (pinned by `tests/test_override.lua`), so LOC-4 now
fails on that placeholder. The quick recipe's step 4 exercised both the toggle and the edit boxes;
PANEL-16 now carries the toggle half too (untick the row's Enable, the next line is Blizzard's at once,
no `/reload`, and ticks it back). The SP-PC-03R re-verification of every expected string against the
code (a headless drive of the real dispatcher) fixed three more: SLASH-3 said "about 170 lines" for
`/pc list`, which prints 180 (170 setting rows, nine group headings and the header); SLASH-6 said
`/pc get` answers `true` and a "quoted" format, but it echoes `<path> = <value>` and the library
renders a string unquoted; RESET-5 said the reset echo shows the default "pipes doubled", but it goes
through the same `Schema.FormatValue` as `/pc get`, so chat shows the single pipes SLASH-6 and
PANEL-17 describe.

| Old location | Behavior | New ID |
|---|---|---|
| Quick recipe step 1 | `/reload` re-runs the file-load builders with no error | INSTALL-2 |
| Quick recipe step 2 | `/pc test` sample into the console, ignores enable toggles | TEST-1, TEST-3 |
| Quick recipe step 3 | One real chat event reads right | OVR-10 |
| Quick recipe step 4 | Exercise the changed row's toggle and edit boxes (both halves now in PANEL-16) | PANEL-16 |
| B / T-01 | Clean load, no errors, `/pc test` prints every category | INSTALL-1 |
| B / T-02 | Overrides and disabled strings survive `/reload` | INSTALL-3 |
| B / T-03 | `/pc` and `/prettychat` help identical, version header, fourteen commands | SLASH-1 |
| O / T-10 | Master off restores every original, customizations kept | STATE-1 |
| O / T-11 | Per-category toggle off | OVR-1 |
| O / T-12 | Per-string toggle off | OVR-2 |
| O / T-13 | Layer priority, three phases | OVR-3 |
| O / T-14 | Master off survives `/reload`, on again at once | INSTALL-4 |
| S / T-20 | `/pc config` lands on the landing page, no breadcrumb | PANEL-1 |
| S / T-21 | Rail auto-expands, three sub-pages, categories not in rail | PANEL-2 |
| S / T-22 | Breadcrumb atlas separator and gold divider | PANEL-3 |
| S / T-23 | Per-string editor layout | PANEL-14 |
| S / T-24 | Preview renders color escapes | PANEL-15 |
| S / T-25 | Row Reset always visible, no-op at default | RESET-1 |
| S / T-26 | Categories Defaults (header and footer) resets every tab, no popup, tooltip, one log line per press (header and footer) | RESET-3, RESET-4, RESET-12 |
| S / T-26b (first, :156) | General Defaults is the reset-all popup; minimap stays hidden | RESET-9, LAUNCH-6 |
| S / T-26a | Categories tab strip order, selection, swap, wrap | PANEL-8 |
| S / T-26b (second, :173) | Categories footnote | PANEL-10 |
| S / T-27 | Reset all settings popup and its effect | RESET-8 |
| S / T-28 | Edit and Enter commits, Preview and live chat follow | PANEL-16 |
| S / T-29 | `\|\|` in the edit box, `\|` from `/pc get` | PANEL-17 |
| S / T-29a step 1 | Master controls first two rows | PANEL-7 |
| S / T-29a steps 2–3 | Debug console checkbox shows and hides the window, not the flag | DIAG-9 |
| S / T-29a steps 4–5 | Checkbox tracks close, Esc and `/pc debug` | DIAG-10 |
| S / T-29b step 1 | Console fully wired on first open | DIAG-11 |
| S / T-29b steps 2–3 | Line counter climbs and pins at 3000 | DIAG-12 |
| S / T-29b steps 4–5 | Scrollbar tracks the wheel and drives the log | DIAG-13 |
| S / T-29b step 6 | Copy window at a full buffer | DIAG-14 |
| S / T-29b step 7 | Clear empties, counter resets, bar inert but visible | DIAG-15 |
| S / T-29c | Landing logo does not leak through AceGUI's pool | PANEL-6 |
| L / T-30 | `/pc list` whole listing | SLASH-3 |
| L / T-31 | `/pc list <Category>` case-insensitive, unknown category | SLASH-4 |
| L / T-31a | `/pc list category` and `formatstring` | SLASH-5 |
| L / T-32 | `/pc get` for each row kind and a bad path | SLASH-6 |
| L / T-33 | `/pc set` boolean spellings and a bad one | SLASH-7 |
| L / T-34 | `/pc set` a format string, live line | SLASH-8 |
| L / T-34a steps 1–2, 5 | Surplus conversion refused on slash and panel | SLASH-9 |
| L / T-34a steps 3–4, 6 | Fewer conversions allowed; reset after | SLASH-10 |
| L / T-35 | `/pc reset <path>` resets one row | RESET-5 |
| L / T-36 | `/pc resetall` | RESET-10 |
| L / T-37 | `/pc config` and `OpenConfig` refused in combat | COMBAT-1 |
| L / T-38 | Unknown verb, bare and padded `/pc`, `/pc help` | SLASH-2, SLASH-1 |
| L / T-39 steps 1–2 | Report appended after the trace, markers, chat line, sections | DIAG-1 |
| L / T-39 step 3 | `[Globals]` mismatch=0 | DIAG-2 |
| L / T-39 step 4 | Doubled pipes in `[Set]`, Copy round-trip | DIAG-3 |
| L / T-39 step 5 | Report lands with logging off, flag unchanged | DIAG-4 |
| L / T-39 step 6 | The other spellings | DIAG-5 |
| L / T-39 step 7 | No short alias | DIAG-6 |
| L / T-39 step 8 | Report while disabled | DIAG-7 |
| L / T-39 step 9 | Report in combat | COMBAT-4 |
| L / T-39 step 10 | README's Reporting a bug steps | DIAG-8 |
| X / T-40 | Slash write reflects in the open panel | PANEL-20 |
| X / T-41 | Master change grays the visible tab and those behind it | PANEL-19 |
| X / T-42 | Panel write reflects in `/pc get` | PANEL-21 |
| X / T-43 | Value set back to default is auto-cleared from SavedVariables | INSTALL-6 |
| P / T-50 | SavedVariables holds only changes | INSTALL-5 |
| P / T-51 | Format-signature mismatch (stale: a dropped conversion now saves and renders) | SLASH-10 |
| P / T-52 | `/pc test` block format (stale `[PC]`-in-chat half moved to the degraded install) | TEST-1, DEGRADED-6 |
| P / T-52a steps 1–4 | `all` and `category` filters, prefix, General | TEST-4 |
| P / T-52a steps 5, 9, 10 | Unknown category, unknown format string, bad keyword | TEST-6 |
| P / T-52a steps 6–8 | `formatstring` filter | TEST-5 |
| P / T-53 expected 1–3 | `LOOT_ITEM_CREATED_SELF` registered under Tradeskill only | OVR-7 |
| P / T-53 expected 4 | Schema v2 moves a Loot-only override onto Tradeskill | INSTALL-7 |
| P / T-54 | Category off disables per-string Enable and New | PANEL-18 |
| P / T-55 | `/pc reset Bogus` (stale wording) | RESET-7 |
| R / preamble | The shared reset semantic | RESET section preamble |
| R / T-56 | Row Reset restores format and Enable | RESET-2 |
| R / T-57 (1)–(4) | Four reset paths leave `/pc list Loot` at default (step 3 now `/pc reset` of the string's `.enabled` and `.format` paths) | RESET-11 (all four arms); the single-path effects also in RESET-2, RESET-3, RESET-5, RESET-10 |
| R / T-57 reload | SavedVariables Loot entry absent after each of the four | RESET-11 |
| R / T-58 | One `[Set]` line per reset | RESET-12 |
| R / T-59 | Reset reflects live in an open panel (now via paths and resetall) | RESET-13 |
| M / preamble | Media audit; library must be told the folder | DIAG-16, DIAG-17 failure lines |
| M / T-60 | Console mono font and chrome | DIAG-16 |
| M / T-60a | Title-bar marks, no tooltips, the × fallback | DIAG-17 |
| M / T-61 | Header in Blizzard fonts, gold divider, no custom typeface | PANEL-3, PANEL-4 |
| M / T-62 | Landing logo texture renders | PANEL-1 |
| M / T-63 | Chat frame keeps its own font and backdrop | OVR-8 |
| G / T-64 | Minimap button wears the logo, AddOns list art | LAUNCH-1 |
| G / T-65 | Left-click opens settings; right-click Enabled menu | LAUNCH-2, LAUNCH-3 |
| G / T-65 in-combat line | Left-click refused in combat | COMBAT-3 |
| G / T-65a | Status tooltip enabled and disabled | LAUNCH-4 |
| G / T-66 | Minimap button row hides at once, remembers, keeps angle | LAUNCH-5 |
| G / T-67 | Hidden button survives a profile switch and reset all | LAUNCH-6 |
| G / T-68 | `/pc disable` echo and checkbox, live verbs, `/pc test` refused, bare `/pc` opens panel | STATE-1, STATE-2, STATE-3, STATE-4 |
| G / T-68a | Combat watcher unregistered while disabled; re-enable reads current mode | STATE-5, STATE-6 |
| G / T-69 | Broker display shows the same plugin | LAUNCH-7 |
| When to run what (table) | Trigger to groups, each row plus the quick recipe | Before you start ▸ Which checks to run (each row lists the new IDs of its old groups' checks; the routine row's INSTALL-2, TEST-1, OVR-10, PANEL-16 replace the quick recipe) |
| K / T-90 steps 1–2 | No errors, the missing-library line once | DEGRADED-1 |
| K / T-90 step 3 | `/pc list` one line | DEGRADED-2 |
| K / T-90 step 4 | `/pc debug on` ack, window unavailable | DEGRADED-3 |
| K / T-90 step 5 | `/pc config` unavailable | DEGRADED-4 |
| K / T-90 step 6 | `/pc resetall` still works | DEGRADED-5 |
| K / T-90 help/version/test line | Verbs that never needed the library | DEGRADED-6, DEGRADED-7 |
| K / T-90 step 7 | `/pc diagnostics` unavailable line | DEGRADED-8 |
| K / T-90 restore | Rename back | DEGRADED-10 |
| K / T-91 | No raw locale key anywhere | DIAG-19 |
| K / T-92 | Console window edge matches a sibling's | DIAG-18 |
| K / T-93 (1)–(2) | `/pc reset Loot.enabled` resets one row | RESET-5 |
| K / T-93 (3)–(4) | Category name answered with the deprecation, case and prefix | RESET-6 |
| K / T-93 (5) | `/pc reset zzz` not found | RESET-7 |
| K / T-94 | Category reset on header, footer and resetall | RESET-3, RESET-4, RESET-10 |
| K / T-95 unchanged | Breadcrumb, fonts, Defaults inset, scrollbar gutter, editor block | PANEL-3, PANEL-4, PANEL-5, PANEL-14 |
| K / T-95 deliberately different | 50/50 General, landing row spacing, Master controls strip | PANEL-7, PANEL-1 |
| K / T-96 (1) | `/pc config` refused in combat | COMBAT-1 |
| K / T-96 (2) | Sidebar page covered, not closed, one chat line | COMBAT-2 |
| K / T-97 steps 1–3 | Version from the TOC in `/pc version` and help | INSTALL-2 |
| K / T-97 step 4 | Landing tagline from the TOC's Notes | PANEL-1 |
| K / T-98 | Library-absent install still knows its version (stale tagline and console halves removed) | DEGRADED-7 |
| K / T-99 | Tab strip survives pooling and re-dressing | PANEL-9 |
| Reporting a failure (4 steps) | What to capture and where to file | Before you start, closing paragraph |
| T-100 | General Master controls strip and row layout | PANEL-7 |
| T-101 steps 1–2, 5 | Visibility Always and Never | OVR-4 |
| T-101 step 3 | Only in combat, live flips | OVR-5 |
| T-101 step 4 | Only out of combat | OVR-6 |
| T-102 (list) | TreeGroup box, entries, highlight, one editor | PANEL-11 |
| T-102 (fit) | Box fills the page, resize, fresh-login first open | PANEL-12 |
| T-102 (Experience, memory) | Pane scrolls itself; last string remembered; reset on reopen | PANEL-13 |
| T-103 (1) | Test button writes to the console | TEST-2 |
| T-103 (2) | `/pc test` output (stale "to chat"; it writes to the console) | TEST-1 |
| F / SMK-F001 | Chat payload flips with combat state; Loot History records | OVR-9 |
| N / preamble | Locale, why, English output by design | Non-English client preamble |
| N / T-104 steps 1 + record | Snapshot holds the client's strings; record eight originals | LOC-1 |
| N / T-104 steps 2–3 | Disable restores the client's strings, enable re-applies | LOC-2 |
| N / T-105 | One real line per category, no raise, no literal conversion | LOC-3 |
| N / T-106 | Globals this client does not define (stale: a missing original prints `(original not available)`, not empty) | LOC-4 |
| N / T-107 | Nothing else moved | LOC-5 |
| N / sign-off paragraph | No sign-off without a non-English client | Non-English client closing paragraph |
| New | Profiles page | PROFILE-1 |
| New | A new profile starts from defaults; switching back restores | PROFILE-2 |
| New | Enable is per profile | PROFILE-3 |
| New | One debug line per switch, copy, page reset and resetall | PROFILE-4 |
| New | `/pc profile` lists | PROFILE-5 |
| New | `/pc profile <name>` switches, open panel follows, already-current | PROFILE-6 |
| New | Unknown name refused, did-you-mean, nothing created | PROFILE-7 |
| New | Quotes and spaces | PROFILE-8 |
| New | The verb answers while disabled and brings the addon up | PROFILE-9 |
| New | No switch in combat | PROFILE-10 |
| New | `/pc profile` on a library-absent install | DEGRADED-9 |
