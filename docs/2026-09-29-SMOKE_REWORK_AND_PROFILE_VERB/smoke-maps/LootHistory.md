# Smoke coverage map — LootHistory

Old `docs/smoke-tests.md` (1469 lines, sections 1-19, about 260 discrete checks plus 6 non-check rows: a field note, two pointers, a restore step, a scope note and the subset guide) → new suite (1224 lines, 229 checks in 14 themes). Line numbers are the old file at `d15c947`. One real check dropped (covered by a named test); 12 new checks (PROFILE-1 to 3, PROFILE-6 to 13, DEGRADED-10) have no old origin. Every old row appears once below. Pending sign-off (spec S4, clarified 2026-09-29): the old file had no `Result:` lines (its **Pass.** headings are expectations, not results), so every carried-over check is owed unless a record of the owner's pass exists. Four do: review F-001 (CAP-4 to CAP-6, docs/ARCHITECTURE.md Known limitations), the old § 3 field note of 2026-07-22 (currency capture and refund, CAP-11 and CAP-12), `2026-09-25-DIAGNOSTICS_COMMAND/99_REPORT.md` LH-S1 to LH-S11 and LH-X1 (PASS 2026-09-26: DIAG-19 to DIAG-22, DIAG-24, DIAG-25 and COMBAT-8, whose texts are unchanged from old § 12a), and the 2026-09-23 plan's X1.4 in `06_SMOKE_TESTS.md` (recorded PASS 2026-09-25 after M6: `/lh disable`, then left-click opens Settings, right-click opens the options menu, the M5 status tooltip shows), which passes LAUNCH-3 whole (its text is unchanged from old § 11 at the M6 commit `b0833a0`, and the launcher code has not changed since: Launcher minor 4, and `core/LauncherSetup.lua` changed only a comment and dropped `NS.RefreshLauncher`, which touches neither click). Those 13 checks are the only ones not listed; the other 216 are. The same report passes only the cap half of DIAG-6 (LH-S7), the diagnostics half of DEGRADED-4 (LH-X1) and the `/lh diag` and `/lh debug diag` inputs of DIAG-23 (LH-S8, which never ran `/lh dump`), so all three stay listed. X1.4 likewise passes only part of LAUNCH-2 (the tooltip, not the re-hover after ticking Lock frame and Test mode, which X1.4 never did), LAUNCH-4 (the menu opening, not its four entries' actions) and LAUNCH-5 (the tooltip and the menu opening while disabled, not the grayed entries or the menu's Enabled, since X1.4 re-enabled with the slash verb), so those three stay listed with what is owed. The 2026-09-23 plan's owed steps are named on their rows: LH.2 = LAUNCH-8, LH.4 = DIAG-7, LH.5 = CAP-28 to CAP-30, LH.6 = STATE-6, LH.8 = COMBAT-5 and COMBAT-7, LH.9 = INSTALL-3, Q.1 = CAP-14, Q.3 = CAP-19 and X2.4 = DEGRADED-8. Q.2 (CAP-15) recorded a PASS on 2026-09-24 for the console order and the stamp's `encounterID` only; the loot was gold, so no row was written and the `sourceDetail` dump and the wipe line are still owed, and CAP-15 stays listed. The NAVRAIL plan's RV-S1 (a no-change look at the settings page, PASS 2026-09-26) matches no check's expectation and signs none.

| Old location | Behavior | New ID |
|---|---|---|
| §1 :62-72 (setup, pass 1) | Clean install loads with no Lua error at login and /reload | INSTALL-1 |
| §1 :73-79 | TOC load order; help prints; options list shows the sub-pages | INSTALL-2 |
| §1 :80-82 | Bare /lh (and spaces only) opens the landing page, no window, no chat | SLASH-1 |
| §1 :83-85 | /lh help index: one row per COMMANDS entry, banner, window stays closed | SLASH-2 |
| §1 :86-90 (fresh DB) | Fresh DB shape: schemaVersion 10, global vs profiles.Default | INSTALL-3 |
| §1 :90-92 (existing account) | Existing account upgrade: history intact, settings in Default, retention global | INSTALL-4 |
| §1 :93-97 | /lh list seeded defaults and the minimap.shown inversion | SLASH-3 (expectation corrected: windowScale prints `1.00x`, the row's `fmt = "%.2fx"` in settings/Schema.lua; excludedSources prints `(none)`, not a table address; `settings.retentionDays` is account-wide, D6, so the check names 30 on a fresh install and 90 after PROFILE-4 instead of a per-profile default; the step now runs `/lh resetall` first so "defaults" is reachable. Verified with a headless probe of `Sl:CliList`) |
| §1 :98-102 | Disable is total: window closes, no capture, /lh show refusal line | STATE-1 |
| §1 :102-104 | Minimap button while disabled: left-click opens settings, right-click menu with Enabled live | LAUNCH-5 |
| §1 :105-110 | Command surface while disabled; only show/hide/toggle/test/purge refuse | STATE-2 |
| §1 :111-114 | /lh enable; the checkbox, verb and get agree (one switch, three surfaces) | STATE-3 (old "and the window opens" corrected: NS.StandUp, core/LifecycleSetup.lua:110-118, re-enables the modules and opens nothing, and B:ApplyVisibility, modules/Browser.lua:1174-1178, only hides; the check now expects `/lh show` to open it again) |
| §1 :115-118 | Untick within 5s of login writes nothing (deferred prune/repair) | STATE-4 (ends by re-ticking the box: old § 1 ran it last, but in the STATE theme STATE-5 to STATE-11 follow it and the COMMANDS gate, settings/Slash.lua liveVerbs, refuses show/toggle/test while disabled) |
| §2 :128,137-138 | toggle/show/hide; opens on History; last tab remembered | HIST-1 |
| §2 :130,139-140 | ESC closes the window and an open filter dropdown | HIST-2 |
| §2 :131-133,141-143 | Position, size (min width) and 1.3x scale persist across /reload | HIST-4 (step path corrected: `/lh set settings.windowScale 1.3`. The CLI resolves exact row paths only, libs/LibKa0s/Schema.lua:330-333 FindRow reads `index[path]`, so the old `/lh set windowScale 1.3` printed `Setting not found: windowScale` and wrote nothing) |
| §2 :134,144 | Window usable in combat, no blocked-action error | COMBAT-1 |
| §2 :144-145 | /lh config is the only combat-blocked path | COMBAT-2 (the old paraphrase "can't open in combat" replaced by the printed line, libs/LibKa0s/Options.lua:200 COMBAT_REFUSED, printed by OptionsRegistry.lua:253: `cannot open settings during combat — Blizzard's category-switch is protected`) |
| §3 matrix row 1 | Kill → Kill, CERTAIN | CAP-1 |
| §3 matrix row 2 | Container → Container, CERTAIN | CAP-2 |
| §3 matrix row 3 | Quest reward → Quest, CERTAIN | CAP-3 |
| §3 matrix row 4 (F-001) | Vendor buy → Vendor | CAP-4 |
| §3 matrix row 5 (F-001) | Mail attachment → Mail | CAP-5 |
| §3 matrix row 6 (F-001) | Trade → Trade | CAP-6 |
| §3 matrix row 7 | M+ chest → Mythic+ | CAP-7 |
| §3 matrix row 8, :176-177 | Bonus roll → Bonus Roll, overriding stale context | CAP-8 |
| §3 matrix row 9, :181-186 (F-009) | Roll win → Roll via the roll-won stamp line | CAP-9 |
| §3 matrix row 10, :176-177 | Craft → Craft, overriding stale context | CAP-10 |
| §3 matrix row 11, :177-181 | Currency refund → Refund currency row, src=REFUND | CAP-11 |
| §3 matrix row 12, :203-204 | Currency loot → Currency row, [Currency] debug line, Type filter | CAP-12 |
| §3 :187-191 | Keystone context clears on leaving / reset; re-armed on re-entry | CAP-14 |
| §3 :192-197 | Boss-corpse loot keeps its encounter (grace window, sourceDetail) | CAP-15 |
| §3 :198-199 | Unattributable loot → Other, INFERRED, never an error | CAP-16 |
| §3 :200-202 | Denormalized columns render (link, quality, iLvl, bound, prices, character) | CAP-17 |
| §3 :204-205 | Record currency off and source mute stop currency rows | CAP-13 (ends by unmuting the source, so CAP-14 to CAP-16 loot is not dropped as `source`) |
| §3 :205-207 | Insights Currency block from a currency loot | INS-20 |
| §3 :207-209 (F-010) | Currency category (SubType) resolves to a real header | CAP-18 |
| §3 :210-215 (S-003) | Currency first seen mid-session gets its category; collapsed-header record | CAP-19 |
| §3 :216-220 | Currency quality color, Quality label and currency tooltip | CAP-20 |
| §3 :221-224 | Currency bound glyph at capture | CAP-21 |
| §3 :225-229 | v3→v4 currency quality backfill | INSTALL-6 |
| §3 :230-233 | v4→v5 currency bound backfill | INSTALL-7 |
| §3 :235-238 (field note) | Historical sign-off record; its owed items carried as CAP-18, CAP-21, INSTALL-7, INS-20 | dropped: filled-in historical sign-off record (D4); owed items carried to Pending sign-off |
| §4 quality | Minimum quality gate, [Drop] quality | CAP-22 (ends by setting Common back: gateReason, modules/Collector.lua:35-39, checks quality before source and quest, so a Rare threshold would turn CAP-23's `quest` and CAP-24's `source` drops into `quality`) |
| §4 quest items | Quest-class gate, reason=quest | CAP-23 |
| §4 source mute | Source mute, reason=source; every source offered | CAP-24 |
| §4 :261-262 | Gates react live without /reload | CAP-22 |
| §5 sort | Every column sorts both ways | HIST-5 |
| §5 group by | Every group mode, collapse/expand, order | HIST-6 |
| §5 filters + footer | Filters narrow rows, "N selected", Showing X of Y | HIST-7 |
| §5 :298-300 | Database ≈ size footer | HIST-8 |
| §5 zone filter :277-281 | Zone filter one entry per name, Unknown bucket | HIST-9 |
| §5 :282-284 | Saved view upgrade v7→v8 keeps zones by name | INSTALL-8 |
| §5 bound filter | Bound filter five options, legend and lock colors match | HIST-10 |
| §5 search | Search matches names; clearing restores | HIST-11 |
| §5 row actions :290-291,302-304 | Row menu Link to chat / Delete, shift-click, hover, dense delete | HIST-15 |
| §6 save | Save stores the view including Bound | HIST-18 |
| §6 clear | Clear returns to saved view + current player | HIST-18 |
| §6 reset | Reset drops to stock defaults | HIST-18 |
| §6 :326 | Bound selection survives Save → Clear → reload | HIST-18 |
| §6 :327-331 | Opens on saved view + Character: Current, even with no loot | HIST-19 |
| §6a :337-341 | Export is tab-aware (Export History / Export Insights) | HIST-24 |
| §6a :351-362 | History CSV header and column formats | HIST-25 |
| §6a :363-375 | Insights CSV sections mirror the panel | HIST-26 (every clause kept: the section list, `Ng Ns Nc` values, the `Char / Category` companion rows with the value on By Character x Source, items-only loot sections so a character's total tallies, and the absent sections; modules/Export.lua:19-24 money, :178-202 charMatrix, :224 the value matrix) |
| §6a :376-377 | All Data vs Current View honor the shared filter | HIST-27 |
| §6a :378 | Auto-highlight, Ctrl+C, Esc | HIST-29 |
| §6a :379 | Modal and copy window centered on the History window | HIST-24 (the modal), HIST-28 (the copy window) |
| §7 :390-394 | Shared filter scopes all cards and charts; empty state | INS-1 |
| §7 :395-397 | KPI cards populate; derived value | INS-2 |
| §7 :398-401 | Headline font parity, one line | INS-3 |
| §7 :402-403 | Smaller coin glyphs | INS-4 (expectation corrected by SP-LH-03R: the old "~25% smaller than before" meant the previous default glyph, and the first rewrite made it "25% smaller than the text's line", which the code does not do. modules/Analytics.lua:210-212 passes a fixed `COIN_H = 10` to `GetCoinTextureString`, about 25% under the client's default of about 14 px, so the check compares against the History Vendor/AH cells, which call `NS.Util.FormatMoney` with no height, modules/BrowserTable.lua:220 and :224; the bars and rows use GameFontHighlightSmall, :250-290, and the KPI cards GameFontNormalHuge, :435) |
| §7 :404-405 | Bigger, thicker section dividers | INS-5 |
| §7 :406-409 | Title Case and renamed titles | INS-6 |
| §7 :410-418 | LOOT chart order; retired charts gone | INS-7 |
| §7 :419-422 | × Character companions; empty companion hides | INS-8 |
| §7 :423-425 | Per-category bar colors | INS-9 |
| §7 :426-428 | Bar-colored labels | INS-10 |
| §7 :429-432 | Palette non-adjacency | INS-11 |
| §7 :433-435 | Companion segment order | INS-12 |
| §7 :436-439 | Legends under every categorical chart, aligned | INS-13 |
| §7 :440-442 | Legend label truncation + hover | INS-14 |
| §7 :443-447 | Totals tally, items-only LOOT | INS-15 |
| §7 :448-451 | Row label truncation + tooltip | INS-16 |
| §7 :452-457 | Every tooltip carries its value | INS-17 |
| §7 :458-459 | Cursor-anchored tooltips | INS-18 |
| §7 :460-462 | Per-segment tooltips | INS-19 (chart names now as drawn: "Currency By Type × Source", "Currency By Character × Type", modules/Analytics.lua:599-600) |
| §7 :463-474 | CURRENCY block layout; hides with no currency in range | INS-20 (chart names now as drawn, modules/Analytics.lua:598-601, including "Currency Over Time (Per Day)") |
| §7 :475 | Cards update live on loot | INS-21 |
| §8 :483,485 | /lh test on/off; window opens / stays closed | STATE-7 |
| §8 :486-488 | Test mode box: tick, untick, /lh test unticks it | STATE-9 |
| §8 :489,496-497 | Combat start ends test mode | COMBAT-6 |
| §8 :490,498 | Visibility Never refuses test mode; set it back to Always | STATE-10 (the set-back step restored by SP-LH-03R: testModeRefusal, modules/BrowserTable.lua:544-551, would otherwise refuse STATE-11's start) |
| §8 :491,499 | /lh test in combat refused | COMBAT-7 |
| §8 :492,500 | Reset all settings leaves test mode off | STATE-11 |
| §8 :501-506 | Test mode badge, synthetic data, filters rebuilt; off returns live | STATE-8 |
| §8 :493,507 | Test mode not persisted across /reload | STATE-11 |
| §9 setup :514-515, :595-597 | /lh config and Esc → Options reach the same category | PANEL-1 |
| §9 strip :518-526 | Six tabs, order, shared with Bank Ledger, headings | PANEL-3 (AH Price's Pricing and Price sources headings kept; Interface's Window and Minimap subsection headings dropped: no longer exist, settings/Schema.lua:345-349 removed them and the Minimap button row moved to Master controls) |
| §9 strip :526-528 | Wrapped strip: controls start below; same row height | PANEL-4 |
| §9 master :529 | Enable Loot History and /lh get agree | STATE-3 |
| §9 master :529-531 | General visibility Never refuses /lh show | STATE-5 ("set Always → the window opens" corrected: B:ApplyVisibility, modules/Browser.lua:1174-1178, only hides, so the check expects a second `/lh show` to open it) |
| §9 master :531-533 | Only out of combat hides at combat start, no reopen | COMBAT-5 |
| §9 master :533-535 | Master scale and Master alpha | PANEL-7 |
| §9 master :535-537 | Lock frame stops drag and resize; size kept on reload | STATE-6 |
| §9 :538-540 | Window scale slider 0.05 steps; set moves slider | PANEL-8 (the slider steps); the "set moves the slider" half is SLASH-4, whose step now uses the full path `settings.windowScale` (the short `windowScale` answers `Setting not found`, libs/LibKa0s/Schema.lua:330-333) |
| §9 :541-544 | Row height slider | PANEL-9 |
| §9 :545-547, :578-579 | Panel writes and /lh set write the same value, live both ways | SLASH-4 (step path corrected to `/lh set settings.windowScale 1.5`; the old short path wrote nothing, libs/LibKa0s/Schema.lua:330-333) |
| §9 :548-553 | History tab readout, Purge only, live count across tab clicks | PANEL-10 |
| §9 :554-556 | Reset position / Reset all settings pair | PANEL-11 |
| §9 :557-560 | Filters secondary strip, one add box, remembered sub-tab | FILT-1 |
| §9 :561-564 | AH Price tab no freeze, pooled rows | PANEL-17 |
| §9 :565-569, :587-589 | Debug console checkbox reflects window (ticks when /lh debug opens it, unticks when /lh debug or Esc/✕ closes it), session-only, syncs | DIAG-9 |
| §9 :570 | Minimap button pointer ("walked in §11") | dropped: pointer, not a check (LAUNCH-7) |
| §9 :571 | Test mode pointer ("walked in §8") | dropped: pointer, not a check (STATE-9) |
| §9 :572, :580-586 | /lh list groups in strip order; every schema row | SLASH-3 |
| §9 :573, :590-591 | Out-of-range clamps; non-number rejected | SLASH-5 (steps corrected to `settings.windowScale`: with the old short path both lines printed `Setting not found: windowScale`, so the clamp and the refusal were never reached. A headless probe of the corrected steps prints `settings.windowScale = 1.60x` for 9, `Invalid value for settings.windowScale` / `expected a number` for abc, libs/LibKa0s/Slash.lua:48 and :54, and `expected true/false/on/off/1/0/yes/no` for `settings.enabled maybe`) |
| §9 :574, :592-594 | /lh reset <path> one row, deep copy | SLASH-6 |
| §9 :575, :595-597 | Mid-combat /lh config refused; out of combat opens | COMBAT-2 (the printed line, as in the §2 row) |
| §10 :607, :616-618 | Scrollbar always shown, grayed on a short page | PANEL-15 (landing page and General only, as the old check had it. Profiles is not in it: settings/Profiles.lua:49-54 renders AceConfigDialog into an AceGUI SimpleGroup inset 8px, AceConfigDialog makes no ScrollFrame for a SimpleGroup, and the page never calls O.EnsureScroll, the one caller of PatchAlwaysShowScrollbar, libs/LibKa0s/Options.lua:849. The check says so in a note) |
| §10 :608-610, :619-622 | Paired buttons draw full right border | PANEL-16 |
| §10 :611, :623-624 | Purge confirm; Cancel/Accept | PANEL-13 |
| §10 :612, :625-628 | Reset all settings canonical confirm; history untouched | PANEL-12 |
| §10 :629 | Reset position raises no dialog, touches no setting | PANEL-11 |
| §10 :613, :630 | /lh purge raises the same dialog | PANEL-13 |
| §11 :644, :659-660 | AddOns list, minimap and broker show the addon's logo | LAUNCH-1 |
| §11 :645, :661-665 | Tooltip block order; Locked/Test mode live | LAUNCH-2 |
| §11 :646, :666 | Left-click opens Settings in either state | LAUNCH-3 |
| §11 :646-647, :667-675 | Right-click menu four checkboxes; each acts once and the menu closes | LAUNCH-4 |
| §11 :648-649, :676-680 | Disabled tooltip and grayed menu; Enabled brings it back | LAUNCH-5 |
| §11 :654-655, :681-684 | Dragged position persists; rename does not move it | LAUNCH-6 |
| §11 :650, :685-686 | Minimap button toggle hides at once, persists | LAUNCH-7 |
| §11 :651-652, :687-690 | get minimap.shown false; Reset all keeps hidden; reset row restores | LAUNCH-8 |
| §11 :653, :691-692 | /lh set minimap.hide true answers Setting not found | dropped: asserted by tests/test_slash.lua "/lh get minimap.shown reads the row's SHOWN sense; the old minimap.hide path is unknown" |
| §11 :656, :693-694 | Broker row answers the same clicks and menu | LAUNCH-9 |
| §11 :695-696 | Hiding the minimap button keeps the broker row | LAUNCH-10 |
| §12 :704, :723 | Bare /lh debug toggles the window only | DIAG-1 |
| §12 :705-706, :724-726 | Logging on/off; [Loot]/[Drop]; captured while hidden | DIAG-2 |
| §12 :727-729 | Chat ack colors; [Debug] enabled/disabled lines | DIAG-3 |
| §12 :707, :730-731 | Copy, Clear, ESC; header toggle same flag | DIAG-4 |
| §12 :708-709, :717-719 | Scrollbar and mousewheel in sync; thumb positions | DIAG-5 |
| §12 :709-712, :720-722 | Line counter, Clear resets, cap at 3000, Copy at cap | DIAG-6 |
| §12 :713, :732-734 | /lh debug events: none; registrations back after disable/enable | DIAG-7 |
| §12 :714, :735 | After /reload logging off, console closed | DIAG-8 |
| §12a step 1 | Report with trace above, markers, one chat line | DIAG-19 |
| §12a step 2 | Pasted report has no escapes | DIAG-20 |
| §12a step 3 | Report lands with logging off; no trace after | DIAG-21 |
| §12a step 4 | /lh debug diagnostics and /loothistory forms | DIAG-22 |
| §12a step 5 | /lh diag, /lh dump, /lh debug diag are not aliases | DIAG-23 |
| §12a step 6 | Report while disabled; identity and capture lines | DIAG-24 |
| §12a step 7 | Report in combat: <secret>/?, no failed section | COMBAT-8 |
| §12a step 8 | README Reporting a bug steps work word for word | DIAG-25 |
| §13 :780, :788-791 | Shorter retention confirm; No keeps and prints one line | CAP-28 |
| §13 :781, :792-793 | Yes prunes (no holes); table and footer refresh | CAP-30 (moved after the slash check: once Yes has pruned to 7 days, `NS.Database:CountOlderThan(7)` is 0, so `S:OnRetentionChanged`, settings/Schema.lua, sets the value silently and no later confirm can appear; 7 is the smallest `C.RETENTION_OPTIONS` value) |
| §13 :782, :794-795 | /lh set retentionDays shows the same confirm; no-op asks nothing | CAP-29 (runs before the Yes prune and answers No, so the older records are still there and the decline prints `retention kept at 90 days; no records were deleted.`, `S:ConfirmRetention`; the no-op is `/lh set settings.retentionDays 0`, since `CountOlderThan(0)` is always 0) |
| §13 :785, :796-797 | PruneOld ~5s after login | CAP-31 (given a runnable setup: after CAP-30 no record is older than the retention, so a `/run` subtracts 8 days from the last record's `ts` in `LootHistoryDB.global.history`; the login prune, core/LootHistory.lua `NS.After(5, …)` into `Database:PruneOld`, then drops it and the count falls by one) |
| §13 :798 | Always keeps everything | CAP-32 |
| §13 :783-784, :799-800 | Retention account-wide across profile switch/copy/reset; tooltip | PROFILE-4 |
| §14 :804-817 | SavedVariables after logout: schemaVersion 10, dense history, scopes, session state absent | INSTALL-5 |
| §15 :824-825 | [Init] line on enable, not at login | DIAG-3 |
| §15 :826 | One [Loot] / one [Drop] | DIAG-2 |
| §15 :827 | One [Open] per LOOT_OPENED | DIAG-12 |
| §15 :828 | One [Set] per setting, no [Cfg] | DIAG-13 |
| §15 :829 | Defaults / footer / resetall bulk reset is one line; reset <path> one line | DIAG-14 |
| §15 :830 | [Data] purge/delete lines; Reset all settings one [Set] line | DIAG-15 |
| §15 :831 | [UI] window shown, tab -> Insights, [Insights] computed | DIAG-16 |
| §15 :832 | One [Table] rendered per change | DIAG-17 |
| §15 :833 | One [Filters] line per list edit | DIAG-18 |
| §16 :842-845, :877-879 | Blacklist item from a row: route in chat, row stays; Blacklist currency names Currencies | FILT-2 |
| §16 :846-848 | Filters tab opens on Blacklist, three-tab sub-strip, one list | FILT-1 |
| §16 :849, :880-881 | Blacklisted item records nothing new, reason=blacklist | FILT-3 |
| §16 :850, :882-884 | X removes; nothing comes back; future loot records | FILT-4 |
| §16 :851-853, :885-886 | Whitelist records despite the gates; one add box | FILT-5 |
| §16 :854, :887-889 | Removing from the whitelist keeps rows | FILT-6 |
| §16 :855, :890 | Adding to one list removes it from the other | FILT-7 |
| §16 :890-894 | Entry layout: X left, icon, name, id, Unknown item, tooltip, (none) | FILT-8 |
| §16 :856-857, :895-896 | Add by name (any case) and by shift-clicked link | FILT-9 |
| §16 :858-860, :897-902 | Suggestions dropdown, ranks with tier icons, keys | FILT-10 |
| §16 :861, :903-908 | Shared name without a pick adds nothing (bags too) | FILT-11 |
| §16 :909-910 | Arrow then type then Enter submits the text | FILT-12 |
| §16 :862-863, :911-912 | Item not carried but in history/list resolves by name | FILT-13 |
| §16 :864-865, :913-916 | Unknown item refused with the orange line and tooltip | FILT-14 |
| §16 :866, :917-918 | Garbage input refused, text kept, nothing in chat | FILT-14 |
| §16 :867-870, :919-923 | Currencies: id, link, looted name, unknown refused | FILT-15 |
| §16 :924-925 | Delete is the only way to remove stored rows | FILT-17 |
| §16 :926 (per profile) | Lists are per profile and survive /reload | PROFILE-5 |
| §16 :926-927 | No blacklist/whitelist option in the browser's filter dropdowns | FILT-17 |
| §16 :871-873, :928-931 | Refresh perf: re-opening Filters and sub-tabs is instant | FILT-18 |
| §16 :873-874, :931-933 | Off-screen blacklist add repaints once on next show | FILT-19 |
| §16 :935-941 | Currency blacklist flow and Clear all | FILT-16 |
| §17a.1 | Degraded: zero Lua errors | DEGRADED-1 |
| §17a.2 | Degraded: /lh list complete | DEGRADED-2 (old expectation was stale: the degraded Sl.CliList, CliGet, CliReset and CliVersion are the `unavailable` function, settings/Slash.lua:152-154 and :227, and the degraded CliSet falls through to it for any path but `settings.enabled`, :241-245. The check now expects that line. Only the `set` half is pinned headlessly, tests/test_slash_degraded.lua "library-less install: set on any other path, or a non-bool value, stays unavailable"; nothing pins the line for list, get, reset or version, so the in-client check carries them) |
| §17a.3 | Degraded: missing-library notice once | DEGRADED-3 |
| §17a.4 | Degraded: debug/config/diagnostics unavailable lines; help omits diagnostics | DEGRADED-4 |
| §17a.5 | Degraded: capture records, zone stamped, version answers | DEGRADED-5 (the "/lh version prints the TOC version" clause dropped: no longer true, the degraded CliVersion is the unavailable line, settings/Slash.lua:227. No headless case pins that line; DEGRADED-2 checks in the client what version prints) |
| §17a.6 | Degraded: filter bar absent, not dead | DEGRADED-6 |
| §17a.7 | Degraded: export modal refuses | DEGRADED-7 (old "if you have another route" replaced by a real one: NS is the AceAddon object, core/LootHistory.lua:4, so `/run LibStub("AceAddon-3.0"):GetAddon("LootHistory").Browser:OpenExport()` calls the button's handler; also asserted headlessly by tests/test_widgets.lua "degraded install: the export modal refuses …" and "… builds no frame, on the first Open or the tenth") |
| §17a.8 | Degraded: enable/disable work; help lists them, not set | DEGRADED-8 |
| §17a.9 | Degraded: resetall empties the lists | DEGRADED-9 |
| §17a.10 | Rename the folder back (instruction) | dropped: setup instruction, not a check; kept in the Degraded install intro |
| §17b :1008-1010 | Help header and rows are prose, no HELP_HEADER | SLASH-2 |
| §17b :1011-1012 | list/get/set refusal/reset/resetall output has no raw keys | SLASH-8 |
| §17b :1013-1015 | Console strings: title, toggle, buttons, status, copy title | DIAG-11 |
| §17b :1016-1017 | Panel labels English, Defaults reads Defaults | PANEL-19 (the four pages are now General and Profiles; Profiles has no Defaults button, settings/Profiles.lua defaultsButton = false, so the Defaults clause is General only) |
| §17c.1-2 | Landing page logo, tagline, Slash Commands, row format | PANEL-2 |
| §17c.3 (header) | General header, gold divider, Defaults button | PANEL-3 |
| §17c.3 (per-tab pairing) | Two-column pairing on each tab | PANEL-5 |
| §17c.4 | Scrollbar grayed/live; body right edge does not shift | PANEL-15 (landing page and General; see the §10 row for why Profiles is not in it) |
| §17c.5 | AH Price no freeze after merge (pooled rows) | PANEL-17 |
| §17d.1 | Blizzard footer Defaults control resets like the header button | PANEL-14 |
| §17d.2 (sidebar in combat) | Gray cover, one notice, clicks inert, Esc closes | COMBAT-3 |
| §17d.2 (/lh config in combat, nothing replays) | /lh config refuses; nothing replays after combat | COMBAT-2 |
| §17d.2 (open then pull; lifts) | Cover drops on an open page and lifts after combat | COMBAT-4 |
| §17d.3 | Checkbox ticked while /lh debug has the console open; Esc/× unticks it | DIAG-9 |
| §17e | Console chrome: border, gold title, three icon buttons; regression note | DIAG-10 |
| §17f purge | /lh purge and Purge history… raise the same popup | PANEL-13 |
| §17f reset all | Reset all settings canonical popup; Cancel | PANEL-12 |
| §17f clear all | Each list's Clear all has its own popup | FILT-24 (Blacklist, Whitelist), FILT-16 (Currencies) |
| §17f Defaults | Page Defaults clears all three lists | PANEL-14 |
| §17f resetall | /lh resetall is non-destructive and does not ask | SLASH-7 |
| §17g close mark | Title-bar close mark on all four windows | HIST-22 |
| §17g chevrons | Every dropdown ends in a gray centered chevron | HIST-13 |
| §17g export marks | Export and Export to CSV marks, label centered | HIST-22 (old text gave the filter bar's Export a mark; stale, modules/Browser.lua:752-757 "NO MARK ON THIS ONE"; HIST-22 now expects no mark on Export and the spreadsheet mark on Export to CSV only, modules/Export.lua:486) |
| §17g Clear/Reset/Save | No marks on Clear/Reset/Save | HIST-22 |
| §17g sort + group | Shared sort arrow; group chevrons not +/- | HIST-5 |
| §17g Bound padlock | Bound column padlock matches its legend | HIST-23 |
| §17g multi-select tick | Tick beside selected multi-select rows | HIST-17 |
| §17g row menu marks | Four row menu items: chat mark, two prohibition marks, clear mark on Delete; words kept | HIST-15 |
| §17g resize grip | Blizzard ChatFrame grabber, not a catalog mark | HIST-23 |
| §17g JetBrains Mono | Console and export copy box in JetBrains Mono | DIAG-11 |
| §17g regression note :1125-1130 | Blank space where a mark belongs is the failure | HIST-22 |
| §17g ladder note :1131-1135 | Blizzard art returning means the library is missing | DEGRADED-11 (limited to what an install with libs/LibKa0s renamed away draws: the client lock atlas in the Bound column, modules/BrowserTable.lua:79-91; Blizzard's sort arrows, :259-260; the thin text × close, core/CoreSetup.lua:53-68. The old note's dropdown arrow, `+`/`-` headers, tick and proportional console font are not observable there: DEGRADED-6 has no filter bar, so no dropdowns, ticks or Group by, and DEGRADED-4 has no console window, core/DebugLogSetup.lua:59. HIST-22's pointer to it now names the text × close) |
| §17g not-a-regression note :1136-1140 | Minimap/TOC icons and panel widgets out of scope; Save has no mark | dropped: scope note, not a check (Save's missing mark is in HIST-22) |
| §17h.1 | First Group by click opens a menu, no Font not set error | HIST-12 |
| §17h.2 | All ten dropdowns open, anchored, wide enough | HIST-13 |
| §17h.3 | One menu at a time; click-away; click lands on window | HIST-14 |
| §17h.4 | Escape closes window and menu | HIST-2 (in the LibKa0s re-vendor line of "Which themes to run", as old §17 was mandatory for every library edit) |
| §17h.5 | /lh hide closes the open menu too | HIST-3 (in the LibKa0s re-vendor line of "Which themes to run", as HIST-2) |
| §17h.6 | Export modal × and Escape close the Data set menu | HIST-33 |
| §17h.7 | Character: Current preset lights gold; one-click select | HIST-20 |
| §17h.8 | Selected character with no rows still shows its name | HIST-21 |
| §17h.9 | Rows: class icon, class color, tick, no empty box | HIST-17 |
| §17h.10 | Row menu unchanged, disables; filter menu + right-click row is one press | HIST-16 |
| §17i.1 | /lh version follows the TOC's ## Version | SLASH-9 |
| §17i.2 | Zone and subzone stamped; zone without subzone | CAP-25 (old text said the tooltip/export carries the subzone; neither does, BrowserTable.lua row OnEnter and Export.lua:80, so the subzone is read with /dump) |
| §17i.3 | Loading-screen zone buckets under Unknown | CAP-26 |
| §17i.4 | Map id stamped (old text said the export carries it; Export.lua:80 does not export mapID) | CAP-27 |
| §17j.1-2 | Copy window centered on History window, above modal, preselected | HIST-28 |
| §17j.3-4 | Ctrl+C whole CSV; Esc leaves the modal open | HIST-29 |
| §17j.5 | Same window reused from Insights | HIST-30 |
| §17j.6 | Copy window follows a dragged History window | HIST-31 |
| §17j.7 | Centers on screen with the History window closed | HIST-31 (route spelled out: open the modal, `/lh hide`, which hides only the History window and its menu, modules/Browser.lua:1198-1205, and leaves the modal up because it is parented to UIParent, modules/Export.lua:432; then Export to CSV, and libs/LibKa0s/Widgets.lua:601-605 falls back to screen center) |
| §17j.8 | Drag the copy window; shared close mark | HIST-32 |
| §17k | Pooled tab strip: labels, selection, band height over three passes | PANEL-6 |
| §17l | AH Price tick/ban/ⓘ catalog marks and their state | PANEL-18 |
| §18a | Six warband globals recorded | LOC-1 |
| §18b | Bind classification on deDE/frFR | LOC-2 |
| §18c | Auction-House mail attribution | LOC-3 |
| §18d | Deconstruct name family (mass variants) | LOC-4 |
| §18e | Walk § 1, § 3 and § 5 on the client | LOC-5 (INSTALL-1 to 4, SLASH-1 to 3, STATE-1 to 4, LAUNCH-5, CAP-1 to 21, INSTALL-6, INSTALL-7, INS-20, HIST-5 to 11, HIST-15, INSTALL-8: every new ID old § 1, § 3 and § 5 map to) |
| §19 :1406-1408 | Blacklist two to a line, aligned | FILT-20 |
| §19 :1409-1410 | Odd count: last entry left, space right | FILT-21 |
| §19 :1411 | Whitelist two to a line | FILT-20 |
| §19 :1412-1414 | Currencies two to a line | FILT-20 |
| §19 :1415-1419 | Long names truncate; hover names the item | FILT-22 |
| §19 :1420-1421 | Remove/add repacks the grid | FILT-23 |
| §19 :1422-1426 | Narrow canvas falls back to one column; widen restores | FILT-23 |
| When to run :1431-1465 | Subset-to-section guidance (not a check) | dropped: guidance, not a check; rewritten as "Which themes to run" under Before you start |
