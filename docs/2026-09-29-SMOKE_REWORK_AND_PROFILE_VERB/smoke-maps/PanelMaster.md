# PanelMaster smoke-test coverage map (SP-PM-03)

Old `docs/smoke-tests.md`: 1233 lines, 22 numbered sections, 321 numbered steps. New: 925 lines,
14 themes, 223 checks (216 carried from the old steps, 7 new: PROFILE-11 to PROFILE-14, PROFILE-16
and PROFILE-17 for the `/pm profile` verb, and DEGRADED-12 for its library-absent line; PROFILE-15
carries § 7 step 12). Three old items dropped: a note with nothing to check, and two combat checks
that no in-client route reaches (§ 8 step 4b with the combat half of § 9 step 11, and § 12b-2 step
2), each now asserted by a named headless test. Every old numbered step
appears below once; a row covering several steps lists them as a range, and a step split across two
new checks names both. Filled sign-off records (`Result: PASS (owner, 2026-09-26)` on § 9 steps 5-w
and 16) are dropped per D4; the checks stay.

| Old location | Behavior | New ID |
|---|---|---|
| Intro (lines 15-16) | Start from `/reload` + `/pm resetall` (a profile reset) | Before you start |
| § 1 step 1 | Login: no Lua error, nothing drawn | INSTALL-1 |
| § 1 step 2 | Bare `/pm` opens the landing page silently; `/pm help` index format | SLASH-1, SLASH-2 |
| § 1 step 3 | `/pm version` matches the TOC | INSTALL-2 |
| § 1 step 4 | `/pm panels` empty state | INSTALL-3 |
| § 2 step 1 | `/pm test` is not a verb; no Test mode row | SLASH-4 |
| § 2 step 2 | Old test-mode samples swept on upgrade | INSTALL-7 (its `[Preview] swept …` line was unreachable: the sweep runs at load, core/Database.lua:21, and logging is session-only and off at load, core/State.lua:10; the check now reads `/pm panels`) |
| § 3 step 1 | `/pm new` confirmation | FRAME-1 |
| § 3 steps 2-3 | Unlock shows outline and name; drag | FRAME-2 |
| § 3 steps 4-5 | Lock hides overlay; locked panel is click-through | FRAME-3 |
| § 3 step 6 | Position persists; unlock is session-only | FRAME-5 |
| § 4 steps 1-5 | Snap to grid on and off | FRAME-6 |
| § 4b steps 1-2 | Outline thickness default 2 px; live change while unlocked | FRAME-7 |
| § 4b steps 3-4 | Outline 0/400 bounded; hand-edited 0 drawn at 1 | FRAME-8 (step 3 rewritten: the CLI clamps since the LibKa0s adoption rather than refusing; see tests/test_slash.lua "Slash.CliSet: an out-of-range number CLAMPS to the row's max (LIBKA0S-17)") |
| § 4b step 5 | Reset outline thickness | FRAME-7 |
| § 4b steps 6-9 | Default width and height; new and reset panels use them | FRAME-9 (step 8's `/pm panel Wide reset` was never a command: `Sl:CliPanel` special-cases only `fitart` and `deleteall`, and `reset` is not a panel field, so it printed `unknown field 'reset'`. The reset half now uses the **Reset** button on the Panels page's General tab, as FRAME-28 does) |
| § 5 step 1 | `bgColor` float form | LOOK-1 |
| § 5 step 1a | `bgColor` byte form with fractional alpha (M4-18, not run) | LOOK-2 (Pending sign-off) |
| § 5 steps 2-3 | Border size and color; corners clean; size 0 | LOOK-3 |
| § 5 step 4 | Alpha clamps to 1.00 | LOOK-4 |
| § 5 step 5 | Strata HIGH / BACKGROUND | LOOK-5 |
| § 5b step 0 | Ka0s shared media registered with LSM | LOOK-6 (PanelMaster has no font dropdown, so `JetBrains Mono` is checked with an LSM `IsValid` dump; run with PanelMaster the only Ka0s addon, since LSM is shared) |
| § 5b steps 1-3 | Background texture list, pick, dropdown keeps value | LOOK-7 |
| § 5b step 4 | Border style Blizzard Tooltip | LOOK-8 |
| § 5b step 5 | Border dropdown flush, PanelMaster alone | LOOK-9 |
| § 5b steps 6-7 | Border thickness scales; style None keeps thickness | LOOK-8 |
| § 5b step 8 | Background texture None | LOOK-11 |
| § 5b step 9 | Textures persist across reload | LOOK-12 (one persistence check) |
| § 5b step 10 | Texture from a disabled addon renders plain | LOOK-13 |
| § 5b-2 steps 1-4 | Color pickers apply without the opacity slider; live; border picker | LOOK-14 |
| § 5b-2 step 5 | Picker Cancel restores | LOOK-15 |
| § 5b-2 step 6 | Colors persist across reload | LOOK-12 |
| § 5b-2 step 7 | Picker alpha multiplies Panel opacity | LOOK-16 |
| § 5b-3 steps 1-5 | Border offset halo, inset, zero, drag, strata | LOOK-17 |
| § 5b-3 step 6 | Offset persists | LOOK-12 |
| § 5b-4 steps 1, 1b | Accent bar shipped look; panel border starts at 0 | ACCENT-1 |
| § 5b-4 step 2 | Enable accent bar toggle | ACCENT-2 |
| § 5b-4 step 2b | Bar draws over the border | ACCENT-3 |
| § 5b-4 steps 3-4 | Edges; unticking all keeps enable on | ACCENT-4 |
| § 5b-4 step 5 | Bars track resize | ACCENT-5 |
| § 5b-4 steps 6-7 | Bar thickness and offset | ACCENT-6 |
| § 5b-4 step 8 | Bar color and class color | ACCENT-7 |
| § 5b-4 step 9 | Bar texture from status-bar list | ACCENT-8 |
| § 5b-4 step 9b | The bar's own border | ACCENT-9 |
| § 5b-4 step 9c | Bar opacity | ACCENT-10 |
| § 5b-4 steps 10-11 | Bars fade and change strata with the panel | ACCENT-11 |
| § 5b-4 step 12 | Bars are click-through | ACCENT-12 |
| § 5b-4 step 13 | Bars follow mouseover fade | ACCENT-11 |
| § 5b-4 step 14 | Deleting leaves no floating bars | ACCENT-13 |
| § 5b-4 step 15 | Accent settings persist | LOOK-12 |
| § 5b-4 step 16 | `accentEdges` CLI | ACCENT-14 |
| § 5c steps 1-2 | Class color on background; picker enabled; tooltip; opacity kept | LOOK-18 |
| § 5c steps 3-4 | Per-control class color; untick restores originals | LOOK-19 |
| § 5c step 4b | Picker opacity usable under class color, five swatches | LOOK-20 |
| § 5c step 4d | Composed blocks (#48) | LOOK-21 |
| § 5c step 4c | Border definition vs contrast | LOOK-22 |
| § 5c step 5 | Another class's color | LOOK-23 |
| § 5d steps 1-3 | Mouseover fade out and in | LOOK-24 |
| § 5d step 4 | Faded-in panel stays click-through | LOOK-25 |
| § 5d steps 5-6 | Faded opacity 0.3; clamp above opacity | LOOK-26 |
| § 5d step 7 | Unlock holds fully visible | LOOK-27 |
| § 5d step 8 | Many mouseover panels, no frame-rate cost | LOOK-28 |
| § 5d step 9 | Ticker returns after the last fader is off (M4-22, not run) | LOOK-29 (Pending sign-off) |
| § 5e steps 1-4 | Every catalog piece draws | ART-1 |
| § 5e-2 steps 1-2 | Fill types under width and height resize | ART-2 |
| § 5e-2 step 3 | Rotation 90 keeps proportions | ART-3 |
| § 5e-3 steps 1-4 | Draw layers | ART-4 |
| § 5e-3 step 5 | Clipping; accent bar unclipped | ART-5 |
| § 5e-3 step 6 | Blend mode Glow / Normal | ART-6 |
| § 5e-4 step 1 | Artwork color, class color, opacity | ART-7 |
| § 5e-4 step 2 | Color controls present for every piece | ART-8 |
| § 5e-4 step 3 | Desaturate | ART-9 |
| § 5e-5 steps 1-2 | Unlock overlay above the fill | FRAME-11 |
| § 5e-5 step 3 | Level stride (corrected: set with `/pm panel <name> level`, no editor control) | FRAME-12 |
| § 5e-6 steps 1-3 | Custom path, nonsense, cleared | ART-10 |
| § 5e-6 step 4 | Artwork persists across reload | ART-11 |
| § 5e-6 step 5 | Copy settings carries artwork | FRAME-26 |
| § 5e-6 step 6 | Artwork intact across a profile switch | PROFILE-4 |
| § 5e-6 step 7 | `art*` fields print; `artFill` refusal | ART-12 (the old `/pm panel set <name> artFill SQUISH` read `set` as the panel name and printed `no panel called 'set'`; corrected to `/pm panel <name> artFill SQUISH`, which reaches the enum refusal) |
| § 6 steps 1-2 | Locked panel behind action bars never takes input | FRAME-4 |
| § 6 step 3 | Unchanged in combat | COMBAT-1 |
| § 7 steps 1-3 | Per-panel `enabled false`; shown while unlocked | FRAME-10 |
| § 7 steps 4-5 | `settings.enabled` and `/pm disable` are one switch | STATE-1 |
| § 7 step 6 | `/pm`, help, version answer while disabled | STATE-3 |
| § 7 step 7 | Checkbox and verbs agree | STATE-2 |
| § 7 step 8 | Feature verbs refused with the collection line and inert | STATE-4 |
| § 7 step 9 | Live verbs answer while disabled | STATE-3 (`/pm profile` while disabled is asserted once, in PROFILE-15; the disabled line sits under the help header, as the library's PrintHelp emits it) |
| § 7 step 10 | Typo while disabled is an unknown command | STATE-5 |
| § 7 step 11 | Stand-down is total | STATE-6 (the profile switches go through the Profiles page between two disabled profiles: `/pm profile` prints `Switched to profile '<name>'.`, and switching to PROFILE-15's enabled profile brings the panels up) |
| § 7 step 12 | Profile route out of the disabled state | PROFILE-15 (now also by `/pm profile`) |
| § 7 step 13 | Unlock does not beat the stand-down | STATE-7 |
| § 7b steps 1-2 | Logo on minimap and in the AddOns list | LAUNCH-1 |
| § 7b step 3 | Left-click opens settings | LAUNCH-2 |
| § 7b step 4 | Right-click menu, Locked | LAUNCH-3 |
| § 7b step 4b | Right-click menu, Enabled | LAUNCH-4 |
| § 7b step 4c | Status tooltip | LAUNCH-5 |
| § 7b step 5 | Button angle persists | LAUNCH-6 |
| § 7b step 6 | Button survives a profile switch | LAUNCH-7 |
| § 7b step 6b | Hidden button survives both resets | LAUNCH-8 |
| § 7b step 7 | Minimap button checkbox | LAUNCH-9 |
| § 7b step 8 | No hide entry in the menu | LAUNCH-10 |
| § 7b step 8b | `global.minimap.shown` CLI path | LAUNCH-11 |
| § 7b step 9 | Broker row | LAUNCH-12 |
| § 8 steps 1-3 | Unlock queued in combat, fires after | COMBAT-2 |
| § 8 step 4 | Lock clears the queue | COMBAT-3 |
| § 8 step 4b | Per-panel Unlock in combat unticks itself | dropped: not reachable in the client. The Panels page is built through `O.CreatePanel` (settings/Panel.lua:438), which gives it the combat cover (COMBAT-5), so the **Unlock** tick cannot be clicked in combat, and no other route queues a per-panel unlock. The expectation is asserted by tests/test_panels_page.lua "Panels page: the per-panel Unlock tick tracks global, per-panel and deferred unlocks" (part b), tests/test_media.lua "Unlock: a per-panel unlock during combat is deferred" and "Unlock: a deferred per-panel unlock is replayed when combat ends" |
| § 8 steps 5-6 | `/pm config` refused in combat; no auto-open | COMBAT-4 |
| § 8 step 7 | Open settings covered in combat | COMBAT-5 |
| § 8 steps 8-9 | General visibility in and out of combat | COMBAT-6 |
| § 9 step 1 | Landing list matches `/pm help` | SLASH-3 |
| § 9 step 2 | General tab strip and Defaults style | PANEL-1 |
| § 9 step 2b | Each tab's contents (corrected: Master controls has 7 rows) | PANEL-2 |
| § 9 step 2c | Master controls canonical order (corrected: Minimap button alone on a fourth line) | PANEL-3 |
| § 9 step 2d | General visibility; Master scale and alpha; Reset position; Reset all tooltip; Reset all popup | COMBAT-6, FRAME-13, FRAME-14, PANEL-7, PANEL-8 |
| § 9 step 3 | Scrollbar present, grayed | PANEL-5 |
| § 9 step 4 | Lock frame checkbox | PANEL-6 |
| § 9 step 5 | Panels page band, one row | PANEL-10 |
| § 9 step 5-w | Panels opened first: half-width controls (PASS 2026-09-26, record dropped) | PANEL-11 |
| § 9 step 5-x | Panels opened after another addon (PASS 2026-09-26 in the navrail adoption's report) | PANEL-12 |
| § 9 step 5a | Empty state | PANEL-13 |
| § 9 step 5b | Editor layout | PANEL-14 |
| § 9 step 5b-2 | Open dropdown closes on scroll | PANEL-15 |
| § 9 step 5c | The General tab's six acts (session 3, not run) | PANEL-16 (Pending sign-off) |
| § 9 step 5c-2 | Rename box keeps uncommitted text (session 3, not run) | PANEL-17 (Pending sign-off) |
| § 9 step 5d | Rename keeps frame name; taken name refused; slug-alike allowed | FRAME-21, FRAME-22 |
| § 9 step 5e | Reset one panel | FRAME-28 |
| § 9 steps 6-7 | Create box: focus loss creates nothing; Enter creates | PANEL-18 |
| § 9 step 7b | Duplicate name keeps the text | PANEL-19 |
| § 9 step 8 | One editor at a time | PANEL-20 |
| § 9 step 9 | `(disabled)` suffix | PANEL-21 |
| § 9 step 10 | Controls apply on release | PANEL-22 |
| § 9 step 11 | Per-panel Unlock; Lock frame sync; combat queue | PANEL-23; the combat-queue half dropped with § 8 step 4b (same reason, same covering tests) |
| § 9 step 12 | Panel name tooltip shows the frame name | FRAME-18 |
| § 9 step 13 | Delete falls back to another panel | PANEL-24 |
| § 9 step 14 | Panels Defaults confirms first | FRAME-29 |
| § 9 step 15 | General Defaults is the profile reset | PANEL-8 (its "stale tooltip" remark is gone: the tooltip now says the panels go with it, PANEL-9) |
| § 9 step 16 | Picker rebuilt on show (PASS 2026-09-26, record dropped) | PANEL-25 |
| § 10 steps 1-3 | `/pm recover` | FRAME-15 |
| § 10 step 4 | No recovery at login | FRAME-16 |
| § 10 steps 5-6 | Recovery in scaled units | FRAME-17 |
| § 11 step 1 | Console opens | DIAG-1 |
| § 11 step 1b | Title-bar icon controls, no words | DIAG-2 |
| § 11 step 1c | Monospace columns | DIAG-3 |
| § 11 step 2 | `debug on` ack and `[Init]` line | DIAG-4 |
| § 11 steps 3-4 | One `[Panel]` / `[Set]` line per act | DIAG-5 |
| § 11 step 4a | Bulk acts log one `[Set]` line | DIAG-6 |
| § 11 step 5 | Scrollbar and wheel | DIAG-7 |
| § 11 step 6 | Copy window | DIAG-8 |
| § 11 step 7 | Clear | DIAG-9 |
| § 11 step 8 | Debug toggle button | DIAG-10 |
| § 11 step 9 | Diagnostics report | DIAG-13 |
| § 11 step 10 | Esc closes the console | DIAG-11 |
| § 11 step 11 | Logging is session-only | DIAG-12 |
| § 11 step 12 | Report keeps the trace | DIAG-14 |
| § 11 step 13 | Report ignores the logging flag | DIAG-15 |
| § 11 step 14 | Report while disabled, both forms | DIAG-16 |
| § 11 step 15 | Report in combat | DIAG-17 |
| § 11 step 16 | No aliases for the report | DIAG-18 |
| § 11 step 17 | 3000-line cap | DIAG-19 |
| § 11b steps 1-2 | Frame name exists and resolves | FRAME-18 |
| § 11b step 3 | Anchored frame follows | FRAME-19 |
| § 11b step 4 | Slug collision refused | FRAME-20 |
| § 11b step 5 | Rename keeps the frame name and anchors | FRAME-21 |
| § 11b step 6 | Renames abandon no frames | FRAME-23 |
| § 11b step 7 | Freed name still claimed | FRAME-24 |
| § 11b step 8 | Frame name persisted | FRAME-25 |
| § 12 steps 1-3 | Shared Default profile across characters | PROFILE-1 |
| § 12b step 1 | Profiles page contents, no Defaults | PROFILE-2 |
| § 12b step 2 | New profile clears the screen | PROFILE-3 |
| § 12b step 3 | Switch back restores panels | PROFILE-4 |
| § 12b step 4 | Copy From | PROFILE-5 |
| § 12b step 5 | Reset Profile | PROFILE-6 |
| § 12b step 6 | Profile persists across reload | PROFILE-7 |
| § 12b step 7 | Panels page follows a switch | PROFILE-8 |
| § 12b-2 step 1 | Per-panel unlock dropped on switch | PROFILE-9 |
| § 12b-2 step 2 | Queued per-panel unlock dropped, global kept | dropped: not reachable in the client. Queuing a per-panel unlock needs the Panels page in combat and switching needs the Profiles page or `/pm profile` in combat; the pages are under the combat cover (COMBAT-5) and the verb refuses in combat (PROFILE-16). Now asserted by the new tests/test_profiles.lua "Database: a profile switch drops a queued per-panel unlock but keeps a queued global one" (added in SP-PM-03R; it fails when modules/Registry.lua's `U:ForgetPending` call is removed) |
| § 12b-2 step 3 | Swapped names, no orphans | PROFILE-10 |
| § 12c steps 1-6 | Copy settings: appearance and size, no move, snapshot | FRAME-26 |
| § 12c step 7 | Copy disabled with a lone panel | FRAME-27 |
| § 13 step 1 | Standalone | INSTALL-5 |
| § 13 step 2 | Skinned Defaults button | INSTALL-6 |
| § 14 steps 1-4 | Degraded: no errors, panels drawn (setup moved to the theme intro) | DEGRADED-1 |
| § 14 step 5 | `/pm panels` complete | DEGRADED-2 |
| § 14 step 6 | Panel verbs work | DEGRADED-2, DEGRADED-9 (its "`/pm unlock`, drag, `/pm lock` all work" was stale and contradicted step 11d; tests/test_libka0s.lua "Degraded install: /pm unlock and /pm lock print the library-absent line and change nothing") |
| § 14 step 7 | Library-absent notice once | DEGRADED-3 |
| § 14 steps 8-9 | Console unavailable once; `debug on` still acks | DEGRADED-4 (the degraded ack is `debug logging is on`, core/DebugLogSetup.lua:66, not the library's green `ON`) |
| § 14 step 9b | Ka0s media absent, panels plain; the names return on restore | DEGRADED-5, DEGRADED-14 (a degraded install has no settings panel and PanelMaster has no font dropdown, so the names are checked with LSM `IsValid` dumps and the panel's stored `accentTexture`) |
| § 14 step 10 | Diagnostics unavailable, both forms | DEGRADED-6 |
| § 14 steps 11, 11b | Settings CLI unavailable; plain help rows | DEGRADED-7 |
| § 14 step 11c | Disable/enable work with echo | DEGRADED-8 |
| § 14 step 11d | Unlock/lock unavailable | DEGRADED-9 |
| § 14 step 12 | `/pm resetall` still works | DEGRADED-10 |
| § 14 steps 13, 13b | `/pm config` answers every time; bare `/pm` | DEGRADED-11 |
| § 14 step 14 | One cause clause across the four library-absent lines (steps 7, 8, 11, 13) and across addons | DEGRADED-13 (compares DEGRADED-3, 4, 7, 11) |
| § 14 step 15 | Restore the folder | DEGRADED-14 |
| § 15 steps 1-3 | No raw string keys (the `L` trap) on settings, console, chat | INSTALL-4 |
| § 16 step 1 | Console wears the Ka0s window edge | DIAG-1 |
| § 16 step 2 | Close control is the library's, red on hover | DIAG-2 (its "`Copy` and `Clear` sit to its left" was stale: § 11 step 1b's icon marks replaced the words) |
| § 16 step 3 | `/pm help` indent and header | SLASH-2 |
| § 16 step 4 | Landing list format matches help | SLASH-3 |
| § 16 step 5 | `set` clamps out-of-range numbers | SLASH-5 |
| § 16 step 6 | Bad value gives two lines | SLASH-6 |
| § 16 step 7 | Combat refusal wording, lighter gray | COMBAT-4 |
| § 16 step 8 | Defaults buttons have tooltips | PANEL-9 |
| § 16 step 9 | Esc-closing the console unticks the checkbox | DIAG-11 |
| § 16 step 10 | General page chrome unchanged | PANEL-4 |
| § 16 step 11 | Recover panels under Editing; Editing line pairing (corrected: Grid size pairs with Unlock outline thickness, not Snap to grid) | PANEL-2 |
| § 16 step 12 | Panels band and one-tab editor | PANEL-10 (its "six panel-wide acts in the band" was stale: they are on the General tab, PANEL-16) |
| § 16 step 13 | Scrollbar always visible | PANEL-5 |
| § 16 step 14 | Default frame strata dropdown closes on scroll | PANEL-15 |
| § 16 step 15 | `/pm list` format | SLASH-7 |
| § 17 steps 1-4 | `deleteall` and Panels Defaults confirm first | FRAME-29 |
| § 17 step 5 | `/pm resetall` popup wording and result | PANEL-8 (its "Config → Panels → Defaults shows the same popup" was wrong: the Panels page's Defaults is the delete-all, settings/Panel.lua:441, checked by FRAME-29. PANEL-8 names the General page's Defaults instead) |
| § 18 step 1 | No Sunn installed, no entries | ART-13 |
| § 18 step 2 | One entry per theme | ART-14 |
| § 18 step 3 | Composite draws edge to edge | ART-15 |
| § 18 step 5 | Seams (the old section had no step 4) | ART-16 |
| § 18 step 6 | Fit to artwork | ART-17 |
| § 18 step 7 | Fit follows rotation and scale | ART-18 |
| § 18 step 8 | Crop drops whole sections | ART-19 |
| § 18 step 9 | Rotated sections stack | ART-20 |
| § 18 step 10 | Flip | ART-21 |
| § 18 step 11 | Tile repeats the bar | ART-22 |
| § 18 step 12 | Even tint | ART-23 |
| § 18 step 13 | Back to a single piece | ART-24 |
| § 18 step 14 | Transparent strip trimmed | ART-25 |
| § 18 step 15 | Pack disabled | ART-26 |
| § 18 step 16 | SunnArt disabled, manifest lists packs | ART-27 |
| § 18 step 17 | 512x512 themes fit 1536 x 512 | ART-28 |
| § 18 step 18 | Live rename wins | ART-29 |
| § 18 step 19 | Only installed packs listed | ART-30 |
| § 19 steps 1-4 | Tab strip survives pooling (session 3, M4-01, not run) | PANEL-26 (Pending sign-off) |
| § 19 closing note | Perf minor 8 respells five strings | dropped: not a check; `LibKa0s-Perf-1.0` is not wired in this addon, so there is no surface |
| § 20 steps 1-3 and Expect | Border dropdown flush with five Ka0s addons, any load order (session 5, M4-05, not run) | LOOK-10 (Pending sign-off; the "re-run after each of the other addons' deletions" schedule is history) |
| § 21 steps 1-5, Expect, Fail | `[Init]` line reports the packaged version (session 3, M4-19, not run) | INSTALL-8 (Pending sign-off; step 3's "in chat and in the console" is now the console only: DebugLog's SetEnabled writes `[Init]` through `D:Add`, never to chat) |
| § 22 step 1 | Panel named in the client's language | LOC-1 (Pending sign-off; **Panel name** is on the General tab, settings/PanelEditorTabs.lua:304-313, not in the band) |
| § 22 step 2 | Two names, one slug | LOC-2 (Pending sign-off) |
| § 22 step 3 | Name lookup folds only ASCII | LOC-3 (Pending sign-off; the comparison is `/pm panel wide` resolving `Wide`, because `/pm panel chat bg` reads only `chat` and prints `no panel called 'chat'`; the second-`übersicht` half now names both refusals, since the frame-name check refuses it even when the name guard does not fold) |
| § 22 step 4 | Sort order | LOC-4 (Pending sign-off) |
| § 22 step 5 | Round trip across reload and profile switch | LOC-5 (Pending sign-off) |
| § 22 sign-off paragraph | Provoking on an English client is not the same test | Non-English client intro |

New checks with no old origin: PROFILE-11 (list), PROFILE-12 (switch, already current), PROFILE-13
(unknown name refused, did-you-mean, nothing created), PROFILE-14 (quotes and spaces), PROFILE-16
(combat refusal), PROFILE-17 (open General page refreshes), DEGRADED-12 (`/pm profile`
library-absent line).

Inbound references: no live file outside `docs/smoke-tests.md` cited the old numbering. The internal
cross-references (§ 5b-2, § 5b step 10, section 20, § 11 step 2, § 11b, § 12) now cite new IDs, the
`ConsumableMaster § 3c` / `KickCD § 9b` citations became `LOC-1`, and the prose pointer in
`tests/test_libka0s.lua:158` ("the headless half of the smoke test") now names DIAG-2.

Pending sign-off in the new file (clarified policy, 2026-09-29): nine carried-over checks have a
recorded pass (owner, 2026-09-26) and an unchanged expectation, so they are not listed. Two passed in
the old doc itself: § 9 step 5-w and § 9 step 16, now PANEL-11 and PANEL-25. One passed in the
2026-09-26 navrail adoption (`2026-09-26-NAVRAIL_ADOPTION/99_REPORT.md`, "Owner results and finalize
(2026-09-26)": "the PanelMaster Panels band fix (5-w, 5-x)"): § 9 step 5-x, now PANEL-12. Step 5-x
was written in `3a7ac19` (pm-band-fix-01) before that pass and PANEL-12 keeps its expectation; the
in-repo record `73d9b8b` filled only 5-w and step 16. Six passed in the
2026-09-25 diagnostics plan (`2026-09-25-DIAGNOSTICS_COMMAND/99_REPORT.md`, PanelMaster table): PM-S1
(§ 11 step 14, now DIAG-16), PM-S2 with PM-S4 (§ 11 step 12, now DIAG-14), PM-S5 (§ 11 step 13, now
DIAG-15), PM-S3 (§ 11 step 15, now DIAG-17), PM-S7 (§ 11 step 17, now DIAG-19) and PM-X1 (§ 14 step
10, now DEGRADED-6). The old § 11 steps 12-17 carry those plan ids (S1-S8) in their titles. DIAG-13
and DIAG-18 stay listed in their own "partly run" row: PM-S2 did not assert the section order,
`frame=yes` or `0 orphaned` (§ 11 step 9), and PM-S8 ran `/pm debug dump` and `/pm diag` but not
`/pm debug diag` (§ 11 step 16). The other 214 checks are listed: grouped by theme as "no result
recorded", with separate rows for the old NOT YET RUN items (INSTALL-8, LOOK-2, LOOK-10, LOOK-29,
PANEL-16, PANEL-17, PANEL-26, LOC-1 to LOC-5), the seven new checks, and every check whose
expectation this rework corrected against the code (INSTALL-7, INSTALL-8, SLASH-2, FRAME-8, FRAME-9,
FRAME-12, LOOK-6, ART-12, PANEL-2, PANEL-3, PANEL-8, PANEL-10, PROFILE-15, STATE-3, STATE-6, DIAG-2, DEGRADED-2, DEGRADED-4,
DEGRADED-5, DEGRADED-9, DEGRADED-13, DEGRADED-14, LOC-1, LOC-3). The 2026-09-22 sweep's "all 20
passed" names no step of this doc, so it counts as no recorded pass here.
