# AuraMaster smoke-test coverage map (SP-AM-03)

Old `docs/smoke-tests.md`: 1941 lines, 300 checks (294 numbered 1-294, the five suffixed 46a, 58a, 59a, 170a and 170b, and the unnumbered "The page draws" paragraph of section L). New: 1636 lines, 246 checks in 14 themes. 8 old checks dropped whole (and parts of D 24, I 47, D 26, P 69, Q 80, T 139, AA 211-213 and AB 234, named in their rows), 86 new IDs under Pending sign-off.

Every old check appears once below. "Also merged into" names the other new checks that took part of an old multi-behavior check. Section letters are the old ones (A-AE; the five unlettered sections by name); line ranges are the old file's.

Pending sign-off rule (spec S4 as clarified on 2026-09-29): (a) old checks with no recorded pass, and (b) every check new on 2026-09-29 or whose expected result was corrected against the code then. (a) An old check is carried as pending when its `Result:` was empty (S1, S6, S9, S10, S12-S15, FP1-FP11, MK1-MK3), when its section was titled "owed" with no later pass record (sections P and Q, except 71 and 85, which the batch 8 run passed; 67 is covered below with the batch 8 fails), or when a plan names it as owed and no later record passes it: `AuraMaster/docs/superpowers/plans/2026-09-19-smoke-feedback-2.md:65` records the owner verifying section U's 143-161 on 2026-09-20 and owes 162, and 163-166 came after that run, so CONT-8 and LAYOUT-6's aura-button step (162), STYLE-9 (163), FILT-11 (164) and FILT-13 (166) are pending (165 was dropped). Checks in sections with an owner-run record (X to AE, the settings redesign, issues #21/#23, new container) count as signed when that record or a later batch's record passed them. A check whose item an owner run failed is pending, for the steps no later record repeats: the batch 8 run (2026-09-25) failed #7 (200-202), #9/#11/#13 (191-196, 67, 68) and #16 (206-209), and the batch 9 run (2026-09-25, late) failed 211 and 212 ("Screen offset reset"), 221 and 225, and 203 and 215. Later records passed 191-196 (HG-1); 202's long-name and untick/tick steps (214); 200's migrated-profile step (213); 67's inherited-growth note (233, F6) and its Automatic placement and Grow horizontally mirror (238); 206's report-runs-clean steps (210); 207's disabled steps (235); 211's and 212's `attach.y=-4` and chain steps (234, 242); 221, 225, 203 and 215 as rewritten by batch 10 F1-F3 (226-232); and 208 and 209 in the diagnostics rollout's owner run (`Ka0sAddonsCommonTasks/docs/2026-09-25-DIAGNOSTICS_COMMAND/99_REPORT.md` section 6, PASS, owner 2026-09-26): AM-X1 is 208's cap step word for word, AM-S2 and AM-S4 are 209's report after the trace in one Copy, AM-S1 and AM-S11 run `/am debug diagnostics`, AM-S8 is `/am debug diag` as an ordinary unknown word (settings/Slash.lua `runDebug`: an unknown word after `debug` takes the same `Toggle()` as bare `/am debug`), and AM-S2 and AM-S5 switch logging with `/am debug on` and `off`, so DIAG-7, DIAG-8 and DIAG-2's 208 step are signed. Never passed later: 68, 67's flow steps and its **Per row** step, the rest of 200, 201, 202's in and out of combat, in-combat, SharedMedia and chained-Text steps, the in-combat half of 207, 208's help-order step, the rest of 211, and 212's screen-to-Another-container step. So LAYOUT-18 and INSTALL-8's v8 offset step (68), LAYOUT-17 and LAYOUT-11 (67), TEXT-27 (200), TEXT-28 (201), TEXT-29 and LAYOUT-25 (202), DIAG-5 (206), DIAG-6 (207), SLASH-2's help-order step (208), DIAG-9 (211) and INSTALL-8's 212 step are pending. LAYOUT-20 is pending too: its outline on lock follows commit d01ac9d (2026-09-27, "outline a container's placeholder block only while unlocked"), after 221 and 227 passed. Sections A-O and R-W carried no result marker, no owed marker and no owed list naming them: their checks are the standing suite and stay evergreen, except where (b) applies. T was owed when written (`AuraMaster/docs/superpowers/plans/2026-09-19-smoke-feedback.md:113`), but the owner then ran S and T in client: `AuraMaster/docs/superpowers/specs/2026-09-19-smoke-feedback-design.md` is sourced from the S run and `specs/2026-09-19-smoke-feedback-2-design.md` from the T run, and U, which re-checks what those runs failed and points at 140-142, passed on 2026-09-20. (b) New: PROFILE-5 to PROFILE-11 (the `/am profile` verb; PROFILE-10 extends 58), LOC-1 and LOC-2. Corrected against the code in SP-AM-03, SP-AM-03R and the fix rounds: INSTALL-2, INSTALL-4 and PROFILE-2 (four starters, not three: defaults/Profile.lua `NS.STARTER_CONTAINERS`), FILT-4 (a debuff container's Spell Categories grid carries Hard CC, Soft CC and Racials with See spells links, the line naming General -> Spell Categories and the hostile-unit note, since issue #11: settings/Filters.lua `renderCustomGrid`, tests/test_pages_filters.lua), FILT-7 and FILT-8 (the rows' real labels, *Dispellable by anyone*, *Boss debuffs* and *From any player*, defaults/Categories.lua), SLASH-2 (24 rows, `profile` listed), STATE-1 and CONT-5 (in-combat steps through `/am set`: the panel is locked in combat), CONT-3 (in-combat create and delete through `/am new`, `/am delete` and a Delete popup opened before the pull: the combat cover, libs/LibKa0s/OptionsCombat.lua `O.__buildCover`, takes every click on the page, band included), LAYOUT-6 (the combat refusal through `/am pick` alone: the Layout page's **Pick a frame…** button is under the same cover), DIAG-6 (its Cast by change through `/am set container.filter.castBy`) and TEXT-29 (its in-combat Size to fit step through `/am set container.text.autoSize`), PROFILE-12 (a reset in combat, not a switch or copy), CONT-21 (one placeholder per ticked slot), DIAG-3 (the copied-profile line's ASCII `->`), INSTALL-6 and INSTALL-8 (the `[Migrate]` read-out, see T 125), PANEL-22 (the tooltip title), FILT-21 (the chat line names each spell), DIAG-11 (the `[Event]` line shape), STYLE-9 (four bullets), TEXT-8 (`/am debug on`: bare `/am debug` only toggles the console, settings/Slash.lua `runDebug`, and Style.ReportError's `[Style]` line goes through the gated NS.Debug, modules/Style.lua:536, which returns while logging is off, libs/LibKa0s/DebugLog.lua:698-699), TEXT-20 (a debuff container previews the HARMFUL placeholder set, modules/Preview.lua `Preview.AurasFor` and core/Constants.lua `C.PREVIEW_AURAS.HARMFUL`, so each typed placeholder gets a box in its type's color and Mortal Wounds none, not the buff set's Bloodlust) and TEXT-23 (a Text container's own icon on a stacked Center, icon size 0 one row's height: modules/Style_Text.lua `layoutIconAndArea`, tests/test_style_text.lua "text style: on a stacked Center, icon size 0 is ONE ROW's height, not the whole stack (fix round 1, feedback #1)"; an Icons container has no Text section since #6 and draws no template text). Restoring a step the rewrite had lost (LAYOUT-8, LAYOUT-23, LAYOUT-37's element hover, STYLE-8's examples, TEXT-19, STYLE-16, PANEL-15, DIAG-5, PANEL-11's tab kept across a container switch from D 28) is not a correction: the restored expectation is the old one, carried with its old status.

| Old location | Behavior | New ID |
|---|---|---|
| A 1 (:10-11) | Fresh install, no Lua error | INSTALL-1 |
| A 2 (:12-15) | Starter containers appear | INSTALL-2 (three corrected to four: #4 *Player cooldowns*) |
| A 3 (:16) | /reload keeps positions | INSTALL-3 |
| A 4 (:17-19) | Deleted starters stay deleted (seeded) | INSTALL-4 (three corrected to four) |
| B 5 (:23-25) | /am, spaces, /auramaster open settings; combat refusal | SLASH-1 |
| B 6 (:26-27) | /am help rows (was 23 commands, now 24) | SLASH-2 |
| B 7 (:28) | Unknown verb prints the unknown line and help | SLASH-3 |
| B 8 (:29) | /am options alias | SLASH-1 |
| B 9 (:30) | /am version | SLASH-4 |
| B 10 (:31) | /am containers lists, selected marked | SLASH-5 |
| B 11 (:32-34) | /am new with words; nonsense refused | SLASH-6 |
| B 12 (:35-36) | /am select by index and name; 999 refused | SLASH-7 |
| B 13 (:37-39) | /am get, set, reset, list | SLASH-8 |
| C 14 (:43-62) | Unlock handles, empty outline, test mode, handle placement, growth flip, hover tooltip, screen edge, attached handle | CONT-7 (unlock, outline); also merged into CONT-8, CONT-9, CONT-10, CONT-18, LAYOUT-2; the attached container's handle and placeholders in test mode, unlocked, into LAYOUT-20 |
| C 15 (:63-66) | Drag; right-click handle or ? opens Containers; combat refusal | CONT-11 (drag); right-click half merged into CONT-12 |
| C 16 (:67) | /am test off and /am lock | CONT-18 |
| C 17 (:68-70) | Test mode row on Master controls; /am test in help; /am preview unknown | PANEL-2 (row); also merged into SLASH-2, SLASH-3 |
| C 18 (:71) | Combat drag refused | CONT-11 |
| D 19 (:75-76) | Landing page and tree | PANEL-1 |
| D 20 (:77-80) | General page strip and Master controls rows | PANEL-2 |
| D 21 (:81-84) | Enable checkbox and General visibility | STATE-1 |
| D 22 (:85-86) | Master scale and alpha | PANEL-3 |
| D 23 (:87-103) | Containers band, General tab rows, Delete keeps band, memory flat, Defaults keeps name, Style switch with auras up | PANEL-4 (band); also merged into PANEL-5, PANEL-6, CONT-6 |
| D 24 (:104-122) | Filters tabs, priority block, category grids, See spells, debuff and enchant containers | FILT-3 (grids and the Hide click's `/am get` value); also merged into FILT-2, FILT-5 (the clicked cell's plain check and the other going unlit), FILT-4 (the debuff container, its grid corrected: since issue #11 it holds Hard CC, Soft CC and Racials with See spells links, under the line naming General -> Spell Categories and over the hostile-unit note), FILT-10; the enchant-only container's **[ Categories ][ Sorting ]** strip dropped: schema v5 removed the Weapon enchants aura type (`C.AURA_TYPES = { "HELPFUL", "HARMFUL" }`, core/Constants.lua), so an enchant-only container is a buff container and gets the full General, Categories, Overrides, Sorting strip (settings/Filters.lua `BUFFS_DEBUFFS`) |
| D 25 (:123-129) | Layout tabs, Anchor drawn by mode, /am set redraw | LAYOUT-1 |
| D 26 (:130-143) | Bars tabs, not-in-use notice, icon border, timeless spark, background opacity | STYLE-1 (tabs); also merged into STYLE-2, STYLE-3, STYLE-5; the not-in-use notice and dimmed style page dropped: retired by #6 |
| D 27 (:144-147) | Icons tabs, countdown and time text agree | STYLE-10 |
| D 28 (:148-149) | The picker is shared across pages | PANEL-11 (both halves: Bars → Icon kept across a switch between two bars containers, since #6 an icons container moves the section; and Layout showing the same container) |
| D 29 (:150) | Media dropdowns have entries | PANEL-16 |
| E 30 (:154-155) | New container from the panel | CONT-1 |
| E 31 (:156-161) | Duplicate, Delete, combat refusals | CONT-2 (duplicate, delete); combat half merged into CONT-3 (pending: corrected to `/am new`, `/am delete` and a Delete popup opened before the pull; New container and Duplicate are under the combat cover, COMBAT-3) |
| E 32 (:162-163) | Copy settings from, bar style only | CONT-4 |
| E 33 (:164-165) | Rename; blank refused | CONT-5 |
| F 34 (:169) | Cast by | FILT-1 |
| F 35 (:170-179) | Category Show/Hide priority, never-match, Uncategorized | FILT-6 |
| F 36 (:180-185) | Spell Categories untick, add by name, Restore; Dispel Colors Magic | FILT-12 (starter list, and a spell added by name is listed with its icon and drawn by a container showing Defensive cooldowns); Dispel Colors half merged into STYLE-9; the no-match refusal merged into FILT-18 |
| F 37 (:186-194) | Overrides blacklist, whitelist, both lists, override notes | FILT-26; the Whitelist's unknown-name refusal merged into FILT-18 ("The same in the Whitelist's Add a spell box"); its opening priority sentence superseded: the priority block moved to General, and FILT-2 checks that Overrides opens on **Whitelist** with no rank line |
| F 38 (:195) | Max duration | FILT-28 |
| F 39 (:196-198) | Only auras without a duration, /am forgettimed | FILT-29 |
| F 40 (:199-204) | Filter warnings | FILT-30 |
| G 41 (:208-222) | Attach to a container, loop refused, unlocked test placement, growth-conflict popup | LAYOUT-4 (attach, loop); also merged into LAYOUT-5 (GC-1), LAYOUT-20 (unlocked in test mode: B's strip one of its Spacings past A's block, its placeholders right under it; `/am test off` unlocked and locked), LAYOUT-19 (the empty chain unlocked, 191) |
| G 42 (:223-227) | Frame picker, Escape, /am pick, combat refusal | LAYOUT-6 (pending: the combat refusal corrected to `/am pick` alone; the button is under the combat cover) |
| G 43 (:228-230) | A frame not there yet | LAYOUT-7 |
| H 44 (:234-237) | Weapon enchants row on Player buffs; Hide enchants without a duration | FILT-40 |
| H 45 (:238-240) | /am new enchants; Aura type offers Buffs and Debuffs only | FILT-41 (chat verb); dropdown half merged into INSTALL-6 |
| I 46 (:244-254) | Settings changes deferred in combat and in keys or encounters | COMBAT-1 (combat); key and encounter half merged into COMBAT-2 |
| I 47 (:255-263) | /am config refused in combat; Reset all in combat; profile switch in combat parks containers | SLASH-1 (config refusal); also merged into COMBAT-6, PROFILE-12 (the teardown after a reset); its profile switch and copy in combat dropped: the Profiles page is under the settings lock (COMBAT-3) and `/am profile` is refused in combat (PROFILE-11), so neither can happen in combat any more |
| I 46a (:265-272) | The settings lock (cover, one line, sidebar switch, lift after combat) | COMBAT-3; sidebar half merged into COMBAT-4 |
| J 48 (:276-281) | Hide Blizzard buffs and debuffs, combat deferral | PANEL-20 |
| K 49 (:285-293) | Tooltips, right-click cancel, click-through, world tooltips, strata | LAYOUT-36 (mouse); world-tooltip half merged into LAYOUT-37, including the element hover reaching the world with Show tooltips off or Click-through on (restored in the 2026-09-29 fix round) |
| L page-draws paragraph (:297-299) | Profiles page draws after another addon's page | PROFILE-1 |
| L 50 (:300-301) | New profile gets the starters; switch back | PROFILE-2 (three corrected to four) |
| L 51 (:302) | Copy a profile | PROFILE-3 |
| L 52 (:303-306) | Reset all settings popup and /am resetall | PROFILE-4 |
| M 53 (:310-312) | /am perf capture | DIAG-1 |
| M 54 (:313-321) | Debug console and one [Set] line per bulk act | DIAG-2 (console); bulk half merged into DIAG-3, the General → Reset position button included |
| M 55 (:322-324) | Memory spot-check | DIAG-4 |
| N 56 (:328-330) | Unit swaps | CONT-22 |
| O 57 (:334-340) | /am disable and enable from chat, lock lines, in combat | STATE-2; combat half merged into STATE-5 |
| O 58 (:341-352) | The disabled addon is inert; reload while disabled; profile switch while disabled | STATE-3; also merged into STATE-4, PROFILE-10; its minimap-button clicks into PANEL-23, PANEL-24; its after-`/am enable` Test mode toggles are CONT-18 (the box) and PANEL-24 (the menu entry) |
| O 59 (:353-355) | Disable in combat | STATE-5 |
| P 58a (:365-374) | Schema v2 migration | INSTALL-5 |
| P 59a (:375-379) | Color by dispel type lets go, and in combat | STYLE-6 |
| P 60 (:380-384) | Icon border color | STYLE-11 |
| P 61 (:385-389) | Icons keep Blizzard colors; bars take the palette | STYLE-9 |
| P 62 (:390-393) | Countdown and time text agree (pointer to 27) | STYLE-10 |
| P 63 (:394-398) | Spark on auras without a duration (pointer to 26) | STYLE-3 |
| P 64 (:399-401) | World tooltips (pointer to 49) | LAYOUT-37 |
| P 65 (:402-405) | Placeholder time text follows the format | STYLE-13 |
| P 66 (:406-410) | Text justify on bars and icons | STYLE-14 |
| P 67 (:411-422) | Inherited flow of an attached container, icon attach points | LAYOUT-17; icon half (IA-1) merged into LAYOUT-11 (both pending: batch 8 failed 67, and 233 and 238 re-passed only the note and the Automatic placement) |
| P 68 (:423-432) | Attached handle unlocked; the seam; v8 offset migration | LAYOUT-18 (seam); also merged into LAYOUT-19, INSTALL-8 |
| P 69 (:433-434) | Dimming: Anchor subsections by mode; style page on the other style | LAYOUT-1 (Anchor half); the dimmed style page half dropped: retired by #6 |
| P 70 (:435-439) | ID lists take a shift-clicked link | FILT-14 |
| P 71 (:440-448) | Dispel border has the Solid border's shape | STYLE-12 |
| P 72 (:449-454) | Suggestions while typing | FILT-15 |
| P 73 (:455-458) | A name the lists know resolves without the spellbook | FILT-16 |
| P 74 (:459-463) | A shared name is refused until picked | FILT-17 |
| P 75 (:464-468) | An unknown name; the box tooltip | FILT-18; tooltip half merged into FILT-19 |
| P 76 (:469-481) | Gaps between bars no longer leak the world tooltip | LAYOUT-37 |
| Q 77 (:489-506) | Many groups: nothing vanishes, cost, block order | FILT-7 (row labels corrected: *Dispellable by anyone*, *Boss debuffs*) |
| Q 78 (:507-514) | The Hide column reads as live | FILT-5 (its comparison with the dimmed Bars page dropped: retired by #6) |
| Q 79 (:515-522) | See spells lands on the row's own category | FILT-10 |
| Q 80 (:523-534) | Priority block, one rank per line | FILT-2 (dropped: "the lead-in is one notch smaller than it was", a comparison against a build that no longer exists; the lead-in's normal-font color is kept) |
| Q 81 (:535-539) | The grid cell is a plain checkbox | FILT-5 |
| Q 82 (:540-545) | An Overrides note wraps under its entry | FILT-27 |
| Q 83 (:546-555) | Every debuff is From players or From non-players | FILT-8 (row label corrected: *From any player*) |
| Q 84 (:556-565) | The mouse blocker covers the whole container | LAYOUT-38 |
| Q 85 (:566-588) | A timed bar's spark reads the same with the option on or off | STYLE-4 |
| R 86 (:596-597) | AddOns list logo | PANEL-21 |
| R 87 (:598-604) | Minimap button, drag, tooltip | PANEL-22 |
| R 88 (:605-607) | Left-click opens the settings | PANEL-23 |
| R 89 (:608-617) | Right-click options menu | PANEL-24 |
| R 90 (:618-621) | Checkbox and button agree | PANEL-25 |
| R 91 (:622-632) | Button survives profile switch and resets; from chat | PANEL-26 |
| R 92 (:633-637) | Broker display | PANEL-27 |
| R 93 (:638-640) | Without LibDBIcon and LibDataBroker | DEGRADED-1 |
| S 94 (:644-645) | Default Text template on player buffs | TEXT-1 |
| S 95 (:646-647) | Several durations | TEXT-2 |
| S 96 (:648-649) | Dispel type token | TEXT-3 |
| S 97 (:650-651) | Loops through a pull | TEXT-4 |
| S 98 (:652-653) | Pandemic window recolor and blink | TEXT-5 |
| S 99 (:654-664) | Text Icon tab dimming, icon right, settings changes keep text | TEXT-6 (Icon tab); also merged into TEXT-7, TEXT-8 |
| S 100 (:665-667) | Template refusals | TEXT-9 |
| S 101 (:668-669) | Style switching Bars, Text, Icons; Fill follows | CONT-6; Fill half merged into LAYOUT-35 |
| S 102 (:670) | /am new enchants text shows the enchant | FILT-41 |
| S 103 (:671-673) | Player cooldowns starter shows cooldowns only | INSTALL-2 |
| S 104 (:674-676) | Pandemic blink feel | TEXT-5 |
| S 105 (:677-678) | Nested clipping | TEXT-10 |
| S 106 (:679-681) | Dispel type text on Bleed and Enrage | TEXT-3 |
| S 107 (:682-684) | A Text button built in combat | TEXT-11 |
| S 108 (:685-687) | Icon Left to None live | TEXT-12 |
| S 109 (:688-689) | A literal percent sign | TEXT-13 |
| S 110 (:690-691) | Bracketed stacks | TEXT-14 |
| S 111 (:692-693) | Unlock keeps live auras; empty container drags | CONT-7; drag half merged into CONT-11 |
| S 112 (:694-696) | Test mode checkbox, ends on pull, refused in combat, menu | CONT-18; menu half in PANEL-24 |
| S 113 (:697-700) | Spell list X rows and Restore | FILT-12 |
| S 114 (:701-702) | The "Not in use" notice in muted red | dropped: retired by #6 (a container's rail offers only its own style section, so the notice no longer exists) |
| S 115 (:703-704) | A 59-minute buff on a bar | STYLE-15 |
| S 116 (:705-709) | Changing Style resets Fill, keeps growth; /am new Fill | LAYOUT-35; chat half merged into SLASH-6 |
| T 117 (:716-721) | Attached handle: no Lua error, strip width | LAYOUT-19; width half merged into CONT-16 |
| T 118 (:722-725) | Center stacks the pieces | TEXT-15 |
| T 119 (:726-728) | The Containers band | PANEL-4 |
| T 120 (:729-730) | Restore beside the Category dropdown | FILT-11 |
| T 121 (:731-732) | TEST on the handle | CONT-17 |
| T 122 (:733-735) | Show all / Hide all, one [Set] line | FILT-9; log half merged into DIAG-3 |
| T 123 (:736-746) | Percent tokens and the probes | TEXT-16 |
| T 124 (:747-752) | Built-in templates and the Preview | TEXT-18 |
| T 125 (:753-761) | Weapon enchants container migration; enchant-only test mode count | INSTALL-6; test-mode half merged into CONT-21. Its "log in with `/am debug on` → one `[Migrate]` line per converted container and one for the cleared whitelist" cannot happen: the debug flag is session state, false at load (core/State.lua:19), D.Debug returns while it is off (libs/LibKa0s/DebugLog.lua:698-699), and the ladder runs in OnInitialize (core/Database.lua:292). INSTALL-6 reads the stamp instead (`/am debug on` → the `[Init]` line's `schema v11`, core/DebugLogSetup.lua:118-125); the log lines are asserted by tests/test_database.lua "v5: MigrateV5 logs one [Migrate] line per converted container, naming it (feedback #6)" |
| T 126 (:762-773) | Bars background by dispel type, opacity in combat | STYLE-7 |
| T 127 (:774-776) | Right-click the ? opens Containers; combat refusal | CONT-12 |
| T 128 (:777-778) | Switched sections on Layout → Anchor (pointer to 25) | LAYOUT-1 |
| T 129 (:779-780) | Switched sections, Party Frame Enhanced | dropped: a check of another addon (Party Frame Enhanced's own smoke suite) |
| T 130 (:781-791) | The dispel type word in color; rows on the Font tab | TEXT-19 (with "toggles set before the move keep their values") |
| T 131 (:792-798) | The dispel backdrop | TEXT-20 (its test-mode step corrected: the debuff placeholders, each typed one boxed, Mortal Wounds none, not the buff set's Bloodlust) |
| T 132 (:799-803) | The dispel edge | TEXT-21 |
| T 133 (:804-808) | The percent formatter's rounding, live | TEXT-17 |
| T 134 (:809-814) | A stacked icon keeps one row's height | TEXT-23 (corrected: a Text container's own icon on a stacked Center, not an Icons container's text, which no longer exists) |
| T 135 (:815-819) | A migrated enchant container's Overrides list is empty | INSTALL-6 |
| T 136 (:820-823) | An enchant-only container in test mode | CONT-21 (its "at most two" count corrected: one placeholder per ticked enchant slot, three by default, modules/Preview.lua `placeholderCount`) |
| T 137 (:824-828) | Dispel color back to static repaints idle slots | STYLE-7 |
| T 138 (:829-833) | An out-of-palette dispel type gets no stand-in | TEXT-22 |
| T 139 (:834-845) | The Text Template section; the not-in-use notice color | TEXT-24; the Centered Preview join merged into TEXT-18; the notice half dropped: retired by #6 |
| T 140 (:846-853) | No gap between template pieces | TEXT-25 |
| T 141 (:854-858) | The Justify note | TEXT-26 |
| T 142 (:859-863) | Typeless debuffs probe; tooltips say so | STYLE-8 (the probe, and the tooltips naming Judgment and Consecration); the Dispel Colors line's "(Text -> Font)" pointer merged into STYLE-9 |
| U 143 (:872-879) | The settings lock covers every page | COMBAT-3 |
| U 144 (:880-888) | Switching category in combat | COMBAT-4 |
| U 145 (:889-892) | A Reset-all popup open at the pull | COMBAT-6 |
| U 146 (:893-903) | Growth flips without a reload | LAYOUT-2; its follower step (which pointed at item 67) is the same check as LAYOUT-17's, kept there once and LAYOUT-2 points to it |
| U 147 (:904-915) | Point rows and the facing-growth hint | LAYOUT-3 |
| U 148 (:916-921) | Dispel-mode bar opacity in combat | STYLE-7 |
| U 149 (:922-927) | The Text style's Enrage stays invisible | TEXT-22 |
| U 150 (:928-932) | The Text icon and its border (pointer to 99) | TEXT-6 |
| U 151 (:933-936) | The moved Dispel type rows (pointer to 130) | TEXT-19 (rows on Font, not Animation; values set before the move kept) |
| U 152 (:937) | The Justify note (pointer to 141) | TEXT-26 |
| U 153 (:938-944) | Item 7 sequence, instrumented | TEXT-8 (bare `/am debug` corrected to `/am debug on`, then `/am debug` to open the console) |
| U 154 (:945-948) | The owner's all-tokens template (pointer to 140) | TEXT-25 |
| U 155 (:949-955) | The item-2 probe and the Paladin bars | STYLE-8 |
| U 156 (:956-964) | The Pandemic tab | STYLE-16 (with "values set before the rename are kept", a threshold of 8 still reading 8) |
| U 157 (:965-969) | Container pickers sort by name | PANEL-18; /am containers order merged into SLASH-5 |
| U 158 (:970-975) | Icon border through the pandemic settings | STYLE-17 |
| U 159 (:976-979) | A Text icon border and Width | TEXT-8 |
| U 160 (:980-982) | A bar border | STYLE-18 |
| U 161 (:983-988) | A border style other than Solid | STYLE-19 |
| U 162 (:989-998) | Outline and handle on an attached container; picker outline | CONT-8 (pending: owed); also merged into CONT-12, LAYOUT-6 (the aura-button step, pending) |
| U 163 (:999-1004) | General → Dispel Colors reads as a list | STYLE-9 (pending; its "three lines" corrected to four: settings/GeneralDispel.lua:50-58 has four facts) |
| U 164 (:1005-1009) | General → Spell Categories split in two | FILT-11 (pending) |
| U 165 (:1010-1016) | The Text Template block dims with the page | dropped: retired by #6 (no dimmed style page exists) |
| U 166 (:1017-1027) | Spell lists alphabetical, three categories renamed | FILT-13 (pending) |
| V 167 (:1034-1039) | Make a category | FILT-31 |
| V 168 (:1040-1045) | It is a real category everywhere | FILT-32 |
| V 169 (:1046-1049) | It filters | FILT-33 |
| V 170 (:1050-1062) | The overlap mark on the row and in the tooltip | FILT-34 |
| V 170a (:1063-1066) | Rename and Delete sit under the picker | FILT-11 |
| V 170b (:1067-1073) | The add box suggests from the spellbook too | FILT-15 |
| V 171 (:1074-1078) | Rename a category | FILT-35 |
| V 172 (:1079-1085) | A shipped category draws nothing about itself | FILT-11 |
| V 173 (:1086-1090) | The answer line knows what it is about | FILT-36 |
| V 174 (:1091-1094) | An empty or duplicate name | FILT-37 |
| V 175 (:1095-1100) | Delete a category | FILT-38 |
| V 176 (:1101-1105) | A deleted category stops filtering | FILT-39 |
| V 177 (:1106-1109) | Categories belong to the profile | PROFILE-13 |
| W 178 (:1123-1126) | A cast id resolves to its aura | FILT-20 |
| W 179 (:1127-1130) | A cast id it cannot resolve lists candidates | FILT-21 (its quoted chat line corrected: modules/CastAura.lua:71-76 names each id, "Renewing Mist (115151)") |
| W 180 (:1131) | Then pick one | FILT-21 |
| W 181 (:1132-1134) | An unknown id is never refused | FILT-22 |
| W 182 (:1135-1138) | The note on a stored entry | FILT-23 |
| W 183 (:1139-1141) | The add box hint | FILT-19 |
| W 184 (:1142-1144) | The Overrides lists take the same path | FILT-24 |
| W 185 (:1146-1159) | The four corrected shipped ids; Fatal Flourish | FILT-25 |
| X 186 (:1163-1167) | Each container previews its own kind | CONT-19 |
| X 187 (:1168-1172) | The icon dispel border in test mode | STYLE-12 |
| X 188 (:1173-1177) | Bars colored by dispel type in test mode | STYLE-6 |
| X 189 (:1178-1180) | Text dispel word in test mode | TEXT-19 |
| X 190 (:1181-1184) | Switching kind while previewing | CONT-20 |
| Y 191 (:1191-1195) | Spike: the filter strings | CONT-23 |
| Y 192 (:1196-1200) | An empty chain unlocked | LAYOUT-19 |
| Y 193 (:1201-1204) | The empty outline fills and empties | CONT-24 |
| Y 194 (:1205-1208) | No overlap with a populated parent | LAYOUT-25 |
| Y 195 (:1209-1211) | Weapon enchants empty outline | CONT-25 |
| Y 196 (:1212-1215) | Empty chain in combat, no emptyPass | LAYOUT-26 |
| Z 197 (:1252-1257) | The X on the strip | CONT-13 |
| Z 198 (:1258-1263) | Click the X | CONT-14 |
| Z 199 (:1264-1269) | What the X does not do | CONT-15 (the drag that starts on the X, and the combat click); the right-click on the strip and "?" merged into CONT-12, the left-drag on the strip and "?" into CONT-11, the screen-edge push into CONT-10 |
| Z 200 (:1270-1274) | Size to fit migrated and new | TEXT-27; migrated half merged into INSTALL-7 |
| Z 201 (:1275-1280) | Size to fit follows the content | TEXT-28 |
| Z 202 (:1281-1288) | Size to fit limits | TEXT-29 (its in-combat tick corrected to `/am set container.text.autoSize true`: the Text section is under the combat cover); chain half merged into LAYOUT-25 (both pending for the steps 214 did not repeat) |
| Z 203 (:1289-1299) | The name label, locked | LAYOUT-31 |
| Z 204 (:1300-1308) | The name label, unlocked | LAYOUT-32 |
| Z 205 (:1309-1316) | The label with the rest (rename, color, scale, visibility, copy) | LAYOUT-34; rename half merged into CONT-5, copy half into CONT-4 |
| Z 206 (:1317-1323) | /am diagnostics out of combat | DIAG-5 (with its recording step: whether the [Shown] button line carries the aura's inst/id or only its name or icon) |
| Z 207 (:1324-1329) | Diagnostics in combat and while disabled | DIAG-6 (its in-combat Cast by change corrected to `/am set container.filter.castBy mine`: the Filters section is under the combat cover) |
| Z 208 (:1330-1334) | Report caps; debug verbs; help order | DIAG-7; also merged into DIAG-2, SLASH-2 (signed but for the help order: AM-X1, AM-S2, AM-S5, AM-S8 of the diagnostics rollout, 2026-09-26) |
| Z 209 (:1335-1338) | The two forms and no diag | DIAG-8 (signed: AM-S1, AM-S2, AM-S4, AM-S8, AM-S11 of the diagnostics rollout, 2026-09-26) |
| AA 210 (:1370-1376) | Diagnostics, test mode off and on | DIAG-5 |
| AA 211 (:1377-1383) | Only the rows in use (non-default and inert lines) | DIAG-9 (its attach.edge part dropped: attach.edge removed by schema v11; its `attach.y=-4` step moved to INSTALL-8; pending: the late 2026-09-25 run failed it) |
| AA 212 (:1384-1392) | The v9 migration | INSTALL-8, with the screen-to-Another-container step (no 4px nudge, X/Y offsets read 0); its Side and attach.edge part dropped: removed by schema v11. Its `[Migrate]` lines cannot reach the console (see T 125): INSTALL-8 reads the `[Init]` line's schema version, and the per-profile lines and the no-op second run are asserted by tests/test_database.lua "database v2: RunMigrations logs one [Migrate] line per profile, and a second run is a no-op" and tests/test_migrations.lua "migrations: every step is idempotent on a fresh default profile" |
| AA 213 (:1393-1397) | Size to fit is Text-only (v9) | INSTALL-7 (its dimmed Text page part dropped: retired by #6) |
| AA 214 (:1398-1405) | A live long name under Size to fit | TEXT-29 |
| AA 215 (:1406-1415) | Label Justify defaults | LAYOUT-31 |
| AA 216 (:1416-1421) | The Side list | dropped: the Side row was retired by batch 11 G1; the two anchor-point rows replacing it are LAYOUT-9 to LAYOUT-14 |
| AA 217 (:1422-1425) | A growth flip mirrors the Side | dropped: the Side row was retired by batch 11 G1; Automatic mirroring is LAYOUT-11 and LAYOUT-12 |
| AA 218 (:1426-1430) | Side limits; /am set attach.edge refused | dropped: the Side row and attach.edge were retired by batch 11 G1; the path now answers Setting not found (LAYOUT-15) |
| AA 219 (:1431-1436) | The Side fallback note | dropped: batch 11 G5 stores any pair, with no fallback note (LAYOUT-9) |
| AA 220 (:1437-1444) | The default side of a new attachment | dropped: the Side row was retired by batch 11 G1; Automatic defaults are LAYOUT-10 to LAYOUT-12, and picks surviving a retarget are asserted by tests/test_anchors_edges.lua "edges: picked points survive an attach, a retarget and a detach and re-attach" |
| AA 221 (:1445-1448) | The test-mode block outline | LAYOUT-20 |
| AA 222 (:1449-1452) | The join tooltip, no join dot | LAYOUT-16 |
| AA 223 (:1453-1465) | Every strip in its own column | LAYOUT-19; side-follower bullets merged into LAYOUT-23, the strip-row push with labels off included |
| AA 224 (:1466-1469) | Weapon enchant placeholders | CONT-21 |
| AA 225 (:1470-1475) | One geometry locked, unlocked and in test mode | LAYOUT-24 |
| AB 226 (:1498-1504) | The chain unlocked (mockup) | LAYOUT-19 |
| AB 227 (:1505-1509) | The chain in test mode | LAYOUT-20 (its outline kept on lock follows the later 2026-09-27 rule in 221: no outline while locked; pending, since that rule postdates both passes) |
| AB 228 (:1510-1514) | Collapse on lock | LAYOUT-21 |
| AB 229 (:1515-1519) | Label order, unlocked | LAYOUT-32 |
| AB 230 (:1520-1524) | Label order and justify, locked | LAYOUT-33 |
| AB 231 (:1525-1529) | Growth up mirrors the chain | LAYOUT-22 |
| AB 232 (:1530-1536) | A side follower | LAYOUT-23 |
| AB 233 (:1537-1541) | The inherited-growth note | LAYOUT-17 |
| AB 234 (:1542-1549) | Schema v10 on a v9 profile | INSTALL-8 (its Side part dropped: retired by batch 11; its `[Migrate]` line read as in AA 212) |
| AB 235 (:1550-1561) | Diagnostics while disabled or stood down | DIAG-6 |
| AC 236 (:1588-1597) | The two anchor-point dropdowns | LAYOUT-9 |
| AC 237 (:1598-1604) | Text under Text (Automatic) | LAYOUT-10 |
| AC 238 (:1605-1610) | Icons under Icons (Automatic) | LAYOUT-11 |
| AC 239 (:1611-1617) | Bars under a centered Text, growth up | LAYOUT-12 |
| AC 240 (:1618-1624) | An odd pair | LAYOUT-13 |
| AC 241 (:1625-1629) | A picked pair that is a side | LAYOUT-14 |
| AC 242 (:1630-1641) | Schema v11: a picked side stays put | INSTALL-8 (its `[Migrate]` line read as in AA 212) |
| AC 243 (:1642-1646) | No join dot | LAYOUT-16 |
| AC 244 (:1647-1654) | /am set with both point paths | LAYOUT-15 |
| AC 245 (:1655-1663) | /am diagnostics shows both points | DIAG-10 |
| AD 246 (:1669-1677) | An attached strip name is gray; its tooltip | CONT-9 |
| AD 247 (:1678-1683) | Named frame's two anchor points | LAYOUT-8 (with the older-build Bottom left / Top left container reading Top left on the left and Bottom left on the right) |
| AD 248 (:1684-1692) | A centered chain holds still with an empty middle link | LAYOUT-27 |
| AD 249 (:1693-1700) | Show all / Hide all on Dispel Types and Who Cast It | FILT-9 |
| AD 250 (:1701-1711) | The strip is never wider than its container | CONT-16 |
| AE 275 (:1722-1725) | Empty links locked and live | LAYOUT-28 |
| AE 276 (:1726-1729) | After an aura on a link expires | LAYOUT-28 |
| AE 277 (:1730-1732) | Empty links in combat | LAYOUT-29 |
| AE 278 (:1733-1739) | Populated links and the first aura | LAYOUT-30 |
| Settings redesign 251 (:1749-1750) | S1: the tree reads General, Containers, Profiles | PANEL-1 |
| Settings redesign 252 (:1751-1754) | S2: band on top, rail on the left, level with the tab art | PANEL-7 |
| Settings redesign 253 (:1755-1756) | S3: only the controls scroll | PANEL-8 |
| Settings redesign 254 (:1757-1759) | S4: the style entry follows the container | PANEL-11 |
| Settings redesign 255 (:1760-1761) | S5: each section keeps its tab | PANEL-12 |
| Settings redesign 256 (:1762-1764) | S6: section Defaults | PANEL-13 |
| Settings redesign 257 (:1765-1767) | S7: the frame picker reopens Layout | LAYOUT-6 |
| Settings redesign 258 (:1768-1770) | S8: the whole page is locked in combat | COMBAT-3 |
| Settings redesign 259 (:1771-1773) | S9: the first draw after a reload | PANEL-9 |
| Settings redesign 260 (:1774-1777) | S10: the rail's look and tooltips | PANEL-10 |
| Settings redesign 261 (:1778-1780) | S11: right-click lands on the last section | CONT-12 |
| Settings redesign 262 (:1781-1783) | S12: See spells lands on its category | FILT-10 |
| Settings redesign 263 (:1784-1787) | S13: no containers, then New container | PANEL-14 |
| Settings redesign 264 (:1788-1789) | S14: General Defaults keeps the name | PANEL-6 |
| Settings redesign 265 (:1790-1792) | S15: a rail entry in combat | COMBAT-5 |
| Settings redesign 266 (:1793-1796) | S16: other Ka0s addons' pages unchanged | PANEL-17 |
| Issues #21/#23 267 (:1805-1808) | I23-1: Preview color and bright cheat sheet | TEXT-24 |
| Issues #21/#23 268 (:1809-1811) | I23-2: Aura type tooltip wording | PANEL-19 |
| Issues #21/#23 269 (:1812-1814) | I23-3: the attached handle's tooltip line | CONT-9 |
| Issues #21/#23 270 (:1815-1819) | I23-4: no containers, no placeholder tab | PANEL-14 |
| Issues #21/#23 271 (:1820-1822) | I21-1: [Set] reset bars counts | DIAG-3 |
| Issues #21/#23 272 (:1823-1826) | I21-2: [Set] reset positions, the -0 case | DIAG-3 |
| Issues #21/#23 273 (:1827-1830) | I21-3: [Set] copy container; reset profile line | DIAG-3 |
| Issues #21/#23 274 (:1831-1833) | I21-4: /am get container and /am set container refused | SLASH-8 |
| New container 279 (:1840-1842) | NC1: New container lands on General | PANEL-15 (with Rail → Bars then reopening on Time text) |
| New container 280 (:1843-1846) | NC2: /am new moves an open page to General | PANEL-15 |
| Font primer 281 (:1859-1864) | FP1: cold cache at login | STYLE-20 |
| Font primer 282 (:1865-1868) | FP2: new auras after login | STYLE-21 |
| Font primer 283 (:1869-1872) | FP3: new auras in combat | STYLE-22 |
| Font primer 284 (:1873-1877) | FP4: a font change | STYLE-23 |
| Font primer 285 (:1878-1880) | FP5: reload with auras up | STYLE-24 |
| Font primer 286 (:1881-1884) | FP6: fonts primed in diagnostics | STYLE-25 |
| Font primer 287 (:1885-1888) | FP7: the primer debug line | STYLE-26 |
| Font primer 288 (:1889-1892) | FP8: while disabled | STYLE-27 |
| Font primer 289 (:1893-1900) | FP9: labels and literal text | STYLE-28 |
| Font primer 290 (:1901-1910) | FP10: the loading-screen gap | STYLE-29 |
| Font primer 291 (:1911-1917) | FP11: every font primed after a cold start | STYLE-30 |
| Mid-key reload 292 (:1924-1928) | MK1: reload inside a key | COMBAT-7 |
| Mid-key reload 293 (:1929-1935) | MK2: the event trace through a key | DIAG-11 |
| Mid-key reload 294 (:1936-1941) | MK3: the event trace at a boss | DIAG-12 |

## New checks with no old origin

| New ID | Why |
|---|---|
| PROFILE-5 | `/am profile` lists (S4: list) |
| PROFILE-6 | `/am profile <name>` switches, one `[Profile]` line, open page refreshes (S4: switch); the refresh step switches back to Default with the page open, since a second switch to the same profile prints "Already on profile" and never fires OnProfileChanged (libs/LibKa0s/Slash.lua:887-889) |
| PROFILE-7 | Already on the profile |
| PROFILE-8 | Unknown name refused, did-you-mean, nothing created (S4: unknown) |
| PROFILE-9 | Quotes and spaces (S4: quotes); each form starts from Default |
| PROFILE-11 | Refused in combat (S4: combat) |
| LOC-1, LOC-2 | The required `## Non-English client` section; AuraMaster had none and no doc-structure test pins its content |

PROFILE-10 (disabled) extends old 58's profile switch while disabled with the verb.

## Old content that was not a check

| Old location | What | Where it went |
|---|---|---|
| Header (:1-6) | Client, order, Lua errors, `[AM]` tag | Intro paragraph and Before you start |
| P preamble (:359-363) | Batch 5 design and notes pointers | dropped: historical (git keeps it) |
| Q preamble (:485-487) | Batch 6 priority revision summary | dropped: historical |
| R preamble (:592-594) | Why the launcher needs the client | dropped: covered by the intro |
| T, U preambles (:713-714, :867-870) | Per-batch container setup | Before you start and the TEXT lead-in |
| V preamble (:1031-1032) | Run 167-177 in order | FILT-31 says FILT-31 to FILT-39 run in order |
| W preamble (:1114-1121) | What cast-to-aura ids are | FILT-20 |
| Y preamble (:1188-1189) | Empty prediction lives in EmptyWatch | dropped: code pointer, not a step |
| Z, AA, AB, AC index and owner-run tables (:1219-1250, :1342-1368, :1479-1496, :1565-1586), AB/AC/AD/AE owner-run lines (:1558-1561, :1663, :1711, :1715-1717), settings redesign, #21/#23, NC owner-run lines (:1743-1747, :1800-1803, :1837-1838) | Historical sign-off batches | dropped per D4 (git keeps them); unsigned checks carried to Pending sign-off |
| AE setup and check line (:1715-1720) | The owner's chain and the bottom-printing `/run` line | LAYOUT-28 (generalized ids) |
| Font primer preamble (:1850-1857) | Font setup and "do not touch" rule | The lead-in before STYLE-20 |
| Mid-key preamble (:1921-1922) | Needs a restricted instance | Before you start (Place) |
| :1838 stray `#1` line | Formatting defect | fixed (gone) |
