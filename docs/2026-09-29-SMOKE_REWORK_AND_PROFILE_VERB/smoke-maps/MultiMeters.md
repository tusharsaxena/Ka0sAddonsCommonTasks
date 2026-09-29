# Smoke-test coverage map — MultiMeters (SP-MM-03)

Old `docs/smoke-tests.md`: 2285 lines, 442 checks (counted per Pass bullet, numbered step with its own expectation, table row and standalone check paragraph). New suite: 1372 lines, 337 checks in 14 themes (INSTALL, SLASH, PANEL, PROFILE, STATE, WIN, VIS, GRID, TIP, EXPORT, COMBAT, DIAG, DEGRADED, LOC). 1 old check dropped whole, and two clauses of the old CSV file checks dropped to named headless tests (the `enemy_damage_taken` and CRLF clauses, §26 file rows below); 14 new checks added (PROFILE-10 to PROFILE-17 and DEGRADED-8 for the `/mm profile` verb; COMBAT-30, cell borders mid-pull, which `modules/Row_Border.lua` already claimed the suite checked; INSTALL-9, PANEL-45, PANEL-46 and DIAG-31 for checks the 2026-09-23 plan owes that the old doc never carried, see "Owed checks from the 2026-09-23 plan" below). Pending sign-off (clarified policy, 2026-09-29) lists the old checks the old doc marked never run, unconfirmed or with an empty Result, plus every check new in this rewrite and every check whose steps or expectation were corrected against the code (each correction is noted on its row below). Line numbers are the old file at `feat/2026-09-29-smoke-and-profile` before SP-MM-03.

| Old location | Behavior | New ID |
|---|---|---|
| Conventions :30-33 | Chat banner: one cyan [MM], no doubled banner, no green trailing-colon line | SLASH-1 |
| §1 :94-97, :162 | Fresh install: login with no Lua error | INSTALL-1 |
| §1 :163-164 | Exactly one window, "Multi Meters #1", centered | INSTALL-1 |
| §1 :165-166 | Six default columns in order | INSTALL-1 |
| §1 :167-168 | Shown solo in the open world on a fresh profile | VIS-1 |
| §1 :169 | /mm help index; banner on every row; yellow verbs | SLASH-1 |
| §1 :170-171 | Bare /mm (and /mm plus spaces) opens the landing page, prints nothing | SLASH-2 |
| §1 :172-173 | Settings tree reads General · Windows · Profiles | PANEL-1 |
| §1 :174-176 | No schema error lines | INSTALL-2 |
| §1 :177-179 | SavedVariables shape after /reload | INSTALL-3 |
| §1 header controls :104-107 | Seven controls right to left, own art; letters mean art and atlas failed | WIN-1 |
| §1 header controls :108-110 | The close button is the collection's art | WIN-1 |
| §1 header controls :111-113 | Icons inset at 72% of Control size | WIN-2 |
| §1 header controls :114-116 | Hiding a control closes the gap | WIN-3 |
| §1 header controls :117-118 | Title never runs under a control | WIN-4 |
| §1 header controls :119-124 | Strip centered on the shared title line | WIN-5 (corrected: the controls are Header → Title bar → Header height, Header → Title text → Font size and Header → Button style → Control size) |
| §1 header controls :125-130 | Exactly one control reveals, locked windows too | WIN-6 |
| §1 header controls :131-133 | Control color and hover color follow at once | WIN-7 |
| §1 header controls :134-140 | Each color has its own mode dropdown | WIN-8 |
| §1 header controls :141-142 | Reveal off keeps full alpha, hover color still marks | WIN-9 |
| §1 header controls :143-145 | Minimize collapses to the title bar | WIN-13 |
| §1 header controls :146-147 | A collapsed window stops updating in a pull | WIN-14 |
| §1 header controls :148-149 | Expand restores exact height; collapsed survives /reload | WIN-15 |
| §1 header controls :150-156 | Reset asks first, warns, cancel intact, dialog centered | WIN-16 (corrected: the dialog asks *Clear every recorded combat session?* with Yes / No; the meter-data warning is on the Show reset row's tooltip, not in the dialog) |
| §1 header controls :157-159 | Segment control is the only route to the selector | GRID-25 |
| §2 :183-186 | /reload keeps position, size, color, visibility, nextWindowId | INSTALL-4 (the "column width" step became "column set": per-column width no longer exists; also holds the drag and resize persistence of §3 :253-257) |
| §2 :188-191 | /reload during a restricted pull comes back clean | COMBAT-10 |
| §2 SM-06 :193-203 | Meter data and roster survive a full logout | INSTALL-5 |
| §3 SM-01 :217, :222-224 | Unticking Test mode while disabled brings no window back | STATE-3 |
| §3 SM-02 :218, :225-226 | /mm toggle refused during a capture's suspended arm | STATE-5 (corrected: the suspended arm is `/mm perf measure b`; `start` alone suspends nothing) |
| §3 SM-03 :219, :227-229 | A window made while disabled comes up live | STATE-4 |
| §3 :230-235 | Lock and Test mode are independent | STATE-6 |
| §3 :236-240 | Lock frame is every window's own lock | STATE-7 |
| §3 :241-242 | Test mode box follows the verb | STATE-8 |
| §3 :243-247 | Combat ends Test mode | STATE-10 |
| §3 :248-249 | Starting Test mode in combat is refused | STATE-11 (corrected: the panel box is under the combat cover, so only `/mm test` and the minimap menu are routes) |
| §3 :250-252 | Placeholder rows are deterministic | STATE-9 |
| §3 :253 | Dragging moves the window; position persists | WIN-25 (merged with §3 :258-259; WIN-23 retired, its number not reused; corrected: the drag is by the title bar; the persistence clause merged into INSTALL-4) |
| §3 :254-257 | Resize grip only while unlocked; no grip setting | WIN-24 (the resize-persists clause merged into INSTALL-4) |
| §3 :258-259 | Locked hands the mouse to cells; unlocked drags | WIN-25 (corrected against `modules/Window_Placement.lua` `ApplyLock` and `modules/Row.lua` `ApplyMouse`: the lock only stops the title-bar drag, and the cells answer the mouse locked or unlocked; Pending sign-off) |
| §3 :260 | /mm reset-positions re-centers and counts | WIN-26 |
| §4 :264-266, :283 | Page sweep: every change applies immediately | PANEL-7 |
| §4 :269-275 | Band switches windows; active tab survives | PANEL-5 |
| §4 :276-282 | First show sizes and skins everything, band and strip included | PANEL-6 |
| §4 :284-285 | Tooltip's General tab holds scale; Targets rows | PANEL-13 (names each Tooltip tab's rows: General holds Tooltip scale, Contents holds Show targets / Maximum targets; tab names and order corrected to General, Bar, Bar background, Bar border, Text, Contents) |
| §4 :285-289 | Tooltip anchors are a 3×3 around the cell; no At cursor; Top default | TIP-23 |
| §4 :289-294 | Tooltip placement mid-pull: no taint error, pcall fallback | COMBAT-21 |
| §4 :294-298 | Target line icons, class-colored name, text color reaches spell name, fill and backdrop colors | TIP-24 |
| §4 :298-299 | Tooltip bar border draws | TIP-28 |
| §4 :300-315 | Five text controls on four surfaces; per-statistic per surface | PANEL-20 (stale: Header → Title text offers Class / Custom only, so its title-bar Per-statistic clause is gone) |
| §4 :316-339 | Media pickers list late-registered LSM media (M3-02), not yet run | PANEL-23 (Pending sign-off) |
| §4 :340-346 | Text color mode Class picks the right class per surface; opacity survives | PANEL-21 |
| §4 :347-353 | Reset all settings starts the profile over, same as Reset Profile | PROFILE-5 (the /mm resetall half: PROFILE-6) |
| §4 :354-357 | Reset all settings tooltip wording | dropped: whole expectation asserted by tests/test_options_panel.lua "Panel: Reset all settings' tooltip says it is the same act as Profiles -> Reset Profile" (the old quote also misspelled the shipped "->") |
| §4 :358-360 | A reset leaves other profiles alone | PROFILE-7 |
| §4 :361-365 | The four (all surfaces) meta rows | PANEL-22 |
| §4 :366-375 | Meta color mode drives six dropdowns, not the text modes; Frame Defaults stays on Frame | PANEL-22 (the Frame Defaults clause: PANEL-26 and PANEL-27) |
| §4 :376-387 | Frame entry shape | PANEL-13 (each tab's rows restated from settings/Schema.lua; Background and border reads a *Background* heading then a *Border* heading, not style first) |
| §4 :388-392 | Bars entry shape; paths unmoved | PANEL-13 (including the `window.rows.*` rows being on Frame → Row, not Bars) |
| §4 :393-400 | Header entry shape; paths unmoved | PANEL-13 (corrected: the close row's path is `window.frame.closeButton`, not `showClose`; Title text styles the face the name is drawn in, and the name row is on Windows → General; Button style is three headings, each state's color then its mode on one line, per the Schema.lua comment on the pairing change) |
| §4 :401-406 | Controls tab icons and order | PANEL-14 |
| §4 :407-410 | Visibility entry shape | PANEL-13 (corrected: the hide rules also cover solo, vehicles and flight paths, and in/out of combat is the Combat tab, not a hide rule) |
| §4 :411-420 | Divider: on by default, nothing moves, thickness, color modes | WIN-18 |
| §4 :421-426 | Two control opacities; reveal off uses the hover value | WIN-9 |
| §4 :427-430 | Lock icon same weight in both states | WIN-10 |
| §4 :431-433 | Tab strips fit one row | PANEL-8 |
| §4 :434-437 | Tab art open question | PANEL-12 |
| §4 :438-442 | Header background stops at the title bar | WIN-19 |
| §4 :443-445 | Scale scales the whole window | WIN-21 |
| §4 :446-451 | Frame border None means no border | WIN-22 |
| §4 :452-456 | Closed Border dropdown flush, previews on hover | PANEL-24 |
| §4 :457-459 | Six pages carry Defaults; Windows and Profiles do not; Columns' resets the list | PANEL-25 (corrected: General and Windows each carry one, the Windows button acting on the entry on screen; only Profiles has none. The Columns clause: PANEL-39) |
| §4 :460-467 | Defaults blast radius is page-wide | PANEL-26 |
| §4 :468-475, :483-496 | General page shape, tabs, no duplicates, no Reset meter data button | PANEL-15 |
| §4 :475-478 | Master scale multiplies the window's own | PANEL-16 |
| §4 :478-482 | Minimap toggle immediate; profile switch and reset leave it | PANEL-18 |
| §4 :483-486 | Behavior rows are addon-wide | PANEL-17 |
| §4 :492-493 | Reset position moves only the band's window | WIN-26 |
| §4 :497-505 | Statistic palette editable; four surfaces follow; Defaults restores | PANEL-19 |
| §4 :506-514 | Death-line switches | TIP-21 (the mid-pull clause: COMBAT-19) |
| §4 :515-520 | Four number formats | GRID-1 |
| §4 :521-525 | Two smart values | GRID-2 (the mid-pull clause: COMBAT-3) |
| §4 :526-533 | Window name takes the header's color; footer Defaults | WIN-20 |
| §4 :534-536 | Panel and CLI parity | PANEL-28 |
| §4 :537-540 | /mm list groups; hidden minimized row; set collapses | SLASH-8 |
| §4 :541-546 | An open page locks when combat starts | PANEL-29 |
| §4 :547-548 | Clicking the current tab does nothing | PANEL-9 |
| §4 :549-550 | /mm config refused in combat, not queued | SLASH-12 |
| §4 :551-562 | Every page mid-combat from the Blizzard sidebar, not yet run | PANEL-30 (Pending sign-off) |
| §5 :579-581 | Drag reorders by the full-height handle | PANEL-32 |
| §5 :582-585 | Debug grab/drop lines when a drag does nothing | PANEL-32 |
| §5 :586-589 | One label and one glyph per block | PANEL-37 |
| §5 :590-591 | Untick drops to the top of the unticked group | PANEL-34 |
| §5 :592 | Re-tick lands at the end, rightmost column | PANEL-34 |
| §5 :593-597 | No handle below the rule; insertion line clamps | PANEL-35 |
| §5 :599-604 | Drag feedback: copy, fade, gold line, past the edges | PANEL-33 |
| §5 :605-606 | The last column cannot be unticked | PANEL-36 |
| §5 :608 | Handle hover goes gold, "Drag to reorder" | PANEL-32 |
| §5 :610-612 | A second drag works like the first | PANEL-38 |
| §5 :614 | Defaults restores shipped statistics | PANEL-39 |
| §5 :616-623 | No leftovers; released equals painted | PANEL-40 (corrected: the released lines come before the paint line, and the handle and paint lines carry their box and boundary fields) |
| §5 :625 | Tick and cross tooltips name the click | PANEL-41 |
| §5 :627-628 | Every column draws a bar; even widths | GRID-4 |
| §5 :630-637 | Three tabs; switching tab after a drag leaves nothing | PANEL-42 |
| §5 :639-644 | Library drag (LK-21), per-window line, no armed OnUpdate | PANEL-43 |
| §5 :646-649 | Columns page under the combat cover | PANEL-29 |
| §5 :649-652 | A drag held into combat is refused | PANEL-44 |
| §6 :657-658 | New window named "Multi Meters #2"; picker follows | WIN-27 |
| §6 :670 | Windows draw independently | WIN-28 (corrected: the refresh interval is addon-wide, PANEL-17, so it is no longer a per-window difference) |
| §6 :671-672 | Editing one changes only that one (aliasing) | WIN-28 |
| §6 :673-674 | Copy Bars copies only bars | WIN-29 |
| §6 :675-676 | Copy Everything skips id, name, position | WIN-30 |
| §6 :677 | Duplicate offsets 24px | WIN-32 |
| §6 :678 | Picker keyed by id | WIN-33 |
| §6 :679-680 | Delete confirms; last window refused | WIN-34 |
| §6 :681-682 | Deleting the picked window re-renders against the first survivor | WIN-35 |
| §6 :683-684 | /mm window list, new, delete, copy | SLASH-11 (corrected: the list line reads Enabled/Disabled and counts every column in the list; `copy` takes a one-word source; the CLI delete does not confirm) |
| §6 :685-686 | Resize and sort land on window 2 only | WIN-36 |
| §6 :687-688 | Copy redraws once, one [Set] copy line | WIN-31 |
| §6 :689-690 | Minimap checkbox immediate; get global.minimap.shown; list shows window.columns | PANEL-18 (the /mm list clause: SLASH-8) |
| §7 :699-701 | Visible in every context on a fresh profile | VIS-1 |
| §7 :702 | Open world off | VIS-2 |
| §7 :703 | Hide when solo | VIS-3 |
| §7 :704-707 | Delve shown, resolved=delve, Delves off vs Scenarios | VIS-4 |
| §7 :708 | Scenario or follower dungeon resolved=scenario | VIS-4 |
| §7 :709-711 | Vehicle hides and shows immediately | VIS-5 (corrected: the rule ships off, so the check now ticks Hide in vehicles first) |
| §7b :720-721 | Housing, flight path, pet battle rules | VIS-6 |
| §7b :722-723 | Hide when mounted, druid forms | VIS-7 |
| §7b :724-730 | Hide when skyriding, both dismounts | VIS-8 |
| §7b :731-732 | Hide while dead | VIS-9 |
| §7b :733-736 | Hide in / out of combat, both ticked | VIS-10 |
| §7b :737 | Diagnostics names the deciding rule | VIS-11 |
| §7b :738-745 | Master enable off stands down; six verbs refuse; the rest answer; minimap | STATE-1 (the minimap clauses: SLASH-14) |
| §7b :746 | Test mode overrides context | VIS-12 |
| §8 :766-769 | No Lua error through a key | COMBAT-1 |
| §8 :770-772 | Bars move | COMBAT-2 |
| §8 :773-779 | Text renders abbreviated; smart slot; <secret> rung | COMBAT-3 |
| §8 :780-783 | Names and class colors hold | COMBAT-4 |
| §8 :784-787 | Header renders in combat | COMBAT-5 |
| §8 :788-793 | Text opacity fades only text; bar opacity multiplies | GRID-3 (setting paths corrected to Bars → Text style / Bars → Bar) |
| §8 :794-805 | Text slots are literal, all six | GRID-2 |
| §8 :806-809 | Percent slots go empty in combat | COMBAT-7 (step names Bars → Text content → Left text and `/mm set window.text.leftSlot percent`) |
| §8 :810-812 | Refresh is smooth | COMBAT-8 |
| §8 :813-816 | The grid is not empty | COMBAT-6 |
| §8 :817-818 | Between packs everything comes back | COMBAT-9 |
| §9 SM-04 :833-841 | Always show yourself: your row in the last slot | GRID-12 (corrected: the controls are Frame → Row → Maximum rows and Always show yourself) |
| §9 :842-844 | Rows re-rank live mid-pull | COMBAT-11 |
| §9 :845-846 | Header says restricted | COMBAT-11 |
| §9 :847-848 | Every row present, pets unfolded mid-pull | COMBAT-12 |
| §9 :849-852 | Two players of one class and spec: Damage right, others empty, header note | COMBAT-13 (header wording updated to the shipped "N of M" strings) |
| §9 :853-854 | After the pull everything fills in | COMBAT-9 |
| §9 :855-857 | roster mode: group order out of combat, engine's in combat | GRID-13 (in combat: COMBAT-14; both now set the mode with `/mm set window.data.sortMode`, since the row is hidden) |
| §9 :858-859 | provider mode: game order both sides | GRID-13 (in combat: COMBAT-14; set with `/mm set window.data.sortMode provider`) |
| §9 :860-862 | Stat header click mid-pull re-ranks and reverses | COMBAT-15 |
| §9 :863-865 | Player header click mid-pull refused | COMBAT-16 |
| §9 :866-868 | Name sort arrow moves to the sort column | COMBAT-17 (step: the Player header click sets the name sort) |
| §10 :884-887 | Cell tooltip spells, icons, cap, and N more | TIP-1 (mid-pull: COMBAT-18) |
| §10 :888-890 | Spell order: biggest first, game order in combat | TIP-2 (mid-pull: COMBAT-18) |
| §10 :891-895 | Avoidable Damage: one line per spell | TIP-3 |
| §10 :896-903 | Name tooltip: every stat, palette match, dimmed | TIP-4 |
| §10 :904-908 | Drill-down replaces the grid; click or right-click returns | TIP-5 |
| §10 :909-915 | Breakdown rows show the spell's tooltip | TIP-6 (corrected: the `[Tooltip] row spell=` line also needs `/mm debug tooltip`, modules/Row.lua:455) |
| §10 :916-918 | Left-click in a spell breakdown does nothing | TIP-7 |
| §10 :919-921 | Wheel scrolls grid and breakdown | TIP-8 |
| §10 :922 | Drill-down does not reshuffle | TIP-9 |
| §10 :923-925 | Renaming keeps the breakdown; copy returns to grid | TIP-10 |
| §10 :926-929 | Death timestamps: two styles agree | TIP-11 (setting path corrected to Bars → Text content) |
| §10 :930-934 | Deaths cell tooltip, newest first | TIP-12 |
| §10 :935-939 | Death list rows | TIP-13 |
| §10 :940-942 | Death list count equals the cell | TIP-14 |
| §10 :943-946 | Death tooltip layout with section gap | TIP-15 |
| §10 :947-954 | Death row: incoming hits, columns, Melee, overkill | TIP-16 |
| §10 :955-959 | Death bars draw mid-pull | COMBAT-20 |
| §10 :960-962 | Death row click opens that exact recap | TIP-17 |
| §10 :963-967 | Feign Death not counted out of combat | TIP-18 |
| §10 :968-970 | No C_DeathRecap fallback | TIP-19 |
| §10 :971-972 | Mouse off hides the tooltip (old §10 ran it mid-pull) | TIP-20; mid-pull: COMBAT-18 |
| §10 :973-976 | Hide tooltips in combat | TIP-22 |
| §11 :993-1006 | Provider-order probe in /mm diagnostics | DIAG-21 |
| §11 :1008-1039 | Manual order comparison against Blizzard's meter, report | DIAG-21 |
| §12 :1050-1052 | Unowned ally has its own row | GRID-14 |
| §12 :1053-1056 | Delve companion has a row | GRID-15 |
| §12 :1057-1062 | No enemy gets a row | GRID-16 |
| §12 :1063-1064 | Pet damage folds out of combat | GRID-17 (corrected: pets have their own rows on the shipped settings, as Blizzard's meter shows them; the fold needs General → Behavior → Merge pets into their owner ticked first, which ships off; the Blizzard comparison is restated as the owner's and the pet's separate figures added together) |
| §12 :1065-1068 | In combat the owner is low, catches up | COMBAT-27 (corrected: ticks Merge pets into their owner first; with it off the pet keeps its own row and there is nothing to catch up) |
| §12 :1069 | No Lua error at the transition | COMBAT-27 |
| §12 :1070-1072 | Debug log dropped= / unfolded= counts | DIAG-1 |
| §12 :1074-1076 | Pet swap corrects within one refresh | GRID-18 (corrected: runs with Merge pets into their owner still ticked from GRID-17) |
| §13 :1085-1091 | Meter-unavailable prompt with Blizzard's reason | GRID-19 |
| §13 :1092 | No Lua error, never an unexplained empty window | GRID-19 |
| §13 :1093-1094 | Re-enabled meter returns without /reload | GRID-20 |
| §13 :1096-1099 | Waiting for combat data is the other empty state | GRID-21 (corrected: the header reset is the route; a fresh login keeps the old fights, INSTALL-5) |
| §13 :1101-1104 | Reset meter data empties Blizzard's meter; drill-downs close | WIN-17 |
| §14 :1126 | Every verb answers; unknown verb prints unknown command | SLASH-3 |
| §14 :1127-1129 | Bare /mm is /mm config, and refuses in combat | SLASH-2 (combat: SLASH-12) |
| §14 :1130-1132 | Help and landing page list the same commands | SLASH-4 |
| §14 :1133 | /mm version matches the TOC | SLASH-5 |
| §14 :1134-1136 | set/get target the active window | SLASH-6 |
| §14 :1137-1138 | window.columns.2.width refused | SLASH-7 (corrected: the CLI answers *Setting not found: window.columns.2.width*; the Windows > Columns wording is NS.SetByPath's and the CLI never reaches it) |
| §14 :1139-1140 | Scale out of range and unknown path refused | SLASH-7 (corrected: an out-of-range scale is clamped to 2.00x, not refused) |
| §14 :1141-1142 | /mm toggle all or by name | SLASH-9 |
| §14 :1143-1146 | /mm lock toggles or sets; does not touch Test mode | SLASH-10 (Test mode clause: STATE-6) |
| §14 :1147-1149 | /mm debug console vs flag | DIAG-3 |
| §14 :1150-1154 | Console title bar icons | DIAG-4 |
| §14 :1155-1157 | Copy and clear hover without a tooltip | DIAG-5 |
| §14 :1158-1159 | Clear empties; copy opens the copy window | DIAG-6 |
| §14 :1163-1167 | Six feature verbs refuse while disabled and do nothing | STATE-1 |
| §14 :1168-1171 | Everything else answers while disabled | STATE-1 |
| §14 :1172-1173 | /mm enable restores at once | STATE-1 |
| §14 :1174-1176 | Help index unchanged while disabled | STATE-2 |
| §14 SM-11a :1182-1189 | Minimap button enabled: tooltip, clicks, menu | SLASH-13 (starts from `/mm lock off`, since SLASH-10 now ends locked; the in-combat Test mode clause: STATE-11) |
| §14 SM-11b :1190-1194 | Minimap button disabled: grayed menu, Enabled back | SLASH-14 |
| §14 SM-02 :1195-1198 | Minimap menu during the suspended arm | STATE-5 (corrected: armed with `/mm perf measure b`) |
| §15 :1206-1208 | Profiles page draws after another addon's page | PROFILE-1 |
| §15 :1209-1210 | Switching rebuilds every window | PROFILE-3 |
| §15 :1211 | Panel re-renders; picker lists the new windows | PROFILE-3 |
| §15 :1212 | Different window counts both ways | PROFILE-3 |
| §15 :1213-1214 | Copy brings windows; profiles stay independent | PROFILE-4 |
| §15 :1215 | Reset re-seeds one window | PROFILE-5 |
| §15 :1216-1223 | Profiles page fresh after a switch made off it (M2-18), not yet run | PROFILE-9 (Pending sign-off) |
| §15 :1224-1226 | Fresh character lands on Default | PROFILE-2 |
| §15 :1227 | No errors, no stale window after a switch | PROFILE-3 |
| §16 :1233 | Scope: page Defaults = that page, active window | PANEL-27 |
| §16 :1234 | Scope: Reset all settings = the whole profile plus positions | PROFILE-5 |
| §16 :1235 | Scope: /mm resetall opens the same popup | PROFILE-6 |
| §16 :1236 | Scope: /mm reset <path> = one row | SLASH-6 |
| §16 :1237 | Scope: Reset position = active window | WIN-26 |
| §16 :1238 | Scope: /mm reset-positions = every window | WIN-26 |
| §16 :1241-1244 | /mm resetall asks first; No changes nothing; Yes gives one window | PROFILE-6 (the popup named by its real text; "no `[Set]` line" after No and "exactly one `[Set]` line" after Yes, since the rebuild also logs Roster, Aggregator and Visibility lines) |
| §16 :1245-1247 | Profiles are never touched by any reset | PROFILE-7 |
| §16 :1248-1251 | Reset all is a profile reset; extras deleted; shipped position | PROFILE-5 |
| §16 :1252-1253 | Column list back to the six shipped | PROFILE-5 |
| §16 :1255-1256 | Defaults console line; second press 0 rows | PANEL-27 |
| §16 :1257 | Columns reset console line | PANEL-39 |
| §16 :1258-1260 | Reset profile console line; popup alone logs nothing | PROFILE-6 (the `[Set]` qualifier kept: showing or declining the popup logs no `[Set]` line) |
| §16 :1261 | Copy console line | WIN-31 |
| §17 :1269-1270 | Addon loads and draws rows without LibKa0s | DEGRADED-1 |
| §17 :1271-1273 | One chat line names the cause | DEGRADED-2 (corrected: the first line ends "; running on reduced built-in fallbacks.", and each seam's later line repeats the cause with its own consequence) |
| §17 :1274-1276 | config, help, schema CLI, perf messages | DEGRADED-3 |
| §17 :1277-1278 | Host verbs still work | DEGRADED-4 |
| §17 :1279-1281 | disable / enable still work | DEGRADED-5 |
| §17 :1282-1284 | /mm resetall still works | DEGRADED-6 |
| §17 :1285-1287 | No partial schema | DEGRADED-7 |
| §17 :1288 | Restoring brings everything back | DEGRADED-9 |
| §18 :1306-1308 | One debug line per aggregator pass | DIAG-1 (corrected: `sort=value/provider` mid-pull, there is no `frozen`; identical passes fold into `(xN)` lines through NS.DebugSteady) |
| §18 :1309 | One line per render, roster, visibility pass | DIAG-1 (render lines fold the same way) |
| §18 :1310-1311 | Nothing logged per row or cell | DIAG-1 |
| §18 :1312-1313 | debug off silences; nothing survives /reload | DIAG-2 |
| §18 :1316-1318 | Perf B window makes the addon inert; nothing brings a window back | DIAG-7 (corrected: the B window is `/mm perf measure b`) |
| §18 :1319-1323 | Perf report buckets and nesting note | DIAG-7 (corrected: `finish` prints no report; `/mm perf report` does; fifth round: restored `meterEvent`, `spellEvent` and `systemEvent` each with calls and ms, and names what makes each fire; Pending sign-off) |
| §18 :1324-1325 | Capture records carry the version | DIAG-8 |
| §18 :1326-1327 | Perf output regardless of debug | DIAG-9 |
| §18 :1328 | Hand the report to /wow-addon:perf-analysis | DIAG-7 |
| §18 :1330-1342 | Group capture with the tooltip path (issue #47), unconfirmed | DIAG-10 (Pending sign-off) |
| §19 steps 1-2 :1353-1357 | Abbreviated, one decimal | GRID-5 |
| §19 step 3 :1358 | No /s on the rate | GRID-5 |
| §19 step 4 :1359-1361 | Same figures in combat | COMBAT-3 |
| §19 step 5 :1362 | full format | GRID-1 (its *Full (12400000)* option; the CLI route is PANEL-28's panel/CLI sync; GRID-6 retired, its number not reused) |
| §19 step 6 :1363-1370 | A rate below 1000 (issue #26), unconfirmed | GRID-7 (Pending sign-off) |
| §19 :1372-1374 | Raw digits mean no formatter | GRID-5 |
| §20 step 1 :1378 | Realm stripped | GRID-8 |
| §20 step 2 :1379-1380 | Follower names at the default cap | GRID-9 (cap corrected: the shipped default is 15, not 20) |
| §20 step 3 :1381 | Truncation with one … glyph | GRID-9 |
| §20 step 4 :1382-1383 | Accent-safe truncation | GRID-10 |
| §20 step 5 :1384 | 0 shows names in full | GRID-9 |
| §20 step 6 :1385-1386 | Hyphen kept in breakdown spell names | GRID-11 |
| §21 step 2 :1391-1394 | Segment menu contents and anchor; session line not a target | GRID-25 |
| §21 step 3 :1395-1396 | Pinning shows the fight and names it | GRID-26 |
| §21 step 4 :1397-1398 | Tooltip and drill describe the pinned fight | GRID-27 |
| §21 step 5 :1399-1400 | Pinned stays, unpinned follows | GRID-28 |
| §21 step 6 :1401 | Current clears the pin | GRID-29 |
| §21 step 7 :1402 | Pin survives /reload | GRID-30 |
| §21 step 8 :1403-1404 | A meter reset falls back to Current | GRID-31 (route corrected: the header's reset control; there is no settings-page reset) |
| §22 step 2 :1411-1412 | v1→v2: every column the same width | INSTALL-6 |
| §22 step 3 :1413-1414 | v1→v2: a wider window keeps its width | INSTALL-6 |
| §22 step 4 :1415 | v1→v2: idempotent after /reload | INSTALL-6 |
| §22 step 5 :1416 | v1→v2: a second profile is lifted too | INSTALL-6 |
| §23 step 2 :1428-1431 | v12→v13: title bar and control colors carried | INSTALL-7 |
| §23 step 3 :1432-1433 | v12→v13: Header → Title bar toggle unticked | INSTALL-7 |
| §23 step 4 :1434-1435 | v12→v13: Class for the ticked flag | INSTALL-7 (location corrected to Header → Button style) |
| §23 step 5 :1436 | v12→v13: idempotent | INSTALL-7 |
| §23 step 6 :1437-1438 | v12→v13: a second profile carried | INSTALL-7 |
| §24 :1459-1460 | Tooltip bars wear the tooltip's texture | TIP-25 |
| §24 :1461 | Bar spacing | TIP-26 (the default corrected: 1, not 0) |
| §24 :1462-1463 | Font reaches spell names | TIP-27 |
| §24 :1464-1468 | Tooltip bar border and None | TIP-28 |
| §24 :1469-1470 | Every anchor differs | TIP-23 (the stale "At cursor" comparison removed: that anchor no longer exists) |
| §24 :1471-1473 | Offsets stay on screen | TIP-29 |
| §24 :1474-1475 | Maximum spells 0 lists everything | TIP-30 |
| §24 :1476-1479 | Other addons' tooltips untouched | TIP-31 |
| §25 :1497-1498 | Targets section out of combat | TIP-32 |
| §25 :1499-1500 | Damage cells only | TIP-33 |
| §25 :1501-1503 | Another player's own targets | TIP-34 |
| §25 :1504-1506 | Absent mid-pull | COMBAT-22 |
| §25 :1507-1508 | No Lua error mid-pull | COMBAT-22 |
| §25 :1509-1510 | Cap trims after ordering | TIP-35 |
| §25 :1511-1513 | Off: no targets bucket activity | TIP-36 |
| §26 control :1532-1534 | Export control leftmost, same size and color | WIN-1 |
| §26 control :1535-1537 | Export control draws the collection's art | WIN-1 |
| §26 control :1538-1542 | Atlas candidates unconfirmed | DIAG-20 (Pending sign-off) |
| §26 control :1543-1545 | /mm diagnostics reports the atlas probe | DIAG-20 (Pending sign-off) |
| §26 control :1546-1548 | Export control tooltip, the only one | WIN-11 |
| §26 control :1549-1550 | Title bar off takes the strip | WIN-12 (location corrected to Header → Title bar) |
| §26 control :1551 | Click opens the modal centered | EXPORT-1 |
| §26 modal :1559-1561 | Modal centered on its window | EXPORT-1 |
| §26 modal :1562-1565 | Title bar, drag, close icon | EXPORT-2 |
| §26 modal :1566-1567 | Three selectors, two actions | EXPORT-3 |
| §26 modal :1568-1571 | Action icons keep their words | EXPORT-4 |
| §26 modal :1572-1574 | One modal, reused, re-centers | EXPORT-5 |
| §26 modal :1575 | Esc and close button close it | EXPORT-6 |
| §26 modal :1576-1580 | Esc with a menu open closes both | EXPORT-7 |
| §26 modal :1581-1582 | Copy window close icon and mono face | EXPORT-22 |
| §26 modal :1583-1586 | Selector menu skin | EXPORT-8 |
| §26 modal :1587-1591 | Click outside closes and lands | EXPORT-9 |
| §26 modal :1592 | Pick closes and labels the button | EXPORT-10 |
| §26 modal :1593 | Same for Channel and Lines | EXPORT-8 (picking: EXPORT-10) |
| §26 modal :1594-1599 | One menu at a time | EXPORT-11 |
| §26 modal :1600-1604 | No leading glyph | EXPORT-12 |
| §26 modal :1605-1607 | Metric reads the window's sort before a touch | EXPORT-13 |
| §26 modal :1608-1609 | Picking repaints immediately | EXPORT-10 |
| §26 modal :1610-1615 | Fresh profile: Metric follows the window | EXPORT-13 |
| §26 modal :1616-1625 | A pick holds; the next open reseeds | EXPORT-14 |
| §26 whisper :1632-1634 | Name box only for Whisper | EXPORT-15 |
| §26 whisper :1635-1638 | Whisper row grows the modal | EXPORT-15 |
| §26 whisper :1639-1640 | Typed name fully visible | EXPORT-16 |
| §26 whisper :1641-1642 | Print without Enter whispers | EXPORT-17 |
| §26 whisper :1643 | Back to Self only shrinks the modal | EXPORT-15 |
| §26 whisper :1644 | Enter stores the name | EXPORT-17 |
| §26 whisper :1645-1647 | Focus loss stores the name | EXPORT-17 |
| §26 whisper :1648 | Esc clears focus; second Esc closes | EXPORT-18 |
| §26 whisper :1649 | Name kept across channel switches | EXPORT-19 |
| §26 whisper :1650-1652 | Empty whisper box | EXPORT-20 (behavior updated: it now refuses with "Enter a name to whisper to.", per tests/test_export_modal.lua "Print to Chat names a blank whisper recipient before it builds anything") |
| §26 whisper :1653 | Cross-realm needs Name-Realm | EXPORT-21 (now a step: whisper `Name-Realm`, Print to Chat) |
| §26 CSV window :1660-1662 | Opens above the modal, title, centered | EXPORT-22 |
| §26 CSV window :1663-1665 | Monospace text | EXPORT-22 |
| §26 CSV window :1666-1669 | Pre-selected, at the top | EXPORT-23 |
| §26 CSV window :1670 | Ctrl+C copies the whole thing | EXPORT-24 |
| §26 CSV window :1671 | Esc closes only the copy window | EXPORT-25 |
| §26 CSV window :1672 | Re-fills rather than stacking | EXPORT-26 |
| §26 CSV window :1673-1675 | First-open width fallback | EXPORT-28 |
| §26 adoption steps 1-2 :1681-1683 | Library copy window centered, pre-selected | EXPORT-22 (selection: EXPORT-23) |
| §26 adoption step 3 :1684 | Paste has the whole CSV | EXPORT-24 |
| §26 adoption step 4 :1685 | Esc leaves the modal | EXPORT-25 |
| §26 adoption step 5 :1686 | Copy window follows a moved meter window | EXPORT-27 |
| §26 adoption step 6 :1687 | After /reload still one window, centered | EXPORT-26 |
| §26 file :1691-1698 | Header line exact; byte-identical on another locale | EXPORT-29 on an English client (its header row compared byte for byte with LOC-1's line; the three tests/test_export.lua cases build the header from Const.STATS and pin no literal line). The locale half and the literal line: LOC-1 (the "26 columns" count corrected, the listed header has 24) |
| §26 file :1699-1700 | _ps twice, _pct per stat | EXPORT-29 |
| §26 file :1701-1704 | Every catalog stat, not the window's columns; `enemy_damage_taken` must not appear | EXPORT-29 (every catalog stat from a Damage-only window). The `enemy_damage_taken` clause: dropped, asserted by tests/test_constants.lua:124 "Constants: EnemyDamageTaken is READABLE but is NOT a column" with tests/test_export.lua:453 (the header is the identity columns plus `Export.Columns()`, built from the catalog alone) |
| §26 file :1705-1706 | Raw integers; bare two-decimal pct | EXPORT-29 |
| §26 file :1707-1710 | session and duration on every row | EXPORT-29 |
| §26 file :1711-1712 | Empty cells, never nil | EXPORT-29 |
| §26 file :1713-1714 | CRLF, no trailing blank row | EXPORT-29 (no trailing blank row). The CRLF clause: dropped, asserted by tests/test_export.lua:463 "Export.CSV writes one row per entry and terminates with a CRLF" |
| §26 file :1715-1716 | 40-row ceiling | EXPORT-29 |
| §26 names :1722 | Space-and-hyphen name in one cell | EXPORT-30 |
| §26 names :1723-1726 | Unquoted; realm strip never reaches the serializer | EXPORT-30 |
| §26 names :1727-1728 | CSV keeps -Realm | EXPORT-31 |
| §26 names :1729-1730 | Comma or quote gets quoted | EXPORT-32 |
| §26 chat :1745-1747 | Self only reaches nobody, with banner | EXPORT-33 |
| §26 chat :1748-1754 | Dump shape, abbreviated | EXPORT-34 |
| §26 chat :1755-1757 | Parenthetical only what is meaningful | EXPORT-35 |
| §26 chat :1758-1760 | Ranking follows the metric | EXPORT-36 |
| §26 chat :1761-1762 | Line cap holds | EXPORT-37 |
| §26 chat :1763-1765 | Channels reach their audience, no banner | EXPORT-38 |
| §26 chat :1766-1769 | No Automatic channel; AUTO folds to Self | EXPORT-39 |
| §26 chat :1770-1774 | Say outdoors arrives whole, with a warning | EXPORT-40 |
| §26 chat :1775-1776 | Say inside an instance is staggered | EXPORT-41 |
| §26 chat :1777-1779 | Pause every fifth line | EXPORT-42 |
| §26 chat :1780 | Whisper reaches only the named character | EXPORT-43 |
| §26 chat :1781-1786 | Whisper my target: member, cross-realm, none, NPC | EXPORT-44 |
| §26 chat :1787-1788 | Target read at the click | EXPORT-45 |
| §26 chat :1789-1792 | Whisper to nobody stops after one line | EXPORT-46 |
| §26 chat :1793-1794 | No truncated line | EXPORT-47 |
| §26 chat :1795-1796 | Empty segment sends nothing | EXPORT-48 (corrected: each action prints *There is nothing to export.*, and the empty segment comes from the header reset, since a fresh login keeps the old fights, INSTALL-5) |
| §26 remembered :1804-1810 | Channel, Lines, name remembered; Metric reseeded; no [Set] on an unchanged seed | EXPORT-49 |
| §26 remembered :1811-1815 | No Export group on General | EXPORT-50 |
| §26 remembered :1816-1819 | get/set export rows; modal follows | EXPORT-51 |
| §26 remembered :1820 | Export choices switch with profiles | PROFILE-8 |
| §26 /mm export :1832-1835 | No name: the active window | EXPORT-52 |
| §26 /mm export :1836-1837 | By name, case and spacing kept | EXPORT-53 |
| §26 /mm export :1838 | Unknown window refused | EXPORT-54 (message updated to the shipped "No window named '%s'.") |
| §26 /mm export :1839-1840 | Verb in help and landing with one description | SLASH-4 |
| §26 /mm export :1841-1842 | A never-drawn window is exportable | EXPORT-55 |
| §26 combat :1859 | Nothing is exported mid-pull | COMBAT-23 |
| §26 combat :1860-1862 | One refusal line | COMBAT-23 |
| §26 combat :1863-1866 | Modal repaints: buttons gray, red sentence | COMBAT-23 |
| §26 combat :1867-1869 | Glyph does not flicker | COMBAT-24 |
| §26 combat :1870 | Glyph and /mm export refuse mid-pull | COMBAT-24 |
| §26 combat :1871-1873 | No Lua error | COMBAT-23 |
| §26 combat :1874-1879 | Buttons come back after the pull on their own | COMBAT-25 |
| §26 combat :1880-1881 | Closed through the pull, opens live | COMBAT-26 |
| §27 steps 1-5 :1898-1906 | Identity capture procedure | DIAG-22 |
| §27 step 6 :1907-1913 | Identity line arithmetic and header count | DIAG-22 (the header wording: COMBAT-13) |
| §27 :1917-1938 | What to read in the capture | DIAG-22 |
| §27 :1940-1944 | What makes the capture worthless | DIAG-22 (corrected: the "not measured" line appears before any flagged pull; the after-combat capture shows the last pass, and a party capture runs but proves nothing) |
| §28 :1962-1968 | Feign verb refuses the typo, stays unarmed | DIAG-23 (corrected: the client prints the backticks around both commands) |
| §28 :1976-1994 | Feign capture and what to read | DIAG-24 |
| §28 :1999-2019 | Recap provider check (issue #25) | DIAG-25 |
| §29 strip :2035-2041, :2051-2054 | Pooled tab strip: labels, selection, band height, not yet run | PANEL-11 (Pending sign-off) |
| §29 strings :2043-2048, :2055-2057 | Perf strings unlabeled / perf run CANCELED, not yet run | DIAG-11 (Pending sign-off; corrected: `start` stamps the date and time into the label, so `unlabeled` never shows, and the report needs `/mm perf report`) |
| §29 :2058 | No Lua error | PANEL-11 (and DIAG-11) |
| §30 :2085-2097 | Border dropdown identical across five addons and load orders, not yet run | PANEL-24 (Pending sign-off) |
| §31 :2119-2121 | Exactly one close control, top right, not yet run | DIAG-12 (Pending sign-off) |
| §31 :2122-2125 | The collection's close mark | DIAG-12 |
| §31 :2126 | Close and reopen | DIAG-12 |
| §31 :2127 | No Lua error | DIAG-12 |
| §32 step 1 :2136-2139 | Bar fills slide out of combat | GRID-22 |
| §32 step 2 :2140-2142 | Bar fills slide in a real pull, no error | COMBAT-28 |
| §32 step 3 :2143-2144 | Animation off snaps | GRID-23 |
| §32 step 4 :2145-2146 | Numbers, order and export unchanged | GRID-24 |
| §33 steps 1-2 :2162-2165 | No stored session id is 0, across a login | GRID-32 |
| §33 step 3 :2166-2167 | Every listed fight pins | GRID-32 |
| §33 step 4 :2168-2169 | get sessionID reads the pin; Overall reads 0 | GRID-32 |
| §33 step 5 :2170-2171 | set 0 unpins; -1 refused | GRID-32 |
| §34 step 2 :2186-2188 | v13→v14: every window locked | INSTALL-8 |
| §34 step 3 :2189 | v13→v14: Lock frame ticked; untick unlocks | INSTALL-8 |
| §34 step 4 :2190-2191 | v13→v14: idempotent; master.locked derived | INSTALL-8 |
| §34 step 5 :2192-2193 | v13→v14: second profile locked | INSTALL-8 |
| §34 step 6 :2194 | v13→v14: unticked keeps each window's lock | INSTALL-8 |
| §35 step 1 :2205-2209 | Report in both forms and both slashes while disabled | DIAG-13 |
| §35 step 2 :2210-2211 | Report appends | DIAG-14 |
| §35 step 3 :2212-2214 | Report under the restriction | COMBAT-29 |
| §35 step 4 :2215-2217 | Copy holds markers, no color escapes | DIAG-15 (corrected: the end line is `==== Ka0s Multi Meters diagnostics end: N line(s) ====`) |
| §35 step 5 :2218-2219 | Report ungated by the debug flag | DIAG-16 |
| §35 step 6 :2220-2222 | Buffer cap 3000 | DIAG-17 |
| §35 step 7 :2223-2224 | Old diag name gone | DIAG-18 |
| §35 step 8 :2225-2227 | README bug-report steps word for word | DIAG-19 |
| §36 MM-S1 :2243 | Settings tree has only three entries | PANEL-1 |
| §36 MM-S2 :2244 | Band, rail, opens on General, rail level with tab art | PANEL-2 |
| §36 MM-S3 :2245 | Only the controls scroll | PANEL-3 |
| §36 MM-S4 :2246 | Per-entry tab memory | PANEL-4 |
| §36 MM-S5 :2247 | Band switch keeps Bars → Border | PANEL-5 |
| §36 MM-S6 :2248 | General entry acts and Copy settings | PANEL-31 |
| §36 MM-S7 :2249 | Leaving Columns mid-drag leaves no handle | PANEL-42 |
| §36 MM-S8 :2250 | Defaults scopes: Frame only, General nothing, Columns list and header rows | PANEL-27 (the Columns clause: PANEL-39) |
| §36 MM-S9 :2251 | Windows page under the combat cover | PANEL-29 |
| §36 MM-S10 :2252 | Tabs in one row from the first frame | PANEL-8 |
| §36 MM-S11 :2253 | Rail tooltips and tree-pane look | PANEL-10 |
| §37 MM-E1 :2261 | [Event] PLAYER_ENTERING_WORLD and ZONE_CHANGED_NEW_AREA | DIAG-26 (Pending sign-off) |
| §37 MM-E2 :2262 | [Event] PLAYER_REGEN_DISABLED / ENABLED | DIAG-27 (Pending sign-off) |
| §37 MM-E3 :2263 | [Event] GROUP_ROSTER_UPDATE | DIAG-28 (Pending sign-off) |
| §37 MM-E4 :2264 | [Event] ADDON_RESTRICTION_STATE_CHANGED pairs | DIAG-29 (Pending sign-off) |
| §37 MM-E5 :2265 | No [Event] line for mount, form, death | DIAG-30 (Pending sign-off) |

## Non-check material

| Old location | What it was | Where it went |
|---|---|---|
| :1-14 | Title, intro, companion docs | Intro paragraph |
| :16-22 | Re-verification note (2026-08-27, settings-redesign branch) | dropped: stale batch history; every step it flagged was re-read against the current code in this rewrite |
| :26-29, :34-42 | Conventions: /reload, BugSack, Restricted, A pull, Pass lines | Before you start (Pass lines replaced by Result lines) |
| :43-49 | What needs no smoke run (M4c-06) | Intro paragraph, without the M4c-06 history |
| :51-89 | Suite index (stale: a wrong §29 anchor; §29, §31, §37 missing) | Index |
| §8 :750-763, :820-821; §26 :1517-1525, :1846-1857, :1883-1884 | Setup, rationale and Record-for-the-report blocks | COMBAT intro and Before you start; the atlas record in DIAG-20 |
| §11 :980-991, §27 :1888-1896, §28 :1953-1960, §29 :2023-2033, §30 :2064-2083, §31 :2105-2110, §32 :2131-2134, §33 :2155-2160, §35 :2200-2203 | Why-this-is-in-client rationale | Condensed into the checks' own wording |
| §36 :2235-2239 | Windows page intro and the owner's 2026-09-26 sign-off (MM-S1 to MM-S11 all passed) | PANEL theme intro; the sign-off record is dropped per D4 (git keeps it) |
| §37 :2257 | Event trace setup line | DIAG-26 |
| §27 :1946-1949 | Record for the report: group size and duplicated class+spec pairs, instance and difficulty, the captures in full, whether any Lua error appeared | DIAG-22 (the record list, and "no Lua error at any point" as an expectation) |
| §28 :1996-1997 | Record for the report: group size and composition, whether the hunter was the local player, the full buffer, the Deaths count | DIAG-24 (the hunter is a party member by the step; the rest on the record list) |
| §32 :2148-2149 | Pass summary and Record (client build, key or raid) | GRID-22, GRID-23, GRID-24, COMBAT-28 (the client build goes on every Result line) |
| §33 :2173-2175 | Pass summary and Record (client build, lowest and highest ids) | GRID-32 |
| §34 :2196 | Record: client build | INSTALL-8's Result line |
| §35 :2229 | Record: client build, whether step 3 ran in a key or a raid, where step 6 settled | COMBAT-29 (key or raid), DIAG-17 (where it settled) |
| :2269-2285 | What to report | Before you start → Reporting a failure |

## Owed checks from the 2026-09-23 plan

Ka0sAddonsCommonTasks `docs/2026-09-23-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION`: `RESUME.md` §5 leaves "the in-client sessions in `06_SMOKE_TESTS.md`" to the owner, the Sign-off table there is empty for every session, and `checkpoints.tsv` records only MM-20's capture, SM-06 and the M6 minimap re-check as run. Every Multi Meters step in `06_SMOKE_TESTS.md` (Session MM, the Multi Meters steps of Q, P and X2, and the steps of L and X1 that run through `/mm`), mapped to the new suite:

| 06 step | What it checks | New ID | Pending? |
|---|---|---|---|
| P.4 | MM-20 before capture | DIAG-7 (the capture procedure) | no: the before bundle 20260924-133043 is committed (checkpoints.tsv, 2026-09-24) |
| P.5 | Fixture: button hidden, a window collapsed, a fight | INSTALL-9 setup | setup, not a check |
| P.6 | Roster survives a real logout | INSTALL-5 | no: recorded yes 2026-09-24 (06 P.6; old §2 SM-06) |
| MM.1 | Upgrade: minimap `hide` carried to `shown`, v16 minimize keys, stamp 16 | INSTALL-9 (new) | yes |
| MM.2 | `/mm set global.minimap.shown false`, checkbox follows, survives `/reload` | PANEL-18 (extended) | yes |
| MM.3 | `rejected events: none` | DIAG-31 (new; `/mm debug diag` is retired, DIAG-18, so read through `/mm diagnostics`) | yes |
| MM.4 | A validated row's refusal, no echo | SLASH-7 (extended with `window.data.sortMode bogus`; the width example clamps, recorded 2026-09-24 in 06 X1.3) | yes |
| MM.5 | Launcher gate disabled and suspended | SLASH-14 (disabled), STATE-5 (suspended) | SLASH-14 no: 06 X1.4 PASS 2026-09-25 after M6; STATE-5 yes |
| MM.6 SM-01 / SM-02 / SM-03 | Latch holds on every show path | STATE-3 / STATE-5 / STATE-4 | yes |
| MM.7 | Rename keeps the drill-down | TIP-10 | yes |
| MM.8 | Only the band's window moves; one refresh and one `[Set]` per copy; minimap checkbox | WIN-28, WIN-31, PANEL-18 | yes |
| MM.9 | Color drag throttle | PANEL-45 (new; the per-column swatch is gone, so it drags Bars → Bar → Bar color) | yes |
| MM.10 | Columns tabs; ReorderList drag | PANEL-42 (tabs), PANEL-43 (drag) | PANEL-42 no: the owner's 2026-09-26 run (old §36 MM-S4, MM-S7); PANEL-43 yes |
| MM.11 | Slash lines through the locale, the plural | SLASH-10, STATE-9 (extended), WIN-26 (extended) | yes |
| MM.12 | MM-20 after capture | DIAG-7 (the capture procedure) | no: PASS 2026-09-24 (06 MM.12; checkpoints.tsv) |
| MM.13 | Roster survives `/reload`; bounded store | INSTALL-4, INSTALL-5 | no for this step: the `/reload` half recorded 2026-09-24, the bound rests on MM-21's headless case (INSTALL-4 is pending for its own correction) |
| MM.14 | The full old suite | every theme | the SM steps are listed by ID above; the rest follows the old doc's own records |
| Q.4 | MM-20 after capture on a dungeon pull | none | not needed: P.4 used a dummy, MM.12 ran |
| Q.5 | Always show yourself, scroll-aware | GRID-12 | yes |
| Q.6 | PARTY reaches the group, SELF prints with no notice | EXPORT-38, EXPORT-33 (both extended) | yes |
| Q.7 | `spellEvent` and `systemEvent` with calls and ms in a raid pull | DIAG-7 (restored, with the whisper `systemEvent` needs) | yes |
| L.7 | Console buffer trim keeps the newest lines in order | DIAG-17 (extended) | yes |
| L.8 | Perf buckets under the right parent; addon restored after `finish` | DIAG-7 (extended with *addon RESUMED*) | yes |
| L.9 | Columns drag through ReorderList | PANEL-43 | yes |
| L.10 | Font picker names in their own face | PANEL-23 (extended) | yes |
| L.12 | No widget leak across window-picker switches | PANEL-46 (new) | yes |
| X1.2 | No leak across page and picker switches (the `/mm` share) | PANEL-46 | yes |
| X1.3 | Slash refusal echo (the `/mm` share) | SLASH-7 | the clamp recorded 2026-09-24; the refusal half is SLASH-7's pending row |
| X1.4 | Launcher refusal and clicks (the `/mm` share) | SLASH-13, SLASH-14 | no: PASS 2026-09-25 after M6 |
| X1.5 | No rejected events at load (the `/mm` share) | DIAG-31 (corrected: the debug flag does not survive `/reload`, so the `[Init]` line is read through `/mm disable`, `/mm enable`) | yes |
| X1.6 | Taint and combat with everything loaded (the `/mm` share) | PANEL-30 (extended with the action-bar click), SLASH-12 | yes |
| X2.11 | Loads degraded and answers `/mm` | DEGRADED-1, DEGRADED-3 | yes |

Session L's other steps (L.1 to L.6, L.11, L.13, L.14) and X1's other steps run in other addons or across the collection with nothing Multi Meters owns, so they belong to their own suites.

## Corrections made while merging

Stale facts in the old doc, checked against the code and fixed in the new check: the reset-all window is **Multi Meters #1**, not *Meter* (PROFILE-5); a meter reset is only on the header control, not a General page button (GRID-31); the default name cap is 15, not 20 (GRID-9); the tooltip anchor "At cursor" no longer exists (TIP-23); control color modes live on Header → Button style (INSTALL-7); the title bar toggle is Header → Title bar (WIN-12); Text opacity is Bars → Text style and Death timestamps Bars → Text content (GRID-3, TIP-11); Tooltip's tabs are General, Bar, Bar background, Bar border, Text, Contents, with the scale slider on General and the Targets rows on Contents (PANEL-13); General and Windows both carry a Defaults button and only Profiles has none (PANEL-25); Tooltip → Bar spacing ships at 1, not 0 (TIP-26); the identity-ambiguity header shows the `N of M` counts (COMBAT-13); a blank whisper is refused with *Enter a name to whisper to.* (EXPORT-20); an unknown export window reads *No window named '…'.* (EXPORT-54); the CSV header has 24 columns, not 26 (EXPORT-29, LOC-1); the General page has three tabs (PANEL-15); a column width is no longer a per-column setting (INSTALL-4); Header → Title text's color mode is Class / Custom, with no Per-statistic (PANEL-20, matching WIN-20); a window drags by its title bar, not its body, and the cells answer the mouse whether or not it is locked (WIN-25); creating a profile on the Profiles page switches to it, so each `/mm profile` switch in PROFILE-14 starts from Default.

Corrected in the second review round (SP-MM-03R), each against the code: VIS-5 switches Hide in vehicles on first (the rule ships off); PROFILE-6 counts only `[Set]` lines and names the popup by its text; WIN-5, GRID-12 and COMBAT-7 name the real controls; WIN-28 drops the per-window refresh; GRID-13, COMBAT-14 and COMBAT-17 set the hidden sort row through `/mm set` or the Player header; EXPORT-21 is a step; EXPORT-29 compares its header row with LOC-1's; DIAG-22 regains its no-Lua-error clause and its record list and says when the not-measured line appears. Re-verifying every chat and console string found more: SLASH-7 (the ordinal path is *Setting not found*, an out-of-range scale is clamped), SLASH-11 (the list line, the one-word copy source, no CLI confirmation), STATE-5 and DIAG-7 (the B window is `measure b`; the report is `/mm perf report`), DIAG-11 (no `unlabeled` from the slash), TIP-6 (`/mm debug tooltip`), PANEL-40 (line order and full shapes), DIAG-1 (`value/provider` mid-pull and `(xN)` folding), DIAG-15 (the end marker's count), DIAG-23 (the printed backticks), EXPORT-48 (*There is nothing to export.*) and DEGRADED-2 (the first line's full text).

Corrected in the third review round (SP-MM-03R), each against the code: PANEL-13 names every tab's rows again (Frame, Header and Visibility from settings/Schema.lua and settings/Schema_Compose.lua, with the old doc's stale Background and border order, Title text name, Button style pairing and hide-rule list fixed) and restores the `window.rows.*`-on-Frame clause; STATE-11 drops the General page's Test mode box, which the combat cover makes unreachable (settings/General.lua renders through H.SetRenderer; PANEL-29, PANEL-30); EXPORT-48 and GRID-21 build the empty segment with the header reset, since a fresh login keeps the old fights (INSTALL-5). Pending sign-off now also lists the checks corrected earlier without a row: INSTALL-6, INSTALL-8, SLASH-9, EXPORT-33, EXPORT-39 and EXPORT-53, plus STATE-11 and GRID-21.

Corrected in the fourth review round (SP-MM-03R), each against the code: PANEL-13 reads `window.frame.closeButton`, the close row's real path (settings/Schema.lua; the key was never renamed to `showClose`); WIN-16 expects the dialog's own text, *Clear every recorded combat session?* with Yes / No (settings/General.lua `MULTIMETERS_RESET_METER_DATA`), and places the meter-data warning on the Show reset row's tooltip, and it joins Pending sign-off; SLASH-13 starts from `/mm lock off`, so the menu's Locked (a bare `/mm lock`, core/LauncherSetup.lua) toggles to locked as the old SM-11a ran it.

Corrected in the fifth review round (SP-MM-03R), each against the code: DIAG-7 regains the old §18 expectation that `meterEvent`, `spellEvent` and `systemEvent` each show calls and ms, and says what makes each fire (core/MultiMeters.lua: the three `DAMAGE_METER_*` handlers, `UNIT_SPELLCAST_SUCCEEDED` from any unit, `CHAT_MSG_SYSTEM`; core/PerfSetup.lua's bucket list; LibKa0s Perf records only inside an armed window's combat and prints no row for an empty bucket), so the capture adds a whisper to a name nobody is playing during window A; it also expects *addon RESUMED — restored* at `finish` and leaves `tooltip` and `targets` to a hovered run (DIAG-10). Pending sign-off now lists every Multi Meters check the 2026-09-23 plan owes (table above), with the new checks INSTALL-9, PANEL-45, PANEL-46 and DIAG-31 and the extended SLASH-7, PANEL-18, PANEL-23, PANEL-30, STATE-9, WIN-26, EXPORT-33, EXPORT-38 and DIAG-17, each re-read against the code (core/Database.lua `migrations[15]`, settings/Schema_Compose.lua's minimap row, core/Diagnostics.lua `reportEvents`, LibKa0s Slash `emitRefusal`, settings/Slash.lua's lock, test and reset-positions lines, modules/Export.lua `Export.Send`, LibKa0s OptionsWidgets' color throttle).

Corrected in the sixth review round (SP-MM-03R), each against the code: DIAG-7's `finish` lines are in chat order, *perf run FINISHED — saved; …* first and *addon RESUMED — restored* second (LibKa0s Perf.lua `SUBS.finish`: `P.Announce` prints at once, the RESUMED line rides the returned table that settings/Slash.lua `doPerf` prints after `OnCommand` returns), with the console's reverse order (`P.Resume`'s *addon RESUMED — events and frames restored* is logged first); and each event row needs calls above zero and a total ms column, not total ms above zero, because the report prints total ms with `%10.2f` and `NS:OnSystemMessage` returns at once when no whisper export is pending, so a correct `systemEvent` row can read 0.00 (the JSON line's `totalMs` keeps the unrounded value).
