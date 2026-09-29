# AbsorbTracker smoke-test coverage map (SP-AT-03)

`docs/smoke-tests.md` went from 580 lines, 168 numbered checks (sections A–V) and about 15,300 words to 282 lines, 150 checks in 13 themes and about 10,500 words. Of the 150, 143 carry old checks and 7 are new for the `profile <name>` verb: PROFILE-3, PROFILE-6 to PROFILE-8 and PROFILE-10 to PROFILE-12. PROFILE-5 carries old G.37 but now drives the verb's bare-name route. No old check was dropped: every old check below maps to at least one new ID, and old checks that repeated the same behavior were merged. A split check lists every new ID it went to.

Old locations cite the pre-rework file at `7508ff0`: section letter, step number, `:line`.

| Old location | Behavior | New ID |
|---|---|---|
| A.1 :12 | Fresh install, zero Lua errors | INSTALL-1 |
| A.2 :13 | Shipped defaults: player bar only, stock media | INSTALL-2 |
| A.3 :14 | `/reload` clean, bar keeps its spot | INSTALL-3 |
| A.4 :15 | Value tracks the absorb | BAR-1 |
| A.5 :16 | Large absorb abbreviates, never nil | BAR-2 |
| A.5a :17 | Secret values in combat with debug on, `[Combat] left` rollup | COMBAT-1 |
| B.6 :20 | Bare `/at` opens the landing page; refused in combat | SLASH-1, COMBAT-2 |
| B.7 :21 | `/absorbtracker` same as `/at` | SLASH-2 |
| B.8 :22 | Help lists all 19 verbs with colors; no `test` row | SLASH-3, SLASH-4 (pending) |
| B.9 :23 | Unknown verb → message then help | SLASH-4 (pending) |
| B.10 :24 | `options` alias | SLASH-5 |
| C.11 :27 | `/at config` opens the tree | PANEL-1 |
| C.11a :28 | About page logo, Notes, command-list colors | PANEL-2 |
| C.12 :29 | `/at config` refused in combat, no queue | COMBAT-2 |
| C.13 :30 | No auto-open after combat | COMBAT-3 |
| C.13a :31 | Sidebar pages covered in combat, one notice | COMBAT-4 (pending) |
| D.14 :34 | General strip and row order; per-bar toggle; Lock frame disables drag; repaint cadence (PANEL-3 corrected: the old step left out the Minimap button row and shortened the `Update throttle (in sec)` label) | PANEL-3 (pending), BAR-4, BAR-11 (pending), BAR-5 |
| D.14c :36 | Enable switch, visibility dropdown, master scale and alpha | STATE-1, BAR-6, BAR-7 |
| D.14d :38 | Visibility migration, active and inactive profile | MIGRATE-5 |
| D.14b :39 | General strip pinned, no stacking, one row | PANEL-4 |
| D.14a :40 | Debug console checkbox follows the window | DIAG-15 |
| D.14e :41 | No Test mode box; unlocked placeholders; box and verbs one switch; combat relock; unlock refused in combat | PANEL-3, BAR-10, BAR-11 (pending), COMBAT-5 (pending), COMBAT-6 (pending) |
| D.15 :42 | Appearance chrome block, strip, tab rows, live edits, font shadow; every LSM list filled (Bar texture, Background Texture, Border style, Font) | LOOK-1, LOOK-5 |
| D.16 :43 | Unit picker keeps the tab | LOOK-2 |
| D.17 :44 | Bar opacity fades the whole bar | LOOK-9 |
| D.17a :45 | Font color, alpha kept under class color | LOOK-10, LOOK-14 |
| D.18 :46 | Profiles page renders in the canvas | PROFILE-1 |
| D.19 :47 | Appearance Defaults: all tabs and units, not throttle, not position | PANEL-6 |
| D.20 :48 | Reset All popup reverts and recenters (corrected: `/at resetall` prints `All settings reset to defaults` with no final period, the button's line has one) | PANEL-7 (pending) |
| D.20a :49 | Reset All tooltip and popup wording; profile list unchanged (corrected: the tooltip reads `Profiles -> Reset Profile`, Options.lua `RESET_ALL_TIP_PROFILES_PAGE`) | PANEL-8 (pending) |
| E.21 :52 | Border dropdown flush, AbsorbTracker alone | LOOK-7 |
| E.22 :53 | Border dropdown hover previews | LOOK-7 |
| F.23 :56 | `/at list` groups and colors | SLASH-6 |
| F.24 :57 | `/at get` | SLASH-7 |
| F.25 :58 | `/at set` writes, repaints, refreshes | SLASH-8 |
| F.26 :59 | `/at set` invalid value | SLASH-10 |
| F.27 :60 | `/at reset <path>`; page form gone | SLASH-11 |
| F.27a :61 | Old paths still resolve, no key moved | MIGRATE-4 |
| F.28 :62 | `/at resetall` same as the popup | PANEL-7 |
| F.29 :63 | `/at resetposition` | BAR-15 |
| F.30 :64 | lock/unlock echo; locked bar refuses the drag, unlocked moves; placeholder survives repaints; position persists | BAR-10, BAR-11 (pending), BAR-14 |
| F.31 :65 | `/at toggle` all and per unit, bad unit | BAR-8 |
| F.32 :66 | `/at update` | BAR-9 |
| F.33 :67 | `/at debug hold` timing, lock ends it, unlocked falls back to placeholder | DIAG-16 (pending) |
| F.34 :68 | `/at debug hold` refusals; `test` verb gone | DIAG-17 (pending), SLASH-4 (pending) |
| G.35 :71 | `/at profile list` / `current` | PROFILE-4 |
| G.36 :72 | `/at profile new` switches to defaults, repaints | PROFILE-9 (pending) |
| G.36a :73 | `/at profile new Default` refused | PROFILE-9 (pending) |
| G.37 :74 | A switch repaints (OnProfileChanged) | PROFILE-5 |
| G.38 :75 | `/at profile copy` repaints | PROFILE-14 (pending) |
| G.38a :76 | copy refusals, no Lua error | PROFILE-14 (pending) |
| G.39 :77 | delete refusals, delete works | PROFILE-15 (pending) |
| G.40 :78 | Profiles-page switch repaints | PROFILE-2 |
| G.40a :79 | Profiles page draws after another addon's page | PROFILE-1 |
| H.41 :82 | Console opens, shared edge, close tints | DIAG-1, DIAG-3 |
| H.41a :83 | Three title-bar marks present; nil-name fallback; icons-folder gap signature | DIAG-2, DEGRADED-3, DEGRADED-4 |
| H.41b :85 | Hover ladders, no tooltip | DIAG-3 |
| H.41c :87 | Nothing else gained a mark (corrected: the perf panel has no JSON Dump row) | DIAG-4 (pending) |
| H.42 :89 | Monospace console font, fallback tell | DIAG-5 |
| H.43 :90 | `/at debug on` ack and `[Init]` | DIAG-6 |
| H.44 :91 | `/at debug off` ack | DIAG-7 |
| H.45 :92 | Header Debug toggle | DIAG-8 |
| H.46 :93 | Copy window | DIAG-9 |
| H.46a :94 | Scrollbar direction and line counter | DIAG-10 |
| H.47 :95 | Clear | DIAG-12 |
| H.48 :96 | Esc closes console and Copy | DIAG-13 |
| H.49 :97 | `/reload` resets console state | DIAG-14 |
| I.50 :100 | Customized values survive reload | MIGRATE-1 |
| I.51 :101 | `schemaVersion = 5`, dead keys swept from every profile | MIGRATE-2 (pending) |
| I.52 :102 | Hand-deleted key restored | MIGRATE-3 |
| J.53 :105 | Bar class color, picker stays live | LOOK-11 |
| J.54 :106 | Background darkened class color | LOOK-11 |
| J.55 :107 | Border class color | LOOK-11 |
| J.55a :108 | Text class color | LOOK-11 |
| J.55b :109 | Target bar takes the target's class | LOOK-12 |
| J.56 :110 | Class colors re-resolve on reload and profile switch | LOOK-13 |
| J.57 :111 | Swatch set under the mode shows after untick | LOOK-14 |
| J.57a :112 | Alpha survives the mode | LOOK-14 |
| K.58 :115 | Target bar needs a target | BAR-4 |
| K.59 :116 | Mirror toggle, hint, live follow | LOOK-15 |
| K.60 :117 | Copy styling from Player is one-shot | LOOK-15 |
| K.60a :118 | Copy logs one `[Set]` line and restyles the bar | DIAG-18 |
| K.60b :119 | Defaults, Reset All, Reset Profile, copy log one line each | DIAG-18 |
| K.61 :120 | Bars drag independently, persist | BAR-14 |
| K.62 :121 | `/at toggle` and visibility govern all three | BAR-8, BAR-6 |
| K.63 :122 | Appearance Defaults covers all units; resetposition covers all bars | PANEL-6, BAR-15 |
| K.64 :123 | Reset position button and verb move every bar | BAR-15 |
| K.65 :124 | Mirror note on get/set | LOOK-16 |
| K.66 :125 | Second pre-v3 profile keeps its layout (saved width, color and position all lifted and used after the switch; MIGRATE-6's hand-made block carries all three) | MIGRATE-6 |
| K.67 :127 | Each bar tracks its own unit | BAR-3 |
| K.68 :128 | Drag strips (a–d); combat relock hides strips (e) (BAR-12 corrected: a bar's width floors at 50 px, `settings/Appearance.lua` min 50, so the old 40 px step was impossible) | BAR-12 (pending), COMBAT-5 |
| K.68b :129 | Strip X hides one bar | BAR-13 |
| K.69 :131 | Disabled bar gets no events | BAR-16 |
| K.70 :132 | Enable flags follow a profile switch (the switch back now goes through `/at profile <name>`) | PROFILE-13 (pending) |
| L.71 :136 | Bare `/at perf` entry point | DIAG-26 |
| L.71a :137 | Usage, unknown sub, no suspend/resume | DIAG-27 |
| L.72 :138 | `start` with logging off (the old "four numbered next steps" was stale: the library prints no step list, the step panel replaced it; see DIAG-37) | DIAG-28 (pending) |
| L.73 :139 | who/where/group context | DIAG-29 |
| L.74 :140 | Armed waits for combat (corrected: the report pads the label, `%-10s (not sampled)`, so the row is not the literal `active: (not sampled)`) | DIAG-30 (pending) |
| L.75 :141 | Recording brackets combat | DIAG-31 |
| L.76 :142 | Experiment B suspends | DIAG-32 |
| L.77 :143 | B records while suspended | DIAG-32 |
| L.78 :144 | Re-arm zeroes | DIAG-33 |
| L.79 :145 | finish restores first, no table (old `RESUMED — bars restored` corrected to the library's `RESUMED — restored` chat line) | DIAG-34 (pending) |
| L.80 :146 | `AbsorbTrackerPerfDB`, 10-run ring | DIAG-36 |
| L.80a :147 | Old-schema ring discarded | DIAG-36 |
| L.81 :148 | Report and JSON Dump into the console (corrected: `dump` merged into `report` in the library, Perf.lua `SUBS.report`; the JSON line starts `{"addon":` since keys are sorted) | DIAG-35 (pending) |
| L.82 :149 | Console copy is plain text | DIAG-9 |
| L.83 :150 | Step panel gates the workflow, shared edge (corrected: six rows, PerfPanel.lua `STEPS`, no JSON Dump row) | DIAG-37 (pending) |
| L.84 :151 | Cancel live only mid-run | DIAG-39 |
| L.84a :152 | Report and Dump repeatable (Report only; see L.81) | DIAG-35 (pending) |
| L.84b :153 | Close mark; closing keeps the run; hide/show/toggle | DIAG-38, DIAG-41 |
| L.85 :154 | Panel and chat same path | DIAG-37 (pending) |
| L.86 :155 | Zero cost when idle | DIAG-42 |
| L.86a :157 | Report shows the observed nesting (`observedWithin`); corrected to read the JSON from Report, written `"observedWithin":"repaintPass"` with no space as `lib.EncodeJSON` writes it | DIAG-43 (pending) |
| M.87 :177 | Help renders, `reset <path>` text | SLASH-3 (pending: the `profile` row's text is new) |
| M.88 :178 | Panel opens, combat refusal, About colors | PANEL-1, COMBAT-2, PANEL-2 |
| M.89 :179 | Console opens, on/off acks | DIAG-5, DIAG-6, DIAG-7, DIAG-10 |
| M.90 :180 | Header toggle, Clear, Copy, Esc, buffer intact | DIAG-8, DIAG-9, DIAG-12, DIAG-13 |
| M.91 :181 | Live edits, same-frame refresh, nothing grays | PANEL-5 |
| M.92 :182 | Unit picker, mirror tick, Copy styling | LOOK-2, LOOK-15 |
| M.93 :183 | List group headers; mirror note | SLASH-6, LOOK-16 |
| M.94 :184 | set clamps; set invalid two-line; reset path; Appearance Defaults intact | SLASH-9, SLASH-10, SLASH-11, PANEL-6 |
| M.95 :186 | Profile round-trip, panel re-syncs | PROFILE-4, PROFILE-5, PROFILE-9, PROFILE-14, PROFILE-15 |
| M.96 :187 | Full perf A/B run | DIAG-26 to DIAG-36 (merged: the same chain step by step) |
| M.97 :188 | Parity capture against the previous bucket figures | DIAG-44 |
| M.98 :189 | `/reload`: debug off, position and profile survive | INSTALL-3, DIAG-14 |
| M.99 :190 | Degraded load: `/at`, MISSING line, host verbs, plain help, list line | DEGRADED-1 (pending: `AT-08`'s session X2.3 never ran), DEGRADED-2 (pending: its `/at profile` step is new) |
| M.100 :192 | Page-wide controls in the chrome band | LOOK-3 |
| M.101 :193 | A raise in the chrome block costs only the block | LOOK-4 |
| M.102 :194 | No raw locale key renders | PANEL-9 |
| N.94 :204 | `/at version` reads the TOC | INSTALL-5 |
| N.95 :208 | About blurb is the TOC Notes | PANEL-2 |
| O.103 :226 | Composed media dropdowns fill and apply | LOOK-5 (pending) |
| O.104 :232 | Late-registered media appears | LOOK-6 (pending) |
| P.105 :257 | Pooled tab strip re-dresses correctly | PANEL-4 (pending) |
| P.106 :264 | Perf strings read US (old expectation of `unlabeled` on the start line and report header was wrong: the library always stamps a `YYYY-MM-DD HH:MM` label, and the cancel line is `perf run CANCELED — nothing saved`; corrected in DIAG-40) | DIAG-40 (pending) |
| Q.107 :299 | Border dropdown identical across five addons and load orders | LOOK-8 (pending) |
| R.108 :331 | `[Migrate]` count includes a hand-made inactive pre-v3 profile (corrected: the sweep runs in `OnInitialize` while `NS.State.debug` is still off, so the `[Migrate]` line never reaches the console; the check now reads the inactive block in the SavedVariables file, and `tests/test_database.lua` pins the count) | MIGRATE-6 (pending) |
| S.109 :358 | Perf panel: one close control, top-right, library mark | DIAG-41 (pending) |
| T.110 :402 | Non-English value text renders and fits | LOC-1 (pending) |
| T.111 :413 | Non-English class colors follow the token | LOC-2 (pending) |
| T.112 :424 | Non-English debug lines survive | LOC-3 (pending) |
| U.1 :449 | AddOns-list logo | INSTALL-4 |
| U.2 :453 | Minimap button present, drag persists | LAUNCH-1 |
| U.3 :457 | Left-click opens settings, tooltip | LAUNCH-2 |
| U.4 :459 | Right-click menu, Locked toggles | LAUNCH-3 |
| U.5 :466 | Menu Locked refused in combat; Enabled; grayed Locked | LAUNCH-4 |
| U.6 :472 | Minimap button row and CLI path | LAUNCH-5 (pending) |
| U.7 :478 | Hidden survives a profile switch | LAUNCH-6 |
| U.8 :480 | Hidden survives Reset All | LAUNCH-7 (pending) |
| U.9 :482 | Hidden survives page Defaults | LAUNCH-8 |
| U.10 :488 | Broker display | LAUNCH-9 |
| U.11 :494 | enable/disable, way back open | STATE-2 |
| U.12 :498 | Disabled refuses feature verbs, keeps repair verbs | STATE-3 (pending) |
| U.13 :504 | Disabled is a full stand-down | STATE-4 |
| U.14 :512 | Disabled addon's button writes nothing | LAUNCH-10 |
| U.15 :518 | Perf hold and disable do not fight | STATE-5 |
| V.1 :529 | Report appends, trace kept, chat line | DIAG-19 |
| V.2 :534 | Sections in order | DIAG-20 |
| V.3 :539 | Ungated, flag untouched | DIAG-21 |
| V.4 :542 | Both forms while disabled | DIAG-22 |
| V.5 :546 | Long prefix forms | DIAG-23 |
| V.6 :548 | No `diag` alias | DIAG-23 |
| V.7 :550 | In combat and in restricted content | DIAG-24 |
| V.8 :553 | Report copy is clean | DIAG-25 |
| V.9 :555 | 3000-line cap | DIAG-11 |
| V.10 :558 | Library absent: diagnostics unavailable line | DEGRADED-2 |

Not checks, folded in:

- The pass criteria at old `:212` (no Lua errors, `[AT]` prefix, no taint warning, the stale "121 checks" count) became the fail rules under "Before you start".
- The sign-off note after old § T (`:433`–`:441`) is now the "No headless stand-in" paragraph in "Non-English client".
- The triage list at old `:562`–`:580` became each theme's **Code** line.
- The section intros for M–S (release and session context, milestone IDs) were dropped. They were history, not checks, and git keeps them.

Pending sign-off in the new file follows the 2026-09-29 clarification of spec S4: old checks with no recorded run, plus every check new in this run or corrected against the code in it. Old and never run: PANEL-4 (P.105, session 3), COMBAT-4 (C.13a; on the unrun 2026-09-07 checklist, no run recorded since the v1.46.1 cover), LOOK-5 and LOOK-6 (O.103–104, session 4), LOOK-8 (Q.107), MIGRATE-6 (R.108 with K.66), DIAG-40 (P.106, session 3), DIAG-41 (S.109), DIAG-43 (L.86a), LOC-1 to LOC-3 (T.110–112). O and P were never stamped NOT YET RUN in the old doc, but the 2026-09-07 checklist (`08_SMOKE_CHECKLIST.md`, "Nothing below has been run") lists them and no later run is recorded. Rewritten on 2026-09-24 by the 2026-09-23 remediation and never run: that plan's `06_SMOKE_TESTS.md` has no `Recorded` line for sessions AT.1, AT.2, AT.6, AT.7, AT.8 or X2.3 (its only records are P.6, MM.12, MM.13, Q.2, X1.3 and X1.4), its `RESUME.md` §5 still lists the in-client sessions as the owner's, and the 2026-09-26 diagnostics run (AT-S1 to AT-S11, AT-X1 to AT-X3) covered only the V-section and drag-strip checks. So these are pending: PROFILE-9, PROFILE-14 and PROFILE-15 (old 36/36a, 38/38a, 39; `AT-03`, session AT.6), BAR-11, COMBAT-5 and COMBAT-6 (old 14e and 30; `AT-04`, session AT.7), MIGRATE-2 (old 51; `AT-06`, session AT.1), DIAG-16, DIAG-17 and SLASH-4 (old 33, 34 and 8/9; `AT-11`, session AT.8), STATE-3 (old U.12, whose refusal list `AT-11` also rewrote), LAUNCH-5 and LAUNCH-7 (old U.6 and U.8; `AT-12`, sessions AT.1 and AT.2) and DEGRADED-1 (old 99; `AT-08`, session X2.3). DEGRADED-2 also carries `AT-09`'s unrun session X2.6. The launcher rewrite in `M6-AT` is not pending: X1.4 records a pass on the M6 builds on 2026-09-25. New with the verb: PROFILE-3, PROFILE-6 to PROFILE-8, PROFILE-10 to PROFILE-12; PROFILE-5 and PROFILE-13 now switch through `/at profile <name>`; SLASH-3 carries the new `profile` help text and DEGRADED-2 the new degraded `/at profile` step. Corrected against the code: PANEL-3, PANEL-7, PANEL-8, BAR-12, COMBAT-6 (the in-combat **Lock frame** untick is dropped: the v1.46 combat cover takes every click on a page on screen), MIGRATE-6, DIAG-4, DIAG-28, DIAG-30, DIAG-34, DIAG-35, DIAG-37, DIAG-40, DIAG-43.

Inbound references updated: `core/MediaSetup.lua` (item `11a` → PANEL-2), `settings/General.lua` (step 20 → PANEL-7), `tests/test_widgets.lua` and `docs/settings-panel.md` (§ C step 13a → COMBAT-4), `docs/debug.md` (section H → the DIAG checks). The citations `ConsumableMaster § 3c` and `KickCD § 9b` are now `ConsumableMaster LOC-1` and `KickCD LOC-1`. `tests/prose_waivers.lua` is deleted, and its row in `docs/module-map.md` with it. It only waived the two British perf-string spellings that old P.106 quoted, and DIAG-40 no longer quotes them.
