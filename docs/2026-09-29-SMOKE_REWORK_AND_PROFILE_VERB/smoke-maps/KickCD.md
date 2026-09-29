# Smoke map — KickCD (SP-KC-03)

Old `docs/smoke-tests.md`: 1165 lines, 45 section headings (§1 – §36 with 7a – c, 9b, 9c, 20a – d; its
index skipped 28 – 35), mapped here in 279 rows (a bullet, table row or numbered step each; adjacent
bullets that state one behavior share a row). New: 966 lines, 226 checks in 14 themes (INSTALL 14,
SLASH 13, PANEL 29, PROFILE 14, STATE 15, COMBAT 11, GRID 14, CAST 14, FOCUS 19, LABEL 15, SPELLS 16,
DIAG 33, DEGRADED 13, LOC 6). Dropped: 2, both checks of things that no longer exist. Eight checks are
new: PROFILE-9 – 14 and DEGRADED-10 (the `/kcd profile` verb), and CAST-14 (an empowered cast, which
`docs/midnight-quirks.md` pointed at as a nonexistent "smoke C-03 step 4").

Pending sign-off follows the clarified rule (spec S4, 2026-09-29). The old doc had no `Result:` lines
at all, so a carried-over check is owed unless an owner run records its pass. Three do: on 2026-09-26
§36's KC-S1 – 11 (`2026-09-26-NAVRAIL_ADOPTION/99_REPORT.md` and `06_SMOKE_TESTS.md`) and §35's
diagnostics checks (`2026-09-25-DIAGNOSTICS_COMMAND/99_REPORT.md` § 6, KC-S1 – S9, S11, X1), and on
2026-09-25 the collection-wide minimap re-run (`2026-09-23-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/
06_SMOKE_TESTS.md` X1.4, "Recorded 2026-09-25: PASS (after M6)": left-click opens settings, right-click
opens the options menu, the M5 status tooltip, in every addon), which covers §33 L981 – 984. The checks
those passes cover whole and whose expectation this rework left alone are signed and not listed:
INSTALL-11, PANEL-4 – 7, COMBAT-4, COMBAT-11, GRID-14, DIAG-27, DIAG-31 – 33, DEGRADED-9 (DIAG-31's quote
now carries the `, holds=…` tail its line always printed, which changes nothing observed). A check that
merged a passed step with an unrun one (INSTALL-12, STATE-9, PANEL-1, PANEL-3, PANEL-12, PANEL-17, SLASH-9, FOCUS-6, FOCUS-7,
DIAG-17, DIAG-28, DIAG-30) is listed for its unrun half. DIAG-28's recorded passes are KC-S2 (the trace above
the begin marker) and KC-S4 (both markers, no `|c` escapes), and DIAG-30's is KC-S5 (full report, `Debug: OFF`);
none of those rows points at §35 or records the console opening, the chat count line, the agreeing counts
or the untraced target change, so those halves stay owed. The rest are listed with why: no result recorded; §31 and §32's
NOT YET RUN (CAST-13, DEGRADED-11, DEGRADED-6's before-the-dump half); never run per the 2026-09-07
checklist (`2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/08_SMOKE_CHECKLIST.md`, "Nothing below has
been run": §14 sidebar → COMBAT-3, §15 → COMBAT-9, §27 → PANEL-19 – 22, §28 → PANEL-24 and DIAG-26,
§29 → PANEL-23, §30 → DIAG-23 – 24, §12 resetposition → STATE-10, §25's `L` trap → PANEL-28, §9b →
LOC-1 – 6); new; or corrected against the code. 213 of the 226 IDs are listed. The 2026-09-23 plan's
Session KC records no KickCD result (its only KickCD-relevant pass is X1.4 above), and the 2026-09-22 sweep's
"20 passed" names no KickCD check. The closing "When to run which
subset" list is guidance, not checks; it became "Which checks to run" under Before you start, with every
old entry's section numbers translated to the IDs they map to below (re-vendor, hot paths, debug console,
perf and media seam included), so no entry runs fewer checks than before. The SP-KC-03R review
re-derived each entry from the rows below and added what the first pass missed: COMBAT-6 (re-vendor,
§34), CAST-8 and SLASH-4 (target and focus, §7a and §7b), DIAG-28 (printer and debug console, §15),
and SPELLS-11 – 12 and DIAG-8 (a new schema row, §12). Rows ending "(clean-run rule)" are "no Lua errors" bullets now carried by Before you
start's rule that a clean run means no error at any point.

Stale items fixed on the way: the six-page settings tree (§1, §2, §14) is now General · Grid · Spells ·
Profiles, and §14's sidebar check covers the Ka0s KickCD page and four subpages, not six; §32's `units.target.visibility` is the
top-level `visibility`; §27's "`/dump` reports 3" now expects the vendored `COMPOSE_MINOR` (7 at
v1.63.0) instead of a number that goes stale on every re-vendor; §12's "mirrors `/kcd reset <panel>`"
named a retired form; §15's "no General → Debug checkbox" predates the session-only Debug console row
on Master controls, so DIAG-3 now says no saved setting holds the logging flag. §12 L360 quoted the
Reset all tooltip with `→`; the vendored `RESET_ALL_TIP_PROFILES_PAGE` (`libs/LibKa0s/Options.lua`)
says `Profiles -> Reset Profile`, and PANEL-18 now quotes that. §13's copy step copied into the
per-character profile; PROFILE-2 copies into a scratch `SmokeCopy`, so `Default` keeps its own
`primarySize` and PROFILE-10's `/kcd profile` switch shows a visible change (64 → 40). Old §20a assumed
Focus started off; Focus is on by default now, so STATE-4 and FOCUS-2 turn it off first. FOCUS-2 also
runs `/kcd unlock` before the enable: a locked cast bar hides whenever no cast is live
(`modules/Castbar.lua` `ApplyLock`, `Stop`), so the old "builds" only shows as the bar's placeholder
while unlocked; FOCUS-3 locks again, since unlocked bypasses visibility. §28's quote of the pre-respell perf strings is gone (DIAG-26 says "one L"), so
`tests/prose_waivers.lua` loses its `docs/smoke-tests.md` entry.

Corrected against the code in the third SP-KC-03R pass (every expected string re-read against the
source and the vendored `libs/LibKa0s`; each is under Pending sign-off). The Slash CLI echoes a number
through its row's `fmt` and a color as `{r, g, b, a}` (`libs/LibKa0s/Slash.lua` `FORMATTERS`), so
INSTALL-5, SLASH-11 and PROFILE-10 now expect `50 px`, `12 px`, `-1 px`, `-20 px`, `64 px` and
`{0.20, 0.80, 0.20, 1.00}` / `{1.00, 0.82, 0.00, 1.00}`; SLASH-5's `scale` row has no `fmt` (`scale = 2`,
not `2.00x`) and PANEL-15's slider reads 1.25; SLASH-6's "a component above 1 is clamped" was wrong
(`parseColor` switches the whole color to the 0 – 255 scale). SLASH-4's gate hint sits on the
`allowed values:` line and adds the flip hint (`settings/Slash.lua` `GateHint`). SLASH-9: `spells`
answers "has moved", not "is gone". GRID-2: the warning's text is `dropped <n> icon(s) past the
<cap>-slot grid for <CLASS>/<specID> …`, each unit warns for its own grid, and fitting re-arms it (the
old "once per session" was wrong, `modules/IconGrid.lua`); GRID-3's 16 → 80 is outside the row's 24 –
96. CAST-10's tooltip is titled `KickCD castbar` (`modules/Castbar_Handle.lua`). LABEL-6: the panel
slider has no `fmt`, so only the `/kcd get` echo reads `45 deg`.
DIAG-1 and DIAG-2 quote the dumps as printed (`[<id>] <name> ready=… cdObj=yes|nil …`, `isSecret=`);
DIAG-3's "`Ka0s_KickCD_*` traffic" is the `debug logging ON` ack and `[Tag]` lines; DIAG-11's lines
carry `[target]` and a stop reads `interruptible none (no hostile cast)`, not `off`; DIAG-13 names the
drag list's own `grab` / `drop` / `released` / `painted` lines; DIAG-16's label is `Debug: ON` /
`Debug: OFF`; DIAG-26: `/kcd perf start` always stamps a `YYYY-MM-DD HH:MM` label, so `unlabeled`
never shows, and the cancel line is `perf run CANCELED — nothing saved`. DEGRADED-8's perf line is
about performance measurement, not the capture. The same pass restored three halves the review found
lost: SLASH-10's free cast-bar anchor (§12 L358, L370), PROFILE-3's realm and class scopes (§13 L388),
and LABEL-12's Attach to `castbar` in Always mode (§22 L635).

Fourth SP-KC-03R pass (review of 2026-09-29). COMBAT-3 carried §14's refuse-and-close expectation, which
predates Options minor 22: `O.SetRenderer`'s OnShow (`libs/LibKa0s/Options.lua`) now covers a page shown in
combat (`coverOnShow`) and leaves the Settings window open, and `O.__combatRefused` prints the gray
`COMBAT_LOCKED_NOTICE` only once per combat (`combatNoticed`, reset in `onCombat`). COMBAT-3 now expects
each of the five pages under the "Settings are locked during combat." cover, one notice on the first, the
window open, and the page drawn when combat ends (`unlockPage`). COMBAT-5 asked for a click the client
cannot deliver: `onCombat` covers every page on screen at PLAYER_REGEN_DISABLED and `O.__buildCover`
(`libs/LibKa0s/OptionsCombat.lua`) makes the cover take the mouse over the whole panel, so the note's link,
and with it `Helpers.OpenPageTab`'s own combat refusal (`settings/Panel_Widgets.lua` `refusedInCombat`), is
unreachable in combat. COMBAT-5 is rewritten to what the cover does: the note is covered, the click opens
nothing and prints no refusal. Both stay under Pending sign-off.

Fifth SP-KC-03R pass (review of 2026-09-29). The rework had folded §12 L362 into PANEL-17, which checks
only the Grid page's Cast bar entry, so the "that panel only" half was lost for General and Icons. PANEL-29
restores it: General's Defaults (`H.RestoreDefaults("general")`, which walks `SchemaForPanel("general")`:
`enabled`, `visibility`, `scale`, `alpha`, `locked`, the units' enable rows and `units.focus.link`) must
leave an Icons row, a Cast bar row and the spell list alone, and Icons' Defaults
(`Helpers.RestoreGridSection`, `SchemaForPanel("icons", <band unit>)`) must leave `scale`, the Cast bar
row and the spell list alone. The echoes are the rows' `fmt` (`%d px`: `50 px`, `64 px`, `-30 px`); the
spell lists are not schema rows, so no page's Defaults reaches them. PANEL-29 is under Pending sign-off
(no result recorded). STATE-15's title now closes its bold after "(the default)", like every other check.

Inbound references updated: `docs/testing.md` (§25 → PANEL-28), `docs/debug.md` (section 35 →
DIAG-27 – 33, DIAG-17, COMBAT-11, GRID-14, DEGRADED-9), `docs/midnight-quirks.md` (C-03 step 4 → CAST-14),
`docs/common-tasks.md` (the waiver paragraph). Cross-addon citations of "KickCD § 9b" become
"KickCD LOC-1" (LOC-1 is the grid-populates check from §9b).

| Old location | Behavior | New ID |
|---|---|---|
| §1 L65 | Log in with zero Lua errors | INSTALL-1 |
| §1 L66 | Grid holds the spec's default, castable spells | INSTALL-2 |
| §1 L67 | Bare `/kcd` opens the landing page, no help list | SLASH-1 |
| §1 L68 | `/kcd help` banner and colors, no `schema error:` | SLASH-2 |
| Conventions L14 | Chat banner rule (no double or missing `[KCD]`) | SLASH-2 (and Before you start) |
| §1 L69 | Settings tree has six subcategories (stale: now General · Grid · Spells · Profiles) | PANEL-1 |
| §1 L70 | `KickCDDB` shape, numeric spec key | INSTALL-3 |
| §1 L71 | An alt's spec seeds on first profile creation | INSTALL-4 |
| §2 L89–93 | `/reload`: no error, position, lock, size, color persist | INSTALL-5 |
| §2 L94 | Six settings tabs after `/reload` (stale count) | PANEL-1 |
| §3 L105–106 | Master off hides both, on restores | STATE-1 |
| §3 L111–114 | Off is total: still loaded, nothing appears, lock unchanged | STATE-2 |
| §3 L115–116 | No `[Combat] entered` while off | STATE-3 |
| §3 L117–118 | Enable rebuilds, including a unit enabled while off (Focus turned off first, since it defaults on) | STATE-4 |
| §3 L119 | Enable checkbox follows a slash write | PANEL-14 |
| §4 L125 (first half) | Unlocked bypasses visibility | STATE-11 |
| §4 L125 (follow-up note) | Known non-interruptible leak at cast start | STATE-15 |
| §4 L129 | `always` | STATE-12 |
| §4 L130 | `in_combat` | STATE-13 |
| §4 L131 | `target_casting` | STATE-14 |
| §4 L132 | `target_casting_interruptible`, alpha fade on a mid-cast flip | STATE-15 |
| §4 L135 | No error at any visibility flip | STATE-12 – 15 (clean-run rule in Before you start) |
| §4 L136 | `debug interrupt` reports secret status and the gate decision | COMBAT-8 |
| §5 L140 | Fresh profile is unlocked and draggable | STATE-6 |
| §5 L151–153 | Unlock drags both, lock drags neither, positions survive `/reload` | STATE-7 (the `/reload` half: INSTALL-5 for the grid, CAST-8 for the cast bar) |
| §5 L154 | PRIMARY cast bar not draggable, follows the grid | CAST-6 |
| §5 L155 | `/kcd toggle` and the Lock frame box | STATE-8 |
| §6 L166 | Anchor × grow layout | GRID-1 |
| §6 L167–168 | Overflow warning, once per tuple | GRID-2 |
| §6 L169 | primarySize 16 → 80 live | GRID-3 |
| §7a L182 | Free cast bar position survives `/reload` | CAST-8 |
| §7a L183–184 | Bar follows a cast; name, time, spark | CAST-1 |
| §7b L196–197 | Auto-size tracks the visible grid, other side fixed | CAST-2 |
| §7b L198 (first half) | Orientation resets grow direction | CAST-3 |
| §7b L198 (second half) | Gated write names the sibling | SLASH-4 |
| §7c L209–210 | Per-state colors, uninterruptible red or faded | CAST-4 |
| §7c L211 | Mid-cast flip with no Lua-side branch | CAST-5 |
| §8 L223 | Desaturate, swipe, countdown on cast | GRID-4 |
| §8 L224 | GCD does not trigger the swipe | GRID-5 |
| §8 L225 | Primary and secondary glow triggers independent | GRID-6 |
| §8 L226 | Ready again, no stuck `0.0` | GRID-7 |
| §9 L238 | Spec swap rebuilds | SPELLS-1 |
| §9 L239 | Talent choice swap rebuilds | SPELLS-2 |
| §9 L240 | Open Spells page follows the spec | SPELLS-3 |
| §9 L241–242 | Pet summon and dismiss, `debug spells` | SPELLS-4 |
| §9b L256 | Grid populates on a non-English client | LOC-1 |
| §9b L257 | `debug spells` English token | LOC-2 |
| §9b L258 | `[Cooldowns] rebuild` line | LOC-3 |
| §9b L259 | Both `spells add` spec forms | LOC-4 |
| §9b L260 | Localized names on the page, `[262]` stored | LOC-5 |
| §9b L261 | Spec-key upgrade, per profile | LOC-6 |
| §9c L275 | Swipe smooth, countdown continuous | GRID-8 |
| §9c L276 | Cooldown alpha and tint to the final second | GRID-9 |
| §9c L277 (with step L270) | Glow type and color, text and badge toggles mid-cooldown | GRID-10 |
| §9c L278 | Glow follows the target mid-cooldown | GRID-11 |
| §9c L279 | Charges badge in combat | GRID-12 |
| §10 L304 | Cooldown Manager gate, page and slash | SPELLS-5 |
| §10 L305 | Wind Shear not split | SPELLS-6 |
| §10 L306 | Unknown class or spec | SPELLS-7 |
| §10 L307 | Closed-page spec switch gates on the new spec | SPELLS-8 |
| §10 L308 | Another spec takes the lenient path | SPELLS-9 |
| §10 L286–293, L309 | Subcommands; page rebuilds live | SPELLS-10 |
| §10 L310 | `spells reset` one spec | SPELLS-11 |
| §10 L311 | `spells resetall` every spec | SPELLS-12 |
| §10 L312 | Spells Defaults resets the selected spec | SPELLS-11 |
| §10 L313 | Drag reorder, drop line, `/reload`, Esc | SPELLS-13 |
| §10 L314 | Row tooltips, remove mark | SPELLS-14 |
| §10 L315 | Other addons' panels unhooked | SPELLS-15 |
| §10 L316 | Racial kept on own-class reset | SPELLS-16 |
| §11 L323 | Enable box → `get enabled` | PANEL-14 |
| §11 L324 | `set scale 1.25` moves the slider | PANEL-15 |
| §11 L325 | Gated `growDirection` error with the depends line | SLASH-4 |
| §11 L326 | `/kcd list` shows every row | SLASH-3 |
| §11 L327 | Number clamp | SLASH-5 |
| §11 L328 | Three-float color | SLASH-6 |
| §11 L329 | Color picker drag throttle | PANEL-16 |
| §11 L330, L333 | Unit picker survives rebuilds and refreshers | PANEL-13 |
| §11 L334–335 | Panel and slash writes redraw modules and widgets | PANEL-15 |
| §11 L336 | Gate errors name the options and the sibling | SLASH-4 |
| §11 L337 | Clamps; color float count and clamp | SLASH-5, SLASH-6 |
| §11 L338 | Tab strips per page; Profiles has none | PANEL-8 |
| §11 L339 | Use class color beside every swatch | PANEL-10 |
| §11 L340 | Headings per tab | PANEL-9 |
| §11 L341 | Label text is a text box | LABEL-2 |
| §11 L342 | Spells rows drag, one handle | SPELLS-13 |
| §11 L343 | Unit picker in the band, stays on tab click | PANEL-3 |
| §11 L344 | The band retargets every tab | PANEL-12 |
| §11 L345 | Charges badge inset and clamp | GRID-13 |
| §11 L346 | Rotation reads `45 deg` | LABEL-6 |
| §11 L347 | Per-row `pcall` in `Helpers.RenderRows` keeps a malformed row from blanking the page | dropped: no longer exists. Rendering moved to LibKa0s-Options-1.0's flow engine, which does not pcall per row (`tests/test_schema.lua` records the removal as a reported finding); the old item also said it had no in-client step |
| §12 L353 | `/kcd reset <path>` one row | SLASH-7 |
| §12 L354 | A reset color is a copy | SLASH-8 |
| §12 L355 | Retired reset words answer | SLASH-9 |
| §12 L356 | Panel Defaults resets that panel (and its `[Set]` line) | PANEL-17 (Cast bar), PANEL-29 (General and Icons) (line: DIAG-8) |
| §12 L357 | `spells resetall` row | SPELLS-12 |
| §12 L358 | `resetall` resets everything, incl. every unit's icon-grid and cast-bar anchor; no confirm | SLASH-10 (the cast-bar anchor: its Free re-check) |
| §12 L359 | `resetposition` exact coordinates | STATE-10 |
| §12 L360 | Reset all settings popup and tooltip | PANEL-18 |
| §12 L361 | Reset position button | STATE-10 |
| §12 L362 | Per-panel Defaults (General / Icons / Cast bar) reset that panel only; other panels and the spell list untouched ("mirrors `/kcd reset <panel>`" is stale) | PANEL-17 (Cast bar), PANEL-29 (General and Icons) |
| §12 L363 | Spells Defaults (duplicate of §10 L312) | SPELLS-11 |
| §12 L366–367 | No error; open panels repaint | PANEL-17 |
| §12 L368 | `resetall` → enabled true, default visibility | SLASH-10 |
| §12 L369 | `resetall` label and cast bar defaults | SLASH-11 |
| §12 L370 | `resetall` snaps a dragged grid, or a Free cast bar, back to its default | SLASH-10 (grids; the Free cast bar after `anchorMode FREE` again) |
| §13 L377–383 | Create, switch, copy, delete, `/reload` each | PROFILE-2 (copy into a scratch profile) |
| §13 L386 | Profiles page draws | PROFILE-1 |
| §13 L387 | Switch re-anchors and re-skins | PROFILE-2 |
| §13 L388 | Per-character, per-class and per-realm scope in `profileKeys` | PROFILE-3 (all three) |
| §13 L389 | Migration on change, version 5 account-wide | PROFILE-4 |
| §13 L390 | Colors and font flags survive a switch | PROFILE-5 |
| §13 L391 | Spell lists per profile | PROFILE-6 |
| §14 L404 | `/kcd config` refused in combat | COMBAT-1 |
| §14 L405 | `/kcd set` applies in combat | COMBAT-2 |
| §14 L406 | Out of combat: landing page, tree expanded, logo and command list | SLASH-1, PANEL-2 |
| §14 L407 | Sidebar pages in combat (six pages, stale: now the Ka0s KickCD page and four subpages; refuse-and-close, stale: now covered) | COMBAT-3 |
| §14 L408 | Each page once under the parent | PANEL-1 |
| §15 L416 | `debug spells` | DIAG-1 |
| §15 L417 | `debug castbar` | DIAG-2 |
| §15 L418, L428 | `debug on/off/toggle`, session-only, console not chat | DIAG-3 |
| §15 L419, L429 | `debug window` leaves the flag | DIAG-4 |
| §15 L420, L430 | `debug events`, `[Init]` clause | DIAG-5 |
| §15 L421 | Bare `/kcd debug` | DIAG-6 |
| §15 L422 | `diagnostics` both forms | DIAG-28 |
| §15 L425 | Every subcommand in combat | COMBAT-7 |
| §15 L426 | `interrupt` shows `<secret>` | COMBAT-8 |
| §15 L427 | `debug castbar` with and without `C_CurveUtil` | COMBAT-9 |
| §16 L439–440, L445–446 | Taint pass: interrupt on and off cooldown 5+ times, target swaps under `target_casting_interruptible`; zero errors, swipe and text work | COMBAT-10 |
| §16 L441–442, L447 | `debug interrupt` mid-cast; mid-cast flip with no Lua branch; `<secret>` in the dump | CAST-5 (dump: COMBAT-8) |
| §16 L448 | Interruptible-only hides by alpha, not `:Hide()` | STATE-15 |
| §17 L458 | No `schema error` on a cold login | INSTALL-6 |
| §18 L469, L471 | Dropdowns list media and apply live; cooldown font | PANEL-19 |
| §18 L470 | No 42×42 Border tile | PANEL-23 |
| §19 L480 | Combat trace | DIAG-7 |
| §19 L481 | Profile switch and copy traces | PROFILE-7 |
| §19 L482 (Defaults) | Section Defaults counts rows | DIAG-8 |
| §19 L482 (Reset all) | Reset all logs one line, `(0 rows)` again | DIAG-9 |
| §19 L482 (Reset Profile) | Reset Profile logs no count | PROFILE-7 |
| §19 L482 (mute, order) | Mute does not stick; `locked` before `reset general` | DIAG-10 |
| §19 L483 | Cast and IconGrid traces | DIAG-11 |
| §19 L484 | Open trace | DIAG-12 |
| §19 L485 | Spell-list traces | DIAG-13 |
| §19 L486 | Debounced `[Set]` | DIAG-14 |
| §19 L487 | No spam | DIAG-15 |
| §20 L491 | Focus on and linked by default, at y = 260 | FOCUS-1 |
| §20a L505 | Enabling Focus builds it live | FOCUS-2 (from Focus off, a `/reload` and `/kcd unlock`) |
| §20a L506 | Independent gating | FOCUS-3 |
| §20a L507 | Disabling tears Focus down | FOCUS-4 |
| §20a L508 | No errors | FOCUS-2 – 4 (clean-run rule) |
| §20b L515–516 | Linked page: grayed strip and note | FOCUS-6 |
| §20b L517 (link) | Note link style, opens General → Units | FOCUS-7 |
| §20b L517 (combat) | Note link refused in combat (unreachable now: the cover blocks the link) | COMBAT-5 |
| §20b L518 | One unit selection across entries, session-only | PANEL-11 |
| §20b L519, L528 | Linked Focus mirrors Target live | FOCUS-8 |
| §20b L520 | Unlink shows seeded rows; hidden page repaints | FOCUS-9 |
| §20b L521 | Focus-only edit leaves Target | FOCUS-10 |
| §20b L522 | Re-tick reverts | FOCUS-11 |
| §20b L523, L531 | Tick and button on one line, nowhere else | FOCUS-12 |
| §20b L524, L530 | Copy styling, one line, one-time copy (N defined; a `/kcd resetall` baseline makes it 4) | FOCUS-13 |
| §20b L525 | `units.focus.link` via slash; Defaults re-links | FOCUS-14 |
| §20b L529 | Position and identity per unit | FOCUS-15 |
| §20b L532 | No errors | FOCUS-6 – 14 (clean-run rule) |
| §20c L544–545 | Mid-cast enable at current progress | FOCUS-5 |
| §20c L546 | Master switch hides both units and revives them | STATE-4 |
| §20d L583, L590 | Unlinked Focus own alpha and tint; GCD note | FOCUS-16 |
| §20d L584 | Focus alpha change mid-cooldown | FOCUS-17 |
| §20d L585 | Border edit leaves the curves | FOCUS-18 |
| §20d L579, L586 | Unit picker after a mid-cooldown `/kcd set` with the panel open | FOCUS-17 (PANEL-13 makes the same check outside a cooldown) |
| §20d L580, L587 | Re-tick mid-cooldown reverts Focus to Target's dim red | FOCUS-19 |
| §20d L588 | No errors | FOCUS-16 – 19 (clean-run rule) |
| §20d L592 | Cleanup: Icons → Defaults for Target, then Focus | FOCUS-19 (its clean-up step) |
| §21 L600–606 | Legacy fold keeps values and position, v1 → v5 | INSTALL-7 |
| §21 L607 | Fold idempotent | INSTALL-8 |
| §21 L608 | Focus arrives with fresh defaults | INSTALL-8 |
| §22 L614, L617, L628 | Default label; Show label hides only the label; no label rows on General | LABEL-1 |
| §22 L618 | Label text live | LABEL-2 |
| §22 L619 | Attach to | LABEL-3 |
| §22 L620 | Anchor pairs, no error | LABEL-4 |
| §22 L621 | Justify | LABEL-5 |
| §22 L622 | Rotation | LABEL-6 |
| §22 L623 | Font, size, flags | LABEL-7 |
| §22 L624 | Color survives re-anchor | LABEL-8 |
| §22 L625 | Linked Focus Text Label shows the note | FOCUS-6 |
| §22 L626, L634 | Unlinked Focus label independent; text stays on relink | LABEL-9 |
| §22 L627 | Focus off hides its label | LABEL-10 |
| §22 L629 | Label follows General visibility, attached to the cast bar, then the icons | LABEL-11 |
| §22 L635 | Label shown only while the grid is; never gated by the cast bar's own cast-presence hiding | LABEL-11 (the grid half), LABEL-12 (Attach to `castbar` in Always mode) |
| §22 L630 | Always shows the label | LABEL-12 |
| §22 L633 | Every change live | LABEL-1 – 8 |
| §22 L636 | No error on rapid attach switching, rapid offset and rotation slider drags, visibility changes | LABEL-15 |
| §23 L644–651 | Label style backfill, idempotent | INSTALL-9 |
| §24 L660, L668 | Console header, Esc, opening never throws | DIAG-16 |
| §24 L661, L669 | Line counter and Clear | DIAG-17 |
| §24 L662–663, L670 | Wheel and thumb in step, bottom is newest | DIAG-18 |
| §24 L664 | Inert when it fits | DIAG-19 |
| §24 L665, L671 | Shared window edge vs a second addon | DIAG-20 |
| §25 L682 | Degrades without error | DEGRADED-1 |
| §25 L683 (list) | `/kcd list` unavailable line | DEGRADED-2 |
| §25 L683 (enable) | Disable, refusal, enable | DEGRADED-3 |
| §25 L683 (lock) | Lock and unlock work | DEGRADED-4 |
| §25 L683 (help) | Plain help rows | DEGRADED-5 |
| §25 L684 | One notice | DEGRADED-6 |
| §25 L685 | Same sentence as AbsorbTracker and ConsumableMaster | DEGRADED-7 |
| §25 L686 | Each seam's own consequence | DEGRADED-8 |
| §25 L687 | Diagnostics unavailable | DEGRADED-9 |
| §25 L690–692, L697 | The `L` trap | PANEL-28 |
| §25 L695 | Rename the folder back | DEGRADED-13 |
| §25 L696 | Degraded summary line | DEGRADED-1 – 8 |
| §26 L714–723 | Three title-bar marks, no tooltip; `×` regression | DIAG-21 |
| §26 L724–726 | Copy window close mark | DIAG-22 |
| §26 L727–733 | Perf panel close is the same mark | DIAG-23 |
| §26 L734–739 | Console is monospace | DIAG-25 |
| §26 L740–742 | JetBrains Mono in the font dropdown | PANEL-25 |
| §26 L743–746 | Degraded: `/kcd config` still opens, no JetBrains Mono | dropped: no longer exists. Without LibKa0s the settings panel is unavailable (`settings/OptionsSetup.lua`'s stub prints "…so the settings panel is unavailable"), so there is no dropdown to inspect; the panel's refusal is DEGRADED-8 |
| §26 L749–752 | Summary of the above | DIAG-21 – 25 |
| §27 L780 | Eight composed dropdowns list real media | PANEL-19 |
| §27 L782 | `MODULES.OptionsCompose` reports 3 (stale number; now the vendored `COMPOSE_MINOR`) | PANEL-20 |
| §27 L784 | Chosen face applies and survives `/reload` | PANEL-21 |
| §27 L785–788 | Media registered later appears | PANEL-22 |
| §27 L789 | No errors | PANEL-19 – 22 (clean-run rule) |
| §28 L805–809, L819–822 | Pooled tab strip, three passes | PANEL-24 |
| §28 L811–816, L823–825 | Perf strings in US spelling | DIAG-26 |
| §28 L826 | No errors | PANEL-24, DIAG-26 (clean-run rule) |
| §29 L855–860 | Border dropdown flush in five addons, any load order | PANEL-23 |
| §30 L877–886 | Perf panel: one close, shared mark, same inset | DIAG-23 |
| §30 L887–889 | Perf close hides, run kept | DIAG-24 |
| §30 L890 | No errors | DIAG-23 – 24 (clean-run rule) |
| §31 L918–922 | Degraded `debug castbar` prints, tagged | DEGRADED-11 |
| §31 L923–924 | Notice once, before the dump | DEGRADED-6 (Pending sign-off) |
| §31 L925 | Rename the folder back and `/reload` | DEGRADED-13 |
| §32 L956–963 | Two cast bars animate independently | CAST-13 |
| §33 L976–980 | Minimap button and AddOns list draw the logo | INSTALL-10 |
| §33 L981–982 | Tooltip | INSTALL-11 (signed: X1.4, 2026-09-25) |
| §33 L983 | Left-click opens settings, lock untouched | INSTALL-12 (the opening signed: X1.4) |
| §33 L984–989 | Right-click menu, Locked tick, agreement | STATE-9 (the opening signed: X1.4) |
| §33 L990–992 | Button position persists | INSTALL-13 |
| §33 L993–997 | Minimap checkbox, `global.minimap.shown`, no alias | PANEL-26 |
| §33 L998–1000 | Broker hide follows the tick | PANEL-26 |
| §33 L1001–1002 | Profile switch leaves the button hidden | PROFILE-8 |
| §33 L1003–1008 | No reset shows a hidden button | PANEL-27 |
| §33 L1009–1012 | Broker display row | INSTALL-14 |
| §33 L1013–1017 | Disabled: bare `/kcd`, help, version, enable | SLASH-12 |
| §33 L1018–1024 | Minimap button while off | STATE-5 |
| §33 L1025–1028 | Feature verbs refuse while off | SLASH-13 |
| §33 L1028–1031 | Live verbs answer while off | SLASH-12 |
| §34 step 0 (L1039–1045) | Strip clears the unit label | LABEL-13 |
| §34 step 0 (L1046–1052) | Strip clears it straight after `/reload`; lock hides both | LABEL-14 |
| §34 step 1 | Strip labeled by unit | CAST-7 |
| §34 step 2 | Drag the strip, position sticks | CAST-8 (also carries §7a L182) |
| §34 step 3 | `?` mark drags | CAST-9 |
| §34 step 4 | Strip and `?` tooltips | CAST-10 |
| §34 step 5 (first half) | Right-click opens settings | CAST-11 |
| §34 step 5 (combat) | Right-click refused in combat | COMBAT-6 |
| §34 step 6 | PRIMARY: no strip, no drag | CAST-6 |
| §34 step 7 | Back to Free, strip returns | CAST-12 |
| §34 step 8 | Lock hides both strips | STATE-7 |
| §34 step 9 | No LibKa0s: body drag, no strip | DEGRADED-12 |
| §35 step 1 | README bug-report steps | DIAG-27 |
| §35 step 2 | Trace kept, Copy clean | DIAG-28 (unrun half under Pending sign-off) |
| §35 step 3 | Report shape | DIAG-29 |
| §35 step 4 | Ungated, flag untouched | DIAG-30 (unrun half under Pending sign-off) |
| §35 step 5 | While disabled, both forms | DIAG-31 |
| §35 step 6 | Combat and restricted instance | COMBAT-11 |
| §35 step 7 | No alias | DIAG-32 |
| §35 step 8 | Long alias and any case | DIAG-33 |
| §35 step 9 | Console cap, Copy without a hitch | DIAG-17 |
| §35 step 10 | Strips carry `?` and no X | GRID-14 |
| §35 step 11 | No LibKa0s: diagnostics unavailable | DEGRADED-9 |
| §36 KC-S1 | Settings tree General · Grid · Spells · Profiles | PANEL-1 |
| §36 KC-S2 | Grid band, rail, first entry, rail top edge | PANEL-3 |
| §36 KC-S3 | Only the controls scroll | PANEL-4 |
| §36 KC-S4 | Each entry remembers its tab | PANEL-7 |
| §36 KC-S5 | Focus in the band keeps the tab, shows Focus's values | PANEL-12 |
| §36 KC-S6 | Linked Focus rail and note; link opens Units | FOCUS-6, FOCUS-7 |
| §36 KC-S7 | Defaults for the band unit only; tooltip | PANEL-17 |
| §36 KC-S8 | Combat cover over Grid | COMBAT-4 |
| §36 KC-S9 | Tabs in one row from the first frame | PANEL-5 |
| §36 KC-S10 | `/kcd reset castbar` answer | SLASH-9 |
| §36 KC-S11 | Rail tooltips | PANEL-6 |
