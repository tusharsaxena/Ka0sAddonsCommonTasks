# ConsumableMaster smoke-test coverage map (SP-CM-03)

Old `docs/smoke-tests.md`: 816 lines, 310 checks (numbered steps, lettered steps, sub-steps and Degraded-install bullets); the table has 311 rows because §3d's seed caveat is mapped on its own row. New: 575 lines, 233 checks in 14 themes (INSTALL 6, SLASH 14, PANEL 31, PROFILE 21, STATE 9, MACRO 23, DISC 8, PRIO 30, BAR 30, LAUNCH 9, COMBAT 17, DIAG 27, DEGRADED 7, LOC 1), 7 of them new (PROFILE-15 – PROFILE-21, the `/cm profile` verb). No old check is dropped; every old check survives, alone or merged into a new check. Old line numbers are from `git show 7c56826:docs/smoke-tests.md`.

Non-check text: the intro and its "thirteen sections" claim (:1-10) became the new intro paragraph; "Working environment" (:12-17) became "Before you start"; the "Smoke, session N" label note (:34-40) is dropped (it policed labels the new file no longer uses); "Targeted by change area" (:767-816, 45 rows) is folded into the Index's "What it covers" column and the seam-file line under it; the per-section "Tests:" lines are folded into each check.

| Old location | Behavior | New ID |
|---|---|---|
| Quick smoke 1 (:23) | `/cm resync` invalidates, re-discovers, recomputes | MACRO-1 |
| Quick smoke 2 (:24) | `/cm dump pick <cat>` shows list, scores, pick | MACRO-1 |
| Quick smoke 3 (:25) | Macro body matches the dump's pick | MACRO-1 |
| Quick smoke 4 (:26) | For UI changes, exercise the page's widgets | merged into the intro (run the Index's theme for the code touched) |
| Quick smoke spec note (:28) | Spec-aware change: switch spec and repeat | MACRO-1 |
| §1 step 1 (:46) | Fresh-install path (delete SavedVariables) | INSTALL-1 (corrected: deletes `ConsumableMaster.lua`, the file the TOC's two SavedVariables live in; the old `ConsumableMasterDB.lua` never existed) |
| §1 step 2 (:47) | No Lua errors or stray warnings at login | INSTALL-1 |
| §1 step 3 (:48) | Exactly fifteen `KCM_*` macros | INSTALL-1 |
| §1 step 4 (:49) | Stored icons: pick texture or cooking pot, never `?` | INSTALL-1 |
| §1 step 5 (:50) | `/cm dump pick food` shows the post-PEW pipeline ran | INSTALL-1 |
| §1 step 6 (:51) | Re-login reuses macros, no duplicates | INSTALL-3 |
| §2 step 1 (:57) | Loot an unseeded item | DISC-1 |
| §2 step 2 (:58) | Dump lists it after `BAG_UPDATE_DELAYED` | DISC-1 |
| §2 step 3 (:59) | Macros tab shows it with the owned glyph | DISC-1 |
| §2 step 4 (:60) | Discovered item persists out of bags, red-X glyph | DISC-2 |
| §2 step 4b (:61-66) | Rows boxed full width, spaced, match MultiMeters, no drift | PRIO-13 |
| §2 step 5 (:67) | Stale discovery swept after 30 days | DISC-3 |
| §3 step 1 (:73) | Action bar shows the picked icon | MACRO-2 |
| §3 step 2 (:74) | Body is `/use item:` or `/cast` | MACRO-2 |
| §3 step 3 (:75) | Clicking the slot uses it | MACRO-2 |
| §3 step 4 (:76) | Blocking the pick moves to the next best | MACRO-3 |
| §3 step 5 (:77) | Empty category writes the empty-state stub | MACRO-4 (corrected: the stub's text differs by category, `defaults/Categories.lua`) |
| §3a step 1 (:83) | Bladed main hand picks a whetstone; tab markers | MACRO-5 |
| §3a step 2 (:84) | Swap to blunt re-picks without reload | MACRO-6 |
| §3a step 3 (:85) | Dual wield picks per hand, MH/OH markers | MACRO-7 |
| §3a step 4 (:86) | Two-hander writes slot 16 only | MACRO-8 |
| §3b step 1 (:92) | Augment Rune body is plain single-pick | MACRO-11 |
| §3b step 2 (:93) | Rune order by stat amount; reusable only wins ties | MACRO-11 |
| §3b step 3 (:94) | Block the top rune, falls back | MACRO-11 |
| §3b step 4 (:95) | Rune classifies from the Use line; unseeded self-adds | DISC-6 |
| §3b step 5 (:96) | Login tooltip race self-corrects | DISC-7 |
| §3c step 1 (:102-106) | Numeric classID/subClassID drives classification | DISC-4 |
| §3c step 2 (:107) | English picks unchanged | DISC-5 |
| §3c step 3 (:108) | Weapon affinity by subclass; oils-only ranged | MACRO-9 |
| §3c step 4 (:109) | Shield is not a polearm | MACRO-10 |
| §3c step 5 (:110) | Non-English client classifies correctly | LOC-1 |
| §3d intro caveat (:114) | Seed IDs unverified; VERIFY checklist link | MACRO-12 |
| §3d step 1 (:116) | Lust classes resolve their spell over drums | MACRO-12 |
| §3d step 2 (:117) | Hunter Harrier's Cry / Primal Rage via CLASS_GATE; no pet → empty | MACRO-13 |
| §3d step 3 (:118) | Drums resolve; capped drum filtered at max level | MACRO-14 |
| §3d step 4 (:119) | Rez classes resolve their spell; Soul Link fallback | MACRO-15 |
| §3d step 5 (:120) | Dump pick matches the lust and rez bodies | MACRO-15 |
| §3d step 6 (:121) | Cast on mouseover clause toggles | MACRO-16 |
| §3d step 7 (:122) | Lust and rez never auto-discover | DISC-8 |
| §4 step 1 (:128) | AIO Health tab section contents | PRIO-19 |
| §4 step 1b (:129-135) | Glyph key on AIO Health and AIO Mana | PRIO-20 |
| §4 step 2 (:136) | `KCM_HP_AIO` hover shows FOOD out of combat | MACRO-17 |
| §4 step 3 (:137) | `/cm dump pick hp_aio` per-section picks | MACRO-17 |
| §4 step 4 (:138-143) | Assembled castsequence body shape | MACRO-17 |
| §4 step 5 (:144) | Toggle HS off, castsequence drops it | PRIO-21 |
| §4 step 6 (:145) | Empty out-of-combat side emits `/run` fallback | MACRO-18 |
| §4 step 7 (:146) | Everything off falls to the empty stub | MACRO-18 |
| §5 step 1 (:152) | Note the flask pick | MACRO-19 |
| §5 step 2 (:153) | Switch spec in the talents UI | MACRO-19 |
| §5 step 3 (:154) | Spec-aware macros update, others do not | MACRO-19 |
| §5 step 4 (:155) | Stat Priority banner shows the new spec | PRIO-28 |
| §5 step 5 (:156) | Dump weighs stats by the new spec | MACRO-19 |
| §6 step 1 (:162) | Loot potions in combat | COMBAT-1 |
| §6 step 2 (:163) | Recompute runs, write queued | COMBAT-1 |
| §6 step 3 (:164) | Dump shows the pending pick in combat | COMBAT-1 |
| §6 step 4 (:165) | Regen flushes; body and icon update | COMBAT-1 |
| §6 step 5 (:166) | Re-entering combat keeps `"deferred"` | COMBAT-2 |
| §6 step 6 (:167) | Third failed attempt prints the give-up warning | COMBAT-3 |
| §6a step 1 (:175) | Category present out of combat (baseline) | COMBAT-5 |
| §6a step 2 (:176) | Pull a dummy | COMBAT-5 |
| §6a step 3 (:177) | `/reload` in combat | COMBAT-5 |
| §6a step 4 (:178) | Category absent in combat, no taint | COMBAT-5 |
| §6a step 5 (:179) | Category back after combat; `/cm config` opens it | COMBAT-5 |
| §6a step 6 (:180) | Same run disabled; `/cm config` gray refusal once in combat | COMBAT-6 (the in-combat `/cm config` refusal is back in the disabled run; COMBAT-7 is the enabled case, spelled out from step 4's pointer; corrected: the refusal is followed by the `config` verb's `Settings panel unavailable.`) |
| §7 step 1 (:188) | Close panel, `/cm config` | PANEL-1 |
| §7 step 2 (:189) | Lands on parent page; five sub-pages in order | PANEL-1 |
| §7 step 3 (:190) | `/cm config` re-expands a collapsed parent | PANEL-2 |
| §7 step 4 (:191) | General page two tabs, nine controls, Maintenance, Defaults | PANEL-6 (corrected: the Maintenance button reads `Force rewrite macros`, as `settings/General.lua` labels it) |
| §7 step 4a (:192) | Nothing declared twice; `macroBar.locked` ticks Lock frame | PANEL-7 |
| §7 step 4b (:193) | Master rows compose with the bar's own | PANEL-8 |
| §7 step 5 (:194) | Enable off stops everything; bar leaves at once | STATE-1 |
| §7 step 5a (:195) | Enable off in combat waits for regen | STATE-2 (corrected: `/cm disable` mid-fight, since the panel is under the combat cover) |
| §7 step 5b (:196) | Disabled through a reload registers nothing | STATE-3 |
| §7 step 5c (:197) | Profile switch into an enabled profile stands the addon up | PROFILE-14 (now sets up the disabled Default itself and ends with `/cm enable`, as old step 6 did) |
| §7 step 6 (:198) | Enable on: the checkbox tick prints nothing; re-registers; bar only if still ticked | STATE-5 |
| §7 step 7 (:199) | Debug toggle ack, console lines, `[Init]` | DIAG-1 (driven by `/cm debug on`/`off` and the console header's toggle: General's **Debug console** row only shows or hides the window, `settings/General.lua:225-245`, and has its own check, DIAG-8) |
| §7 step 8 (:200) | Force resync; blocked in combat | PANEL-9 (corrected: `/cm resync` in combat recomputes with a notice, `settings/Slash.lua:227-230`; the button is covered) |
| §7 step 9 (:201) | Force rewrite macros re-issues every body | PANEL-10 (the button's label `Force rewrite macros` kept, as the old step had it) |
| §7 step 10 (:202) | Reset all settings tooltip, popup, effect, combat refusal | PANEL-11 (corrected: the tooltip spells `->`, `libs/LibKa0s/Options.lua:252-254`; the combat Yes goes through the raised popup) |
| §7 step 10a, first (:203) | Reset closes the debug console session row | PANEL-13 |
| §7 step 10b (:204) | Reset all priorities, narrower popup; combat refusal | PANEL-14 (corrected: the combat case is the popup's Yes in combat, `settings/General.lua:125-127`) |
| §7 step 10a, second (:205) | `/cm resetall` raises the same popup; Cancel (the popup's button is No: PANEL-12 names No or Escape); bare `/cm reset` usage; one-row reset | PANEL-12 (the `/cm reset` half: SLASH-5) |
| §7 step 11 (:206) | General page Defaults resets this page only; combat refusal | PANEL-15 (combat: PANEL-17) |
| §7c step 1 (:212) | Minimap button wears the logo; AddOns list icon | LAUNCH-1 |
| §7c step 2 (:217) | Left-click opens settings, lock untouched | LAUNCH-2 |
| §7c step 3 (:220-230) | Right-click menu, Locked and Enabled entries, four doors, grayed Locked when disabled | LAUNCH-3 (four doors: STATE-6; grayed entry: LAUNCH-4) |
| §7c step 4 (:231) | Dragged position survives reload | LAUNCH-5 |
| §7c step 5 (:234) | Minimap button row; `global.minimap.shown` get/set; `hide` not found | LAUNCH-6 |
| §7c step 6 (:240) | Button visibility is installation-wide across profiles | LAUNCH-6 (PROFILE-13 no longer repeats it) |
| §7c step 7 (:242) | No reset brings the button back | LAUNCH-7 |
| §7c step 8 (:252) | Broker plugin, same object | LAUNCH-8 |
| §7c step 9 (:256) | Status tooltip lines, flip, disabled | LAUNCH-9 |
| §7a setup + step 1 (:268-270) | No freeze on a mutation with many pages built | PANEL-19 |
| §7a step 2 (:271) | Off-screen page rebuilt on show | PANEL-20 |
| §7a step 3 (:272) | Defaults button is AceGUI dark/gold, still resets | PANEL-16 |
| §7a step 4.1 (:278) | First-open item storm fills once | PANEL-30 (pending) |
| §7a step 4.2 (:279) | Refresh cap under constant traffic | PANEL-31 (pending) |
| §7a step 4.3 (:280) | Each rebuild is a single hitch | PANEL-30 and PANEL-31 (pending) |
| §7b console step 1 (:288) | First open raises nothing; header; Esc closes | DIAG-3 |
| §7b console step 2 (:289) | Line counter climbs; Clear resets it | DIAG-4 |
| §7b console step 3 (:290) | Scrollbar always shown, inert when it fits | DIAG-5 |
| §7b console step 4 (:291) | Wheel and thumb stay in sync | DIAG-6 |
| §7b console step 5 (:292) | Thumb direction: top oldest | DIAG-6 |
| §7b console step 6 (:293) | Log caps at 3000; Copy holds newest | DIAG-7 |
| §7d step 1 (:299) | Report appends below the trace, markers, chat line | DIAG-11 |
| §7d step 2 (:300) | Report sections in order | DIAG-12 |
| §7d step 3 (:301) | Report is read-only | DIAG-13 |
| §7d step 4 (:302) | Report with logging off | DIAG-14 |
| §7d step 5 (:303) | Report opens a hidden console | DIAG-15 |
| §7d step 6 (:304) | Other spellings and the long alias | DIAG-16 |
| §7d step 7 (:305) | No short alias; `/cm diag` unknown | DIAG-17 (corrected: `Unknown command: diag`) |
| §7d step 8 (:306) | Report while disabled | DIAG-18 |
| §7d step 9 (:307) | Report in combat, secret values | DIAG-19 |
| §7d step 10 (:308) | Copy is clean | DIAG-20 |
| §7b tabs step 1 (:318) | Macros strip pinned, fifteen full-name tabs | PANEL-24 |
| §7b tabs step 2 (:323) | Food selected on open; body contents | PANEL-24 |
| §7b tabs step 3 (:325) | Battle Rez checkbox appears and goes | PANEL-25 |
| §7b tabs step 4 (:328) | Scroll does not carry across a tab switch | PANEL-26 |
| §7b tabs step 5 (:331) | Strip wraps with the window, first draw correct | PANEL-27 |
| §7b tabs step 6 (:335) | Per-tab Defaults names the tab | PRIO-16 |
| §7b tabs step 7 (:338) | Tab click works in combat | COMBAT-8 (corrected: since the Options combat lock, an open page is covered in combat and a tab click does nothing, `libs/LibKa0s/Options.lua:336-346`, `OptionsCombat.lua:205-217`) |
| §7b tabs step 8 (:344) | Macro Bar's eight tabs in order | BAR-1 |
| §7b tabs step 9 (:347) | Only the active tab's controls, no repeated heading | BAR-1 |
| §7b tabs step 10 (:349) | Row counts per tab | BAR-2 |
| §7b tabs step 11 (:354) | Bar opacity once under Opacity | BAR-3 |
| §7b tabs step 11a (:357) | Subsection headings on mixed tabs | BAR-3 |
| §7b tabs step 11b (:362) | Use class color beside all seven swatches | BAR-4 |
| §7b tabs step 11c (:366) | Border block order | BAR-4 |
| §7b tabs step 12 (:370) | Labels tab layout, font, flags, shadow, v3 carry-over | BAR-13 (v3 carry-over: INSTALL-5) |
| §7b tabs step 13 (:377) | Tab switch keeps the slider value | BAR-5 |
| §7b tabs step 14 (:383) | Stat Priority banner above the scroll, labeled | PRIO-28 |
| §7b tabs step 15 (:386) | No Selection section, no second picker; spec sentence on Macros | PRIO-28 |
| §7b tabs step 16 (:389) | Banner pick drives Macros spec-aware tabs | PRIO-29 |
| §7b tabs step 17 (:392) | Banner dropdown not clipped | PRIO-28 |
| §7b tabs step 18 (:394) | Stat Priority one-tab strip | PRIO-28 |
| §7b tabs step 19 (:401) | General two-tab strip | PANEL-6 |
| §7b tabs step 20 (:403) | Profiles page has no strip | PROFILE-1 |
| §7b tabs step 21 (:407) | Wrapped strip does not move on click | PANEL-28 |
| §8 step 1 (:418) | Banner, full-width spec dropdown, sorted specs, one-tab strip | PRIO-28 |
| §8 step 1a (:419) | Strip drawn with no spec; "No spec selected" inside | PRIO-28 |
| §8 step 2 (:420) | Picking a spec repopulates fields | PRIO-29 |
| §8 step 3 (:421) | Flask tab follows the viewed spec | PRIO-29 |
| §8 step 4 (:422) | Primary stat full width, commits | PRIO-30 |
| §8 step 5 (:423-435) | Secondaries list: rows, drag, dimmed block, tick/cross, pooled handler | PRIO-30 (box look: PRIO-13) |
| §8 step 5a (:436) | Re-render leaves no stray handle or box | PRIO-12 |
| §8 step 6 (:437) | Reset stat priority and Defaults | PRIO-30 |
| §9 step 1 (:443) | Open a single-category tab | PRIO-1 |
| §9 step 2 (:444) | Drag icon places the macro | PRIO-1 |
| §9 step 2, in-combat bullet (:445) | Drag refused in combat | COMBAT-9 (corrected: the Macros tab's icon is under the combat cover, so the check drags a bar slot) |
| §9 step 3 (:446) | Add by ID, item | PRIO-2 |
| §9 step 4 (:447) | Add by ID, spell; non-Rogue refusal | PRIO-3 (corrected: a spell the class cannot cast is added with a chat line since `5d69177`, `settings/CategoryAddByID.lua:291-311`; the status-line refusal is checked with an unknown ID) |
| §9 step 5 (:448) | Add by name (a potion you carry, removed with × first); a ×-removed item no longer resolves unless carried; refusal wording; lookup wait, even for an item you carry | PRIO-4 |
| §9 step 5a (:449) | Suggestions while typing; Type→Spell redraws, keeps the text, picking a subtext spell adds it | PRIO-5 |
| §9 step 5b (:450) | Name submitted while items load | PRIO-6 |
| §9 step 6 (:451) | Refused add keeps text; legend intact | PRIO-7 |
| §9 step 7 (:452) | Drag shows copy, fade, gold line; drop pins | PRIO-8 |
| §9 step 7, several-rows bullet (:453) | A long drag is one move | PRIO-9 |
| §9 step 7, drop-back bullet (:454) | Drop in place writes nothing | PRIO-9 |
| §9 step 7, scroll bullet (:455) | A drag keeps the scroll | PRIO-11 |
| §9 step 7, handle-only bullet (:456) | Only the handle drags | PRIO-10 |
| §9 step 7, stray-handle bullet (:457) | No stray handles after drag or Defaults | PRIO-12 |
| §9 step 8 (:458) | Info button score tooltip matches dump | PRIO-14 |
| §9 step 9 (:459) | × removes and blocks | PRIO-15 |
| §9 step 10 (:460) | Reset category and Defaults | PRIO-16 |
| §9 step 11 (:461) | Spec-aware tabs edit the viewed spec | PRIO-17 |
| §9 step 11, no-spec bullet (:462) | No active spec refuses a spec-aware add | PRIO-18 |
| §9a step 1 (:469) | Drag looks identical to MultiMeters | PRIO-13 |
| §9a step 2 (:473) | MultiMeters' divide stops the line; none here | PRIO-13 |
| §9a step 3.1 (:494) | Gold insertion line on all four lists | PRIO-25 (pending) |
| §9a step 3.2 (:496) | Drop commits once on all four lists | PRIO-25 (pending) |
| §9a step 3.3 (:498) | Cancel mid-drag leaves nothing | PRIO-25 (pending) |
| §9a step 3.4 (:503) | Row hover works after a drag | PRIO-26 (pending) |
| §9a step 3, two pages (:508) | Two lists, one line each | PRIO-27 (pending) |
| §10 step 1 (:517) | Open AIO Health | PRIO-19 |
| §10 step 2 (:518) | Composite rows: handle, row, Enabled; no arrows; boxed | PRIO-19 |
| §10 step 3 (:519) | Enabled toggle recomputes | PRIO-21 |
| §10 step 4 (:520) | Composite drag is one write | PRIO-22 |
| §10 step 5 (:521) | Drag cannot cross sections | PRIO-23 |
| §10 step 5a (:522) | Re-render leaves nothing on either section | PRIO-12 |
| §10 step 6 (:523) | Composite Reset category and Defaults | PRIO-24 |
| §11 step 1 (:529) | Bare `/cm` opens the panel | SLASH-1 |
| §11 step 2 (:530) | `/cm help` lists every COMMANDS entry | PANEL-4 (help against About); every-entry is also `tests/test_slash.lua` |
| §11 step 3 (:531) | `/cm config` opens the panel | PANEL-1 |
| §11 step 4 (:532) | `/cm version` prints the version | INSTALL-6 |
| §11 step 5 (:533) | `/cm debug` toggles; checkbox flips | DIAG-1 (`/cm debug on`/`off` arm logging) and DIAG-2 (bare `/cm debug` toggles the window and the **Debug console** box follows it; see also DIAG-8) |
| §11 step 5a (:534) | `/cm diagnostics` and `/cm debug diagnostics` | DIAG-16 |
| §11 step 6 (:535) | resync / rewritemacros / resetall; bare reset; one-row reset | SLASH-5 (resync: PANEL-9; rewritemacros: PANEL-10; resetall: PANEL-12) |
| §11 step 7 (:536) | `/cm list` grouping | SLASH-3 (corrected: `[statpriority]` prints before `[macros]`) |
| §11 step 8 (:537) | `/cm get` single row | SLASH-4 |
| §11 step 9 (:538) | `/cm set enabled false`; type validation | SLASH-4 (corrected: `Invalid value for enabled` then the library's `expected true/false/on/off/1/0/yes/no`; the host's shorter ERR_BOOL is dead, `settings/Slash.lua:446-452`) |
| §11 step 9b (:539) | Whole-value rows; one `[Set]` per panel write | SLASH-6 (the `[Set]` half: SLASH-7) |
| §11 step 10 (:540) | `/cm priority … list` | SLASH-8 |
| §11 step 11 (:541) | `/cm priority` add/remove/up/down/reset | SLASH-8 |
| §11 step 12 (:542) | `s:<spellID>` sentinel | SLASH-8 |
| §11 step 13 (:543) | `/cm stat` verbs | SLASH-9 |
| §11 step 14 (:544) | `/cm aio` verbs | SLASH-10 |
| §11 step 14a (:545) | Disabled addon refuses feature verbs | SLASH-13 |
| §11 step 14b (:554) | The rest answers while disabled; typo gets unknown | SLASH-14 (corrected: the typo line is the host's `Unknown command: resyncc`, `settings/Slash.lua:429`) |
| §11 step 14c (:562) | Launcher while disabled | LAUNCH-2 (left-click) and LAUNCH-4 (menu) |
| §11 step 15 (:568) | `/cm dump categories` | SLASH-11 |
| §11 step 16 (:569) | `/cm dump statpriority` | SLASH-11 |
| §11 step 17 (:570) | `/cm dump bags` | SLASH-11 |
| §11 step 18 (:571) | `/cm dump item` | SLASH-11 |
| §11 step 19 (:572) | `/cm dump pick`, composite bodies | SLASH-11 |
| §11 step 19b (:573) | `/cm dump events`; no rejected clause in `[Init]` | SLASH-12 |
| §11a step 1 (:579) | Fresh install bar, tooltips incl. AIO, checkbox states | INSTALL-2 |
| §11a step 1a (:580) | Upgrade path: v2 step once per profile | INSTALL-4 (corrected: edits the live SavedVariables file) |
| §11a step 1b (:581) | v3 label-flags conversion keeps the choice | INSTALL-5 (corrected: edits the live SavedVariables file) |
| §11a step 2 (:583) | Enable macro bar off and on | BAR-7 |
| §11a step 3 (:584) | Slot click in and out of combat, key-down both values | BAR-8 |
| §11a step 4 (:585) | Move via handle, tooltips, help mark, lock | BAR-9 |
| §11a step 4a (:586) | The lock's four doors; handle names the short form | STATE-6 (the handle clause is rewritten: the old step hovered the handle while locked, but the handle is hidden then, `modules/MacroBar.lua:343`; STATE-6 hovers the help mark while unlocked and expects the footer to name `/cm lock`, `modules/MacroBar.lua:245-250`) |
| §11a step 4b (:587) | Unlock refused while disabled | STATE-7 |
| §11a step 4c (:588) | Unlocking a switched-off bar says so; grayed menu when disabled | STATE-8 (menu while disabled: LAUNCH-4) |
| §11a step 4d (:589) | Handle close mark X, in and out of combat | BAR-10 |
| §11a step 5 (:590) | Layout | BAR-11 |
| §11a step 6 (:591) | Bar and button appearance; LSM dropdown flush; run 19 too | BAR-12 (routes to BAR-28) |
| §11a step 6a (:592) | Labels, font block, font preload, shadow, class color | BAR-13 |
| §11a step 7 (:593) | Cooldown swipe and numbers | BAR-14 |
| §11a step 7a (:594) | Restricted spell cooldown in combat | COMBAT-10 |
| §11a step 8 (:595) | Reorder by drag on the bar; Reset slot order | BAR-15 |
| §11a step 8a (:596) | Reorder on the Buttons tab | BAR-16 (its `[Set]` lines: SLASH-7) |
| §11a step 9 (:597) | Drag out to a Blizzard bar | BAR-17 |
| §11a step 10 (:598) | CM-only: nothing drags in | BAR-17 |
| §11a step 11 (:599) | Which macros show; untick all fifteen | BAR-18 |
| §11a step 11b (:600) | Flyout band, strip, settings (incl. Flyout button size, Flyout spacing, Gap from button) | BAR-19 |
| §11a step 11e (:601) | Flyout closing, combat close, stand-down re-arm | BAR-20 (combat: COMBAT-11; stand-down: STATE-9) |
| §11a step 11c (:602) | Flyout on AIO and Weapon Enchant | BAR-21 |
| §11a step 11d (:603) | Flyout in combat | COMBAT-11 |
| §11a step 12 (:604) | Combat visibility | COMBAT-12 |
| §11a step 13 (:605) | Fade unless hovered | BAR-22 |
| §11a step 14 (:606) | Bar changes in combat deferred; Buttons tab refusal | COMBAT-13 (corrected: the in-combat changes are made from chat; the Buttons tab is under the combat cover, so its refusal line cannot be reached) |
| §11a step 15 (:607) | `/cm bar` sub-verbs; set buttonSize; reject orientation | BAR-23 |
| §11a step 16 (:608) | Macro Bar page Defaults and its `[Set]` lines | BAR-24 (General Defaults line: PANEL-15; Reset all settings line: PANEL-13 and PROFILE-9) |
| §12 step 1 (:614) | Oversized body falls back | MACRO-20 |
| §12 step 2 (:615) | Locked bag item does not flap | MACRO-21 |
| §12 step 3 (:616) | Renamed macro left alone | MACRO-22 |
| §12 step 4 (:617) | Full macro pool fails gracefully | MACRO-23 |
| §12 step 5 (:618) | Master enable persists across relog | STATE-4 |
| §12 step 6 (:619) | Bar with a full macro pool | BAR-25 |
| §12 step 7 (:620) | `/reload` mid-pending drops the queue | COMBAT-4 |
| §13 step 1 (:628) | `/cm debug on` | PROFILE-1 (setup) |
| §13 step 2 (:629) | Create and switch to a new profile | PROFILE-2 |
| §13 step 3 (:630) | Migration line on the new profile | PROFILE-2 |
| §13 step 4 (:631) | Switch back: silent, nothing lost | PROFILE-5 |
| §13 step 5 (:632) | Every visited profile stamped 3 | PROFILE-5 (corrected: reads the live file) |
| §13 step 6 (:633) | v2 one-time cost; bar stays off afterward | PROFILE-6 |
| §13a step 1 (:641) | Profiles page inside the canvas; no Defaults, no strip | PROFILE-1 |
| §13a step 2 (:642) | New profile: `[Profile]`, `[DB]`, `[Macro]` lines, no `[Set]` | PROFILE-2 |
| §13a step 3 (:643) | Make Alt different | PROFILE-3 |
| §13a step 4 (:644) | Switch back moves everything without reload | PROFILE-3 |
| §13a step 5 (:645) | Round trip rewrites the macros (fingerprints) | PROFILE-4 |
| §13a step 6 (:646) | Bar off in one profile | PROFILE-7 |
| §13a step 7 (:647) | Copy | PROFILE-8 |
| §13a step 8 (:648) | Reset Profile and Reset all settings are one act | PROFILE-9 |
| §13a step 9 (:649) | Delete | PROFILE-10 |
| §13a step 10 (:650) | Open page follows a switch made elsewhere (now via `/cm profile Alt` instead of `/run … SetProfile`) | PROFILE-11 |
| §13a step 11 (:651) | Switch in combat through AceDB | PROFILE-12 |
| §13a step 12 (:652) | Console state and perf runs stay out | PROFILE-13 (the minimap clause the rewrite added is LAUNCH-6's) |
| Seam step 1 (:660) | Chat tag on every line | SLASH-2 |
| Seam step 2 (:661) | Panel opens on About; header and divider | PANEL-1 |
| Seam step 3 (:662) | Breadcrumb | PANEL-3 |
| Seam step 4 (:663) | Defaults is the AceGUI button on every page | PANEL-16 |
| Seam step 5 (:664) | Defaults works; refuses in combat | PANEL-17 (works: PANEL-15; corrected: Defaults is under the combat cover) |
| Seam step 6 (:665) | Section spacing | PANEL-23 |
| Seam step 7 (:666) | Scrollbar always visible | PANEL-22 |
| Seam step 8 (:667) | Live slider preview | BAR-6 |
| Seam step 9 (:668) | Two-tier refresh | PANEL-21 |
| Seam step 10 (:669) | Console opens, header, line order, Copy/Clear/counter | DIAG-1 (Copy, Clear, counter: DIAG-4) |
| Seam step 10a (:670) | Shared window edge on console and perf panel | DIAG-9 |
| Seam step 11 (:671) | Console checkbox sync on Esc and close | DIAG-8 |
| Seam step 12 (:672) | Bare `/cm debug` toggles the window only | DIAG-2 |
| Seam step 13 (:673) | No raw locale key renders | PANEL-5 |
| Seam step 14 (:674) | Settings window footer Defaults | PANEL-18 |
| Seam step 15 (:675) | About list matches `/cm help` | PANEL-4 |
| Seam step 15a (:677-685) | The collection's marks on console, handle, perf panel | DIAG-10 |
| Seam step 16 (:687) | TOC version and About notes | INSTALL-6 |
| Seam step 17.1 (:693) | Composed media dropdowns populated | BAR-26 (pending) |
| Seam step 17.2 (:694) | Picking a value applies it | BAR-26 (pending) |
| Seam step 17.3 (:695) | `/dump LibStub("LibKa0s-Options-1.0").MODULES.OptionsCompose` proves the live client loaded the vendored payload | BAR-26 (pending); made evergreen: the expected value is now "at least the `COMPOSE_MINOR` in `libs/LibKa0s/OptionsCompose.lua`" (7 at LibKa0s v1.63.0, `:28`) instead of the stale 3 |
| Seam step 17.4 (:696) | `/cm set` border style validated | BAR-27 (pending; corrected: values unquoted, since a quoted value is refused) |
| Seam step 18 (:698-702) | Tab strip survives pooling on all four strips | PANEL-29 (pending) |
| Seam step 19 (:704-716) | Border dropdown flush with five Ka0s addons, load-order independent | BAR-28 (pending) |
| Seam step 20.1 (:724) | Bar backdrop color round trip in the picker | BAR-29 (pending) |
| Seam step 20.2 (:725) | `/cm get` matches the picker, survives reload | BAR-29 (pending) |
| Seam step 20.3 (:726) | Repeat for the other four swatches | BAR-29 (pending) |
| Seam step 20.4 (:727-729) | Absent color channels draw; both surfaces agree | BAR-30 (pending) |
| Seam step 20.5 (:730) | Restore the file afterward | BAR-30 (pending) |
| Perf step 1 (:736) | Seven-step panel opens | DIAG-21 |
| Perf step 2 (:737) | Arm A with the Stopwatch | DIAG-22 |
| Perf step 3 (:738) | Arm B suspends the addon | DIAG-23 |
| Perf step 4 (:739) | Finish restores; report; dump | DIAG-24 |
| Perf step 5 (:740) | Capture reaches SavedVariables | DIAG-25 |
| Perf step 6 (:741) | Cancel restores the addon | DIAG-26 |
| Perf step 7 (:742) | Perf strings read US English | DIAG-27 (pending) |
| Degraded bullet 1 (:748) | Loads; macros work; list/get/set | DEGRADED-1 (corrected: list, get and set print the library-absent notice and change nothing) |
| Degraded bullet 2 (:749) | Absent from the AddOns list | DEGRADED-2 |
| Degraded bullet 3 (:750) | `/cm config` explains once | DEGRADED-3 (corrected: the notice prints once during the `/reload`, from the settings bootstrap's `registerPanel` at `PLAYER_LOGIN`, and every `/cm config` prints only `Settings panel unavailable.`) |
| Degraded bullet 4 (:751) | Debug logging routes to chat | DEGRADED-4 |
| Degraded bullet 5 (:752) | enable/lock/bar lock refuse; bar on/off work | DEGRADED-5 (now with `/cm profile`) |
| Degraded bullet 6 (:753) | Version and About notes survive | DEGRADED-6 |
| Degraded bullet 7 (:754) | Chrome loses its art, help control still drawn | DEGRADED-7 |
| Mid-key step 1 (:762) | Mid-key reload does not blank the macros | COMBAT-14 (pending) |
| Mid-key step 2 (:763) | Restriction trace through a key | COMBAT-15 (pending) |
| Mid-key step 3 (:764) | Restriction trace at any boss | COMBAT-16 (pending) |
| Mid-key step 4 (:765) | Equipment and spec event trace | COMBAT-17 (pending) |

New checks with no old counterpart: PROFILE-15 (`/cm profile` lists), PROFILE-16 (switch), PROFILE-17 (already current), PROFILE-18 (unknown name refused, never created), PROFILE-19 (quotes, case, spaces), PROFILE-20 (verb live while disabled, switch stands the addon up), PROFILE-21 (verb refused in combat). DEGRADED-5 gained the `/cm profile` library-absent line, SLASH-14 lists `/cm profile` among the verbs that answer while disabled, and PROFILE-11 makes its switch through `/cm profile Alt`.

Pending sign-off (the 2026-09-29 clarification of S4) lists, with origin and reason: (a) the carried-over checks the old doc marked "Not yet run" (PANEL-29 – PANEL-31, PRIO-25 – PRIO-27, BAR-26 – BAR-30, COMBAT-14 – COMBAT-17, DIAG-27) and the ones left on an owed list with no later pass: batch 5 (2026-09-13, memory `ka0s-batch5-2026-09-13`: "CM §9 5a/5b") → PRIO-5, PRIO-6; the 2026-09-12 triage batch (`AuraMaster/_dev/triage-2026-09-12/FINAL_REPORT_DRAFT.md:55-57`: "CM Macro Bar steps 9b/16; bulk-reset one-line logging") → SLASH-6, SLASH-7, BAR-24 and the one-line checks PANEL-13, PANEL-15, PROFILE-8, PROFILE-9; the 2026-09-07 remediation's owed checklist (`2026-09-07-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/08_SMOKE_CHECKLIST.md:4-9`, "Nothing below has been run", no later run recorded) → COMBAT-5 (§1.2, `M2-08`), PROFILE-6 (§5.2 step 5, `M2-07`) and LOC-1 (§6.7, Session 6); Session CM of the 2026-09-23 remediation (`2026-09-23-REVIEW_AND_STANDARDS_AUDIT_REMEDIATION/06_SMOKE_TESTS.md:1168-1278`, under the file's "Nothing below has been performed" and `RESUME.md` §5's "Still the owner's", with no CM step recorded) → LAUNCH-6 (CM.1, CM.2, `CM-19`), PANEL-1 (CM.3, `CM-21`), SLASH-12 (CM.4, `CM-15`), STATE-8 (CM.5, `CM-09`: the bar-off unlock line; the step's left-click half was replaced by the M5/M6 launcher, whose left-click opens settings, recorded PASS under X1.4), BAR-23 (CM.6's enum refusal, `CM-17`; X1.3's ConsumableMaster enum row was never recorded either, its record names only `/bl` and `/mm`), PANEL-10, PANEL-27, PANEL-28 and BAR-16 (CM.8, `CM-20`: Maintenance's buttons, the strips at the narrowest width, the Buttons-tab reorder), PANEL-12 (CM.10, `CM-11`), STATE-9 (CM.12, `CM-06`) and COMBAT-5 (CM.13's enabled run, `CM-05`). The rest of Session CM already lands on pending checks: CM.6 on PANEL-15, BAR-24 and SLASH-7; CM.7 on BAR-29; CM.8's Master controls and tab switch mid-drag on PANEL-6 and PRIO-25; CM.9 on PRIO-25 – PRIO-27; CM.10's panel button on PANEL-11; CM.13's disabled run and in-combat refusal on COMBAT-6 and COMBAT-7; CM.14 on PROFILE-5; X2.8 (`CM-18`) on DEGRADED-5. CM.11 (`CM-04`, a combat-deferred `/cm rewritemacros` keeping both hands' lines) had no step in the old doc, so no new check carries it; (b) every check new in this run (PROFILE-11, PROFILE-15 – PROFILE-21, SLASH-14, DEGRADED-5) and every check whose steps or expectation were corrected against the code (INSTALL-1, INSTALL-4, INSTALL-5, SLASH-3, SLASH-4, PANEL-6, PANEL-9, PANEL-11, PANEL-14, PANEL-17, PROFILE-2, PROFILE-5, STATE-2, STATE-6, MACRO-4, PRIO-3, PRIO-12, BAR-26, BAR-27, BAR-30, COMBAT-6, COMBAT-7, COMBAT-8, COMBAT-9, COMBAT-13, DIAG-1, DIAG-17, DEGRADED-1, DEGRADED-3). Wording-only fixes that leave the expectation unchanged (MACRO-10 and DISC-4 split `classID=` / `subClassID=` because the dump prints two spaces between them) and restored clauses of passed checks (PANEL-10's button label, PRIO-4, PRIO-28, BAR-12, PROFILE-14) are not pending.

`/cm config` in combat prints two lines: the library's refusal (`libs/LibKa0s/OptionsRegistry.lua:250-254`, through the host's tagged printer), then the host's `Settings panel unavailable.` (`settings/Slash.lua:167-171`; `KCM.Options.Open` answers false on the library's refusal, `settings/OptionsShim.lua:198-201`). COMBAT-6 and COMBAT-7 state both lines, since the smoke suite describes what the code does. If the second line is judged a defect in the `config` verb, the fix changes both checks with it.

DEGRADED-3 follows the code's order, which `tests/test_settingsui.lua:421-436` pins: with the library absent the settings bootstrap calls `registerPanel` at `PLAYER_LOGIN` (`settings/Panel.lua:1156-1166`), whose library-absent arm says the panel notice (`settings/Panel.lua:1131-1133`), once per session (`announcedMissing`, `settings/Panel.lua:349-363`). So the notice prints during the section's `/reload`, and every later `/cm config` reaches `KCM.Options.Open` with the flag already set and prints only `Settings panel unavailable.`.
